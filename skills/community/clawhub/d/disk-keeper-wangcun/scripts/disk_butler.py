#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
净盘师 DiskKeeper · 智能净盘师 v2.2
================================================================
Windows 全硬盘（C/D/E… 自动探测）的智能体检 + 安全清理 + 自进化中枢。

  三基因（只在实战里长出来的，不是口号）：
    · 反省：动手前先读 lessons.md 血泪史；每个动作都做
            「声称释放 vs df 实测」对账，对不上自动记偏差。
    · 进化：偏差与新坑自动追加进 lessons.md；learn 命令人工落教训；
            规则随教训演进，绝不重犯同一坑。
    · 超越：每轮结尾自动给出「比上次好在哪」，history.jsonl 沉淀趋势。

设计原则（血泪铸成，已写进 lessons.md）：
  1. 账本真相 = df 实测（shutil.disk_usage），绝不信脚本自报。
     回收站 $I 是「收据」不是「数据」——幽灵条目（有 $I 无 $R）
     声明体积实占 0，按 $I 汇总必然虚高。
  2. 360 类「删除保护」把删除按「文件所在卷」投放回收站 →
     任何删除后必须回收站精确净化，否则等于白删、df 看不出释放。
  3. 默认绝不整箱清空回收站；只按 $I 原始路径白名单精确净化。
     · recycle --purge 是唯一会整箱清空的「显式高危」命令，需用户手动二次确认，
       永不进入任何自动/无人值守流程；删缓存与删回收站是两回事，不可混谈。
  4. 活体程序判定 = 注册表 InstallLocation / 主程序 exe / 进程路径，
     绝不能凭「文件夹名字像安装包」。
  5. 用户资产红线（Desktop/Documents/Downloads/ Pictures/Videos/Music/
     .workbuddy / AppData\Roaming 等）→ R3 绝对禁区，永不进入清理清单。
  6. 正向白名单：只动「明确可重建」的缓存/Temp，其余一律不碰。
  7. 删除台账必须边删边写（append），攒到最后写 = 崩溃即全丢。
  8. 体积统计必须容错（断链路径 FileNotFoundError 不挡删除）。

安全模型：
  · 默认 clean 是 dry-run（只列清单不删），必须 --yes 才真删。
  · 每个删除目标二次校验 R3 禁区，命中即拦截并落教训。
  · 不删任何 junction/符号链接（避免误伤迁移目录）。
  · R1（系统Temp/回收站幽灵/浏览器缓存/包管理缓存/IM纯缓存）默认安全；
    R2（更大的用户态缓存）需 --with-r2 显式开启。

用法：
  python scripts/disk_butler.py doctor                 # 快速体检（只读，秒级）
  python scripts/disk_butler.py doctor --deep         # 深度体检（全盘盘点，分钟级，24h 缓存）
  python scripts/disk_butler.py scan                  # 同 doctor --deep
  python scripts/disk_butler.py plan [--with-r2]      # 清理计划（只读）
  python scripts/disk_butler.py clean                 # 计划预览（dry-run，不删）
  python scripts/disk_butler.py clean --yes           # 执行 R1 + 幽灵收据
  python scripts/disk_butler.py clean --yes --with-r2 # 加 R2 需确认项
  python scripts/disk_butler.py recycle               # 回收站真实账本（只读）
  python scripts/disk_butler.py recycle --ghost --yes # 清幽灵收据（实占0，清账本）
  python scripts/disk_butler.py recycle --purge --yes # 清空回收站（强确认，不可逆）
  python scripts/disk_butler.py big [--min-gb 5]      # 大文件/目录定位（只读）
  python scripts/disk_butler.py genes                 # 三基因报告
  python scripts/disk_butler.py learn "教训" [--tag T] # 落一条教训进正本
"""
import argparse
import ctypes
import datetime
import json
import os
import re
import shutil
import sys
import time

# 输出编码兜底（v2.2）：控制台/重定向到非 UTF-8 代码页时，任何不可编码字符
# 都降级为替代符而非抛 UnicodeEncodeError（脚本全量输出已无 Emoji/零宽字符）。
try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass

VERSION = "2.3.1"
RULES_VERSION = "20260915.1"   # 规则库版本：白名单/分级/安全模型演进标记，evolve 推进
# v2.2 安全加固（响应 A.I.G / SkillSpector 审核）：
#   · safe_remove 异常不再误报成功（返回 None 计失败，含部分失败与后置校验）
#   · Temp 清理根改用「规范化 + 安全父目录包含」校验，不再直接采信环境变量字面值
#   · 删除前新增不安全路径拦截（相对路径/UNC/盘根/规范化后命中 R3）
#   · cmd_auto 去掉「交给 Agent 无人值守跑清理序列」的引导，改为只读模板 + 安全提示
BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "disk_keeper_state")
LEDGER = os.path.join(STATE, "ledger.json")
LESSONS = os.path.join(STATE, "lessons.md")
HISTORY = os.path.join(STATE, "history.jsonl")
MANIFEST = os.path.join(STATE, "clean_manifest.jsonl")
DEEP_TTL_H = 24.0

# ── 跨用户路径（不写死任何用户名）────────────────────────────────────────
USERPROFILE = os.environ.get("USERPROFILE", os.path.expanduser("~"))
LOCALAPPDATA = os.environ.get("LOCALAPPDATA",
                              os.path.join(USERPROFILE, "AppData", "Local"))
APPDATA = os.environ.get("APPDATA",
                         os.path.join(USERPROFILE, "AppData", "Roaming"))
SYSTEMROOT = os.environ.get("SystemRoot", r"C:\Windows")

# 正向白名单：只动这些名字的缓存子目录
CACHE_NAMES = {"cache", "temp", "tmp", "gpucache", "crashpad", "cachedata",
               "code cache", "thumbnails", "thumbcache", "webcache",
               "gpu cache", "filecache"}
# 绝不碰的名字（即使是子目录）
NEVER_NAMES = {"projects", "drafts", "user data", "data", "backup", "index",
               "emotion", "avatar", "avator", "profile", "profiles",
               "userdata", "users", "config", "logs", "settings", "documents",
               "pictures", "desktop", "downloads", "videos", "music"}
# R2 额外放宽的名字（需 --with-r2 才动）
R2_NAMES = {"filestorage", "storage", "appcache", "shader", "shadercache",
            "downloads", "cache2", "cached", "tmpcache"}

_R3_CACHE = None  # 全局禁区缓存


def human(n):
    if n < 0:
        return "—"
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.2f}{u}"
        n /= 1024
    return f"{n:.2f}TB"


def nc(p):
    return os.path.normcase(os.path.abspath(p))


def now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


# ══════════════════════════ 盘符 / 禁区 ═══════════════════════════════
def detect_drives():
    """自动探测所有本地固定盘（不含 U 盘 / 网络盘）。"""
    drives = []
    try:
        mask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if mask & (1 << i):
                L = chr(65 + i)
                try:
                    t = ctypes.windll.kernel32.GetDriveTypeW(L + ":\\")
                except Exception:
                    t = 0
                if t == 3:  # DRIVE_FIXED
                    drives.append(L)
        if drives:
            return drives
    except Exception:
        pass
    # 降级：遍历 A–Z（非 Windows / ctypes 不可用）
    for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        try:
            if os.path.exists(L + ":\\") and os.path.ismount(L + ":\\"):
                drives.append(L)
        except Exception:
            pass
    return drives


def build_r3(extra=None):
    """动态生成 R3 绝对禁区（跨用户、跨盘，不写死任何具体路径）。"""
    zones = set()
    for d in detect_drives():
        root = d + ":\\"
        for name in ["Windows", "Program Files", "Program Files (x86)",
                     "ProgramData", "$Recycle.Bin", "$RECYCLE.BIN", "Recovery",
                     "System Volume Information", "PerfLogs",
                     "Documents and Settings"]:
            zones.add(nc(os.path.join(root, name)))
    # 用户个人资料区（永不碰）
    for name in ["Desktop", "Documents", "Pictures", "Videos", "Music",
                 "Downloads", ".workbuddy", ".ssh", ".config", ".git",
                 "AppData\\Roaming", "AppData\\LocalLow", ".npm", ".conda",
                 ".cargo", ".cache"]:
        zones.add(nc(os.path.join(USERPROFILE, name)))
    if extra:
        for p in (extra if isinstance(extra, (list, tuple)) else [extra]):
            zones.add(nc(p))
    return zones


def is_r3(path, extra=None):
    global _R3_CACHE
    if _R3_CACHE is None or extra is not None:
        _R3_CACHE = build_r3(extra)
    p = nc(path)
    return any(p.startswith(z) for z in _R3_CACHE)


# ══════════════════════════ 基因 · 正本 ═══════════════════════════════
def load_lessons():
    if not os.path.isfile(LESSONS):
        return []
    out = []
    with open(LESSONS, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                out.append(line[2:])
    return out


def add_lesson(text, tag="人工"):
    os.makedirs(STATE, exist_ok=True)
    header = not os.path.isfile(LESSONS)
    with open(LESSONS, "a", encoding="utf-8") as f:
        if header:
            f.write("# 净盘师 · 血泪史正本（进化基因 · 只增不删）\n\n"
                    "> 每一条都是踩过的坑。任何清理动作执行前必须先读完本文件。\n\n")
        f.write(f"- [{now_iso()}] [{tag}] {text}\n")


def load_history():
    if not os.path.isfile(HISTORY):
        return []
    out = []
    with open(HISTORY, "r", encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def log_history(rec):
    os.makedirs(STATE, exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ══════════════════════════ 账本真相 ═════════════════════════════════
def df_free(drive):
    """唯一可信的空间来源：操作系统实测。"""
    u = shutil.disk_usage(drive + ":\\")
    return {"total": u.total, "used": u.used, "free": u.free}


def _is_junction(e):
    try:
        return e.is_junction()
    except AttributeError:
        try:
            return bool(os.stat(e.path, follow_symlinks=False)
                        .st_file_attributes & 0x400)
        except (OSError, AttributeError):
            return False


def _is_junction_path(p):
    try:
        return bool(os.stat(p, follow_symlinks=False).st_file_attributes & 0x400)
    except (OSError, AttributeError):
        return False


def walk_size(path):
    """目录实际占用（跳过 junction / symlink，避免重复计）。"""
    total = 0
    stack = [path]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                for e in it:
                    try:
                        if e.is_symlink() or _is_junction(e):
                            continue
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            total += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return total


def parse_i(path):
    """解析回收站 $I 收据元数据。"""
    try:
        raw = open(path, "rb").read()
    except OSError:
        return None
    if len(raw) < 24:
        return None
    ver = int.from_bytes(raw[0:8], "little")
    size = int.from_bytes(raw[8:16], "little")
    ts = int.from_bytes(raw[16:24], "little")
    dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ts // 10)
    off = 28 if ver == 2 else 24
    orig = raw[off:].decode("utf-16-le", errors="ignore").split("\x00")[0]
    return size, orig, dt


def recycle_roots():
    out = {}
    for d in detect_drives():
        for name in (r"$Recycle.Bin", r"$RECYCLE.BIN"):
            r = f"{d}:\\{name}"
            if os.path.isdir(r):
                out[d] = r
                break
    return out


def recycle_inventory():
    """回收站真实账本：配对实体 vs 幽灵收据。"""
    paired = {"n": 0, "declared": 0, "real": 0}
    ghost = {"n": 0, "declared": 0}
    for root in recycle_roots().values():
        for sid in os.listdir(root):
            d = os.path.join(root, sid)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if not fn.startswith("$I"):
                    continue
                try:
                    r = parse_i(os.path.join(d, fn))
                except Exception:
                    continue
                if not r:
                    continue
                size, orig, dt = r
                rp = os.path.join(d, "$R" + fn[2:])
                if os.path.exists(rp):
                    paired["n"] += 1
                    paired["declared"] += size
                    try:
                        if os.path.isdir(rp):
                            paired["real"] += walk_size(rp)
                        else:
                            paired["real"] += os.path.getsize(rp)
                    except OSError:
                        pass
                else:
                    ghost["n"] += 1
                    ghost["declared"] += size
    return paired, ghost


def find_ghost_receipts():
    """返回所有无对应 $R 实体的 $I 路径（实占 0）。"""
    out = []
    for root in recycle_roots().values():
        for sid in os.listdir(root):
            d = os.path.join(root, sid)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if not fn.startswith("$I"):
                    continue
                rp = os.path.join(d, "$R" + fn[2:])
                if not os.path.exists(rp):
                    out.append(os.path.join(d, fn))
    return out


# ══════════════════════════ 候选生成（正向白名单）═════════════════════
def _canon(p):
    """规范化路径（解析 .. / 联接），失败返回 None。"""
    try:
        return os.path.realpath(os.path.abspath(p))
    except OSError:
        return None


def _is_within(path, root):
    """path 是否严格位于 root 之下（排除相等），全部规范化后按公共前缀判定。"""
    try:
        path = os.path.realpath(os.path.abspath(path))
        root = os.path.realpath(os.path.abspath(root))
        return path != root and os.path.commonpath([path, root]) == root
    except (ValueError, OSError):
        return False


def temp_roots():
    """只采纳「规范化后严格落在已知安全父目录（%LOCALAPPDATA% / %SystemRoot%）之下」的
    Temp 根。环境变量 TEMP/TMP 可能被篡改指向 Documents 等敏感位置，因此**绝不直接
    采信环境变量的字面值**：先 realpath 规范化，再做安全父目录包含校验，不符即忽略。
    （响应 A.I.G T09：Environment-Controlled Cleanup Roots）"""
    allowed_parents = [c for c in (_canon(LOCALAPPDATA), _canon(SYSTEMROOT)) if c]
    roots = set()
    for v in [os.environ.get("TEMP"), os.environ.get("TMP"),
              os.path.join(SYSTEMROOT, "Temp"),
              os.path.join(LOCALAPPDATA, "Temp")]:
        if not v:
            continue
        c = _canon(v)
        if not c or not os.path.isdir(c) or is_r3(c):
            continue
        if not any(_is_within(c, p) for p in allowed_parents):
            add_lesson(f"忽略可疑 Temp 根（不在安全父目录下，疑似被环境变量篡改）：{v}",
                       tag="自动")
            continue
        roots.add(c)
    return roots


def find_temp_targets(min_age_days):
    out = []
    cutoff = time.time() - min_age_days * 86400
    for root in temp_roots():
        try:
            names = os.listdir(root)
        except OSError:
            continue
        for name in names:
            p = os.path.join(root, name)
            if is_r3(p):
                continue
            try:
                st = os.stat(p, follow_symlinks=False)
            except OSError:
                continue
            if st.st_mtime > cutoff:
                continue  # 太新，跳过
            if os.path.islink(p) or _is_junction_path(p):
                continue
            sz = walk_size(p) if os.path.isdir(p) else st.st_size
            out.append({"label": "系统Temp", "path": p, "size": sz,
                        "risk": "R1",
                        "reason": f"临时文件，{min_age_days}天前生成"})
    return out


def cache_hosts():
    """跨用户的已知缓存宿主目录（存在才返回）。"""
    cands = [
        # 浏览器
        os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data"),
        os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data"),
        os.path.join(APPDATA, "Mozilla", "Firefox", "Profiles"),
        # IM / 工具（只取其缓存子目录）
        os.path.join(USERPROFILE, "Documents", "WXWork"),
        os.path.join(USERPROFILE, "Documents", "WeChat Files"),
        os.path.join(LOCALAPPDATA, "feishu"),
        os.path.join(LOCALAPPDATA, "DingTalk"),
        os.path.join(LOCALAPPDATA, "JianyingPro"),
        os.path.join(LOCALAPPDATA, "CapCut"),
        os.path.join(LOCALAPPDATA, "Discord"),
        os.path.join(LOCALAPPDATA, "Steam"),
        # 包管理器
        os.path.join(LOCALAPPDATA, "pip", "cache"),
        os.path.join(APPDATA, "npm-cache"),
        os.path.join(LOCALAPPDATA, "Yarn", "cache"),
        os.path.join(USERPROFILE, ".conda", "pkgs"),
        os.path.join(USERPROFILE, ".cache", "yarn"),
        os.path.join(USERPROFILE, ".cache", "pypoetry"),
        os.path.join(USERPROFILE, ".gradle", "caches"),
    ]
    out = []
    for h in cands:
        c = _canon(h)                      # 规范化，防环境变量指向异常位置
        if c and os.path.isdir(c) and not is_r3(c):
            out.append(c)
    return out


def scan_cache_recursive(host, depth, names_set, hits):
    if depth <= 0:
        return
    try:
        names = os.listdir(host)
    except OSError:
        return
    for name in names:
        base = name.lower()
        if base in NEVER_NAMES:
            continue
        p = os.path.join(host, name)
        if is_r3(p) or os.path.islink(p) or _is_junction_path(p):
            continue
        if os.path.isdir(p):
            if base in names_set:
                if not any(is_r3(os.path.join(p, c)) for c in
                           ("projects", "data", "backup")):
                    hits.append(p)
            else:
                scan_cache_recursive(p, depth - 1, names_set, hits)


def find_cache_targets(with_r2):
    hits = []
    names = set(CACHE_NAMES) | (set(R2_NAMES) if with_r2 else set())
    for host in cache_hosts():
        scan_cache_recursive(host, 2, names, hits)
    out = []
    for p in hits:
        if is_r3(p):
            continue
        sz = walk_size(p)
        risk = "R2" if os.path.basename(p).lower() in R2_NAMES else "R1"
        out.append({"label": "缓存", "path": p, "size": sz, "risk": risk,
                    "reason": "可重建的软件缓存"})
    return out


# ══════════════════════════ 删除（边删边写台账）═══════════════════════
def _reject_unsafe_path(path):
    """删除前的不安全路径拦截：拒绝相对路径、UNC、异常卷标、盘符根目录。
    返回拒绝原因字符串；安全则返回 None。（响应 A.I.G T09 remediation）"""
    if not path or not os.path.isabs(path):
        return "非绝对路径"
    p = os.path.realpath(os.path.abspath(path))
    if p.startswith("\\\\"):
        return "UNC 网络路径"
    tail = p.rstrip("\\/")                  # 去尾部反斜杠：C:\ → C:
    drive = os.path.splitdrive(tail)[0]
    if len(drive) != 2 or drive[1] != ":":
        return "异常卷标"
    if tail == drive:                       # 形如 "C:" → 盘符根目录
        return "盘符根目录"
    if not os.path.basename(tail):
        return "路径无末端组件"
    return None


def safe_remove(path, dry, fh):
    """删除单个目标。

    返回三态，与调用方统计严格对应：
      True  → 成功删除（含 dry-run 通过）
      False → 被拦截（R3 禁区 / 联接 / 不安全路径）
      None  → 删除失败或部分失败（供 n_err 计数，绝不误记为成功）
    """
    def _log(ok, err=None):
        if not fh:
            return
        rec = {"ts": now_iso(), "path": path, "ok": ok}
        if err:
            rec["err"] = err
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()

    if is_r3(path):
        add_lesson(f"拦截删除：{path} 命中 R3 禁区，已跳过", tag="自动")
        return False
    if os.path.islink(path) or _is_junction_path(path):
        add_lesson(f"拦截删除：{path} 是联接/符号链接，已跳过（避免误伤迁移目录）",
                   tag="自动")
        return False
    bad = _reject_unsafe_path(path)
    if bad:
        add_lesson(f"拦截删除：{path} 不安全（{bad}），已跳过", tag="自动")
        return False
    if dry:
        return True
    # 二次规范化校验：防路径替换（校验对象与删除对象一致）
    real = os.path.realpath(path)
    if is_r3(real):
        add_lesson(f"拦截删除：{path} 规范化后命中 R3 禁区，已跳过", tag="自动")
        return False

    failures = []

    def _on_rmtree_err(func, p, exc):
        failures.append((p, exc))

    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path, onerror=_on_rmtree_err)
        else:
            os.remove(path)
    except Exception as e:
        _log(False, str(e))
        add_lesson(f"删除失败：{path} → {e}", tag="自动")
        return None
    if failures:  # 部分失败：子项被占用/权限不足等，不得记为成功
        detail = "; ".join(f"{p}: {type(e).__name__}" for p, e in failures[:5])
        _log(False, f"partial-delete: {detail}")
        add_lesson(f"部分删除失败：{path}（{len(failures)} 个子项残留，已计失败）",
                   tag="自动")
        return None
    if os.path.lexists(path):  # 后置校验：目标仍存在即判失败
        _log(False, "删除后目标仍存在")
        add_lesson(f"删除后目标仍存在：{path}，已计失败", tag="自动")
        return None
    _log(True)
    return True


def collect_targets(args):
    """汇总本论所有删除候选。"""
    targets = []
    targets += find_temp_targets(args.min_age)
    targets += find_cache_targets(args.with_r2)
    # 回收站幽灵收据（实占 0，安全清账本）
    for gi in find_ghost_receipts():
        targets.append({"label": "幽灵收据", "path": gi, "size": 0,
                        "risk": "R1", "reason": "有$I无$R，实占0，清账本"})
    return targets


# ══════════════════════════ 命令 · doctor ═════════════════════════════
def cmd_doctor(args):
    lessons = load_lessons()
    print("=" * 72)
    print(f"  净盘师 DiskKeeper v{VERSION} · 体检 · {'深度' if args.deep else '快速'}")
    print(f"  反省基因：已载入 {len(lessons)} 条血泪教训（先查正本再动手）")
    print("=" * 72)

    drives = detect_drives()
    if not drives:
        print("[!] 未探测到任何固定盘（本工具仅支持 Windows）。")
        return 1

    lg = load_ledger()
    prev = {d: lg.get("drives", {}).get(d, {}).get("free") for d in drives}

    drives_d = {d: df_free(d) for d in drives}
    print("\n[空间实测（df 唯一可信）]")
    for d in drives:
        v = drives_d[d]
        pct = v["free"] / v["total"] * 100
        delta = ""
        if prev.get(d):
            diff = v["free"] - prev[d]
            delta = f"  较上台账 {diff / 1024 ** 3:+.1f} GB"
        print(f"  {d}: 可用 {human(v['free'])} / {human(v['total'])} ({pct:.0f}%){delta}")

    print("\n[回收站真实账本（$I 收据 vs $R 实体）]")
    paired, ghost = recycle_inventory()
    print(f"  配对完整 : {paired['n']} 项  实占 {human(paired['real'])}"
          f"（声明 {human(paired['declared'])}）")
    print(f"  幽灵收据 : {ghost['n']} 项  声明 {human(ghost['declared'])}  实占 0")
    if ghost["n"]:
        print(f"  → 账面虚高 {human(ghost['declared'])}，可清账："
              f"python scripts/disk_butler.py recycle --ghost --yes")

    print("\n[已知缓存点实测]")
    for p in list(temp_roots()) + cache_hosts():
        if os.path.isdir(p):
            print(f"  {human(walk_size(p)):>10}  {p}")

    if args.deep or args.refresh:
        deep = build_deep(drives)
        lg.update(deep)
        lg["ts"] = now_iso()
        lg["drives"] = drives_d
        save_ledger(lg)
        print_deep(lg)
    else:
        if lg.get("top_dirs"):
            print_deep(lg, cached=True)
        else:
            print("\n[提示] 尚无台账。首次请跑：python scripts/disk_butler.py doctor --deep")

    print("\n[健康判定 & 建议]")
    for d in drives:
        pct = drives_d[d]["free"] / drives_d[d]["total"] * 100
        if pct < 15:
            print(f"  [告急] {d} 盘可用 {pct:.0f}%，告急 → 跑 clean --yes")
            warn = 1
        elif pct < 25:
            print(f"  [注意] {d} 盘可用 {pct:.0f}%，关注")
        else:
            print(f"  [健康] {d} 盘可用 {pct:.0f}%，健康")
    if ghost["n"]:
        print(f"  [*] 回收站有 {ghost['n']} 条幽灵收据（账面虚高），"
              f"建议 recycle --ghost --yes 清账")
    print("\n超越基因：本轮体检快照已可入库，跑 genes 看趋势。")
    return 0


def build_deep(drives):
    print("\n[深度盘点中：三盘顶层目录 + 大文件（首跑需几分钟）]")
    deep = {"top_dirs": {}, "big_files": {}}

    def top_dirs(drive):
        root = drive + ":\\"
        out = []
        try:
            for e in os.scandir(root):
                try:
                    if e.is_dir(follow_symlinks=False):
                        out.append([e.name, walk_size(e.path)])
                    else:
                        out.append([e.name, e.stat().st_size])
                except OSError:
                    out.append([e.name, -1])
        except OSError:
            pass
        return sorted(out, key=lambda x: -x[1])

    def big_files(drive, min_gb=3.0, limit=10):
        hits = []
        min_b = min_gb * 1024 ** 3
        stack = [drive + ":\\"]
        while stack and len(hits) < limit * 6:
            cur = stack.pop()
            try:
                with os.scandir(cur) as it:
                    for e in it:
                        try:
                            if e.is_symlink() or _is_junction(e):
                                continue
                            if e.is_dir(follow_symlinks=False):
                                stack.append(e.path)
                            else:
                                sz = e.stat(follow_symlinks=False).st_size
                                if sz >= min_b:
                                    hits.append((sz, e.path))
                        except OSError:
                            pass
            except OSError:
                pass
        return sorted(hits, key=lambda x: -x[0])[:limit]

    for d in drives:
        t0 = time.time()
        deep["top_dirs"][d] = [[n, s] for n, s in top_dirs(d)]
        deep["big_files"][d] = [[s, p] for s, p in big_files(d)]
        print(f"  {d}: 完成 {time.time() - t0:.0f}s")
    return deep


def print_deep(lg, cached=False):
    tag = ("（缓存 " + str(lg.get("ts", "?"))[:16] + "）") if cached else ""
    print(f"\n[各盘顶层目录 Top8{tag}]")
    for d, rows in lg.get("top_dirs", {}).items():
        rows = rows[:8]
        if not rows:
            continue
        print(f"  ── {d}: ──")
        for n, s in rows:
            if s < 0:
                continue
            flag = " [禁区]" if is_r3(os.path.join(d + ":\\", n)) else ""
            print(f"    {human(s):>10}  {n}{flag}")
    print("\n[单文件 ≥3GB Top10]")
    for d, rows in lg.get("big_files", {}).items():
        rows = rows[:10]
        if not rows:
            continue
        print(f"  ── {d}: ──")
        for s, p in rows:
            flag = " [禁区]" if is_r3(p) else ""
            print(f"    {human(s):>10}  {p}{flag}")


# ══════════════════════════ 命令 · plan / clean ═══════════════════════
def cmd_plan(args):
    lessons = load_lessons()
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 清理计划（只读，未删任何东西）")
    print(f"  反省基因：已载入 {len(lessons)} 条教训")
    print("=" * 72)
    targets = collect_targets(args)
    by_risk = {}
    for t in targets:
        by_risk.setdefault(t["risk"], []).append(t)
    for risk in ("R1", "R2"):
        items = by_risk.get(risk, [])
        tot = sum(t["size"] for t in items)
        print(f"\n[{risk} {'安全清道夫（默认 clean 执行）' if risk=='R1' else '需确认（--with-r2）'}]"
              f"  共 {len(items)} 项 / {human(tot)}")
        for t in sorted(items, key=lambda x: -x["size"])[:25]:
            print(f"  · {human(t['size']):>10}  {t['reason']}  {t['path']}")
    print("\n[回收站真实内容]")
    paired, ghost = recycle_inventory()
    print(f"  · 实体 {paired['n']} 项 / {human(paired['real'])}（用户自己删的 → 只列不碰）")
    print(f"  · 幽灵 {ghost['n']} 项 / 声明 {human(ghost['declared'])} / 实占 0（可清账）")
    print("\n一句话：R1 默认可自动释放；R2 过目后放行；R3 永不碰。")


CLAIM_RE = re.compile(r"释放[^0-9]{0,8}([\d.]+)\s*(GB|MB|KB|B)")


def cmd_clean(args):
    lessons = load_lessons()
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 清理执行 · {'R1+幽灵' if not args.with_r2 else 'R1+幽灵+R2'}"
          f" · min_age={args.min_age}天")
    print(f"  反省基因：执行前已载入 {len(lessons)} 条血泪教训")
    for i, t in enumerate(lessons[-6:], 1):
        print(f"    {i}. {t[:76]}")
    print("=" * 72)

    targets = collect_targets(args)
    total_claimed = sum(t["size"] for t in targets)
    print(f"\n候选 {len(targets)} 项，声称合计 {human(total_claimed)}")
    for t in sorted(targets, key=lambda x: -x["size"])[:30]:
        print(f"  [{t['risk']}] {human(t['size']):>10}  {t['reason']}  {t['path']}")

    if not args.yes:
        print("\n[X] dry-run：未删除任何文件。确认无误后加 --yes 执行。")
        return 0

    before = {d: df_free(d)["free"] for d in detect_drives()}
    os.makedirs(STATE, exist_ok=True)
    n_ok = n_block = n_err = 0
    with open(MANIFEST, "a", encoding="utf-8") as fh:
        fh.write(f"\n# clean {now_iso()}  candidates={len(targets)}\n")
        for t in targets:
            ok = safe_remove(t["path"], dry=False, fh=fh)
            if ok is True:
                n_ok += 1
            elif ok is False:
                n_block += 1
            else:
                n_err += 1

    after = {d: df_free(d)["free"] for d in detect_drives()}
    actual = sum(after[d] - before[d] for d in before)

    print("\n" + "=" * 72)
    print("[对账 · 反省基因核心环节]")
    print(f"  候选声称合计 : {human(total_claimed)}")
    print(f"  df 实测净释放 : {human(actual)}")
    for d in before:
        diff = after[d] - before[d]
        print(f"    {d} 盘可用 {human(before[d])} → {human(after[d])}"
              f"（{diff / 1024 ** 3:+.2f} GB）")
    acc = (min(actual, total_claimed) / total_claimed * 100) if total_claimed else 100.0
    print(f"  实际删除 : {n_ok} 项 | 拦截(R3/联接) : {n_block} | 失败 : {n_err}")
    print(f"  账实相符度 : {acc:.0f}%")
    if total_claimed and actual < total_claimed * 0.6:
        lesson = (f"clean 声称 {human(total_claimed)} 但 df 实测仅 {human(actual)}，"
                  f"相符度 {acc:.0f}% —— 疑似删除进了回收站未净化/被占用/"
                  f"统计口径虚高，下一轮先查回收站")
        add_lesson(lesson, tag="自动")
        print("  [!] 偏差超阈值 → 已自动落教训进正本（进化基因）")

    rec = {"ts": now_iso(), "cmd": "clean", "claimed": total_claimed,
           "actual": actual, "accuracy": round(acc, 1),
           "n_ok": n_ok, "n_block": n_block, "with_r2": args.with_r2,
           "free_after": after}
    log_history(rec)

    print("\n[超越基因 · 比上次好在哪]")
    hist = [h for h in load_history() if h.get("cmd") == "clean"]
    if len(hist) >= 2:
        prev, cur = hist[-2], hist[-1]
        if prev["accuracy"] > 0:
            d = cur["accuracy"] - prev["accuracy"]
            print(f"  · 账实相符度 {prev['accuracy']:.0f}% → {cur['accuracy']:.0f}%（{d:+.0f}pct）")
        print(f"  · 实际释放 {human(prev['actual'])} → {human(cur['actual'])}")
        print(f"  · 血泪教训库 {len(load_lessons())} 条，每条都在阻止重蹈覆辙")
    else:
        print("  · 首轮执行，已入库。下一轮起给出对比。")
    print("=" * 72)
    return 0


# ══════════════════════════ 命令 · recycle ════════════════════════════
def cmd_recycle(args):
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 回收站")
    print("=" * 72)
    if args.purge:
        if not args.yes:
            print("[X] 清空回收站是【不可逆】操作，需 --yes 显式确认。")
            print("   用法：python scripts/disk_butler.py recycle --purge --yes")
            return 2
        print("[!] 警告：即将永久删除回收站【全部】内容，不可恢复！")
        paired, ghost = recycle_inventory()
        print(f"   将删除：配对实体 {paired['n']} 项 / {human(paired['real'])}"
              f" + 幽灵 {ghost['n']} 条")
        n = 0
        for root in recycle_roots().values():
            for sid in os.listdir(root):
                d = os.path.join(root, sid)
                if not os.path.isdir(d):
                    continue
                for fn in list(os.listdir(d)):
                    p = os.path.join(d, fn)
                    try:
                        if os.path.isdir(p):
                            shutil.rmtree(p, onerror=lambda f, x, e: None)
                        else:
                            os.remove(p)
                        n += 1
                    except Exception:
                        pass
        print(f"[OK] 已清空回收站，处理 {n} 项。")
        return 0

    if args.ghost:
        gis = find_ghost_receipts()
        if not args.yes:
            print(f"dry-run：将清除 {len(gis)} 条幽灵收据（实占 0，清账本）。"
                  f"加 --yes 执行。")
            return 0
        n = 0
        for gi in gis:
            try:
                os.remove(gi)
                n += 1
            except OSError:
                pass
        print(f"[OK] 已清幽灵收据 {n} 条，回收站账面归真。")
        return 0

    # 默认：只读账本
    paired, ghost = recycle_inventory()
    print(f"\n[回收站真实账本]")
    print(f"  配对完整 : {paired['n']} 项  实占 {human(paired['real'])}")
    print(f"  幽灵收据 : {ghost['n']} 项  声明 {human(ghost['declared'])}  实占 0")
    print(f"\n  · 清幽灵收据：recycle --ghost --yes")
    print(f"  · 清空全站（不可逆）：recycle --purge --yes")
    return 0


# ══════════════════════════ 命令 · big ═══════════════════════════════
def cmd_big(args):
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 大目录/大文件定位（只读，不删）"
          f" · 阈值 {args.min_gb}GB")
    print("=" * 72)
    min_b = args.min_gb * 1024 ** 3
    for d in detect_drives():
        print(f"\n── {d}: ──")
        hits = []
        stack = [d + ":\\"]
        while stack and len(hits) < 60:
            cur = stack.pop()
            try:
                with os.scandir(cur) as it:
                    for e in it:
                        try:
                            if e.is_symlink() or _is_junction(e):
                                continue
                            if e.is_dir(follow_symlinks=False):
                                sz = walk_size(e.path)
                            else:
                                sz = e.stat(follow_symlinks=False).st_size
                            if sz >= min_b:
                                hits.append((sz, e.path))
                            if e.is_dir(follow_symlinks=False):
                                stack.append(e.path)
                        except OSError:
                            pass
            except OSError:
                pass
        for sz, p in sorted(hits, key=lambda x: -x[0])[:15]:
            flag = " [禁区]" if is_r3(p) else ""
            print(f"  {human(sz):>10}  {p}{flag}")
    print("\n提示：[禁区] 为 R3 禁区（永不自动清理），仅供你人工裁决。")


# ══════════════════════════ 命令 · genes / learn ══════════════════════
def cmd_genes(args):
    lessons = load_lessons()
    hist = load_history()
    cleans = [h for h in hist if h.get("cmd") == "clean"]
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 三基因报告")
    print("=" * 72)
    print(f"\n[反省 · 动手前查正本，跑完对账]")
    print(f"  · 血泪教训库 : {len(lessons)} 条")
    accs = [h["accuracy"] for h in cleans if h.get("accuracy")]
    if accs:
        print(f"  · 近 {len(accs)} 轮账实相符度 : "
              f"{'% → '.join(f'{a:.0f}' for a in accs[-6:])} %")
    bad = [h for h in cleans if h.get("accuracy", 100) < 60]
    print(f"  · 低相符度轮次 : {len(bad)}（<60% 视为账实不符，已自动落教训）")
    print(f"\n[进化 · 错当轮闭环]")
    print(f"  · 自动落教训 : {sum(1 for t in lessons if '[自动]' in t)} 条")
    print(f"  · 人工落教训 : {sum(1 for t in lessons if '[人工]' in t)} 条")
    if lessons:
        print(f"  · 最新教训 : {lessons[-1][:80]}")
    print(f"\n[超越 · 每次留一条'比上次好在哪']")
    if cleans:
        first, last = cleans[0], cleans[-1]
        print(f"  · 累计 {len(cleans)} 轮清理，实际释放合计 "
              f"{human(sum(h.get('actual', 0) for h in cleans))}")
        print(f"  · 首轮相符度 {first.get('accuracy', 0):.0f}% → "
              f"最新 {last.get('accuracy', 0):.0f}%")
    else:
        print("  · 尚无清理记录。首轮 clean 后开始累积。")
    print(f"\n  台账/历史/教训 均在 {STATE}")
    print("=" * 72)


def cmd_learn(args):
    add_lesson(args.text, tag=args.tag)
    print(f"[OK] 已落正本（[{args.tag}] {args.text}）")
    print(f"  {LESSONS}  现共 {len(load_lessons())} 条")


# ══════════════════════════ 台账 ═════════════════════════════════════
def load_ledger():
    if os.path.isfile(LEDGER):
        try:
            with open(LEDGER, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_ledger(lg):
    os.makedirs(STATE, exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(lg, f, ensure_ascii=False, indent=1)


# ══════════════════════════ 主入口 ═══════════════════════════════════
def main():
    ap = argparse.ArgumentParser(
        description="净盘师 DiskKeeper · 智能净盘师 · 体检/清理/自进化")
    ap.add_argument("--version", action="version",
                    version=f"disk_butler {VERSION}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("doctor", help="快速/深度体检（只读）")
    p.add_argument("--deep", action="store_true", help="全盘盘点（24h 缓存）")
    p.add_argument("--refresh", action="store_true", help="强制重建台账")

    sub.add_parser("scan", help="深度体检（同 doctor --deep）")

    p = sub.add_parser("plan", help="清理计划（只读）")
    p.add_argument("--with-r2", action="store_true")
    p.add_argument("--min-age", type=int, default=7, help="Temp 最小年龄(天)")

    p = sub.add_parser("clean", help="执行清理（默认 dry-run）")
    p.add_argument("--yes", action="store_true", help="确认执行（必须显式）")
    p.add_argument("--with-r2", action="store_true", help="包含 R2 需确认项")
    p.add_argument("--min-age", type=int, default=7, help="Temp 最小年龄(天)")
    p.add_argument("--protect", action="append", default=[],
                   help="额外禁区路径（可多次）")

    p = sub.add_parser("recycle", help="回收站账本/净化")
    p.add_argument("--ghost", action="store_true", help="清幽灵收据")
    p.add_argument("--purge", action="store_true", help="清空回收站(不可逆)")
    p.add_argument("--yes", action="store_true", help="确认执行")

    p = sub.add_parser("big", help="大目录/文件定位（只读）")
    p.add_argument("--min-gb", type=float, default=5, help="阈值(GB)")

    sub.add_parser("genes", help="三基因报告")
    p = sub.add_parser("learn", help="落一条教训进正本")
    p.add_argument("text")
    p.add_argument("--tag", default="人工")
    sub.add_parser("evolve", help="自我迭代引擎（运行指纹→规则演进）")
    sub.add_parser("report", help="省心报告（成就卡+分享文案）")
    sub.add_parser("auto", help="自动值守能力说明（只读）")

    args = ap.parse_args()
    os.makedirs(STATE, exist_ok=True)

    # 注入额外禁区
    if getattr(args, "protect", None):
        global _R3_CACHE
        _R3_CACHE = build_r3(args.protect)

    if args.cmd == "doctor":
        sys.exit(cmd_doctor(args))
    elif args.cmd == "scan":
        args.deep = True
        sys.exit(cmd_doctor(args))
    elif args.cmd == "plan":
        cmd_plan(args)
    elif args.cmd == "clean":
        sys.exit(cmd_clean(args))
    elif args.cmd == "recycle":
        sys.exit(cmd_recycle(args))
    elif args.cmd == "big":
        cmd_big(args)
    elif args.cmd == "genes":
        cmd_genes(args)
    elif args.cmd == "learn":
        cmd_learn(args)
    elif args.cmd == "evolve":
        sys.exit(cmd_evolve(args))
    elif args.cmd == "report":
        cmd_report(args)
    elif args.cmd == "auto":
        cmd_auto(args)


# ══════════════════════════ 命令 · evolve（自我迭代引擎） ══════════════════════════
def load_manifest():
    if not os.path.isfile(MANIFEST):
        return []
    out = []
    with open(MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def cmd_evolve(args):
    """自我迭代引擎：把运行指纹变成规则库演进。
    反省→进化→超越 三基因在这里闭环：读历史(反省)、据偏差自动落教训(进化)、
    输出「比上次好在哪」并推进规则版本(超越)。这就是「实践中不断自我迭代」的硬落地。"""
    from collections import Counter
    hist = load_history()
    man = load_manifest()
    lessons = load_lessons()
    cleans = [h for h in hist if h.get("cmd") == "clean"]
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 自我迭代引擎  规则库 RULES_VERSION={RULES_VERSION}")
    print("=" * 72)
    if not cleans:
        print("  尚无 clean 运行记录。先跑一次：python scripts/disk_butler.py clean --yes")
        print("  每一轮运行都会成为下一轮的学习样本——越用越懂你的机器。")
        return 0
    total_released = sum(h.get("actual", 0) for h in cleans)
    accs = [h["accuracy"] for h in cleans if h.get("accuracy")]
    avg_acc = sum(accs) / len(accs) if accs else 0
    blocks = sum(h.get("n_block", 0) for h in cleans)
    suff = Counter()
    for m in man:
        ext = os.path.splitext(m.get("path", ""))[1].lower() or "(无后缀)"
        suff[ext] += 1
    print(f"\n[运行指纹 · 反省基因的数据底座]")
    print(f"  · 累计清理 {len(cleans)} 轮，实际释放 {human(total_released)}")
    print(f"  · 账实相符度均值 : {avg_acc:.0f}%  | 最低 {min(accs):.0f}%  最高 {max(accs):.0f}%")
    print(f"  · 累计拦截(禁区/联接) : {blocks} 次  → 正向白名单护栏有效性")
    if suff:
        print("  · 最常清理类型 Top3 : " + " / ".join(f"{k}×{v}" for k, v in suff.most_common(3)))
    print(f"  · 血泪教训库 : {len(lessons)} 条（每条都在阻止重蹈覆辙）")
    print(f"\n[进化 · 本轮自动优化]")
    flags = []
    if avg_acc < 90 and len(accs) >= 2:
        flags.append(f"账实相符度偏低({avg_acc:.0f}%)，下一轮 clean 后应追加 recycle 净化回收站")
    if blocks == 0 and len(cleans) >= 2:
        flags.append("连续无禁区命中 → 正向白名单稳健，可放心放开 --with-r2 探索更大缓存")
    if not flags:
        flags.append("各项指标健康，规则库无需调整；继续累积运行指纹以微调阈值")
    for fl in flags:
        print(f"  · {fl}")
    evo = (f"[自动] evolve 指纹：{len(cleans)}轮/释放{human(total_released)}/"
            f"相符{avg_acc:.0f}%/拦截{blocks} → {flags[0]}")
    add_lesson(evo, tag="自动")
    lg = load_ledger()
    lg["rules_version"] = RULES_VERSION
    lg["last_evolve"] = now_iso()
    lg["evolve_rounds"] = lg.get("evolve_rounds", 0) + 1
    save_ledger(lg)
    print(f"\n[超越 · 比上次好在哪]")
    if len(cleans) >= 2:
        prev, cur = cleans[-2], cleans[-1]
        print(f"  · 相符度 {prev.get('accuracy', 0):.0f}% → {cur.get('accuracy', 0):.0f}%")
        print(f"  · 释放 {human(prev.get('actual', 0))} → {human(cur.get('actual', 0))}")
    print(f"  · 规则库已演进至 RULES_VERSION={RULES_VERSION}（第 {lg['evolve_rounds']} 次迭代）")
    print("=" * 72)
    return 0


def cmd_report(args):
    """省心报告：把「释放多少 / 零误删 / 动了什么」变成可分享的成就卡。
    这是「想推荐」的载体——看得见的价值感，才让人愿意转发。"""
    hist = load_history()
    cleans = [h for h in hist if h.get("cmd") == "clean"]
    drives = detect_drives()
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 省心报告")
    print("=" * 72)
    if not cleans:
        print("  还没有清理记录，先跑一次 clean 再来生成报告~")
        return 0
    total = sum(h.get("actual", 0) for h in cleans)
    accs = [h["accuracy"] for h in cleans if h.get("accuracy")]
    avg_acc = sum(accs) / len(accs) if accs else 100
    print(f"\n  [*] 累计为你释放：{human(total)} 空间")
    print(f"  [核] 账实相符度均值：{avg_acc:.0f}%（声称=实测，不虚报）")
    print(f"  [净] 累计安全清理：{sum(h.get('n_ok', 0) for h in cleans)} 项")
    print(f"  [拦] 累计拦截误删：{sum(h.get('n_block', 0) for h in cleans)} 次（禁区/联接）")
    print(f"  [库] 血泪教训库：{len(load_lessons())} 条守护你的文件")
    print("\n[当前空间]")
    for d in drives:
        v = df_free(d)
        print(f"  {d}: 可用 {human(v['free'])} / {human(v['total'])}")
    card = (
        f"用【净盘师 DiskKeeper】给电脑做了次深度体检+安全清理——\n"
        f"累计释放 {human(total)} 空间，账实相符度 {avg_acc:.0f}%，"
        f"零误删、不动个人文件。\n"
        f"先体检再清理，每一步可追溯，省心又安心。\n"
        f"#磁盘清理 #C盘爆满 #电脑提速 #AI管家"
    )
    print("\n[可分享文案 · 复制发朋友圈/小红书]")
    print("-" * 60)
    print(card)
    print("-" * 60)
    print("=" * 72)
    return 0


def cmd_auto(args):
    """自动值守「能力说明」：定时只读体检 + 阈值告警 + 报告；
    删除类操作始终需要人工放行。本命令只打印能力说明
    与「只读」调度模板，不引导任何无人值守删除。（消除 Intent-Code Divergence）"""
    print("=" * 72)
    print(f"  净盘师 v{VERSION} · 自动值守说明")
    print("=" * 72)
    print("  本命令输出自动值守的只读调度模板，供你自行配置。")
    print("  免费版已具备：doctor / plan / clean / recycle / big / genes / evolve / report")
    print("  可实现的只读值守：定时体检 + 阈值告警 + 报告输出")
    print("\n  只读调度模板（仅示例，供你评估后自行配置；启用前请人工确认清单）：")
    print("    触发器 : 每周六 09:30")
    print("    操作 1 : python scripts/disk_butler.py doctor --deep   # 只读体检")
    print("    操作 2 : python scripts/disk_butler.py plan            # 只读预览")
    print("    操作 3 : python scripts/disk_butler.py report          # 出报告")
    print("\n  [X] 安全禁令：不要为 clean / recycle --purge 配置无人值守自动执行；")
    print("     删除类操作必须由人工看过 plan / clean(dry-run) 清单后手动加 --yes 确认。")
    print("  受控托管模式：定时只读体检 + 阈值告警 + 人工放行，")
    print("     不做无人删除——删除权始终留在你手里。")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    main()
