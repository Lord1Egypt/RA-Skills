#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — 环境/依赖/向导（doctor、setup、MCP 指引）子模块。"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import json
import os
import platform
import shlex
import shutil
import sys
from pathlib import Path

# 共享工具函数从 engine 懒加载（engine 的命令为懒代理，运行期才 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403

ENV_HINT_CMDS = {
    "rclone": ("rclone", "brew install rclone（目录递归 / 转存 / 同步需要）"),
    "alist": ("AList", "安装 AList（官方脚本或 Docker；或只用直链 / WebDAV）"),
    "aria2": ("aria2", "brew install aria2（http/ftp/BT/磁力多线程，突破单连接限速需要）"),
    "ytdlp": ("yt-dlp", "网页视频/HLS/多站直接下载需要；pip/brew 安装或 .codex/bin 便携版"),
    "baidupcs": ("BaiduPCS-Go", "安装 BaiduPCS-Go（百度分享需要）"),
    "quarkcli": ("quark-cli", "安装 quark-cli（夸克需要）"),
}


PLATFORM_SETUP_HINTS = {
    "darwin": [
        "依赖安装：brew install aria2 yt-dlp rclone",
        "凭据库：macOS Keychain",
    ],
    "windows": [
        "依赖安装：winget install --id aria2.aria2、--id yt-dlp.yt-dlp、--id Rclone.Rclone",
        "路径写法：D:\\Downloads 或 C:\\Users\\<user>\\Downloads",
        "凭据库：Windows Credential Manager",
    ],
    "linux": [
        "依赖安装：sudo apt-get install -y aria2 yt-dlp libsecret-tools；或 sudo dnf install -y aria2 yt-dlp libsecret",
        "凭据库：libsecret / secret-tool",
    ],
}


def platform_setup_hints():
    return PLATFORM_SETUP_HINTS.get(platform.system().lower(), ["依赖安装：使用系统包管理器或手动安装"])


def env_install_hints(cfg):
    hints = []
    for engine, (label, hint) in ENV_HINT_CMDS.items():
        if not find_engine_binary(engine, cfg):
            hints.append("%s：%s" % (label, hint))
    return hints


def cmd_init_wizard(args):
    cfg = load_config()
    created = False
    root0 = default_root(cfg)
    hints = env_install_hints(cfg)
    try:
        drives = sorted(all_drives(cfg).keys())
    except Exception:
        drives = []
    plan = {
        "ok": True,
        "config": str(CONFIG_PATH),
        "created": created,
        "download_root": str(root0),
        "hints": hints,
        "drives": drives,
        "next_steps": [
            "python3 scripts/pan.py doctor --json",
            "python3 scripts/pan.py secret set notify.work_weixin --stdin",
            "python3 scripts/pan.py login <盘名>",
        ],
    }
    if getattr(args, "json", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    print("向导：只读检测（要创建配置请运行：pan init）")
    print("配置文件：%s" % CONFIG_PATH)
    print("默认下载目录：%s" % root0)
    if hints:
        print("建议安装：")
        for h in hints:
            print("  - %s" % h)
    if drives:
        print("可识别网盘：%s 个" % len(drives))
    print("下一步：doctor 检查 → login 登录 → get 下载")
    return 0


# ------------------------------------------------------------------ 一键安装与配置向导
INSTALL_CMDS = {
    "rclone": {
        "brew": ["brew", "install", "rclone"],
        "apt": ["sudo", "apt-get", "install", "-y", "rclone"],
        "dnf": ["sudo", "dnf", "install", "-y", "rclone"],
        "winget": ["winget", "install", "--id", "Rclone.Rclone", "--accept-source-agreements", "--accept-package-agreements"],
    },
    "aria2": {
        "brew": ["brew", "install", "aria2"],
        "apt": ["sudo", "apt-get", "install", "-y", "aria2"],
        "dnf": ["sudo", "dnf", "install", "-y", "aria2"],
        "winget": ["winget", "install", "--id", "aria2.aria2", "--accept-source-agreements", "--accept-package-agreements"],
    },
    "ytdlp": {
        "brew": ["brew", "install", "yt-dlp"],
        "apt": ["sudo", "apt-get", "install", "-y", "yt-dlp"],
        "dnf": ["sudo", "dnf", "install", "-y", "yt-dlp"],
        "pip": [".codex/bin/yt-dlp", "--version"],
        "winget": ["winget", "install", "--id", "yt-dlp.yt-dlp", "--accept-source-agreements", "--accept-package-agreements"],
    },
}


def detect_pkg_manager():
    """按当前平台返回可用于自动安装的包管理器；找不到返回空。"""
    sys_name = platform.system().lower()
    if sys_name == "darwin":
        return "brew" if shutil.which("brew") else ""
    if sys_name in ("linux",):
        for name in ("apt-get", "dnf", "yum", "apk"):
            if shutil.which(name):
                return name.replace("-get", "") if name in ("apt-get",) else name
        return ""
    if sys_name == "windows":
        for name in ("winget", "choco", "scoop"):
            if shutil.which(name):
                return name
        return ""
    return ""


def setup_install_plan(cfg):
    """生成一键安装计划：缺失依赖 + 可执行命令列表。"""
    missing = []
    commands = []
    pkg = detect_pkg_manager()
    for engine, (label, hint) in ENV_HINT_CMDS.items():
        if find_engine_binary(engine, cfg):
            continue
        item = {"engine": engine, "label": label, "manual": (hint or "").strip()}
        cmd = (INSTALL_CMDS.get(engine) or {}).get(pkg) if pkg else None
        if cmd:
            item["command"] = cmd
            commands.append(cmd)
        missing.append(item)
    return {"pkg_manager": pkg or "", "missing": missing, "commands": commands}


def _deployment_dirs(root):
    base = Path(os.path.expanduser(root))
    return {"默认": str(base), "电影": str(base / "电影"), "音乐": str(base / "音乐"),
            "资料": str(base / "资料"), "临时": "/tmp"}


def apply_deployment(cfg, args):
    """把部署模式/地址/目录写入配置；所有入口都从这里读取。"""
    mode = getattr(args, "mode", None)
    port = int(getattr(args, "port", 0) or 17890)
    host = str(getattr(args, "host", "") or "").strip()
    dep = cfg.setdefault("deployment", {})
    if mode:
        dep["mode"] = mode
    dep["web_port"] = port
    if host:
        dep["web_host"] = host
    if getattr(args, "api_url", None):
        dep["api_url"] = str(args.api_url).strip()
    elif host:
        dep["api_url"] = "http://%s:%d" % (host, port)
    root = str(getattr(args, "root", "") or "").strip()
    if root:
        root = os.path.expanduser(root)
        cfg["download_root"] = root
    elif mode in ("nas_docker", "server_docker"):
        cfg["download_root"] = cfg.get("download_root") or "/data/download"
    elif mode == "local" and not cfg.get("download_root"):
        cfg["download_root"] = str(default_root(cfg))
    dep["download_dirs"] = _deployment_dirs(cfg.get("download_root") or default_root(cfg))
    if getattr(args, "alist_url", None):
        cfg.setdefault("engines", {})["alist_url"] = str(args.alist_url).strip()
    if getattr(args, "rclone_remote", None):
        cfg.setdefault("engines", {})["rclone_remote"] = str(args.rclone_remote).strip()
    return cfg


def cmd_setup(args):
    """一键安装 + 配置向导：创建配置、补依赖、输出下一步。"""
    cfg = load_config()
    created = False
    deployment_applied = any(getattr(args, k, None) for k in ("mode", "host", "alist_url", "rclone_remote")) or getattr(args, "root", None)
    if deployment_applied:
        cfg = apply_deployment(cfg, args)
        save_config(cfg)
        created = created or not CONFIG_PATH.exists()
    elif not CONFIG_PATH.exists() or getattr(args, "force", False):
        cfg["download_root"] = os.path.expanduser(getattr(args, "root", None) or default_root(cfg))
        cfg.setdefault("deployment", {})
        save_config(cfg)
        created = True
    plan = setup_install_plan(cfg)
    ok = True
    applied = []
    if getattr(args, "apply", False) and plan["commands"]:
        # 安全模式：不代跑包管理器；只输出已脱敏命令，由用户复核后手动执行。
        for argv in plan["commands"]:
            print("SAFE_RUN_SUGGESTION:", " ".join(shlex.quote(x) for x in mask_argv(argv)))
    mcp_script = Path(__file__).resolve().parent.parent / "pan_mcp.py"
    dep = cfg.get("deployment") or {}
    result = {
        "ok": ok,
        "setup": "complete" if (not plan["missing"] and ok) else "partial",
        "config": str(CONFIG_PATH),
        "created": created,
        "deployment": {
            "mode": dep.get("mode") or ("docker" if os.environ.get("PAN_CONFIG") or Path("/.dockerenv").exists() else "local"),
            "web_port": int(dep.get("web_port") or 17890),
            "api_url": dep.get("api_url") or "http://127.0.0.1:%d" % int(dep.get("web_port") or 17890),
            "download_root": str(default_root(cfg)),
            "download_dirs": dep.get("download_dirs") or _deployment_dirs(default_root(cfg)),
        },
        "agent_mcp": {
            "script": str(mcp_script),
            "config_toml": '[mcp_servers.pan-cloud-drive]\ncommand = %s\nenabled = true\n' % json.dumps(str(mcp_script)),
        },
        "browser_extension": {
            "manifest": str(Path(__file__).resolve().parent.parent.parent / "extensions" / "chrome" / "manifest.json"),
            "server_url": dep.get("api_url") or "http://127.0.0.1:%d" % int(dep.get("web_port") or 17890),
        },
        "pkg_manager": plan["pkg_manager"],
        "missing": plan["missing"],
        "applied": applied,
        "next_steps": [
            "python3 scripts/pan.py doctor --json",
            "python3 scripts/pan.py login <盘名>",
            "python3 scripts/pan.py get <链接>",
        ],
    }
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    print("pan-downloader setup")
    print("配置文件：%s%s" % (CONFIG_PATH, "（已创建）" if created else ""))
    print("配置优先级：CLI 参数 > 环境变量 > config.json > 内置默认值")
    dep = cfg.get("deployment") or {}
    print("部署模式：%s（local 默认；nas_docker/server_docker 可选）" % (dep.get("mode") or ("docker" if os.environ.get("PAN_CONFIG") or Path("/.dockerenv").exists() else "local")))
    print("Web/API：%s" % (dep.get("api_url") or "http://127.0.0.1:%d" % int(dep.get("web_port") or 17890)))
    print("默认目录：%s" % default_root(cfg))
    print("三类入口：Agent/MCP/CLI、Web UI、浏览器插件")
    print("浏览器插件：extensions/chrome；支持本机、NAS、服务器地址；只投递用户提供链接")
    print("MCP 注册片段：%s（无服务模式可直接调用 pan.py）" % (Path(__file__).resolve().parent.parent / "pan_mcp.py"))
    print("系统用法：" + "；".join(platform_setup_hints()))
    print("系统包管理器：%s" % (plan["pkg_manager"] or "未识别（按需手动安装）"))
    if plan["missing"]:
        print("待安装：")
        for item in plan["missing"]:
            cmds = "、".join(shlex.quote(x) for x in item.get("command", [])) if item.get("command") else item.get("manual", "手动安装")
            print("  - %s：%s" % (item["label"], cmds))
    if applied:
        print("已执行：%d 条" % len(applied))
        for item in applied:
            print("  - %s → %s" % (" ".join(shlex.quote(x) for x in item["argv"]), "成功" if item["ok"] else "失败"))
    if not plan["missing"]:
        print("✅ 环境已就绪，下一步：login 登录 → get 下载")
    else:
        print("提示：本 Skill 不自动执行系统安装；请复制上面命令，复核后手动运行。")
    return 0 if ok else 1


def cmd_mcp_guide(args):
    script = Path(__file__).resolve().parent.parent / "pan_mcp.py"
    ok = script.exists()
    snippet = ("[mcp_servers.pan-cloud-drive]\n"
               "command = %s\n"
               "enabled = true\n" % json.dumps(str(script)))
    body = {
        "ok": ok,
        "script": str(script),
        "config_toml": snippet if ok else "",
        "note": "加到 <codex-home>/config.toml 后重启 Codex；如被配置接管工具覆盖，需重新注册",
    }
    if getattr(args, "json", False):
        print(json.dumps(body, ensure_ascii=False, indent=2))
    elif not ok:
        print("❌ 未找到 %s" % script)
    else:
        print("MCP 注册片段（写入 <codex-home>/config.toml 的 [mcp_servers] 区）：")
        print(snippet)
        print("提示：重启 Codex 后在对话里应能看到 pan_doctor / pan_detect / pan_dirs / pan_get_plan")
    return 0 if ok else 1


def cmd_doctor(args):
    cfg = load_config()
    backend_names = {
        "macos": "macOS Keychain",
        "windows": "Windows Credential Manager",
        "secret-tool": "libsecret / secret-tool",
        "unsupported": "不可用（拒绝保存明文）",
    }
    backend = credential_backend()
    # 运行模式：本机默认；Docker 只是可选部署
    dep0 = cfg.get("deployment") or {}
    if dep0.get("mode") == "local":
        _mode = "local / 本机 Agent / CLI"
    elif os.environ.get("PAN_CONFIG") or Path("/.dockerenv").exists():
        _mode = "Docker 部署（curl/aria2 已由镜像提供）"
    elif dep0.get("mode") in ("nas_docker", "server_docker"):
        _mode = "%s 配置模式（Docker 引擎由远端提供）" % dep0["mode"]
    else:
        _mode = "local / 本机 Agent / CLI"
    checks = [
        ("运行模式", _mode),
        ("python3", sys.version.split()[0]),
        ("系统", "%s / %s" % (platform.system() or "unknown", backend_names.get(backend, backend))),
        ("零客户端桥", "浏览器直链捕获 / AList / OAuth / WebDAV"),
        ("curl", shutil.which("curl") or "缺失"),
        ("aria2c", find_engine_binary("aria2", cfg) or "未安装（可选）"),
        ("alist", find_engine_binary("alist", cfg) or "未安装（多数网盘挂载需要）"),
        ("BaiduPCS-Go", find_engine_binary("baidupcs", cfg) or "未安装（百度分享需要）"),
        ("quark-cli", find_engine_binary("quarkcli", cfg) or "未安装（夸克分享需要）"),
        ("rclone", find_engine_binary("rclone", cfg) or "未安装（可选，目录递归需要）"),
        ("webdav", ((cfg.get("engines") or {}).get("webdav_url") or "未配置（坚果云 WebDAV 需要）")),
        ("系统凭据库", backend_names.get(backend, backend) if credential_available() else "不可用（拒绝保存明文）"),
        ("配置文件", str(CONFIG_PATH) if CONFIG_PATH.exists() else "未创建（运行 init）"),
        ("默认下载目录", str(default_root(cfg))),
    ]
    if _mode != "local / 本机 Agent / CLI":
        checks += [
            ("ssh", find_engine_binary("ssh", cfg) or "未安装（远程执行/部署需要）"),
            ("scp", find_engine_binary("scp", cfg) or "未安装（远程部署需要）"),
            ("远程设备", "%d 个已登记" % len(cfg.get("remotes") or {})),
        ]
    hints = env_install_hints(cfg)
    if args.json:
        print(json.dumps({"checks": checks, "config": mask_value("config", cfg), "hints": hints},
                          ensure_ascii=False, indent=2))
        return 0
    print("pan-downloader doctor")
    for name, value in checks:
        print("  %-14s %s" % (name, value))
    if hints:
        print("建议命令：")
        for h in hints:
            print("  - %s" % h)
    for h in platform_setup_hints():
        print("系统用法：%s" % h)
    if _mode == "local / 本机 Agent / CLI":
        print("本机模式：不要求 NAS；无服务时 Agent 可直接调用 CLI。")
    return 0


