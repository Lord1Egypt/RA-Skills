#!/usr/bin/env python3
import argparse
import json
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADER = ROOT / 'scripts' / 'douyin_downloader.py'
TITLE_CHECK = ROOT / 'scripts' / 'title_match_check.py'
CLEANUP = ROOT / 'scripts' / 'transcript_cleanup.py'
MAX_TITLE_RETRY = 5
DEFAULT_PROFILE_DIR = str(Path.home() / '.playwright' / 'douyinflow')
DEFAULT_HUMAN_DELAY_MIN_MS = 800
DEFAULT_HUMAN_DELAY_MAX_MS = 2500
DEFAULT_CAPTCHA_MAX_WAITS = 3


@dataclass
class Candidate:
    ref: str
    title: str
    author: str = ''
    date_text: str = ''
    duration_sec: int = 0
    likes_text: str = ''


def run(cmd: List[str], check: bool = True, input_text: Optional[str] = None) -> str:
    res = subprocess.run(cmd, input=input_text, text=True, capture_output=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
    return res.stdout.strip()


def pw(session: str, *args: str, check: bool = True) -> str:
    return run(['playwright-cli', f'-s={session}', *args], check=check)


def human_sleep(min_ms: int, max_ms: int):
    low = max(0, min(min_ms, max_ms))
    high = max(0, max(min_ms, max_ms))
    time.sleep(random.uniform(low, high) / 1000.0)


def get_snapshot(session: str) -> str:
    return pw(session, '--raw', 'snapshot')


def has_captcha(snapshot: str) -> bool:
    markers = [
        '验证码中间页',
        '点击两个形状相同的物体',
        '请完成下列验证后继续',
        '按住左边按钮拖动完成上方拼图',
        'captcha_container',
    ]
    return any(marker in snapshot for marker in markers)


def wait_for_captcha_resolution(session: str, max_waits: int = DEFAULT_CAPTCHA_MAX_WAITS):
    for _ in range(max_waits):
        snap = get_snapshot(session)
        if not has_captcha(snap):
            return
        print('检测到抖音验证码，请在浏览器中完成验证后按回车继续...', file=sys.stderr)
        input()
    snap = get_snapshot(session)
    if has_captcha(snap):
        raise SystemExit('当前会话被抖音验证码拦截，请先在浏览器中完成验证后重试')


def parse_duration(text: str) -> int:
    m = re.match(r'^(\d{2}):(\d{2})$', text.strip())
    if not m:
        return 0
    return int(m.group(1)) * 60 + int(m.group(2))


def parse_candidates(snapshot: str) -> List[Candidate]:
    candidates: List[Candidate] = []
    item_pattern = re.compile(r'(^\s*- listitem \[ref=(e\d+)\]:\n(?P<block>(?:\s+.*\n)+?))(?=^\s*- listitem \[ref=e\d+\]:|\Z)', re.M)
    leaf_generic = re.compile(r'- generic \[ref=e\d+\]: ?"?(.*?)"?$')
    date_re = re.compile(r'^(\d+分钟前|\d+小时前|\d+天前|\d+周前|\d+月前)$')

    for match in item_pattern.finditer(snapshot + '\n'):
        ref = match.group(2)
        block = match.group('block')
        title = ''
        author = ''
        date_text = ''
        duration_sec = 0
        likes_text = ''
        generic_values = []

        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            m_dur = re.search(r'(^|\s)(\d{2}:\d{2})$', line)
            if m_dur and duration_sec == 0:
                duration_sec = parse_duration(m_dur.group(2))

            m_leaf = leaf_generic.search(line)
            if m_leaf:
                value = m_leaf.group(1).strip()
                if value:
                    generic_values.append(value)

        for value in generic_values:
            if value.startswith('@') and not author:
                author = value
                continue
            if date_re.fullmatch(value) and not date_text:
                date_text = value
                continue
            if re.fullmatch(r'[\d.]+万?|[\d.]+', value) and not likes_text:
                likes_text = value
                continue

        title_candidates = []
        for value in generic_values:
            if value == '合集':
                continue
            if value.startswith('@'):
                continue
            if date_re.fullmatch(value):
                continue
            if re.fullmatch(r'[\d.]+万?|[\d.]+', value):
                continue
            if re.fullmatch(r'\d{2}:\d{2}', value):
                continue
            if len(value) < 8:
                continue
            title_candidates.append(value)

        if title_candidates:
            title = max(title_candidates, key=len)

        if title:
            candidates.append(Candidate(ref=ref, title=title, author=author, date_text=date_text, duration_sec=duration_sec, likes_text=likes_text))
    return candidates


def like_to_num(text: str) -> float:
    text = text.strip()
    if not text:
        return 0
    if text.endswith('万'):
        try:
            return float(text[:-1]) * 10000
        except Exception:
            return 0
    try:
        return float(text)
    except Exception:
        return 0


def filter_candidates(candidates: List[Candidate], args) -> List[Candidate]:
    result = []
    for c in candidates:
        title = c.title
        author = c.author
        if args.must_include and not all(word in title for word in args.must_include):
            continue
        if args.exclude_word and any(word in title or word in author for word in args.exclude_word):
            continue
        if args.content_type_hint and not any(word in title for word in args.content_type_hint):
            continue
        if args.account_hint and not any(word in author for word in args.account_hint):
            continue
        if args.duration_min_sec and c.duration_sec and c.duration_sec < args.duration_min_sec:
            continue
        if args.duration_max_sec and c.duration_sec and c.duration_sec > args.duration_max_sec:
            continue
        if args.min_likes and like_to_num(c.likes_text) < args.min_likes:
            continue
        result.append(c)
    return result


def ensure_open(session: str, headed: bool, persistent: bool, profile: Optional[str] = None):
    cmd = ['playwright-cli', f'-s={session}', 'open', 'https://www.douyin.com/']
    if headed:
        cmd.append('--headed')
    if persistent:
        cmd.append('--persistent')
    if profile:
        cmd.extend(['--profile', profile])
    run(cmd, check=True)


def maybe_wait_for_login(session: str):
    snap = get_snapshot(session)
    if 'button "登录"' in snap or 'paragraph [ref=e167]: 登录' in snap:
        print('检测到未登录，请在打开的浏览器中手动登录后按回车继续...', file=sys.stderr)
        input()


def search_keyword(session: str, keyword: str, human_delay_min_ms: int, human_delay_max_ms: int, captcha_max_waits: int):
    pw(session, 'run-code', "async page => { await page.goto('https://www.douyin.com/'); await page.waitForTimeout(2200); }")
    human_sleep(human_delay_min_ms, human_delay_max_ms)
    wait_for_captcha_resolution(session, captcha_max_waits)

    fill_and_search = (
        "async page => {"
        f" const box = page.getByRole('textbox', {{ name: '搜索你感兴趣的内容' }});"
        f" await box.click();"
        f" await page.waitForTimeout({max(250, human_delay_min_ms // 2)});"
        f" await box.fill({json.dumps(keyword)});"
        f" await page.waitForTimeout({max(400, human_delay_min_ms)});"
        f" await page.getByRole('button', {{ name: '搜索' }}).click();"
        f" await page.waitForTimeout({max(3000, human_delay_max_ms + 1500)});"
        " }"
    )
    pw(session, 'run-code', fill_and_search)
    human_sleep(human_delay_min_ms, human_delay_max_ms)
    wait_for_captcha_resolution(session, captcha_max_waits)

    switch_video_tab = (
        "async page => {"
        " const tab = page.getByText('视频', { exact: true }).first();"
        " if (await tab.count()) {"
        "   await tab.click();"
        f"   await page.waitForTimeout({max(2200, human_delay_max_ms + 1200)});"
        " }"
        " }"
    )
    pw(session, 'run-code', switch_video_tab, check=False)
    human_sleep(human_delay_min_ms, human_delay_max_ms)
    wait_for_captcha_resolution(session, captcha_max_waits)


def click_candidate_by_title(session: str, title: str, human_delay_min_ms: int, human_delay_max_ms: int, captcha_max_waits: int):
    human_sleep(human_delay_min_ms, human_delay_max_ms)
    script = f"async page => {{ await page.getByText({json.dumps(title)}, {{ exact: true }}).click(); await page.waitForTimeout({max(1800, human_delay_max_ms + 800)}); }}"
    pw(session, 'run-code', script, check=False)
    wait_for_captcha_resolution(session, captcha_max_waits)


def close_modal(session: str):
    pw(session, 'key', 'Escape', check=False)


def get_modal_id(session: str) -> str:
    out = pw(session, 'eval', "new URL(location.href).searchParams.get('modal_id')")
    # Clean up: take first line and strip any markdown/code block markers
    lines = out.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove markdown code block markers
        line = line.replace('```', '').strip()
        if line and not line.startswith('//') and not line.startswith('http'):
            # Looks like a video ID (numeric)
            if re.fullmatch(r'\d+', line):
                return line
    return ''


def check_title(expected: str, actual: str, mode: str = 'default', min_similarity: float = 0.82) -> dict:
    out = run([
        'python3', str(TITLE_CHECK),
        '--expected', expected,
        '--actual', actual,
        '--mode', mode,
        '--min-similarity', str(min_similarity),
    ], check=False)
    payload = json.loads(out)
    payload['exit_ok'] = True if payload.get('matched') else False
    return payload


def choose_valid_video(session: str, candidates: List[Candidate], start_index: int = 0, max_retry: int = MAX_TITLE_RETRY, title_match_mode: str = 'default', title_min_similarity: float = 0.82, human_delay_min_ms: int = DEFAULT_HUMAN_DELAY_MIN_MS, human_delay_max_ms: int = DEFAULT_HUMAN_DELAY_MAX_MS, captcha_max_waits: int = DEFAULT_CAPTCHA_MAX_WAITS):
    attempts = []
    upper = min(len(candidates), start_index + max_retry)
    for idx in range(start_index, upper):
        candidate = candidates[idx]
        click_candidate_by_title(session, candidate.title, human_delay_min_ms, human_delay_max_ms, captcha_max_waits)
        video_id = get_modal_id(session)
        if not video_id:
            attempts.append({
                'candidateIndex': idx + 1,
                'candidateTitle': candidate.title,
                'matched': False,
                'reason': 'missing-modal-id',
            })
            close_modal(session)
            continue

        share_info = get_share_info(video_id)
        actual_title = share_info['title']
        title_check = check_title(candidate.title, actual_title, mode=title_match_mode, min_similarity=title_min_similarity)
        attempts.append({
            'candidateIndex': idx + 1,
            'candidateTitle': candidate.title,
            'actualTitle': actual_title,
            'videoId': video_id,
            'matched': title_check.get('matched', False),
            'reason': title_check.get('reason', 'unknown'),
            'similarity': title_check.get('similarity'),
            'mode': title_check.get('mode', title_match_mode),
        })
        if title_check.get('matched'):
            return candidate, video_id, actual_title, attempts

        close_modal(session)

    return None, None, None, attempts


def get_share_info(video_id: str) -> dict:
    out = run(['python3', str(DOWNLOADER), '--link', f'https://www.iesdouyin.com/share/video/{video_id}', '--action', 'info'])
    return json.loads(out)


def write_meta(outdir: Path, payload: dict):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / 'meta.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    if 'share_link' in payload:
        (outdir / 'source-link.txt').write_text(payload['share_link'] + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='抖音搜索→筛选→校验→提取→修正 一体化脚本')
    parser.add_argument('--keyword', required=True)
    parser.add_argument('--pick-index', type=int, default=1)
    parser.add_argument('--must-include', action='append', default=[])
    parser.add_argument('--exclude-word', action='append', default=[])
    parser.add_argument('--content-type-hint', action='append', default=[])
    parser.add_argument('--account-hint', action='append', default=[])
    parser.add_argument('--min-likes', type=float, default=0)
    parser.add_argument('--duration-min-sec', type=int, default=0)
    parser.add_argument('--duration-max-sec', type=int, default=0)
    parser.add_argument('--session', default='douyinflow')
    parser.add_argument('--profile', default=DEFAULT_PROFILE_DIR, help='playwright-cli 持久化浏览器 profile 目录')
    parser.add_argument('--title-match-mode', choices=['strict', 'default', 'loose'], default='default')
    parser.add_argument('--title-min-similarity', type=float, default=0.82)
    parser.add_argument('--max-title-retry', type=int, default=MAX_TITLE_RETRY)
    parser.add_argument('--human-delay-min-ms', type=int, default=DEFAULT_HUMAN_DELAY_MIN_MS)
    parser.add_argument('--human-delay-max-ms', type=int, default=DEFAULT_HUMAN_DELAY_MAX_MS)
    parser.add_argument('--captcha-max-waits', type=int, default=DEFAULT_CAPTCHA_MAX_WAITS)
    parser.add_argument('--headed', action='store_true')
    parser.add_argument('--persistent', action='store_true')
    parser.add_argument('--output-dir', default='output')
    parser.add_argument('--skip-login-check', action='store_true')
    args = parser.parse_args()

    ensure_open(args.session, args.headed, args.persistent, args.profile)
    if not args.skip_login_check:
        maybe_wait_for_login(args.session)

    search_keyword(args.session, args.keyword, args.human_delay_min_ms, args.human_delay_max_ms, args.captcha_max_waits)
    snapshot = get_snapshot(args.session)
    if has_captcha(snapshot):
        raise SystemExit('当前会话被抖音验证码拦截，请先在浏览器中完成验证后重试')
    candidates = parse_candidates(snapshot)
    candidates = filter_candidates(candidates, args)
    if not candidates:
        raise SystemExit('未找到符合筛选条件的视频候选项')

    if args.pick_index < 1 or args.pick_index > len(candidates):
        raise SystemExit(f'pick-index 超出范围，可选数量: {len(candidates)}')

    start_index = args.pick_index - 1
    target, video_id, actual_title, attempts = choose_valid_video(
        args.session,
        candidates,
        start_index=start_index,
        max_retry=args.max_title_retry,
        title_match_mode=args.title_match_mode,
        title_min_similarity=args.title_min_similarity,
        human_delay_min_ms=args.human_delay_min_ms,
        human_delay_max_ms=args.human_delay_max_ms,
        captcha_max_waits=args.captcha_max_waits,
    )
    if not target or not video_id or not actual_title:
        raise SystemExit('候选视频已尝试，但未找到标题校验通过的视频；请调整筛选条件、pick-index，或放宽标题匹配规则')

    share_link = f'https://www.iesdouyin.com/share/video/{video_id}'
    out = run(['python3', str(DOWNLOADER), '--link', share_link, '--action', 'extract', '--output', args.output_dir], check=True)

    output_path = None
    try:
        extracted = json.loads(out)
        output_path = extracted.get('output_path')
    except Exception:
        # fallback: conventional output dir
        output_path = str(Path(args.output_dir) / video_id)

    outdir = Path(output_path)
    transcript = outdir / 'transcript.md'
    run(['python3', str(CLEANUP), '--title', actual_title, '--raw', str(transcript), '--outdir', str(outdir)], check=True)

    meta = {
        'keyword': args.keyword,
        'pickIndex': args.pick_index,
        'selected': {
            'title': target.title,
            'author': target.author,
            'date': target.date_text,
            'durationSec': target.duration_sec,
            'likes': target.likes_text,
        },
        'validatedTitle': actual_title,
        'videoId': video_id,
        'share_link': share_link,
        'profile': args.profile,
        'humanDelayMinMs': args.human_delay_min_ms,
        'humanDelayMaxMs': args.human_delay_max_ms,
        'captchaMaxWaits': args.captcha_max_waits,
        'titleMatchMode': args.title_match_mode,
        'titleMinSimilarity': args.title_min_similarity,
        'titleValidationAttempts': attempts,
        'generatedAt': datetime.now().isoformat(timespec='seconds')
    }
    write_meta(outdir, meta)
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
