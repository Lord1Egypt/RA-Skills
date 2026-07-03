#!/usr/bin/env python3
"""
Push progress management for book-to-learn.
Parameterized by --book <slug> (each book has its own data dir).

Subcommands:
  status --book <slug>                     Show push progress.
  next --book <slug> [--force]             Get next card payload as JSON.
  mark --book <slug> <id> <status>         Update progress.json.
  weekday                                  Exit 0 if Mon-Fri else 1.
  list-books                               List all books set up.

All data lives under books/<slug>/.
"""
import json, os, sys, re, html, argparse, datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(SKILL_DIR, 'books')

def book_dir(slug):
    return os.path.join(BOOKS_DIR, slug)

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
    return d.weekday() < 5

def get_next_index(progress, index):
    last_id = progress.get('lastPushedId')
    items = index['items']
    if not last_id:
        return 0
    last_fn = 'card_%s.html' % last_id  # match filename format in index
    try:
        pos = items.index(last_fn)
    except ValueError:
        return 0
    nxt = pos + 1
    return None if nxt >= len(items) else nxt

def extract_card_id(filename):
    m = re.match(r'card_(.+)\.html', filename)
    return m.group(1) if m else None

def extract_text_from_html(htmlstr):
    """Extract visible text sections from a card HTML."""
    out = {}
    def grab(cls):
        m = re.search(r'<div class="%s">(.*?)</div>' % cls, htmlstr, flags=re.S)
        if not m: return ''
        if cls in ('expl', 'app'):
            paras = re.findall(r'<p>(.*?)</p>', m.group(1), flags=re.S)
            return '\n'.join(html.unescape(re.sub(r'<[^>]+>', '', p)).strip() for p in paras)
        return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    out['topic'] = grab('topic')
    out['coreIdea'] = grab('core')
    out['explanation'] = grab('expl')
    out['quote'] = grab('quote')
    out['application'] = grab('app')
    return out

def cmd_status(args):
    bd = book_dir(args.book)
    progress = load_json(os.path.join(bd, 'progress.json'))
    index = load_json(os.path.join(bd, 'index.json'))
    print('Book:', index.get('bookTitle'))
    print('Total cards:', index.get('totalCards'))
    print('Last pushed ID:', progress.get('lastPushedId'))
    print('Last push date:', progress.get('lastPushDate'))
    print('History entries:', len(progress.get('pushHistory', [])))
    nxt = get_next_index(progress, index)
    if nxt is None:
        print('Status: ALL CARDS PUSHED ✓')
    else:
        print('Next card:', index['items'][nxt], '(#%d)' % (nxt + 1))

def cmd_next(args):
    bd = book_dir(args.book)
    if not os.path.isdir(bd):
        print(json.dumps({'error': 'book not found: ' + args.book}, ensure_ascii=False))
        sys.exit(1)
    if not args.force and not is_workday():
        print(json.dumps({'skip': True, 'reason': 'weekend', 'date': today_str()}, ensure_ascii=False))
        return
    progress = load_json(os.path.join(bd, 'progress.json'))
    index = load_json(os.path.join(bd, 'index.json'))
    if not args.force and progress.get('lastPushDate') == today_str():
        print(json.dumps({'skip': True, 'reason': 'already_pushed_today', 'date': today_str()}, ensure_ascii=False))
        return
    nxt = get_next_index(progress, index)
    if nxt is None:
        print(json.dumps({'skip': True, 'reason': 'all_done', 'date': today_str()}, ensure_ascii=False))
        return
    filename = index['items'][nxt]
    card_id = extract_card_id(filename)
    card_path = os.path.join(bd, 'cards', filename)
    with open(card_path, 'r', encoding='utf-8') as f:
        htmlstr = f.read()
    sections = extract_text_from_html(htmlstr)
    items = load_json(os.path.join(bd, 'items.json'))
    item = next((it for it in items if it['id'] == card_id), {})
    config = load_json(os.path.join(bd, 'config.json'))
    payload = {
        'nextId': card_id,
        'filename': filename,
        'cardIndex': nxt + 1,
        'totalCards': index['totalCards'],
        'bookTitle': index.get('bookTitle', ''),
        'bookSlug': args.book,
        'chapter': item.get('chapter', ''),
        'topic': sections['topic'] or item.get('topic', ''),
        'coreIdea': sections['coreIdea'] or item.get('coreIdea', ''),
        'explanation': sections['explanation'] or item.get('explanation', ''),
        'quote': sections['quote'] or item.get('quote', ''),
        'application': sections['application'] or item.get('application', ''),
        'image': item.get('image', ''),
        'relatedLinks': item.get('relatedLinks', []),
        'terminology': item.get('terminology', []),
        'source': item.get('link', '') or index.get('bookSource', ''),
        'language': config.get('language', 'en'),
        'pushMethod': config.get('pushMethod', 'ima'),
        'date': today_str(),
        'bookDir': bd,
        'configPath': os.path.join(bd, 'config.json'),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

def cmd_mark(args):
    bd = book_dir(args.book)
    progress = load_json(os.path.join(bd, 'progress.json'))
    if args.status == 'success':
        progress['lastPushedId'] = args.id
        progress['lastPushDate'] = today_str()
        progress.setdefault('pushHistory', []).append({'id': args.id, 'date': today_str(), 'status': 'success'})
    else:
        progress.setdefault('pushHistory', []).append({'id': args.id, 'date': today_str(), 'status': args.status})
    save_json(os.path.join(bd, 'progress.json'), progress)
    print(json.dumps({'ok': True, 'marked': args.id, 'status': args.status}, ensure_ascii=False))

def cmd_weekday(args):
    sys.exit(0 if is_workday() else 1)

def cmd_list_books(args):
    if not os.path.isdir(BOOKS_DIR):
        print('No books set up yet.')
        return
    books = [d for d in os.listdir(BOOKS_DIR) if os.path.isdir(os.path.join(BOOKS_DIR, d))]
    if not books:
        print('No books set up yet.')
        return
    for slug in sorted(books):
        cfg_path = os.path.join(BOOKS_DIR, slug, 'config.json')
        title = slug
        if os.path.exists(cfg_path):
            title = load_json(cfg_path).get('bookTitle', slug)
        idx_path = os.path.join(BOOKS_DIR, slug, 'index.json')
        total = '?'
        if os.path.exists(idx_path):
            total = load_json(idx_path).get('totalCards', '?')
        prog_path = os.path.join(BOOKS_DIR, slug, 'progress.json')
        pushed = 0
        if os.path.exists(prog_path):
            p = load_json(prog_path)
            pushed = len(p.get('pushHistory', []))
        print(f'  {slug} | {title} | {pushed}/{total} pushed')

def main():
    ap = argparse.ArgumentParser(description='Book-to-learn push progress manager')
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('status'); s.add_argument('--book', required=True)
    n = sub.add_parser('next'); n.add_argument('--book', required=True); n.add_argument('--force', action='store_true')
    m = sub.add_parser('mark'); m.add_argument('--book', required=True); m.add_argument('id'); m.add_argument('status', choices=['success', 'fail'])
    sub.add_parser('weekday')
    sub.add_parser('list-books')
    args = ap.parse_args()
    {'status': cmd_status, 'next': cmd_next, 'mark': cmd_mark, 'weekday': cmd_weekday, 'list-books': cmd_list_books}.get(args.cmd, lambda a: ap.print_help())(args)

if __name__ == '__main__':
    main()
