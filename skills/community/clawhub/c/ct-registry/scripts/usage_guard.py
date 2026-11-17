#!/usr/bin/env python3
"""usage_guard.py - Daily call-limit guard for shared external-workflow retrieval.

WHY (ct-registry policy, user rule 2026-07-28, shipped in v0.3.1)
-----------------------------------------------------------------
WHO / CDE retrieval is currently offered **free of charge**, but it rides on a
*shared* third-party endpoint (the Coze /run workflow). To keep that shared
resource minimally occupied:

  1. WHO / CDE and the other external-workflow sources (ChiCTR / ISRCTN / DRKS)
     all consume the SAME shared endpoint, so they share ONE daily budget.
  2. Hard cap: **100 retrieval calls per day** (local time, rolls over at midnight).
  3. A counted call prints a one-line confirmation; the remaining quota is NOT
     echoed on every call (user rule 2026-08-03) — only the hard block at the cap.
  4. At the cap -> the call is BLOCKED with "come back tomorrow" + a pointer to
     contact the skill author for bulk / coordinated retrieval.

What counts as a "call": every real network retrieval against the shared endpoint
(i.e. when `--run` is set), regardless of source. Preview (`--run` absent),
the direct Tier-1 sources (CT.gov v2, EU CTR HTML parse,
PubChem) are NOT counted — they don't hit the shared workflow.

DEMAND-BASED DEDUP (user rule 2026-07-29, shipped in v0.3.5)
-----------------------------------------------------------
The 100/day cap is charged **per retrieval DEMAND (a user request)**, NOT per raw
HTTP call. A "demand" is identified by `demand_id`:
  * One `ct_registry.py --run` invocation = ONE demand. WHO + CDE + any keyword
    tweaks / re-runs inside that one run all share ONE demand_id and cost 1 call.
  * When the agent searches step-by-step (e.g. CDE list, then CDE detail, then WHO),
    it reuses the SAME `demand_id` (via `--demand-id` or env `CT_DEMAND_ID`) so all
    those calls collapse to 1 counted call.
  * The same `demand_id` seen again on the same day is NOT re-counted (idempotent) —
    adjusting filters or repeating the same search does not burn extra quota.
So: "a demand = 1 call; WHO+CDE merged; tweaks/repeats within a demand are free."

Fail-open: if the counter file can't be read/written, we WARN but do NOT block,
so a corrupted counter can never wedge the skill.

State file: ~/.workbuddy/skills/ct-registry/config/usage.json
  {"date": "YYYY-MM-DD", "count": <int>, "demands": ["<demand_id>", ...]}
"""
import datetime
import json
import os
import time

DAILY_LIMIT = 1000  # 用户 2026-10-23 明确：WHO/CDE 共享端点每日配额由 100 调整为 1000（取代 2026-08-12 的 100）
# State file: default packaged path. Overridable via CT_USAGE_CONFIG so that
# tests / CI / parallel sandboxes use an ISOLATED counter and never drain the
# real shared daily quota (shipped in v0.3.47 regression-hardening).
def _usage_path():
    return os.environ.get("CT_USAGE_CONFIG") or os.path.expanduser(
        "~/.workbuddy/skills/ct-registry/config/usage.json")
USAGE_PATH = _usage_path()
AUTHOR_HINT = "（大批量检索需求请联系技能作者 Wintone 协调）"
# Req2: make the "free but capped" policy explicit in every quota message.
QUOTA_NOTE = ("当前免费使用；为充分利用共享资源，每日上限 1000 个需求（按 demand_id 计），"
              "配额与资源使用详情见 README 的「配额与资源使用」小节。")


def _lock_path():
    return USAGE_PATH + ".lock"


def _with_lock(fn, *a, **k):
    """Serialize the read-modify-write of the shared usage counter across concurrent
    sessions (P1-7, 2026-08-12). Advisory lockfile; a stale lock (>120s old) is broken
    because a quota increment is sub-second. Fail-open: if the lock can't be taken we
    still run fn so a lock glitch can never wedge the skill.
    """
    lock = _lock_path()
    # 确保锁文件父目录存在（云端沙箱 ~ 展开为 /root/，但工作目录是 /workspace/，
    # ~/.workbuddy/skills/ct-registry/config/ 不存在，os.open O_CREAT 不会建父目录）
    lock_dir = os.path.dirname(lock)
    if lock_dir:
        os.makedirs(lock_dir, exist_ok=True)
    deadline = time.time() + 30
    acquired = False
    while time.time() < deadline:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            acquired = True
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock) > 120:
                    os.remove(lock)
                    continue
            except OSError:
                pass
            time.sleep(0.1)
    try:
        return fn(*a, **k)
    finally:
        if acquired:
            try:
                os.remove(lock)
            except OSError:
                pass


def _today():
    return datetime.date.today().isoformat()


def _load():
    if os.path.exists(USAGE_PATH):
        try:
            with open(USAGE_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"date": _today(), "count": 0, "demands": []}


def _save(data):
    os.makedirs(os.path.dirname(USAGE_PATH), exist_ok=True)
    with open(USAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _apply_check(demand_id, source_label):
    data = _load()
    today = _today()
    if data.get("date") != today:
        data = {"date": today, "count": 0, "demands": []}
    used = int(data.get("count", 0))
    demands = list(data.get("demands") or [])

    # Idempotent: same demand already counted today -> no extra charge.
    if demand_id and demand_id in demands:
        remaining = DAILY_LIMIT - used
        msg = (
            f"[usage-guard] 需求(demand_id={demand_id})今日已计入配额，"
            f"本次（WHO+CDE 合并 / 关键词微调 / 重复检索）不重复计数。")
        return True, remaining, msg

    if used >= DAILY_LIMIT:
        msg = (
            f"[usage-guard] 今日（{today}）对共享检索端点（{source_label}）的调用已达"
            f"每日上限 {DAILY_LIMIT} 次（按需求计，已达 {used} 个需求），本次不再执行。"
            f"{QUOTA_NOTE}请于明天（次日）0 点后再使用；如有大批量检索需求，请联系技能作者协调。{AUTHOR_HINT}")
        return False, 0, msg

    used += 1
    data["count"] = used
    if demand_id:
        demands.append(demand_id)
        data["demands"] = demands
    try:
        _save(data)
    except Exception as e:  # fail-open
        return True, DAILY_LIMIT - used, (
            f"[usage-guard] 本次为今日第 {used} 个需求（demand_id={demand_id or '无'}）共享检索调用，"
            f"计数器写入失败（{e}），未限制本次。")
    remaining = DAILY_LIMIT - used
    msg = (
        f"[usage-guard] 本次为今日第 {used} 个需求（demand_id={demand_id or '无'}）共享检索调用（每日上限 {DAILY_LIMIT} 次）。")
    return True, remaining, msg


def check(demand_id=None, source_label="WHO/CDE"):
    """Call BEFORE a real network retrieval against the shared endpoint.

    Charges **one counted call per demand_id** (idempotent within a day), NOT per
    raw HTTP call. WHO + CDE + keyword tweaks + repeats that share the same
    `demand_id` collapse to a single counted call.

    The read-modify-write of the shared counter is serialized via an advisory
    lockfile (P1-7) so concurrent AI sessions never corrupt usage.json.

    Returns (allowed: bool, remaining: int, msg: str).
    On allowed, increments + persists the daily counter (once per demand_id).
    """
    return _with_lock(_apply_check, demand_id, source_label)


def _apply_peek(demand_id):
    data = _load()
    today = _today()
    used = int(data.get("count", 0)) if data.get("date") == today else 0
    demands = list(data.get("demands") or [])
    # Idempotent: an already-counted demand is never blocked, regardless of cap.
    if demand_id and demand_id in demands:
        return DAILY_LIMIT - used, False
    if used >= DAILY_LIMIT:
        return 0, True
    return DAILY_LIMIT - used, False


def peek(demand_id=None):
    """Non-mutating remaining-quota probe (R7: adaptive scheduling).

    Mirrors the date-roll + per-demand idempotency logic of check(), but
    NEVER increments or persists the counter — safe to call during preview
    or repeatedly before dispatch. Returns (remaining:int, blocked:bool):
      * same demand already counted today -> (remaining, False)
      * used >= DAILY_LIMIT                 -> (0, True)   # would be blocked
      * otherwise                           -> (remaining, False)

    Runs under the same advisory lockfile as check() (P1-7) so a concurrent
    increment can't produce a stale probe result.
    """
    return _with_lock(_apply_peek, demand_id)


if __name__ == "__main__":
    for _ in range(DAILY_LIMIT + 2):
        ok, rem, m = check()
        print(ok, rem, m)
        if not ok:
            break
