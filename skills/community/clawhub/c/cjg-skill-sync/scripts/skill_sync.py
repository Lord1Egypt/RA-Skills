#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cjg-skill-sync：技能更新助手核心脚本。

子命令：
  check       只检查，不动任何文件（默认、最安全）
  apply       应用更新（先备份；大版本/本地改动需显式确认）
  rollback    回滚到最近一次备份
  baseline    建立/重建"安装快照"（本地改动检测的基线）
  autoupdate  开关每日自动检查（默认关）

设计铁律（勿改）：
  1. 更新前必备份，失败必回滚。
  2. 检测到本地改动 → 不覆盖，先问（--force-overwrite 才强制）。
  3. 主版本变化 → 不自动执行（--allow-major 才允许）。
  4. 默认不联网改状态；每日自动检查默认关（opt-in）。
零第三方依赖（仅标准库），离线也能跑 check 的扫描部分。
"""
import os
import sys
import json
import time
import shutil
import hashlib
import argparse
import datetime
import subprocess
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
SYNC_META = ".cjg_sync"
# 备份外置根目录：绝不能放技能目录里（--force 安装会整目录替换，备份会一起没）
BACKUP_ROOT = os.path.join(os.path.expanduser("~"), ".workbuddy", "backups",
                           "cjg-skill-sync")

DEFAULT_CONFIG = {
    "skill_version_url": "https://1318491188-05nz50b82l.ap-guangzhou.tencentscf.com",
    "auto_check_enabled": False,
    "auto_apply_safe_only": True,
}

# 平台命令行工具（用于自动安装；藏经阁不托管安装包）
SKILLHUB_CLI = os.path.join(os.path.expanduser("~"), ".skillhub", "skills_store_cli.py")
CLAWHUB_CMD = os.path.join(os.path.expanduser("~"), ".workbuddy", "binaries",
                           "node", "versions", "22.12.0", "clawhub.cmd")

# 扫描目录：用户级 + 项目级（都存在时都扫）
SKILLS_DIRS = [
    os.path.expanduser("~/.workbuddy/skills"),
    os.path.join(os.getcwd(), ".workbuddy", "skills"),
]

# 哈希计算时跳过的目录/文件（噪音，不代表用户改动）
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".cjg_sync", ".backups"}
SKIP_SUFFIX = {".pyc", ".pyo", ".tmp", ".log"}


# ------------------------------------------------------------------ 基础工具


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            cfg.update(json.load(open(CONFIG_PATH, encoding="utf-8")))
        except Exception as e:
            print(f"⚠ config.json 解析失败，用默认值: {e}")
    return cfg


def save_config(cfg):
    json.dump(cfg, open(CONFIG_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def vkey(v):
    """语义化版本排序键：3.1.0 -> (3,1,0)。"""
    parts = []
    for p in str(v or "0.0.0").split("+")[0].split("-")[0].split(".")[:3]:
        digits = "".join(ch for ch in p if ch.isdigit())
        try:
            parts.append(int(digits or 0))
        except Exception:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def parse_frontmatter(path):
    """极简 YAML frontmatter 解析（只取 key: value，够用且零依赖）。"""
    meta = {}
    try:
        lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    except Exception:
        return meta
    if not lines or lines[0].strip() != "---":
        return meta
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def http_json(url, method="GET", body=None, timeout=30):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return json.loads(raw or "{}")
        except Exception:
            return {"ok": False, "error": raw[:160]}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"}


# ------------------------------------------------------------------ 扫描


def scan_installed():
    """扫描本机已装技能：返回 {slug: {dir, name, version}}。

    布局兼容：
      用户级   ~/.workbuddy/skills/<技能>/SKILL.md
      命名空间 ~/.workbuddy/skills/@user_xxx/<技能>/SKILL.md   <- 再深一层
      项目级   <cwd>/.workbuddy/skills/<技能>/SKILL.md
    WorkBuddy 会把部分来源的技能装进 `@handle/` 命名空间子目录，
    只看一级会漏扫（实测本机因此漏掉 2 个），故递归取一层。
    """
    found = {}
    seen_dirs = set()

    def collect(d, fallback_name):
        """若 d 是技能目录则收录，返回 True。"""
        if not os.path.isdir(d) or d in seen_dirs:
            return True
        skill_md = os.path.join(d, "SKILL.md")
        if not os.path.exists(skill_md):
            return False
        meta = parse_frontmatter(skill_md)
        slug = meta.get("slug") or fallback_name
        seen_dirs.add(d)
        found[slug] = {
            "dir": d,
            "name": meta.get("displayName") or meta.get("name") or fallback_name,
            "version": meta.get("version") or "0.0.0",
        }
        return True

    for base in SKILLS_DIRS:
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            # 跳过隐藏目录与下划线开头的（_deprecated/.backup 等）
            if entry.startswith(".") or entry.startswith("_"):
                continue
            d = os.path.join(base, entry)
            if not os.path.isdir(d):
                continue
            if collect(d, entry):
                continue
            # 不是技能目录 → 可能是命名空间层（@handle/），再下一层
            try:
                subs = sorted(os.listdir(d))
            except OSError:
                continue
            for sub in subs:
                if sub.startswith(".") or sub.startswith("_"):
                    continue
                collect(os.path.join(d, sub), sub)
    return found
    return found


# ------------------------------------------------------------------ 本地改动检测


def file_hashes(root):
    """计算技能目录下所有有效文件的哈希。"""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.startswith(".") and fn in {".DS_Store"}:
                continue
            if os.path.splitext(fn)[1].lower() in SKIP_SUFFIX:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            try:
                h = hashlib.sha256(open(full, "rb").read()).hexdigest()
                out[rel] = h
            except Exception:
                continue
    return out


def baseline_path(slug_dir):
    return os.path.join(slug_dir, SYNC_META, "baseline.json")


def check_local_changes(slug_dir):
    """返回 (state, changed_files)。state: unknown / clean / modified。"""
    bp = baseline_path(slug_dir)
    if not os.path.exists(bp):
        return "unknown", []
    try:
        base = json.load(open(bp, encoding="utf-8")).get("files", {})
    except Exception:
        return "unknown", []
    now = file_hashes(slug_dir)
    changed = sorted(set(now) | set(base))
    changed = [f for f in changed
               if f != f"{SYNC_META}/baseline.json" and base.get(f) != now.get(f)]
    return ("modified" if changed else "clean"), changed


def write_baseline(slug_dir):
    os.makedirs(os.path.join(slug_dir, SYNC_META), exist_ok=True)
    json.dump(
        {"created_at": datetime.datetime.now().isoformat(timespec="seconds"),
         "files": file_hashes(slug_dir)},
        open(baseline_path(slug_dir), "w", encoding="utf-8"),
        ensure_ascii=False, indent=2,
    )


# ------------------------------------------------------------------ 停滞检测


def _stalled_path():
    return os.path.join(BACKUP_ROOT, "stalled.json")


def load_stalled():
    try:
        return json.load(open(_stalled_path(), encoding="utf-8"))
    except Exception:
        return {}


def mark_stalled(slug, version):
    """记下「云端说有 X，但装完还是旧版」——平台包尚未放出该版本。

    没有这个机制会形成死循环：每次 check 都提示可更新，装完版本号不变，
    下次又提示（2026-09-13 真机验证 bagua-furnace 时踩到）。
    """
    try:
        os.makedirs(BACKUP_ROOT, exist_ok=True)
        data = load_stalled()
        data[slug] = {"version": str(version),
                      "at": datetime.datetime.now().isoformat(timespec="seconds")}
        json.dump(data, open(_stalled_path(), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    except Exception:
        pass


def is_stalled(slug, version):
    rec = load_stalled().get(slug)
    if not rec:
        return False
    try:
        return vkey(version) <= vkey(rec.get("version", "0"))
    except Exception:
        return False


# ------------------------------------------------------------------ 远端查询


def fetch_latest(slugs, cfg, batch=50):
    """调藏经阁公开读接口。失败返回 {}（离线降级：只报本地版本）。

    注意：服务端单批上限 50 个 slug，超过会被静默截断 —— 本机技能数普遍 >50
    （实测 74 个），故必须分批。首版一次性全发导致后半部分查不到，已修。
    """
    url = cfg["skill_version_url"].rstrip("/")
    out = {}
    for i in range(0, len(slugs), batch):
        chunk = slugs[i:i + batch]
        res = http_json(url + "/", method="POST", body={"slugs": chunk})
        if not res.get("ok"):
            res = http_json(url + "/?slugs=" + ",".join(chunk))
        for s in (res.get("skills") or []):
            out[s.get("slug")] = s
    return out


def classify(cur, new, indexed=True):
    """返回 latest / patch / minor / major / ahead / no_index。

    ahead    = 本地版本高于云端索引（云端索引滞后，不是"你落后了"）
    no_index = 云端根本没有这个 slug 的记录
    区分这两种很重要：早期版本一律显示"最新"会误导用户（实为云端数据陈旧）。
    """
    if not indexed:
        return "no_index"
    c, n = vkey(cur), vkey(new)
    if n > c:
        if n[0] != c[0]:
            return "major"
        if n[1] != c[1]:
            return "minor"
        return "patch"
    if c > n:
        return "ahead"
    return "latest"


# ------------------------------------------------------------------ 备份/回滚


def backup_dir(slug_dir, slug):
    """备份到技能目录之外。

    ⚠ 事故教训（2026-09-13）：备份原先放在技能目录内的 .cjg_sync/backups/，
    而平台 CLI 的 --force 安装会**整目录替换**（连同 .cjg_sync 一起删）→
    备份与技能同归于尽，回滚直接失效（真机验证时实测踩到，报销了自己造的备份）。
    因此备份一律外置到 ~/.workbuddy/backups/，安装再暴力也删不到。
    """
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(BACKUP_ROOT, slug, ts)
    os.makedirs(dest, exist_ok=True)
    for entry in os.listdir(slug_dir):
        if entry == SYNC_META:
            continue
        s, d = os.path.join(slug_dir, entry), os.path.join(dest, entry)
        try:
            shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
        except Exception as e:
            print(f"  ⚠ 备份 {entry} 失败：{type(e).__name__}: {str(e)[:80]}")
    # 指针也写外部（写技能目录内会被 --force 一起删掉）
    try:
        os.makedirs(os.path.join(BACKUP_ROOT, slug), exist_ok=True)
        open(os.path.join(BACKUP_ROOT, slug, "last_backup.txt"), "w").write(dest)
    except Exception:
        pass
    print(f"  📦 已备份 -> {dest}")
    return dest


def restore_dir(slug_dir, backup):
    """用备份覆盖回去（先清空现有内容，保留 .cjg_sync）。"""
    if not backup or not os.path.isdir(backup):
        print("  ❌ 备份不存在，无法回滚")
        return False
    for entry in os.listdir(slug_dir):
        if entry == SYNC_META:
            continue
        p = os.path.join(slug_dir, entry)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for entry in os.listdir(backup):
        s, d = os.path.join(backup, entry), os.path.join(slug_dir, entry)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
    print(f"  ↩ 已回滚到 {backup}")
    return True


def last_backup(slug_dir, slug=None):
    """最近一次备份：优先外部（新的），回退技能目录内（旧版留下的）。"""
    cands = []
    if slug:
        cands.append(os.path.join(BACKUP_ROOT, slug, "last_backup.txt"))
    cands.append(os.path.join(slug_dir, SYNC_META, "last_backup.txt"))
    for p in cands:
        if os.path.exists(p):
            v = open(p).read().strip()
            if v and os.path.isdir(v):
                return v
    # 指针丢了就从外部目录里按时间戳取最新的
    if slug:
        root = os.path.join(BACKUP_ROOT, slug)
        if os.path.isdir(root):
            subs = [d for d in os.listdir(root)
                    if os.path.isdir(os.path.join(root, d))]
            if subs:
                return os.path.join(root, sorted(subs)[-1])
    return None


# ------------------------------------------------------------------ 安装源


def _which(name):
    try:
        return shutil.which(name) or ""
    except Exception:
        return ""


def cli_available(plat):
    """平台 CLI 是否可用（决定能否自动安装）。"""
    if plat == "skillhub":
        return os.path.exists(SKILLHUB_CLI)
    if plat == "clawhub":
        return bool(_which("clawhub")) or os.path.exists(CLAWHUB_CMD)
    return False


def build_install_cmd(plat, slug, target_dir=None, version=None):
    """构造真实安装命令。返回 {plat, display, cmd, auto, cwd}。

    · skillhub CLI 支持 --dir，可精确装到技能原目录（首选）。
    · clawhub CLI 无 --dir，改为把 cwd 设成技能父目录，让它落到同名目录里；
      安装后一律校验版本号，装错位置能立刻发现。
    """
    if plat == "skillhub":
        cmd = [sys.executable, SKILLHUB_CLI, "install", slug]
        # ⚠ 实测：SkillHub CLI 会把包装成「<dir>/<slug>/」——传技能目录会多套一层
        # （2026-09-13 真机验证：传目标目录后版本纹丝不动，多出 <dir>/bagua-furnace/）。
        # 因此 --dir 必须传技能目录的「父目录」，才能覆盖回原位置。
        parent = os.path.dirname(target_dir) if target_dir else None
        if parent:
            cmd += ["--dir", parent]
        cmd += ["--force"]
        return {"plat": plat, "display": " ".join(cmd), "cmd": cmd,
                "auto": True, "cwd": None}
    if plat == "clawhub":
        exe = _which("clawhub") or CLAWHUB_CMD
        cmd = [exe, "install", slug]
        if version:
            cmd += ["--version", version]
        cmd += ["--force"]
        cwd = os.path.dirname(target_dir) if target_dir else None
        disp = " ".join(cmd) + (f"   （在 {cwd} 下执行）" if cwd else "")
        return {"plat": plat, "display": disp, "cmd": cmd,
                "auto": True, "cwd": cwd}
    return None


def run_install(item, timeout=180):
    """真实执行安装命令（仅当显式 --execute）。返回 (ok, 输出尾部)。"""
    try:
        r = subprocess.run(item["cmd"], cwd=item["cwd"] or None,
                           capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return r.returncode == 0, out[-400:]
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:200]}"


def plan_install(slug, info, target_dir=None, version=None):
    """决定怎么装。返回条目列表 [{plat, display, cmd, auto, cwd}]。

    install_urls 的取值有两种：
      · 普通 URL（github/gitee 等）→ 只展示，供你手动下载
      · "cli:<平台>:<slug>"       → 可用 CLI 自动安装（藏经阁不托管包，只存安装线索）
    """
    urls = info.get("install_urls") or {}
    out = []
    for plat in ("skillhub", "clawhub", "gitee", "github"):
        u = urls.get(plat)
        if not u:
            continue
        if str(u).startswith("cli:"):
            if cli_available(plat):
                item = build_install_cmd(plat, slug, target_dir, version)
                if item:
                    out.append(item)
                    continue
            out.append({"plat": plat,
                        "display": f"（需先安装 {plat} 命令行工具，之后可自动安装）",
                        "cmd": None, "auto": False, "cwd": None})
        else:
            out.append({"plat": plat, "display": u,
                        "cmd": None, "auto": False, "cwd": None})
    if not out:
        out.append({"plat": "manual",
                    "display": f"未登记安装链接，请到作者发布页搜索 {slug}",
                    "cmd": None, "auto": False, "cwd": None})
    return out


# ------------------------------------------------------------------ 子命令


def cmd_check(args):
    cfg = load_config()
    installed = scan_installed()
    if not installed:
        print("未扫描到已安装技能（查找 ~/.workbuddy/skills 与 ./ .workbuddy/skills）")
        return 0

    # 支持只看单个技能：本机常装 70+ 个技能，全量列表刷屏不好用
    if getattr(args, "slug", None):
        if args.slug not in installed:
            print(f"❌ 本机未安装 {args.slug}")
            return 1
        installed = {args.slug: installed[args.slug]}

    print(f"技能更新检查 · {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"（共扫描 {len(installed)} 个技能）\n")

    latest = fetch_latest(list(installed), cfg) if not args.offline else {}
    if not args.offline and not latest:
        print("⚠ 无法连接版本服务，仅显示本机版本（离线模式）\n")

    rows = []
    for slug, meta in sorted(installed.items()):
        info = latest.get(slug)
        cur = meta["version"]
        new = (info or {}).get("latest_version") or cur
        kind = classify(cur, new, indexed=bool(info))
        # 平台包尚未放出该版本（此前装过、版本号没变）→ 不再反复提示
        if kind in ("patch", "minor", "major") and is_stalled(slug, new):
            kind = "stalled"
        state, changed = check_local_changes(meta["dir"])
        rows.append({
            "slug": slug, "cur": cur, "new": new, "kind": kind,
            "changelog": (info or {}).get("changelog") or "",
            "state": state, "changed": changed, "dir": meta["dir"],
            "info": info or {},
        })

    updatable = [r for r in rows if r["kind"] in ("patch", "minor", "major")]
    ahead = [r for r in rows if r["kind"] == "ahead"]
    noidx = [r for r in rows if r["kind"] == "no_index"]
    stalled = [r for r in rows if r["kind"] == "stalled"]

    print(f"{'技能':<26}{'当前':<10}{'最新':<10}{'类型':<10}{'本地':<8}")
    print("-" * 70)
    for r in rows:
        kind_cn = {"latest": "最新", "patch": "补丁", "minor": "小版本",
                   "major": "大版本⚠", "ahead": "本地领先",
                   "no_index": "云端无记录",
                   "stalled": "平台未放出"}.get(r["kind"], r["kind"])
        state_cn = {"clean": "干净", "modified": "已改动", "unknown": "未知"}[r["state"]]
        print(f"{r['slug'][:25]:<26}{r['cur']:<10}{r['new']:<10}{kind_cn:<10}{state_cn:<8}")

    if args.verbose:
        print("\n--- 详情 ---")
        for r in rows:
            if r["kind"] == "latest":
                continue
            print(f"\n● {r['slug']}  {r['cur']} → {r['new']}（{r['kind']}）")
            if r["changelog"]:
                print(f"  变更说明：{r['changelog']}")
            if r["state"] == "modified":
                print(f"  ⚠ 你改过这些文件（更新会覆盖）：{', '.join(r['changed'][:8])}")
            elif r["state"] == "unknown":
                print("  ⚠ 无安装快照，按最保守处理（视为可能改过）")

    safe = [r for r in updatable
            if r["kind"] in ("patch", "minor") and r["state"] == "clean"]
    need_confirm = [r for r in updatable if r not in safe]

    print(f"\n可安全更新（同主版本 + 无本地改动）：{len(safe)} 个")
    print(f"需你确认（大版本 / 本地有改动 / 无快照）：{len(need_confirm)} 个")
    if safe:
        print("  → python scripts/skill_sync.py apply --safe-only")
    for r in need_confirm:
        why = "大版本" if r["kind"] == "major" else "本地有改动/无快照"
        print(f"  → {r['slug']}（{why}）：python scripts/skill_sync.py apply --slug {r['slug']} --allow-major")
    if ahead:
        print(f"\nℹ 本地版本高于云端索引 {len(ahead)} 个（云端索引滞后，非你落后）"
              f"：{', '.join(r['slug'] for r in ahead[:6])}")
    if noidx:
        print(f"ℹ 云端暂无记录 {len(noidx)} 个（作者尚未回写过版本）"
              f"：{', '.join(r['slug'] for r in noidx[:6])}")
    if stalled:
        print(f"ℹ 平台尚未放出新包 {len(stalled)} 个（云端已登记版本号，但装下来还是旧版，"
              f"通常等平台审核完成即可）：{', '.join(r['slug'] for r in stalled[:6])}")
    if not updatable:
        print("\n✅ 没有需要更新的技能")

    # 顺带：没有快照的补建（check 是只读动作，仅写 .cjg_sync 元数据）
    if not args.no_baseline:
        built = 0
        for r in rows:
            if r["state"] == "unknown":
                try:
                    write_baseline(r["dir"])
                    built += 1
                except Exception:
                    pass
        if built:
            print(f"\n（已为 {built} 个技能建立安装快照，便于以后检测你的本地改动）")
    return 0


def cmd_gate(args):
    """调用门闸（2026-09-28）：技能脚本执行前校验版本策略。

    输出 JSON（stdout）：{slug, local, latest, sync_policy, action, message}
    action: none（放行）/ warn（放行+提示）/ block（拒绝执行）/ error（参数错）
    退出码：0 = 放行（none/warn），2 = 拒绝（block）。
    fail-open：索引不可达/超时 → action=none（本地优先铁律；fail-closed 由技能自身声明）。
    """
    import json as _json
    import sys as _sys

    slug = args.slug
    local = args.local
    if not local:
        installed = scan_installed()
        info = installed.get(slug)
        local = (info or {}).get("version") or ""

    latest_row = {}
    try:
        cfg = load_config()
        latest_row = fetch_latest([slug], cfg).get(slug) or {}
    except Exception as e:
        print(_json.dumps({"slug": slug, "local": local, "latest": None,
                           "sync_policy": None, "action": "none",
                           "message": f"索引不可达，fail-open 放行（{e}）"}, ensure_ascii=False))
        return 0

    policy = (latest_row.get("sync_policy") or "warn").lower()
    latest = latest_row.get("latest_version")

    def emit(action, message):
        print(_json.dumps({"slug": slug, "local": local, "latest": latest,
                           "sync_policy": policy, "action": action,
                           "message": message}, ensure_ascii=False))
        if action == "block":
            _sys.stderr.write(f"[sync-gate] {message}\n")
            return 2
        return 0

    if not latest:
        return emit("none", "索引无此技能记录，放行")
    if policy == "off":
        return emit("none", "该技能未接入更新机制")
    if not local:
        return emit("none", "无法确定本地版本，fail-open 放行")
    try:
        behind = vkey(latest) > vkey(local)
    except Exception:
        return emit("none", "版本号无法解析，fail-open 放行")
    if not behind:
        return emit("none", "本地版本不落后于索引，放行")
    if policy == "block":
        return emit("block",
                    f"{slug} 需要强制更新：本地 v{local} < 索引 v{latest}。"
                    f"请先执行：python skill_sync.py apply --slug {slug} --execute，更新后再使用本技能。")
    return emit("warn",
                f"{slug} 有新版本：v{local} → v{latest}（可继续使用，建议更新）。")


def cmd_apply(args):
    cfg = load_config()
    installed = scan_installed()
    if args.slug and args.slug not in installed:
        print(f"❌ 本机未安装 {args.slug}")
        return 1

    latest = fetch_latest(list(installed), cfg)
    if not latest:
        print("❌ 无法连接版本服务，取消更新（避免盲目操作）")
        return 1

    targets = []
    for slug, meta in sorted(installed.items()):
        if args.slug and slug != args.slug:
            continue
        info = latest.get(slug) or {}
        new = info.get("latest_version")
        if not new:
            continue
        kind = classify(meta["version"], new)
        if kind == "latest":
            continue
        state, changed = check_local_changes(meta["dir"])
        targets.append({"slug": slug, "dir": meta["dir"], "cur": meta["version"],
                        "new": new, "kind": kind, "state": state,
                        "changed": changed, "info": info})

    if not targets:
        print("✅ 没有需要更新的技能")
        return 0

    if args.safe_only:
        targets = [t for t in targets
                   if t["kind"] in ("patch", "minor") and t["state"] == "clean"]
        if not targets:
            print("没有可安全自动更新的项（其余需你确认）")
            return 0

    for t in targets:
        print(f"\n=== {t['slug']}  {t['cur']} → {t['new']}（{t['kind']}）===")
        if t["kind"] == "major" and not args.allow_major:
            print("  ⏭ 跳过：主版本变化属不兼容升级，需 --allow-major 显式确认")
            continue
        # dry-run 必须先于「补建快照」，否则预览也会写 .cjg_sync 元数据
        if args.dry_run:
            if t["state"] == "modified":
                print("  （dry-run）将因本地改动跳过，除非加 --force-overwrite："
                      + ", ".join(t["changed"][:6]))
            elif t["state"] == "unknown":
                print("  （dry-run）将先建立安装快照，再备份更新")
            else:
                print("  （dry-run）将执行：备份 → 从原平台安装")
            for it in plan_install(t["slug"], t["info"], t["dir"], t["new"]):
                tag = "可自动安装" if it["auto"] else "手动"
                print(f"    [{it['plat']}] ({tag}) {it['display']}")
            continue

        if t["state"] == "unknown" and not args.force_overwrite:
            # 「从未建过快照」不等于「改过文件」——首次运行无从判断，
            # 让用户为此输 --force-overwrite 是糟糕体验且并无额外安全。
            # 与 check 的行为保持一致：补建快照后视为未改动，
            # 真正的兜底是备份 + rollback（可逆）。
            try:
                write_baseline(t["dir"])
                print("  ℹ 首次运行无安装快照，已建当前快照并视为未改动（备份+回滚兜底）")
            except Exception as e:
                print(f"  ⏭ 跳过：无法建立快照（{type(e).__name__}: {str(e)[:80]}）")
                continue
        elif t["state"] == "modified" and not args.force_overwrite:
            print("  ⏭ 跳过：检测到本地改动，需 --force-overwrite（会覆盖你的修改）")
            if t["changed"]:
                print(f"     受影响文件：{', '.join(t['changed'][:8])}")
            continue

        bak = backup_dir(t["dir"], t["slug"])
        if args.offline_install:
            print("  ⏭ 已备份；离线模式不执行安装")
            continue

        # 安装：默认只给命令；加 --execute 才用平台 CLI 真实安装
        items = plan_install(t["slug"], t["info"], target_dir=t["dir"], version=t["new"])
        print("  安装源（藏经阁不托管安装包，从原平台获取）：")
        for it in items:
            tag = "可自动安装" if it["auto"] else "手动"
            print(f"    [{it['plat']}] ({tag}) {it['display']}")

        if not args.execute:
            print("  ⏭ 未执行安装（默认只给命令）。加 --execute 才会调用平台 CLI 自动安装；")
            print("     也可以自己按上面的命令装完，再跑一次 check 确认版本。")
            print(f"  若安装出问题：python scripts/skill_sync.py rollback --slug {t['slug']}")
            print(f"  （备份位置 {bak}）")
            continue

        done, last_err = False, ""
        for it in items:
            if not it["auto"]:
                continue
            ok, out = run_install(it)
            print(f"    → {it['plat']} 安装：{'成功' if ok else '失败'}")
            if ok:
                done = True
                break
            last_err = out
            if out:
                print(f"      {out.splitlines()[-1][:160]}")
        if not done:
            print(f"  ❌ 自动安装未完成{'：' + last_err.splitlines()[-1][:160] if last_err else ''}")
            print(f"  已备份，可回滚：python scripts/skill_sync.py rollback --slug {t['slug']}")
            continue

        got = parse_frontmatter(os.path.join(t["dir"], "SKILL.md")).get("version")
        if got == t["new"]:
            print(f"  ✅ 安装后本地版本 = {got}，已跟上最新")
            write_baseline(t["dir"])
        else:
            alt = os.path.join(os.path.dirname(t["dir"]), t["slug"])
            if os.path.isdir(alt) and os.path.normcase(alt) != os.path.normcase(t["dir"]):
                print(f"  ⚠ 安装后本地版本 = {got}，目标 = {t['new']}")
                print(f"     CLI 把新包装到了 {alt}（与你的目录 {t['dir']} 不同名），"
                      f"未擅自覆盖，请你确认后再处理。")
            else:
                # 装完版本没变 = 平台放出的包还是旧的（审核/同步未完成）。
                # 标记停滞，避免以后每次 check 都提示、装完又回到原点。
                mark_stalled(t["slug"], t["new"])
                print(f"  ⚠ 安装后本地版本 = {got}，目标 = {t['new']}")
                print(f"     平台尚未放出 {t['new']} 的安装包（版本号已登记，包还在审核/同步）。")
                print(f"     已记为「平台未放出」，check 不再重复提示；过段时间重跑即可。")
            print(f"  回滚：python scripts/skill_sync.py rollback --slug {t['slug']}")
        print(f"  （备份位置 {bak}）")

    return 0


def cmd_rollback(args):
    installed = scan_installed()
    if args.slug not in installed:
        print(f"❌ 本机未安装 {args.slug}")
        return 1
    d = installed[args.slug]["dir"]
    bak = args.backup or last_backup(d, args.slug)
    ok = restore_dir(d, bak)
    return 0 if ok else 1


def cmd_baseline(args):
    installed = scan_installed()
    slugs = [args.slug] if args.slug else sorted(installed)
    n = 0
    for s in slugs:
        if s not in installed:
            print(f"⏭ 未安装 {s}")
            continue
        write_baseline(installed[s]["dir"])
        print(f"✅ 已建立快照：{s}")
        n += 1
    print(f"共 {n} 个")
    return 0


def cmd_autorun(args):
    """供宿主调度器调用的一次性动作：自动应用「同主版本 + 无本地改动」的更新。

    铁律：未显式开启（autoupdate --on）时什么也不做 —— 默认不改机器。
    本技能自身不注册任何定时调度（不在后台常驻），定时由宿主负责，见 cmd_autoupdate。
    """
    cfg = load_config()
    if not cfg.get("auto_check_enabled"):
        print("⏭ 自动更新未开启（先跑 autoupdate --on 开启）。本次不改动任何文件。")
        return 0
    print(f"[autorun] {datetime.datetime.now():%Y-%m-%d %H:%M} 自动检查并应用安全更新")
    return cmd_apply(argparse.Namespace(
        slug=None, safe_only=True, allow_major=False,
        force_overwrite=False, dry_run=args.dry_run, offline_install=False,
        execute=args.execute))


def cmd_autoupdate(args):
    cfg = load_config()
    if args.on:
        cfg["auto_check_enabled"] = True
        save_config(cfg)
        print("✅ 已开启自动更新策略（只自动应用「同主版本 + 无本地改动」的更新）")
        print()
        print("⚠ 本技能自身不含定时调度器 —— 开启只是把「允许自动应用」这个开关打开。")
        print("   要真正做到每天检查，需要由你的宿主定时调用：")
        print()
        print("     python scripts/skill_sync.py autorun")
        print()
        print("   三种可接的调度方式（任选其一）：")
        print("   · WorkBuddy：新建自动化，提示词写「跑一次技能更新自动检查」，周期每天")
        print("   · Windows 计划任务：schtasks /create /tn cjg-skill-sync /sc daily /st 09:00 \\")
        print("       /tr \"python <技能目录>\\scripts\\skill_sync.py autorun\"")
        print("   · cron / CI：0 9 * * * cd <技能目录> && python scripts/skill_sync.py autorun")
        print()
        print("   autorun 在未开启时会自动跳过，不会改任何文件；开启后也只碰安全项。")
    elif args.off:
        cfg["auto_check_enabled"] = False
        save_config(cfg)
        print("✅ 已关闭自动更新（autorun 将跳过，本技能不会主动改动任何文件）")
    else:
        print(f"当前状态：{'开启' if cfg.get('auto_check_enabled') else '关闭（默认）'}")
        print(f"auto_apply_safe_only = {cfg.get('auto_apply_safe_only')}")
        print()
        print("说明：本技能不自带定时调度，需由宿主定时调用 autorun；")
        print("      开启仅表示「允许被调度时自动应用安全更新」。")
    return 0


def main():
    ap = argparse.ArgumentParser(description="技能更新助手")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="只检查，不动任何文件")
    p.add_argument("--slug", help="只看这一个技能（默认全列，技能多时刷屏）")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--offline", action="store_true", help="不联网")
    p.add_argument("--no-baseline", action="store_true", help="不自动补建快照")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("apply", help="应用更新")
    p.add_argument("--slug")
    p.add_argument("--safe-only", action="store_true", help="只应用可安全自动更新的")
    p.add_argument("--allow-major", action="store_true", help="允许主版本升级")
    p.add_argument("--force-overwrite", action="store_true", help="覆盖本地改动")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--offline-install", action="store_true", help="只备份不安装")
    p.add_argument("--execute", action="store_true",
                   help="调用平台 CLI 真实安装（默认只给命令，不动机器）")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("gate", help="调用门闸：技能脚本执行前校验版本策略（输出 JSON，fail-open）")
    p.add_argument("--slug", required=True)
    p.add_argument("--local", help="本地版本（缺省则读已装技能 frontmatter）")
    p.add_argument("--timeout", type=int, default=2, help="索引查询超时秒数（默认 2，超时 fail-open）")
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("rollback", help="回滚到最近备份")
    p.add_argument("--slug", required=True)
    p.add_argument("--backup")
    p.set_defaults(func=cmd_rollback)

    p = sub.add_parser("baseline", help="建立安装快照")
    p.add_argument("--slug")
    p.set_defaults(func=cmd_baseline)

    p = sub.add_parser("autoupdate", help="开关自动更新策略（默认关）")
    p.add_argument("--on", action="store_true")
    p.add_argument("--off", action="store_true")
    p.set_defaults(func=cmd_autoupdate)

    p = sub.add_parser("autorun", help="供宿主定时调用：自动应用安全更新（需已 --on）")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--execute", action="store_true",
                   help="同时用平台 CLI 真实安装（默认只备份+给命令）")
    p.set_defaults(func=cmd_autorun)

    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
