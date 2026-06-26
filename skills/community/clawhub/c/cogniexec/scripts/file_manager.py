#!/usr/bin/env python3
"""
file_manager.py — 文件批量操作工具（纯标准库）
覆盖：归类/重命名/去重/扫描/清理/查找/同步/树形展示

用法：
  python file_manager.py classify ./Downloads --by ext -o ./Sorted
  python file_manager.py rename ./photos --pattern "IMG_{seq:04d}.jpg"
  python file_manager.py dedup ./folder --by content --dry-run
  python file_manager.py scan ./project --size-sort --top 20
  python file_manager.py clean ./folder --older-than 30d --pattern "*.tmp"
  python file_manager.py find ./src --name "*.py" --contains "TODO"
  python file_manager.py tree ./project --depth 3
  python file_manager.py sync ./src ./backup --dry-run
  python file_manager.py batch-replace ./src --from "old_api" --to "new_api" --ext .py
  python file_manager.py archive ./logs --zip --older-than 7d
"""

import sys
import os
import re
import json
import hashlib
import shutil
import time
import fnmatch
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                val = argv[i + 1]
                args[key] = val
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36, 'white': 37}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


def confirm(prompt: str) -> bool:
    try:
        ans = input(f'{prompt} [y/N]: ').strip().lower()
        return ans in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        return False


# ─── 文件信息 ────────────────────────────────────────────────

class FileInfo:
    """文件元数据"""
    __slots__ = ('path', 'size', 'mtime', 'ext', 'is_dir')

    def __init__(self, path: str):
        self.path = path
        self.is_dir = os.path.isdir(path)
        self.ext = ''
        self.size = 0
        self.mtime = 0
        if not self.is_dir:
            self.ext = os.path.splitext(path)[1].lower()
            try:
                stat = os.stat(path)
                self.size = stat.st_size
                self.mtime = stat.st_mtime
            except OSError:
                pass

    @property
    def size_human(self) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if self.size < 1024:
                return f'{self.size:.1f} {unit}'
            self.size /= 1024
        return f'{self.size:.1f} PB'

    @property
    def mtime_str(self) -> str:
        return datetime.fromtimestamp(self.mtime).strftime('%Y-%m-%d %H:%M') if self.mtime else ''

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    def get_hash(self, block_size=65536) -> str:
        """计算文件内容哈希"""
        hasher = hashlib.md5()
        with open(self.path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_classify(args):
    """按扩展名或类型归类文件"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    by = args.get('by', 'ext')
    out_dir = args.get('o', os.path.join(src_dir, '_classified'))
    dry_run = args.get('dry_run', False)

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    groups: dict[str, list[str]] = defaultdict(list)
    for entry in os.listdir(src_dir):
        full_path = os.path.join(src_dir, entry)
        if not os.path.isfile(full_path):
            continue

        ext = os.path.splitext(entry)[1].lower() or '(no_ext)'
        # 按类型分组映射
        type_map = {
            '.jpg': '.images', '.jpeg': '.images', '.png': '.images',
            '.gif': '.images', '.webp': '.images', '.svg': '.images', '.bmp': '.images', '.ico': '.images',
            '.mp4': '.videos', '.avi': '.videos', '.mkv': '.videos',
            '.mov': '.videos', '.wmv': '.videos', '.flv': '.videos',
            '.mp3': '.audio', '.wav': '.audio', '.flac': '.audio',
            '.aac': '.audio', '.ogg': '.audio', '.wma': '.audio',
            '.pdf': '.documents', '.doc': '.documents', '.docx': '.documents',
            '.xls': '.documents', '.xlsx': '.documents', '.ppt': '.documents',
            '.pptx': '.documents', '.txt': '.documents', '.csv': '.documents',
            '.md': '.documents', '.rtf': '.documents', '.odt': '.documents',
            '.py': '.code', '.js': '.code', '.ts': '.code', '.java': '.code',
            '.cpp': '.code', '.c': '.code', '.h': '.code', '.cs': '.code',
            '.go': '.code', '.rs': '.code', '.rb': '.code', '.php': '.code',
            '.html': '.code', '.css': '.code', '.json': '.code', '.xml': '.code',
            '.sh': '.code', '.bat': '.code', '.ps1': '.code', '.sql': '.code',
            '.zip': '.archives', '.rar': '.archives', '.7z': '.archives',
            '.tar': '.archives', '.gz': '.archives', '.bz2': '.archives',
        }

        category = ext if by == 'ext' else type_map.get(ext, f'.{ext.strip(".")}s' if ext else '.other')
        groups[category].append(full_path)

    if dry_run:
        echo('📋 归类预览 (dry-run):', fg='cyan')
        from scripts.table_format import tabulate
        rows = [[cat, str(len(files))] for cat, files in sorted(groups.items())]
        print(tabulate(rows, headers=['类别', '文件数'], tablefmt='grid'))
        return

    moved_count = 0
    for category, files in groups.items():
        target_dir = os.path.join(out_dir, category.lstrip('.'))
        os.makedirs(target_dir, exist_ok=True)
        for fpath in files:
            dest = os.path.join(target_dir, os.path.basename(fpath))
            if not os.path.exists(dest):
                shutil.move(fpath, dest)
                moved_count += 1

    total = sum(len(v) for v in groups.values())
    echo(f'✅ 分类完成: {total} 文件 → {len(groups)} 个类别 → {out_dir}', fg='green')


def cmd_rename(args):
    """批量重命名文件"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    pattern = args.get('pattern', '{name}{ext}')
    ext_filter = args.get('ext', '')
    dry_run = args.get('dry_run', False)
    start_seq = int(args.get('start', 1))

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    files = []
    for entry in sorted(os.listdir(src_dir)):
        full_path = os.path.join(src_dir, entry)
        if not os.path.isfile(full_path):
            continue
        if ext_filter and not entry.lower().endswith(ext_filter.lower()):
            continue
        files.append((full_path, entry))

    renames = []
    seq = start_seq
    for full_path, name in files:
        base, ext = os.path.splitext(name)
        new_name = pattern.format(
            name=base, ext=ext,
            seq=seq,
            date=datetime.now().strftime('%Y%m%d'),
            datetime_str=datetime.now().strftime('%Y%m%d_%H%M%S'),
        )
        new_path = os.path.join(os.path.dirname(full_path), new_name)
        renames.append((full_path, new_path))
        seq += 1

    if dry_run or not confirm(f'⚠️ 即将重命名 {len(renames)} 个文件?'):
        if dry_run:
            echo('📋 重命名预览 (dry-run):', fg='cyan')
            for old, new in renames[:30]:
                echo(f'  {os.path.basename(old)} → {os.path.basename(new)}', fg='yellow')
            if len(renames) > 30:
                echo(f'  ... 还有 {len(renames)-30} 个', fg='yellow')
        return

    count = 0
    for old_path, new_path in renames:
        if old_path != new_path and not os.path.exists(new_path):
            os.rename(old_path, new_path)
            count += 1

    echo(f'✅ 已重命名 {count} 个文件', fg='green')


def cmd_dedup(args):
    """文件去重（按名称、大小或内容）"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    by = args.get('by', 'name')
    dry_run = args.get('dry_run', False)

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    all_files = []
    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            fi = FileInfo(fpath)
            all_files.append(fi)

    duplicates: list[list[FileInfo]] = []

    if by == 'name':
        name_map: dict[str, list[FileInfo]] = defaultdict(list)
        for fi in all_files:
            name_map[fi.name].append(fi)
        duplicates = [group for group in name_map.values() if len(group) > 1]

    elif by == 'size':
        size_map: dict[int, list[FileInfo]] = defaultdict(list)
        for fi in all_files:
            size_map[int(fi.size)].append(fi)
        # 大小相同的进一步用内容确认
        for group in size_map.values():
            if len(group) > 1:
                hash_map: dict[str, list[FileInfo]] = defaultdict(list)
                for fi in group:
                    h = fi.get_hash()
                    hash_map[h].append(fi)
                for h_group in hash_map.values():
                    if len(h_group) > 1:
                        duplicates.append(h_group)

    elif by == 'content':
        hash_map: dict[str, list[FileInfo]] = defaultdict(list)
        echo(f'🔍 计算内容哈希 ({len(all_files)} 个文件)...', fg='cyan')
        for idx, fi in enumerate(all_files):
            h = fi.get_hash()
            hash_map[h].append(fi)
            if (idx + 1) % 100 == 0:
                echo(f'  进度: {idx+1}/{len(all_files)}', fg='cyan')
        duplicates = [group for group in hash_map.values() if len(group) > 1]

    total_dupes = sum(len(g) - 1 for g in duplicates)
    if not duplicates:
        echo('✅ 未发现重复文件', fg='green')
        return

    from scripts.table_format import tabulate
    echo(f'\n🔍 发现 {len(duplicates)} 组重复，共 {total_dupes} 个多余副本:', fg='yellow')
    print()

    dup_rows = []
    for gi, group in enumerate(duplicates):
        keep = group[0]
        for dupe in group[1:]:
            dup_rows.append({
                '#': gi + 1,
                '保留': keep.name,
                '删除': dupe.name,
                '大小': dupe.size_human,
                '路径': dupe.path,
            })
    print(tabulate(dup_rows[:50], tablefmt='grid'))
    if len(dup_rows) > 50:
        echo(f'  ... 还有 {len(dup_rows)-50} 行', fg='yellow')

    if dry_run:
        return

    if confirm(f'\n⚠️ 确认删除以上 {total_dupes} 个重复文件? 此操作不可逆!'):
        removed = 0
        for group in duplicates:
            for dupe in group[1:]:
                try:
                    os.remove(dupe.path)
                    removed += 1
                except OSError as e:
                    echo(f'  删除失败: {dupe.path} → {e}', fg='red')
        echo(f'✅ 已删除 {removed} 个重复文件', fg='green')


def cmd_scan(args):
    """扫描目录并生成报告"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    size_sort = args.get('size_sort', False)
    top_n = int(args.get('top', 30))
    output = args.get('o', '')

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    all_files = []
    total_size = 0
    ext_stats: dict[str, dict] = defaultdict(lambda: {'count': 0, 'size': 0})
    dir_count = 0

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', '.venv')]
        dir_count += 1
        for fname in filenames:
            fpath = os.path.join(root, fname)
            try:
                fi = FileInfo(fpath)
                all_files.append(fi)
                total_size += fi.size
                ext_stats[fi.ext or '(none)']['count'] += 1
                ext_stats[fi.ext or '(none)']['size'] += fi.size
            except OSError:
                pass

    # 排序
    if size_sort:
        all_files.sort(key=lambda f: f.size, reverse=True)
    else:
        all_files.sort(key=lambda f: f.path)

    # 格式化总大小
    def fmt_size(b):
        for u in ['B', 'KB', 'MB', 'GB']:
            if b < 1024:
                return f'{b:.1f} {u}'
            b /= 1024
        return f'{b:.1f} TB'

    echo(f'📂 扫描报告: {src_dir}', fg='cyan', bold=True)
    echo(f'   文件数: {len(all_files)} | 目录数: {dir_count} | 总大小: {fmt_size(total_size)}', fg='cyan')
    print()

    # 扩展名统计
    from scripts.table_format import tabulate
    ext_rows = [
        {
            '扩展名': ext,
            '数量': stats['count'],
            '总大小': fmt_size(stats['size']),
            '占比': f'{stats["size"]/total_size*100:.1f}%' if total_size else '0%',
        }
        for ext, stats in sorted(ext_stats.items(), key=lambda x: x[1]['size'], reverse=True)[:20]
    ]
    echo('📊 扩展名分布 TOP 20:', fg='cyan')
    print(tabulate(ext_rows, tablefmt='grid'))

    print()
    # 最大文件
    top_files = all_files[:top_n]
    echo(f'📁 {"最大" if size_sort else "前"} {min(top_n, len(top_files))} 个文件:', fg='cyan')
    file_rows = [{
        '名称': fi.name,
        '大小': fi.size_human,
        '修改时间': fi.mtime_str,
        '路径': fi.path,
    } for fi in top_files]
    print(tabulate(file_rows, tablefmt='grid'))

    # 输出 JSON 报告
    if output:
        report = {
            'directory': src_dir,
            'scan_time': datetime.now().isoformat(),
            'total_files': len(all_files),
            'total_dirs': dir_count,
            'total_size': total_size,
            'extensions': dict(ext_stats),
            'largest_files': [{'path': f.path, 'size': f.size, 'name': f.name} for f in all_files[:100]],
        }
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        echo(f'\n📄 报告已保存: {output}', fg='green')


def cmd_clean(args):
    """清理旧文件/临时文件"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    pattern = args.get('pattern', '*.tmp')
    older_than = args.get('older_than', '')  # 如 30d, 60m, 1y
    max_size = args.get('max_size', '')     # 如 10MB, 1GB
    empty_dirs = args.get('empty_dirs', False)
    dry_run = args.get('dry_run', False)

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    now = time.time()
    cutoff_time = None
    size_limit_bytes = None

    if older_than:
        cutoff_time = _parse_duration(older_than, now)
    if max_size:
        size_limit_bytes = _parse_size(max_size)

    to_delete: list[tuple[str, str]] = []  # (path, reason)

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            reasons = []

            # 通配符匹配
            if pattern and not fnmatch.fnmatch(fname, pattern):
                # 也检查扩展名模式
                if not fnmatch.fnmatch(fname, '*' + pattern.strip('*')):
                    continue

            try:
                stat = os.stat(fpath)
                ftime = stat.st_mtime
                fsize = stat.st_size

                if cutoff_time and ftime < cutoff_time:
                    reasons.append(f'旧于 {older_than}')
                if size_limit_bytes is not None and fsize > size_limit_bytes:
                    reasons.append(f'大于 {max_size}')

                if reasons:
                    to_delete.append((fpath, ', '.join(reasons)))
            except OSError:
                continue

    # 清理空目录
    empty_dir_list = []
    if empty_dirs:
        for root, dirs, filenames in os.walk(src_dir, topdown=False):
            if not dirs and not filenames:
                empty_dir_list.append(root)

    if not to_delete and not empty_dir_list:
        echo('✅ 无需清理的文件', fg='green')
        return

    from scripts.table_format import tabulate
    echo(f'🧹 待清理: {len(to_delete)} 文件 + {len(empty_dir_list)} 空目录', fg='yellow')

    del_rows = [{'路径': p, '原因': r, '大小': FileInfo(p).size_human} for p, r in to_delete]
    print(tabulate(del_rows, tablefmt='grid'))

    if dry_run:
        return

    if confirm('\n⚠️ 确认清理以上项目?'):
        deleted = 0
        freed = 0
        for fpath, reason in to_delete:
            try:
                sz = os.path.getsize(fpath)
                os.remove(fpath)
                deleted += 1
                freed += sz
            except OSError as e:
                echo(f'  删除失败: {fpath}', fg='red')

        for dpath in empty_dir_list:
            try:
                os.rmdir(dpath)
                deleted += 1
            except OSError as e:
                echo(f'  删除目录失败: {dpath}', fg='red')

        def fmt_sz(b):
            for u in ['B', 'KB', 'MB', 'GB']:
                if b < 1024:
                    return f'{b:.1f} {u}'
                b /= 1024
            return f'{b:.1f} TB'

        echo(f'✅ 已清理 {deleted} 项，释放 {fmt_sz(freed)}', fg='green')


def cmd_find(args):
    """高级文件搜索"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    name_pattern = args.get('name', '*')
    contains_text = args.get('contains', '')
    ext_filter = args.get('ext', '').split(',') if args.get('ext') else []
    min_size = _parse_size(args.get('min_size', '0')) if args.get('min_size') else None
    max_size = _parse_size(args.get('max_size', '0')) if args.get('max_size') else None
    newer_than = args.get('newer_than', '')
    max_depth = int(args.get('depth', 0)) if args.get('depth') else 0
    output = args.get('o', '')

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    results = []
    search_start = src_dir.count(os.sep)
    now = time.time()
    newer_cutoff = _parse_duration(newer_than, now) if newer_than else None

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', '.venv')]

        if max_depth:
            current_depth = root.count(os.sep) - search_start
            if current_depth >= max_depth:
                dirs.clear()
                continue

        for fname in filenames:
            # 名称过滤
            if not fnmatch.fnmatch(fname, name_pattern) and name_pattern != '*':
                continue
            # 扩展名过滤
            if ext_filter and ext_filter != ['']:
                fext = os.path.splitext(fname)[1].lower()
                if fext not in [e.lower().strip() for e in ext_filter]:
                    continue

            fpath = os.path.join(root, fname)
            fi = FileInfo(fpath)

            # 大小过滤
            if min_size and fi.size < min_size:
                continue
            if max_size and fi.size > max_size:
                continue
            # 时间过滤
            if newer_cutoff and fi.mtime < newer_cutoff:
                continue

            # 内容搜索
            if contains_text:
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        if contains_text not in f.read():
                            continue
                except (OSError, UnicodeDecodeError):
                    continue

            results.append(fi)

    from scripts.table_format import tabulate
    echo(f'🔍 找到 {len(results)} 个匹配文件:', fg='cyan')
    res_rows = [{
        '名称': fi.name,
        '大小': fi.size_human,
        '修改时间': fi.mtime_str,
        '路径': fi.path,
    } for fi in results[:100]]
    print(tabulate(res_rows, tablefmt='grid'))

    if len(results) > 100:
        echo(f'  ... 还有 {len(results)-100} 个结果', fg='yellow')

    # 导出结果
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump([{'path': fi.path, 'name': fi.name, 'size': fi.size} for fi in results],
                      f, ensure_ascii=False, indent=2)
        echo(f'\n📄 结果已导出: {output}', fg='green')


def cmd_tree(args):
    """树形展示目录结构"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    max_depth = int(args.get('depth', 3))
    show_hidden = args.get('all', False)
    show_size = args.get('size', False)

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    lines = []
    total_files = 0
    total_dirs = 0

    def walk(dir_path: str, prefix: str = '', depth: int = 0):
        nonlocal total_files, total_dirs
        if depth > max_depth:
            return

        try:
            entries = sorted(os.listdir(dir_path))
        except PermissionError:
            lines.append(f'{prefix}└── [无权限]')
            return

        for idx, entry in enumerate(entries):
            if not show_hidden and entry.startswith('.'):
                continue
            full_path = os.path.join(dir_path, entry)
            is_last = idx == len(entries) - 1
            connector = '└── ' if is_last else '├── '
            extension = '    ' if is_last else '│   '

            if os.path.isdir(full_path):
                total_dirs += 1
                line = f'{prefix}{connector}{color(entry, "blue")}/'
                if show_size:
                    line += f' ({color("[DIR]", "cyan")})'
                lines.append(line)
                walk(full_path, prefix + extension, depth + 1)
            else:
                total_files += 1
                fi = FileInfo(full_path)
                line = f'{prefix}{connector}{entry}'
                if show_size:
                    line += f' ({fi.size_human})'
                lines.append(line)

    lines.append(color(f'{src_dir}', bold=True))
    walk(src_dir)
    lines.append('')
    lines.append(f'{total_dirs} directories, {total_files} files')

    result = '\n'.join(lines)
    print(result)

    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            f.write(result)


def cmd_sync(args):
    """双向文件同步预览"""
    src_dir = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    dst_dir = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''
    dry_run = args.get('dry_run', True)
    delete_orphans = args.get('delete', False)

    if not src_dir or not dst_dir:
        echo('用法: sync <源目录> <目标目录> [--delete] [--no-dry-run]', fg='yellow')
        return

    if not os.path.isdir(src_dir):
        echo(f'❌ 源目录不存在: {src_dir}', fg='red')
        sys.exit(1)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
        echo(f'📁 目标目录不存在，已创建: {dst_dir}', fg='cyan')

    # 收集两侧文件信息
    def collect(base_dir):
        file_dict: dict[str, float] = {}
        for root, _, filenames in os.walk(base_dir):
            for fname in filenames:
                rel = os.path.relpath(os.path.join(root, fname), base_dir).replace('\\', '/')
                try:
                    file_dict[rel] = os.path.getmtime(os.path.join(root, fname))
                except OSError:
                    pass
        return file_dict

    src_files = collect(src_dir)
    dst_files = collect(dst_dir)

    # 比较
    only_in_src = set(src_files.keys()) - set(dst_files.keys())
    only_in_dst = set(dst_files.keys()) - set(src_files.keys())
    both = set(src_files.keys()) & set(dst_files.keys())
    newer_in_src = {f for f in both if src_files[f] > dst_files[f]}
    newer_in_dst = {f for f in both if dst_files[f] > src_files[f]}

    from scripts.table_format import tabulate

    actions = []
    for f in sorted(only_in_src):
        actions.append({'操作': 'COPY→', '文件': f, '说明': '仅存在于源'})
    for f in sorted(only_in_dst):
        op = 'DELETE' if delete_orphans else '孤立'
        actions.append({'操作': op, '文件': f, '说明': '仅存在于目标'})
    for f in sorted(newer_in_src):
        actions.append({'操作': '更新→', '文件': f, '说明': '源更新'})
    for f in sorted(newer_in_dst):
        actions.append({'操作': '←更新', '文件': f, '说明': '目标更新'})

    echo(f'🔄 同步预览: {src_dir} ↔ {dst_dir}', fg='cyan', bold=True)
    if actions:
        print(tabulate(actions, tablefmt='grid'))
        echo(f'共 {len(actions)} 项操作', fg='yellow')
    else:
        echo('✅ 两边完全一致', fg='green')

    if dry_run:
        return

    if actions and confirm('\n⚠️ 确认执行以上同步操作?'):
        copied = 0
        for f in only_in_src:
            s = os.path.join(src_dir, f.replace('/', os.sep))
            d = os.path.join(dst_dir, f.replace('/', os.sep))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            copied += 1
        for f in newer_in_src:
            s = os.path.join(src_dir, f.replace('/', os.sep))
            d = os.path.join(dst_dir, f.replace('/', os.sep))
            shutil.copy2(s, d)
            copied += 1
        for f in newer_in_dst:
            s = os.path.join(dst_dir, f.replace('/', os.sep))
            d = os.path.join(src_dir, f.replace('/', os.sep))
            shutil.copy2(s, d)
            copied += 1
        if delete_orphans:
            for f in only_in_dst:
                d = os.path.join(dst_dir, f.replace('/', os.sep))
                os.remove(d)
                copied += 1
        echo(f'✅ 同步完成: {copied} 项操作', fg='green')


def cmd_batch_replace(args):
    """批量文本替换（文件内搜索替换）"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    from_str = args.get('from', '')
    to_str = args.get('to', '')
    ext_filter = args.get('ext', '').split(',') if args.get('ext') else []
    regex_flag = args.get('regex', False)
    dry_run = args.get('dry_run', False)

    if not from_str:
        echo('⚠️ 请提供 --from 和 --to 参数', fg='yellow')
        return

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    replacements = []

    for root, dirs, filenames in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', '.venv')]
        for fname in filenames:
            if ext_filter:
                if os.path.splitext(fname)[1].lower() not in [e.lower().strip() for e in ext_filter]:
                    continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, PermissionError):
                continue

            if regex_flag:
                matches = re.findall(from_str, content)
                if matches:
                    new_content = re.sub(from_str, to_str, content)
                    count = len(matches)
                    replacements.append((fpath, count, content != new_content))
                    if not dry_run:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
            else:
                count = content.count(from_str)
                if count > 0:
                    new_content = content.replace(from_str, to_str)
                    replacements.append((fpath, count, True))
                    if not dry_run:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

    if not replacements:
        echo('✅ 未找到匹配内容', fg='green')
        return

    from scripts.table_format import tabulate
    rows = [{'文件': r[0], '替换次数': r[1]} for r in replacements]
    echo(f'🔄 将在 {len(replacements)} 个文件中执行替换:', fg='cyan')
    print(tabulate(rows, tablefmt='grid'))

    if dry_run:
        total_replacements = sum(r[1] for r in replacements)
        echo(f'(共 {total_replacements} 处替换)', fg='yellow')


def cmd_archive(args):
    """归档旧文件"""
    src_dir = args['_pos'][0] if args.get('_pos') else '.'
    zip_mode = args.get('zip', False)
    older_than = args.get('older_than', '30d')
    pattern = args.get('pattern', '*')
    archive_name = args.get('archive', 'archive')
    dry_run = args.get('dry_run', False)

    if not os.path.isdir(src_dir):
        echo(f'❌ 目录不存在: {src_dir}', fg='red')
        sys.exit(1)

    now = time.time()
    cutoff = _parse_duration(older_than, now)

    archive_dir = os.path.join(src_dir, archive_name)
    to_archive = []

    for root, dirs, filenames in os.walk(src_dir):
        # 跳过归档目录自身
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', archive_name)]
        for fname in filenames:
            if not fnmatch.fnmatch(fname, pattern):
                continue
            fpath = os.path.join(root, fname)
            try:
                mtime = os.path.getmtime(fpath)
                if mtime < cutoff:
                    to_archive.append(fpath)
            except OSError:
                continue

    if not to_archive:
        echo('✅ 无需归档的文件', fg='green')
        return

    echo(f'📦 待归档 {len(to_archive)} 个文件 (早于 {older_than}):', fg='cyan')
    total_size = sum(os.path.getsize(f) for f in to_archive if os.path.exists(f))
    echo(f'   总大小: {_human_size(total_size)}', fg='cyan')

    if dry_run:
        for f in to_archive[:20]:
            echo(f'  - {f}', fg='yellow')
        if len(to_archive) > 20:
            echo(f'  ... 还有 {len(to_archive)-20} 个', fg='yellow')
        return

    if not confirm(f'⚠️ 确认归档这 {len(to_archive)} 个文件?'):
        return

    os.makedirs(archive_dir, exist_ok=True)
    moved = 0
    for fpath in to_archive:
        rel = os.path.relpath(fpath, src_dir)
        dest = os.path.join(archive_dir, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(fpath, dest)
        moved += 1

    # 如果需要压缩
    if zip_mode:
        zip_path = os.path.join(src_dir, f'{archive_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip')
        shutil.make_archive(zip_path[:-4], 'zip', archive_dir)
        shutil.rmtree(archive_dir)
        echo(f'✅ 归档完成: {moved} 个文件 → {zip_path}', fg='green')
    else:
        echo(f'✅ 归档完成: {moved} 个文件 → {archive_dir}/', fg='green')


# ─── 工具函数 ─────────────────────────────────────────────────

def _parse_duration(duration_str: str, reference_time: float) -> float:
    """解析持续时间字符串为 Unix 时间戳阈值"""
    m = re.match(r'^(\d+)\s*(d|day|days|h|hour|hour|m|min|mins|w|week|weeks|y|year|years)$',
                 duration_str.lower().strip())
    if not m:
        raise ValueError(f'无法解析时间: {duration_str}')

    value = int(m.group(1))
    unit = m.group(2)

    multipliers = {
        'm': 60, 'min': 60, 'mins': 60,
        'h': 3600, 'hour': 3600, 'hours': 3600,
        'd': 86400, 'day': 86400, 'days': 86400,
        'w': 604800, 'week': 604800, 'weeks': 604800,
        'y': 31536000, 'year': 31536000, 'years': 31536000,
    }

    seconds = value * multipliers.get(unit, 86400)
    return reference_time - seconds


def _parse_size(size_str: str) -> int:
    """解析文件大小字符串为字节数"""
    m = re.match(r'^(\d+(?:\.\d+)?)\s*(B|K|KB|M|MB|G|GB|T|TB)?$',
                 size_str.upper().strip())
    if not m:
        raise ValueError(f'无法解析大小: {size_str}')

    value = float(m.group(1))
    unit = (m.group(2) or 'B').upper()

    multipliers = {'B': 1, 'K': 1024, 'KB': 1024, 'M': 1048576, 'MB': 1048576,
                   'G': 1073741824, 'GB': 1073741824, 'T': 1099511627776, 'TB': 1099511627776}
    return int(value * multipliers[unit])


def _human_size(byte_count: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_count < 1024:
            return f'{byte_count:.1f} {unit}'
        byte_count /= 1024
    return f'{byte_count:.1f} PB'


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'classify': cmd_classify,
    'rename': cmd_rename,
    'dedup': cmd_dedup,
    'scan': cmd_scan,
    'clean': cmd_clean,
    'find': cmd_find,
    'tree': cmd_tree,
    'sync': cmd_sync,
    'batch-replace': cmd_batch_replace,
    'archive': cmd_archive,
}

ALIASES = {
    'sort-files': 'classify', 'organize': 'classify',
    'batch-rename': 'rename',
    'duplicate': 'dedup', 'dup': 'dedup',
    'report': 'scan', 'du': 'scan',
    'cleanup': 'clean', 'purge': 'clean',
    'search': 'find', 'grep-file': 'find',
    'ls-tree': 'tree', 'list': 'tree',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
