#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_ledgers_to_feishu.py — 把第5/6步台账 + 流程状态表同步到飞书云文档

🔴🔴 隐私红线（不可改、不可绕过）
────────────────────────────────────────────────────────────
只有 **第5步/第6步** 台账允许上传。**第7步（持仓中/）的台账永不上传**，
持仓数量、成本、盈亏、金额一律不出本机。
实现方式是**目录级硬排除**：脚本根本不打开 `持仓中/` 下的任何文件，
不是「读了再过滤」，而是「不读」——避免未来新增字段时漏过滤。
"""
import os
import json, os, pathlib, re, subprocess, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_guard import fetch_status
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )

# ── Hermes 主目录（可选；未设置时依赖它的功能跳过，不报错）──────────────
_H = os.environ.get("HERMES_HOME", "").rstrip("/")


BASE = pathlib.Path(_D + "/股票台账")
CAND = BASE / "候选"                    # 第5/6步台账
POSI = BASE / "持仓中"                   # 🔴 第7步台账 —— 永不读取
STATE = BASE / "流程状态表.md"
WRITER = _H + "/skills/feishu/feishu-doc-sync/scripts/feishu_doc_write.py"
INDEX = pathlib.Path(_D + "/.feishu_docs.json")   # 台账名 → doc_token

# ⭐ 目标飞书文件夹（**你自己的** token，从环境变量读；未配置则整条同步跳过）
#   根目录 token：  FEISHU_FOLDER_TOKEN=<根文件夹 token>
#   子目录映射：    FEISHU_FOLDER_SUBDIR='{"ledgers":"...","status":"...","todo":"..."}'
#   🔴 禁止新建文件夹：先在你的飞书云空间建好目录，把 token 填进环境变量。
FEISHU_FOLDER = os.environ.get("FEISHU_FOLDER_TOKEN", "").strip()
try:
    FEISHU_SUBDIR = json.loads(os.environ.get("FEISHU_FOLDER_SUBDIR", "{}") or "{}")
except Exception:
    FEISHU_SUBDIR = {}

# 各功能文件夹 token（全部从环境变量读；缺失 → 该功能跳过，不报错）
FOLDERS = {
    "root":      FEISHU_FOLDER,
    "ledgers":   FEISHU_SUBDIR.get("ledgers", ""),
    "status":    FEISHU_SUBDIR.get("status", ""),
    "todo":      FEISHU_SUBDIR.get("todo", ""),
    "direction": os.environ.get("FEISHU_FOLDER_DIRECTION", "").strip(),
    "notice":    os.environ.get("FEISHU_FOLDER_NOTICE", "").strip(),
}
TODO = BASE / "待办与时点.md"

# 🔴 硬排除：这些目录/文件永远不进入同步范围
FORBIDDEN = (POSI,)

def guard(path: pathlib.Path) -> None:
    """🔴 同步前强制校验路径。命中第7步目录立即终止整个进程。"""
    rp = path.resolve()
    for f in FORBIDDEN:
        if f.resolve() == rp or rp.is_relative_to(f.resolve()):
            sys.exit(f"🔴 拒绝同步第7步持仓台账：{path}")

def load_index() -> dict:
    """🔴 索引读不到 = 台账同步会全部走「新建文档」，产生重复文档。
    原来静默返回空 dict —— 现在直接终止，让看门狗/用户发现。"""
    if not INDEX.exists():
        sys.exit(f"🔴 取数失败 · 飞书文档索引不存在：{INDEX}\n"
                 f"   首次使用须先创建索引，否则每份台账都会新建重复文档。")
    try:
        d = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.exit(f"🔴 取数失败 · 索引解析失败（可能被写坏）：{type(exc).__name__}: {exc}\n"
                 f"   文件：{INDEX}\n"
                 f"   🔴 不要重新生成 —— 会导致飞书上出现重复台账文档。先人工修复。")
    for k in ("folder_token", "status_doc", "ledgers"):
        if k not in d:
            sys.exit(f"🔴 取数失败 · 索引缺字段 '{k}'：{INDEX}")
    return d

def save_index(d: dict) -> None:
    INDEX.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def token() -> str:
    """飞书 tenant_access_token。

    🔴 凭证取不到 = 「没配置飞书」，**跳过而不报错**（原实现在这里 sys.exit 报故障，
       对没配飞书的使用者是假故障）。优先环境变量，其次 .env 文件。
    """
    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    if not (app_id and app_secret):
        candidates = ([pathlib.Path(_H + "/.env")] if _H else []) + \
                     [pathlib.Path(_D + "/.env")]
        for envf in candidates:
            if not envf.is_file():
                continue
            env = {}
            try:
                for line in envf.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            except Exception:  # noqa: BLE001
                continue
            app_id = app_id or env.get("FEISHU_APP_ID", "")
            app_secret = app_secret or env.get("FEISHU_APP_SECRET", "")
            if app_id and app_secret:
                break
    if not (app_id and app_secret):
        print("ℹ️ 未配置飞书凭据（FEISHU_APP_ID / FEISHU_APP_SECRET）→ 跳过飞书同步。"
              "配置方法见 README。", file=sys.stderr)
        raise SystemExit(0)

    def _do():
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=json.dumps({"app_id": app_id,
                             "app_secret": app_secret}).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        r = json.load(urllib.request.urlopen(req, timeout=25))
        if r.get("code") != 0:
            raise ValueError(f"code={r.get('code')} msg={r.get('msg')}")
        return r["tenant_access_token"]

    res = fetch_status(_do, tries=2, delay=1.0)
    if res.failed:
        sys.exit(f"🔴 取数失败 · 飞书鉴权失败：{res.error}\n"
                 f"   台账**未同步**到云端，本地台账不受影响。")
    return res.value

def api(method: str, T: str, path: str, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis" + path, data=body,
        headers={"Authorization": f"Bearer {T}",
                 "Content-Type": "application/json; charset=utf-8"}, method=method)
    try:
        r = json.load(urllib.request.urlopen(req, timeout=40))
    except urllib.error.HTTPError as e:
        return {"code": -1, "msg": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as exc:
        # 🔴 原来只捕 HTTPError，超时/连接重置会直接抛出中断整个同步
        return {"code": -2, "msg": f"{type(exc).__name__}: {exc}"}
    return r

def write_doc(src: pathlib.Path, doc_token: str, real_table: bool = False) -> tuple[bool, str]:
    """🔴 real_table=True 走飞书原生表格（带网格线）。

    ⭐ 本工作流决定：**只给 流程状态表 + 待办与时点 开真表格**，
    15 份候选台账继续用 ` | ` 文本行 —— 台账主要是我读写；
    而真表格一份要 2–4 分钟（逐 cell PATCH + 429 节流），17 份会跑 30–60 分钟。
    """
    guard(src)
    cmd = ["python3", WRITER, str(src), "--doc", doc_token]
    if real_table:
        cmd.append("--real-table")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    tail = (r.stdout or r.stderr).strip().splitlines()
    return r.returncode == 0, (tail[-1] if tail else "")

def ensure_doc(T: str, folder: str, title: str, old: str = "") -> str:
    if old:
        return old
    r = api("POST", T, "/docx/v1/documents", {"folder_token": folder, "title": title})
    return (r.get("data") or {}).get("document", {}).get("document_id", "")

def main() -> None:
    if not FEISHU_FOLDER or not FEISHU_SUBDIR.get("ledgers"):
        print("ℹ️ 未配置飞书文件夹 token（FEISHU_FOLDER_TOKEN / FEISHU_FOLDER_SUBDIR）"
              "→ 跳过飞书同步。配置方法见 README。", file=sys.stderr)
        return
    idx = load_index()
    T = token()
    folder = FEISHU_FOLDER
    ledgers_dir = FEISHU_SUBDIR["ledgers"]
    idx["folder_token"] = folder
    # ① 状态表：直接写进用户已有文档（替换模式会先清空）
    idx["status_doc"] = FEISHU_SUBDIR["status"]
    # ② 候选台账（第5/6步）
    try:
        files = sorted(CAND.glob("*_跟踪台账.md"))
    except Exception as exc:
        sys.exit(f"🔴 取数失败 · 候选台账目录扫描失败：{type(exc).__name__}: {exc}")
    for f in files:
        guard(f)
    ok = bad = 0
    errors = []          # 🔴 逐份失败原因，不能只留一个计数
    for f in files:
        name = f.stem.replace("_跟踪台账", "")
        doc = idx["ledgers"].get(name, "")
        if not doc:
            r = api("POST", T, "/docx/v1/documents",
                    {"folder_token": ledgers_dir, "title": f"{name} 跟踪台账"})
            doc = (r.get("data") or {}).get("document", {}).get("document_id", "")
            if not doc:
                msg = f"{name}：建文档失败 {r.get('msg')}"
                print(f"  ❌ {msg}")
                errors.append(msg); bad += 1; continue
            # 🔴 建完**立刻**落盘索引：曾实测——脚本若在建完文档后被超时
            #    杀掉（exit 124），token 没写进索引 → 下次重跑再建一份，飞书上出现重名。
            #    曾有多份台账因此被重复创建（同一份建出 3 份重名文档）。
            idx["ledgers"][name] = doc
            save_index(idx)
        good, msg = write_doc(f, doc)
        if good:
            idx["ledgers"][name] = doc
        else:
            errors.append(f"{name} 写入失败：{msg}")
        print(f"  {'✅' if good else '❌'} {name}  {msg[:56]}")
        ok += good; bad += (not good)
    good, msg = write_doc(STATE, idx["status_doc"])          # 🔴 不传 real_table：表格降级为文本行
    print(f"  {'✅' if good else '❌'} 流程状态表  {msg[:56]}")
    if not good:
        errors.append(f"流程状态表 写入失败：{msg}")
    ok += good; bad += (not good)
    # ③ 待办与关键时点（无隐私内容）
    if TODO.exists():
        guard(TODO)
        good, msg = write_doc(TODO, FEISHU_SUBDIR["todo"])       # 🔴 同上
        print(f"  {'✅' if good else '❌'} 待办与关键时点  {msg[:50]}")
        if not good:
            errors.append(f"待办与关键时点 写入失败：{msg}")
        ok += good; bad += (not good)
    else:
        # 🔴 原来只 print 一句就过 —— 文件丢失等于云端少一份文档，无人知晓
        msg = f"待办文件不存在：{TODO}"
        print(f"  ⚠️ {msg}")
        errors.append(msg); bad += 1
    save_index(idx)
    print(f"\n📊 成功 {ok}｜失败 {bad}")
    print(f"📁 目标：01_候选台账 ＋ 股票流程状态表 ＋ 待办与关键时点（{ledgers_dir}）＋ 股票流程状态表")
    print(f"🔴 已跳过（第7步，永不上传）：{POSI.name}/ 共 "
          f"{len(list(POSI.glob('*.md')))} 份")

    # ④ 台账 ↔ 流程状态表 一致性校验（全步骤 第2–8步）
    # 🔴 新增：防"建了台账忘更新状态表" / "删了台账忘清状态表"
    #    不一致时打印告警 → no_agent 的 stdout 非空即投递，用户会在周一收到
    print()
    try:
        r = subprocess.run(
            ["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_ledgers.py")],
            capture_output=True, text=True, timeout=180)
        out = (r.stdout or "") + (r.stderr or "")
        warns = [l.strip() for l in out.split("\n")
                 if l.strip().startswith("🔴")
                 and ("流程状态" in l or "台账" in l or "登记" in l or "脚本漂移" in l)]
        if "流程状态表一致性：" in out or warns:
            print("🔴🔴 校验器告警（台账↔流程状态表 / cron 脚本漂移）——需人工修正：")
            for w in warns or ["（解析异常，请手动跑 validate_ledgers.py）"]:
                print(f"   {w}")
        else:
            print("✅ 台账 ↔ 流程状态表 一致性通过（全步骤 第2–8步）")
    except Exception as e:
        print(f"⚠️ 一致性校验未执行：{e}")
        errors.append(f"一致性校验未执行：{type(e).__name__}: {e}")

    # 🔴 失败明细：no_agent 判定是「stdout 非空即投递」，
    #    这里把逐份原因打出来，周一用户能看到到底哪几份没同步上云。
    if errors:
        print()
        print(f"🔴🔴 本次同步 {len(errors)} 项失败（云端与本地不一致，需人工处理）：")
        for e in errors:
            print(f"   · {e}")


if __name__ == "__main__":
    main()