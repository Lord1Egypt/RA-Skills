"""CLAM MCP Server — 让 AI 通过 MCP 协议直接控制 macOS 应用。

Usage:
    clam-mcp              # 启动 MCP server (stdio 模式)

Claude Code 配置 (~/.claude.json):
    {
      "mcpServers": {
        "clam": { "command": "clam-mcp" }
      }
    }
"""

from __future__ import annotations

import json
import subprocess

from mcp.server.fastmcp import FastMCP

from clam.generator.applescript_gen import (
    check_command_support,
    generate_basic_wrapper,
    generate_ui_wrapper,
    generate_wrapper,
    get_ui_wrapper_info,
    get_wrapper_info,
)
from clam.generator.installer import install_wrapper
from clam.registry import registry
from clam.scanner.app_scanner import find_app, find_basic_app, scan_applications
from clam.scanner.menu_scanner import scan_menus
from clam.scanner.sdef_parser import parse_sdef

mcp = FastMCP("clam")


@mcp.tool()
def clam_scan() -> str:
    """扫描 macOS 上可被脚本化控制的应用。

    返回所有可控应用的列表，包含名称、ID、命令数、属性数、模式等信息。
    mode: "full" = 完整 AppleScript 支持, "ui" = UI Scripting (菜单点击), "basic" = 基础模式。
    """
    apps = scan_applications()
    results = []
    for app in apps:
        if app.sdef_path:
            try:
                sdef_info = parse_sdef(app.sdef_path, app.name)
                wi = get_wrapper_info(sdef_info, app.app_id)
                results.append({
                    "name": app.name,
                    "app_id": app.app_id,
                    "commands": len(wi["commands"]),
                    "properties": len(wi["properties"]),
                    "nested_groups": len(wi["nested_groups"]),
                    "installed": app.installed,
                    "mode": "full",
                })
            except Exception:
                continue
        else:
            results.append({
                "name": app.name,
                "app_id": app.app_id,
                "commands": 0,
                "properties": 0,
                "installed": app.installed,
                "mode": "ui",
            })
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def clam_info(app_id: str) -> str:
    """查看某个应用的完整能力清单（命令、属性、嵌套对象）。

    每个命令都有 supported 字段标记是否可靠。调用前先用此工具了解有哪些命令可用。
    app_id 支持模糊匹配：chrome → google-chrome, word → microsoft-word。
    """
    app = find_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    if not app.sdef_path:
        return json.dumps({
            "app_id": app.app_id,
            "app_name": app.name,
            "mode": "ui" if not app.basic_mode else "basic",
            "note": "此应用无 AppleScript 脚本定义，请用 clam_install 安装后通过菜单点击控制",
            "commands": [],
            "properties": [],
            "nested_groups": [],
        }, ensure_ascii=False)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        return json.dumps({"error": f"解析 sdef 失败: {e}"})

    wi = get_wrapper_info(sdef_info, app.app_id)
    support = check_command_support(sdef_info, app.app_id)
    support_map = {r["name"]: r["supported"] for r in support}

    return json.dumps({
        "app_id": app.app_id,
        "app_name": app.name,
        "entry_point": f"clam-{app.app_id}",
        "commands": [
            {
                "name": cmd.cli_name,
                "description": cmd.description,
                "has_direct_param": cmd.direct_param,
                "supported": support_map.get(cmd.cli_name, True),
                "params": [
                    {"name": f"--{p.cli_name}", "description": p.description}
                    for p in cmd.params
                ],
            }
            for cmd in wi["commands"]
        ],
        "properties": [
            {
                "name": prop.cli_name,
                "access": prop.access,
                "type": prop.value_type,
                "get_command": f"get-{prop.cli_name}",
                "set_command": f"set-{prop.cli_name}" if prop.access == "rw" else None,
            }
            for prop in wi["properties"]
        ],
        "nested_groups": [
            {
                "name": group.cli_name,
                "compound_command": f"get-{group.cli_name}",
                "properties": [
                    {
                        "name": prop.cli_name,
                        "access": prop.access,
                        "get_command": f"get-{group.cli_name}-{prop.cli_name}",
                        "set_command": (
                            f"set-{group.cli_name}-{prop.cli_name}"
                            if prop.access == "rw" else None
                        ),
                    }
                    for prop in group.properties
                ],
            }
            for group in wi["nested_groups"]
        ],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def clam_install(app_id: str) -> str:
    """为指定应用安装 CLI wrapper，安装后可通过 clam_execute 执行命令。

    安装过程自动选择最佳模式：full (sdef) → ui (菜单点击) → basic (标准套件)。
    """
    app = find_app(app_id)
    if not app:
        app = find_basic_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    wrapper_dir = registry.REGISTRY_DIR / "wrappers" / app.app_id

    mode = "full"
    menu_scan = None

    if not app.sdef_path:
        menu_scan = scan_menus(app.name, app.process_name or None)
        if menu_scan and menu_scan.total_items > 0:
            mode = "ui"
        else:
            mode = "basic"

    try:
        if mode == "basic":
            generate_basic_wrapper(app.name, wrapper_dir)
            cmd_count, prop_count = 3, 3
        elif mode == "ui":
            generate_ui_wrapper(app.name, menu_scan.process_name, menu_scan, wrapper_dir)
            ui_info = get_ui_wrapper_info(menu_scan)
            cmd_count = ui_info["menu_cmd_count"] + 3
            prop_count = 3
        else:
            sdef_info = parse_sdef(app.sdef_path, app.name)
            generate_wrapper(sdef_info, wrapper_dir)
            wi = get_wrapper_info(sdef_info)
            cmd_count = len(wi["commands"])
            prop_count = len(wi["properties"])
    except Exception as e:
        return json.dumps({"error": f"生成 wrapper 失败: {e}"})

    if not install_wrapper(app.app_id, wrapper_dir):
        return json.dumps({"error": "pip install 失败"})

    registry.register(
        app_id=app.app_id,
        app_name=app.name,
        sdef_path=app.sdef_path,
        wrapper_dir=str(wrapper_dir),
        command_count=cmd_count,
        property_count=prop_count,
    )

    return json.dumps({
        "app_id": app.app_id,
        "entry_point": f"clam-{app.app_id}",
        "commands": cmd_count,
        "properties": prop_count,
        "mode": mode,
    }, ensure_ascii=False)


@mcp.tool()
def clam_execute(app_id: str, command: str, args: dict | None = None) -> str:
    """在已安装的应用 wrapper 上执行命令。

    必须先用 clam_install 安装 wrapper。
    command 是命令名（如 "play", "get-sound-volume", "set-sound-volume"）。
    args 是命名参数字典（如 {"once": true}），位置参数用 "_direct" 键传递。

    示例：
      clam_execute("music", "play")
      clam_execute("music", "set-sound-volume", {"_direct": "50"})
      clam_execute("music", "get-current-track")
    """
    # 检查是否已安装
    wrapper = registry.get(app_id)
    if not wrapper:
        return json.dumps({"error": f"未安装 wrapper: {app_id}，请先调用 clam_install"})

    entry_point = wrapper["entry_point"]
    cmd = [entry_point, "--json", command]

    if args:
        direct = args.pop("_direct", None)
        if direct is not None:
            cmd.append(str(direct))
        for key, value in args.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            else:
                cmd.extend([f"--{key}", str(value)])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=35,
        )
    except FileNotFoundError:
        return json.dumps({"error": f"找不到命令 {entry_point}，可能需要重新安装"})
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "命令执行超时 (35s)"})

    if result.returncode != 0:
        return json.dumps({
            "error": result.stderr.strip() or "命令执行失败",
            "exit_code": result.returncode,
        })

    return result.stdout.strip() or '{"result": "ok"}'


@mcp.tool()
def clam_doctor(app_id: str) -> str:
    """检查应用命令的可靠性，分析哪些命令的参数类型完全支持、哪些可能不可用。

    返回每个命令的 supported 状态和具体问题描述。
    """
    app = find_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    if not app.sdef_path:
        return json.dumps({"error": f"{app.name} 无 AppleScript 脚本定义，doctor 仅适用于 full 模式应用"})

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        return json.dumps({"error": f"解析 sdef 失败: {e}"})

    results = check_command_support(sdef_info, app.app_id)
    supported = [r for r in results if r["supported"]]
    unsupported = [r for r in results if not r["supported"]]

    return json.dumps({
        "app_id": app.app_id,
        "total": len(results),
        "supported": len(supported),
        "unsupported": len(unsupported),
        "commands": results,
    }, ensure_ascii=False, indent=2)


def main():
    """启动 CLAM MCP Server (stdio 模式)。"""
    mcp.run()


if __name__ == "__main__":
    main()
