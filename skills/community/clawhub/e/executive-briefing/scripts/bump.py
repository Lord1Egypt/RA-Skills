#!/usr/bin/env python3
"""版本号自动升级 + 新文件生成 + 变更摘要（V2.0 增强版）

用法:
  python3 bump.py --major              # X+1, Y=0, Z=0, 生成新文件
  python3 bump.py --minor              # Y+1, Z=0, 生成新文件
  python3 bump.py --patch              # Z+1, 生成新文件
  python3 bump.py --major --dry-run    # 预览变更（不实际修改）
  python3 bump.py --major --note "移除了Part 3旧架构章节"

变更内容:
  - 更新 version.json 版本号
  - 复制当前最新 md 文件 → 新版本文件
  - 更新 VERSION.md 版本历史
  - 更新 README.md 索引
  - （可选）在文件头部添加变更注释
"""
import json, sys, argparse, shutil, re
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))


def parse_version(v: str) -> Tuple[int, int, int]:
    parts = v.split('.')
    if len(parts) != 3:
        raise ValueError(f'版本号格式错误（期望 X.Y.Z）: {v}')
    return tuple(int(p) for p in parts)


def find_latest_md(report_dir: Path) -> Optional[Path]:
    """找到目录中版本号最高的 md 文件"""
    mds = sorted(report_dir.glob('*.md'))
    # 按文件名中的版本号排序
    versioned = []
    for f in mds:
        if f.name in ('README.md', 'VERSION.md'):
            continue
        m = re.search(r'v(\d+\.\d+\.\d+)', f.name)
        if m:
            versioned.append((parse_version(m.group(1)), f))
    if not versioned:
        return None
    return sorted(versioned, key=lambda x: x[0], reverse=True)[0][1]


def find_report_dir() -> Optional[Path]:
    """在当前目录或父目录中查找包含 version.json 的报告目录"""
    for d in [Path.cwd()] + list(Path.cwd().parents):
        if (d / 'version.json').exists():
            return d
    # 查找 reports/ 下的子目录
    reports_root = Path.cwd() / 'reports'
    if reports_root.exists():
        for sub in reports_root.iterdir():
            if sub.is_dir() and (sub / 'version.json').exists():
                return sub
    return None


def update_readme(report_dir: Path, new_file: Path, new_version: str):
    """更新 README.md 索引"""
    readme_path = report_dir / 'README.md'
    if not readme_path.exists():
        return
    content = readme_path.read_text(encoding='utf-8')
    entry = f'| [{new_file.name}](./{new_file.name}) | V{new_version} | 草稿 |'
    # 在第一个表格行后插入
    lines = content.split('\n')
    inserted = False
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.startswith('| [') and '.md' in line:
            new_lines.append(entry)
            inserted = True
    if not inserted:
        new_lines.append(entry)
    readme_path.write_text('\n'.join(new_lines), encoding='utf-8')


def update_version_md(report_dir: Path, old_ver: str, new_ver: str, note: str):
    """更新 VERSION.md"""
    vmd_path = report_dir / 'VERSION.md'
    if not vmd_path.exists():
        return
    content = vmd_path.read_text(encoding='utf-8')
    today = datetime.now(CST).strftime('%Y-%m-%d')
    entry = f'| V{new_ver} | {today} | {note or "版本升级"} | report-builder V2.0 |'
    lines = content.split('\n')
    inserted = False
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.startswith('| V') and '|' in line:
            new_lines.append(entry)
            inserted = True
    if not inserted:
        new_lines.append(entry)
    vmd_path.write_text('\n'.join(new_lines), encoding='utf-8')


def add_change_comment(file_path: Path, old_ver: str, new_ver: str, note: str):
    """在文件头部添加版本变更注释"""
    content = file_path.read_text(encoding='utf-8')
    today = datetime.now(CST).strftime('%Y-%m-%d')
    comment = f'<!-- V{old_ver} → V{new_ver} ({today}): {note or "版本升级"} -->\n'
    # 插入到第一个 # 标题之前
    idx = content.find('# ')
    if idx >= 0:
        content = content[:idx] + comment + content[idx:]
    else:
        content = comment + content
    file_path.write_text(content, encoding='utf-8')


def main():
    p = argparse.ArgumentParser(description='版本号升级 + 新文件生成')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--major', action='store_true')
    g.add_argument('--minor', action='store_true')
    g.add_argument('--patch', action='store_true')
    p.add_argument('--dry-run', action='store_true', help='预览变更')
    p.add_argument('--note', default='', help='变更说明')
    p.add_argument('--dir', help='报告目录路径（默认自动查找）')
    args = p.parse_args()

    # 查找报告目录
    report_dir = Path(args.dir) if args.dir else find_report_dir()
    if not report_dir:
        print('错误：未找到报告目录（确保在报告目录下或 reports/ 包含 version.json）',
              file=sys.stderr)
        sys.exit(1)

    version_file = report_dir / 'version.json'
    if not version_file.exists():
        print(f'错误：{version_file} 未找到', file=sys.stderr)
        sys.exit(1)

    # 读取当前版本
    data = json.loads(version_file.read_text(encoding='utf-8'))
    major, minor, patch = parse_version(data['version'])
    old_version = data['version']

    if args.major:
        major += 1; minor = patch = 0
    elif args.minor:
        minor += 1; patch = 0
    else:
        patch += 1
    new_version = f'{major}.{minor}.{patch}'

    # 找到最新 md 文件
    latest_md = find_latest_md(report_dir)
    if not latest_md:
        print('错误：未找到报告 md 文件', file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f'[DRY RUN] {old_version} → {new_version}')
        print(f'  源文件：{latest_md.name}')
        print(f'  新文件：{latest_md.name.replace(old_version, new_version)}')
        print(f'  变更说明：{args.note or "(无)"}')
        return

    # 生成新文件
    new_md_name = latest_md.name.replace(old_version, new_version)
    new_md_path = report_dir / new_md_name
    shutil.copy2(latest_md, new_md_path)
    add_change_comment(new_md_path, old_version, new_version, args.note)

    # 更新 version.json
    data['version'] = new_version
    data['releaseDate'] = datetime.now(CST).strftime('%Y-%m-%d')
    data.setdefault('changes', []).insert(0,
        f'V{new_version}: {args.note or "版本升级"}（{old_version} → {new_version}）')
    version_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n',
                            encoding='utf-8')

    # 更新 VERSION.md
    update_version_md(report_dir, old_version, new_version, args.note)

    # 更新 README.md
    update_readme(report_dir, new_md_path, new_version)

    change_type = {'major': '主版本', 'minor': '次版本', 'patch': '补丁'}
    ctype = change_type.get(
        'major' if args.major else 'minor' if args.minor else 'patch')

    print(f'✅ 版本升级完成：{old_version} → {new_version}（{ctype}）')
    print(f'   新文件：{new_md_name}')
    if args.note:
        print(f'   变更说明：{args.note}')


if __name__ == '__main__':
    main()
