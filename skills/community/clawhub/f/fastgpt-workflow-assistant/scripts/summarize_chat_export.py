"""Read-only CSV/XLSX inventory. Never evaluates spreadsheet cells or log content."""
import argparse, collections, csv, hashlib, json, pathlib, re, zipfile
from xml.etree import ElementTree as ET

def decode_details(value):
    item = value
    for _ in range(4):
        if isinstance(item, list):
            return item
        if not isinstance(item, str):
            break
        try:
            item = json.loads(item)
        except (ValueError, TypeError):
            if item.startswith('"') and item.endswith('"') and '""' in item:
                item = item[1:-1].replace('""', '"')
            else:
                break
    raise ValueError('conversation details are not a JSON array')

def read_sheets(file):
    if file.suffix.lower() == '.csv':
        raw = file.read_bytes()
        for encoding in ['utf-8-sig', 'gb18030']:
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError('unsupported CSV encoding')
        import io
        return [('CSV', list(csv.reader(io.StringIO(text, newline=''))))]
    if file.suffix.lower() != '.xlsx':
        raise ValueError('supported: CSV/XLSX; convert legacy XLS before analysis')
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(file) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
                strings.append(''.join(si.itertext()))
        rels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        result = []
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet', ns):
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = rels[rid]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            rows = []
            for row in ET.fromstring(z.read(target)).findall('m:sheetData/m:row', ns):
                values = []
                for c in row:
                    letters = re.match('[A-Z]+', c.attrib.get('r', 'A')).group()
                    col = 0
                    for letter in letters:
                        col = col * 26 + ord(letter) - 64
                    while len(values) < col:
                        values.append('')
                    v = c.find('m:v', ns)
                    val = v.text or '' if v is not None else ''
                    if c.attrib.get('t') == 's':
                        val = strings[int(val)]
                    elif c.attrib.get('t') == 'inlineStr':
                        val = ''.join(t.text or '' for t in c.findall('.//m:t', ns))
                    values[col - 1] = val  # cached values only; no formula execution
                rows.append(values)
            result.append((sheet.attrib['name'], rows))
        return result

def summarize(file):
    report = {'source_sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'sheets': [], 'warning': 'Inventory only; no semantic failure rate. Last conversation date is not message time.'}
    for name, rows in read_sheets(file):
        if not rows:
            continue
        header = rows[0]
        col = next((i for i, h in enumerate(header) if h in ['对话详情', 'conversation', 'messages']), None)
        date_col = next((i for i, h in enumerate(header) if h in ['最后对话时间', 'last_time']), None)
        stats = {'sheet': name, 'rows': len(rows)-1, 'parsed_sessions': 0, 'messages': 0, 'attachments': 0, 'empty_text_messages': 0, 'column_mismatch_rows': [], 'unparsed_rows': [], 'date_min': None, 'date_max': None}
        dates = []
        for rowno, row in enumerate(rows[1:], 2):
            if len(row) != len(header):
                stats['column_mismatch_rows'].append(rowno)
            if date_col is not None and date_col < len(row) and re.match(r'^\d{4}-\d{2}-\d{2}', row[date_col]):
                dates.append(row[date_col])
            try:
                if col is None:
                    raise ValueError('missing conversation column')
                messages = decode_details(row[col])
                stats['parsed_sessions'] += 1
                stats['messages'] += len(messages)
                for msg in messages:
                    values = msg.get('value', []) if isinstance(msg, dict) else []
                    stats['attachments'] += sum('file' in v for v in values if isinstance(v, dict))
                    if not values or all(not v.get('text', {}).get('content', '').strip() and 'file' not in v for v in values if isinstance(v, dict)):
                        stats['empty_text_messages'] += 1
            except (ValueError, IndexError, TypeError, AttributeError):
                stats['unparsed_rows'].append(rowno)
        if dates:
            stats['date_min'], stats['date_max'] = min(dates), max(dates)
        report['sheets'].append(stats)
    return report

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=pathlib.Path)
    p.add_argument('--output', type=pathlib.Path, required=True)
    args = p.parse_args()
    args.output.write_text(json.dumps(summarize(args.input), ensure_ascii=False, indent=2), encoding='utf-8')
