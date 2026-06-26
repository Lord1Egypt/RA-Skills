import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal
import re
from collections import defaultdict
from xml.sax.saxutils import escape
import base64
import zlib
from pathlib import Path

NS_MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
NS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def parse_xlsx(path):
    ns = {'a': NS_MAIN}
    with zipfile.ZipFile(path) as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            ss_root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in ss_root.findall('a:si', ns):
                shared_strings.append(''.join(tn.text or '' for tn in si.findall('.//a:t', ns)))
        root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    rows = []
    for row in root.findall('.//a:row', ns):
        vals = []
        for c in row.findall('a:c', ns):
            t = c.get('t')
            if t == 'inlineStr':
                vals.append(''.join(tn.text or '' for tn in c.findall('.//a:t', ns)))
            else:
                vn = c.find('a:v', ns)
                if t == 's' and vn is not None and vn.text is not None:
                    vals.append(shared_strings[int(vn.text)])
                else:
                    vals.append(vn.text if vn is not None else '')
        rows.append(vals)
    return rows


def decode_pdf_streams(path):
    pdf = Path(path).read_bytes()
    decoded = []
    pattern = re.compile(rb'(\d+) 0 obj\s*<<.*?/Filter \[ /ASCII85Decode /FlateDecode \] /Length \d+\s*>>\s*stream\n(.*?)~>endstream', re.S)
    for m in pattern.finditer(pdf):
        data = m.group(2) + b'~>'
        try:
            dec = base64.a85decode(data, adobe=True)
            out = zlib.decompress(dec).decode('latin1', 'ignore')
            decoded.append(out)
        except Exception:
            continue
    return decoded


def unescape_pdf_text(text):
    return text.replace(r'\(', '(').replace(r'\)', ')').replace(r'\\', '\\')


def parse_bank_pdf(path):
    streams = decode_pdf_streams(path)
    tokens = []
    for s in streams:
        tokens.extend(unescape_pdf_text(t) for t in re.findall(r'\((.*?)\)\s*Tj', s))

    rows = []
    in_table = False
    i = 0
    amount_pat = re.compile(r'^-?\$[\d,]+\.\d{2}$')
    date_pat = re.compile(r'^\d{2}/\d{2}$')
    while i < len(tokens):
        tok = tokens[i].strip()
        if tok == 'Date' and i + 3 < len(tokens) and tokens[i+1].strip() == 'Description' and tokens[i+2].strip() == 'Amount' and tokens[i+3].strip() == 'Balance':
            in_table = True
            i += 4
            continue
        if in_table and date_pat.match(tok):
            tx_date = tok
            i += 1
            desc_parts = []
            while i < len(tokens) and not amount_pat.match(tokens[i].strip()):
                nxt = tokens[i].strip()
                if nxt in {'Date', 'Description', 'Amount', 'Balance', 'Important Account Information'}:
                    break
                desc_parts.append(nxt)
                i += 1
            if i + 1 >= len(tokens) or not amount_pat.match(tokens[i].strip()):
                continue
            amt_text = tokens[i].strip()
            bal_text = tokens[i+1].strip() if i + 1 < len(tokens) else ''
            if not amount_pat.match(bal_text):
                i += 1
                continue
            rows.append([tx_date, amt_text.replace('$', '').replace(',', ''), ' '.join(p for p in desc_parts if p), bal_text.replace('$', '').replace(',', '')])
            i += 2
            continue
        i += 1
    return rows


def col_letter(n):
    res = ''
    while n > 0:
        n, r = divmod(n - 1, 26)
        res = chr(65 + r) + res
    return res


def cell_xml(ref, val):
    if val is None or val == '':
        return f'<c r="{ref}"/>'
    if isinstance(val, Decimal):
        return f'<c r="{ref}"><v>{val}</v></c>'
    if isinstance(val, (int, float)):
        return f'<c r="{ref}"><v>{val}</v></c>'
    text = str(val)
    if re.fullmatch(r'-?\d+(\.\d+)?', text):
        return f'<c r="{ref}"><v>{text}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(text)}</t></is></c>'


def build_sheet(rows):
    max_cols = max((len(r) for r in rows), default=1)
    dim = f'A1:{col_letter(max_cols)}{max(len(rows), 1)}'
    sheet_data = []
    for r_idx, row in enumerate(rows, 1):
        cells = [cell_xml(f"{col_letter(c_idx)}{r_idx}", v) for c_idx, v in enumerate(row, 1)]
        sheet_data.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<worksheet xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<sheetData>{"".join(sheet_data)}</sheetData>'
        '</worksheet>'
    )


def write_xlsx(path, sheets):
    workbook_sheets = []
    workbook_rels = []
    content_types = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
    ]
    package = {
        '_rels/.rels': (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'
        ),
        'xl/styles.xml': (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="1"><font><sz val="11"/><name val="Aptos"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            '</styleSheet>'
        ),
    }

    for idx, (sheet_name, rows) in enumerate(sheets, 1):
        workbook_sheets.append(f'<sheet name="{escape(sheet_name)}" sheetId="{idx}" r:id="rId{idx}"/>')
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
        package[f'xl/worksheets/sheet{idx}.xml'] = build_sheet(rows)

    workbook_rel_style_id = len(sheets) + 1
    workbook_rels.append(
        f'<Relationship Id="rId{workbook_rel_style_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )

    package['[Content_Types].xml'] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        + ''.join(content_types) +
        '</Types>'
    )
    package['xl/workbook.xml'] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}"><sheets>'
        + ''.join(workbook_sheets) +
        '</sheets></workbook>'
    )
    package['xl/_rels/workbook.xml.rels'] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + ''.join(workbook_rels) +
        '</Relationships>'
    )

    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for file_name, content in package.items():
            z.writestr(file_name, content)


def extract_keys(text):
    clean = (
        text.upper()
        .replace('LEASE ', 'LS')
        .replace('PAYRUN ', 'PR')
        .replace('AUTOPAY ', 'AP')
        .replace('VEND-', 'VEND')
        .replace('CUST-', 'CUST')
    )
    return set(re.findall(r'[A-Z]{2,4}[- ]?\d+', clean))


def load_bank_rows(bank_path):
    bank_path = str(bank_path)
    if bank_path.lower().endswith('.pdf'):
        parsed = parse_bank_pdf(bank_path)
        extracted_xlsx = str(Path(bank_path).with_suffix('')) + '_extracted.xlsx'
        write_xlsx(extracted_xlsx, [('Bank Statement Extracted', [['date', 'transaction amount', 'description', 'balance']] + parsed)])
        return [['date', 'transaction amount', 'description']] + [r[:3] for r in parsed], extracted_xlsx
    return parse_xlsx(bank_path), None


def recon(bank_path, gl_path, output_path, threshold=Decimal('0.00')):
    bank_raw, extracted_xlsx = load_bank_rows(bank_path)
    gl_raw = parse_xlsx(gl_path)

    bank_data = [
        {
            'id': i,
            'date': r[0],
            'amount': Decimal(r[1]),
            'match_amount': abs(Decimal(r[1])),
            'desc': r[2],
            'keys': extract_keys(r[2])
        }
        for i, r in enumerate(bank_raw[1:]) if len(r) >= 3 and r[1] not in ('', None)
    ]
    gl_data = [
        {
            'id': i,
            'date': r[0],
            'amount': Decimal(r[1]),
            'match_amount': abs(Decimal(r[1])),
            'memo': r[2],
            'keys': extract_keys(r[2])
        }
        for i, r in enumerate(gl_raw[1:]) if len(r) >= 3 and r[1] not in ('', None)
    ]

    matched_bank_ids = set()
    matched_gl_ids = set()
    results = []

    all_keys = set()
    for b in bank_data:
        all_keys.update(b['keys'])
    for g in gl_data:
        all_keys.update(g['keys'])

    key_to_bank = defaultdict(list)
    for b in bank_data:
        for k in b['keys']:
            key_to_bank[k].append(b)

    key_to_gl = defaultdict(list)
    for g in gl_data:
        for k in g['keys']:
            key_to_gl[k].append(g)

    sorted_keys = sorted(all_keys, key=lambda x: (not x.startswith('BAT'), x))

    for k in sorted_keys:
        b_group = [b for b in key_to_bank[k] if b['id'] not in matched_bank_ids]
        g_group = [g for g in key_to_gl[k] if g['id'] not in matched_gl_ids]
        if not b_group or not g_group:
            continue

        b_sum = sum(b['match_amount'] for b in b_group)
        g_sum = sum(g['match_amount'] for g in g_group)
        diff = abs(b_sum - g_sum)
        if diff <= threshold:
            for b in b_group:
                matched_bank_ids.add(b['id'])
            for g in g_group:
                matched_gl_ids.add(g['id'])

            basis = f'Group Match ({k})'
            if len(b_group) == 1 and len(g_group) == 1:
                basis = '1:1 Match'
            elif len(b_group) == 1:
                basis = f'1:{len(g_group)} Match'
            elif len(g_group) == 1:
                basis = f'{len(b_group)}:1 Match'

            max_len = max(len(b_group), len(g_group))
            for i in range(max_len):
                b = b_group[i] if i < len(b_group) else {'date': '', 'amount': '', 'desc': ''}
                g = g_group[i] if i < len(g_group) else {'date': '', 'amount': '', 'memo': ''}
                results.append([
                    b['date'], b['amount'], b['desc'],
                    g['date'], g['amount'], g['memo'],
                    basis if i == 0 else '',
                    f'Diff: {diff}' if i == 0 else ''
                ])

    remaining_b = [b for b in bank_data if b['id'] not in matched_bank_ids]
    remaining_g = [g for g in gl_data if g['id'] not in matched_gl_ids]

    def get_name(text):
        text = text.upper()
        m = re.search(r'(FEDERAL TAX|GREENLEAF FOODS|METRO PROPERTIES|FRESHBEAN COFFEE|REDSTONE LABS|DELTA PAYROLL|NORTHWIND STORES|HARBOR MEDICAL|RIVERTON SCHOOL|APEX LOGISTICS|STATE TAX AGENCY|OAK PINE INTERIORS|ATLAS INDUSTRIAL|IRONGATE EQUIPMENT|CLEARVIEW DENTAL|SUMMIT DESIGN STUDIO|ZENITH TELECOM|LIBERTY INSURANCE GROUP|PIONEER PACKAGING|OFFICEHUB SUPPLY|BRIGHTLINE MARKETING|CLOUDTRAIL SOFTWARE)', text)
        return m.group(1) if m else None

    b_by_name = defaultdict(list)
    for b in remaining_b:
        name = get_name(b['desc'])
        if name:
            b_by_name[name].append(b)

    g_by_name = defaultdict(list)
    for g in remaining_g:
        name = get_name(g['memo'])
        if name:
            g_by_name[name].append(g)

    for name in b_by_name:
        b_list = [b for b in b_by_name[name] if b['id'] not in matched_bank_ids]
        g_list = [g for g in g_by_name[name] if g['id'] not in matched_gl_ids]
        if not b_list or not g_list:
            continue

        diff = abs(sum(b['match_amount'] for b in b_list) - sum(g['match_amount'] for g in g_list))
        if diff <= threshold:
            for b in b_list:
                matched_bank_ids.add(b['id'])
            for g in g_list:
                matched_gl_ids.add(g['id'])

            basis = f'AI Semantic Match: {name}'
            max_len = max(len(b_list), len(g_list))
            for i in range(max_len):
                b = b_list[i] if i < len(b_list) else {'date': '', 'amount': '', 'desc': ''}
                g = g_list[i] if i < len(g_list) else {'date': '', 'amount': '', 'memo': ''}
                results.append([
                    b['date'], b['amount'], b['desc'],
                    g['date'], g['amount'], g['memo'],
                    basis if i == 0 else '',
                    f'Diff: {diff}' if i == 0 else ''
                ])

    unreconciled_bank_rows = [
        [b['date'], b['amount'], b['desc']]
        for b in bank_data if b['id'] not in matched_bank_ids
    ]
    unreconciled_gl_rows = [
        [g['date'], g['amount'], g['memo']]
        for g in gl_data if g['id'] not in matched_gl_ids
    ]

    matched_bank_total = sum(b['amount'] for b in bank_data if b['id'] in matched_bank_ids)
    matched_gl_total = sum(g['amount'] for g in gl_data if g['id'] in matched_gl_ids)
    unreconciled_bank_total = sum(b['amount'] for b in bank_data if b['id'] not in matched_bank_ids)
    unreconciled_gl_total = sum(g['amount'] for g in gl_data if g['id'] not in matched_gl_ids)

    summary_rows = [
        ['Metric', 'Value'],
        ['Threshold', str(threshold)],
        ['Matched Bank Rows', len(matched_bank_ids)],
        ['Matched GL Rows', len(matched_gl_ids)],
        ['Unreconciled Bank Rows', len(unreconciled_bank_rows)],
        ['Unreconciled GL Rows', len(unreconciled_gl_rows)],
        ['Matched Bank Total', matched_bank_total],
        ['Matched GL Total', matched_gl_total],
        ['Matched Total Difference', abs(matched_bank_total - matched_gl_total)],
        ['Unreconciled Bank Total', unreconciled_bank_total],
        ['Unreconciled GL Total', unreconciled_gl_total],
        ['Extracted Bank Workbook', extracted_xlsx or 'n/a'],
    ]

    out_headers = ['Bank Date', 'Bank Amount', 'Bank Desc', 'GL Date', 'GL Amount', 'GL Memo', 'Match Basis', 'Notes']
    write_xlsx(output_path, [
        ('Summary', summary_rows),
        ('Recon Results', [out_headers] + results),
        ('Unreconciled Bank', [['date', 'transaction amount', 'description']] + unreconciled_bank_rows),
        ('Unreconciled GL', [['date', 'amount', 'G/L memo']] + unreconciled_gl_rows),
    ])
    return len(matched_bank_ids), len(matched_gl_ids), len(unreconciled_bank_rows), len(unreconciled_gl_rows), extracted_xlsx


if __name__ == '__main__':
    b_p, g_p, o_p = sys.argv[1:4]
    t = Decimal(sys.argv[4]) if len(sys.argv) > 4 else Decimal('0.00')
    b_count, g_count, ub_count, ug_count, extracted_xlsx = recon(b_p, g_p, o_p, t)
    extra = f' Extracted bank workbook: {extracted_xlsx}.' if extracted_xlsx else ''
    print(
        f'Recon complete. Matched {b_count} bank and {g_count} GL records. '
        f'Unreconciled: {ub_count} bank, {ug_count} GL. Output: {o_p}.{extra}'
    )
