#!/usr/bin/env python3
"""init_project.py — ctx-lockstep v2 项目初始化

v2 结构（收敛到项目内单目录，尊重个人隐私/仓库整洁）:
    <项目>/.ctx-lockstep/
    ├── PROJECT.md        # 唯一恢复入口（恢复信息+决策+索引 三合一）
    ├── checkpoints/      # 阶段快照
    └── commits.log       # git 项目: post-commit hook 自动写入；固化后清空

额外动作:
    - git 项目: 向 .git/hooks/post-commit 幂等追加 hook 块
    - 非 git 项目: 提示（不擅自 git init）

用法:
    python3 init_project.py '<json>'

JSON 参数:
    projects_root   必填（新项目模式: 项目父目录）
    project_name    新项目模式必填；与 existing_path 二选一
    existing_path   接管已有目录模式（优先于 projects_root/project_name）
    create_workspace_rule  默认 true，写 workspace 级 PROJECT_SYSTEM.md
    workspace_root         默认 ~/.openclaw/workspace
    project_rule_filename  默认 PROJECT_SYSTEM.md
    overwrite       默认 false
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOOK_MARK_BEGIN = '# >>> ctx-lockstep >>>'
HOOK_MARK_END = '# <<< ctx-lockstep <<<'
HOOK_BODY = '''{0}
{{
  _cl_root="$(git rev-parse --show-toplevel 2>/dev/null)" &&
  printf '{{"commit":"%s","date":"%s","subject":"%s"}}\\n' \\
    "$(git rev-parse --short HEAD)" \\
    "$(date '+%Y-%m-%d %H:%M')" \\
    "$(git log -1 --pretty=%s)" \\
    >> "$_cl_root/.ctx-lockstep/commits.log"
}} 2>/dev/null
{1}'''.format(HOOK_MARK_BEGIN, HOOK_MARK_END)


def expand(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def now_str() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def write_text(path: Path, content: str, overwrite: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False
    path.write_text(content, encoding='utf-8')
    return True


def read_template(base: Path, rel: str) -> str:
    return (base / 'templates' / rel).read_text(encoding='utf-8')


def install_git_hook(project_dir: Path) -> str:
    """幂等安装 post-commit hook；返回动作说明。"""
    git_dir = project_dir / '.git'
    if not git_dir.exists():
        return 'skipped: 非 git 项目（如需精确漂移追踪，建议 git init 后重跑）'
    hooks = git_dir / 'hooks'
    hooks.mkdir(exist_ok=True)
    hook_path = hooks / 'post-commit'
    block = HOOK_BODY
    if hook_path.exists():
        content = hook_path.read_text(encoding='utf-8', errors='replace')
        if HOOK_MARK_BEGIN in content:
            return 'skipped: hook 已安装'
        # 追加到已有 hook 末尾，不覆盖用户自己的逻辑
        hook_path.write_text(content.rstrip() + '\n\n' + block + '\n', encoding='utf-8')
        action = 'appended to existing post-commit hook'
    else:
        hook_path.write_text('#!/bin/sh\n\n' + block + '\n', encoding='utf-8')
        action = 'created post-commit hook'
    try:
        hook_path.chmod(hook_path.stat().st_mode | 0o111)
    except OSError:
        pass
    return action


def main():
    if len(sys.argv) != 2:
        print(json.dumps({'ok': False, 'error': 'Usage: init_project.py <json-args>'}))
        sys.exit(1)
    try:
        args = json.loads(sys.argv[1])
    except Exception as e:
        print(json.dumps({'ok': False, 'error': f'Invalid JSON: {e}'}, ensure_ascii=False))
        sys.exit(1)

    existing_path = args.get('existing_path')
    projects_root = args.get('projects_root')
    project_name = args.get('project_name')
    create_workspace_rule = bool(args.get('create_workspace_rule', True))
    workspace_root = expand(args.get('workspace_root', '~/.openclaw/workspace'))
    project_rule_filename = args.get('project_rule_filename', 'PROJECT_SYSTEM.md')
    overwrite = bool(args.get('overwrite', False))

    if existing_path:
        project_dir = expand(existing_path)
        if not project_dir.is_dir():
            print(json.dumps({'ok': False, 'error': f'existing_path not found: {project_dir}'},
                             ensure_ascii=False))
            sys.exit(1)
        mode = 'adopt'
    else:
        if not projects_root or not project_name:
            print(json.dumps({'ok': False,
                              'error': 'projects_root and project_name (or existing_path) required'},
                             ensure_ascii=False))
            sys.exit(1)
        project_dir = expand(projects_root) / project_name
        mode = 'new'

    base_dir = Path(__file__).resolve().parent.parent
    ts = now_str()

    created, skipped = [], []

    # workspace 级规则文件（接管已有项目且非强制时默认不覆盖已有规则）
    if create_workspace_rule:
        system_path = workspace_root / project_rule_filename
        content = read_template(base_dir, 'PROJECT_SYSTEM.md').replace(
            '`<在初始化时填写>`', f'`{project_dir.parent}`')
        if write_text(system_path, content, overwrite=overwrite):
            created.append(str(system_path))
        else:
            skipped.append(str(system_path))

    # v2 单目录结构
    lockstep_dir = project_dir / '.ctx-lockstep'
    (lockstep_dir / 'checkpoints').mkdir(parents=True, exist_ok=True)

    posix_path = str(project_dir)
    try:
        import getpass
        win_path = project_dir.as_posix().replace(
            f'/mnt/{posix_path.split("/")[2].lower()}',
            f'{posix_path.split("/")[2].upper()}:') if posix_path.startswith('/mnt/') else ''
    except (IndexError, AttributeError):
        win_path = ''
    if not win_path:
        win_path = ''  # 无法推导时留空，由调用方补

    project_md = read_template(base_dir, 'PROJECT.md').replace('<项目名称>', project_dir.name)
    project_md = project_md.replace('<POSIX路径>', posix_path)
    project_md = project_md.replace('<WINDOWS路径>', win_path or '待填写')
    project_md = project_md.replace('<初始化时间>', ts)
    # 默认无仓库；git 项目接管后可手动补
    project_md = project_md.replace('<git URL 或"无（非 git 项目）">', '待填写')
    target = lockstep_dir / 'PROJECT.md'
    if write_text(target, project_md, overwrite=overwrite):
        created.append(str(target))
    else:
        skipped.append(str(target))

    ck_readme = lockstep_dir / 'checkpoints' / 'README.md'
    if write_text(ck_readme, read_template(base_dir, 'checkpoints/README.md'), overwrite=overwrite):
        created.append(str(ck_readme))
    else:
        skipped.append(str(ck_readme))

    # 空 commits.log（git 与非 git 都建，统一路径）
    log = lockstep_dir / 'commits.log'
    if not log.exists():
        log.touch()
        created.append(str(log))

    # git hook
    hook_action = install_git_hook(project_dir)

    # 非 git 项目提示
    git_hint = ''
    if not (project_dir / '.git').exists():
        git_hint = ('此项目不是 git 仓库：漂移检测将走 mtime 扫描（近似值）。'
                    '如追求精确，建议 git init 后重跑本脚本安装 hook（不会动你的文件）。')

    print(json.dumps({
        'ok': True,
        'mode': mode,
        'project_dir': str(project_dir),
        'structure': 'v2 (single .ctx-lockstep/ directory)',
        'created': created,
        'skipped': skipped,
        'git_hook': hook_action,
        'git_hint': git_hint,
        'next': [
            f'Edit {target} to fill 主线/断点/决策 (remove HTML meta comment placeholder only after first checkpoint).',
            'Run scripts/check_drift.py <project> on project enter/resume.',
            'Checkpoint (固化) updates PROJECT.md meta last_checkpoint + checkpoints/ snapshot + truncates commits.log.'
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
