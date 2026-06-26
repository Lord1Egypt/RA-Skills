#!/usr/bin/env python3
"""
git_advanced.py — Git 高级操作工具

功能：
  - stash:      暂存/恢复/列出/丢弃工作区修改
  - blame:      逐行查看文件修改历史（谁在何时改了哪一行）
  - diff:       对比差异（提交间、暂存区 vs 工作区、分支间）
  - cherry-pick: 将指定提交的改动移植到当前分支
  - rebase:     变基操作（交互式变基摘要）
  - conflicts:  查看和解决合并冲突状态
  - log-graph:  图形化提交历史（ASCII 树形图）
  - hooks:      管理 Git hooks（列表/启用/禁用）

纯标准库实现，依赖系统 git 命令行。

用法:
  python git_advanced.py stash save "临时保存"
  python git_advanced.py blame src/main.py
  python git_advanced.py diff HEAD~3 HEAD --stat
  python git_advanced.py cherry-pick abc1234
  python git_advanced.py log-graph -n 20
  python git_advanced.py conflicts list
"""

import argparse
import sys
import os
import subprocess
import json
from datetime import datetime, timezone


def _run_git(*args, check=False):
    """执行 git 命令，返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            ['git'] + list(args),
            capture_output=True,
            text=True,
            timeout=60,
        )
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, 'git', result.stderr)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        print("[!] 未找到 git 命令，请确认已安装 Git")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("[!] 命令执行超时")
        return -1, "", "timeout"


def _is_git_repo():
    """检查当前目录是否是 git 仓库"""
    rc, out, err = _run_git('rev-parse', '--is-inside-work-tree')
    return rc == 0 and out == 'true'


def cmd_stash(args):
    """Git Stash 操作"""
    action = args.action or 'list'
    message = getattr(args, 'message', None) or ''
    index = getattr(args, 'index', None)

    if action == 'save':
        if not message:
            message = f"WIP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        git_args = ['stash', 'push', '-m', message]
        if args.include_untracked:
            git_args.append('-u')
        rc, out, err = _run_git(*git_args)
        if rc == 0:
            # Extract stash ref
            for line in out.split('\n'):
                if 'Saved' in line:
                    print(f"[✓] {line}")
                    break
            else:
                    print(f"[✓] 已暂存: {message}")
        else:
            print(f"[!] 暂存失败: {err}")

    elif action == 'list':
        rc, out, err = _run_git('stash', 'list')
        if not out.strip():
            print("[*] 暂存列表为空")
            return
        print("=== Git Stash 列表 ===")
        for i, line in enumerate(out.split('\n'), 1):
            print(f"  {i:3d}. {line}")

    elif action == 'show':
        target = index or 'stash@{0}'
        rc, out, err = _run_git('stash', 'show', '-p', target)
        print(f"=== Stash: {target} ===\n{out or '(无输出)'}")

    elif action == 'pop':
        target = index or 'stash@{0}'
        rc, out, err = _run_git('stash', 'pop', target)
        if rc == 0:
            print(f"[✓] 已恢复并删除: {target}")
        else:
            print(f"[!] 恢复失败: {err}")

    elif action == 'drop':
        target = index or 'stash@{0}'
        rc, out, err = _run_git('stash', 'drop', target)
        if rc == 0:
            print(f"[✓] 已丢弃: {target}")
        else:
            print(f"[!] 丢弃失败: {err}")

    elif action == 'clear':
        rc, out, err = _run_git('stash', 'clear')
        if rc == 0:
            print("[✓] 所有暂存已清除")
        else:
            print(f"[!] 清除失败: {err}")


def cmd_blame(args):
    """逐行查看文件修改历史"""
    filepath = args.file
    start_line = args.start or 1
    end_line = args.end or 0

    if not os.path.exists(filepath):
        print(f"[!] 文件不存在: {filepath}")
        return

    git_args = ['blame', '--porcelain']
    if args.revision:
        git_args.extend([args.revision])
    if start_line > 1:
        git_args.extend(['-L', f'{start_line},'])
    if end_line > start_line:
        # Fix the range in git_args
        new_args = [a for a in git_args if a != '-L' and not a.startswith(f'{start_line},')]
        new_args.extend(['-L', f'{start_line},{end_line}'])
        git_args = new_args
    git_args.append('--')
    git_args.append(filepath)

    rc, out, err = _run_git(*git_args)

    if rc != 0:
        print(f"[!] blame 失败: {err}")
        return

    print(f"=== Blame: {filepath}{' @ ' + args.revision if args.revision else ''} ===\n")

    # Parse porcelain output
    lines_info = []
    current = {}
    content_lines = []

    for line in out.split('\n'):
        if line.startswith('author '):
            current['author'] = line[7:]
        elif line.startswith('author-mail '):
            current['mail'] = line[12:]
        elif line.startswith('author-time '):
            ts = int(line[12:])
            current['time'] = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        elif line.startswith('summary '):
            current['summary'] = line[8:60]
        elif line.startswith('\t'):
            current['content'] = line[1:][:80]
            lines_info.append(dict(current))
            content_lines.append(current.get('content', ''))
            current = {}

    # Display with formatting
    max_author_len = max((len(li.get('author', '')) for li in lines_info), default=10)
    max_author_len = min(max_author_len, 16)

    for i, info in enumerate(lines_info, start=start_line):
        author = info.get('author', '?')[:max_author_len]
        time_str = info.get('time', '')
        summary = info.get('summary', '') or ''
        content = info.get('content', '')
        print(f"  {i:5d} │ {author:{max_author_len}s} │ {time_str} │ {content}")


def cmd_diff(args):
    """对比差异"""
    target1 = args.target1 or 'HEAD'
    target2 = args.target2 or ''

    git_args = ['diff']

    if args.cached:
        git_args.append('--cached')

    if target2:
        git_args.extend([target1, target2])
    elif target1 and target1 != 'HEAD':
        git_args.append(target1)

    if args.stat:
        git_args.append('--stat')

    if args.name_only:
        git_args.append('--name-only')

    if args.files:
        git_args.append('--')
        git_args.extend(args.files)

    rc, out, err = _run_git(*git_args)

    if not out:
        print("[*] 无差异")
        return

    if args.stat or args.name_only:
        print(out)
    else:
        print(out)


def cmd_cherry_pick(args):
    """Cherry-pick 提交"""
    commits = args.commits

    if not commits:
        print("[!] 需要指定至少一个提交 hash")
        return

    git_args = ['cherry-pick']

    if args.no_commit:
        git_args.append('--no-commit')
    if args.edit:
        git_args.append('--edit')

    git_args.extend(commits)

    rc, out, err = _run_git(*git_args)

    if rc == 0:
        print(f"[✓] Cherry-pick 成功:")
        for c in commits:
            print(f"    {c}")
    elif rc == 1:
        print(f"[!] 存在冲突，需要解决后执行 git cherry-pick --continue")
        print(f"    或者 git cherry-pick --abort 放弃")
    else:
        print(f"[!] Cherry-pick 失败: {err}")


def cmd_rebase(args):
    """变基操作（信息展示与辅助）"""
    action = args.action or 'info'
    upstream = args.upstream or 'main'
    branch = args.branch or ''

    if action == 'info':
        # Show current branch status
        rc_branch, branch_out, _ = _run_git('branch', '--show-current')
        rc_upstream, upstream_out, _ = _run_git('merge-base', upstream, 'HEAD')
        rc_ahead, ahead_out, _ = _run_git('rev-list', '--count', f'{upstream_out or upstream}..HEAD')
        rc_behind, behind_out, _ = _run_git('rev-list', '--count', f'HEAD..{upstream}')

        current = branch_out or '(detached)'
        ahead = int(ahead_out) if ahead_out.isdigit() else 0
        behind = int(behind_out) if behind_out.isdigit() else 0

        print(f"=== Rebase 信息 ===")
        print(f"  当前分支:   {current}")
        print(f"  目标基线:   {upstream}")
        print(f"  领先:       {ahead} 个提交")
        print(f"  落后:       {behind} 个提交")

        if ahead > 0:
            print(f"\n  待变基提交:")
            rc_log, log_out, _ = _run_git('log', '--oneline', f'{upstream}..HEAD')
            for i, line in enumerate(log_out.split('\n')[::-1], 1):
                print(f"    {i}. {line}")

    elif action == 'start':
        git_args = ['rebase', upstream]
        if branch:
            git_args.extend([branch])
        if args.interactive:
            git_args.insert(1, '-i')
        rc, out, err = _run_git(*git_args)
        if rc == 0:
            print("[✓] 变基完成")
        elif rc == 1:
            print("[!] 变基中存在冲突，请解决后 git rebase --continue")
        else:
            print(f"[!] 变基失败: {err}")

    elif action == 'abort':
        rc, _, _ = _run_git('rebase', '--abort')
        print("[✓] 变基已中止")

    elif action == 'continue':
        rc, _, _ = _run_git('rebase', '--continue')
        print("[✓] 变基继续")


def cmd_conflicts(args):
    """合并冲突管理"""
    action = args.action or 'list'

    if action == 'list':
        # Find conflicted files
        rc, out, _ = _run_git('diff', '--name-only', '--diff-filter=U')
        if not out.strip():
            print("[*] 无冲突文件")
            return

        files = out.strip().split('\n')
        print(f"=== 冲突文件 ({len(files)}) ===\n")

        for f in files:
            rc_cnt, cnt_out, _ = _run_git('diff', '--check', '--', f)
            conflict_lines = len([l for l in cnt_out.split('\n') if l.strip()])
            print(f"  ⚠️  {f} ({conflict_lines} 处冲突)")

    elif action == 'ours':
        for f in args.files:
            _run_git('checkout', '--ours', '--', f)
            _run_git('add', '--', f)
            print(f"[✓] 已采用 ours 版本: {f}")

    elif action == 'theirs':
        for f in args.files:
            _run_git('checkout', '--theirs', '--', f)
            _run_git('add', '--', f)
            print(f"[✓] 已采用 theirs 版本: {f}")

    elif action == 'summary':
        # Show conflict context
        rc, out, _ = _run_git('diff', '--diff-filter=U', '--', *args.files)
        if out:
            print(out)
        else:
            print("[*] 无冲突详情")


def cmd_log_graph(args):
    """图形化提交历史"""
    count = args.count or 15
    branch = args.branch or '--all'
    since = args.since or ''
    until = args.until or ''
    author = args.author or ''
    grep = args.grep or ''

    git_args = [
        'log',
        '--graph',
        '--pretty=format:│%h │%an │%ar │%s%d',
        '--abbrev-commit',
        f'-{count}',
    ]

    if branch != '--all':
        git_args.append(branch)
    else:
        git_args.append('--all')

    if since:
        git_args.append(f'--since={since}')
    if until:
        git_args.append(f'--until={until}')
    if author:
        git_args.append(f'--author={author}')
    if grep:
        git_args.append(f'--grep={grep}')

    rc, out, err = _run_git(*git_args)

    if not out:
        print("[*] 无匹配的提交记录")
        return

    print(f"=== Git Log Graph ({count} 条) ===\n")
    print(out)


def cmd_hooks(args):
    """管理 Git Hooks"""
    action = args.action or 'list'
    hook_type = args.type or ''
    hook_dir = '.git/hooks'

    if not os.path.isdir(hook_dir):
        print("[!] 非 git 仓库或 hooks 目录不存在")
        return

    known_hooks = [
        'applypatch-msg', 'pre-applypatch', 'post-applypatch',
        'pre-commit', 'prepare-commit-msg', 'commit-msg',
        'post-commit', 'pre-rebase', 'post-checkout',
        'post-merge', 'pre-push', 'pre-receive',
        'update', 'post-receive', 'post-update',
        'push-to-checkout', 'pre-auto-gc', 'post-rewrite',
    ]

    if action == 'list':
        print("=== Git Hooks 状态 ===\n")
        for hook in sorted(known_hooks):
            path = os.path.join(hook_dir, hook)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                executable = os.access(path, os.X_OK)
                status = "🟢 可执行" if executable else "🟡 存在(无权限)"
                print(f"  {status:16s} {hook:>22s}  ({size} bytes)")
            else:
                print(f"  ⬜ 未配置          {hook:>22s}")

    elif action == 'enable':
        if not hook_type:
            print("[!] 请指定 hook 类型 (--type pre-commit 等)")
            return
        path = os.path.join(hook_dir, hook_type)
        if not os.path.isfile(path):
            print(f"[!] Hook 不存在: {hook_type}")
            return
        os.chmod(path, 0o755)
        print(f"[✓] 已启用: {hook_type}")

    elif action == 'disable':
        if not hook_type:
            print("[!] 请指定 hook 类型")
            return
        path = os.path.join(hook_dir, hook_type)
        if not os.path.isfile(path):
            print(f"[!] Hook 不存在: {hook_type}")
            return
        os.chmod(path, 0o644)
        print(f"[✓] 已禁用: {hook_type}")

    elif action == 'show':
        if not hook_type:
            print("[!] 请指定 hook 类型")
            return
        path = os.path.join(hook_dir, hook_type)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                print(f.read())
        else:
            print(f"[!] Hook 不存在: {hook_type}")


# ─── 命令注册 ──────────────────────────────────────────────
COMMANDS = {
    'stash':      cmd_stash,
    'blame':      cmd_blame,
    'diff':       cmd_diff,
    'cherry-pick': cmd_cherry_pick,
    'rebase':     cmd_rebase,
    'conflicts':  cmd_conflicts,
    'log-graph':  cmd_log_graph,
    'hooks':      cmd_hooks,
}

ALIASES = {
    'st':         'stash',
    'save':       'stash',
    'bl':         'blame',
    'cp':         'cherry-pick',
    'rb':         'rebase',
    'conflict':   'conflicts',
    'log':        'log-graph',
    'graph':      'log-graph',
    'hook':       'hooks',
}


def main():
    parser = argparse.ArgumentParser(
        prog='git_advanced',
        description='Git 高级操作工具',
        epilog='示例:\n'
              '  %(prog)s stash save "WIP"\n'
              '  %(prog)s blame src/main.py\n'
              '  %(prog)s diff main..feature --stat\n'
              '  %(prog)s cherry-pick abc123\n'
              '  %(prog)s log-graph -n 20\n'
              '  %(prog)s conflicts list\n'
              '  %(prog)s hooks list',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('command', nargs='?', help='子命令: ' + ', '.join(COMMANDS))
    parser.add_argument('rest', nargs=argparse.REMAINDER, help='命令参数')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n可用子命令:", ', '.join(COMMANDS))
        print(f"共 {len(COMMANDS)} 个命令 | 别名数: {len(ALIASES)}")
        sys.exit(0)

    # Resolve alias
    cmd_name = ALIASES.get(args.command, args.command)

    if cmd_name not in COMMANDS:
        print(f"[!] 未知命令: {args.command}")
        print(f"    可用: {', '.join(COMMANDS)}")
        sys.exit(1)

    sub_parser = argparse.ArgumentParser(prog=f'{parser.prog} {cmd_name}', add_help=False)

    if cmd_name == 'stash':
        sub_parser.add_argument('action', nargs='?', default='list',
                                choices=['save', 'list', 'show', 'pop', 'drop', 'clear'])
        sub_parser.add_argument('message', nargs='?', default='', help='暂存消息 (save 时)')
        sub_parser.add_argument('-i', '--index', default=None, help='暂存索引 (show/pop/drop)')
        sub_parser.add_argument('-u', '--include-untracked', action='store_true', help='包含未跟踪文件')

    elif cmd_name == 'blame':
        sub_parser.add_argument('file', help='目标文件')
        sub_parser.add_argument('-r', '--revision', default='', help='指定版本')
        sub_parser.add_argument('-s', '--start', type=int, default=1, help='起始行号')
        sub_parser.add_argument('-e', '--end', type=int, default=0, help='结束行号 (0=到末尾)')

    elif cmd_name == 'diff':
        sub_parser.add_argument('target1', nargs='?', default='HEAD', help='目标1 (默认: HEAD)')
        sub_parser.add_argument('target2', nargs='?', default='', help='目标2 (留空则对比工作区)')
        sub_parser.add_argument('--stat', action='store_true', help='仅显示统计')
        sub_parser.add_argument('--name-only', action='store_true', help='仅显示文件名')
        sub_parser.add_argument('--cached', action='store_true', help='暂存区 vs HEAD')
        sub_parser.add_argument('files', nargs='*', default=[], help='限定文件')

    elif cmd_name == 'cherry-pick':
        sub_parser.add_argument('commits', nargs='+', help='提交 hash (支持多个)')
        sub_parser.add_argument('--no-commit', action='store_true', help='不自动提交')
        sub_parser.add_argument('--edit', action='store_true', help='编辑提交信息')

    elif cmd_name == 'rebase':
        sub_parser.add_argument('action', nargs='?', default='info',
                                choices=['info', 'start', 'abort', 'continue'])
        sub_parser.add_argument('upstream', nargs='?', default='main', help='上游分支')
        sub_parser.add_argument('branch', nargs='?', default='')
        sub_parser.add_argument('-i', '--interactive', action='store_true', help='交互式变基')

    elif cmd_name == 'conflicts':
        sub_parser.add_argument('action', nargs='?', default='list',
                                choices=['list', 'ours', 'theirs', 'summary'])
        sub_parser.add_argument('files', nargs='*', default=[], help='目标文件')

    elif cmd_name == 'log-graph':
        sub_parser.add_argument('-n', '--count', type=int, default=15, help='显示条数')
        sub_parser.add_argument('-b', '--branch', default='--all', help='分支 (默认: --all)')
        sub_parser.add_argument('--since', default='', help='起始日期')
        sub_parser.add_argument('--until', default='', help='截止日期')
        sub_parser.add_argument('--author', default='', help='作者过滤')
        sub_parser.add_argument('--grep', default='', help='消息过滤')

    elif cmd_name == 'hooks':
        sub_parser.add_argument('action', nargs='?', default='list',
                                choices=['list', 'enable', 'disable', 'show'])
        sub_parser.add_argument('-t', '--type', default='', help='Hook 类型')

    sub_args = sub_parser.parse_args(args.rest)

    # Check git repo for commands that need it
    non_repo_commands = {'hooks'}  # hooks can work outside repo to show available types
    if cmd_name not in non_repo_commands and not _is_git_repo():
        print("[!] 当前目录不是 Git 仓库")
        sys.exit(1)

    try:
        COMMANDS[cmd_name](sub_args)
    except KeyboardInterrupt:
        print("\n[!] 操作已取消")
        sys.exit(130)
    except Exception as e:
        print(f"[!] 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
