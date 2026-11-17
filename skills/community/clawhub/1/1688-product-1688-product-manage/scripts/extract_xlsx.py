#!/usr/bin/env python3
"""Extract XLSX cells and anchored images; no macros, formula execution or network."""
import argparse
import hashlib
import importlib.util
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from _local_io import cached, emit, finish, workspace

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
D = "{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def xml(archive, name):
    data = archive.read(name)
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("不支持 XML DTD/实体声明")
    return ET.fromstring(data)


def relationships(archive, owner):
    filename = posixpath.join(posixpath.dirname(owner), "_rels", posixpath.basename(owner) + ".rels")
    if filename not in archive.namelist():
        return {}
    result = {}
    for item in xml(archive, filename):
        target = item.attrib["Target"]
        external = item.get("TargetMode") == "External"
        if not external:
            target = posixpath.normpath(target.lstrip("/") if target.startswith("/")
                                       else posixpath.join(posixpath.dirname(owner), target))
            if target.startswith("../") or target == "..":
                raise ValueError("关系路径越出 XLSX 包")
        result[item.attrib["Id"]] = {"target": target, "external": external, "type": item.get("Type", "")}
    return result


def rich_text(node):
    if node is None:
        return ""
    return "".join((child.text or "") if child.tag == S + "t"
                   else "".join(t.text or "" for t in child.findall(S + "t"))
                   for child in node if child.tag in (S + "t", S + "r"))


def marker(node):
    if node is None:
        return None
    return {child.tag.split("}")[-1]: int(child.text) for child in node}


def extract(source, output, backend="auto"):
    if backend == "auto":
        backend = "openpyxl" if importlib.util.find_spec("openpyxl") else "xml"
    source, folder, fingerprint = workspace(source, output, {"backend": backend}, __file__)
    old = cached(folder, fingerprint)
    if old:
        return old
    sheets, issues, notes, paths, used_media = [], [], [], [], set()
    with zipfile.ZipFile(source) as archive:
        members = archive.infolist()
        if len(members) > 20000 or sum(m.file_size for m in members) > 256 * 1024 * 1024:
            raise ValueError("XLSX 解压规模超出处理上限")
        if len({m.filename for m in members}) != len(members):
            raise ValueError("XLSX 含重名 ZIP 成员")
        for member in members:
            if member.filename.startswith("/") or ".." in member.filename.split("/") or "\\" in member.filename:
                raise ValueError("XLSX 含不安全成员路径")
        names = set(archive.namelist())
        book = xml(archive, "xl/workbook.xml")
        if book.tag != S + "workbook":
            raise ValueError("不支持此 SpreadsheetML 命名空间，请转存标准 XLSX")
        book_rels = relationships(archive, "xl/workbook.xml")
        strings = ([rich_text(si) for si in xml(archive, "xl/sharedStrings.xml")]
                   if "xl/sharedStrings.xml" in names else [])
        formats, style_ids = {}, []
        if "xl/styles.xml" in names:
            styles = xml(archive, "xl/styles.xml")
            formats = {int(e.get("numFmtId")): e.get("formatCode")
                       for e in styles.findall(S + "numFmts/" + S + "numFmt")}
            style_ids = [int(e.get("numFmtId", "0")) for e in styles.findall(S + "cellXfs/" + S + "xf")]
        for sheet in book.findall(S + "sheets/" + S + "sheet"):
            entry = {"name": sheet.get("name"), "sheetId": sheet.get("sheetId"),
                     "state": sheet.get("state", "visible"), "cells": [], "images": [],
                     "mergedRanges": [], "hyperlinks": []}
            sheets.append(entry)
            try:
                rel = book_rels[sheet.attrib[R + "id"]]
                if rel["external"] or not rel["type"].endswith("/worksheet"):
                    raise ValueError("工作表关系不是本地 worksheet")
                part = rel["target"]
                root = xml(archive, part)
                rels = relationships(archive, part)
                for cell in root.findall(S + "sheetData/" + S + "row/" + S + "c"):
                    address = cell.get("r")
                    if not address or not re.fullmatch(r"[A-Z]+[1-9][0-9]*", address):
                        raise ValueError("单元格缺少有效坐标")
                    kind = cell.get("t", "n")
                    raw = cell.findtext(S + "v")
                    value = raw
                    if kind == "s":
                        if raw is None or not 0 <= int(raw) < len(strings):
                            raise ValueError("共享字符串索引缺失或越界")
                        value = strings[int(raw)]
                    elif kind == "inlineStr":
                        value = rich_text(cell.find(S + "is"))
                    formula = cell.find(S + "f")
                    style = int(cell.get("s", "0"))
                    fmt_id = style_ids[style] if style < len(style_ids) else None
                    fmt = formats.get(fmt_id, {0: "General", 1: "0", 2: "0.00", 49: "@"}.get(fmt_id))
                    display = value
                    if kind == "n" and value and fmt and re.fullmatch(r"0+", fmt) and re.fullmatch(r"[0-9]+", value):
                        display = value.zfill(len(fmt))
                    record = {"cell": address, "type": kind, "value": value, "rawValue": raw,
                              "styleIndex": style, "numberFormatId": fmt_id,
                              "numberFormat": fmt, "displayText": display}
                    if formula is not None:
                        record.update(formula=formula.text, formulaAttributes=formula.attrib,
                                      cachedValue=raw, cacheMissing=raw is None)
                        if raw is None:
                            issues.append(f"{entry['name']}!{address}: 公式无缓存值，未计算")
                    entry["cells"].append(record)
                entry["mergedRanges"] = [e.get("ref") for e in root.findall(S + "mergeCells/" + S + "mergeCell")]
                for link in root.findall(S + "hyperlinks/" + S + "hyperlink"):
                    target = rels.get(link.get(R + "id"), {})
                    entry["hyperlinks"].append({"cell": link.get("ref"), "location": link.get("location"),
                                                "target": target.get("target")})
                for drawing in root.findall(S + "drawing"):
                    drawing_rel = rels[drawing.attrib[R + "id"]]
                    if drawing_rel["external"]:
                        issues.append(f"{entry['name']}: 外部 drawing 未读取")
                        continue
                    drawing_part = drawing_rel["target"]
                    drawing_rels = relationships(archive, drawing_part)
                    for anchor in xml(archive, drawing_part):
                        for blip in anchor.findall(".//" + A + "blip"):
                            image_rel = drawing_rels.get(blip.get(R + "embed") or blip.get(R + "link"))
                            if not image_rel:
                                issues.append(f"{entry['name']}: 图片关系缺失")
                                continue
                            if image_rel["external"]:
                                issues.append(f"{entry['name']}: 外链图片需由宿主单独读取")
                                entry["images"].append({"sourceUrl": image_rel["target"],
                                                        "from": marker(anchor.find(D + "from"))})
                                continue
                            image_part = image_rel["target"]
                            data = archive.read(image_part)
                            if not data:
                                raise ValueError("嵌图为空")
                            suffix = Path(image_part).suffix.lower()
                            if suffix not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".emf", ".wmf", ".svg"):
                                suffix = ".bin"
                            target = folder / "images" / (hashlib.sha256(data).hexdigest() + suffix)
                            target.parent.mkdir(exist_ok=True)
                            target.write_bytes(data)
                            used_media.add(image_part)
                            if target not in paths:
                                paths.append(target)
                            origin = marker(anchor.find(D + "from"))
                            entry["images"].append({
                                "path": str(target), "sourcePart": image_part,
                                "anchorType": anchor.tag.split("}")[-1],
                                "from": origin, "to": marker(anchor.find(D + "to")),
                                "position": anchor.find(D + "pos").attrib if anchor.find(D + "pos") is not None else None,
                                "extent": anchor.find(D + "ext").attrib if anchor.find(D + "ext") is not None else None,
                                "row": origin["row"] + 1 if origin else None,
                                "column": origin["col"] + 1 if origin else None})
                            if origin is None:
                                issues.append(f"{entry['name']}: 图片仅有绝对位置，商品归属待确认")
                if root.find(S + "legacyDrawing") is not None:
                    notes.append(f"{entry['name']}: 存在 VML 对象；其未关联图片列入缺口")
            except (KeyError, ValueError, ET.ParseError) as exc:
                issues.append(f"{entry['name']}: {exc}")
        unassociated = sorted(n for n in names if n.startswith("xl/media/") and not n.endswith("/") and n not in used_media)
        if unassociated:
            issues.append("存在未关联嵌图，不能按文件顺序猜归属: " + ", ".join(unassociated))
        if any(n.startswith(("xl/richData/", "xl/cellimages")) for n in names):
            issues.append("存在单元格图片扩展，常规 drawing 不能保证完整关联，请补导出图或截图")
        date1904 = book.find(S + "workbookPr")
        date1904 = date1904 is not None and date1904.get("date1904") in ("1", "true")
    if backend == "openpyxl":
        try:
            import openpyxl
            book = openpyxl.load_workbook(source, read_only=False, data_only=False, keep_links=False)
            try:
                for sheet in sheets:
                    ws = book[sheet["name"]]
                    for cell in sheet["cells"]:
                        cell["numberFormat"] = ws[cell["cell"]].number_format
            finally:
                book.close()
        except Exception as exc:
            notes.append("库读取不可用，已使用固定 ZIP/XML 结果: " + str(exc))
    if not sheets:
        issues.append("没有可读取的工作表")
    return finish(folder, fingerprint, {
        "status": "partial" if issues else "ok", "backend": backend,
        "source": str(source), "date1904": date1904, "sheets": sheets,
        "unassociatedMedia": unassociated, "issues": issues, "notes": notes,
        "anchorUnits": "from/to 行列从 0 起，row/column 从 1 起，偏移及 extent 为 EMU",
        "numericValues": "保留 XML 数值字符串以免丢精度；按 type/numberFormat 解释，不执行公式"},
        paths)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--backend", choices=["auto", "openpyxl", "xml"], default="auto")
    args = p.parse_args()
    try:
        result = extract(args.input, args.output_dir, args.backend)
        # Full cells stay on disk, not in a potentially truncated tool response.
        _, folder, _ = workspace(args.input, args.output_dir, {"backend": result["backend"]}, __file__)
        emit({"status": result["status"], "resultPath": str(folder / "result.json"),
              "reused": result["reused"], "sheets": [
                  {"name": s["name"], "cells": len(s["cells"]), "images": len(s["images"])}
                  for s in result["sheets"]], "issues": result["issues"]})
        return 0 if result["status"] == "ok" else 2
    except Exception as exc:
        emit({"status": "failed", "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
