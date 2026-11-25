"""Read-only material extraction with stable, source-local evidence locations.

This module neither executes uploaded content nor reads links/external references.
The project service owns source identities, revisions, storage and proposals.
"""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import io
import json
import posixpath
import re
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile


MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_EXPANDED_BYTES = 128 * 1024 * 1024
MAX_XML_PARTS = 10000
MAX_SHEET_CELLS = 100000
PARSER_VERSION = "1.0"
_NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
       "p": "http://schemas.openxmlformats.org/package/2006/relationships",
       "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _result(fmt, status="complete", warnings=None, structure=None):
    return {"format": fmt, "status": status, "fragments": [], "warnings": warnings or [],
            "structure": {"parser_version": PARSER_VERSION, **(structure or {})}}


def _warn(result, message):
    if message not in result["warnings"]:
        result["warnings"].append(message)


def _fragment(result, location, text):
    text = str(text)
    payload = json.dumps([location, text], ensure_ascii=False, sort_keys=True).encode("utf-8")
    fid = "f_" + hashlib.sha256(payload).hexdigest()[:24]
    result["fragments"].append({"id": fid, "location": location, "text": text})
    return fid


def _finish(result, *, no_text="failed"):
    if not any(f['text'].strip() for f in result["fragments"]):
        result["status"] = no_text
        _warn(result, "未取得可用文本；请检查所选范围，或提供可复制的文字版本后重试。")
    elif result["warnings"]:
        result["status"] = "partial"
    return result


def _decode(content, options):
    encoding = options.get("encoding", "utf-8-sig")
    if encoding not in {"utf-8", "utf-8-sig", "utf-16", "gb18030"}:
        raise ValueError("文本编码仅支持 UTF-8、UTF-16 或 GB18030；请转换文件或选择对应编码。")
    if "encoding" not in options and content.startswith((b"\xff\xfe", b"\xfe\xff")):
        encoding = "utf-16"
    try:
        text = content.decode(encoding)
    except UnicodeError as exc:
        raise ValueError("文件不能按所选编码读取；请转存 UTF-8，或明确选择 UTF-16/GB18030 后重试。") from exc
    if "\x00" in text:
        raise ValueError("文件含二进制空字节，不能作为文本解析；请核对文件格式和编码。")
    return text


def _text(content, options, fmt):
    text = _decode(content, options)
    result = _result(fmt)
    lines = text.splitlines()
    headings, paragraph, start, paragraph_length = [], [], 1, 0

    def flush(end):
        nonlocal paragraph, paragraph_length
        if paragraph:
            _fragment(result, {"type": "text", "line_start": start, "line_end": end,
                               "headings": list(headings)}, "\n".join(paragraph))
            paragraph = []
            paragraph_length = 0

    fenced = False
    for i, line in enumerate(lines, 1):
        if fmt == "markdown" and re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
        heading = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line) if fmt == "markdown" and not fenced else None
        if heading:
            flush(i - 1)
            level, title = len(heading.group(1)), heading.group(2)
            headings[:] = headings[:level - 1] + [title]
        if not line.strip():
            flush(i - 1)
        else:
            if not paragraph:
                start = i
            paragraph.append(line)
            paragraph_length += len(line)
            if paragraph_length > 8000:
                flush(i)
    flush(len(lines))
    result["structure"]["line_count"] = len(lines)
    return _finish(result)


_COMMON_TABLE_OPTION = re.compile(
    r"(?<!\S)(ENGINE|(?:DEFAULT\s+)?(?:CHARSET|CHARACTER\s+SET)|COLLATE|ROW_FORMAT)"
    r"\s*=?\s*([\w-]+)(?=\s|$)|(?<!\S)(AUTO_INCREMENT)\s*=\s*\d+(?=\s|$)",
    re.I)
_EXPORT_SET = re.compile(
    r"SET\s+(?:(?:SESSION\s+)?FOREIGN_KEY_CHECKS\s*=\s*[01]|"
    r"NAMES\s+[\w-]+(?:\s+COLLATE\s+[\w-]+)?)", re.I)


def _ddl(content, options, progress=None):
    from scripts.ingest_ddl import CREATE_RE, COMMENT_RE, extract_table_bodies, qualified_identifier, mask_quoted, parse_sql, split_columns, strip_comments, QUALIFIED_IDENTIFIER
    text = _decode(content, options)
    clean = strip_comments(text)
    result = _result("ddl", structure={"tables": [], "relationships": []})
    common_options = {}
    routine_declarations = Counter()
    index_counts = Counter()
    export_drop = re.compile(r'DROP\s+TABLE\s+IF\s+EXISTS\s+' + QUALIFIED_IDENTIFIER, re.I)
    starts, start, quoted, i = [], 0, None, 0
    while i < len(clean):
        c = clean[i]
        if quoted:
            if c == "\\" and quoted in {"'", '"', '`'}:
                i += 2
                continue
            if c == quoted:
                if i + 1 < len(clean) and clean[i + 1] == quoted:
                    i += 1
                else:
                    quoted = None
        elif c in "'\"`[":
            quoted = ']' if c == '[' else c
        elif c == ';':
            starts.append((start, i + 1))
            start = i + 1
        i += 1
    if clean[start:].strip():
        starts.append((start, len(text)))
    if quoted:
        _warn(result, "文件末尾存在未闭合引号；相关语句未确认完整，请修复后重试。")
    for number, (begin, end) in enumerate(starts, 1):
        if progress and (number == 1 or number % 100 == 0):
            progress("parsing_ddl", statements_completed=number-1, statements_total=len(starts),
                     tables_parsed=len(result["structure"]["tables"]))
        part, masked = text[begin:end], clean[begin:end]
        if not masked.strip(' \t\r\n;'):
            continue
        loc = {"type": "ddl", "statement": number, "line_start": text.count('\n', 0, begin) + 1,
               "line_end": text.count('\n', 0, end) + 1}
        sid = _fragment(result, loc, part)
        if not CREATE_RE.match(masked.lstrip()):
            statement = masked.strip().removesuffix(';').strip()
            if _EXPORT_SET.fullmatch(statement):
                routine_declarations["SET"] += 1
                continue
            if export_drop.fullmatch(statement):
                routine_declarations["DROP TABLE IF EXISTS"] += 1
                continue
            _warn(result, f"第 {number} 条语句未提取结构：仅支持 SQLite/MySQL CREATE TABLE；原文已保留，未执行 SQL。")
            continue
        tables, failures = parse_sql(part, "material.sql")
        for fail in failures:
            _warn(result, f"第 {number} 条语句 / {fail.get('table', '?')}：{fail['reason']}；请修复该语句后重试。")
        create_offsets = [(qualified_identifier(m.group(1)), m.start()) for m in CREATE_RE.finditer(masked)]
        position = 0
        for table in tables:
            matching = next((j for j in range(position, len(create_offsets)) if create_offsets[j][0] == table['name']), position)
            table_offset = create_offsets[matching][1]
            position = matching + 1
            table["fragment_id"] = sid
            table["source_file"] = options.get("filename", "material.sql")
            _, body = next(extract_table_bodies(masked[table_offset:]))
            opening = CREATE_RE.match(masked, table_offset)
            tail = masked[opening.end() + len(body) + 1:].strip().rstrip(';').strip() if body is not None else ''
            table_comment = re.search(r'\bCOMMENT\b', mask_quoted(tail), re.I)
            if table_comment:
                match = COMMENT_RE.match(tail[table_comment.start():])
                if match:
                    table['comment'] = match.group(1).replace("''", "'")
                    tail = tail[:table_comment.start()] + tail[table_comment.start() + match.end():]
            remaining = []
            cursor = 0
            masked_tail = mask_quoted(tail)
            for option in _COMMON_TABLE_OPTION.finditer(tail):
                if masked_tail[option.start():option.end()] != option.group():
                    continue
                remaining.append(tail[cursor:option.start()])
                cursor = option.end()
                key = (option.group(1) or option.group(3)).upper()
                if key.endswith(('CHARSET', 'CHARACTER SET')):
                    key = 'CHARSET'
                value = option.group(2)
                identity = (key, value.casefold() if value else None)
                spelling, count = common_options.get(identity, (option.group() if value else key, 0))
                common_options[identity] = spelling, count + 1
            remaining.append(tail[cursor:])
            tail = ''.join(remaining)
            if tail.strip():
                _warn(result, f"表 {table['name']} 的附加选项仅保留原文、未解释：{tail.strip()}")
            index_counts.update(table.get("unmodeled_index_counts", {}))
            for warning in table.get("unsupported", []):
                _warn(result, f"表 {table['name']}：{warning}")
            occurrences = {}
            cursor = opening.end()
            for definition in split_columns(body):
                offset = masked.find(definition, cursor)
                if definition and offset >= 0:
                    occurrences.setdefault(definition, []).append(offset)
                    cursor = offset + len(definition)
            for kind, items in (("column", table["columns"]), ("foreign_key", table["foreign_keys"])):
                used = Counter()
                locations = set()
                for item in items:
                    raw = item.pop("raw_definition", "")
                    offsets = occurrences.get(raw, ())
                    index = used[raw]
                    used[raw] += 1
                    if index >= len(offsets):
                        item["fragment_id"] = sid
                        continue
                    offset = offsets[index]
                    line_start = text.count('\n', 0, begin + offset) + 1
                    line_end = text.count('\n', 0, begin + offset + len(raw)) + 1
                    excerpt = part[offset:offset + len(raw)]
                    item_loc = {**loc, "part": kind, "table": table["name"],
                                "line_start": line_start, "line_end": line_end}
                    identity = (line_start, line_end, excerpt)
                    if identity in locations:
                        item_loc["statement_offset"] = offset
                    locations.add(identity)
                    item["fragment_id"] = _fragment(result, item_loc, excerpt)
            for fk in table["foreign_keys"]:
                own_fields = {c['name'] for c in table['columns']}
                valid_source = set(fk['from_columns']) <= own_fields and len(set(fk['from_columns'])) == len(fk['from_columns'])
                if not valid_source:
                    _warn(result, f"表 {table['name']} 的外键引用缺失或重复的本表列；保留原文，请修复后再绑定。")
                if valid_source and fk["to_columns"] and len(fk["from_columns"]) == len(fk["to_columns"]):
                    result["structure"]["relationships"].append({"from": table["name"], "to": fk["to_table"], **fk})
            result["structure"]["tables"].append(table)
    if not result["structure"]["tables"]:
        result["status"] = "failed"
        _warn(result, "没有解析到受支持的表结构；请提供 SQLite/MySQL CREATE TABLE 或改为文本资料。")
        return result
    # Resolve after reading every statement so forward declarations work. Raw
    # foreign_keys remain available for review; relationships are bindable only
    # when both ends can be checked against this material, never by name guess.
    by_name = {}
    for table in result["structure"]["tables"]:
        by_name.setdefault(table["name"], []).append(table)
        names = [column["name"] for column in table["columns"]]
        if len(names) != len(set(names)):
            _warn(result, f"表 {table['name']} 有重复列名；请修复后再绑定关系。")
    for name, tables in by_name.items():
        if len(tables) > 1:
            _warn(result, f"表 {name} 有多份声明；保留原文，请确定要采用的定义。")
    checked = []
    for relation in result["structure"]["relationships"]:
        source = by_name[relation["from"]]
        target = by_name.get(relation["to"], [])
        if len(source) != 1 or len(target) != 1:
            _warn(result, f"外键 {relation['from']} → {relation['to']} 的表定义缺失或有多份；保留声明，需补充或核对目标表后再绑定。")
            continue
        source_names = [column["name"] for column in source[0]["columns"]]
        target_names = [column["name"] for column in target[0]["columns"]]
        if (len(source_names) != len(set(source_names)) or
                len(target_names) != len(set(target_names)) or
                len(relation["to_columns"]) != len(set(relation["to_columns"])) or
                not set(relation["to_columns"]) <= set(target_names)):
            _warn(result, f"外键 {relation['from']} → {relation['to']} 引用缺失或重复的列；保留声明，请修复后再绑定。")
            continue
        checked.append(relation)
    result["structure"]["relationships"] = checked
    for kind, count in routine_declarations.items():
        label = "导出会话 SET" if kind == "SET" else kind
        _warn(result, f"{label} 声明共 {count} 条；原文已保留，未执行 SQL。")
    for kind, count in index_counts.items():
        label = "唯一索引" if kind == "unique" else "普通索引"
        _warn(result, f"{label}声明共 {count} 条；保留原文，未提取索引语义。")
    for spelling, count in common_options.values():
        _warn(result, f"附加选项 {spelling} 出现 {count} 次；仅保留原文、未解释。")
    return _finish(result)


def _column(n):
    result = ""
    while n:
        n, r = divmod(n - 1, 26)
        result = chr(65 + r) + result
    return result


def _cell(address):
    match = re.fullmatch(r"\$?([A-Za-z]+)\$?([1-9]\d*)", address or "")
    if not match:
        raise ValueError(f"无效单元格位置 {address!r}；请使用 A1 或 A1:C20 形式。")
    col = 0
    for letter in match.group(1).upper():
        col = col * 26 + ord(letter) - 64
    return int(match.group(2)), col


def _selection(options, max_row, max_col):
    value = options.get("range")
    if value:
        parts = str(value).split(":")
        if len(parts) not in {1, 2}:
            raise ValueError("所选区域无效；请使用 A1:C20 形式。")
        r1, c1 = _cell(parts[0])
        r2, c2 = _cell(parts[-1])
        if r2 < r1 or c2 < c1:
            raise ValueError("所选区域起点必须在终点之前；请检查范围。")
        if r1 > max_row or c1 > max_col:
            raise ValueError("所选区域没有已读取的单元格；请查看预览并调整范围。")
        r2, c2 = min(r2, max_row), min(c2, max_col)
    else:
        r1, c1, r2, c2 = 1, 1, max_row, max_col
    header = options.get("header", r1)
    if header is not False and (type(header) is not int or not r1 <= header <= r2):
        raise ValueError("表头必须为所选范围内的行号，或 false（无表头）；请调整表头行。")
    if (r2 - r1 + 1) * (c2 - c1 + 1) > MAX_SHEET_CELLS:
        raise ValueError("所选区域超过 100000 个单元格；请指定较小区域后重试，不会截取后冒充完整解析。")
    return r1, c1, r2, c2, header


def _selected_cell(options, row, column):
    """Read only an explicitly requested area, without expanding empty grids."""
    value = options.get('range')
    if not value:
        return True
    parts = str(value).split(':')
    if len(parts) not in {1, 2}:
        raise ValueError('所选区域无效；请使用 A1:C20 形式。')
    r1, c1 = _cell(parts[0])
    r2, c2 = _cell(parts[-1])
    if r1 > r2 or c1 > c2:
        raise ValueError('所选区域起点必须在终点之前；请检查范围。')
    return r1 <= row <= r2 and c1 <= column <= c2


def _tabulate(result, name, cells, options, *, row_lines=None, merges=None):
    if not cells:
        return None
    max_row, max_col = max(r for r, c in cells), max(c for r, c in cells)
    r1, c1, r2, c2, header = _selection(options, max_row, max_col)
    headers = [str(cells.get((header, c), {}).get("value") if cells.get((header, c), {}).get("value") is not None else "")
               for c in range(c1, c2 + 1)] if header is not False else []
    good_headers = bool(headers) and all(h.strip() for h in headers) and len(headers) == len(set(headers))
    if headers and not good_headers:
        _warn(result, f"工作表 {name} 的表头有空值或重复名称；保留各列位置，请选择正确表头，不按重复名称覆盖字段。")
    sheet = {"name": name, "header_row": header, "headers": headers,
             "range": f"{_column(c1)}{r1}:{_column(c2)}{r2}", "rows": [], "merges": merges or []}
    for r in range(r1, r2 + 1):
        selected = []
        for c in range(c1, c2 + 1):
            if (r, c) not in cells:
                continue
            cell = dict(cells[r, c])
            address = f"{_column(c)}{r}"
            cell.update(ref=address, row=r, column=c)
            location = {"type": "cell", "sheet": name, "cell": address, "row": r, "column": c}
            if row_lines and r in row_lines:
                location.update(line_start=row_lines[r][0], line_end=row_lines[r][1])
            display = str(cell.get("value") if cell.get("value") is not None else "")
            if "formula" in cell:
                display = f"公式：{cell['formula']}\n缓存值：" + ("缺失（未重算）" if cell.get("cache_missing") else str(cell.get("cached_value")))
            cell["fragment_id"] = _fragment(result, location, display)
            selected.append(cell)
        if not selected:
            continue
        values = [cells.get((r, c), {}).get("value") for c in range(c1, c2 + 1)]
        row = {"row": r, "cells": selected, "values": values, "is_header": r == header,
               "row_type": "header" if r == header else ("preamble" if header is not False and r < header else "data")}
        if good_headers and r > header:
            row["record"] = dict(zip(headers, values))
        line = " | ".join(f"{x['ref']}={x.get('value') if x.get('value') is not None else '[空或无缓存]'}" for x in selected)
        row["fragment_id"] = _fragment(result, {"type": "row", "sheet": name, "row": r,
                                                "range": f"{_column(c1)}{r}:{_column(c2)}{r}"}, line)
        sheet["rows"].append(row)
    return sheet


def _csv(content, options):
    text = _decode(content, options)
    delimiter = options.get("delimiter", ",")
    if delimiter not in {",", ";", "\t", "|"}:
        raise ValueError("CSV 分隔符仅支持逗号、分号、制表符或竖线；请明确选择分隔符。")
    result = _result("csv", structure={"sheets": [], "delimiter": delimiter})
    cells, row_lines, previous = {}, {}, 0
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True)
    widths = set()
    try:
        for r, row in enumerate(reader, 1):
            row_lines[r] = (previous + 1, reader.line_num)
            previous = reader.line_num
            widths.add(len(row))
            for c, value in enumerate(row, 1):
                if not _selected_cell(options, r, c):
                    continue
                if len(cells) >= MAX_SHEET_CELLS:
                    raise ValueError("CSV 所选范围超过 100000 个单元格；请缩小范围后重试，不会截取数据。")
                cells[r, c] = {"value": value, "data_type": "string"}
    except csv.Error as exc:
        _warn(result, f"CSV 第 {reader.line_num} 行附近解析失败：{exc}；此前完整行已保留，请修复引号或分隔符后重试。")
    if len(widths) > 1:
        _warn(result, "CSV 各行列数不一致；缺失单元格与空字符串分开保留，请检查分隔符及表头。")
    sheet = _tabulate(result, "CSV", cells, options, row_lines=row_lines)
    if sheet:
        result["structure"]["sheets"].append(sheet)
    return _finish(result)


def _archive(content):
    archive = zipfile.ZipFile(io.BytesIO(content))
    infos = archive.infolist()
    if len(infos) > MAX_XML_PARTS or sum(x.file_size for x in infos) > MAX_EXPANDED_BYTES:
        archive.close()
        raise ValueError("Office 文件展开后过大；请缩小文档或工作簿后重试。")
    names = [x.filename for x in infos]
    if len(names) != len(set(names)):
        archive.close()
        raise ValueError("Office 文件包含重复组件，无法确定内容；请用办公软件另存为新文件。")
    if any(x.flag_bits & 1 for x in infos):
        archive.close()
        raise ValueError("Office 文件含加密组件；请先提供可读取的副本。")
    return archive


def _xml(archive, name):
    if name not in archive.namelist():
        raise ValueError(f"Office 文件缺少 {name}，请检查格式或另存后重试。")
    raw = archive.read(name)
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", raw.replace(b'\x00', b''), re.I):
        raise ValueError(f"{name} 含不支持的 XML 实体定义；请另存为标准 Office 文件。")
    return ET.fromstring(raw)


def _xlsx(content, options):
    result = _result("xlsx", structure={"sheets": [], "available_sheets": []})
    with _archive(content) as archive:
        names = archive.namelist()
        book = _xml(archive, "xl/workbook.xml")
        rels = _xml(archive, "xl/_rels/workbook.xml.rels")
        targets = {}
        for rel in rels:
            if rel.get("TargetMode") == "External":
                _warn(result, "工作簿含外部链接；未读取或连接外部内容。")
                continue
            path = rel.get("Target", "")
            path = posixpath.normpath(path.lstrip('/') if path.startswith('/') else posixpath.join("xl", path))
            if not path.startswith("xl/"):
                raise ValueError("工作簿组件路径越界；请另存为标准 XLSX 文件。")
            targets[rel.get("Id")] = path
        strings = []
        if "xl/sharedStrings.xml" in names:
            strings = [''.join(t.text or '' for t in x.findall('.//x:t', _NS))
                       for x in _xml(archive, "xl/sharedStrings.xml")]
        if any("externalLinks/" in n for n in names):
            _warn(result, "工作簿含外部链接；仅保留文件内已有值，未访问链接或刷新公式。")
        if any("vbaProject" in n for n in names):
            _warn(result, "工作簿含宏组件；未执行或解析宏。")
        available = list(book.findall('x:sheets/x:sheet', _NS))
        result["structure"]["available_sheets"] = [s.get("name") for s in available]
        selection = options.get("sheet")
        if selection is not None and selection not in result["structure"]["available_sheets"]:
            raise ValueError("所选工作表不存在；请从实际工作表名称中重新选择。")
        for entry in available:
            name = entry.get("name", "")
            if selection is not None and selection != name:
                continue
            path = targets.get(entry.get('{' + _NS['r'] + '}id'))
            if not path:
                _warn(result, f"工作表 {name} 的内容引用缺失或为外部引用，请另存后重试。")
                continue
            try:
                root = _xml(archive, path)
            except (ValueError, ET.ParseError) as exc:
                _warn(result, f"工作表 {name} 读取失败：{exc}")
                continue
            cells = {}
            for element in root.findall('.//x:sheetData/x:row/x:c', _NS):
                address = element.get("r")
                r, c = _cell(address)
                if not _selected_cell(options, r, c):
                    continue
                if len(cells) >= MAX_SHEET_CELLS:
                    raise ValueError(f"工作表 {name} 超过 100000 个已存单元格；请拆分工作簿后重试。")
                if (r, c) in cells:
                    raise ValueError(f"工作表 {name} 的 {address} 重复出现；请另存后重试。")
                typ, value_node = element.get("t", "n"), element.find("x:v", _NS)
                raw = value_node.text if value_node is not None else None
                value = raw
                if typ == "s":
                    try:
                        index = int(raw)
                        if index < 0:
                            raise ValueError('negative shared-string index')
                        value = strings[index]
                    except (ValueError, TypeError, IndexError) as exc:
                        raise ValueError(f"工作表 {name} 的 {address} 共享文本引用无效；请另存后重试。") from exc
                elif typ == "inlineStr":
                    value = ''.join(t.text or '' for t in element.findall('.//x:is//x:t', _NS))
                elif typ == "b" and raw is not None:
                    value = raw == "1"
                cell = {"value": value, "data_type": {"n": "number", "b": "boolean", "e": "error"}.get(typ, "string"),
                        "raw_type": typ, "style": element.get("s")}
                formula = element.find('x:f', _NS)
                if formula is not None:
                    _warn(result, f"工作表 {name} 含公式；仅读取文件中已有公式及缓存值，未重算或刷新。")
                    cell.update(formula=formula.text or "", cached_value=value, cache_missing=value_node is None or raw is None,
                                formula_attributes=dict(formula.attrib))
                    if cell["cache_missing"]:
                        cell["value"] = None
                        _warn(result, f"工作表 {name} 的 {address} 公式没有缓存值；未重算，不能将其视为 0。")
                    if formula.get("t") in {"shared", "array", "dataTable"}:
                        _warn(result, f"工作表 {name} 的 {address} 使用共享/数组公式；仅保留原式和缓存，未展开或重算。")
                if typ == "e":
                    _warn(result, f"工作表 {name} 的 {address} 保存的是错误值 {raw}，请在原文件修正。")
                if typ == "n" and element.get("s") and raw is not None:
                    _warn(result, f"工作表 {name} 的数值保留原始值；日期、百分比等显示样式未换算，请核对原件。")
                cells[r, c] = cell
            merges = [x.get('ref') for x in root.findall('x:mergeCells/x:mergeCell', _NS)]
            if merges:
                _warn(result, f"工作表 {name} 含合并单元格（{', '.join(merges[:8])}）；未向空格填充值，请核对表头和区域。")
            sheet = _tabulate(result, name, cells, options, merges=merges)
            if sheet:
                sheet["visibility"] = entry.get("state", "visible")
                result["structure"]["sheets"].append(sheet)
    return _finish(result)


def _word_text(element):
    pieces = []
    for part in element.iter():
        tag = part.tag.rsplit('}', 1)[-1]
        if tag == 't':
            pieces.append(part.text or '')
        elif tag == 'tab':
            pieces.append('\t')
        elif tag in {'br', 'cr'}:
            pieces.append('\n')
    return ''.join(pieces)


def _docx(content, options):
    result = _result("docx", structure={"paragraphs": [], "tables": []})
    with _archive(content) as archive:
        root = _xml(archive, "word/document.xml")
        body = root.find('w:body', _NS)
        if body is None:
            raise ValueError("DOCX 缺少正文；请另存为含正文文字的文档。")
        names = archive.namelist()
        if any(n.startswith(('word/media/', 'word/embeddings/')) for n in names):
            _warn(result, "文档含图片或嵌入对象；仅提取正文与普通表格，未识别这些对象中的文字。")
        if any(re.match(r'word/(?:header|footer|footnotes|endnotes|comments)', n) for n in names):
            _warn(result, "文档含页眉页脚、脚注、尾注或批注；这些内容未进入正文提取，请按需补充文字。")
        if root.findall('.//w:ins', _NS) or root.findall('.//w:del', _NS):
            _warn(result, "文档含未接受的修订；仅保留可见正文文本，不能据此确定修订的正式状态。")
        if root.findall('.//w:txbxContent', _NS):
            _warn(result, "文档含文本框；正文定位不代表文本框的视觉顺序，请核对原件。")
        headings, paragraph_no, table_no = [], 0, 0
        for block in body:
            kind = block.tag.rsplit('}', 1)[-1]
            if kind == 'p':
                paragraph_no += 1
                text = _word_text(block)
                style_node = block.find('w:pPr/w:pStyle', _NS)
                style = style_node.get('{' + _NS['w'] + '}val', '') if style_node is not None else ''
                match = re.search(r'(?:Heading|标题)\s*([1-9])', style, re.I)
                if match:
                    headings[:] = headings[:int(match.group(1)) - 1] + [text]
                if text.strip():
                    fid = _fragment(result, {"type": "paragraph", "paragraph": paragraph_no,
                                             "headings": list(headings)}, text)
                    result['structure']['paragraphs'].append({"paragraph": paragraph_no, "style": style, "fragment_id": fid})
            elif kind == 'tbl':
                table_no += 1
                table = {"table": table_no, "rows": []}
                for ri, row in enumerate(block.findall('w:tr', _NS), 1):
                    cells = []
                    for ci, cell in enumerate(row.findall('w:tc', _NS), 1):
                        if cell.find('w:tcPr/w:gridSpan', _NS) is not None or cell.find('w:tcPr/w:vMerge', _NS) is not None:
                            _warn(result, f"表格 {table_no} 含合并单元格；按原始单元格顺序定位，未填充或推测表头。")
                        if cell.find('w:tbl', _NS) is not None:
                            _warn(result, f"表格 {table_no} 含嵌套表格；内层结构未提取，请补充独立表格。")
                        text = '\n'.join(_word_text(p) for p in cell.findall('w:p', _NS))
                        fid = _fragment(result, {"type": "table_cell", "table": table_no, "row": ri, "column": ci,
                                                 "headings": list(headings)}, text)
                        cells.append({"column": ci, "text": text, "fragment_id": fid})
                    table['rows'].append({"row": ri, "cells": cells})
                result['structure']['tables'].append(table)
            elif kind not in {'sectPr'}:
                _warn(result, f"正文包含未展开的 {kind} 内容，请核对或另存为普通段落后重试。")
    return _finish(result)


def _pdf(content, options):
    result = _result("pdf", structure={"pages": [], "table_extraction": "text_only"})
    try:
        from pypdf import PdfReader
    except ImportError:
        result['status'] = 'needs_conversion'
        result['warnings'].append("PDF 解析依赖 pypdf 尚未安装；请安装 requirements.txt，或提供文本副本。")
        return result
    try:
        reader = PdfReader(io.BytesIO(content), strict=False)
        if reader.is_encrypted:
            result['status'] = 'needs_conversion'
            result['warnings'].append("PDF 已加密；请提供可读取的副本或提取后的文字，不会尝试密码或外部转换。")
            return result
        result['structure']['page_count'] = len(reader.pages)
        for number, page in enumerate(reader.pages, 1):
            try:
                stream = page.get_contents()
                if stream is not None and len(stream.get_data()) > 16 * 1024 * 1024:
                    raise ValueError("页面展开内容超过 16 MB，请将该页转换成文字后补充")
                text = page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False) or ''
            except Exception as exc:
                result['structure']['pages'].append({"page": number, "status": "failed"})
                _warn(result, f"PDF 第 {number} 页无法提取：{type(exc).__name__}；请提供该页文字后重试。")
                continue
            if not text.strip():
                result['structure']['pages'].append({"page": number, "status": "needs_conversion"})
                _warn(result, f"PDF 第 {number} 页没有可提取文字，可能是扫描页或空页；未执行 OCR，请核对并补充文字。")
                continue
            fid = _fragment(result, {"type": "page", "page": number}, text)
            result['structure']['pages'].append({"page": number, "status": "extracted", "fragment_id": fid})
        _warn(result, "PDF 按页提取文本；表格结构、复杂多栏阅读顺序和图片内容未验证，请在原页核对。")
        return _finish(result, no_text='needs_conversion')
    except Exception as exc:
        result['status'] = 'failed'
        result['warnings'].append(f"PDF 文件无法读取（{type(exc).__name__}）；请检查文件是否损坏或另存后重试。")
        return result


def _structured(content, options, fmt):
    text = _decode(content, options)
    duplicates = []
    if fmt == 'json':
        def pairs(items):
            obj = {}
            for key, value in items:
                if key in obj:
                    duplicates.append(str(key))
                obj[key] = value
            return obj
        def invalid_constant(value):
            raise ValueError(f'JSON 中的 {value} 不是有限标准值')
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid_constant)
    else:
        import yaml
        class MaterialLoader(yaml.SafeLoader):
            pass
        def mapping(loader, node):
            loader.flatten_mapping(node)
            obj = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=True)
                if key in obj:
                    duplicates.append(str(key))
                obj[key] = loader.construct_object(value_node, deep=True)
            return obj
        MaterialLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
        try:
            value = yaml.load(text, Loader=MaterialLoader)
        except yaml.YAMLError as exc:
            raise ValueError(f'YAML 格式无效：{exc}') from exc
        value = json.loads(json.dumps(value, ensure_ascii=False, default=str, allow_nan=False))
    result = _result(fmt, structure={"document": value})
    # Preserve exact original text and identify semantic records without guessing their meaning.
    _fragment(result, {"type": "text", "line_start": 1, "line_end": len(text.splitlines())}, text)
    if not isinstance(value, (dict, list)):
        _warn(result, "资料不是对象或记录列表；保留原文，字段含义请由操作者或宿主核对。")
    if duplicates:
        _warn(result, '资料含重复字段：' + ', '.join(duplicates[:12]) + '；结构视图只显示末次值，请核对原文并修正后再生成候选。')
    return _finish(result)


def parse_material(filename, content: bytes, options=None, *, progress=None):
    """Return the parser contract; recoverable input errors remain local results.

    Options: encoding; CSV delimiter; spreadsheet sheet (name), header (one-based
    row or False), range (A1:C20). Unspecified XLSX sheet reads all sheets and
    reports their names so the UI can choose a narrower reparse.
    """
    ext = Path(str(filename or '')).suffix.lower()
    fmt = {'.txt': 'text', '.md': 'markdown', '.markdown': 'markdown', '.sql': 'ddl', '.ddl': 'ddl',
           '.csv': 'csv', '.tsv': 'csv', '.xlsx': 'xlsx', '.docx': 'docx', '.pdf': 'pdf',
           '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml', '': 'text'}.get(ext, 'unsupported')
    result = _result(fmt, status='failed')
    if not isinstance(content, bytes):
        result['warnings'].append('导入内容必须是原始文件字节；请重新选择文件。')
        return result
    if len(content) > MAX_FILE_BYTES:
        result['warnings'].append('单个文件不能超过 32 MB；请拆分文件后重试，原文件不会被截断。')
        return result
    if not content:
        result['warnings'].append('文件为空；请提供包含文字或结构的资料。')
        return result
    if options is not None and not isinstance(options, dict):
        result['warnings'].append('解析选项必须是对象；请重新选择解析范围。')
        return result
    options = dict(options or {})
    options['filename'] = str(filename)
    if ext == '.tsv':
        options.setdefault('delimiter', '\t')
    if fmt == 'unsupported':
        result['status'] = 'needs_conversion'
        result['warnings'].append('此格式尚不支持；请提供 TXT/MD/DDL/CSV/XLSX/DOCX/文本 PDF/JSON/YAML，不接受 ZIP 批量导入。')
        return result
    try:
        if fmt in {'text', 'markdown'}:
            return _text(content, options, fmt)
        if fmt in {'json', 'yaml'}:
            return _structured(content, options, fmt)
        if fmt == 'ddl':
            return _ddl(content, options, progress)
        return {'csv': _csv, 'xlsx': _xlsx, 'docx': _docx, 'pdf': _pdf}[fmt](content, options)
    except (ValueError, TypeError, KeyError, IndexError, LookupError, RecursionError, OSError, RuntimeError,
            NotImplementedError, zipfile.BadZipFile, ET.ParseError, csv.Error) as exc:
        result['warnings'].append(f'解析失败：{exc}；请修正资料或解析选项后重试，已有来源和图谱不会被修改。')
        return result
