#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import time
from pathlib import Path
from typing import Any

CONTACT_RE = re.compile(r'(?:\+?\d[\d\s\-().]{8,}\d)|(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})')
ISSUE_KEYWORDS = {
    'appointment': ['randevu', 'appointment', 'slot', 'termin'],
    'documents': ['evrak', 'document', 'belge', 'dosya'],
    'rejection': ['red', 'reddedildi', 'refusal', 'ret'],
    'delay': ['gecik', 'bekli', 'delay', 'uzadı'],
    'passport': ['pasaport', 'passport'],
}


def now_ms() -> int:
    return int(time.time() * 1000)


def now_iso() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def resolve_config(config_path: Path) -> dict[str, Any]:
    cfg = load_json(config_path)
    cfg['statePath'] = str(Path(cfg.get('statePath') or config_path.resolve().parent.parent / 'state' / 'chrome-cdp-browser-operator-state.json'))
    cfg['outputDir'] = str(Path(cfg.get('outputDir') or config_path.resolve().parent.parent / 'outputs' / 'chrome-cdp-browser-operator'))
    Path(cfg['outputDir']).mkdir(parents=True, exist_ok=True)
    Path(cfg['statePath']).parent.mkdir(parents=True, exist_ok=True)
    return cfg


def normalize_text(value: str) -> str:
    return ' '.join((value or '').split()).strip()


def classify_issue(text: str) -> str:
    lowered = normalize_text(text).lower()
    for label, keywords in ISSUE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                return label
    return 'general'


def detect_contacts(text: str) -> list[str]:
    return sorted(set(match.group(0).strip() for match in CONTACT_RE.finditer(text or '')))


def score_candidate(text: str) -> int:
    issue = classify_issue(text)
    score = 1 if issue != 'general' else 0
    lowered = normalize_text(text).lower()
    if '?' in text:
        score += 1
    if any(token in lowered for token in ['yardım', 'help', 'ne yap', 'sorun', 'problem', 'reddedildi', 'bulamıyorum']):
        score += 2
    return score


def build_public_reply(text: str, website_url: str) -> str:
    issue = classify_issue(text)
    if issue == 'appointment':
        return f'Benzer durumlarda doğru adım detaylara göre değişebiliyor. İsterseniz {website_url} üzerinden kısa bilgi bırakın, ekip size daha net yönlendirme paylaşsın.'
    if issue == 'rejection':
        return f'Böyle durumlarda bağlama göre farklı yollar çıkabiliyor. Dilerseniz {website_url} üzerinden kısa bilgi bırakın, ekip size uygun bir sonraki adımı paylaşsın.'
    if issue == 'documents':
        return f'Küçük ayrıntılar sonucu etkileyebiliyor. İsterseniz {website_url} üzerinden kısa bilgi bırakın, ekip bunu daha net değerlendirsin.'
    return f'Detaylar netleşince daha doğru yönlendirme yapılabiliyor. İsterseniz {website_url} üzerinden kısa bilgi bırakın, ekip sizinle paylaşsın.'


class JsonStore:
    def __init__(self, path: Path):
        self.path = path
        self.data = load_json(path)
        self.data.setdefault('version', 1)
        self.data.setdefault('repliedTweets', {})

    def save(self) -> None:
        write_json(self.path, self.data)

    def is_recent(self, tweet_id: str, cooldown_hours: int) -> bool:
        ts = self.data.setdefault('repliedTweets', {}).get(tweet_id)
        if ts is None:
            return False
        return now_ms() - int(ts) < cooldown_hours * 60 * 60 * 1000

    def mark_replied(self, tweet_id: str) -> None:
        self.data.setdefault('repliedTweets', {})[tweet_id] = now_ms()


def notify(cfg: dict[str, Any], text: str) -> None:
    telegram = cfg.get('telegram') or {}
    if not telegram.get('enabled'):
        return
    target = str(telegram.get('target') or '').strip()
    if not target:
        return
    cmd = ['openclaw', 'message', 'send', '--channel', str(telegram.get('channel') or 'telegram'), '--target', target, '-m', text]
    account = str(telegram.get('account') or '').strip()
    if account:
        cmd.extend(['--account', account])
    subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)


def import_playwright():
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError  # type: ignore
        return sync_playwright, PlaywrightTimeoutError
    except Exception as exc:
        raise RuntimeError('playwright_not_installed: run `pip install playwright` and optionally `python -m playwright install chromium` when using bundled browsers') from exc


class BrowserSession:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self._pw = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        sync_playwright, _ = import_playwright()
        self._pw = sync_playwright().start()
        cdp_url = str(self.cfg.get('cdpUrl') or '').strip()
        fallback = self.cfg.get('launchFallback') or {}
        if cdp_url:
            self.browser = self._pw.chromium.connect_over_cdp(cdp_url)
            self.context = self.browser.contexts[0] if self.browser.contexts else self.browser.new_context()
        elif fallback.get('enabled'):
            user_data_dir = str(fallback.get('userDataDir') or '')
            executable_path = str(fallback.get('executablePath') or '') or None
            args = []
            profile_directory = str(fallback.get('profileDirectory') or '').strip()
            if profile_directory:
                args.append(f'--profile-directory={profile_directory}')
            self.context = self._pw.chromium.launch_persistent_context(user_data_dir=user_data_dir, executable_path=executable_path, headless=False, args=args)
            self.browser = self.context.browser
        else:
            raise RuntimeError('no_browser_connection_mode_configured')
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.context and hasattr(self.context, 'close'):
                self.context.close()
        except Exception:
            pass
        try:
            if self.browser and hasattr(self.browser, 'close'):
                self.browser.close()
        except Exception:
            pass
        try:
            if self._pw:
                self._pw.stop()
        except Exception:
            pass


def sleep_range(min_ms: int, max_ms: int) -> None:
    time.sleep(random.uniform(min_ms, max_ms) / 1000.0)


def locate_visible(page, selectors: list[str]):
    for selector in selectors:
        locator = page.locator(selector)
        if locator.count() > 0:
            return locator.first
    return None


def human_click(page, locator) -> None:
    box = locator.bounding_box()
    if not box:
        locator.click(timeout=5000)
        return
    target_x = box['x'] + box['width'] * random.uniform(0.35, 0.65)
    target_y = box['y'] + box['height'] * random.uniform(0.35, 0.65)
    start_x, start_y = random.uniform(0, 50), random.uniform(0, 50)
    steps = random.randint(12, 20)
    for step in range(steps):
        ratio = (step + 1) / steps
        page.mouse.move(start_x + (target_x - start_x) * ratio, start_y + (target_y - start_y) * ratio, steps=1)
        sleep_range(8, 18)
    page.mouse.click(target_x, target_y)
    sleep_range(120, 260)


def human_type(page, locator, text: str) -> None:
    human_click(page, locator)
    try:
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
    except Exception:
        pass
    for char in text:
        page.keyboard.type(char, delay=random.randint(40, 120))
    sleep_range(100, 220)


def open_x_home(session: BrowserSession):
    session.page.goto(str(session.cfg.get('baseUrl') or 'https://x.com/home'), wait_until='domcontentloaded')
    sleep_range(600, 1200)


def maybe_click_latest(page) -> None:
    locator = locate_visible(page, [
        "a[role='tab']:has-text('Latest')",
        "a[role='tab']:has-text('Son')",
        "a[href*='f=live']",
    ])
    if locator:
        try:
            human_click(page, locator)
            sleep_range(600, 1100)
        except Exception:
            pass


def extract_tweet_items(page, keyword: str, max_items: int) -> list[dict[str, Any]]:
    items = []
    articles = page.locator("article[data-testid='tweet']")
    count = min(articles.count(), max_items)
    seen = set()
    for idx in range(count):
        article = articles.nth(idx)
        try:
            text = article.inner_text(timeout=3000)
            href = article.locator("a[href*='/status/']").first.get_attribute('href', timeout=3000)
        except Exception:
            continue
        if not href:
            continue
        url = href if href.startswith('http') else f'https://x.com{href}'
        match = re.search(r'/([^/]+)/status/(\d+)', url)
        if not match:
            continue
        username, tweet_id = match.group(1), match.group(2)
        if tweet_id in seen:
            continue
        seen.add(tweet_id)
        items.append({
            'tweetId': tweet_id,
            'url': url,
            'username': username,
            'text': normalize_text(text),
            'keyword': keyword,
        })
    return items


def search_keyword(session: BrowserSession, keyword: str, max_items: int) -> list[dict[str, Any]]:
    open_x_home(session)
    search_box = locate_visible(session.page, [
        "input[data-testid='SearchBox_Search_Input']",
        "input[aria-label='Search query']",
    ])
    if not search_box:
        raise RuntimeError('search_box_not_found')
    human_type(session.page, search_box, keyword)
    session.page.keyboard.press('Enter')
    sleep_range(900, 1600)
    maybe_click_latest(session.page)
    sleep_range(700, 1300)
    return extract_tweet_items(session.page, keyword, max_items)


def post_reply(session: BrowserSession, tweet_url: str, text: str) -> dict[str, Any]:
    session.page.goto(tweet_url, wait_until='domcontentloaded')
    sleep_range(800, 1400)
    reply_button = locate_visible(session.page, [
        "[data-testid='reply']",
        "button[aria-label*='Reply']",
        "div[role='button'][aria-label*='Reply']",
    ])
    if not reply_button:
        raise RuntimeError('reply_button_not_found')
    human_click(session.page, reply_button)
    sleep_range(700, 1200)
    textarea = locate_visible(session.page, [
        "div[data-testid='tweetTextarea_0']",
        "div[role='textbox'][data-testid='tweetTextarea_0']",
        "div[role='textbox']",
    ])
    if not textarea:
        raise RuntimeError('reply_textarea_not_found')
    human_type(session.page, textarea, text)
    send_button = locate_visible(session.page, [
        "button[data-testid='tweetButtonInline']",
        "button[data-testid='tweetButton']",
    ])
    if not send_button:
        raise RuntimeError('reply_send_button_not_found')
    human_click(session.page, send_button)
    sleep_range(900, 1500)
    return {'ok': True, 'tweetUrl': tweet_url}


def write_bundle(cfg: dict[str, Any], stem: str, payload: dict[str, Any]) -> Path:
    out = Path(cfg['outputDir']) / f'{stem}-{time.strftime("%Y%m%d-%H%M%S")}.json'
    write_json(out, payload)
    return out


def run_check(config_path: Path) -> dict[str, Any]:
    cfg = resolve_config(config_path)
    with BrowserSession(cfg) as session:
        title = session.page.title()
        url = session.page.url
    return {'ok': True, 'title': title, 'url': url}


def run_search(config_path: Path, keyword: str | None, max_items: int) -> dict[str, Any]:
    cfg = resolve_config(config_path)
    keywords = [keyword] if keyword else list(cfg.get('keywords') or [])
    with BrowserSession(cfg) as session:
        items = []
        for term in keywords:
            items.extend(search_keyword(session, term, max_items=max_items))
    out_path = write_bundle(cfg, 'browser-search', {'generatedAt': now_iso(), 'items': items})
    return {'generatedAt': now_iso(), 'itemCount': len(items), 'outputPath': str(out_path)}


def run_cycle(config_path: Path, apply: bool) -> dict[str, Any]:
    cfg = resolve_config(config_path)
    state = JsonStore(Path(cfg['statePath']))
    cooldown_hours = int(cfg.get('replyCooldownHours', 72) or 72)
    website_url = str(cfg.get('websiteUrl') or 'https://example.com').rstrip('/')
    max_per_keyword = int(cfg.get('maxTweetsPerKeyword', 8) or 8)
    max_replies = int(cfg.get('maxRepliesPerCycle', 3) or 3)
    allow_public_reply = bool(cfg.get('allowPublicReply'))
    drafts = []
    applied = []
    with BrowserSession(cfg) as session:
        for keyword in list(cfg.get('keywords') or []):
            for item in search_keyword(session, keyword, max_per_keyword):
                if state.is_recent(item['tweetId'], cooldown_hours):
                    continue
                item['score'] = score_candidate(item['text'])
                item['contactSignals'] = detect_contacts(item['text'])
                item['replyText'] = build_public_reply(item['text'], website_url)
                drafts.append(item)
        drafts.sort(key=lambda row: (row.get('score') or 0, row.get('tweetId') or ''), reverse=True)
        for item in drafts[:max_replies]:
            if item['contactSignals']:
                notify(cfg, f'☎️ Browser contact signal: {item["url"]} | {", ".join(item["contactSignals"][:3])}')
            if apply and allow_public_reply:
                item['sendResult'] = post_reply(session, item['url'], item['replyText'])
                item['applied'] = True
                applied.append(item['tweetId'])
                state.mark_replied(item['tweetId'])
            else:
                item['applied'] = False
    state.save()
    out_path = write_bundle(cfg, 'browser-cycle', {'generatedAt': now_iso(), 'items': drafts})
    return {'generatedAt': now_iso(), 'draftCount': len(drafts), 'appliedCount': len(applied), 'outputPath': str(out_path), 'apply': apply, 'allowPublicReply': allow_public_reply}


def run_reply(config_path: Path, tweet_url: str, text: str, apply: bool) -> dict[str, Any]:
    cfg = resolve_config(config_path)
    if not apply:
        return {'ok': True, 'dryRun': True, 'tweetUrl': tweet_url, 'text': text}
    with BrowserSession(cfg) as session:
        result = post_reply(session, tweet_url, text)
    return {'ok': True, 'result': result}


def run_self_test() -> dict[str, Any]:
    assert classify_issue('Randevu tarihi bulamıyorum') == 'appointment'
    assert classify_issue('Evrak listesi nedir') == 'documents'
    assert score_candidate('Randevu bulamıyorum, ne yapmalıyım?') >= 3
    assert detect_contacts('Bana +90 555 123 45 67 den ulaşın')
    tmp = Path('/tmp/chrome-cdp-browser-operator-state.json')
    tmp.unlink(missing_ok=True)
    state = JsonStore(tmp)
    assert not state.is_recent('1', 24)
    state.mark_replied('1')
    assert state.is_recent('1', 24)
    tmp.unlink(missing_ok=True)
    return {'ok': True, 'testedAt': now_iso()}


def main() -> int:
    parser = argparse.ArgumentParser(description='chrome cdp browser operator')
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('self-test')

    check = sub.add_parser('check')
    check.add_argument('--config', required=True)

    search = sub.add_parser('search')
    search.add_argument('--config', required=True)
    search.add_argument('--keyword')
    search.add_argument('--max-items', type=int, default=8)

    cycle = sub.add_parser('run-cycle')
    cycle.add_argument('--config', required=True)
    cycle.add_argument('--apply', action='store_true')

    reply = sub.add_parser('reply')
    reply.add_argument('--config', required=True)
    reply.add_argument('--tweet-url', required=True)
    reply.add_argument('--text', required=True)
    reply.add_argument('--apply', action='store_true')

    args = parser.parse_args()
    if args.cmd == 'self-test':
        out = run_self_test()
    elif args.cmd == 'check':
        out = run_check(Path(args.config))
    elif args.cmd == 'search':
        out = run_search(Path(args.config), args.keyword, args.max_items)
    elif args.cmd == 'run-cycle':
        out = run_cycle(Path(args.config), apply=args.apply)
    elif args.cmd == 'reply':
        out = run_reply(Path(args.config), args.tweet_url, args.text, apply=args.apply)
    else:
        raise SystemExit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
