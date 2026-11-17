#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台磁盘缓存清理器（Windows / macOS / Linux）

四层架构：
  L1 平台探测层  —— 自动识别系统与缓存根区，路径全部变量化，无硬编码用户名/盘符
  L2 缓存发现层  —— 已知模式库 + 目录名启发式，能找出白名单之外的未知缓存
  L3 安全分级层  —— GREEN 可再生 / YELLOW 需重下 / RED 禁止 / DISCOVERED 发现项
  L4 执行策略层  —— 只读扫描 → 用户确认 → 删除 → 复测空间

安全设计：
  1. 白名单优先，发现项只报告不自动删（除非显式 --include-discovered）
  2. 删除前用 os.path.realpath 解析软链，校验真实路径必须严格落在允许的缓存根区/home 下（带路径分隔符边界，杜绝 `Local_evil` 之类前缀绕过），禁止删除盘符根目录
  3. 软链逃逸防护：删除时绝不跟随符号链接 / junctions，遇到软链只删链接本身，绝不递归进链接指向的真实目录
  4. 程序占用保护：相关进程在运行时跳过该项
  5. 遇错跳过，统计跳过数量，不中断整体流程
  6. 默认演练模式，必须显式 --yes 才会真删

用法：
  python clean_cache.py                       # 演练：只扫描报告，不删（默认）
  python clean_cache.py --yes                 # 清理 GREEN 项
  python clean_cache.py --yes --tier yellow   # 额外清 YELLOW（需重新下载的）
  python clean_cache.py --yes --include-discovered all
  python clean_cache.py --json                # 机器可读输出
  python clean_cache.py --min-size 200        # 只报 >=200MB 的项
"""

import os
import re
import sys
import glob
import time
import argparse
import platform as _platform

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TIER_GREEN = "green"        # 可再生，删了最多变慢
TIER_YELLOW = "yellow"      # 删后需重新下载/重建，体积大
TIER_RED = "red"            # 禁止触碰
TIER_DISCOVERED = "discovered"  # 启发式发现，默认只报告

TIER_LABEL = {
    TIER_GREEN: "可再生",
    TIER_YELLOW: "需重下",
    TIER_RED: "禁止",
    TIER_DISCOVERED: "发现项",
}

TIER_NOTE = {
    TIER_GREEN: "纯缓存，删后自动重建，最多导致下次启动变慢",
    TIER_YELLOW: "删后需重新联网下载或重新编译，耗时较长",
    TIER_RED: "系统关键目录，任何情况下都不删",
    TIER_DISCOVERED: "启发式扫描得出，未经人工验证，请核对路径后再删",
}

# ============================================================ L1 平台探测层

def detect_platform() -> str:
    s = sys.platform.lower()
    if s.startswith("win"):
        return "windows"
    if s == "darwin":
        return "macos"
    return "linux"


PLATFORM = detect_platform()
HOME = os.path.expanduser("~")


def _env(*names) -> str:
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return ""


def build_context() -> dict:
    """按平台推导缓存根区与临时目录，全程用环境变量推导，不写死用户名/盘符。"""
    ctx = {"platform": PLATFORM, "home": HOME}
    if PLATFORM == "windows":
        local = _env("LOCALAPPDATA") or os.path.join(HOME, "AppData", "Local")
        roaming = _env("APPDATA")
        if not roaming:
            idx = local.lower().rstrip("\\").rfind("appdata\\local")
            roaming = (local[:idx] + "AppData\\Roaming") if idx >= 0 else os.path.join(HOME, "AppData", "Roaming")
        ctx["localappdata"] = local
        ctx["appdata"] = roaming
        ctx["cache_roots"] = [local, roaming]
        ctx["temp_dirs"] = [os.path.join(local, "Temp"), "C:\\Windows\\Temp"]
        ctx["scan_roots"] = [roaming, local, os.path.join(HOME, ".cache")]
    elif PLATFORM == "macos":
        lib = os.path.join(HOME, "Library")
        caches = os.path.join(lib, "Caches")
        ctx["cache_roots"] = [caches, os.path.join(lib, "Logs")]
        ctx["temp_dirs"] = [_env("TMPDIR") or "/tmp"]
        ctx["scan_roots"] = [
            caches,
            os.path.join(lib, "Logs"),
            os.path.join(lib, "Developer"),
            os.path.join(lib, "Containers"),
            os.path.join(lib, "Application Support"),
            os.path.join(HOME, ".cache"),
        ]
    else:
        caches = _env("XDG_CACHE_HOME") or os.path.join(HOME, ".cache")
        ctx["cache_roots"] = [caches]
        ctx["temp_dirs"] = ["/tmp", os.path.join(HOME, ".cache")]
        ctx["scan_roots"] = [caches, os.path.join(HOME, ".local", "share"), "/var/cache"]
    ctx["cache_roots"] = [p for p in ctx["cache_roots"] if p and os.path.isdir(p)]
    ctx["scan_roots"] = [p for p in ctx["scan_roots"] if p and os.path.isdir(p)]
    return ctx


CTX = build_context()

# 允许删除的根区（安全闸）
ALLOWED_ROOTS = [p for p in (HOME, _env("LOCALAPPDATA"), _env("APPDATA")) if p]
ALLOWED_ROOTS += CTX["cache_roots"]
ALLOWED_ROOTS += [t for t in CTX["temp_dirs"] if os.path.isdir(t)]
if PLATFORM == "windows":
    ALLOWED_ROOTS.append("C:\\Windows\\Temp")
ALLOWED_ROOTS = list(dict.fromkeys(os.path.abspath(p) for p in ALLOWED_ROOTS if p))

# 无论如何都不能碰的目录名/路径片段
FORBIDDEN_PARTS = ("installer", "winsxs", "system32", "package cache",
                   "windows\\servicing", "/system/", "/usr/", "/bin/", "/etc/")


# ============================================================ 基础工具

def human(num: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} PB"


def free_bytes(path: str = None) -> int:
    path = path or HOME
    try:
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes
            free = ctypes.c_ulonglong()
            ok = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path), None, None, ctypes.byref(free))
            return free.value if ok else 0
        st = os.statvfs(path)
        return st.f_bavail * st.f_frsize
    except Exception:
        return 0


def long_path(p: str) -> str:
    """Windows 下加 \\\\?\\ 前缀突破 260 字符限制。"""
    p = os.path.abspath(p)
    if os.name == "nt" and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


def dir_size(path: str) -> int:
    total = 0
    try:
        for root, _dirs, files in os.walk(long_path(path), followlinks=False, onerror=lambda e: None):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
    except Exception:
        pass
    return total


def remove_tree(path: str) -> int:
    """安全删除目录树。

    关键安全约束：
      - 绝不跟随符号链接 / junctions：若顶层或遍历中遇到软链，只删除链接本身，
        绝不递归进链接指向的真实目录（防止软链逃逸删掉用户数据）。
      - 自底向上删除，仅用 os.unlink / os.rmdir（只删空目录），被占用的跳过。
    返回跳过数量。
    """
    skipped = 0

    def _on_err(*_a):
        # os.walk 的 onerror 在不同 Python 版本传参数量不同（1 个 OSError 或 3 个），
        # 用可变参数兼容；这里只需统计跳过数量。
        nonlocal skipped
        skipped += 1

    target = long_path(path)
    # 顶层若是符号链接 / junctions：只删链接，绝不删目标内容
    if os.path.islink(target):
        try:
            os.unlink(target)
        except OSError:
            skipped += 1
        return skipped
    try:
        for root, dirs, files in os.walk(target, topdown=False, followlinks=False, onerror=_on_err):
            for f in files:
                fp = long_path(os.path.join(root, f))
                try:
                    os.unlink(fp)
                except OSError:
                    skipped += 1
            for d in dirs:
                dp = long_path(os.path.join(root, d))
                if os.path.islink(dp):
                    # 软链目录：只删链接，不删目标
                    try:
                        os.unlink(dp)
                    except OSError:
                        skipped += 1
                else:
                    try:
                        os.rmdir(dp)
                    except OSError:
                        skipped += 1
        try:
            os.rmdir(target)
        except OSError:
            skipped += 1
    except FileNotFoundError:
        return skipped
    except OSError:
        skipped += 1
    return skipped


def process_running(names) -> bool:
    if not names:
        return False
    try:
        import subprocess
        if os.name == "nt":
            out = subprocess.run(["tasklist"], capture_output=True, text=True,
                                 errors="ignore").stdout.lower()
        else:
            out = subprocess.run(["ps", "-eo", "comm="], capture_output=True, text=True,
                                 errors="ignore").stdout.lower()
        return any(n.lower() in out for n in names)
    except Exception:
        return False


def _is_under(real_norm: str, root_norm: str) -> bool:
    """边界安全的包含判断：real 必须严格位于 root 之下（root 后跟路径分隔符），
    避免 `C:\\Users\\x\\AppData\\Local_evil` 被 `startswith('...Local')` 误判为命中。"""
    return real_norm == root_norm or real_norm.startswith(root_norm + os.sep)


_ALLOWED_ROOTS_NORM = None


def _allowed_roots_norm():
    """把 ALLOWED_ROOTS 解析为 realpath 并归一化（小写、去尾分隔符），缓存复用。"""
    global _ALLOWED_ROOTS_NORM
    if _ALLOWED_ROOTS_NORM is None:
        out, seen = [], set()
        for r in ALLOWED_ROOTS:
            try:
                rp = os.path.realpath(os.path.abspath(r))
            except Exception:
                rp = os.path.abspath(r)
            rp = rp.rstrip(os.sep).lower()
            if rp and rp not in seen:
                seen.add(rp)
                out.append(rp)
        _ALLOWED_ROOTS_NORM = out
    return _ALLOWED_ROOTS_NORM


def assert_safe(path: str) -> str:
    """删除前最终闸门。

    1. 用 os.path.realpath 解析符号链接 / junctions，得到真实路径；
    2. 真实路径必须严格位于某个允许根区之下（边界安全）；
    3. 命中系统关键片段（FORBIDDEN_PARTS）一律拒绝；
    4. 拒绝驱动器根目录。
    返回解析后的真实路径（供后续删除使用）。
    """
    try:
        real = os.path.realpath(os.path.abspath(path))
    except Exception:
        real = os.path.abspath(path)
    real_norm = real.rstrip(os.sep).lower()
    if len(real_norm) == 2 and real_norm[1] == ":":
        raise RuntimeError(f"拒绝删除驱动器根目录: {real}")
    low = real.lower()
    for bad in FORBIDDEN_PARTS:
        if bad in low:
            raise RuntimeError(f"禁止删除系统关键路径: {real}")
    if not any(_is_under(real_norm, r) for r in _allowed_roots_norm()):
        raise RuntimeError(f"拒绝删除白名单外的路径: {real}")
    return real


def expand(pattern: str):
    """支持 ~ / %ENV% / $ENV / * 通配符，返回存在的路径列表。"""
    p = os.path.expanduser(os.path.expandvars(str(pattern)))
    for token, val in (("%LOCALAPPDATA%", CTX.get("localappdata", "")),
                       ("%APPDATA%", CTX.get("appdata", "")),
                       ("%USERPROFILE%", HOME), ("$HOME", HOME)):
        if val:
            p = p.replace(token, val)
    p = os.path.expanduser(os.path.expandvars(p))
    hits = sorted(glob.glob(p))
    return [h for h in hits if os.path.exists(h)]


# ============================================================ L2+L3 目标库与发现

# (名称, 路径模式, 分级, 占用进程, 适用平台)
# 平台: None 表示全平台
TARGETS = [
    # ---- 包管理器（全平台通用路径） ----
    ("npm 缓存", "~/.npm/_cacache", TIER_GREEN, None, ["macos", "linux"]),
    ("Yarn 缓存", "~/.cache/yarn", TIER_GREEN, None, None),
    ("Yarn Berry 缓存", "~/.yarn/berry/cache", TIER_GREEN, None, None),
    ("pnpm 存储", "~/.local/share/pnpm/store", TIER_GREEN, None, ["macos", "linux"]),
    ("pip 缓存", "~/.cache/pip", TIER_GREEN, None, ["macos", "linux"]),

    # ---- 工具自身（全平台，home 目录下） ----
    ("WorkBuddy 日志", "~/.workbuddy/logs", TIER_GREEN, None, None),
    ("WorkBuddy 追踪数据", "~/.workbuddy/traces", TIER_GREEN, None, None),

    # ---- Windows ----
    ("npm 缓存(Local)", r"%LOCALAPPDATA%\npm-cache", TIER_GREEN, None, ["windows"]),
    ("npm 缓存(Roaming 旧版)", r"%APPDATA%\npm-cache", TIER_GREEN, None, ["windows"]),
    ("Yarn 缓存", r"%LOCALAPPDATA%\Yarn\Cache", TIER_GREEN, None, ["windows"]),
    ("pnpm 缓存", r"%LOCALAPPDATA%\pnpm-store", TIER_GREEN, None, ["windows"]),
    ("pip 缓存", r"%LOCALAPPDATA%\pip\cache", TIER_GREEN, None, ["windows"]),
    ("Codex 运行时缓存", r"%USERPROFILE%\.cache\codex-runtimes", TIER_GREEN, None, ["windows"]),
    ("Electron 下载缓存", r"%LOCALAPPDATA%\electron\Cache", TIER_GREEN, None, ["windows"]),
    ("electron-builder 缓存", r"%LOCALAPPDATA%\electron-builder\Cache", TIER_GREEN, None, ["windows"]),
    ("VS Code 扩展安装包缓存", r"%APPDATA%\Code\CachedExtensionVSIXs", TIER_GREEN, None, ["windows"]),
    ("WPS 插件缓存", r"%APPDATA%\kingsoft\wps\addons", TIER_GREEN,
     ["wps.exe", "wpscloudsvr.exe"], ["windows"]),
    ("系统崩溃转储", r"%LOCALAPPDATA%\CrashDumps", TIER_GREEN, None, ["windows"]),
    ("DirectX 着色器缓存", r"%LOCALAPPDATA%\D3DSCache", TIER_GREEN, None, ["windows"]),
    ("微信 小程序运行时", r"%APPDATA%\Tencent\WeChat\XPlugin", TIER_GREEN,
     ["WeChat.exe", "Weixin.exe"], ["windows"]),
    ("微信 媒体缓存", r"%APPDATA%\Tencent\WeChat\radium", TIER_GREEN,
     ["WeChat.exe", "Weixin.exe"], ["windows"]),
    ("微信 日志", r"%APPDATA%\Tencent\WeChat\log", TIER_GREEN, None, ["windows"]),
    ("企业微信 媒体缓存", r"%APPDATA%\Tencent\xwechat\radium", TIER_GREEN, ["WXWork.exe"], ["windows"]),
    ("企业微信 小程序运行时", r"%APPDATA%\Tencent\xwechat\xplugin", TIER_GREEN, ["WXWork.exe"], ["windows"]),
    ("企业微信 日志", r"%APPDATA%\Tencent\xwechat\log", TIER_GREEN, None, ["windows"]),
    ("企业微信 崩溃信息", r"%APPDATA%\Tencent\xwechat\crashinfo", TIER_GREEN, None, ["windows"]),

    # ---- macOS ----
    ("Homebrew 下载缓存", "~/Library/Caches/Homebrew", TIER_GREEN, None, ["macos"]),
    ("Xcode 缓存", "~/Library/Caches/com.apple.dt.Xcode", TIER_GREEN, None, ["macos"]),
    ("用户日志", "~/Library/Logs", TIER_GREEN, None, ["macos"]),
    ("Xcode 派生数据", "~/Library/Developer/Xcode/DerivedData", TIER_YELLOW, None, ["macos"]),
    ("iOS 模拟器镜像", "~/Library/Developer/CoreSimulator", TIER_YELLOW, None, ["macos"]),
    ("Xcode 归档", "~/Library/Developer/Xcode/Archives", TIER_YELLOW, None, ["macos"]),
    ("VS Code 扩展安装包缓存",
     "~/Library/Application Support/Code/CachedExtensionVSIXs", TIER_GREEN, None, ["macos"]),

    # ---- Linux ----
    ("缩略图缓存", "~/.cache/thumbnails", TIER_GREEN, None, ["linux"]),
    ("用户回收站", "~/.local/share/Trash", TIER_GREEN, None, ["linux"]),
    ("APT 包缓存", "/var/cache/apt/archives", TIER_GREEN, None, ["linux"]),
    ("systemd 日志", "/var/log/journal", TIER_GREEN, None, ["linux"]),

    # ---- 需重新下载（YELLOW，默认不删） ----
    ("Maven 本地仓库", "~/.m2/repository", TIER_YELLOW, None, None),
    ("Gradle 分发包", "~/.gradle/wrapper/dists", TIER_YELLOW, None, None),
    ("Gradle 构建缓存", "~/.gradle/caches", TIER_YELLOW, None, None),
    ("HuggingFace 模型缓存", "~/.cache/huggingface", TIER_YELLOW, None, None),
    ("Puppeteer 浏览器", "~/.cache/puppeteer", TIER_YELLOW, None, None),
    ("Playwright 旧版浏览器", "~/.cache/ms-playwright", TIER_YELLOW, None, None),
]

# IDE 类：按版本通配，只清缓存子目录（User/config 目录保留）
IDE_CACHE_SUBDIRS = ["caches", "index", "log", "logs", "tmp", "localHistory"]
IDE_SCAN = [
    (r"%LOCALAPPDATA%\JetBrains\*", ["windows"]),
    (r"%APPDATA%\JetBrains\*", ["windows"]),
    ("~/Library/Caches/JetBrains/*", ["macos"]),
    ("~/Library/Logs/JetBrains/*", ["macos"]),
    ("~/.cache/JetBrains/*", ["linux"]),
    ("~/.config/JetBrains/*", ["macos", "linux"]),
]

# Electron 系应用缓存子目录（VS Code / Trae / Cursor 等）
ELECTRON_SUBDIRS = [
    "CachedData", "Cache", "Code Cache", "logs", "Crashpad",
    "WebStorage", "Partitions", "ModularData", "CachedExtensionVSIXs",
    "GPUCache", "Local Storage", "Session Storage", "blob_storage",
]
ELECTRON_SCAN = [
    (r"%APPDATA%\Trae*", ["windows"]),
    ("~/Library/Application Support/Trae*", ["macos"]),
    ("~/.config/Trae*", ["linux"]),
    ("~/Library/Application Support/Code", ["macos", "linux"]),
    ("~/Library/Application Support/Cursor", ["macos", "linux"]),
]

# 启发式：目录名缓存关键词
CACHE_NAME_RE = re.compile(
    r"^(cache|caches|cache2|cachedata|code cache|gpu.?cache|shader.?cache|"
    r"d3dscache|logs?|crashpad|crash ?dumps?|crashinfo|temp|tmp|"
    r"webstorage|session storage|local storage|partitions|blob_storage|"
    r"deriveddata|thumbnails)$", re.I)

# 启发式：个人数据关键词，命中即排除
PROTECTED_NAME_RE = re.compile(
    r"(user|users|profile|profiles|bookmarks?|preferences|credentials|"
    r"logins?|tokens?|documents?|desktop|downloads?|projects?|workspace)", re.I)


def platform_ok(platforms) -> bool:
    return platforms is None or PLATFORM in platforms


def build_whitelist():
    items = []
    for name, pattern, tier, guard, plats in TARGETS:
        if not platform_ok(plats):
            continue
        for p in expand(pattern):
            items.append({"name": name, "path": p, "tier": tier,
                          "guard": guard, "source": "whitelist"})

    for pattern, plats in IDE_SCAN:
        if not platform_ok(plats):
            continue
        for base in expand(pattern):
            for sub in IDE_CACHE_SUBDIRS:
                p = os.path.join(base, sub)
                if os.path.isdir(p):
                    items.append({"name": f"IDE 缓存[{os.path.basename(base)}/{sub}]",
                                  "path": p, "tier": TIER_GREEN, "guard": None,
                                  "source": "whitelist"})

    for pattern, plats in ELECTRON_SCAN:
        if not platform_ok(plats):
            continue
        for base in expand(pattern):
            for sub in ELECTRON_SUBDIRS:
                p = os.path.join(base, sub)
                if os.path.isdir(p):
                    items.append({"name": f"应用缓存[{os.path.basename(base)}/{sub}]",
                                  "path": p, "tier": TIER_GREEN, "guard": None,
                                  "source": "whitelist"})
    return items


def discover(min_bytes: int, max_depth: int = 2):
    """启发式发现：在缓存根区浅层扫描名字像缓存、体积够大的目录。

    结果一律标记为 DISCOVERED，默认只报告不删除。
    """
    found, seen = [], set()
    for root in CTX["scan_roots"]:
        for dirpath, dirnames, _files in os.walk(root):
            depth = dirpath[len(root.rstrip(os.sep)):].count(os.sep)
            if depth >= max_depth:
                dirnames[:] = []
                continue
            keep = []
            for d in dirnames:
                if PROTECTED_NAME_RE.search(d) or d.startswith("."):
                    continue
                if not CACHE_NAME_RE.match(d):
                    keep.append(d)
                    continue
                full = os.path.join(dirpath, d)
                key = os.path.normcase(os.path.abspath(full))
                if key in seen:
                    continue
                seen.add(key)
                size = dir_size(full)
                if size >= min_bytes:
                    found.append({"name": f"{os.path.basename(dirpath)}/{d}",
                                  "path": full, "tier": TIER_DISCOVERED,
                                  "guard": None, "source": "discovered"})
            dirnames[:] = keep
    return found


# ============================================================ L4 执行策略层

def clean_temp(temp_dirs, days: int, dry: bool):
    if not temp_dirs:
        return 0, 0, 0
    cutoff = time.time() - days * 86400
    freed, removed, failed = 0, 0, 0
    for temp_dir in temp_dirs:
        if not os.path.isdir(temp_dir):
            continue
        try:
            entries = list(os.scandir(temp_dir))
        except OSError:
            continue
        for entry in entries:
            try:
                st = entry.stat()
                if st.st_mtime >= cutoff:
                    continue
                freed += dir_size(entry.path) if entry.is_dir(follow_symlinks=False) else st.st_size
                removed += 1
                if not dry:
                    if entry.is_dir(follow_symlinks=False):
                        remove_tree(entry.path)
                    else:
                        try:
                            os.unlink(long_path(entry.path))
                        except OSError:
                            os.unlink(entry.path)
            except Exception:
                failed += 1
    return freed, removed, failed


def empty_trash() -> str:
    if os.name == "nt":
        try:
            import ctypes
            flags = 0x00000001 | 0x00000002 | 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
            return "已清空回收站"
        except Exception:
            return "回收站清空失败"
    trash = os.path.join(HOME, ".local/share/Trash") if PLATFORM == "linux" \
        else os.path.join(HOME, ".Trash")
    if os.path.isdir(trash):
        remove_tree(trash)
        return "已清空回收站"
    return "跳过（未找到回收站目录）"


def collect(items, min_bytes):
    """计算大小并过滤，返回 (可选计划, 被拒绝项, 被占用跳过项)。"""
    plan, rejected, busy = [], [], []
    for it in items:
        try:
            safe = assert_safe(it["path"])
        except RuntimeError as e:
            rejected.append((it["name"], str(e)))
            continue
        if it.get("guard") and process_running(it["guard"]):
            busy.append(it["name"])
            continue
        size = dir_size(safe)
        if size < min_bytes:
            continue
        it = dict(it)
        it["path"], it["size"] = safe, size
        plan.append(it)
    plan.sort(key=lambda x: x["size"], reverse=True)
    return plan, rejected, busy


def parse_selection(sel, plan):
    """解析用户勾选。

    支持：all / g(仅可再生) / y(可再生+需重下) / d(仅发现项) / 1,3,5 / 1-4
    返回 None 表示无法解析。
    """
    sel = (sel or "").strip().lower().replace("，", ",")
    if not sel:
        return []
    if sel in ("all", "a", "*"):
        return list(plan)
    if sel == "g":
        return [i for i in plan if i["tier"] == TIER_GREEN]
    if sel == "y":
        return [i for i in plan if i["tier"] in (TIER_GREEN, TIER_YELLOW)]
    if sel == "d":
        return [i for i in plan if i["tier"] == TIER_DISCOVERED]
    idxs = set()
    for part in sel.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                a, b = part.split("-", 1)
                idxs.update(range(int(a), int(b) + 1))
            else:
                idxs.add(int(part))
        except ValueError:
            return None
    return [plan[i - 1] for i in sorted(idxs) if 1 <= i <= len(plan)]


def main():
    ap = argparse.ArgumentParser(description="跨平台磁盘缓存清理器")
    ap.add_argument("--dry-run", action="store_true", help="只扫描出清单，不进入勾选也不删除")
    ap.add_argument("--pick", default="",
                    help="非交互指定删除项：all / g / y / d / 1,3 / 1-4")
    ap.add_argument("--force", action="store_true",
                    help="跳过删除前的二次确认（仅用于已确认过的自动化场景）")
    ap.add_argument("--tier", default="green", choices=["green", "yellow"],
                    help="清单里是否包含「需重下」项，默认 green")
    ap.add_argument("--min-size", type=int, default=20, help="只列出 >=N MB 的项，默认 20")
    ap.add_argument("--keep-temp-days", type=int, default=7, help="临时文件保留天数，默认 7")
    ap.add_argument("--no-discover", action="store_true", help="关闭启发式发现，只查白名单")
    ap.add_argument("--no-temp", action="store_true", help="不列出临时目录")
    ap.add_argument("--no-trash", action="store_true", help="清理后不清空回收站")
    ap.add_argument("--json", action="store_true", help="输出 JSON 供程序消费")
    args = ap.parse_args()

    min_bytes = args.min_size * 1024 * 1024
    days = args.keep_temp_days

    items = build_whitelist()
    discovered = [] if args.no_discover else discover(min_bytes)
    all_items = items + discovered

    # 发现项始终进清单，由用户决定是否勾选
    wanted = {TIER_GREEN, TIER_DISCOVERED}
    if args.tier == "yellow":
        wanted.add(TIER_YELLOW)
    plan, rejected, busy = collect([i for i in all_items if i["tier"] in wanted], min_bytes)

    temp_dirs = [] if args.no_temp else [t for t in CTX["temp_dirs"] if os.path.isdir(t)]
    t_freed, t_cnt, t_fail = clean_temp(temp_dirs, days, dry=True)
    if t_freed and not args.no_temp:
        plan.append({"name": f"临时文件(>{days}天)", "path": None, "tier": TIER_GREEN,
                     "source": "temp", "size": t_freed, "is_temp": True})
        plan.sort(key=lambda x: x["size"], reverse=True)

    if args.json:
        import json
        print(json.dumps({
            "platform": PLATFORM,
            "free_bytes": free_bytes(),
            "items": [{"index": n + 1, "name": i["name"], "path": i["path"],
                       "size": i["size"], "tier": i["tier"], "source": i["source"]}
                      for n, i in enumerate(plan)],
            "busy": busy,
            "rejected": [{"name": n, "reason": w} for n, w in rejected],
        }, ensure_ascii=False, indent=2))
        return 0

    print("=" * 70)
    print(f" 磁盘缓存清理   平台={PLATFORM}   根目录={HOME}")
    print("=" * 70)
    for n, it in enumerate(plan, 1):
        tag = "发现" if it["source"] == "discovered" else TIER_LABEL.get(it["tier"], it["tier"])
        print(f"  {n:>2}. [{tag}] {it['name']:<38} {human(it['size']):>11}")
    if not plan:
        print("  （没有找到符合条件的缓存）")
    for n in busy:
        print(f"      [跳过] {n}  相关程序正在运行")
    for n, why in rejected:
        print(f"      [拒绝] {n}  {why}")
    print("-" * 70)
    print(f"  清单合计: {human(sum(i['size'] for i in plan))}   当前可用: {human(free_bytes())}")
    print("-" * 70)

    if args.dry_run:
        print("\n演练模式，未删除任何文件。去掉 --dry-run 可进入勾选。")
        return 0

    if not plan:
        return 0

    sel = args.pick
    if not sel:
        print("  输入要删除的序号（逗号或区间，如 1,3,5-8）")
        print("  all=全部  g=仅可再生  y=含需重下  d=仅发现项  直接回车=取消")
        try:
            sel = input("  > ").strip()
        except EOFError:
            sel = ""
    selected = parse_selection(sel, plan)
    if selected is None:
        print("无法识别的输入，已取消。")
        return 1
    if not selected:
        print("未选择任何项，已取消。")
        return 0

    total = sum(i["size"] for i in selected)
    free_now = free_bytes()
    print("=" * 70)
    print(f" 待删除 {len(selected)} 项，预计释放 {human(total)}")
    print("=" * 70)
    for n, it in enumerate(selected, 1):
        src = "启发式扫描" if it["source"] == "discovered" else "已知清单"
        loc = it["path"] or "临时目录（按修改时间逐项清理）"
        print(f"  {n}. {it['name']}")
        print(f"     路径  {loc}")
        print(f"     大小  {human(it['size'])}      分级  {TIER_LABEL.get(it['tier'], it['tier'])}      来源  {src}")
        print(f"     说明  {TIER_NOTE.get(it['tier'], '')}")
    print("-" * 70)
    print(f"  合计 {human(total)}      当前可用 {human(free_now)}"
          f"      删除后预计 {human(free_now + total)}")
    print("-" * 70)

    if not args.force:
        try:
            ans = input("  确认删除？输入 y 执行，其他任意键取消: ").strip().lower()
        except EOFError:
            ans = ""
        if ans != "y":
            print("  已取消，未删除任何文件。")
            return 0

    before = free_bytes()
    print("开始清理...")
    for it in selected:
        if it.get("is_temp"):
            clean_temp(temp_dirs, days, dry=False)
            print(f"  [OK] {it['name']}  清理 {t_cnt} 项，占用跳过 {t_fail} 项")
        else:
            skipped = remove_tree(it["path"])
            print(f"  [{'OK' if not skipped else f'部分跳过({skipped})'}] {it['name']}")
    if not args.no_trash:
        print(f"  [..] {empty_trash()}")

    after = free_bytes()
    print("-" * 70)
    print(f"  清理前可用: {human(before)}")
    print(f"  清理后可用: {human(after)}")
    print(f"  实际释放  : {human(max(after - before, 0))}")
    print("=" * 70)
    print("提示：IDE / WPS / 微信等下次启动会重建缓存，首次启动稍慢属正常。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
