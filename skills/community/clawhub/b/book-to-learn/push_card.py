#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push progress management for book-to-learn.

Parameterized by --book <slug> (each book has its own data dir).

Subcommands:
  status --book <slug>                     Show push progress.
  list-next --book <slug> [--n N]          Preview the next N cards (no lock, no side effect).
  next --book <slug> [--n N] [--force]     Get next card payload (or N payloads) as JSON.
  mark --book <slug> <id> [<id>…] success  Update progress (batch: several ids at once).
  weekday                                  Exit 0 if Mon-Fri else 1.
  list-books                               List all sources set up.

All data lives under books/<slug>/.

Design notes:
- The content source (items.json **or** items/ split layout) is the single source of
  truth; cards/*.html are preview-only and are NEVER parsed to recover content
  (historically this silently dropped markdown URLs and desynced from items.json).
- A lock file guards next->mark so a re-triggered cron run cannot push the same card
  twice in one day. Batch mode (--n > 1) is explicit user intent, so it bypasses the
  day/weekend guards and the lock, and must be marked with all ids afterwards.
- mark fail does not inflate push statistics: only successes count.
- **首次启动门禁**：config 里有 `confirmed` 块且存在未确认项时，`next` 拒绝发载荷
  （避免「还没跟用户确认配置就开始拆解/推送」）。1.4.x 的老配置没有该字段，不拦截。
"""
import argparse
import datetime
import json
import os
import re
import sys
import tempfile

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# 数据根目录：默认在 skill 目录下的 books/；可用环境变量 B2L_DATA_DIR 改到持久化工作目录
BOOKS_DIR = os.environ.get('B2L_DATA_DIR') or os.path.join(SKILL_DIR, 'books')
sys.path.insert(0, SKILL_DIR)
import items_io  # noqa: E402  （分章节/单文件两种 items 布局）


class StaleProgress(ValueError):
    """lastPushedId 不在 index.json 中（索引被重建/进度被污染），需要人工核对。"""


def book_dir(slug):
    return os.path.join(BOOKS_DIR, slug)


def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(p, obj):
    """原子写：先写临时文件再 os.replace，进程中途被杀不会留下截断的 JSON。"""
    d = os.path.dirname(os.path.abspath(p))
    fd, tmp = tempfile.mkstemp(prefix='.tmp_', dir=d)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        os.replace(tmp, p)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _now():
    """当前时间。支持环境变量 B2L_TZ 指定时区（如 Asia/Shanghai），
    避免宿主机为 UTC 时「当天」翻转时刻与用户实际时区不一致。"""
    tz_name = os.environ.get('B2L_TZ')
    if tz_name:
        try:
            from zoneinfo import ZoneInfo
            return datetime.datetime.now(ZoneInfo(tz_name))
        except Exception:
            pass
    return datetime.datetime.now()


def today_str():
    return _now().date().isoformat()


def is_workday(d=None):
    d = d or _now().date()
    return d.weekday() < 5


def out(obj):
    """Print a JSON line (always parseable by the cron agent)."""
    print(json.dumps(obj, ensure_ascii=False))


def check_unique_ids(items):
    """Raise ValueError listing duplicate ids in the content source."""
    dups = items_io.check_unique_ids(items)
    if dups:
        raise ValueError('duplicate ids in content source: %s' % ', '.join(map(str, dups)))


def pending_confirmations(cfg):
    """返回尚未确认的配置项。老配置（无 confirmed 块）返回空，保持兼容。"""
    conf = (cfg or {}).get('confirmed')
    if not conf:
        return []
    return [k for k, v in (conf.get('items') or {}).items() if not v]


def get_next_index(progress, index):
    last_id = progress.get('lastPushedId')
    items = index['items']
    if not last_id:
        return 0
    last_fn = 'card_%s.html' % last_id  # match filename format in index
    try:
        pos = items.index(last_fn)
    except ValueError:
        # 索引被重建导致 id 变化、或进度被污染（如误把文件名当 id 写入）：
        # 静默从第 1 张重推会整本书重复推送，必须停下来让人核对。
        raise StaleProgress(
            'lastPushedId=%r 不在 index.json 中（索引重建过？progress.json 被污染？）。'
            '请人工核对 books 目录下 progress.json 与 index.json 后再继续' % last_id)
    nxt = pos + 1
    return None if nxt >= len(items) else nxt


def extract_card_id(filename):
    m = re.match(r'card_(.+)\.html', filename)
    return m.group(1) if m else None


def acquire_lock(bd, card_id, force=False):
    """Return True if we may push card_id now; False if another run is
    mid-flight (lock exists and is fresh) or this card was already
    delivered today. force=True 时无条件接管锁（手动重推的逃生门）。"""
    lock_path = os.path.join(bd, '.push_lock')
    today = today_str()
    if not force and os.path.exists(lock_path):
        try:
            lock = load_json(lock_path)
        except Exception:
            lock = {}
        # stale lock from a previous day -> takeover
        if lock.get('date') != today:
            os.remove(lock_path)
        else:
            if lock.get('cardId') == card_id and lock.get('done'):
                return False  # already delivered today
            if not lock.get('done'):
                return False  # another run mid-flight today
            os.remove(lock_path)
    save_json(lock_path, {'date': today, 'cardId': card_id, 'done': False,
                          'ts': datetime.datetime.now().isoformat(timespec='seconds')})
    return True


def release_lock(bd, card_id, done=True):
    lock_path = os.path.join(bd, '.push_lock')
    save_json(lock_path, {'date': today_str(), 'cardId': card_id, 'done': done,
                          'ts': datetime.datetime.now().isoformat(timespec='seconds')})


def _format_marker(template, idx, seq, total):
    """格式化 marker；模板含未知占位符时给出可定位的错误（而不是笼统的 bad_index_entry）。"""
    try:
        return template.format(idx=idx, seq=seq, total=total)
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError('bad_marker_template: %r 含未知占位符 %s（可用：{idx}/{seq}/{total}）'
                         % (template, e))


def build_payload(bd, book_slug, card_id, filename, nxt):
    """Build a card payload from the content source (single source of truth)."""
    items = items_io.load_items(bd)
    item = items_io.find_item(items, card_id)
    if item is None:
        raise ValueError('card id %r not found in content source (stale index.json? '
                         're-run gen-index)' % card_id)
    index = load_json(os.path.join(bd, 'index.json'))
    config = load_json(os.path.join(bd, 'config.json'))
    naming = config.get('naming') or {}
    payload = {
        'nextId': card_id,
        'filename': filename,
        'cardIndex': nxt + 1,
        'totalCards': index.get('totalCards', '?'),
        'bookTitle': index.get('bookTitle', ''),
        'bookSlug': book_slug,
        'chapter': item.get('chapter', ''),
        'topic': item.get('topic', ''),
        'coreIdea': item.get('coreIdea', ''),
        'explanation': item.get('explanation', ''),
        'quote': item.get('quote', ''),
        'application': item.get('application', ''),
        'points': item.get('points', []),          # 长图引擎用：要点列表（可选）
        'image': item.get('image', ''),
        'relatedLinks': item.get('relatedLinks', []),
        'terminology': item.get('terminology', []),
        'source': item.get('link', '') or index.get('bookSource', ''),
        'language': config.get('language', 'en'),
        'pushMethod': config.get('pushMethod', 'local'),
        'cardType': config.get('cardType', config.get('template', 'pdf-standard')),
        'date': today_str(),
        'bookDir': bd,
        'configPath': os.path.join(bd, 'config.json'),
        # 双轨编号：manifestIdx = 内容源中的绝对序号（跳过也占号），用于卡片标记与笔记
        'manifestIdx': item.get('idx', nxt + 1),
        'marker': _format_marker(naming.get('markerTemplate') or '{idx}/{total}',
                                 item.get('idx', nxt + 1), nxt + 1,
                                 index.get('totalCards', '?')),
        'sectionZh': item.get('sectionZh', naming.get('sectionZh', '')),
    }
    assets_dir = os.path.join(bd, 'raw', 'imgs')
    if os.path.isdir(assets_dir):
        payload['assetsDir'] = assets_dir
    return payload


def cmd_status(args):
    bd = book_dir(args.book)
    progress = load_json(os.path.join(bd, 'progress.json'))
    index = load_json(os.path.join(bd, 'index.json'))
    print('Book:', index.get('bookTitle'))
    print('Total cards:', index.get('totalCards'))
    print('Last pushed ID:', progress.get('lastPushedId'))
    print('Last push date:', progress.get('lastPushDate'))
    succ = [h for h in progress.get('pushHistory', []) if h.get('status') == 'success']
    print('Successful pushes:', len(succ))
    print('History entries:', len(progress.get('pushHistory', [])))
    nxt = get_next_index(progress, index)
    if nxt is None:
        print('Status: ALL CARDS PUSHED [DONE]')
    else:
        print('Next card:', index['items'][nxt], '(#%d)' % (nxt + 1))


def _collect(progress, index, n):
    """从当前位置起，取最多 n 个连续卡片 → [(card_id, filename, pos), …]"""
    start = get_next_index(progress, index)
    if start is None:
        return []
    picked = []
    for k in range(n):
        pos = start + k
        if pos >= len(index['items']):
            break
        fn = index['items'][pos]
        cid = extract_card_id(fn)
        if not cid:
            break
        picked.append((cid, fn, pos))
    return picked


def cmd_list_next(args):
    """只预览接下来 N 张（不加锁、不改进度），用于「每次推送后列出接下来 N 张」。"""
    bd = book_dir(args.book)
    index = load_json(os.path.join(bd, 'index.json'))
    progress = load_json(os.path.join(bd, 'progress.json'))
    picked = _collect(progress, index, args.n)
    out({'ok': True, 'count': len(picked),
         'cards': [{'id': cid, 'cardIndex': pos + 1} for cid, fn, pos in picked]})


def cmd_next(args):
    bd = book_dir(args.book)
    if not os.path.isdir(bd):
        out({'skip': True, 'reason': 'book_not_found', 'book': args.book})
        sys.exit(1)

    # —— 首次启动门禁：配置未确认前不发载荷 ——
    cfg_path = os.path.join(bd, 'config.json')
    cfg = load_json(cfg_path) if os.path.exists(cfg_path) else {}
    pending = pending_confirmations(cfg)
    if pending and not args.force:
        out({'skip': True, 'reason': 'config_not_confirmed', 'pending': pending,
             'hint': '先与用户逐项确认并发回 config.confirmed.items，或显式 --force'})
        sys.exit(1)

    batch = max(1, args.n or 1)
    if batch == 1:
        if not args.force and not is_workday():
            out({'skip': True, 'reason': 'weekend', 'date': today_str()})
            return
        if not args.force and load_json(os.path.join(bd, 'progress.json')).get('lastPushDate') == today_str():
            out({'skip': True, 'reason': 'already_pushed_today', 'date': today_str()})
            return

    progress = load_json(os.path.join(bd, 'progress.json'))
    index = load_json(os.path.join(bd, 'index.json'))
    picked = _collect(progress, index, batch)
    if not picked:
        out({'skip': True, 'reason': 'all_done', 'date': today_str()})
        return
    # guard against duplicate ids (cards would silently overwrite each other)
    try:
        check_unique_ids(items_io.load_items(bd))
    except ValueError as e:
        out({'skip': True, 'reason': 'duplicate_ids', 'error': str(e)})
        sys.exit(1)

    if batch == 1:
        card_id, filename, pos = picked[0]
        # lock: block a second same-day run mid-flight or after delivery.
        # --force 是文档化的手动重推逃生门：无条件接管锁。
        if not acquire_lock(bd, card_id, force=args.force):
            lock_path = os.path.join(bd, '.push_lock')
            lock = load_json(lock_path) if os.path.exists(lock_path) else {}
            reason = 'already_pushed_today' if lock.get('done') else 'push_in_progress'
            out({'skip': True, 'reason': reason, 'cardId': lock.get('cardId', ''),
                 'date': today_str()})
            return
        try:
            payload = build_payload(bd, args.book, card_id, filename, pos)
        except ValueError as e:
            release_lock(bd, card_id, done=False)
            out({'skip': True, 'reason': 'card_not_found', 'error': str(e)})
            sys.exit(1)
        out(payload)
        return

    # —— 批量：显式用户意图，跳过 当日/周末 守卫与单卡锁（需要用 mark 全部回写）——
    payloads = []
    for card_id, filename, pos in picked:
        try:
            payloads.append(build_payload(bd, args.book, card_id, filename, pos))
        except ValueError as e:
            out({'skip': True, 'reason': 'card_not_found', 'cardId': card_id, 'error': str(e)})
            sys.exit(1)
    out({'ok': True, 'batch': True, 'count': len(payloads), 'payloads': payloads,
         'hint': '全部推完后用 mark --book %s --ids %s success 一次性回写'
                 % (args.book, ','.join(p['nextId'] for p in payloads))})


def cmd_mark(args):
    bd = book_dir(args.book)
    ids = []
    if getattr(args, 'ids', None):
        ids += [x.strip() for x in args.ids.split(',') if x.strip()]
    if getattr(args, 'id', None):
        ids += args.id
    if not ids:
        out({'ok': False, 'error': '需要至少一个卡片 id'})
        sys.exit(1)
    idx_path = os.path.join(bd, 'index.json')
    if not os.path.exists(idx_path):
        out({'ok': False, 'error': 'index.json 不存在，先运行 book_setup.py gen-index <slug>'})
        sys.exit(1)
    # —— id 白名单校验：误传文件名（如 card_ch01-02.html）会静默重置整本书进度 ——
    index = load_json(idx_path)
    known = set(index.get('items') or [])
    bad = [cid for cid in ids if ('card_%s.html' % cid) not in known]
    if bad:
        out({'ok': False, 'error': '未知卡片 id：%s（应传 items.json 里的 id，如 ch01-02，'
             '不是文件名/其他字符串）。可用 id 见 index.json' % ', '.join(map(repr, bad))})
        sys.exit(1)
    progress = load_json(os.path.join(bd, 'progress.json'))
    for cid in ids:
        if args.status == 'success':
            progress.setdefault('pushHistory', []).append(
                {'id': cid, 'date': today_str(), 'status': 'success'})
            release_lock(bd, cid, done=True)
        else:
            # failure: keep history for audit but do NOT touch lastPushedId/lastPushDate
            progress.setdefault('pushHistory', []).append(
                {'id': cid, 'date': today_str(), 'status': args.status})
            release_lock(bd, cid, done=False)
    if args.status == 'success':
        # lastPushedId 必须取「内容源中位置最靠后」的那个（与传参顺序无关），
        # 否则乱序回写（mark --ids c,a,b）会让 get_next_index 回退、已推卡重推。
        order = {fn: i for i, fn in enumerate(index.get('items') or [])}
        last = max(ids, key=lambda c: order.get('card_%s.html' % c, -1))
        progress['lastPushedId'] = last
        progress['lastPushDate'] = today_str()
    save_json(os.path.join(bd, 'progress.json'), progress)
    out({'ok': True, 'marked': ids, 'status': args.status, 'count': len(ids),
         'lastPushedId': progress.get('lastPushedId')})


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
        layout = items_io.describe_layout(os.path.join(BOOKS_DIR, slug))
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
            pushed = len([h for h in p.get('pushHistory', []) if h.get('status') == 'success'])
        print('  %s | %s | %s/%s pushed | items=%s' % (slug, title, pushed, total, layout))


def main():
    ap = argparse.ArgumentParser(description='Book-to-learn push progress manager')
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('status'); s.add_argument('--book', required=True)
    ln = sub.add_parser('list-next'); ln.add_argument('--book', required=True)
    ln.add_argument('--n', type=int, default=10)
    n = sub.add_parser('next')
    n.add_argument('--book', required=True)
    n.add_argument('--force', action='store_true')
    n.add_argument('--n', type=int, default=1, help='批量取 N 张（>1 时跳过当日/周末守卫）')
    m = sub.add_parser('mark')
    m.add_argument('--book', required=True)
    m.add_argument('id', nargs='*', help='一个或多个卡片 id')
    m.add_argument('status', choices=['success', 'fail'])
    m.add_argument('--ids', help='逗号分隔的 id 列表（批量）')
    sub.add_parser('weekday')
    sub.add_parser('list-books')
    args = ap.parse_args()
    try:
        {'status': cmd_status, 'list-next': cmd_list_next, 'next': cmd_next,
         'mark': cmd_mark, 'weekday': cmd_weekday, 'list-books': cmd_list_books}.get(
            args.cmd, lambda a: ap.print_help())(args)
    except StaleProgress as e:
        out({'skip': True, 'reason': 'stale_progress', 'error': str(e),
             'hint': '进度与索引不一致，请人工核对，切勿直接重推'})
        sys.exit(1)
    except KeyError as e:
        out({'skip': True, 'reason': 'bad_index_entry', 'error': str(e)})
        sys.exit(1)
    except Exception as e:  # keep cron runs diagnosable
        out({'skip': True, 'reason': 'error', 'error': '%s: %s' % (type(e).__name__, e)})
        sys.exit(1)


if __name__ == '__main__':
    main()
