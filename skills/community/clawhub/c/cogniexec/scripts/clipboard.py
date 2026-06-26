#!/usr/bin/env python3
"""
clipboard.py — 系统剪贴板读写工具（纯标准库 + Windows API）
覆盖：文本读取/写入/图片剪贴板/历史记录模拟/格式检测

用法：
  python clipboard.py read                          # 读取剪贴板文本
  python clipboard.py write "Hello World"            # 写入文本
  python clipboard.py write --file data.txt          # 从文件写入
  python clipboard.py copy --file report.pdf         # 复制文件路径
  python clipboard.py clear                          # 清空剪贴板
  python clipboard.py info                           # 查看剪贴板格式信息
  python clipboard.py watch                          # 监听剪贴板变化
  python clipboard.py base64                         # 以 Base64 输出内容
  python clipboard.py hash                           # 计算剪贴板内容的哈希
"""

import sys
import os
import hashlib
import base64
import time


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


# ─── Windows 剪贴板操作（ctypes，纯标准库） ──────────────

try:
    import ctypes
    from ctypes import wintypes

    # Windows 常量
    CF_TEXT = 1
    CF_UNICODETEXT = 13
    CF_HDROP = 15
    GMEM_MOVEABLE = 0x0002

    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32

    OpenClipboard = user32.OpenClipboard
    CloseClipboard = user32.CloseClipboard
    EmptyClipboard = user32.EmptyClipboard
    GetClipboardData = user32.GetClipboardData
    SetClipboardData = user32.SetClipboardData
    GlobalLock = kernel32.GlobalLock
    GlobalUnlock = kernel32.GlobalUnlock
    GlobalAlloc = kernel32.GlobalAlloc
    IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
    EnumClipboardFormats = user32.EnumClipboardFormats
    CountClipboardFormats = user32.CountClipboardFormats
    GetClipboardFormatNameA = user32.GetClipboardFormatNameA

    HAS_CLIPBOARD_API = True
except Exception:
    HAS_CLIPBOARD_API = False


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def _open_clipboard():
    """打开剪贴板"""
    if not HAS_CLIPBOARD_API:
        echo('❌ Windows API 不可用', 'red')
        sys.exit(1)
    for attempt in range(5):
        if OpenClipboard(0):
            return True
        time.sleep(0.05)
    echo('❌ 无法打开剪贴板（可能被其他程序占用）', 'red')
    sys.exit(1)


def _close_clipboard():
    """关闭剪贴板"""
    CloseClipboard()


# ─── read: 读取剪贴板 ──────────────────────────────────────

def cmd_read(args):
    """读取当前剪贴板的文本内容"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    try:
        _open_clipboard()

        # 优先读取 Unicode 文本
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                if ptr:
                    text = ctypes.wstring_at(ptr)
                    GlobalUnlock(h_data)
                    _close_clipboard()
                    # 输出（不换行，方便管道使用）
                    output = args.get('o')
                    if output:
                        with open(output, 'w', encoding='utf-8') as f:
                            f.write(text)
                        echo(f'✅ 已保存到 {output}', 'green')
                    else:
                        print(text, end='')
                    return

        # 回退到 ANSI 文本
        if IsClipboardFormatAvailable(CF_TEXT):
            h_data = GetClipboardData(CF_TEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                if ptr:
                    text = ctypes.string_at(ptr).decode('utf-8', errors='replace')
                    GlobalUnlock(h_data)
                    _close_clipboard()
                    output = args.get('o')
                    if output:
                        with open(output, 'w', encoding='utf-8') as f:
                            f.write(text)
                        echo(f'✅ 已保存到 {output}', 'green')
                    else:
                        print(text, end='')
                    return

        _close_clipboard()
        echo('(剪贴板无文本内容)', 'yellow')

    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 读取失败: {e}', 'red')


# ─── write: 写入剪贴板 ─────────────────────────────────────

def cmd_write(args):
    """将文本或文件内容写入剪贴板"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    pos = args.get('_pos', [])
    file_path = args.get('file')

    # 获取要写入的文本
    if file_path:
        if not os.path.exists(file_path):
            echo(f'❌ 文件不存在: {file_path}', 'red')
            sys.exit(1)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        source_desc = file_path
    elif pos:
        text = ' '.join(pos)  # 将位置参数拼接为文本
        source_desc = '参数'
    else:
        echo('❌ 请提供文本内容或 --file 参数', 'red')
        sys.exit(1)

    append_mode = args.get('append')

    if append_mode:
        # 追加模式：先读现有内容
        try:
            _open_clipboard()
            if IsClipboardFormatAvailable(CF_UNICODETEXT):
                h_data = GetClipboardData(CF_UNICODETEXT)
                if h_data:
                    ptr = GlobalLock(h_data)
                    existing = ctypes.wstring_at(ptr)
                    GlobalUnlock(h_data)
                    text = existing + text
            _close_clipboard()
        except Exception:
            pass

    try:
        _open_clipboard()
        EmptyClipboard()

        # 编码为 UTF-16LE (Windows Unicode)
        encoded = (text + '\0').encode('utf-16-le')
        size = len(encoded)

        h_global = GlobalAlloc(GMEM_MOVEABLE, size)
        if not h_global:
            _close_clipboard()
            echo('❌ 内存分配失败', 'red')
            sys.exit(1)

        ptr = GlobalLock(h_global)
        ctypes.memmove(ptr, encoded, size)
        GlobalUnlock(h_global)

        result = SetClipboardData(CF_UNICODETEXT, h_global)
        _close_clipboard()

        if result:
            echo(f'✅ 已写入剪贴板 ({len(text)} 字符, 来源: {source_desc})', 'green')
        else:
            echo('⚠️  写入可能失败', 'yellow')

    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 写入失败: {e}', 'red')


# ─── clear: 清空剪贴板 ─────────────────────────────────────

def cmd_clear(args):
    """清空剪贴板"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    try:
        _open_clipboard()
        EmptyClipboard()
        _close_clipboard()
        echo('✅ 剪贴板已清空', 'green')
    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 清空失败: {e}', 'red')


# ─── info: 剪贴板信息 ─────────────────────────────────────

def cmd_info(args):
    """显示剪贴板的详细信息"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    try:
        _open_clipboard()

        total_formats = CountClipboardFormats()
        echo(f'\n📋 剪贴板信息', 'bold')
        echo(f'   格式数量: {total_formats}', 'cyan')

        # 枚举所有可用格式
        format_id = 0
        formats = []
        while True:
            format_id = EnumClipboardFormats(format_id)
            if format_id == 0:
                break

            name_map = {
                1: 'CF_TEXT (ANSI文本)',
                2: 'CF_BITMAP',
                3: 'CF_METAFILEPICT',
                4: 'CF_SYLK',
                5: 'CF_DIF',
                6: 'CF_TIFF',
                7: 'CF_OEMTEXT',
                8: 'CF_DIB',
                9: 'CF_PALETTE',
                10: 'CF_PENDATA',
                11: 'CF_RIFF',
                12: 'CF_WAVE',
                13: 'CF_UNICODETEXT (Unicode文本)',
                14: 'CF_ENHMETAFILE',
                15: 'CF_HDROP (文件列表)',
                16: 'CF_LOCALE',
                17: 'CF_DIBV5',
            }

            fmt_name = name_map.get(format_id, '')
            if not fmt_name and format_id > 0xC000:
                buf = ctypes.create_string_buffer(256)
                ret = GetClipboardFormatNameA(format_id, buf, 256)
                fmt_name = buf.value.decode('utf-8', errors='replace') if ret else f'Registered({format_id})'
            elif not fmt_name:
                fmt_name = f'Unknown({format_id})'

            available = IsClipboardFormatAvailable(format_id)
            status = '✓' if available else ' '
            formats.append((format_id, fmt_name, status))

        if formats:
            echo('\n   格式列表:', 'cyan')
            for fid, fname, st in formats:
                echo(f'   [{st}] [{fid:>5}] {fname}', 'cyan' if st == '✓' else '')

        # 显示文本预览
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                text = ctypes.wstring_at(ptr)
                GlobalUnlock(h_data)
                preview = text[:200].replace('\n', '\\n').replace('\r', '')
                echo(f'\n   文本预览 ({len(text)} 字符):', 'cyan')
                echo(f'   "{preview}{("..." if len(text) > 200 else "")}"', '')

        _close_clipboard()

    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 获取信息失败: {e}', 'red')


# ─── watch: 监听剪贴板变化 ────────────────────────────────

def cmd_watch(args):
    """监听剪贴板变化并输出新内容"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    interval = float(args.get('interval', '0.5'))
    timeout_val = float(args.get('timeout', '0'))  # 0 = 无限等待
    quiet = args.get('quiet')

    last_hash = ''
    start_time = time.time()

    echo(f'👁️  监听剪贴板变化 (间隔={interval}s, Ctrl+C 退出)\n', 'cyan')

    try:
        while True:
            if timeout_val > 0 and (time.time() - start_time) > timeout_val:
                echo(f'\n⏰ 超时 ({timeout_val}s)', 'yellow')
                break

            current_hash = _get_text_hash()
            if current_hash and current_hash != last_hash:
                if last_hash:
                    if not quiet:
                        echo(f'--- [{time.strftime("%H:%M:%S")}] 变化检测到 ---', 'green')
                    _read_and_print(args.get('max_chars'))
                last_hash = current_hash

            time.sleep(interval)

    except KeyboardInterrupt:
        echo(f'\n\n停止监听', 'yellow')


def _get_text_hash():
    """获取剪贴板文本的哈希值用于变化检测"""
    try:
        _open_clipboard()
        h = None
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                text = ctypes.wstring_at(ptr)
                GlobalUnlock(h_data)
                h = hashlib.md5(text.encode()).hexdigest()[:12]
        _close_clipboard()
        return h or ''
    except Exception:
        try:
            _close_clipboard()
        except Exception:
            pass
        return ''


def _read_and_print(max_chars=None):
    """读取并打印当前剪贴板内容"""
    try:
        _open_clipboard()
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                text = ctypes.wstring_at(ptr)
                GlobalUnlock(h_data)
                _close_clipboard()
                limit = int(max_chars) if max_chars else None
                if limit and len(text) > limit:
                    text = text[:limit] + '...'
                print(text)
                return
        _close_clipboard()
    except Exception:
        try:
            _close_clipboard()
        except Exception:
            pass


# ─── base64: Base64 编码输出 ──────────────────────────────

def cmd_base64(args):
    """以 Base64 格式输出剪贴板内容"""
    if not HAS_CLIPBOARD_API:
        echo('❌ 此功能仅支持 Windows', 'red')
        sys.exit(1)

    try:
        _open_clipboard()
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                text = ctypes.wstring_at(ptr)
                GlobalUnlock(h_data)
                _close_clipboard()
                encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
                output = args.get('o')
                if output:
                    with open(output, 'w', encoding='utf-8') as f:
                        f.write(encoded)
                    echo(f'✅ 已保存到 {output}', 'green')
                else:
                    print(encoded)
                return
        _close_clipboard()
        echo('(剪贴板无文本内容)', 'yellow')

    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 操作失败: {e}', 'red')


# ─── hash: 计算哈希 ────────────────────────────────────────

def cmd_hash(args):
    """计算剪贴板内容的哈希值"""
    algo = args.get('algo', 'md5').lower()

    try:
        _open_clipboard()
        if IsClipboardFormatAvailable(CF_UNICODETEXT):
            h_data = GetClipboardData(CF_UNICODETEXT)
            if h_data:
                ptr = GlobalLock(h_data)
                text = ctypes.wstring_at(ptr)
                GlobalUnlock(h_data)
                _close_clipboard()

                h = hashlib.new(algo)
                h.update(text.encode('utf-8'))

                size_bytes = len(text.encode('utf-8'))
                echo(f'算法: {algo.upper()}', 'cyan')
                echo(f'哈希: {h.hexdigest()}', 'bold')
                echo(f'大小: {_format_size(size_bytes)} | 字符数: {len(text)}', 'cyan')
                return
        _close_clipboard()
        echo('(剪贴板无文本内容)', 'yellow')

    except ValueError:
        echo(f'❌ 不支持的哈希算法: {algo}', 'red')
    except Exception as e:
        try:
            _close_clipboard()
        except Exception:
            pass
        echo(f'❌ 操作失败: {e}', 'red')


# ─── 辅助函数 ──────────────────────────────────────────────

def _format_size(size_bytes):
    """格式化大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024.0
    return f'{size_bytes:.1f} TB'


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'read': cmd_read,
    'write': cmd_write,
    'clear': cmd_clear,
    'info': cmd_info,
    'watch': cmd_watch,
    'base64': cmd_base64,
    'hash': cmd_hash,
}

ALIASES = {
    'get': 'read', 'paste': 'read',
    'set': 'write', 'copy': 'write', 'put': 'write', 'clip': 'write',
    'reset': 'clear', 'empty': 'clear',
    'status': 'info', 'about': 'info',
    'monitor': 'watch', 'listen': 'watch',
    'b64': 'base64', 'encode-base64': 'base64',
    'checksum': 'hash', 'fingerprint': 'hash', 'md5': 'hash',
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
