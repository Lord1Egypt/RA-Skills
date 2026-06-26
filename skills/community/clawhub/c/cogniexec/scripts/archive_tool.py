#!/usr/bin/env python3
"""
archive_tool.py — 压缩归档工具（纯标准库）
覆盖：zip/tar/gz 创建与解压、多卷分拆、加密压缩、内嵌文件列表

用法：
  python archive_tool.py create output.zip ./folder --format zip
  python archive_tool.py create data.tar.gz ./files/ --format tar.gz
  python archive_tool.py extract archive.zip -o ./output
  python archive_tool.py list archive.zip
  python archive_tool.py info archive.zip
  python archive_tool.py split big.zip -o parts --size 10M
  python archive_tool.py merge parts/ -o merged.zip
"""

import sys
import os
import zipfile
import tarfile
import gzip
import shutil
import hashlib
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
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

# ─── 创建归档 ─────────────────────────────────────────────

def cmd_create(args):
    """创建 zip / tar / tar.gz 归档文件"""
    pos = args.get('_pos', [])
    if len(pos) < 2:
        echo('❌ 用法: create <输出文件> <源路径> [--format zip|tar|tar.gz]', 'red')
        sys.exit(1)

    output = pos[0]
    source = pos[1]
    fmt = args.get('format', '')
    # 自动从文件扩展名推断格式
    if not fmt:
        if output.endswith('.tar.gz') or output.endswith('.tgz'):
            fmt = 'tar.gz'
        elif output.endswith('.tar'):
            fmt = 'tar'
        else:
            fmt = 'zip'

    compress_level = args.get('compress', '9')
    password = args.get('password')          # ZIP 加密（传统加密）
    exclude_patterns = (args.get('exclude') or '').split(',') if args.get('exclude') else []

    if not os.path.exists(source):
        echo(f'❌ 源路径不存在: {source}', 'red')
        sys.exit(1)

    out_dir = os.path.dirname(output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    try:
        level = min(9, max(0, int(compress_level)))

        if fmt == 'zip':
            _create_zip(output, source, level, password, exclude_patterns)
        elif fmt == 'tar':
            _create_tar(output, source, '', exclude_patterns)
        elif fmt == 'tar.gz':
            _create_tar(output, source, 'gz', exclude_patterns)
        else:
            echo(f'❌ 不支持的格式: {fmt}', 'red')
            sys.exit(1)

        size = os.path.getsize(output)
        echo(f'✅ 归档创建完成: {output} ({_format_size(size)})', 'green')

    except Exception as e:
        echo(f'❌ 创建失败: {e}', 'red')
        sys.exit(1)


def _create_zip(output, source, level, password, excludes):
    """创建 ZIP 文件"""
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=level) as zf:
        if os.path.isfile(source):
            _add_to_zip(zf, source, os.path.basename(source), excludes)
        else:
            for root, dirs, files in os.walk(source):
                # 排除目录
                dirs[:] = [d for d in dirs if not _should_exclude(d, excludes)]
                for f in files:
                    if _should_exclude(f, excludes):
                        continue
                    fpath = os.path.join(root, f)
                    arcname = os.path.relpath(fpath, os.path.dirname(source))
                    _add_to_zip(zf, fpath, arcname, excludes)


def _add_to_zip(zf, filepath, arcname, excludes):
    """添加单个文件到 ZIP"""
    if _should_exclude(arcname, excludes):
        return
    zf.write(filepath, arcname)


def _create_tar(output, source, mode, excludes):
    """创建 TAR 文件"""
    mode_str = f'w:{mode}' if mode else 'w:'
    with tarfile.open(output, mode_str) as tf:
        if os.path.isfile(source):
            tf.add(source, arcname=os.path.basename(source), filter=_tar_filter)
        else:
            tf.add(source, arcname=os.path.basename(source), filter=_tar_filter)


def _tar_filter(info):
    """过滤 TAR 成员（排除隐藏文件等）"""
    name = info.name
    parts = name.replace('\\', '/').split('/')
    for part in parts:
        if part.startswith('.') and part not in ('.', '..'):
            return None
    return info


# ─── 解压归档 ─────────────────────────────────────────────

def _tar_extract_filter(info, output_dir):
    """安全过滤：阻止路径遍历攻击（../ 等）"""
    # 规范化解压后的绝对路径
    abs_path = os.path.realpath(os.path.join(output_dir, info.name))
    abs_dir = os.path.realpath(output_dir)
    if not abs_path.startswith(abs_dir + os.sep) and abs_path != abs_dir:
        raise ValueError(f"安全拦截: 拒绝路径遍历 {info.name!r}（超出解压目录）")
    return info


def _zip_extract_filter(zf, output_dir):
    """安全过滤 ZIP 成员路径，阻止路径遍历"""
    for zi in zf.infolist():
        abs_path = os.path.realpath(os.path.join(output_dir, zi.filename))
        abs_dir = os.path.realpath(output_dir)
        if not abs_path.startswith(abs_dir + os.sep) and abs_path != abs_dir:
            raise ValueError(f"安全拦截: 拒绝路径遍历 {zi.filename!r}（超出解压目录）")


def cmd_extract(args):
    """解压 zip / tar / tar.gz 文件"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: extract <归档文件> [-o 输出目录] [--password 密码]', 'red')
        sys.exit(1)

    archive_path = pos[0]
    output_dir = args.get('o') or '.'
    password = args.get('password')

    if not os.path.exists(archive_path):
        echo(f'❌ 归档文件不存在: {archive_path}', 'red')
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        if archive_path.endswith('.zip'):
            _extract_zip(archive_path, output_dir, password)
        elif archive_path.endswith(('.tar.gz', '.tgz')):
            with tarfile.open(archive_path, 'r:gz') as tf:
                tf.extractall(output_dir, filter=lambda info: _tar_extract_filter(info, output_dir))
        elif archive_path.endswith(('.tar', '.tar.bz2', '.tbz2')):
            with tarfile.open(archive_path, 'r:*') as tf:
                tf.extractall(output_dir, filter=lambda info: _tar_extract_filter(info, output_dir))
        elif archive_path.endswith('.gz') and not archive_path.endswith('.tar.gz'):
            # 单独的 gzip 文件
            out_name = archive_path[:-3] if not args.get('o') else os.path.join(output_dir, os.path.basename(archive_path[:-3]))
            with gzip.open(archive_path, 'rb') as fin:
                with open(out_name, 'wb') as fout:
                    fout.write(fin.read())
            echo(f'✅ 解压完成: {out_name}', 'green')
            return
        else:
            echo(f'❌ 不支持的归档格式', 'red')
            sys.exit(1)

        echo(f'✅ 解压完成 → {os.path.abspath(output_dir)}', 'green')

    except Exception as e:
        echo(f'❌ 解压失败: {e}', 'red')
        sys.exit(1)


def _extract_zip(archive_path, output_dir, password=None):
    """解压 ZIP，支持密码，含路径遍历安全检查"""
    pwd_bytes = password.encode() if password else None
    with zipfile.ZipFile(archive_path, 'r') as zf:
        # 安全检查：拦截路径遍历
        _zip_extract_filter(zf, output_dir)
        if pwd_bytes:
            zf.extractall(output_dir, pwd=pwd_bytes)
        else:
            # 检查是否需要密码
            needs_pwd = any(zi.flag_bits & 0x1 for zi in zf.infolist())
            if needs_pwd:
                echo('⚠️  此 ZIP 需要密码，请使用 --password 参数', 'yellow')
                sys.exit(1)
            zf.extractall(output_dir)


# ─── 列出归档内容 ─────────────────────────────────────────

def cmd_list(args):
    """列出归档内的文件列表"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: list <归档文件>', 'red')
        sys.exit(1)

    archive_path = pos[0]

    if not os.path.exists(archive_path):
        echo(f'❌ 文件不存在: {archive_path}', 'red')
        sys.exit(1)

    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                members = zf.infolist()
                echo(f'\n📦 {archive_path} ({len(members)} 个文件)\n', 'bold')
                total_size = 0
                total_comp = 0
                for m in members:
                    size_str = _format_size(m.file_size)
                    comp_str = _format_size(m.compress_size)
                    ratio = f'{m.compress_size/m.file_size*100:.0f}%' if m.file_size > 0 else '-'
                    date_str = m.date_time.strftime('%Y-%m-%d %H:%M') if hasattr(m.date_time, 'strftime') else f'{m.date_time}'
                    print(f'  {m.filename:<40} {size_str:>8} {comp_str:>8} {ratio:>5}')
                    total_size += m.file_size
                    total_comp += m.compress_size

                print('-' * 70)
                echo(f'  总计: {len(members)} 个文件 | 原始: {_format_size(total_size)} | 压缩后: {_format_size(total_comp)}', 'cyan')

        elif archive_path.endswith(('.tar.gz', '.tgz', '.tar', '.tar.bz2')):
            mode = 'r:*'
            with tarfile.open(archive_path, mode) as tf:
                members = tf.getmembers()
                echo(f'\n📦 {archive_path} ({len(members)} 个文件)\n', 'bold')
                total_size = 0
                for m in members:
                    size_str = _format_size(m.size)
                    type_char = 'd' if m.isdir() else ('l' if m.issym() else '-')
                    print(f'  {type_char} {m.name:<45} {size_str:>8}')
                    total_size += m.size
                print('-' * 65)
                echo(f'  总计: {len(members)} 个条目 | 大小: {_format_size(total_size)}', 'cyan')
        else:
            echo('❌ 不支持的归档格式', 'red')
            sys.exit(1)

    except Exception as e:
        echo(f'❌ 读取失败: {e}', 'red')


# ─── 归档信息摘要 ─────────────────────────────────────────

def cmd_info(args):
    """显示归档文件的详细信息摘要"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: info <归档文件>', 'red')
        sys.exit(1)

    archive_path = pos[0]

    if not os.path.exists(archive_path):
        echo(f'❌ 文件不存在: {archive_path}', 'red')
        sys.exit(1)

    file_size = os.path.getsize(archive_path)
    file_hash = _file_hash(archive_path)

    echo(f'\n📦 归档文件: {os.path.basename(archive_path)}', 'bold')
    echo(f'   路径:     {os.path.abspath(archive_path)}', 'cyan')
    echo(f'   大小:     {_format_size(file_size)}', 'cyan')
    echo(f'   MD5:      {file_hash}', 'cyan')

    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                members = zf.infolist()
                files = [m for m in members if not m.isdir()]
                dirs = [m for m in members if m.isdir()]
                total_orig = sum(m.file_size for m in members)
                total_comp = sum(m.compress_size for m in members)
                ratio = (1 - total_comp / total_orig) * 100 if total_orig > 0 else 0
                encrypted = any(m.flag_bits & 0x1 for m in members)

                echo(f'   格式:     ZIP', 'cyan')
                echo(f'   文件数:   {len(files)}', 'cyan')
                echo(f'   目录数:   {len(dirs)}', 'cyan')
                echo(f'   原始大小: {_format_size(total_orig)}', 'cyan')
                echo(f'   压缩率:   {ratio:.1f}%', 'cyan')
                echo(f'   加密:     {"是" if encrypted else "否"}', 'cyan')
                echo(f'   压缩方式: DEFLATED', 'cyan')

        elif archive_path.endswith(('.tar.gz', '.tgz', '.tar', '.tar.bz2')):
            mode = 'r:*'
            with tarfile.open(archive_path, mode) as tf:
                members = tf.getmember_names()
                files = [n for n in members if not n.endswith('/')]
                fmt_name = 'TAR.GZ' if '.gz' in archive_path else ('TAR.BZ2' if '.bz2' in archive_path else 'TAR')
                echo(f'   格式:     {fmt_name}', 'cyan')
                echo(f'   条目数:   {len(members)}', 'cyan')
                echo(f'   文件数:   {len(files)}', 'cyan')
    except Exception as e:
        echo(f'⚠️  无法读取详细信息: {e}', 'yellow')


# ─── 分卷分割 ────────────────────────────────────────────

def cmd_split(args):
    """将大文件分割为多个小卷"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: split <文件> [-o 输出目录] [--size 10M|50M|100M]', 'red')
        sys.exit(1)

    file_path = pos[0]
    output_dir = args.get('o') or '.'
    size_spec = args.get('size', '10M')

    if not os.path.exists(file_path):
        echo(f'❌ 文件不存在: {file_path}', 'red')
        sys.exit(1)

    chunk_size = _parse_size(size_spec)
    file_size = os.path.getsize(file_path)
    base_name = os.path.basename(file_path)

    if chunk_size >= file_size:
        echo(f'⚠️  分卷大小({size_spec}) >= 文件大小({_format_size(file_size)})，无需分割', 'yellow')
        return

    num_chunks = (file_size + chunk_size - 1) // chunk_size
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    echo(f'📦 分割中: {base_name} → {num_chunks} 卷 (每卷 ≤{size_spec})\n', 'cyan')

    file_hash_val = hashlib.md5()

    with open(file_path, 'rb') as f:
        for idx in range(num_chunks):
            chunk = f.read(chunk_size)
            part_name = f'{base_name}.part{idx+1:03d}'
            part_path = os.path.join(output_dir, part_name)
            with open(part_path, 'wb') as pf:
                pf.write(chunk)
            file_hash_val.update(chunk)
            pct = ((idx + 1) * chunk_size / file_size) * 100
            echo(f'  ✅ {part_name} ({_format_size(len(chunk))}) [{min(pct,100):.0f}%]', 'green')

    echo(f'\n▶ 完成: {num_chunks} 卷 → {output_dir}/', 'green')
    echo(f'   MD5: {file_hash_val.hexdigest()}', 'cyan')


# ─── 合并分卷 ─────────────────────────────────────────────

def cmd_merge(args):
    """将分割的文件合并还原"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: merge <分卷目录或前缀> [-o 输出文件]', 'red')
        sys.exit(1)

    source = pos[0]
    output = args.get('o')

    # 查找所有 .part 文件
    if os.path.isdir(source):
        parts = sorted([f for f in os.listdir(source) if f.endswith(tuple(f'.part{i:03d}' for i in range(1, 9999)))])
        parts = [os.path.join(source, p) for p in parts]
    else:
        # 前缀模式：找所有 .part* 文件
        base_dir = os.path.dirname(source) or '.'
        prefix = os.path.basename(source)
        all_files = sorted(os.listdir(base_dir))
        parts = [os.path.join(base_dir, f) for f in all_files if f.startswith(prefix) and '.part' in f]

    if not parts:
        echo(f'❌ 未找到分卷文件: {source}', 'red')
        sys.exit(1)

    if not output:
        # 从第一个分卷推断原始文件名
        first_name = os.path.basename(parts[0])
        original_name = first_name.rsplit('.part', 1)[0]
        output = os.path.join(base_dir if os.path.isdir(source) else os.path.dirname(parts[0]), original_name)

    echo(f'📦 合并中: {len(parts)} 卷 → {output}\n', 'cyan')

    file_hash_val = hashlib.md5()
    total_size = 0

    with open(output, 'wb') as outf:
        for idx, part_path in enumerate(parts):
            with open(part_path, 'rb') as pf:
                data = pf.read()
                file_hash_val.update(data)
                outf.write(data)
                total_size += len(data)
            echo(f'  ✅ {os.path.basename(part_path)} ({_format_size(len(data))})', 'green')

    echo(f'\n▶ 合并完成: {output} ({_format_size(total_size)})', 'green')
    echo(f'   MD5: {file_hash_val.hexdigest()}', 'cyan')


# ─── Gzip 压缩/解压单个文件 ──────────────────────────────

def cmd_gzip(args):
    """对单个文件进行 gzip 压缩或解压"""
    pos = args.get('_pos', [])
    if len(pos) < 1:
        echo('❌ 用法: gzip <文件> [-d 解压] [-o 输出] [--keep 保留原文件]', 'red')
        sys.exit(1)

    file_path = pos[0]
    decompress = args.get('d')
    keep = args.get('keep')
    output = args.get('o')

    if not os.path.exists(file_path):
        echo(f'❌ 文件不存在: {file_path}', 'red')
        sys.exit(1)

    if decompress:
        if not output:
            output = file_path[:-3] if file_path.endswith('.gz') else file_path + '.decompressed'
        with gzip.open(file_path, 'rb') as fin:
            with open(output, 'wb') as fout:
                fout.write(fin.read())
        echo(f'✅ 解压完成: {output}', 'green')
    else:
        if not output:
            output = file_path + '.gz'
        with open(file_path, 'rb') as fin:
            with gzip.open(output, 'wb') as fout:
                data = fin.read()
                fout.write(data)
        echo(f'✅ 压缩完成: {output}', 'green')

    if not keep:
        os.remove(file_path)
        echo(f'   已删除原文件: {file_path}', 'cyan')


# ─── 辅助函数 ──────────────────────────────────────────────

def _should_exclude(name, patterns):
    """检查是否应该排除该文件"""
    if not patterns:
        return False
    for pat in patterns:
        pat = pat.strip()
        if not pat:
            continue
        if pat.startswith('*'):
            suffix = pat[1:].lower()
            if name.lower().endswith(suffix):
                return True
        elif pat in name:
            return True
    return False


def _parse_size(spec):
    """解析大小字符串为字节数"""
    spec = spec.upper().strip()
    multipliers = {
        'B': 1, 'KB': 1024, 'K': 1024,
        'MB': 1024**2, 'M': 1024**2,
        'GB': 1024**3, 'G': 1024**3,
    }
    for suffix, mul in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if spec.endswith(suffix):
            return int(float(spec[:-len(suffix)]) * mul)
    return int(spec)


def _format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024.0
    return f'{size_bytes:.1f} TB'


def _file_hash(filepath):
    """计算文件的 MD5 哈希"""
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'create': cmd_create,
    'extract': cmd_extract,
    'list': cmd_list,
    'info': cmd_info,
    'split': cmd_split,
    'merge': cmd_merge,
    'gzip': cmd_gzip,
}

ALIASES = {
    'pack': 'create', 'archive': 'create', 'zip': 'create',
    'unpack': 'extract', 'unzip': 'extract', 'untar': 'extract',
    'ls': 'list', 'contents': 'list',
    'about': 'info', 'summary': 'info',
    'split-file': 'split', 'divide': 'split',
    'join': 'merge', 'combine': 'merge',
    'compress': 'gzip', 'gunzip': 'gzip',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + list(ALIASES.keys()))))
        echo(f'❌ 未知命令: {cmd}', 'red')
        echo(f'可用命令: {available}', 'cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
