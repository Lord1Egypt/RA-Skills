#!/usr/bin/env python3
"""
Open Music Theory — daily bilingual card pusher.

Subcommands:
  status              Show current push progress.
  next                Determine & output the next card payload as JSON (English + terminology).
  render <id> --zh F  Inject Chinese translations (from JSON file F) into the card's
                      translation-panel; write a bilingual card to delivered/.
  mark <id> <status>  Update progress.json after a push (success/fail).
  weekday             Exit 0 if today is a workday (Mon-Fri), else exit 1.

The translation itself (terminology verification via web + bilingual rendering) is
performed by the AI at push time; this script handles state, extraction & assembly.

All paths are relative to this script's directory.
"""
import json, os, sys, re, html, argparse, datetime, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE, 'cards')
DELIVERED_DIR = os.path.join(BASE, 'delivered')
INDEX_PATH = os.path.join(BASE, 'index.json')
PROGRESS_PATH = os.path.join(BASE, 'progress.json')
ITEMS_PATH = os.path.join(BASE, 'items.json')


def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(p, obj):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def today_str():
    return datetime.date.today().isoformat()

def is_workday(d=None):
    d = d or datetime.date.today()
    return d.weekday() < 5  # Mon=0..Fri=4


def get_next_index(progress, index):
    """Return the 0-based index in index['items'] of the next card to push."""
    last_id = progress.get('lastPushedId')
    items = index['items']
    if not last_id:
        return 0
    # find position of last_id
    last_fn = 'card_%s.html' % last_id
    try:
        pos = items.index(last_fn)
    except ValueError:
        return 0
    nxt = pos + 1
    if nxt >= len(items):
        return None  # all done
    return nxt

def extract_card_id(filename):
    m = re.match(r'card_(.+)\.html', filename)
    return m.group(1) if m else None

def extract_text_from_html(htmlstr):
    """Extract visible English text sections from a card HTML for translation."""
    out = {}
    # core idea
    m = re.search(r'<div class="core">(.*?)</div>', htmlstr, flags=re.S)
    out['coreIdeaEn'] = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    # explanation paragraphs
    m = re.search(r'<div class="expl">(.*?)</div>', htmlstr, flags=re.S)
    if m:
        paras = re.findall(r'<p>(.*?)</p>', m.group(1), flags=re.S)
        out['explanationEn'] = '\n'.join(html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in paras)
    else:
        out['explanationEn'] = ''
    # quote
    m = re.search(r'<div class="quote">(.*?)</div>', htmlstr, flags=re.S)
    out['quoteEn'] = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    # application
    m = re.search(r'<div class="app">(.*?)</div>', htmlstr, flags=re.S)
    if m:
        paras = re.findall(r'<p>(.*?)</p>', m.group(1), flags=re.S)
        out['applicationScenarios'] = '\n'.join(html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in paras)
    else:
        out['applicationScenarios'] = ''
    # topic
    m = re.search(r'<div class="topic">(.*?)</div>', htmlstr, flags=re.S)
    out['topic'] = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    return out


def cmd_status(args):
    progress = load_json(PROGRESS_PATH)
    index = load_json(INDEX_PATH)
    print('Book:', index.get('bookTitle'))
    print('Total cards:', index.get('totalCards'))
    print('Last pushed ID:', progress.get('lastPushedId'))
    print('Last push date:', progress.get('lastPushDate'))
    print('History entries:', len(progress.get('pushHistory', [])))
    nxt = get_next_index(progress, index)
    if nxt is None:
        print('Status: ALL CARDS PUSHED ✓')
    else:
        fn = index['items'][nxt]
        print('Next card:', fn, '(#%d)' % (nxt + 1))


def cmd_next(args):
    force = getattr(args, 'force', False)
    # workday guard (skip silently on weekends by emitting a marker)
    if not force and not is_workday():
        print(json.dumps({'skip': True, 'reason': 'weekend', 'date': today_str()}, ensure_ascii=False))
        return
    progress = load_json(PROGRESS_PATH)
    index = load_json(INDEX_PATH)
    # if already pushed today, skip
    if not force and progress.get('lastPushDate') == today_str():
        print(json.dumps({'skip': True, 'reason': 'already_pushed_today', 'date': today_str(),
                          'lastPushedId': progress.get('lastPushedId')}, ensure_ascii=False))
        return
    nxt = get_next_index(progress, index)
    if nxt is None:
        print(json.dumps({'skip': True, 'reason': 'all_done', 'date': today_str()}, ensure_ascii=False))
        return
    filename = index['items'][nxt]
    card_id = extract_card_id(filename)
    card_path = os.path.join(CARDS_DIR, filename)
    with open(card_path, 'r', encoding='utf-8') as f:
        htmlstr = f.read()
    sections = extract_text_from_html(htmlstr)
    # terminology from items.json
    items = load_json(ITEMS_PATH)
    item = next((it for it in items if it['id'] == card_id), {})
    payload = {
        'nextId': card_id,
        'filename': filename,
        'cardIndex': nxt + 1,
        'totalCards': index['totalCards'],
        'chapter': item.get('chapter', ''),
        'topic': sections['topic'] or item.get('topic', ''),
        'coreIdeaEn': sections['coreIdeaEn'],
        'explanationEn': sections['explanationEn'],
        'quoteEn': sections['quoteEn'],
        'applicationScenarios': sections['applicationScenarios'],
        'image': item.get('image', ''),
        'relatedLinks': item.get('relatedLinks', []),
        'terminology': item.get('terminology', []),
        'source': item.get('link', '') or index.get('bookSource', ''),
        'date': today_str(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_render(args):
    card_id = args.id
    zh_path = args.zh
    zh = load_json(zh_path)
    index = load_json(INDEX_PATH)
    filename = 'card_%s.html' % card_id
    card_path = os.path.join(CARDS_DIR, filename)
    with open(card_path, 'r', encoding='utf-8') as f:
        htmlstr = f.read()
    # build bilingual translation block to inject into #translation-panel
    parts = []
    parts.append('<div class="bi-wrap" style="text-align:left">')
    # terminology table
    terms = zh.get('terminologyZh', {})
    if terms:
        parts.append('<div style="margin-bottom:14px"><div style="font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:.7px;color:#ff4b4b;margin-bottom:8px">术语对照 / Terminology</div>')
        parts.append('<table style="width:100%;font-size:13px;border-collapse:collapse">')
        for en, cn in terms.items():
            parts.append('<tr><td style="padding:4px 8px 4px 0;color:#8a5a00;font-weight:600;white-space:nowrap">%s</td><td style="padding:4px 0;color:#444">%s</td></tr>' % (html.escape(en), html.escape(cn)))
        parts.append('</table></div>')

    def p_block(title_cn, title_en, text, color):
        if not text:
            return ''
        paras = ''.join('<p style="margin:0 0 8px 0">%s</p>' % html.escape(ln) for ln in text.split('\n') if ln.strip())
        return ('<div style="margin-bottom:14px">'
                '<div style="font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:.7px;color:%s;margin-bottom:6px">%s / %s</div>'
                '<div style="font-size:14.5px;color:#222;line-height:1.7">%s</div></div>') % (color, title_cn, title_en, paras)

    parts.append(p_block('核心观点', 'Core Idea', zh.get('coreIdeaZh', ''), '#58cc02'))
    parts.append(p_block('详细解释', 'Explanation', zh.get('explanationZh', ''), '#1cb0f6'))
    parts.append(p_block('金句', 'Key Quote', zh.get('quoteZh', ''), '#a560e8'))
    parts.append(p_block('应用场景', 'Application Scenarios', zh.get('applicationZh', ''), '#ff9600'))
    note = zh.get('note', '')
    if note:
        parts.append('<div style="font-size:12px;color:#8a8a8a;margin-top:10px;border-top:1px solid #eee;padding-top:8px">%s</div>' % html.escape(note))
    parts.append('</div>')
    bi_html = ''.join(parts)
    # replace the placeholder inside translation-panel
    new_html = re.sub(
        r'(<div class="translation-panel"[^>]*id="translation-panel">).*?(</div>)',
        r'\1%s\2' % bi_html.replace('\\', r'\\'),
        htmlstr, count=1, flags=re.S)
    # also restyle translation-panel to solid border when filled
    new_html = new_html.replace('border:2px dashed #d7dbe2', 'border:1px solid #e5e7eb;background:#fff')
    os.makedirs(DELIVERED_DIR, exist_ok=True)
    out_name = 'card_%s_bilingual_%s.html' % (card_id, today_str())
    out_path = os.path.join(DELIVERED_DIR, out_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(json.dumps({'ok': True, 'file': out_path, 'card_id': card_id, 'date': today_str()}, ensure_ascii=False))


def cmd_mark(args):
    card_id = args.id
    status = args.status
    progress = load_json(PROGRESS_PATH)
    if status == 'success':
        progress['lastPushedId'] = card_id
        progress['lastPushDate'] = today_str()
        progress.setdefault('pushHistory', []).append({'id': card_id, 'date': today_str(), 'status': 'success'})
    else:
        progress.setdefault('pushHistory', []).append({'id': card_id, 'date': today_str(), 'status': status})
    save_json(PROGRESS_PATH, progress)
    print(json.dumps({'ok': True, 'marked': card_id, 'status': status, 'lastPushedId': progress.get('lastPushedId')}, ensure_ascii=False))


def cmd_weekday(args):
    sys.exit(0 if is_workday() else 1)


def main():
    ap = argparse.ArgumentParser(description='OMT daily bilingual card pusher')
    sub = ap.add_subparsers(dest='cmd')
    sub.add_parser('status')
    p_next = sub.add_parser('next')
    p_next.add_argument('--force', action='store_true', help='ignore workday/already-pushed guards')
    r = sub.add_parser('render')
    r.add_argument('id')
    r.add_argument('--zh', required=True)
    m = sub.add_parser('mark')
    m.add_argument('id')
    m.add_argument('status', choices=['success', 'fail'])
    sub.add_parser('weekday')
    args = ap.parse_args()
    if args.cmd == 'status':
        cmd_status(args)
    elif args.cmd == 'next':
        cmd_next(args)
    elif args.cmd == 'render':
        cmd_render(args)
    elif args.cmd == 'mark':
        cmd_mark(args)
    elif args.cmd == 'weekday':
        cmd_weekday(args)
    else:
        ap.print_help()

if __name__ == '__main__':
    main()
