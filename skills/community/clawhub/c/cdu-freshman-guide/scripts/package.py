#!/usr/bin/env python3
"""cdu-freshman-guide 三平台打包脚本。

按 .skillignore 规则排除文件，生成 SkillHub / ClawHub / TRAE 三个 zip。
zip 内文件位于根目录（不套父文件夹）。

用法:
  python scripts/package.py
"""
from __future__ import annotations

import fnmatch
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORE_FILE = ROOT / '.skillignore'
OUT_DIR = ROOT.parent  # 输出到 cdu-freshman-guide 同级目录

VERSION = '1.4.0'

# 平台 → 额外排除规则（相对路径/通配）
PLATFORM_EXCLUDES = {
    'skillhub': [],
    'clawhub': ['skill-card/', 'skill-card/**', '_meta.json', '.clawhubignore'],
    'trae': [],
}


def load_ignore_patterns() -> list[str]:
    patterns = []
    if IGNORE_FILE.exists():
        for line in IGNORE_FILE.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns


def is_ignored(rel: str, patterns: list[str]) -> bool:
    for pat in patterns:
        pat = pat.rstrip('/')
        if fnmatch.fnmatch(rel, pat):
            return True
        # 目录前缀匹配（如 data/raw_desensitized/ 排除其下所有文件）
        if rel.startswith(pat + '/'):
            return True
    return False


def collect_files(patterns: list[str]) -> list[Path]:
    files = []
    for root, dirs, names in os.walk(ROOT):
        root_p = Path(root)
        # 跳过被忽略的目录
        dirs[:] = [d for d in dirs if not is_ignored(
            root_p.relative_to(ROOT).as_posix() + '/' + d, patterns)]
        for name in names:
            f = root_p / name
            rel = f.relative_to(ROOT).as_posix()
            if not is_ignored(rel, patterns):
                files.append(f)
    return files


def make_zip(name: str, files: list[Path]) -> Path:
    out = OUT_DIR / name
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(files):
            rel = f.relative_to(ROOT).as_posix()
            zf.write(f, rel)
    return out


def main() -> int:
    base_patterns = load_ignore_patterns()
    base_files = collect_files(base_patterns)
    print(f'基础文件数（排除 .skillignore 规则后）：{len(base_files)}')

    for platform, extra in PLATFORM_EXCLUDES.items():
        patterns = base_patterns + extra
        files = [f for f in base_files
                 if not is_ignored(f.relative_to(ROOT).as_posix(), extra)]
        zip_name = f'cdu-freshman-guide-v{VERSION}-{platform}.zip'
        out = make_zip(zip_name, files)
        size_kb = out.stat().st_size / 1024
        print(f'✅ {zip_name}  {len(files)} 个文件  {size_kb:.1f} KB')
        # 打印文件清单（前 30 个）
        for f in sorted(files)[:30]:
            print(f'    {f.relative_to(ROOT).as_posix()}')
        if len(files) > 30:
            print(f'    ... 共 {len(files)} 个文件')
    return 0


if __name__ == '__main__':
    sys.exit(main())
