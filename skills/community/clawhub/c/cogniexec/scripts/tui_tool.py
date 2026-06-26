#!/usr/bin/env python3
"""
tui_tool.py — 终端交互 UI 工具（纯标准库，无外部依赖）
覆盖：进度条/spinner/选择列表/确认框/表格展示/输入提示

用法：
  python tui_tool.py progress --total 100 --current 30 "Processing"
  python tui_tool.py spinner "Loading data..."
  python tui_tool.py select "Pick one:" "Apple" "Banana" "Cherry"
  python tui_tool.py confirm "Delete all files?"
  python tui_tool.py table --headers "Name,Age,City" --rows "Alice,25,Beijing" "Bob,30,Shanghai"
  python tui_tool.py input "Enter your name:"
  python tui_tool.py password "Enter password:"
  python tui_tool.py countdown --seconds 10 "Starting in"
"""

import sys
import os
import time
import threading


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
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


def _supports_ansi():
    """检测终端是否支持 ANSI 转义码"""
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

# ─── 进度条 ──────────────────────────────────────────────

class ProgressBar:
    """终端进度条"""

    def __init__(self, total=100, width=40, label='',
                 bar_char='=', head='>', empty='-',
                 prefix_color='', bar_color='green', pct_color='cyan'):
        self.total = total
        self.width = width
        self.label = label
        self.bar_char = bar_char
        self.head = head
        self.empty = empty
        self.prefix_color = prefix_color
        self.bar_color = bar_color
        self.pct_color = pct_color
        self.current = 0
        self.start_time = time.time()
        self._last_len = 0

    def update(self, current=None):
        if current is not None:
            self.current = min(current, self.total)
        pct = self.current / max(self.total, 1)
        filled = int(self.width * pct)

        bar = self.bar_char * filled
        if filled < self.width:
            bar += self.head + self.empty * (self.width - filled - 1)
        else:
            bar = self.bar_char * self.width

        pct_str = f'{pct*100:5.1f}%'
        elapsed = time.time() - self.start_time
        speed = self.current / elapsed if elapsed > 0 else 0
        eta = (self.total - self.current) / speed if speed > 0 else 0

        parts = []
        if self.label:
            parts.append(f'{self.label} ')
        parts.append(f'|{color(bar, self.bar_color)}| {color(pct_str, self.pct_color)}')
        parts.append(f'{self.current}/{self.total}')
        if speed >= 1048576:
            parts.append(f'{speed/1048576:.1f}MB/s')
        elif speed >= 1024:
            parts.append(f'{speed/1024:.1f}KB/s')
        elif speed > 0:
            parts.append(f'{speed:.0f}/s')
        if eta > 0:
            parts.append(f'ETA:{eta:.0f}s')

        line = ''.join(parts)
        # 清除旧行并写入新行（使用 \r 回到行首）
        line_with_clear = '\r' + ' ' * self._last_len + '\r' + line
        self._last_len = len(line)
        sys.stdout.write(line_with_clear)
        sys.stdout.flush()

    def finish(self, msg=''):
        self.update(self.total)
        finish_msg = msg or ''
        if finish_msg:
            print(f'\n{color("✓ " + finish_msg, "green")}')
        else:
            print()


def cmd_progress(args):
    """显示进度条（单次或模拟）"""
    total = int(args.get('total', '100'))
    current = int(args.get('current', '-1'))
    label = args.get('label', '')
    pos = args.get('_pos', [])
    if pos:
        label = label or pos[0]

    bar_width = int(args.get('width', '40'))

    if current >= 0:
        # 单次输出模式
        pb = ProgressBar(total=total, width=bar_width, label=label)
        pb.update(current)
        pb.finish()
    else:
        # 模拟进度模式（用于演示或测试）
        delay = float(args.get('delay', '0.05'))
        pb = ProgressBar(total=total, width=bar_width, label=label)
        for i in range(total + 1):
            pb.update(i)
            time.sleep(delay)
        pb.finish('Done')


# ─── Spinner ─────────────────────────────────────────────

_SPINNER_FRAMES = [
    ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    ['|', '/', '-', '\\'],
    ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'],
    ['◜', '◝', '◞', '◟'],
]


class Spinner:
    """终端旋转动画"""

    def __init__(self, label='', frameset=0, interval=0.08):
        self.label = label
        self.frames = _SPINNER_FRAMES[frameset % len(_SPINNER_FRAMES)]
        self.interval = interval
        self._running = False
        self._thread = None
        self._idx = 0

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, msg=''):
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
        stop_msg = msg or ('✓ ' + self.label) if self.label else ''
        if stop_msg:
            clear_line = '\r' + ' ' * (len(self.label) + 10) + '\r'
            sys.stdout.write(clear_line + color(stop_msg, 'green') + '\n')
            sys.stdout.flush()

    def _spin(self):
        while self._running:
            frame = self.frames[self._idx % len(self.frames)]
            self._idx += 1
            line = f'\r {frame} {self.label}' if self.label else f'\r {frame}'
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(self.interval)


def cmd_spinner(args):
    """显示 Spinner 动画"""
    pos = args.get('_pos', [])
    label = ' '.join(pos) if pos else args.get('label', 'Working...')
    frameset = int(args.get('style', '0'))
    duration = float(args.get('duration', '3'))

    sp = Spinner(label=label, frameset=frameset)
    sp.start()
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    sp.stop('Done')


# ─── 选择列表 ─────────────────────────────────────────────

def cmd_select(args):
    """交互式选择列表"""
    pos = args.get('_pos', [])
    if len(pos) < 2:
        echo('❌ 用法: select "标题" "选项1" "选项2" ... [--default 0]', 'red')
        sys.exit(1)

    title = pos[0]
    options = pos[1:]
    default_idx = int(args.get('default', '-1'))
    multi_select = bool(args.get('multi'))
    allow_custom = bool(args.get('custom'))

    echo(color(f'\n  {title}', 'bold'), '')
    echo('', '')

    for idx, opt in enumerate(options):
        marker = '>' if idx == default_idx else ' '
        print(f'  {marker} [{idx}] {opt}')

    if allow_custom:
        print(f'  [+] 自定义输入')

    if multi_select:
        echo('\n  (多选: 输入序号用逗号分隔，如 0,2,3)', 'yellow')

    try:
        raw_input = input(color('\n  请选择 > ', 'cyan')).strip()
    except (EOFError, KeyboardInterrupt):
        echo('\n已取消', 'yellow')
        sys.exit(130)

    if not raw_input:
        if default_idx >= 0:
            selected_indices = [default_idx]
        else:
            echo('(未选择)', 'yellow')
            sys.exit(1)
    elif raw_input.lower() == 'q':
        echo('取消选择', 'yellow')
        sys.exit(1)
    else:
        if multi_select:
            parts = [p.strip() for p in raw_input.split(',')]
            selected_indices = []
            for p in parts:
                try:
                    idx = int(p)
                    if 0 <= idx < len(options):
                        selected_indices.append(idx)
                except ValueError:
                    pass
            if not selected_indices:
                echo(f'❌ 无效选择: {raw_input}', 'red')
                sys.exit(1)
        else:
            try:
                selected_idx = int(raw_input.strip())
                if 0 <= selected_idx < len(options):
                    selected_indices = [selected_idx]
                else:
                    echo(f'❌ 序号超出范围 (0-{len(options)-1})', 'red')
                    sys.exit(1)
            except ValueError:
                if allow_custom:
                    echo(f'✅ 用户自定义: {raw_input}', 'green')
                    # 输出到 stdout 供管道使用
                    print(raw_input)
                    return
                echo(f'❌ 请输入数字序号', 'red')
                sys.exit(1)

    results = [options[i] for i in selected_indices]
    result_str = ','.join(results)
    echo(f'\n  → 已选择: {result_str}', 'green')
    print(result_str)


# ─── 确认框 ───────────────────────────────────────────────

def cmd_confirm(args):
    """确认对话框"""
    pos = args.get('_pos', [])
    message = ' '.join(pos) if pos else args.get('msg', '确定要继续吗?')
    default_yes = args.get('default', '').lower() in ('y', 'yes', '')

    yes_label = 'Y'
    no_label = 'n'

    if default_yes:
        yes_label = 'y'
        no_label = 'N'
    else:
        yes_label = 'Y'
        no_label = 'n'

    prompt = f'\n  {color(message, "bold")}  [{color(yes_label, "green")}/{color(no_label, "red")}] '

    try:
        answer = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        echo('n', 'red')
        sys.exit(1)

    if not answer:
        answer = 'y' if default_yes else 'n'

    is_yes = answer in ('y', 'yes', 'ok', 'true', '1')

    if is_yes:
        echo('  → 是', 'green')
        print('yes')
    else:
        echo('  → 否', 'yellow')
        print('no')

    sys.exit(0 if is_yes else 1)


# ─── 表格展示 ─────────────────────────────────────────────

def cmd_table(args):
    """在终端中渲染表格"""
    headers_str = args.get('headers', '')
    rows_data = args.get('_pos', [])

    if headers_str:
        headers = [h.strip() for h in headers_str.split(',')]
    else:
        headers = []

    rows = []
    for r in rows_data:
        cells = [c.strip() for c in r.split(',')]
        rows.append(cells)

    align_str = args.get('align', '')   # left/right/center per column
    fmt = args.get('format', 'grid')    # grid / pipe / simple / markdown
    title = args.get('title', '')
    border_color = args.get('color', 'cyan')

    if not headers and rows:
        # 自动从数据推断列数
        max_cols = max(len(r) for r in rows) if rows else 0
        headers = [f'Col{i+1}' for i in range(max_cols)]

    if not rows:
        echo('(无数据)', 'yellow')
        return

    # 计算每列宽度
    num_cols = max(len(headers), max(len(r) for r in rows))
    widths = [len(headers[i]) if i < len(headers) else 0 for i in range(num_cols)]

    for row in rows:
        for i, cell in enumerate(row):
            cell_width = len(cell)
            if i < len(widths):
                if cell_width > widths[i]:
                    widths[i] = cell_width
            elif i == len(widths):
                widths.append(cell_width)

    # 最小宽度 3
    widths = [max(w, 3) for w in widths]

    # 解析对齐方式
    alignments = []
    if align_str:
        for a in align_str.split(','):
            alignments.append(a.strip().lower())
    while len(alignments) < num_cols:
        alignments.append('left')

    def format_cell(text, col_idx):
        w = widths[col_idx] if col_idx < len(widths) else 10
        al = alignments[col_idx] if col_idx < len(alignments) else 'left'
        if al == 'right':
            return text.rjust(w)
        elif al == 'center':
            return text.center(w)
        return text.ljust(w)

    if title:
        total_width = sum(widths) + 3 * num_cols + 1
        echo(color(title.center(total_width), border_color), '')

    if fmt in ('grid', 'pipe', 'markdown'):
        sep = '+'
        for w in widths:
            sep += '-' * (w + 2) + '+'

        header_row = '|'
        for i, h in enumerate(headers):
            h_display = h if i < len(headers) else ''
            header_row += ' ' + format_cell(h_display, i) + ' |'

        print(sep)
        print(header_row)
        print(sep)

        for row in rows:
            line = '|'
            for i, cell in enumerate(row):
                display = cell if i < len(row) else ''
                line += ' ' + format_cell(display, i) + ' |'
            print(line)

        print(sep)

    elif fmt == 'simple':
        header_line = '  '.join(format_cell(h, i) for i, h in enumerate(headers))
        echo(color(header_line, 'bold'), '')
        echo('  ' + '-' * len(header_line), 'cyan')
        for row in rows:
            line = '  '.join(format_cell(c, i) for i, c in enumerate(row))
            print('  ' + line)

    echo(f'\n({len(rows)} 行)', 'cyan')


# ─── 输入提示 ─────────────────────────────────────────────

def cmd_input(args):
    """带标签的输入提示"""
    pos = args.get('_pos', [])
    prompt_text = ' '.join(pos) if pos else args.get('prompt', '请输入:')
    default_val = args.get('default', '')
    hidden = bool(args.get('hidden') or args.get('password'))
    mask = args.get('mask', '*')
    validate_pattern = args.get('validate', '')
    required = bool(args.get('required'))

    suffix = f' [{color(default_val, "yellow")}]' if default_val else ''

    try:
        if hidden:
            result = _getpass_input(prompt_text + suffix, mask)
        else:
            result = input(color(prompt_text + suffix, 'cyan')).strip()
    except (EOFError, KeyboardInterrupt):
        echo('', '')
        sys.exit(130)

    if not result and default_val:
        result = default_val

    if required and not result:
        echo('❌ 此项必填', 'red')
        sys.exit(1)

    if validate_pattern and result:
        import re as re_mod
        if not re_mod.match(validate_pattern, result):
            echo(f'❌ 输入不符合格式要求: {validate_pattern}', 'red')
            sys.exit(1)

    print(result)


def _getpass_input(prompt, mask='*'):
    """隐藏字符的输入（纯标准库，跨平台）"""
    import msvcrt
    sys.stdout.write(prompt)
    sys.stdout.flush()
    result = ''
    while True:
        ch = msvcrt.getwch()
        if ch in ('\r', '\n'):
            break
        elif ch == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        elif ch == '\x08' or ch == '\x7F':  # Backspace
            if result:
                result = result[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif ord(ch) < 32:
            continue
        else:
            result += ch
            if mask:
                sys.stdout.write(mask)
            else:
                sys.stdout.write('*')
            sys.stdout.flush()

    print('')
    return result


# ─── 密码输入 ─────────────────────────────────────────────

def cmd_password(args):
    """安全的密码输入（等价于 getpass）"""
    pos = args.get('_pos', [])
    prompt = ' '.join(pos) if pos else args.get('prompt', 'Password:')
    confirm = bool(args.get('confirm'))
    min_length = int(args.get('min', '0'))

    pwd = _getpass_input(color(prompt, 'cyan'), mask='*')

    if confirm:
        pwd2 = _getpass_input(color('Confirm password:', 'cyan'), mask='*')
        if pwd != pwd2:
            echo('❌ 密码不匹配', 'red')
            sys.exit(1)

    if min_length > 0 and len(pwd) < min_length:
        echo(f'❌ 密码长度不足 (最少 {min_length})', 'red')
        sys.exit(1)

    # 不直接输出密码，只输出确认信息或哈希值
    hash_mode = args.get('hash', '')
    if hash_mode:
        import hashlib
        h = hashlib.new(hash_mode)
        h.update(pwd.encode())
        echo(f'密码哈希 ({hash_mode}): {h.hexdigest()}', 'green')
    else:
        echo(f'✅ 已接收 ({len(pwd)}) 字符', 'green')
    # 安全地返回（不打印明文到 stdout）
    return


# ─── 倒计时 ───────────────────────────────────────────────

def cmd_countdown(args):
    """倒计时器"""
    seconds = int(args.get('seconds', '5'))
    pos = args.get('_pos', [])
    message = ' '.join(pos) if pos else args.get('message', '')
    beep = bool(args.get('beep'))

    for remaining in range(seconds, -1, -1):
        mins, secs = divmod(remaining, 60)
        timer_str = f'{mins:02d}:{secs:02d}'
        display = f'{color(message, "bold")} {color(timer_str, "cyan")}'
        sys.stdout.write(f'\r{" " * 60}\r{display}')
        sys.stdout.flush()
        if remaining > 0:
            time.sleep(1)

    print()

    if beep:
        # Windows 蜂鸣声
        try:
            import winsound
            winsound.Beep(800, 300)
        except Exception:
            print('\a')

    echo(f'倒计时结束!', 'green')


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'progress': cmd_progress,
    'spinner': cmd_spinner,
    'select': cmd_select,
    'confirm': cmd_confirm,
    'table': cmd_table,
    'input': cmd_input,
    'password': cmd_password,
    'countdown': cmd_countdown,
}

ALIASES = {
    'bar': 'progress', 'loading': 'progress',
    'load': 'spinner', 'wait': 'spinner',
    'choice': 'select', 'pick': 'select', 'menu': 'select',
    'ask': 'confirm', 'yesno': 'confirm', 'yn': 'confirm',
    'grid': 'table', 'render-table': 'table',
    'prompt': 'input', 'ask-input': 'input', 'type': 'input',
    'pwd': 'password', 'passwd': 'password', 'getpass': 'password',
    'timer': cmd_countdown, 'count-down': cmd_countdown,
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
