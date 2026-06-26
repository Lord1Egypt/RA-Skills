#!/usr/bin/env python3
"""
多词库同步：从 config/wordlist_sources.json 拉取多个免费词库，写入 config/wordlists/。
用户无需运行——技能已随包附带词库，开箱即用。维护者想更新词库时可执行一次。
用法: python sync_wordlists.py [--dry-run]
"""
import os
import re
import sys
import json
import urllib.request
from urllib.parse import urlparse, quote

def find_config_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def safe_filename(name):
    """词库名转安全文件名（仅保留字母数字、中文、横线）"""
    s = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', name)
    s = re.sub(r'[\s]+', '-', s).strip('-') or 'wordlist'
    return s[:80]

def fetch_url(url, timeout=30):
    try:
        # 中文等非 ASCII 路徑需 percent-encode，否則部分環境請求失敗
        p = urlparse(url)
        path_enc = quote(p.path, safe='/')
        full_url = p.scheme + '://' + p.netloc + path_enc + ('?' + p.query if p.query else '')
        req = urllib.request.Request(full_url, headers={'User-Agent': 'OpenClaw-ComplianceCheck/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception:
        return None

def normalize_content(raw):
    """一行一个词，去空、去 # 注释，去重顺序保留"""
    seen = set()
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('regex:'):
            lines.append(line)
            continue
        if line not in seen:
            seen.add(line)
            lines.append(line)
    return '\n'.join(lines)

def main():
    dry_run = '--dry-run' in sys.argv
    config_dir = find_config_dir()
    sources_path = os.path.join(config_dir, 'config', 'wordlist_sources.json')
    wordlists_dir = os.path.join(config_dir, 'config', 'wordlists')

    if not os.path.exists(sources_path):
        print('未找到 config/wordlist_sources.json', file=sys.stderr)
        sys.exit(1)
    try:
        with open(sources_path, 'r', encoding='utf-8') as f:
            sources = json.load(f)
    except Exception as e:
        print(f'解析 wordlist_sources.json 失败: {e}', file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(wordlists_dir):
        os.makedirs(wordlists_dir)

    ok = 0
    fail = 0
    for item in sources:
        if isinstance(item, dict) and not item.get('enabled', True):
            continue
        name = item.get('name') if isinstance(item, dict) else str(item)
        url = item.get('url') if isinstance(item, dict) else None
        if not name or not url:
            continue
        fname = safe_filename(name) + '.txt'
        out_path = os.path.join(wordlists_dir, fname)
        if dry_run:
            print(f'[dry-run] 会拉取: {name} -> {fname}')
            ok += 1
            continue
        raw = fetch_url(url)
        if raw is None:
            print(f'拉取失败: {name} ({url})', file=sys.stderr)
            fail += 1
            continue
        content = normalize_content(raw)
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f'写入失败 {out_path}: {e}', file=sys.stderr)
            fail += 1
            continue
        print(f'已同步: {name} -> {fname} ({len(content.splitlines())} 条)')
        ok += 1

    if dry_run:
        print(f'[dry-run] 共 {ok} 个词库会拉取')
    else:
        print(f'同步完成: 成功 {ok}，失败 {fail}')
    sys.exit(0 if fail == 0 else 1)

if __name__ == '__main__':
    main()
