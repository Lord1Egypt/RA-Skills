#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_THEME_DIR = SKILL_ROOT / 'assets' / 'theme'
DEFAULT_DIST_CANDIDATES = (
    Path.home() / '.npm-global/lib/node_modules/openclaw/dist/control-ui',
    Path('/opt/homebrew/lib/node_modules/openclaw/dist/control-ui'),
    Path('/usr/local/lib/node_modules/openclaw/dist/control-ui'),
    Path('/usr/lib/node_modules/openclaw/dist/control-ui'),
)
TARGET_THEME_DIR_REL = Path('customizations/openclaw-control-ui')
TARGET_APPLY_SCRIPT_REL = Path('scripts/apply_cyberpunk_theme.py')
STYLE_ID = 'openclaw-workspace-theme'
SCRIPT_ID = 'openclaw-workspace-theme-script'
LEGACY_STYLE_IDS = ['openclaw-custom-theme']
LEGACY_SCRIPT_IDS = ['openclaw-custom-theme-script']
DEFAULT_ASSISTANT_NAMEPLATE = '菠萝包 // BOLO BAO'
HELPER_NAMEPLATE = '消息助手 helper'

THEME_ASSET_NAMES = (
    'bao-dream.gif',
    'chat-bg-cyberpunk.jpg',
    'avatar1.png',
    'avatar2.png',
    'header.png',
    'history-avatar.png',
)
OBSOLETE_THEME_ASSET_NAMES = (
    'tool-avatar.gif',
    'pineapple-bun-breathe.gif',
)
ENCODED_THEME_ASSET_TARGETS = {
    'bao-dream.gif.txt': Path('assets/bao-dream.gif'),
    'chat-bg-cyberpunk.jpg.txt': Path('assets/chat-bg-cyberpunk.jpg'),
    'avatar1.png.txt': Path('assets/avatar1.png'),
    'avatar2.png.txt': Path('assets/avatar2.png'),
    'header.png.txt': Path('assets/header.png'),
    'history-avatar.png.txt': Path('assets/history-avatar.png'),
    'dreaming-bg.png.txt': Path('dreaming-bg.png'),
}
SLOT_TARGETS = {
    'assistant_avatar': Path('assets/avatar2.png'),
    'tool_avatar': Path('assets/avatar1.png'),
    'help_avatar': Path('assets/history-avatar.png'),
    'user_avatar': Path('assets/header.png'),
    'chat_background': Path('assets/chat-bg-cyberpunk.jpg'),
    'dream_avatar': Path('assets/bao-dream.gif'),
    'dream_background': Path('dreaming-bg.png'),
}

CONFIG_KEY_ALIASES = {
    'workspace': ('workspace', 'workspacePath'),
    'dist_dir': ('dist_dir', 'distDir'),
    'assistant_avatar': ('assistant_avatar', 'assistantAvatar'),
    'tool_avatar': ('tool_avatar', 'toolAvatar'),
    'help_avatar': ('help_avatar', 'helpAvatar', 'history_avatar', 'historyAvatar', 'other_avatar', 'otherAvatar'),
    'user_avatar': ('user_avatar', 'userAvatar'),
    'chat_background': ('chat_background', 'chatBackground'),
    'dream_avatar': ('dream_avatar', 'dreamAvatar'),
    'dream_background': ('dream_background', 'dreamBackground'),
}


def detect_default_dist_dir() -> Path:
    env_value = os.environ.get('OPENCLAW_CONTROL_UI_DIST')
    if env_value:
        return Path(env_value).expanduser()

    for candidate in DEFAULT_DIST_CANDIDATES:
        if candidate.exists():
            return candidate

    try:
        npm_root = subprocess.run(
            ['npm', 'root', '-g'],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        npm_root = ''

    if npm_root:
        candidate = Path(npm_root) / 'openclaw' / 'dist' / 'control-ui'
        if candidate.exists():
            return candidate

    return DEFAULT_DIST_CANDIDATES[0]


DEFAULT_DIST_DIR = detect_default_dist_dir()


def normalize_name_fragment(value: str | None) -> str:
    if not value:
        return ''
    return re.sub(r'\s+', ' ', value.strip().strip('`\'"“”‘’')).strip()


def css_string(value: str) -> str:
    return value.replace('\\', '\\\\').replace('"', '\\"')


def build_nameplate(primary: str | None, alias: str | None = None) -> str | None:
    normalized_primary = normalize_name_fragment(primary)
    normalized_alias = normalize_name_fragment(alias)
    if normalized_alias:
        normalized_alias = normalize_name_fragment(re.split(r'\s*/\s*', normalized_alias, maxsplit=1)[0])
    if normalized_primary and normalized_alias:
        return f'{normalized_primary} // {normalized_alias.upper()}'
    return normalized_primary or None


def parse_identity_nameplate(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8')
    match = re.search(r'^\s*-\s*\*\*Name\*\*:\s*(.+?)\s*$', text, flags=re.M)
    if not match:
        return None
    raw = match.group(1)
    parts = re.match(r'(?P<primary>[^()]+?)(?:\s*\((?P<alias>[^)]+)\))?\s*$', raw)
    if parts:
        return build_nameplate(parts.group('primary'), parts.group('alias'))
    return build_nameplate(raw)


def parse_soul_nameplate(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8')
    match = re.search(r'You are\s+["“](.+?)["”](?:\s*\(([^)]+)\))?', text)
    if not match:
        return None
    return build_nameplate(match.group(1), match.group(2))


def resolve_assistant_nameplate(workspace: Path) -> str:
    return (
        parse_identity_nameplate(workspace / 'IDENTITY.md')
        or parse_soul_nameplate(workspace / 'SOUL.md')
        or DEFAULT_ASSISTANT_NAMEPLATE
    )


def build_runtime_theme_css(css_source: str, workspace: Path) -> str:
    assistant_nameplate = resolve_assistant_nameplate(workspace)
    vars_block = (
        ':root {\n'
        f'  --oc-assistant-nameplate: "{css_string(assistant_nameplate)}";\n'
        f'  --oc-helper-nameplate: "{css_string(HELPER_NAMEPLATE)}";\n'
        '}\n\n'
    )
    return vars_block + css_source


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Install or re-apply the Cyberpunk OpenClaw theme with optional asset overrides.'
    )
    parser.add_argument('--workspace', type=Path, default=Path.cwd(), help='Target OpenClaw workspace')
    parser.add_argument(
        '--dist-dir',
        type=Path,
        default=Path(os.environ.get('OPENCLAW_CONTROL_UI_DIST', str(DEFAULT_DIST_DIR))),
        help='control-ui dist directory',
    )
    parser.add_argument('--assistant-avatar', type=Path, help='Override main assistant portrait')
    parser.add_argument('--tool-avatar', type=Path, help='Override tool portrait')
    parser.add_argument('--help-avatar', type=Path, help='Override help/history portrait')
    parser.add_argument('--user-avatar', type=Path, help='Override user portrait')
    parser.add_argument('--chat-background', type=Path, help='Override chat background image')
    parser.add_argument('--dream-avatar', type=Path, help='Override dream avatar image')
    parser.add_argument('--dream-background', type=Path, help='Override dream background image')
    parser.add_argument('--from-config', type=Path, help='Load slot overrides from a JSON config file')
    parser.add_argument('--skip-apply', action='store_true', help='Install files but do not apply to dist')
    parser.add_argument('--apply-only', action='store_true', help='Only apply the already-installed theme')
    return parser.parse_args()


def resolve_workspace(path: Path) -> Path:
    return path.expanduser().resolve()


def load_config(path: Path | None) -> dict[str, object]:
    if path is None:
        return {}
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise SystemExit(f'config file not found: {resolved}')
    if not resolved.is_file():
        raise SystemExit(f'config path is not a file: {resolved}')
    data = json.loads(resolved.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise SystemExit(f'config root must be a JSON object: {resolved}')
    return data


def config_value(config: dict[str, object], *keys: str) -> object | None:
    for key in keys:
        if key in config:
            return config[key]
    return None


def merge_config_into_args(args: argparse.Namespace, config: dict[str, object]) -> None:
    if not config:
        return

    default_workspace = Path.cwd()
    default_dist_dir = Path(os.environ.get('OPENCLAW_CONTROL_UI_DIST', str(DEFAULT_DIST_DIR)))

    workspace_value = config_value(config, *CONFIG_KEY_ALIASES['workspace'])
    if args.workspace == default_workspace and isinstance(workspace_value, str):
        args.workspace = Path(workspace_value)

    dist_dir_value = config_value(config, *CONFIG_KEY_ALIASES['dist_dir'])
    if args.dist_dir == default_dist_dir and isinstance(dist_dir_value, str):
        args.dist_dir = Path(dist_dir_value)

    for attr in (
        'assistant_avatar',
        'tool_avatar',
        'help_avatar',
        'user_avatar',
        'chat_background',
        'dream_avatar',
        'dream_background',
    ):
        if getattr(args, attr) is not None:
            continue
        value = config_value(config, *CONFIG_KEY_ALIASES[attr])
        if isinstance(value, str) and value.strip():
            setattr(args, attr, Path(value))


def validate_override(path: Path | None, label: str) -> Path | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise SystemExit(f'{label} not found: {resolved}')
    if not resolved.is_file():
        raise SystemExit(f'{label} is not a file: {resolved}')
    return resolved


def resolve_slot_overrides(args: argparse.Namespace) -> dict[str, Path | None]:
    return {
        'assistant_avatar': validate_override(args.assistant_avatar, 'assistant avatar'),
        'tool_avatar': validate_override(args.tool_avatar, 'tool avatar'),
        'help_avatar': validate_override(args.help_avatar, 'help avatar'),
        'user_avatar': validate_override(args.user_avatar, 'user avatar'),
        'chat_background': validate_override(args.chat_background, 'chat background'),
        'dream_avatar': validate_override(args.dream_avatar, 'dream avatar'),
        'dream_background': validate_override(args.dream_background, 'dream background'),
    }


def backup_existing_theme(workspace: Path, theme_dir: Path, apply_script: Path) -> Path | None:
    if not theme_dir.exists() and not apply_script.exists():
        return None
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_root = workspace / 'backups' / f'cyberpunk-theme-{stamp}'
    if theme_dir.exists():
        shutil.copytree(theme_dir, backup_root / TARGET_THEME_DIR_REL.name)
    if apply_script.exists():
        (backup_root / 'scripts').mkdir(parents=True, exist_ok=True)
        shutil.copy2(apply_script, backup_root / 'scripts' / apply_script.name)
    return backup_root


def install_theme_sources(theme_dir: Path) -> None:
    theme_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DEFAULT_THEME_DIR, theme_dir, dirs_exist_ok=True)
    restore_encoded_theme_assets(theme_dir)


def restore_encoded_theme_assets(theme_dir: Path) -> list[Path]:
    encoded_dir = theme_dir / 'encoded-assets'
    if not encoded_dir.exists():
        return []

    restored: list[Path] = []
    for encoded_name, target_rel in ENCODED_THEME_ASSET_TARGETS.items():
        encoded_path = encoded_dir / encoded_name
        target = theme_dir / target_rel
        if target.exists() or not encoded_path.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(encoded_path.read_text(encoding='ascii')))
        restored.append(target)
    return restored


def apply_slot_overrides(theme_dir: Path, overrides: dict[str, Path | None]) -> list[str]:
    applied: list[str] = []
    for slot, source in overrides.items():
        if source is None:
            continue
        target = theme_dir / SLOT_TARGETS[slot]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        applied.append(f'{slot} <- {source}')
    return applied


def build_apply_wrapper() -> str:
    return '''#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
THEME_DIR = WORKSPACE / 'customizations' / 'openclaw-control-ui'
STYLE_ID = 'openclaw-workspace-theme'
SCRIPT_ID = 'openclaw-workspace-theme-script'
LEGACY_STYLE_IDS = ['openclaw-custom-theme']
LEGACY_SCRIPT_IDS = ['openclaw-custom-theme-script']
DEFAULT_ASSISTANT_NAMEPLATE = '菠萝包 // BOLO BAO'
HELPER_NAMEPLATE = '消息助手 helper'
THEME_ASSET_NAMES = (
    'bao-dream.gif',
    'chat-bg-cyberpunk.jpg',
    'avatar1.png',
    'avatar2.png',
    'header.png',
    'history-avatar.png',
)
OBSOLETE_THEME_ASSET_NAMES = (
    'tool-avatar.gif',
    'pineapple-bun-breathe.gif',
)
DIST_CANDIDATES = (
    Path.home() / '.npm-global/lib/node_modules/openclaw/dist/control-ui',
    Path('/opt/homebrew/lib/node_modules/openclaw/dist/control-ui'),
    Path('/usr/local/lib/node_modules/openclaw/dist/control-ui'),
    Path('/usr/lib/node_modules/openclaw/dist/control-ui'),
)


def css_string(value: str) -> str:
    return value.replace('\\\\', '\\\\\\\\').replace('"', '\\\\"')


def normalize_name_fragment(value: str | None) -> str:
    if not value:
        return ''
    return re.sub(r'\\s+', ' ', value.strip().strip('`\\'"“”‘’')).strip()


def build_nameplate(primary: str | None, alias: str | None = None) -> str | None:
    normalized_primary = normalize_name_fragment(primary)
    normalized_alias = normalize_name_fragment(alias)
    if normalized_alias:
        normalized_alias = normalize_name_fragment(re.split(r'\\s*/\\s*', normalized_alias, maxsplit=1)[0])
    if normalized_primary and normalized_alias:
        return f'{normalized_primary} // {normalized_alias.upper()}'
    return normalized_primary or None


def parse_identity_nameplate(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8')
    match = re.search(r'^\\s*-\\s*\\*\\*Name\\*\\*:\\s*(.+?)\\s*$', text, flags=re.M)
    if not match:
        return None
    raw = match.group(1)
    parts = re.match(r'(?P<primary>[^()]+?)(?:\\s*\\((?P<alias>[^)]+)\\))?\\s*$', raw)
    if parts:
        return build_nameplate(parts.group('primary'), parts.group('alias'))
    return build_nameplate(raw)


def parse_soul_nameplate(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8')
    match = re.search(r'You are\\s+["“](.+?)["”](?:\\s*\\(([^)]+)\\))?', text)
    if not match:
        return None
    return build_nameplate(match.group(1), match.group(2))


def resolve_assistant_nameplate() -> str:
    return (
        parse_identity_nameplate(WORKSPACE / 'IDENTITY.md')
        or parse_soul_nameplate(WORKSPACE / 'SOUL.md')
        or DEFAULT_ASSISTANT_NAMEPLATE
    )


def build_runtime_theme_css(css_source: str) -> str:
    assistant_nameplate = resolve_assistant_nameplate()
    vars_block = (
        ':root {\\n'
        f'  --oc-assistant-nameplate: "{css_string(assistant_nameplate)}";\\n'
        f'  --oc-helper-nameplate: "{css_string(HELPER_NAMEPLATE)}";\\n'
        '}\\n\\n'
    )
    return vars_block + css_source


def resolve_dist_dir() -> Path:
    env_value = os.environ.get('OPENCLAW_CONTROL_UI_DIST')
    if env_value:
        return Path(env_value).expanduser().resolve()
    for candidate in DIST_CANDIDATES:
        if candidate.exists():
            return candidate.resolve()
    try:
        npm_root = subprocess.run(
            ['npm', 'root', '-g'],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        npm_root = ''
    if npm_root:
        candidate = Path(npm_root) / 'openclaw' / 'dist' / 'control-ui'
        if candidate.exists():
            return candidate.resolve()
    checked = ', '.join(str(path) for path in DIST_CANDIDATES)
    raise SystemExit(
        'control-ui dist not found. Set OPENCLAW_CONTROL_UI_DIST to the live '
        f'dist/control-ui directory. Checked: {checked}'
    )


def backup_index(dist_dir: Path) -> Path:
    backup_dir = WORKSPACE / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_index_path = backup_dir / 'openclaw-control-ui-index.before-cyberpunk-theme.html'
    index_html = dist_dir / 'index.html'
    if not backup_index_path.exists():
        backup_index_path.write_text(index_html.read_text(encoding='utf-8'), encoding='utf-8')
    return backup_index_path


def ensure_inline_theme(dist_dir: Path) -> str:
    index_html = dist_dir / 'index.html'
    workspace_theme = THEME_DIR / 'control-ui-overrides.css'
    workspace_script = THEME_DIR / 'control-ui-overlay.js'

    html = index_html.read_text(encoding='utf-8')
    css = build_runtime_theme_css(workspace_theme.read_text(encoding='utf-8'))
    js = workspace_script.read_text(encoding='utf-8') if workspace_script.exists() else ''

    html = re.sub(
        r'\\n\\s*<link rel="stylesheet" href="\\./assets/control-ui-overrides\\.css(?:\\?v=[^"]+)?"\\s*/?>',
        '',
        html,
    )

    style_block = f'    <style id="{STYLE_ID}">\\n{css}\\n    </style>\\n'
    script_block = f'    <script id="{SCRIPT_ID}">\\n{js}\\n    </script>\\n' if js else ''

    style_ids = [STYLE_ID] + LEGACY_STYLE_IDS
    script_ids = [SCRIPT_ID] + LEGACY_SCRIPT_IDS
    style_pattern = r'\\s*<style[^>]*id="(?:' + '|'.join(map(re.escape, style_ids)) + r')"[^>]*>.*?</style>\\s*'
    script_pattern = r'\\s*<script[^>]*id="(?:' + '|'.join(map(re.escape, script_ids)) + r')"[^>]*>.*?</script>\\s*'

    html = re.sub(style_pattern, '\\n', html, flags=re.S)
    html = re.sub(script_pattern, '\\n', html, flags=re.S)

    if '</head>' not in html:
        raise RuntimeError(f'Could not find </head> in {index_html}')
    html = html.replace('</head>', style_block + '  </head>')

    if js:
        if '</body>' not in html:
            raise RuntimeError(f'Could not find </body> in {index_html}')
        html = html.replace('</body>', script_block + '</body>')

    index_html.write_text(html, encoding='utf-8')
    return 'updated-inline'


def copy_theme_assets(dist_dir: Path) -> list[str]:
    dist_assets = dist_dir / 'assets'
    dist_assets.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    asset_pairs = [
        (THEME_DIR / 'dreaming-bg.png', dist_assets / 'dreaming-bg.png'),
    ]
    asset_pairs.extend((THEME_DIR / 'assets' / name, dist_assets / name) for name in THEME_ASSET_NAMES)

    for src, dst in asset_pairs:
        if src.exists():
            shutil.copy2(src, dst)
            copied.append(f'{src.name} -> {dst.relative_to(dist_dir)}')
    return copied


def cleanup_obsolete_theme_assets(dist_dir: Path) -> list[str]:
    removed: list[str] = []
    for name in OBSOLETE_THEME_ASSET_NAMES:
        target = dist_dir / 'assets' / name
        if target.exists():
            target.unlink()
            removed.append(str(target.relative_to(dist_dir)))
    return removed


def apply_theme(dist_dir: Path) -> tuple[str, list[str], list[str], Path]:
    index_html = dist_dir / 'index.html'
    if not THEME_DIR.exists():
        raise SystemExit(f'installed theme dir not found: {THEME_DIR}')
    if not dist_dir.exists():
        raise SystemExit(f'control-ui dist not found: {dist_dir}')
    if not index_html.exists():
        raise SystemExit(f'control-ui index.html not found: {index_html}')
    backup_path = backup_index(dist_dir)
    inline_state = ensure_inline_theme(dist_dir)
    copied = copy_theme_assets(dist_dir)
    removed = cleanup_obsolete_theme_assets(dist_dir)
    return inline_state, copied, removed, backup_path


def main() -> int:
    dist_dir = resolve_dist_dir()
    inline_state, copied, removed, backup_path = apply_theme(dist_dir)
    print('Cyberpunk theme re-applied.')
    print(f'- workspace: {WORKSPACE}')
    print(f'- live dist: {dist_dir}')
    print(f'- backup index: {backup_path}')
    print(f'- inline mode: {inline_state}')
    if copied:
        print(f"- copied assets: {', '.join(copied)}")
    if removed:
        print(f"- removed obsolete assets: {', '.join(removed)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
'''


def write_apply_wrapper(workspace: Path) -> Path:
    target = workspace / TARGET_APPLY_SCRIPT_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_apply_wrapper(), encoding='utf-8')
    target.chmod(0o755)
    return target


def ensure_inline_theme(workspace: Path, dist_dir: Path) -> str:
    index_html = dist_dir / 'index.html'
    theme_dir = workspace / TARGET_THEME_DIR_REL
    workspace_theme = theme_dir / 'control-ui-overrides.css'
    workspace_script = theme_dir / 'control-ui-overlay.js'

    html = index_html.read_text(encoding='utf-8')
    css = build_runtime_theme_css(workspace_theme.read_text(encoding='utf-8'), workspace)
    js = workspace_script.read_text(encoding='utf-8') if workspace_script.exists() else ''

    html = re.sub(
        r'\n\s*<link rel="stylesheet" href="\./assets/control-ui-overrides\.css(?:\?v=[^"]+)?"\s*/?>',
        '',
        html,
    )

    style_block = f'    <style id="{STYLE_ID}">\n{css}\n    </style>\n'
    script_block = f'    <script id="{SCRIPT_ID}">\n{js}\n    </script>\n' if js else ''

    style_ids = [STYLE_ID] + LEGACY_STYLE_IDS
    script_ids = [SCRIPT_ID] + LEGACY_SCRIPT_IDS
    style_pattern = r'\s*<style[^>]*id="(?:' + '|'.join(map(re.escape, style_ids)) + r')"[^>]*>.*?</style>\s*'
    script_pattern = r'\s*<script[^>]*id="(?:' + '|'.join(map(re.escape, script_ids)) + r')"[^>]*>.*?</script>\s*'

    html = re.sub(style_pattern, '\n', html, flags=re.S)
    html = re.sub(script_pattern, '\n', html, flags=re.S)

    if '</head>' not in html:
        raise RuntimeError(f'Could not find </head> in {index_html}')
    html = html.replace('</head>', style_block + '  </head>')

    if js:
        if '</body>' not in html:
            raise RuntimeError(f'Could not find </body> in {index_html}')
        html = html.replace('</body>', script_block + '</body>')

    index_html.write_text(html, encoding='utf-8')
    return 'updated-inline'


def copy_theme_assets(workspace: Path, dist_dir: Path) -> list[str]:
    theme_dir = workspace / TARGET_THEME_DIR_REL
    dist_assets = dist_dir / 'assets'
    dist_assets.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    asset_pairs = [
        (theme_dir / 'dreaming-bg.png', dist_assets / 'dreaming-bg.png'),
    ]
    asset_pairs.extend((theme_dir / 'assets' / name, dist_assets / name) for name in THEME_ASSET_NAMES)

    for src, dst in asset_pairs:
        if src.exists():
            shutil.copy2(src, dst)
            copied.append(f'{src.name} -> {dst.relative_to(dist_dir)}')
    return copied


def cleanup_obsolete_theme_assets(dist_dir: Path) -> list[str]:
    removed: list[str] = []
    for name in OBSOLETE_THEME_ASSET_NAMES:
        target = dist_dir / 'assets' / name
        if target.exists():
            target.unlink()
            removed.append(str(target.relative_to(dist_dir)))
    return removed


def backup_index(workspace: Path, dist_dir: Path) -> Path:
    backup_dir = workspace / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_index = backup_dir / 'openclaw-control-ui-index.before-cyberpunk-theme.html'
    index_html = dist_dir / 'index.html'
    if not backup_index.exists():
        backup_index.write_text(index_html.read_text(encoding='utf-8'), encoding='utf-8')
    return backup_index


def validate_live_dist(dist_dir: Path, *, require_body: bool = False) -> None:
    index_html = dist_dir / 'index.html'
    if not dist_dir.exists():
        raise SystemExit(f'control-ui dist not found: {dist_dir}')
    if not index_html.exists():
        raise SystemExit(f'control-ui index.html not found: {index_html}')
    html = index_html.read_text(encoding='utf-8')
    if '</head>' not in html:
        raise SystemExit(f'control-ui index.html missing </head>: {index_html}')
    if require_body and '</body>' not in html:
        raise SystemExit(f'control-ui index.html missing </body>: {index_html}')


def apply_theme(workspace: Path, dist_dir: Path) -> tuple[str, list[str], list[str], Path]:
    validate_live_dist(dist_dir)
    backup_path = backup_index(workspace, dist_dir)
    inline_state = ensure_inline_theme(workspace, dist_dir)
    copied = copy_theme_assets(workspace, dist_dir)
    removed = cleanup_obsolete_theme_assets(dist_dir)
    return inline_state, copied, removed, backup_path


def main() -> int:
    args = parse_args()
    merge_config_into_args(args, load_config(args.from_config))
    workspace = resolve_workspace(args.workspace)
    dist_dir = args.dist_dir.expanduser().resolve()
    theme_dir = workspace / TARGET_THEME_DIR_REL
    apply_script = workspace / TARGET_APPLY_SCRIPT_REL

    if args.apply_only:
        inline_state, copied, removed, backup_path = apply_theme(workspace, dist_dir)
        print('Cyberpunk theme re-applied.')
        print(f'- workspace: {workspace}')
        print(f'- live dist: {dist_dir}')
        print(f'- backup index: {backup_path}')
        print(f'- inline mode: {inline_state}')
        if copied:
            print(f"- copied assets: {', '.join(copied)}")
        if removed:
            print(f"- removed obsolete assets: {', '.join(removed)}")
        return 0

    overrides = resolve_slot_overrides(args)
    if not args.skip_apply:
        validate_live_dist(
            dist_dir,
            require_body=(DEFAULT_THEME_DIR / 'control-ui-overlay.js').exists(),
        )

    backup_root = backup_existing_theme(workspace, theme_dir, apply_script)
    install_theme_sources(theme_dir)
    applied_overrides = apply_slot_overrides(theme_dir, overrides)
    apply_wrapper = write_apply_wrapper(workspace)

    print('Cyberpunk theme installed.')
    print(f'- workspace: {workspace}')
    print(f'- theme dir: {theme_dir}')
    print(f'- apply script: {apply_wrapper}')
    if backup_root:
        print(f'- backup: {backup_root}')
    if applied_overrides:
        print(f"- overrides: {', '.join(applied_overrides)}")

    if args.skip_apply:
        print('- apply skipped by flag')
        return 0

    inline_state, copied, removed, backup_path = apply_theme(workspace, dist_dir)
    print(f'- backup index: {backup_path}')
    print(f'- inline mode: {inline_state}')
    if copied:
        print(f"- copied assets: {', '.join(copied)}")
    if removed:
        print(f"- removed obsolete assets: {', '.join(removed)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
