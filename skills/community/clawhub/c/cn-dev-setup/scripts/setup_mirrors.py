#!/usr/bin/env python3
"""Configure Chinese mirror sources for development tools."""

import os
import sys
import json
import shutil
import subprocess
import platform
from pathlib import Path

# Fix encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ── Mirror definitions ──────────────────────────────────────────────────────

MIRRORS = {
    "npm": {
        "name": "npm / yarn / pnpm",
        "mirror": "https://registry.npmmirror.com",
        "default": "https://registry.npmjs.org",
        "check_cmd": ["npm", "config", "get", "registry"],
        "set_cmds": [
            ["npm", "config", "set", "registry", "https://registry.npmmirror.com"],
        ],
        "reset_cmds": [
            ["npm", "config", "set", "registry", "https://registry.npmjs.org"],
        ],
    },
    "pip": {
        "name": "pip (Python)",
        "mirror": "https://pypi.tuna.tsinghua.edu.cn/simple",
        "default": "https://pypi.org/simple",
        "check_cmd": ["pip", "config", "get", "global.index-url"],
        "set_cmds": [
            ["pip", "config", "set", "global.index-url", "https://pypi.tuna.tsinghua.edu.cn/simple"],
            ["pip", "config", "set", "global.trusted-host", "pypi.tuna.tsinghua.edu.cn"],
        ],
        "reset_cmds": [
            ["pip", "config", "unset", "global.index-url"],
            ["pip", "config", "unset", "global.trusted-host"],
        ],
    },
    "go": {
        "name": "Go (GOPROXY)",
        "mirror": "https://goproxy.cn,direct",
        "default": "https://proxy.golang.org,direct",
        "check_cmd": ["go", "env", "GOPROXY"],
        "set_cmds": [
            ["go", "env", "-w", "GOPROXY=https://goproxy.cn,direct"],
            ["go", "env", "-w", "GOSUMDB=sum.golang.google.cn"],
        ],
        "reset_cmds": [
            ["go", "env", "-w", "GOPROXY=https://proxy.golang.org,direct"],
            ["go", "env", "-u", "GOSUMDB"],
        ],
    },
    "cargo": {
        "name": "Cargo (Rust)",
        "mirror": "tuna",
        "config_file": "cargo",
    },
    "docker": {
        "name": "Docker",
        "mirror": "registry-mirrors",
        "config_file": "docker",
    },
}


def run_cmd(cmd, capture=True):
    """Run a command and return (success, output)."""
    try:
        exe = shutil.which(cmd[0])
        if not exe:
            return False, f"{cmd[0]} not found"
        result = subprocess.run(
            cmd, capture_output=capture, text=True, timeout=15
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def check_tool_installed(tool_name):
    """Check if a tool is installed."""
    cmd_map = {"npm": "npm", "pip": "pip", "go": "go", "cargo": "cargo", "docker": "docker"}
    exe = cmd_map.get(tool_name, tool_name)
    return shutil.which(exe) is not None


def get_current_source(tool_name):
    """Get current mirror source for a tool."""
    info = MIRRORS.get(tool_name)
    if not info:
        return "unknown"

    if "check_cmd" in info:
        ok, output = run_cmd(info["check_cmd"])
        if ok:
            return output
        return info.get("default", "unknown")

    if tool_name == "cargo":
        config = Path.home() / ".cargo" / "config.toml"
        if config.exists():
            content = config.read_text()
            if "tuna" in content or "ustc" in content or "rsproxy" in content:
                return "CN mirror configured"
        return "default (crates.io)"

    if tool_name == "docker":
        paths = [
            Path("/etc/docker/daemon.json"),
            Path.home() / ".docker" / "daemon.json",
        ]
        for p in paths:
            if p.exists():
                try:
                    data = json.loads(p.read_text())
                    mirrors = data.get("registry-mirrors", [])
                    if mirrors:
                        return f"mirrors: {', '.join(mirrors[:2])}"
                except:
                    pass
        return "default (Docker Hub)"

    return "unknown"


def is_cn_mirror(tool_name, current):
    """Check if current source is already a CN mirror."""
    cn_keywords = [
        "npmmirror", "taobao", "tuna", "aliyun", "huaweicloud",
        "tencent", "ustc", "douban", "goproxy.cn", "goproxy.io",
        "1ms.run", "xuanyuan", "daocloud", "nju.edu", "rsproxy",
        "CN mirror",
    ]
    return any(k in current.lower() for k in cn_keywords)


def setup_tool(tool_name):
    """Configure CN mirror for a tool."""
    info = MIRRORS.get(tool_name)
    if not info:
        print(f"  ❌ Unknown tool: {tool_name}")
        return False

    if not check_tool_installed(tool_name):
        print(f"  ⏭️  {info['name']} — not installed, skipping")
        return False

    current = get_current_source(tool_name)
    if is_cn_mirror(tool_name, current):
        print(f"  ✅ {info['name']} — already using CN mirror")
        return True

    if "set_cmds" in info:
        for cmd in info["set_cmds"]:
            ok, output = run_cmd(cmd)
            if not ok:
                print(f"  ❌ {info['name']} — failed: {output}")
                return False
        print(f"  ✅ {info['name']} — switched to CN mirror")
        return True

    if tool_name == "cargo":
        config_dir = Path.home() / ".cargo"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "config.toml"
        content = ""
        if config_file.exists():
            content = config_file.read_text()
        if "[source.tuna]" not in content:
            content += """
[source.crates-io]
replace-with = "tuna"

[source.tuna]
registry = "sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/"
"""
            config_file.write_text(content)
        print(f"  ✅ {info['name']} — switched to TUNA mirror")
        return True

    if tool_name == "docker":
        print(f"  ⚠️  {info['name']} — requires manual setup:")
        print(f"       See references/mirrors.md for Docker mirror configuration")
        print(f"       (needs root/admin access to modify daemon.json)")
        return False

    return False


def reset_tool(tool_name):
    """Reset tool to default source."""
    info = MIRRORS.get(tool_name)
    if not info:
        return False

    if "reset_cmds" in info:
        for cmd in info["reset_cmds"]:
            run_cmd(cmd)
        print(f"  🔄 {info['name']} — restored to default")
        return True

    if tool_name == "cargo":
        config_file = Path.home() / ".cargo" / "config.toml"
        if config_file.exists():
            content = config_file.read_text()
            # Remove source sections
            lines = content.split("\n")
            new_lines = []
            skip = False
            for line in lines:
                if line.startswith("[source."):
                    skip = True
                    continue
                if skip and line.startswith("["):
                    skip = False
                if not skip:
                    new_lines.append(line)
            config_file.write_text("\n".join(new_lines))
        print(f"  🔄 {info['name']} — restored to default")
        return True

    return False


def show_status():
    """Show current mirror configuration for all tools."""
    print("📊 Mirror Source Status")
    print("=" * 60)

    for tool_name, info in MIRRORS.items():
        installed = check_tool_installed(tool_name)
        if not installed:
            print(f"  ⬜ {info['name']:20s} — not installed")
            continue

        current = get_current_source(tool_name)
        is_cn = is_cn_mirror(tool_name, current)
        icon = "🇨🇳" if is_cn else "🌍"
        print(f"  {icon} {info['name']:20s} — {current}")

    print()


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("CN Dev Setup — 国内开发环境镜像源配置")
        print()
        print("Usage:")
        print("  setup_mirrors.py --all              配置所有已安装工具")
        print("  setup_mirrors.py npm pip go          配置指定工具")
        print("  setup_mirrors.py --status            查看当前源配置")
        print("  setup_mirrors.py --reset npm pip     恢复默认源")
        print()
        print(f"Supported tools: {', '.join(MIRRORS.keys())}")
        sys.exit(0)

    if "--status" in args:
        show_status()
        sys.exit(0)

    if "--reset" in args:
        tools = [a for a in args if a != "--reset" and not a.startswith("-")]
        if not tools:
            tools = list(MIRRORS.keys())
        print("🔄 Restoring default sources...")
        for tool in tools:
            reset_tool(tool)
        print("\n✅ Done.")
        sys.exit(0)

    if "--all" in args:
        tools = list(MIRRORS.keys())
    else:
        tools = [a for a in args if not a.startswith("-")]

    if not tools:
        print("No tools specified. Use --all or list tool names.")
        sys.exit(1)

    print(f"🇨🇳 Configuring CN mirrors for {len(tools)} tools...")
    print()

    success = 0
    for tool in tools:
        if tool in MIRRORS:
            if setup_tool(tool):
                success += 1
        else:
            print(f"  ❌ Unknown tool: {tool}")

    print()
    print(f"✅ Configured: {success}/{len(tools)}")
    print("💡 Some changes may require terminal restart to take effect.")


if __name__ == "__main__":
    main()
