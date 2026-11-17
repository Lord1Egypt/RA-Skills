#!/usr/bin/env python3
"""dgngjx-skill 首次运行体检报告 v4.1.0"""
import sys, subprocess, os, json, platform

HEALTH_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_health.json")

def check_python():
    v = sys.version_info
    ok = v >= (3, 8)
    return {
        "name": "Python",
        "status": "ok" if ok else "warn",
        "version": f"{v.major}.{v.minor}.{v.micro}",
        "required": "≥ 3.8",
        "fix": None if ok else "请升级 Python 到 3.8+"
    }

def check_module(pkg_name, import_name=None):
    import_name = import_name or pkg_name
    try:
        __import__(import_name)
        return {"name": pkg_name, "status": "ok", "version": "", "required": "", "fix": None}
    except ImportError:
        return {"name": pkg_name, "status": "missing", "version": "", "required": "", "fix": f"pip install {pkg_name}"}

def check_ffmpeg():
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            line = r.stdout.split("\n")[0]
            return {"name": "FFmpeg", "status": "ok", "version": line[:50], "required": "", "fix": None}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {"name": "FFmpeg", "status": "missing", "version": "", "required": "视频转换/编辑", "fix": "winget install ffmpeg"}

def check_network():
    try:
        import urllib.request
        req = urllib.request.Request("https://api.github.com", headers={"User-Agent":"dgngjx/4.1"})
        urllib.request.urlopen(req, timeout=5)
        return {"name": "网络连接", "status": "ok", "version": "", "required": "", "fix": None}
    except Exception as e:
        return {"name": "网络连接", "status": "warn", "version": "", "required": "汇率/知识查询", "fix": f"网络受限: {type(e).__name__}"}

def check_disk():
    try:
        import shutil
        total, used, free = shutil.disk_usage(os.path.expanduser("~"))
        free_gb = free / (1024**3)
        ok = free_gb >= 1.0
        return {
            "name": "磁盘空间",
            "status": "ok" if ok else "warn",
            "version": f"剩余 {free_gb:.1f} GB",
            "required": "≥ 1GB",
            "fix": None if ok else "磁盘空间不足，建议清理"
        }
    except Exception:
        return {"name": "磁盘空间", "status": "ok", "version": "", "required": "", "fix": None}

def run_health_check(force=False):
    """运行体检，首次自动显示，后续可通过 dgngjx --health 触发"""
    # 检查是否已体检过
    if not force and os.path.exists(HEALTH_FILE):
        try:
            with open(HEALTH_FILE, encoding="utf-8") as f:
                prev = json.load(f)
            if prev.get("skipped", False):
                return None  # 用户跳过，不显示
        except:
            pass

    checks = [
        check_python(),
        check_module("Pillow", "PIL"),
        check_module("PyPDF2"),
        check_module("rembg"),
        check_module("jieba"),
        check_ffmpeg(),
        check_network(),
        check_disk(),
    ]

    ok_count = sum(1 for c in checks if c["status"] == "ok")
    missing = [c for c in checks if c["status"] == "missing"]
    warnings = [c for c in checks if c["status"] == "warn"]

    print("=" * 50)
    print("  🏥 dgngjx-skill 首次运行体检报告")
    print("=" * 50)
    print()

    for c in checks:
        icon = "✅" if c["status"] == "ok" else ("⚠️" if c["status"] == "warn" else "❌")
        ver = f" ({c['version']})" if c["version"] else ""
        print(f"  {icon} {c['name']}{ver}")

    print()
    print(f"  就绪率: {ok_count}/{len(checks)} ({ok_count*100//len(checks)}%)")

    if missing:
        print()
        print("  📦 缺失依赖（一键安装）：")
        cmds = []
        for c in missing:
            if c["fix"]:
                print(f"    • {c['name']}: {c['fix']}")
                if "pip install" in c["fix"]:
                    cmds.append(c["fix"].replace("pip install ", ""))
        if cmds:
            print()
            print(f"  快速安装: pip install {' '.join(cmds)}")

    if warnings:
        print()
        print("  ⚠️ 警告：")
        for c in warnings:
            if c["fix"]:
                print(f"    • {c['name']}: {c['fix']}")

    print()
    print("  💡 提示：随时运行 dgngjx --health 重新体检")
    print("=" * 50)

    # 记录体检状态
    os.makedirs(os.path.dirname(HEALTH_FILE), exist_ok=True)
    with open(HEALTH_FILE, "w", encoding="utf-8") as f:
        json.dump({"checked": True, "skipped": False, "ok_count": ok_count, "total": len(checks)}, f)

    return checks

if __name__ == "__main__":
    force = "--force" in sys.argv
    run_health_check(force=force)
