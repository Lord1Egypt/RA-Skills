"""Cursor 自动修复功能 — 基于诊断结果应用修复方案"""

from cursor_doctor.signatures.database import ErrorSignature, find_by_id
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
import subprocess
import os
import shutil
import json

console = Console()


def _run_cmd(cmd: list[str], timeout: int = 30) -> tuple[str, str, int]:
    """运行系统命令"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout, r.stderr, r.returncode
    except FileNotFoundError:
        return "", "命令未找到", -1
    except subprocess.TimeoutExpired:
        return "", "执行超时", -1


def fix_mcp_connection() -> str:
    """修复 MCP 连接问题"""
    steps = []
    # Kill any existing cursor processes
    stdout, stderr, rc = _run_cmd(["pkill", "-f", "Cursor"])
    steps.append("✅ 已终止 Cursor 进程")
    
    # Clear MCP cache
    home = os.path.expanduser("~")
    mcp_dir = os.path.join(home, ".cursor", ".mcp")
    if os.path.isdir(mcp_dir):
        try:
            shutil.rmtree(mcp_dir, ignore_errors=True)
            steps.append("✅ 已清除 MCP 缓存")
        except Exception:
            steps.append("⚠️ 无法清除 MCP 缓存, 需要手动删除")
    
    steps.append("💡 重启 Cursor 后重试 MCP 连接")
    return "\n".join(steps)


def fix_crash_clear_cache() -> str:
    """清除 Cursor 缓存修复崩溃"""
    steps = []
    home = os.path.expanduser("~")
    
    cache_dirs = [
        os.path.join(home, "Library", "Application Support", "Cursor", "Cache"),
        os.path.join(home, "Library", "Application Support", "Cursor", "CachedData"),
        os.path.join(home, "Library", "Application Support", "Cursor", "Code Cache"),
        os.path.join(home, ".cursor", ".mcp"),
    ]
    
    for d in cache_dirs:
        if os.path.isdir(d):
            try:
                shutil.rmtree(d, ignore_errors=True)
                steps.append(f"✅ 已清除: {os.path.basename(d)}")
            except Exception:
                steps.append(f"⚠️ 清除失败: {os.path.basename(d)}")
    
    # Kill Cursor
    _run_cmd(["pkill", "-f", "Cursor"])
    steps.append("✅ 已终止 Cursor 进程")
    
    return "\n".join(steps)


def fix_network_proxy() -> str:
    """修复代理/网络问题"""
    steps = []
    
    # Check what proxies are set
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy", "")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy", "")
    
    if http_proxy:
        steps.append(f"⚠️ 检测到 HTTP_PROXY={http_proxy}")
    if https_proxy:
        steps.append(f"⚠️ 检测到 HTTPS_PROXY={https_proxy}")
    
    steps.append("💡 建议: 在 Cursor 设置中搜索 'proxy' 配置代理")
    steps.append("💡 或在终端执行: unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY && open -a Cursor")
    steps.append("💡 中国用户建议: Cursor 设置 → HTTP: Proxy → 填入代理地址")
    
    return "\n".join(steps)


def fix_config_reset() -> str:
    """重置 Cursor 配置"""
    steps = []
    home = os.path.expanduser("~")
    
    config_dir = os.path.join(home, "Library", "Application Support", "Cursor", "User")
    if not os.path.isdir(config_dir):
        config_dir = os.path.join(home, ".cursor", "User")
    
    settings_file = os.path.join(config_dir, "settings.json")
    backup_file = settings_file + ".backup." + str(int(__import__('time').time()))
    
    if os.path.isfile(settings_file):
        try:
            shutil.copy2(settings_file, backup_file)
            steps.append(f"✅ 已备份配置到 {backup_file}")
            
            # Reset to minimal valid config
            with open(settings_file, "w") as f:
                json.dump({}, f)
            steps.append("✅ 配置已重置为默认")
        except Exception as e:
            steps.append(f"⚠️ 配置重置失败: {e}")
    
    return "\n".join(steps)


# 修复方案映射
FIX_MAP: dict[str, tuple[str, callable]] = {
    "mcp_connection": ("🔌 MCP 连接修复", fix_mcp_connection),
    "crash": ("💥 崩溃修复 (清除缓存)", fix_crash_clear_cache),
    "network_proxy": ("🌐 网络/代理修复", fix_network_proxy),
    "config_env": ("⚙️ 配置修复", fix_config_reset),
}


def suggest_fixes(errors: list[dict]) -> list[dict]:
    """根据诊断结果推荐修复方案"""
    applied = set()
    suggestions = []
    
    for error in errors:
        sig = find_by_id(error["signature_id"])
        if not sig or sig.category in applied:
            continue
        applied.add(sig.category)
        
        fix_info = FIX_MAP.get(sig.category)
        if fix_info:
            suggestions.append({
                "category": sig.category,
                "name": fix_info[0],
                "description": sig.fix_hint,
                "severity": sig.severity if hasattr(sig, 'severity') else "medium",
            })
    
    return suggestions


def apply_fix(errors: list[dict], fix_category: str) -> str:
    """应用指定类别的修复"""
    fix_info = FIX_MAP.get(fix_category)
    if not fix_info:
        return f"❌ 未知修复类别: {fix_category}"
    
    name, fix_fn = fix_info
    console.print(Panel(f"正在执行: {name}", style="bold yellow"))
    result = fix_fn()
    console.print(Panel(f"完成: {name}", style="bold green"))
    return result
