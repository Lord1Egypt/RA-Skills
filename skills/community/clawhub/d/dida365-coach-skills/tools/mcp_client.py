"""处理滴答清单 MCP 检测、本地配置写入与设置文案。"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_SERVER_NAME = "dida365"
DEFAULT_MCP_URL = "https://mcp.dida365.com"


def _candidate_mcp_config_paths() -> List[Path]:
    override = os.environ.get("DIDA_COACH_MCP_CONFIG_PATH")
    if override:
        return [Path(override).expanduser()]

    home = Path.home()
    return [
        home / ".openclaw" / "openclaw.json",
        home / ".openclaw" / "workspace" / "openclaw.json",
        home / ".codex" / "mcp.json",
        home / ".claude" / "mcp.json",
    ]


def _load_mcp_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        return data
    return {}


def _save_mcp_config(path: Path, config: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def _find_server(config: Dict[str, Any], server_name: str) -> Optional[Dict[str, Any]]:
    for key in ("mcpServers", "servers"):
        server_map = config.get(key)
        if isinstance(server_map, dict) and isinstance(server_map.get(server_name), dict):
            return server_map[server_name]
    return None


def _extract_server_url(server: Dict[str, Any]) -> str:
    direct_url = server.get("url")
    if isinstance(direct_url, str) and direct_url:
        return direct_url

    transport = server.get("transport")
    if isinstance(transport, dict):
        transport_url = transport.get("url")
        if isinstance(transport_url, str):
            return transport_url

    return ""


def get_openclaw_config_path() -> Path:
    """返回 OpenClaw 首选配置文件路径。"""

    override = os.environ.get("DIDA_COACH_OPENCLAW_CONFIG_PATH")
    if override:
        return Path(override).expanduser()

    home = Path.home()
    primary = home / ".openclaw" / "openclaw.json"
    if primary.exists():
        return primary
    workspace = home / ".openclaw" / "workspace" / "openclaw.json"
    if workspace.exists():
        return workspace
    return primary


def build_setup_guide() -> str:
    """返回 MCP 未配置时的引导文案。"""

    return (
        "👋 欢迎使用 Dida Coach！\n\n"
        "检测到你还没有连接滴答清单。先按你当前使用的客户端选择最快路径：\n\n"
        "1. OpenClaw：优先自动把 dida365 写进 OpenClaw 的 MCP 配置，再刷新客户端并点一次 Connect。\n"
        "   推荐配置片段：\n"
        '   {"mcpServers":{"dida365":{"transport":{"type":"http","url":"https://mcp.dida365.com"}}}}\n'
        "2. ClawHub / 其他带连接按钮的客户端：直接点 dida365 的 Connect、Authorize、Sign in 或 Enable。\n"
        "3. Claude Desktop：Customize > Connectors > Add Connector > 填 URL > Connect。\n"
        "4. ChatGPT：设置 > 应用 > 高级设置 > 开发人员模式 > 创建应用 > 填 URL。\n"
        "5. Cursor / VS Code：在 MCP 设置页添加 dida365，然后点 connect。\n"
        "6. Claude Code：运行下面这条兜底命令，再在 Claude 会话里执行 `/mcp` 授权。\n\n"
        "所有客户端统一使用这组连接信息：\n\n"
        f"- 服务名：{DEFAULT_SERVER_NAME}\n"
        f"- 服务地址：{DEFAULT_MCP_URL}\n"
        "- 传输方式：HTTP 或 streamable_http\n"
        f"- Claude Code 兜底命令：claude mcp add --transport http {DEFAULT_SERVER_NAME} {DEFAULT_MCP_URL}\n\n"
        "如果你在 OpenClaw 里允许我改本地配置，我会优先帮你写入 dida365 的 MCP 配置，再引导你刷新客户端并点击 Connect 完成浏览器 OAuth。\n"
        "不要把 `/mcp` 当成 shell 命令直接执行；它只属于 Claude Code 会话内的 slash command。\n\n"
        "完成浏览器授权后，告诉我“已连接”，我会继续帮你拆目标、排时间盒和做复盘。"
    )


def check_mcp_configured(server_name: str = DEFAULT_SERVER_NAME) -> Tuple[bool, str]:
    """
    检查滴答清单 MCP 是否已配置。

    返回:
        (是否已配置, 文案)
    """

    config_paths = _candidate_mcp_config_paths()
    existing_paths = [path for path in config_paths if path.exists()]
    if not existing_paths:
        return False, build_setup_guide()

    read_errors = []
    for config_path in existing_paths:
        try:
            config = _load_mcp_config(config_path)
        except (OSError, json.JSONDecodeError) as exc:
            read_errors.append(f"{config_path}: {exc}")
            continue

        server = _find_server(config, server_name)
        if not server:
            continue

        server_url = _extract_server_url(server)
        if server_url and DEFAULT_MCP_URL not in server_url:
            return True, f"✅ 已检测到 {server_name} MCP（URL: {server_url}）"

        return True, f"✅ 已检测到 {server_name} MCP（配置文件：{config_path}）"

    if read_errors and len(read_errors) == len(existing_paths):
        return False, "❌ 读取 MCP 配置失败：\n" + "\n".join(read_errors)

    searched_paths = "\n".join(f"- {path}" for path in existing_paths)
    return False, (
        "👋 检测到已有 MCP 配置文件，但里面没有 dida365。\n\n"
        "已检查：\n"
        f"{searched_paths}\n\n"
        "请优先在当前客户端点击 dida365 的 Connect/Authorize 按钮完成浏览器授权；"
        "如果当前客户端不支持内置入口，再手动添加 dida365 MCP。"
    )


def get_mcp_setup_command(server_name: str = DEFAULT_SERVER_NAME) -> str:
    """返回 Claude CLI 的 MCP 添加命令，用作兜底方案。"""

    return f"claude mcp add --transport http {server_name} {DEFAULT_MCP_URL}"


def get_mcp_server_config(server_name: str = DEFAULT_SERVER_NAME) -> Optional[Dict[str, Any]]:
    """返回当前 dida365 MCP 配置，若不存在则返回 None。"""

    for config_path in _candidate_mcp_config_paths():
        if not config_path.exists():
            continue

        try:
            config = _load_mcp_config(config_path)
        except (OSError, json.JSONDecodeError):
            continue

        server = _find_server(config, server_name)
        if server:
            return server

    return None


def build_openclaw_http_config(server_name: str = DEFAULT_SERVER_NAME) -> Dict[str, Any]:
    """返回 OpenClaw 远程 HTTP MCP 的最小配置片段。"""

    return {
        "mcpServers": {
            server_name: {
                "transport": {
                    "type": "http",
                    "url": DEFAULT_MCP_URL,
                }
            }
        }
    }


def write_openclaw_mcp_config(server_name: str = DEFAULT_SERVER_NAME) -> Path:
    """将 dida365 写入 OpenClaw MCP 配置。"""

    config_path = get_openclaw_config_path()
    current: Dict[str, Any] = {}
    if config_path.exists():
        try:
            current = _load_mcp_config(config_path)
        except (OSError, json.JSONDecodeError):
            current = {}

    _deep_merge(current, build_openclaw_http_config(server_name))
    _save_mcp_config(config_path, current)
    return config_path


def build_openclaw_connect_guide() -> str:
    """返回 OpenClaw 半自动接入说明。"""

    config_path = get_openclaw_config_path()
    return (
        "在 OpenClaw 里推荐走半自动接入：\n\n"
        f"1. 先把 dida365 写入 `{config_path}`\n"
        "2. 刷新或重启 OpenClaw，让 dida365 出现在 MCP / Tools / 依赖面板里\n"
        "3. 点击 dida365 的 `Connect`、`Authorize` 或 `Sign in`\n"
        "4. 浏览器完成 OAuth 后，回到对话继续\n\n"
        "如果运行环境支持浏览器自动化，可以帮你打开页面、把面板切到前台并跟随普通网页按钮；"
        "但账号登录、验证码、通行密钥和 2FA 仍然必须由你本人完成。"
    )
