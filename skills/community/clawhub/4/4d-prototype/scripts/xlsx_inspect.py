#!/usr/bin/env python3
"""Inspect the layout and statistical profile of Excel samples (standard library only; the source file is never modified).

Usage:
    python3 -I xlsx_inspect.py dump <file.xlsx> [--rows 40]
        Per sheet: row count, merged cells, the first N rows (column:value) — to find the header row, summary rows and layout.
    python3 -I xlsx_inspect.py profile <file.xlsx> [--header-row 1] [--max-distinct 30] [--json out.json]
        Per column: non-empty count, distinct values, fill colors; low-cardinality columns (distinct ≤ max-distinct) get a value
        distribution, while high-cardinality and likely-sensitive columns only get the "shape" of their values
        (D=digit L=letter C=CJK …, e.g. D9L2), so names, account numbers and the like never enter the context.
        Likely sensitive: the header mentions name / account / phone / ID / address and similar (English or Chinese),
        or values contain 8+ consecutive digits, or the average length exceeds 24.
        Use --reveal G,H (column letters) when you really need the raw values of a column.
        --json writes the per-column profile to a file for later scripts (without raw values of high-cardinality columns).

If the samples contain real customer data: run locally only, write output to the scratchpad, and commit aggregate numbers only.
"""
import argparse
import collections
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
SENSITIVE_HEADER = re.compile(r'名称|姓名|名字|账号|帐号|卡号|电话|手机|证件|身份证|地址|邮箱|联系人|name|account|phone|mobile|email|addr', re.I)
RNS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def col_index(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


class Book:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        names = self.z.namelist()
        self.ss = []
        if 'xl/sharedStrings.xml' in names:
            for si in ET.fromstring(self.z.read('xl/sharedStrings.xml')).findall(NS + 'si'):
                self.ss.append(''.join(t.text or '' for t in si.iter(NS + 't')))
        self.fills = self._fills() if 'xl/styles.xml' in names else []
        wb = ET.fromstring(self.z.read('xl/workbook.xml'))
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(self.z.read('xl/_rels/workbook.xml.rels'))}
        self.sheets = []
        for sh in wb.find(NS + 'sheets'):
            tgt = rels[sh.get(RNS + 'id')]
            path = tgt[1:] if tgt.startswith('/') else 'xl/' + tgt
            self.sheets.append((sh.get('name'), path))

    def _fills(self):
        st = ET.fromstring(self.z.read('xl/styles.xml'))
        colors = []
        fills = st.find(NS + 'fills')
        for f in fills if fills is not None else []:
            pf = f.find(NS + 'patternFill')
            c = None
            if pf is not None and pf.get('patternType') not in (None, 'none', 'gray125'):
                fg = pf.find(NS + 'fgColor')
                if fg is not None:
                    c = fg.get('rgb') or (f"theme{fg.get('theme')}" if fg.get('theme') else None)
            colors.append(c)
        xfs = st.find(NS + 'cellXfs')
        return [colors[int(x.get('fillId', 0))] if colors else None for x in (xfs if xfs is not None else [])]

    def rows(self, path):
        """Yield (row number, {column letter: value}, {column letter: fill color}) per row"""
        root = ET.fromstring(self.z.read(path))
        data = root.find(NS + 'sheetData')
        merges = root.find(NS + 'mergeCells')
        self.last_merges = [m.get('ref') for m in merges] if merges is not None else []
        for r in data.findall(NS + 'row') if data is not None else []:
            vals, fills = {}, {}
            for c in r.findall(NS + 'c'):
                col = re.match(r'[A-Z]+', c.get('r')).group()
                t, v, isel = c.get('t'), c.find(NS + 'v'), c.find(NS + 'is')
                if t == 's' and v is not None:
                    val = self.ss[int(v.text)]
                elif t == 'inlineStr' and isel is not None:
                    val = ''.join(x.text or '' for x in isel.iter(NS + 't'))
                elif v is not None:
                    val = v.text or ''
                else:
                    val = ''
                if val != '':
                    vals[col] = val
                s = c.get('s')
                if s and self.fills and int(s) < len(self.fills) and self.fills[int(s)]:
                    fills[col] = self.fills[int(s)]
            yield int(r.get('r')), vals, fills


def shape(v):
    out, last, n = [], None, 0
    for ch in v:
        k = 'D' if ch.isdigit() else 'L' if ch.isascii() and ch.isalpha() else 'C' if '一' <= ch <= '鿿' else 'S' if ch.isspace() else 'P'
        if k == last:
            n += 1
        else:
            if last:
                out.append(f'{last}{n}')
            last, n = k, 1
    if last:
        out.append(f'{last}{n}')
    return ''.join(out)


def dump(book, rows):
    for name, path in book.sheets:
        it = list(book.rows(path))
        print(f'===== SHEET: {name}  rows={len(it)}')
        if book.last_merges:
            print('merges:', book.last_merges[:30])
        for rn, vals, fills in it[:rows]:
            if vals:
                cells = ' || '.join(f'{k}:{v}' for k, v in sorted(vals.items(), key=lambda x: col_index(x[0])))
                mark = f'  [fill {sorted(set(fills.values()))}]' if fills else ''
                print(f'{rn} {cells}{mark}')


def sensitive(header, values):
    if SENSITIVE_HEADER.search(header or ''):
        return True
    if any(re.search(r'\d{8,}', v) for v in values[:2000]):
        return True
    return bool(values) and sum(len(v) for v in values) / len(values) > 24


def profile(book, header_row, max_distinct, reveal=()):
    result = {}
    for name, path in book.sheets:
        header, cols, row_fills, n = {}, collections.defaultdict(list), collections.Counter(), 0
        for rn, vals, fills in book.rows(path):
            if rn < header_row:
                continue
            if rn == header_row:
                header = vals
                continue
            if not vals:
                continue
            n += 1
            if fills:
                row_fills[tuple(sorted(set(fills.values())))] += 1
            for k, v in vals.items():
                cols[k].append(v)
        print(f'===== SHEET: {name}  data rows={n}  header row={header_row}')
        if row_fills:
            print('rows with fill colors:', row_fills.most_common(5))
        sheet = []
        for k in sorted(set(header) | set(cols), key=col_index):
            vs = cols.get(k, [])
            cnt = collections.Counter(vs)
            item = {'col': k, 'header': header.get(k, ''), 'nonEmpty': len(vs), 'distinct': len(cnt)}
            if len(cnt) <= max_distinct and (k in reveal or not sensitive(header.get(k, ''), vs)):
                item['values'] = cnt.most_common()
                desc = ', '.join(f'{v}×{c}' for v, c in cnt.most_common(12))
            else:
                shapes = collections.Counter(shape(v) for v in vs)
                item['shapes'] = shapes.most_common(5)
                lens = [len(v) for v in vs]
                desc = f'shapes {shapes.most_common(5)}, length {min(lens)}–{max(lens)}' if lens else 'no values'
            sheet.append(item)
            print(f"  {k} {item['header'] or '(no header)'}: non-empty {item['nonEmpty']}/{n}, {item['distinct']} distinct; {desc}")
        result[name] = {'rows': n, 'columns': sheet}
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=['dump', 'profile'])
    ap.add_argument('xlsx')
    ap.add_argument('--rows', type=int, default=40)
    ap.add_argument('--header-row', type=int, default=1)
    ap.add_argument('--max-distinct', type=int, default=30)
    ap.add_argument('--json')
    ap.add_argument('--reveal', default='', help='comma-separated column letters: print value distributions for these columns even if they look sensitive')
    args = ap.parse_args()
    try:
        book = Book(args.xlsx)
    except (zipfile.BadZipFile, FileNotFoundError, KeyError) as e:
        sys.exit(f'cannot read {args.xlsx}: {e} (save legacy .xls files as .xlsx first)')
    if args.mode == 'dump':
        dump(book, args.rows)
    else:
        res = profile(book, args.header_row, args.max_distinct, tuple(x.strip().upper() for x in args.reveal.split(',') if x.strip()))
        if args.json:
            with open(args.json, 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False, indent=1)
            print('profile written to', args.json)


if __name__ == '__main__':
    main()
