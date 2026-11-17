#!/usr/bin/env python3
"""check_drift.py — ctx-lockstep 漂移检测（进入/恢复项目时按需执行一次，无常驻进程）

用法:
    python3 check_drift.py <项目路径> [--json]

行为:
    - git 项目:    读 .ctx-lockstep/commits.log 积压行数（由 post-commit hook 写入）
    - 非 git 项目: 扫描 mtime 晚于 last_checkpoint 的文件数（排除常见噪声目录）

输出 (人类可读):
    DRIFT: 3 pending commits since last checkpoint (2026-09-03 13:24)
    OK:    no drift — 0 commits since last checkpoint (2026-09-03 13:24)

输出 (--json):
    {"ok":true,"git":true,"pending":3,"last_checkpoint":"2026-09-03 13:24","items":["36585c8 feat: ...",...]}

退出码: 永远 0（检测失败不算错误，只报告 unknown）。
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# mtime 扫描时排除的目录/文件名（噪声压制）
EXCLUDE_DIRS = {
    '.git', '.ctx-lockstep', 'node_modules', '__pycache__', '.venv', 'venv',
    'dist', 'build', 'out', 'target', '.next', '.nuxt', 'coverage',
    '.cache', '.gradle', 'bin', 'obj', 'vendor', '.idea', '.vscode',
}
EXCLUDE_FILES = {'.DS_Store', 'package-lock.json', 'poetry.lock', 'yarn.lock'}
MAX_SCAN_ITEMS = 500  # 防止超大项目慢扫


def read_meta(project: Path) -> dict:
    """从 .ctx-lockstep/PROJECT.md 头部 HTML 注释解析 last_checkpoint。"""
    meta = {}
    pj = project / '.ctx-lockstep' / 'PROJECT.md'
    if not pj.exists():
        return meta
    try:
        for line in pj.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line.startswith('last_checkpoint:'):
                meta['last_checkpoint'] = line.split(':', 1)[1].strip()
                break
            if line and not line.startswith('<!--') and not line.startswith('last_checkpoint'):
                if meta:  # 注释块已结束还没找到 → 停
                    break
    except OSError:
        pass
    return meta


def parse_ts(s: str) -> float:
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
        try:
            return datetime.strptime(s, fmt).timestamp()
        except ValueError:
            continue
    return 0.0


def git_drift(project: Path) -> dict:
    log = project / '.ctx-lockstep' / 'commits.log'
    pending, items = 0, []
    if log.exists():
        lines = [l.strip() for l in log.read_text(encoding='utf-8').splitlines() if l.strip()]
        pending = len(lines)
        items = lines[-10:]  # 最多展示最近 10 条
    return {'git': True, 'pending': pending, 'items': items,
            'hint': 'commits.log 有积压 → 建议固化；固化后清空该文件'}


def mtime_drift(project: Path) -> dict:
    meta = read_meta(project)
    ts_raw = meta.get('last_checkpoint', '')
    ts = parse_ts(ts_raw)
    changed = []
    if ts > 0:
        for p in project.rglob('*'):
            if len(changed) >= MAX_SCAN_ITEMS:
                break
            name = p.name
            if p.is_dir():
                if name in EXCLUDE_DIRS:
                    # rglob 不好剪枝，跳过判断在下面统一做
                    continue
                continue
            if name in EXCLUDE_FILES or name.startswith('.ctx'):
                continue
            rel = p.relative_to(project)
            if any(part in EXCLUDE_DIRS for part in rel.parts[:-1]):
                continue
            try:
                if p.stat().st_mtime > ts:
                    changed.append(str(rel))
            except OSError:
                continue
    return {'git': False, 'pending': len(changed), 'items': changed[:10],
            'last_checkpoint': ts_raw,
            'hint': '非 git 项目：mtime 扫描为近似值；如追求精确建议 git init'}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    as_json = '--json' in sys.argv
    if not args:
        print(json.dumps({'ok': False, 'error': 'usage: check_drift.py <project_path> [--json]'}))
        sys.exit(0)
    project = Path(args[0]).expanduser().resolve()
    if not project.is_dir():
        print(json.dumps({'ok': False, 'error': f'not a directory: {project}'} if as_json
                         else f'NOT FOUND: {project}'))
        sys.exit(0)

    is_git = (project / '.git').exists()
    result = git_drift(project) if is_git else mtime_drift(project)
    result.update({'ok': True, 'project': str(project), 'git': result.get('git', is_git)})
    lc = result.get('last_checkpoint') or read_meta(project).get('last_checkpoint', '未记录')

    if as_json:
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    if result['pending'] > 0:
        unit = 'pending commits' if is_git else 'changed files since checkpoint'
        print(f"DRIFT: {result['pending']} {unit} (last_checkpoint: {lc})")
        for it in result['items']:
            print(f"  - {it}")
        print(f"  → {result['hint']}")
    else:
        print(f"OK: no drift — nothing pending since checkpoint ({lc})")
    sys.exit(0)


if __name__ == '__main__':
    main()
