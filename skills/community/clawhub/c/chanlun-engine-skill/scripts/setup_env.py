#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_env.py — 环境自检与分层安装 (给 AI 助手替用户跑的, 报错文案写给普通人看)
分层:
  核心层   零第三方依赖: 缠论计算引擎已打包在本技能内, 有 Python 3.11+ 就能跑 (CSV 输入)
  推荐层   --recommended: 装 akshare (免费行情, 不需要任何账号, 装完即可分析任意A股)
  完整层   --full: 再装 duckdb (同花顺全市场本地库, 全市场扫描用)
用法:
  python setup_env.py              # 只自检, 报告缺什么
  python setup_env.py --recommended
  python setup_env.py --full
  python setup_env.py --set-key    # 本地录入同花顺数据钥匙(输入不回显, 不经过AI对话)
pip 自动走清华镜像, 国内外网络都能装。
"""
import importlib.util
import os
import json
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIRROR = ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]


def has(mod):
    return importlib.util.find_spec(mod) is not None


def pip_install(*pkgs):
    cmd = [sys.executable, "-m", "pip", "install", "-q", *pkgs, *MIRROR]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # 镜像失败退回官方源再试一次
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs],
                           capture_output=True, text=True)
    return r.returncode == 0, (r.stderr or "")[-300:]


def cred_path():
    base = os.environ.get("APPDATA") or os.path.expanduser("~/.config")
    return os.path.join(base, "hithink-finance", "credentials.env")


def _dpapi_protect(data):
    """Windows 用户级 DPAPI 加密(仅本机本用户可解), 纯 ctypes 零依赖"""
    import base64
    import ctypes
    import ctypes.wintypes as wt

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    buf = ctypes.create_string_buffer(data, len(data))
    bin_ = BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    bout = BLOB()
    if not ctypes.windll.crypt32.CryptProtectData(
            ctypes.byref(bin_), None, None, None, None, 0, ctypes.byref(bout)):
        raise OSError("DPAPI 加密失败")
    try:
        return base64.b64encode(ctypes.string_at(bout.pbData, bout.cbData)).decode()
    finally:
        ctypes.windll.kernel32.LocalFree(bout.pbData)


def set_key():
    """钥匙只在本地终端录入并落本地文件, 绝不经过AI对话记录"""
    if sys.stdin.isatty():
        import getpass
        key = getpass.getpass("粘贴你的同花顺数据钥匙(以 sk-fuyao- 开头, 输入不显示), 回车确认: ").strip()
    else:
        key = sys.stdin.readline().strip()
    if not key.startswith("sk-"):
        print(json.dumps({"error": "格式不像有效钥匙(应以 sk- 开头), 未保存"}, ensure_ascii=False))
        sys.exit(1)
    p = cred_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.name == "nt":
        line = "HITHINK_FINANCE_API_KEY_DPAPI=" + _dpapi_protect(key.encode()) + "\n"
        how = "DPAPI 加密(仅本机本用户可解)"
    else:
        line = "HITHINK_FINANCE_API_KEY=" + key + "\n"
        how = "文件权限600"
    with open(p, "w", encoding="utf-8") as f:
        f.write(line)
    if os.name != "nt":
        os.chmod(p, 0o600)
    print(json.dumps({"saved": p, "protection": how,
                      "message": "钥匙已存本机, 之后取数自动使用官方源"}, ensure_ascii=False))


def main():
    if "--set-key" in sys.argv:
        set_key()
        return
    report = {"python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"}

    if sys.version_info < (3, 11):
        report["status"] = "python_too_old"
        report["message"] = ("本机 Python 版本是 " + report["python"] +
                             "，缠论引擎需要 3.11 或更新。对你的 AI 助手说：帮我安装 Python 3.11，它会带你装好。")
        print(json.dumps(report, ensure_ascii=False))
        sys.exit(1)

    report["core"] = "就绪(引擎已随技能打包, 无需安装)"
    report["akshare"] = "已装" if has("akshare") else "未装(免费行情源, 推荐)"
    report["duckdb"] = "已装" if has("duckdb") else "未装(仅全市场扫描需要, 可不装)"

    want = []
    if "--recommended" in sys.argv or "--full" in sys.argv:
        if not has("akshare"):
            want.append("akshare")
    if "--full" in sys.argv and not has("duckdb"):
        want.append("duckdb==1.3.2")

    for pkg in want:
        ok, err = pip_install(pkg)
        key = pkg.split("==")[0]
        report[key] = "安装成功" if ok else f"安装失败: {err}"
        if not ok:
            report["message"] = f"{key} 没装上，把这条结果原样发给你的 AI 助手，它会处理。"

    report.setdefault("status", "ok")
    if report["status"] == "ok" and not want:
        report["message"] = "环境就绪。" + ("" if has("akshare") else
                            "想直接分析A股行情, 跑: python setup_env.py --recommended")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
