#!/usr/bin/env python3
"""
1688-open-skill-template CLI — 统一命令入口

用法：
    python3 cli.py <command> [options]

命令：
    ali_dingtalk      发送钉钉消息
    configure         配置 AK（查看状态/设置/清除）
    auth_status       检查当前授权状态
    authorize         发起 OAuth 授权流程
    interactive       交互式授权向导
    check_token       验证 Token 对指定 scope 是否有效
    get_token         获取有效 Token
    revoke            撤销当前授权
    query_all_scope   查询所有可用权限（scope）列表
    get_ak            通过浏览器获取 1688 AK

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""
from __future__ import annotations

import importlib
import json
import logging
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = str(SKILL_DIR / "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from _const import ENV_FILE
from token_manager import (
    load_token,
    ensure_valid_token,
    revoke_access,
    revoke_refresh,
    clear_token,
)
from scope_manager import (
    query_all_scope,
    format_scope_list_markdown,
)

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def _output(success: bool, markdown: str = "", data: dict | None = None,
            error_code: str = "", required_scope: str = "", current_scope: str = "") -> None:
    """输出标准 JSON 结果"""
    result: dict = {"success": success}
    if markdown:
        result["markdown"] = markdown
    if data is not None:
        result["data"] = data
    if error_code:
        result["error_code"] = error_code
    if required_scope:
        result["required_scope"] = required_scope
    if current_scope:
        result["current_scope"] = current_scope
    print(json.dumps(result, ensure_ascii=False), flush=True)


# ── OAuth 命令实现 ──

def _scope_display(scope_str: str) -> str:
    """将 scope 标识符转为描述展示，失败时回退原始标识符"""
    if not scope_str or scope_str == "无":
        return "无"
    scope_result = query_all_scope()
    if not scope_result.get("success"):
        return scope_str
    desc_map = {s["scope"]: s.get("description", s["scope"]) for s in scope_result["scopes"]}
    parts = []
    for sid in scope_str.split():
        desc = desc_map.get(sid)
        parts.append(f"{desc}（`{sid}`）" if desc else f"`{sid}`")
    return "、".join(parts)


def cmd_auth_status(args: list[str]) -> None:
    """检查当前授权状态"""
    token = load_token(ENV_FILE)

    if not token:
        _output(success=True,
                markdown="**授权状态**: 未授权\n\n需要执行授权后才能使用 1688 API。",
                data={"authorized": False})
        return

    status = "有效" if not token["expired"] else "已过期"
    scope = token["scope"] or "无"
    scope_display = _scope_display(scope)
    expires_in = token["expires_in"]

    md = (f"**授权状态**: {status}\n"
          f"**已授权权限**: {scope_display}\n"
          f"**剩余有效期**: {expires_in // 60} 分钟 {expires_in % 60} 秒")

    if scope != "无" and scope_display == scope:
        md += ("\n\n（注意：以上权限显示为 scope 标识符，"
               "请调用 query_all_scope 命令获取中文描述后再展示给用户）")

    _output(success=True, markdown=md, data={
        "authorized": True,
        "status": status,
        "scope": scope,
        "scope_is_raw": scope != "无" and scope_display == scope,
        "expires_in": expires_in,
        "expired": token["expired"],
    })


def cmd_authorize(args: list[str]) -> int:
    """发起 OAuth 授权流程（需要 --scope 参数）"""
    if "--scope" not in args:
        _output(success=False, error_code="MISSING_PARAM",
                markdown='缺少必填参数: --scope\n\n用法: `authorize --scope "read:order write:order"`')
        return 1

    import subprocess
    script = str(SKILL_DIR / "scripts" / "authorize.py")
    result = subprocess.run([sys.executable, script] + args, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip(), flush=True)
    return result.returncode


def _run_authorize(scope: str) -> int:
    """内部辅助：调用 authorize.py 并透传输出"""
    import subprocess
    script = str(SKILL_DIR / "scripts" / "authorize.py")
    result = subprocess.run(
        [sys.executable, script, "--scope", scope], capture_output=True, text=True
    )
    if result.stdout.strip():
        print(result.stdout.strip(), flush=True)
    return result.returncode


def cmd_interactive(args: list[str]) -> int:
    """交互式授权向导（用户主动触发）"""
    token = load_token(ENV_FILE)

    if token and not token["expired"]:
        current_scope = token["scope"] or "无"
        scope_display = _scope_display(current_scope)
        expires_in_min = token["expires_in"] // 60
        md = (f"**当前授权状态**: 有效\n\n"
              f"**已授权权限**: {scope_display}\n"
              f"**剩余有效期**: {expires_in_min} 分钟\n\n"
              "您已有一个有效的 1688 授权。您可以选择：\n"
              "1. 继续使用当前授权\n"
              "2. 重新授权（获取新的 Token）\n"
              "3. 扩展授权权限（增量授权）")
        _output(success=True, markdown=md, data={
            "authorized": True,
            "scope": current_scope,
            "expires_in": token["expires_in"],
            "action_required": "user_choice",
        })
        return 0

    if token and token["expired"]:
        expired_scope = token.get("scope", "")
        if expired_scope:
            _output(success=True,
                    markdown="**当前授权状态**: 已过期\n\n"
                             "您的 1688 授权已过期，需要重新授权才能继续使用。\n\n"
                             "正在为您打开浏览器进行授权...",
                    data={"authorized": False, "expired": True, "action": "auto_redirect"})
            return _run_authorize(expired_scope)

    scope_result = query_all_scope()
    data: dict = {"authorized": False, "action_required": "user_input_scope"}

    if scope_result.get("success") and scope_result.get("scopes"):
        scope_list_md = format_scope_list_markdown(scope_result["scopes"])
        data["available_scopes"] = scope_result["scopes"]
        md = (f"**欢迎使用 1688 账号授权**\n\n"
              f"您尚未授权 1688 账号。以下是平台支持的权限列表：\n\n"
              f"{scope_list_md}\n请告诉我您需要授权哪些权限。")
    else:
        md = ("**欢迎使用 1688 账号授权**\n\n"
              "您尚未授权 1688 账号。授权后您可以：\n"
              "- 查询和管理您的 1688 订单\n"
              "- 查看商品信息\n"
              "- 进行其他需要账号权限的操作\n\n"
              "请告诉我您需要授权哪些权限。")

    _output(success=True, markdown=md, data=data)
    return 0


def _parse_scope(args: list[str], command_name: str) -> str | None:
    """解析 --scope 参数，缺失时输出错误并返回 None"""
    for i, arg in enumerate(args):
        if arg == "--scope" and i + 1 < len(args):
            return args[i + 1]
    _output(success=False, error_code="MISSING_PARAM",
            markdown=f'缺少必填参数: --scope\n\n用法: `{command_name} --scope "read:order"`')
    return None


def _output_token_error(token_check: dict) -> None:
    _output(
        success=False,
        error_code=token_check["error_code"],
        markdown=token_check.get("message", "需要授权"),
        required_scope=token_check.get("required_scope", ""),
        current_scope=token_check.get("current_scope", ""),
    )


def cmd_check_token(args: list[str]) -> None:
    """验证 Token 对指定 scope 是否有效"""
    scope = _parse_scope(args, "check_token")
    if not scope:
        return
    token_check = ensure_valid_token(required_scope=scope, env_file=ENV_FILE)
    if token_check["valid"]:
        _output(success=True, markdown="Token 有效，已具备所需权限。", data={
            "valid": True,
            "scope": token_check["scope"],
            "expires_in": token_check["expires_in"],
        })
    else:
        _output_token_error(token_check)


def cmd_get_token(args: list[str]) -> None:
    """获取有效 Token（供业务 Skill 通过 stdout pipe 调用）"""
    scope = _parse_scope(args, "get_token")
    if not scope:
        return
    token_check = ensure_valid_token(required_scope=scope, env_file=ENV_FILE)
    if token_check["valid"]:
        _output(success=True, markdown="Token 有效。", data={
            "access_token": token_check["access_token"],
            "scope": token_check["scope"],
            "expires_in": token_check["expires_in"],
        })
    else:
        _output_token_error(token_check)


def cmd_revoke(args: list[str]) -> None:
    """撤销当前授权"""
    token = load_token(ENV_FILE)
    if not token:
        _output(success=True, markdown="当前没有活跃的授权，无需撤销。")
        return

    access_result = revoke_access(ENV_FILE)
    refresh_result = revoke_refresh(ENV_FILE)
    clear_token(ENV_FILE)

    access_ok = access_result.get("success", False)
    refresh_ok = refresh_result.get("success", False)

    if access_ok and refresh_ok:
        _output(success=True,
                markdown="授权已撤销。Token 已从本地清除，Access Token 和 Refresh Token 已在服务端吊销。")
    else:
        failures = []
        if not access_ok:
            failures.append(f"Access Token: {access_result.get('error', '未知错误')}")
        if not refresh_ok:
            failures.append(f"Refresh Token: {refresh_result.get('error', '未知错误')}")
        detail = "\n".join(f"- {f}" for f in failures)
        _output(success=True,
                markdown=f"Token 已从本地清除，但服务端吊销部分失败：\n\n{detail}\n\n"
                         "建议联系管理员手动吊销，或等待 Token 自然过期。")


def cmd_query_all_scope(args: list[str]) -> None:
    """查询所有可用权限（scope）列表"""
    result = query_all_scope()
    if not result.get("success"):
        _output(success=False, error_code="SCOPE_QUERY_FAILED",
                markdown=f"获取权限列表失败: {result.get('error_description', '未知错误')}")
        return

    scopes = result["scopes"]
    md = "**1688 平台可用权限列表**\n\n" + format_scope_list_markdown(scopes)
    if result.get("stale"):
        md += "\n> 注意: 数据来自本地缓存，可能不是最新。\n"

    _output(success=True, markdown=md, data={
        "scopes": scopes,
        "from_cache": result.get("from_cache", False),
    })


def cmd_get_ak(args: list[str]) -> int:
    """通过浏览器获取 1688 AK（Access Key）"""
    import subprocess
    timeout = 300
    for i, arg in enumerate(args):
        if arg == "--timeout" and i + 1 < len(args):
            try:
                timeout = int(args[i + 1])
            except ValueError:
                pass

    script = str(SKILL_DIR / "scripts" / "authorize.py")
    result = subprocess.run(
        [sys.executable, script, "--mode", "AK", "--timeout", str(timeout)],
        capture_output=True, text=True,
    )
    if result.stdout.strip():
        print(result.stdout.strip(), flush=True)
    if result.stderr.strip() and not result.stdout.strip():
        _output(success=False, error_code="SUBPROCESS_ERROR",
                markdown=f"获取 AK 失败：{result.stderr.strip()}")
    return result.returncode


# ── OAuth 命令表（显式注册，优先级高于自动发现） ──

OAUTH_COMMANDS: dict[str, tuple] = {
    "get_ak": (cmd_get_ak,"通过浏览器页面登录获取AK"),
}

def _discover_capabilities() -> dict[str, str]:
    """扫描 capabilities/*/cmd.py，自动注册命令。返回 {cmd_name: module_path}"""
    commands: dict[str, str] = {}
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")
    if not os.path.isdir(caps_dir):
        return commands
    for name in sorted(os.listdir(caps_dir)):
        cmd_path = os.path.join(caps_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"capabilities.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, "COMMAND_NAME", name)
            commands[cmd_name] = module_path
        except Exception:
            pass
    return commands


def _usage(commands: dict) -> None:
    lines = ["**1688-open-skill-template 用法**\n", "```"]
    for name in sorted(commands):
        handler = commands[name]
        if isinstance(handler, tuple):
            desc = handler[1]
        else:
            try:
                mod = importlib.import_module(handler)
                desc = getattr(mod, "COMMAND_DESC", "")
            except Exception:
                desc = ""
        lines.append(f"python3 cli.py {name:<20} {desc}")
    lines.append("```")
    _output(success=True, markdown="\n".join(lines))


def main() -> int:
    # 自动发现 capability 目录命令（module_path 字符串）
    cap_commands = _discover_capabilities()

    # 合并：capability 命令 + OAuth 命令（OAuth 优先级更高，但 configure 只在 cap_commands）
    all_commands: dict = {**cap_commands, **OAUTH_COMMANDS}

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        _usage(all_commands)
        return 1

    command = sys.argv[1]
    cmd_args = sys.argv[2:]

    handler = all_commands.get(command)
    if not handler:
        _output(success=False, error_code="UNKNOWN_COMMAND",
                markdown=f"未知命令: `{command}`\n\n可用命令: {', '.join(sorted(all_commands.keys()))}")
        return 1

    if isinstance(handler, tuple):
        # OAuth 命令：直接调用函数
        result = handler[0](cmd_args)
    else:
        # capability 模块：重置 sys.argv 后调用 module.main()
        sys.argv = [f"cli.py {command}"] + cmd_args
        mod = importlib.import_module(handler)
        result = mod.main()

    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass

    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
