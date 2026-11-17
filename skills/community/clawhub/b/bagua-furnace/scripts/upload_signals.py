#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upload_signals.py — 藏经阁·易筋 信号上传器（共享 · 确定性 · 去智能体化）

扫描 base 下所有含 references/signals.md 的技能，对每个技能：
  1. bootstrap 状态文件（.optin / .anon_id / .cloud_optin）
  2. 读 signals-log.jsonl，逐行解析 signal_id，跳过 .uploaded_ids.txt 已传
  3. 标准映射（带 signal_id 幂等键）POST 到 cloud_config.json 的 ingest_url + /ingest/anon
  4. 逐行原子确认：每条 200 后追加 signal_id 到 .uploaded_ids.txt 并 flush
  5. 失败处理：网络/5xx 重试≤3（失败不标记留本地）；429 停本轮；4xx 永久失败进 .errored_ids.txt
  6. 死信：连续 7 轮"有未传行 + 服务端持续报错 + 0 成功" → 移入 signals-log.dead.jsonl

设计要点（评审 §3 改动 C + 四问）：
  - 离线 = 本地排队不丢：网络失败的行不写 .uploaded_ids.txt，下轮续传。
  - 断点续传：逐行 200 后立刻 flush 副索引，中途被杀已确认跳过、未确认续。
  - 防重复：客户端 .uploaded_ids.txt 副索引 + 服务端 UNIQUE(client_signal_id) 双保险。
  - 隐私：只读白名单字段，绝不读用户文件；失败静默。

依赖：仅 Python 3 标准库（urllib / json / uuid / hashlib / time）。
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

# 端点完全来自外部配置（cloud_config.json / 环境变量 CJG_INGEST_URL），
# 代码中不硬编码任何 URL —— 配置缺失则跳过云端上传（本地记录照常）。
ANON_PATH = "/ingest/anon"

# 死信阈值：连续多少轮"有未传行 + 服务端持续报错 + 0 成功"触发
DEAD_ROUNDS_THRESHOLD = 7

# 重试：网络/5xx 最多重试次数 + 指数退避基准（秒）
MAX_RETRY = 3
BACKOFF_BASE = 2.0

# 标准白名单字段（本地 → 云端）
EVENTS = {"helpful", "unhelpful", "confusion", "suggestion", "abandoned", "misdiagnosis",
          "accept", "reject", "iteration", "edit_capture",
          "usage_call", "usage_error", "usage_slow", "no_signoff",
          "action_trace"}   # G1 客观事件 + G4 缺失检测哨兵 + P1-4 动作链遥测

# P0 闭环质量新增字段（透传；剥字段降级时排除这些）
NEW_FIELDS = {"accepted", "revision_rounds", "feedback_tag", "recurrence",
              "attribution", "attribution_note",
              "metric",                                       # G1 客观指标（对象，服务端校验后落库 metric_json）
              "action_name", "action_outcome"}                # P1-4 动作链遥测（白名单方法层标签 + 结果枚举）


def _is_schema_reject(err_text):
    """GAP-2/兼容性降级判定：服务端是否因「结构未就绪」拒绝——

    - "unknown column"（迁移尚未跑的列竞态窗口）
    - "白名单外字段"（服务端白名单尚未含新增字段的竞态窗口）
    任一命中即剥 NEW_FIELDS 重试一次，使新字段上线前后都能优雅降级、不丢基础信号。
    """
    if not err_text:
        return False
    t = err_text.lower()
    return ("unknown column" in t) or ("白名单外字段" in t) or ("未知列" in t)


def resolve_ingest_url(skill_dir):
    """云端端点完全来自外部配置，不在代码中硬编码。

    优先级：环境变量 CJG_INGEST_URL → 技能目录 cloud_config.json(ingest_url)
    → 创作者本机密钥目录 cloud_config.json(ingest_url)。都缺失返回 None（跳过云端上传）。
    """
    env = os.environ.get("CJG_INGEST_URL")
    if env:
        return env.strip().rstrip("/") + ANON_PATH
    cands = [
        os.path.join(skill_dir, "cloud_config.json"),
        os.path.expanduser("~/.workbuddy/secrets/cjg-evo/cloud_config.json"),
    ]
    for cc in cands:
        if os.path.exists(cc):
            try:
                with open(cc, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                u = (cfg.get("ingest_url") or "").strip()
                if u:
                    return u.rstrip("/") + ANON_PATH
            except Exception:
                pass
    return None

LAYERS = {"L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7"}  # L0=客观层（G1 客观事件 usage_* 固定）


def log(msg):
    # 仅输出极简进度；失败静默不喧宾夺主
    print("[upload_signals] " + msg, flush=True)


def read_state_file(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def write_state_file(path, value):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(value)
        return True
    except Exception:
        return False


def bootstrap(skill_dir):
    """确定性补齐状态文件：.optin=on / .anon_id=uuid / .cloud_optin=off（缺失才建；云端默认关，需显式开启云同步）。"""
    created = []
    optin = os.path.join(skill_dir, ".optin")
    if not os.path.exists(optin):
        if write_state_file(optin, "on"):
            created.append(".optin")
    anon = os.path.join(skill_dir, ".anon_id")
    if not os.path.exists(anon):
        import uuid
        if write_state_file(anon, str(uuid.uuid4())):
            created.append(".anon_id")
    cloud = os.path.join(skill_dir, ".cloud_optin")
    if not os.path.exists(cloud):
        if write_state_file(cloud, "off"):
            created.append(".cloud_optin")
    return created


def load_uploaded(path):
    s = set()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        s.add(line)
        except Exception:
            pass
    return s


def append_uploaded(path, cid):
    """逐行原子确认：追加 signal_id 并 flush（断点续传关键）。"""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(cid + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception:
        return False


def client_signal_id(obj, raw_line):
    """幂等键：优先用采集时生成的 signal_id；缺失则用行内容 hash（稳定、可去重）。"""
    sid = obj.get("signal_id")
    if isinstance(sid, str) and sid.strip():
        return sid.strip()
    h = hashlib.sha256(raw_line.rstrip(b"\n").strip()).hexdigest()[:32]
    return "h-" + h


def build_payload(obj, anon_id_fallback):
    """标准映射：只取白名单字段，带 signal_id 幂等键。"""
    slug = obj.get("skill_slug") or obj.get("slug")
    method_layer = obj.get("method_layer")
    event = obj.get("event")
    weight = obj.get("weight")
    note = obj.get("note") or obj.get("trigger_class")
    anon_id = obj.get("anon_id") or anon_id_fallback
    skill_version = obj.get("skill_version")

    # 规范化 weight → int 1..5
    try:
        weight = int(weight)
    except (TypeError, ValueError):
        weight = 1
    if weight < 1:
        weight = 1
    if weight > 5:
        weight = 5

    payload = {
        "slug": slug,
        "method_layer": method_layer,
        "event": event,
        "weight": weight,
        "note": note,
        "anon_id": anon_id or "",
        "skill_version": skill_version,
        "mode": "cloud",
    }
    # P0 闭环质量：透传新增字段（非 None 才塞，保持向后兼容）
    for nf in NEW_FIELDS:
        val = obj.get(nf)
        if val is not None:
            payload[nf] = val
    # client_signal_id（幂等键）由调用方用稳定的 cid 填充
    return payload


def post_signal(url, payload, timeout=10):
    """返回 (status, ok_bool, category, anon_id, err_text)。

    anon_id：服务端签发的稳定匿名 ID（仅 2xx 且有 body 时非空）。
    err_text：错误响应体文本（GAP-2 降级判定用；成功时为空串）。
    客户端据此回写 .anon_id 文件，使同机后续上传复用 → 人数去重准确。
    """
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            anon_id = ""
            if 200 <= status < 300:
                try:
                    anon_id = (json.loads(resp.read().decode("utf-8")) or {}).get("anon_id", "")
                except Exception:
                    anon_id = ""
                return status, True, "ok", anon_id, ""
            if status == 429:
                return status, False, "stop", "", ""
            if 400 <= status < 500:
                try:
                    body = resp.read().decode("utf-8", errors="replace")
                except Exception:
                    body = ""
                return status, False, "perm", "", body
            return status, False, "retry", "", ""  # 5xx 等
    except urllib.error.HTTPError as e:
        status = e.code
        if status == 429:
            return status, False, "stop", "", ""
        if 400 <= status < 500:
            try:
                body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            except Exception:
                body = ""
            return status, False, "perm", "", body
        return status, False, "retry", "", ""
    except (urllib.error.URLError, TimeoutError, OSError, ConnectionError):
        # 网络不可达 / 超时 / DNS 失败 → 离线排队，不计入死信
        return -1, False, "net", "", ""
    except Exception:
        return -2, False, "net", "", ""


def process_skill(skill_dir, dry_run=False):
    name = os.path.basename(skill_dir)
    signals_md = os.path.join(skill_dir, "references", "signals.md")
    if not os.path.exists(signals_md):
        return None  # 非信号技能，跳过

    created = bootstrap(skill_dir)
    if created:
        log(f"[{name}] bootstrap 新建状态文件: {', '.join(created)}")

    # 云端授权检查
    cloud_optin = read_state_file(os.path.join(skill_dir, ".cloud_optin"))
    if cloud_optin == "off":
        log(f"[{name}] .cloud_optin=off，跳过云端上传（本地记录照常）")
        return 0, []

    log_path = os.path.join(skill_dir, "signals-log.jsonl")
    if not os.path.exists(log_path):
        return 0, []

    anon_id = read_state_file(os.path.join(skill_dir, ".anon_id")) or ""

    # 读取端点（仅来自外部配置 / 环境变量；代码中不硬编码任何 URL）
    url = resolve_ingest_url(skill_dir)
    if not url:
        log(f"[{name}] 未配置云端端点（缺 cloud_config.json 且无 CJG_INGEST_URL）→ 跳过云端上传（本地记录照常）")
        return 0, []

    uploaded = load_uploaded(os.path.join(skill_dir, ".uploaded_ids.txt"))
    errored = load_uploaded(os.path.join(skill_dir, ".errored_ids.txt"))

    # 读全部行（保留原始字节以稳定 hash）
    try:
        with open(log_path, "rb") as f:
            raw_lines = f.read().split(b"\n")
    except Exception:
        return 0, []

    pending_before = 0
    uploaded_now = 0
    uploaded_details = []  # 本次成功上传的 (method_layer, event) 明细，用于给用户列清楚
    conn_failed = 0
    server_failed = 0
    dead_candidates = []  # 未传且未永久失败的行（原始 bytes）

    for raw in raw_lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw.decode("utf-8"))
        except Exception:
            # 损坏行：当作永久失败（不阻塞），进 errored
            cid = "h-" + hashlib.sha256(raw).hexdigest()[:32]
            if cid not in errored and not dry_run:
                errored.add(cid)
                append_uploaded(os.path.join(skill_dir, ".errored_ids.txt"), cid)
            continue

        cid = client_signal_id(obj, raw)
        if cid in uploaded or cid in errored:
            continue  # 已处理，跳过

        pending_before += 1

        # 必要字段校验
        slug = obj.get("skill_slug") or obj.get("slug")
        method_layer = obj.get("method_layer")
        event = obj.get("event")
        if not slug or method_layer not in LAYERS or event not in EVENTS:
            # 缺必要字段 → 永久失败，移出主循环（避免无限重试）
            if not dry_run:
                errored.add(cid)
                append_uploaded(os.path.join(skill_dir, ".errored_ids.txt"), cid)
            log(f"[{name}] 跳过缺字段行 signal_id={cid} (slug={slug} layer={method_layer} event={event})")
            continue

        # 构造 payload（含 client_signal_id）
        payload = build_payload(obj, anon_id)
        payload["client_signal_id"] = cid

        if dry_run:
            uploaded_now += 1
            continue

        # 上传 + 重试（含 GAP-2 优雅降级：unknown column → 剥新字段重试一次）
        ok = False
        category = "net"
        returned_anon = ""
        err_text = ""
        gap2_stripped = False  # 是否已执行过剥字段降级
        for attempt in range(MAX_RETRY + 1):
            status, ok, category, returned_anon, err_text = post_signal(url, payload)
            if ok:
                break
            # GAP-2：首次遇到结构未就绪（未知列 / 白名单外字段）→ 剥新字段重试一次（迁移竞态窗口）
            if not gap2_stripped and _is_schema_reject(err_text):
                log(f"[{name}] GAP-2 降级：服务端结构未就绪(迁移未跑?)，剥 {len(NEW_FIELDS)} 个新字段重试 signal_id={cid}")
                for nf in NEW_FIELDS:
                    payload.pop(nf, None)
                gap2_stripped = True
                continue  # 用精简 payload 重试（不计入 attempt）
            if category == "stop":
                # 429：立即停本轮
                log(f"[{name}] 收到 429 限流，停止本轮批量（下轮续传）")
                return uploaded_now, uploaded_details
            if category == "perm":
                # 4xx 永久失败
                server_failed += 1
                errored.add(cid)
                append_uploaded(os.path.join(skill_dir, ".errored_ids.txt"), cid)
                log(f"[{name}] 永久失败 signal_id={cid} status={status}")
                ok = False
                break
            if category == "net":
                conn_failed += 1
                # 网络失败：不标记，留本地排队；退避后重试
                if attempt < MAX_RETRY:
                    time.sleep(BACKOFF_BASE * (2 ** attempt))
                continue
            # retry（5xx）：退避后重试
            server_failed += 1
            if attempt < MAX_RETRY:
                time.sleep(BACKOFF_BASE * (2 ** attempt))

        if ok:
            append_uploaded(os.path.join(skill_dir, ".uploaded_ids.txt"), cid)
            uploaded_now += 1
            uploaded_details.append((method_layer, event))
            # A-fix：回存服务端签发的稳定 anon_id（覆盖 bootstrap 的裸 uuid4）；
            # 同机后续上传复用 → COUNT(DISTINCT anon_id) 才能正确去重人数。
            if returned_anon and returned_anon != anon_id:
                anon_id = returned_anon
                write_state_file(os.path.join(skill_dir, ".anon_id"), returned_anon)
        else:
            # 未成功：留本地（不在 uploaded/errored 中），下轮续传
            dead_candidates.append(raw)

    # 死信判定：有未传行 + 服务端持续报错 + 0 成功（网络离线不计死信，保留队列）
    zero_rounds_path = os.path.join(skill_dir, ".upload_zero_rounds")
    zr = 0
    try:
        v = read_state_file(zero_rounds_path)
        if v is not None:
            zr = int(v)
    except Exception:
        zr = 0

    pending_after = len(dead_candidates)
    if pending_before > 0:
        if uploaded_now > 0:
            zr = 0
        elif conn_failed > 0:
            zr = 0  # 纯离线，保留队列，不惩罚
        else:
            zr += 1

        if zr >= DEAD_ROUNDS_THRESHOLD and pending_after > 0 and not dry_run:
            # 移入死信
            dead_path = os.path.join(skill_dir, "signals-log.dead.jsonl")
            try:
                with open(dead_path, "a", encoding="utf-8") as df:
                    for raw in dead_candidates:
                        df.write(raw.decode("utf-8") + "\n")
                # 重写 jsonl，剔除死信行
                keep = [raw for raw in raw_lines if raw.strip() and raw not in dead_candidates]
                with open(log_path, "w", encoding="utf-8") as wf:
                    for raw in keep:
                        wf.write(raw.decode("utf-8") + "\n")
                write_state_file(
                    os.path.join(skill_dir, ".upload_error"),
                    "dead-lettered after %d zero-success rounds; see signals-log.dead.jsonl" % zr,
                )
                log(f"[{name}] 连续 {zr} 轮零成功 → 死信 {pending_after} 行移入 signals-log.dead.jsonl")
                zr = 0
            except Exception as e:
                log(f"[{name}] 死信处理失败: {e}")
        write_state_file(zero_rounds_path, str(zr))

    return uploaded_now, uploaded_details


def main():
    parser = argparse.ArgumentParser(description="藏经阁·易筋 信号上传器")
    parser.add_argument(
        "--base",
        default=os.path.expanduser("~/.workbuddy/skills"),
        help="技能基目录（默认 ~/.workbuddy/skills）",
    )
    parser.add_argument("--dry-run", action="store_true", help="只统计待传行数，不发送")
    args = parser.parse_args()

    base = os.path.expanduser(args.base)
    if not os.path.isdir(base):
        log(f"基目录不存在: {base}")
        return 1

    total = 0
    skills_scanned = 0
    breakdown = {}  # 技能名 -> [(method_layer, event), ...]
    for entry in sorted(os.listdir(base)):
        skill_dir = os.path.join(base, entry)
        if not os.path.isdir(skill_dir):
            continue
        res = process_skill(skill_dir, dry_run=args.dry_run)
        if res is not None:
            skills_scanned += 1
            cnt, details = res
            total += cnt
            if details:
                breakdown[entry] = details

    # 给用户看清楚"本次到底传了什么"（全部是方法层标签，零对话内容/零个人信息）
    if args.dry_run:
        log(f"dry-run 完成：扫描 {skills_scanned} 个信号技能，本应上传 {total} 条")
    else:
        log(f"完成：扫描 {skills_scanned} 个信号技能，本次成功上传 {total} 条")
        if total == 0:
            log("本轮无新增信号需上传（昨天没产生新反馈，任务已检查完毕）")
        else:
            log("本次上传明细（全部为方法层标签，不含任何对话内容或个人隐私）：")
            for name, details in breakdown.items():
                # 按 (层码, 事件) 聚合计数
                agg = {}
                for layer, ev in details:
                    agg[(layer, ev)] = agg.get((layer, ev), 0) + 1
                parts = "、".join(f"{layer}·{ev}×{c}" for (layer, ev), c in sorted(agg.items()))
                log(f"  {name}: {len(details)} 条（{parts}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
