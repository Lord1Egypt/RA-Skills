"""扫描 macOS /Applications 发现可脚本化应用。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from clam.registry import registry

SCAN_DIRS = [
    Path("/Applications"),
    Path("/System/Applications"),
    Path("/System/Applications/Utilities"),
    Path("/System/Library/CoreServices"),  # Finder.app lives here
    Path.home() / "Applications",          # 用户自装应用
]


# Apps that have no .sdef but are known to support UI Scripting (menu clicks).
# Each entry: (bundle_name, app_id, display_name, process_name)
_KNOWN_UI_APPS: list[tuple[str, str, str, str]] = [
    ("Figma.app", "figma", "Figma", "Figma"),
    # 通信
    ("Telegram.app", "telegram", "Telegram", "Telegram"),
    ("WeChat.app", "wechat", "微信", "WeChat"),
    ("QQ.app", "qq", "QQ", "QQ"),
    ("DingTalk.app", "dingtalk", "钉钉", "DingTalk"),
    ("Lark.app", "lark", "飞书", "Miwork"),
    ("Discord.app", "discord", "Discord", "Discord"),
    ("Slack.app", "slack", "Slack", "Slack"),
    ("zoom.us.app", "zoom", "Zoom", "zoom.us"),
    # 开发 / 效率
    ("Visual Studio Code.app", "visual-studio-code", "VS Code", "Code"),
    ("Cursor.app", "cursor", "Cursor", "Cursor"),
    ("Notion.app", "notion", "Notion", "Notion"),
    ("Obsidian.app", "obsidian", "Obsidian", "Obsidian"),
    # 媒体
    ("Spotify.app", "spotify", "Spotify", "Spotify"),
    ("QQMusic.app", "qqmusic", "QQ音乐", "QQMusic"),
]


@dataclass
class AppInfo:
    name: str          # "Music"
    app_id: str        # "music"
    bundle_path: str   # "/System/Applications/Music.app"
    sdef_path: str     # ".../com.apple.Music.sdef" 或 "" (基础模式)
    installed: bool    # 查注册表
    basic_mode: bool = False   # 无 sdef，仅支持标准套件
    process_name: str = ""     # System Events 进程名（UI Scripting 用）


def _app_name_to_id(name: str) -> str:
    """将应用显示名转为 CLI 安全的 id。"""
    return name.lower().replace(" ", "-")


def scan_applications() -> list[AppInfo]:
    """扫描所有含 .sdef 文件的 .app 应用包，以及已知的 UI Scripting 应用。"""
    installed = registry.list_all()
    results: list[AppInfo] = []
    seen_ids: set[str] = set()

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue

        for app_bundle in sorted(scan_dir.iterdir()):
            if not app_bundle.name.endswith(".app") or not app_bundle.is_dir():
                continue

            resources = app_bundle / "Contents" / "Resources"

            sdef_files = list(resources.glob("*.sdef")) if resources.exists() else []

            # Fallback: search nested .app bundles for sdef (e.g. ChatGPT Atlas)
            if not sdef_files:
                try:
                    sdef_files = list(app_bundle.rglob("*.sdef"))[:1]
                except (PermissionError, OSError):
                    pass

            if not sdef_files:
                continue

            sdef_path = sdef_files[0]
            app_name = app_bundle.name.removesuffix(".app")
            app_id = _app_name_to_id(app_name)

            if app_id in seen_ids:
                continue
            seen_ids.add(app_id)

            results.append(AppInfo(
                name=app_name,
                app_id=app_id,
                bundle_path=str(app_bundle),
                sdef_path=str(sdef_path),
                installed=app_id in installed,
            ))

    # Append known UI Scripting apps (no .sdef) if installed
    for bundle_name, app_id, display_name, process in _KNOWN_UI_APPS:
        if app_id in seen_ids:
            continue
        for scan_dir in SCAN_DIRS:
            bundle_path = scan_dir / bundle_name
            if bundle_path.is_dir():
                seen_ids.add(app_id)
                results.append(AppInfo(
                    name=display_name,
                    app_id=app_id,
                    bundle_path=str(bundle_path),
                    sdef_path="",
                    installed=app_id in installed,
                    basic_mode=True,  # will be upgraded to UI mode at install time
                    process_name=process,
                ))
                break

    return results


def find_app(name_or_id: str) -> AppInfo | None:
    """按名称或 ID 查找应用（大小写不敏感，支持子串匹配）。"""
    needle = name_or_id.lower().strip()
    apps = scan_applications()

    # 精确匹配
    for app in apps:
        if app.app_id == needle or app.name.lower() == needle:
            return app

    # 子串匹配（如 "chrome" → "google-chrome"）
    matches = [a for a in apps if needle in a.app_id or needle in a.name.lower()]
    if len(matches) == 1:
        return matches[0]

    return None


def suggest_app(name_or_id: str) -> list[str]:
    """返回与输入相近的 app_id 列表，用于 "Did you mean?" 提示。"""
    needle = name_or_id.lower().strip()
    apps = scan_applications()
    return [a.app_id for a in apps if needle in a.app_id or needle in a.name.lower()]


# 常见中文名 → 英文 bundle 名映射
_CN_ALIASES: dict[str, list[str]] = {
    "qq音乐": ["qqmusic"],
    "钉钉": ["dingtalk"],
    "飞书": ["飞书", "lark", "feishu"],
    "微信": ["wechat"],
    "企业微信": ["wecom"],
    "网易云音乐": ["neteasemusic"],
    "酷狗音乐": ["kugou"],
    "百度网盘": ["baidunetdisk"],
    "腾讯会议": ["tencentmeeting", "wemeet"],
    "剪映": ["jianying"],
}


def _expand_aliases(name: str) -> list[str]:
    """将中文名扩展为可能的英文匹配名列表。"""
    lower = name.lower().strip()
    result = [lower]
    for cn, aliases in _CN_ALIASES.items():
        if cn in lower or lower in cn:
            result.extend(aliases)
    return result


def find_basic_app(name_or_id: str) -> AppInfo | None:
    """查找已安装但无 .sdef 的应用，返回基础模式 AppInfo。"""
    needles = _expand_aliases(name_or_id)
    installed = registry.list_all()
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for app_bundle in scan_dir.iterdir():
            if not app_bundle.name.endswith(".app") or not app_bundle.is_dir():
                continue
            app_name = app_bundle.name.removesuffix(".app")
            app_lower = app_name.lower()
            app_id = _app_name_to_id(app_name)
            if any(n in app_lower or n in app_id for n in needles):
                resources = app_bundle / "Contents" / "Resources"
                has_sdef = resources.exists() and list(resources.glob("*.sdef"))
                if not has_sdef:
                    return AppInfo(
                        name=app_name,
                        app_id=app_id,
                        bundle_path=str(app_bundle),
                        sdef_path="",
                        installed=app_id in installed,
                        basic_mode=True,
                    )
    return None
