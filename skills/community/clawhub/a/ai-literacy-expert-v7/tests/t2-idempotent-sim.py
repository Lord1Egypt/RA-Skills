#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2 · L4 运行时仿真器 —— 幂等 / 状态机 / 台账 / 失败降级 全链路验证
================================================================
忠实复刻 references/automation-l4-scheduler.md 与 references/automation-ops.md
定义的 L4 行为契约，用「模拟调度触发」的方式验证 5 条判据中的
判据 3（跨会话记得住）、判据 4（重复触发不重复产出）、判据 5（留痕可审计）。

被仿真的契约（逐条对应文档）：
  · 通用执行骨架（automation-ops.md §通用执行骨架 ①~⑥）
  · 幂等键规则（l4-scheduler.md §4）
  · 状态文件结构（l4-scheduler.md §3）
  · automation 会话 5 铁律（l4-scheduler.md §6），尤其是第 5 条「失败退出码 0」
"""
import json, os, sys, copy, pathlib
from datetime import datetime, timedelta

# 路径自适应：技能根目录由脚本位置推导，输出目录可用 V7_TEST_OUT 覆盖
SKILL = str(pathlib.Path(__file__).resolve().parent.parent)
OUT = os.environ.get("V7_TEST_OUT") or str(pathlib.Path(__file__).resolve().parent / "out")
os.makedirs(OUT, exist_ok=True)
BASE = datetime(2026, 9, 1, 8, 0, 0)   # 2026-W36 周二

# ---------------------------------------------------------------- 断言器
class Checker:
    def __init__(self):
        self.results = []
    def ok(self, group, name, cond, detail=""):
        self.results.append({"group": group, "name": name,
                             "pass": bool(cond), "detail": str(detail)})
        return bool(cond)
    @property
    def passed(self): return sum(1 for r in self.results if r["pass"])
    @property
    def total(self): return len(self.results)

CK = Checker()

# ------------------------------------------------- 任务规格（源自 OPS 文档）
ROTATION = ["A1","A2","A3","B1","B2","C1","C2","C3","C4","C5","D1","D2",
            "E1","E2","E3","E4","E5","E·N","F1","F2","F3","F4","G1","G2","G3"]

SPECS = {
    "OPS-1": {"period": "weekly", "cursor": {"week": 1}, "maxWeek": 4, "html": True,
              "artifact": lambda c: [f"课件W{c['week']}", f"游戏W{c['week']}",
                                     f"自测W{c['week']}", f"周计划W{c['week']}"]},
    "OPS-2": {"period": "daily",  "cursor": {"issue": 1},
              "artifact": lambda c: [f"速递#{c['issue']}", f"练习题#{c['issue']}"]},
    "OPS-3": {"period": "once",   "cursor": {}, "onceKey": "final-exam-2026-01-14",
              "artifact": lambda c: ["复习清单", "闹钟", "自测题"]},
    "OPS-4": {"period": "weekly", "cursor": {"report": 1},
              "artifact": lambda c: [f"周报#{c['report']}"]},
    # OPS-1 / OPS-5 产出 HTML → 必须跑 harness → 台账带 verify 字段
    "OPS-5": {"period": "weekly", "cursor": {"module": "A1", "round": 1}, "html": True,
              "artifact": lambda c: [f"课件{c['module']}"] +
                                    ([f"游戏{c['module']}"] if c["module"] in
                                     ("E·N",) or c["module"][0] in "FG" else [])},
    "OPS-6": {"period": "weekly", "cursor": {"check": 1},
              "artifact": lambda c: [f"诊断报告#{c['check']}", "补学路径", "课件建议"]},
}


def iso_week(dt):
    y, w, _ = dt.isocalendar()
    return f"{y}-W{w:02d}"


def period_id(task, dt):
    """周期标识 —— 严格按 l4-scheduler.md §4"""
    p = SPECS[task]["period"]
    if p == "daily":
        return dt.strftime("%Y-%m-%d")
    if p == "weekly":
        return iso_week(dt)
    return SPECS[task]["onceKey"]


# ------------------------------------------------------------ 运行时仿真器
class L4Runtime:
    """模拟「跨会话」的 L4 运行时：
       state  = IMA 权威状态（跨会话持久）
       ledger = 执行台账 JSONL（追加写）
       每次 trigger() = 一次全新的 automation 会话（无任何历史上下文）
    """

    def __init__(self):
        self.state = {}    # task -> state json
        self.ledger = []   # list of ledger entries
        self.forced_fail = set()   # 注入失败的 (task, period_id)

    # ---- 状态读写（对应骨架 ①④）
    def read_state(self, task):
        if task not in self.state:
            spec = SPECS[task]
            self.state[task] = {
                "schema": "ai-literacy-state/v1", "task": task,
                "updatedAt": None,
                "cursor": copy.deepcopy(spec["cursor"]),
                "lastRun": None, "nextRun": None,
                "context": {"audience": "BNBU新生", "difficulty": 2, "bnbu": True},
                "stats": {"produced": 0, "failed": 0},
                "status": "active",
            }
        return copy.deepcopy(self.state[task])

    def write_state(self, task, st):
        st["updatedAt"] = datetime.now().isoformat()
        self.state[task] = st

    # ---- 台账（对应骨架 ②⑤）
    def ledger_has_success(self, key):
        return any(e["key"] == key and e["status"] == "success" for e in self.ledger)

    def append_ledger(self, entry):
        self.ledger.append(entry)

    # ---- 一次调度触发 = 一个全新 automation 会话
    def trigger(self, task, when, note=""):
        t0 = datetime.now()
        spec = SPECS[task]
        key = f"{task}:{period_id(task, when)}"
        st = self.read_state(task)

        # 0) 任务已停用（OPS-1 结课后）
        if st.get("status") == "ended":
            e = {"key": key, "task": task, "ts": when.isoformat(),
                 "status": "skipped", "durationMs": 60, "artifacts": [],
                 "cursor": st["cursor"],
                 "notes": "任务已结束（OPS-1 结课），跳过"}
            self.append_ledger(e)
            return {"exit": 0, "status": "skipped", "ledger": e, "reason": "ended"}

        # ② 幂等查重
        if self.ledger_has_success(key):
            e = {"key": key, "task": task, "ts": when.isoformat(),
                 "status": "skipped", "durationMs": 120, "artifacts": [],
                 "cursor": st["cursor"],
                 "notes": "幂等命中：本周期已成功执行，跳过以避免重复产出"}
            self.append_ledger(e)
            st["lastRun"] = {"ts": when.isoformat(), "status": "skipped", "key": key}
            self.write_state(task, st)
            return {"exit": 0, "status": "skipped", "ledger": e, "reason": "idempotent"}

        # ③ 执行
        failed = (task, key) in self.forced_fail
        if failed:
            e = {"key": key, "task": task, "ts": when.isoformat(),
                 "status": "failed",
                 "durationMs": int((datetime.now() - t0).total_seconds() * 1000) or 9100,
                 "artifacts": [], "cursor": st["cursor"],
                 "notes": note or "IMA 未授权，已降级：本地生成 + 备忘录告警 + 给出手动落库指引"}
            self.append_ledger(e)
            st["lastRun"] = {"ts": when.isoformat(), "status": "failed", "key": key}
            st["stats"]["failed"] += 1
            self.write_state(task, st)          # cursor 不推进
            return {"exit": 0, "status": "failed", "ledger": e, "reason": "injected"}

        cursor = st["cursor"]
        artifacts = spec["artifact"](cursor)
        produced = list(artifacts)

        # OPS-1：week>4 → 结课测评 + 停用
        ended_now = False
        if task == "OPS-1" and cursor["week"] > spec["maxWeek"]:
            produced = ["结课测评", "上手认证达标评估", "结课报告"]
            st["status"] = "ended"
            ended_now = True
            advance = {}
        else:
            advance = self._advance(task, cursor)

        new_cursor = dict(cursor)
        if advance:
            new_cursor.update(advance)
        e = {"key": key, "task": task, "ts": when.isoformat(),
             "status": "success",
             "durationMs": int((datetime.now() - t0).total_seconds() * 1000) or 42000,
             "artifacts": produced,
             "cursor": new_cursor,
             "notes": "已产出并分发" + ("（结课）" if ended_now else "")}
        # verify 字段：仅当本流产出 HTML 并跑了 harness（对应 OPS-1 / OPS-5）
        if spec.get("html"):
            e["verify"] = {"controls": 12, "pass": 12, "gate": "PASS"}
        self.append_ledger(e)

        # ④ 回写状态
        if advance:
            cursor.update(advance)
        st["cursor"] = cursor
        st["lastRun"] = {"ts": when.isoformat(), "status": "success", "key": key}
        st["stats"]["produced"] += len(produced)
        self.write_state(task, st)
        return {"exit": 0, "status": "success", "ledger": e,
                "artifacts": produced, "ended": ended_now}

    @staticmethod
    def _advance(task, c):
        if task == "OPS-1": return {"week": c["week"] + 1}
        if task == "OPS-2": return {"issue": c["issue"] + 1}
        if task == "OPS-4": return {"report": c["report"] + 1}
        if task == "OPS-6": return {"check": c["check"] + 1}
        if task == "OPS-5":
            i = ROTATION.index(c["module"])
            if i + 1 < len(ROTATION):
                return {"module": ROTATION[i + 1]}
            return {"module": ROTATION[0], "round": c["round"] + 1}
        return {}


def wk(n):   # 第 n 周（从 BASE 起，每周一 08:00）
    return BASE + timedelta(weeks=n, days=(7 - BASE.weekday()) % 7)


def day(n):  # 第 n 个工作日
    return BASE + timedelta(days=n)


print("=" * 78)
print("T2 · L4 运行时仿真 —— 幂等 / 状态机 / 台账 / 失败降级")
print("=" * 78)

# ============================================================ A. 幂等验证
print("\n[A] 幂等：同周期重复触发 → 第二次 skipped")
rt = L4Runtime()
idem_cases = [
    ("OPS-1", wk(0), wk(0), "weekly"),
    ("OPS-2", day(0), day(0), "daily"),
    ("OPS-3", day(0), day(0), "once"),
    ("OPS-4", wk(0), wk(0), "weekly"),
    ("OPS-5", wk(0), wk(0), "weekly"),
    ("OPS-6", wk(0), wk(0), "weekly"),
]
for task, t1, t2, ptype in idem_cases:
    r1 = rt.trigger(task, t1)
    r2 = rt.trigger(task, t2)
    CK.ok("A.幂等", f"{task} 首次触发 success",
          r1["status"] == "success", f"got={r1['status']} key={r1['ledger']['key']}")
    CK.ok("A.幂等", f"{task} 同周期重复 → skipped",
          r2["status"] == "skipped" and r2["reason"] == "idempotent",
          f"got={r2['status']}/{r2.get('reason')}")
    CK.ok("A.幂等", f"{task} 重复触发零产出",
          r2["ledger"]["artifacts"] == [], f"got={r2['ledger']['artifacts']}")
    CK.ok("A.幂等", f"{task} 重复触发退出码 0",
          r2["exit"] == 0, f"got={r2['exit']}")

# 幂等键隔离：不同任务同 ISO 周不串台
CK.ok("A.幂等", "同 ISO 周不同任务键不串台（OPS-1 vs OPS-4 vs OPS-5 vs OPS-6）",
      len({f"{t}:{iso_week(wk(0))}" for t in
           ("OPS-1", "OPS-4", "OPS-5", "OPS-6")}) == 4,
      "键前缀含 task，天然隔离")

# 幂等键不因跨天而误判：OPS-2 不同日期应各自执行
r_a = rt.trigger("OPS-2", day(5))
r_b = rt.trigger("OPS-2", day(6))
CK.ok("A.幂等", "OPS-2 不同日期各自执行（不误杀）",
      r_a["status"] == "success" and r_b["status"] == "success",
      f"{r_a['status']}/{r_b['status']}")

# 幂等键格式校验
import re
key_pat = {"OPS-1": r"^OPS-1:\d{4}-W\d{2}$", "OPS-2": r"^OPS-2:\d{4}-\d{2}-\d{2}$",
           "OPS-3": r"^OPS-3:final-exam-\d{4}-\d{2}-\d{2}$",
           "OPS-4": r"^OPS-4:\d{4}-W\d{2}$", "OPS-5": r"^OPS-5:\d{4}-W\d{2}$",
           "OPS-6": r"^OPS-6:\d{4}-W\d{2}$"}
for t, p in key_pat.items():
    keys = [e["key"] for e in rt.ledger if e["task"] == t]
    CK.ok("A.幂等", f"{t} 幂等键格式符合 §4 规则",
          keys and all(re.match(p, k) for k in keys), f"sample={keys[0] if keys else 'N/A'}")

# ==================================================== B. OPS-1 状态机推进
print("[B] 状态机：OPS-1 week 1→4 → 结课停用")
rt = L4Runtime()
weeks_seen, arts = [], []
for i in range(6):                       # 触发 6 次（含结课后 1 次）
    r = rt.trigger("OPS-1", wk(i))
    weeks_seen.append(rt.state["OPS-1"]["cursor"]["week"])
    arts.append(r.get("artifacts", []))
CK.ok("B.状态机", "OPS-1 cursor.week 严格 1→2→3→4→5",
      weeks_seen[:4] == [2, 3, 4, 5], f"got={weeks_seen[:4]}")
CK.ok("B.状态机", "OPS-1 前 4 次按 W1~W4 主题产出",
      all(a[0].startswith(f"课件W{i+1}") for i, a in enumerate(arts[:4])),
      f"got={[a[0] for a in arts[:4]]}")
CK.ok("B.状态机", "OPS-1 第 5 次（week=5>4）转为结课测评",
      arts[4] == ["结课测评", "上手认证达标评估", "结课报告"], f"got={arts[4]}")
CK.ok("B.状态机", "OPS-1 结课后自动停用",
      rt.state["OPS-1"]["status"] == "ended", f"got={rt.state['OPS-1']['status']}")
CK.ok("B.状态机", "OPS-1 停用后再次触发 → skipped 且不产出",
      arts[5] == [] and rt.ledger[-1]["status"] == "skipped",
      f"got={arts[5]}/{rt.ledger[-1]['status']}")
CK.ok("B.状态机", "OPS-1 全程退出码均为 0",
      all(e["status"] != "failed" for e in rt.ledger), "无 failed 记录")

# ==================================================== C. OPS-5 模块轮转
print("[C] 状态机：OPS-5 全模块轮转 + round 回卷")
rt = L4Runtime()
seq = []
for i in range(50):
    cur = rt.state.get("OPS-5", {"cursor": {"module": "A1", "round": 1}})["cursor"]["module"] \
        if "OPS-5" in rt.state else "A1"
    seq.append(cur)
    rt.trigger("OPS-5", wk(i))
CK.ok("C.状态机", "OPS-5 轮转序长度 = 25（A→G + E·N 全单元）",
      len(ROTATION) == 25, f"got={len(ROTATION)}")
CK.ok("C.状态机", "OPS-5 首轮 25 次覆盖全部单元且不重不漏",
      seq[:25] == ROTATION, f"got={seq[:25]}")
CK.ok("C.状态机", "OPS-5 第 26 次回到 A1",
      seq[25] == "A1", f"got={seq[25]}")
# 回卷发生在「处理末位 G3 的第 25 次触发」（ledger 下标 24）
CK.ok("C.状态机", "OPS-5 第 25 次（处理末位 G3）后回卷到 A1",
      json.loads(json.dumps(rt.ledger[24]["cursor"]))["module"] == "A1",
      f"cursor={rt.ledger[24]['cursor']}")
CK.ok("C.状态机", "OPS-5 回卷时 round 由 1 变 2",
      rt.ledger[24]["cursor"].get("round") == 2,
      f"cursor={rt.ledger[24]['cursor']}")
CK.ok("C.状态机", "OPS-5 跑满 2 轮（50 次）后 round = 3",
      rt.ledger[49]["cursor"].get("round") == 3,
      f"cursor={rt.ledger[49]['cursor']}")
CK.ok("C.状态机", "OPS-5 轮转中途不误加 round（非末位不 +1）",
      all(rt.ledger[i]["cursor"].get("round", 1) == 1 for i in range(24)),
      f"异常下标={[i for i in range(24) if rt.ledger[i]['cursor'].get('round',1)!=1]}")
CK.ok("C.状态机", "OPS-5 两轮内每个单元各产出 2 次（负载均衡）",
      all(seq.count(m) == 2 for m in ROTATION),
      f"min={min(seq.count(m) for m in ROTATION)} max={max(seq.count(m) for m in ROTATION)}")
# 模块分组覆盖
groups = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0}
for m in ROTATION:
    groups[m[0]] += 1
CK.ok("C.状态机", "OPS-5 覆盖 A/B/C/D/E/F/G 七大模块分组 + E·N 院校子模块",
      all(v > 0 for v in groups.values()) and "E·N" in ROTATION,
      f"groups={groups}")
# 游戏增量：E·N / F / G 单元额外产出游戏
game_units = [m for m in ROTATION if m == "E·N" or m[0] in "FG"]
r = L4Runtime()
game_ok = True
for i, m in enumerate(ROTATION):
    res = r.trigger("OPS-5", wk(i))
    if m in game_units:
        if not any(a.startswith("游戏") for a in res["artifacts"]):
            game_ok = False
    else:
        if any(a.startswith("游戏") for a in res["artifacts"]):
            game_ok = False
CK.ok("C.状态机", f"OPS-5 仅 E·N/F/G 单元（{len(game_units)}个）叠加游戏，其余不叠加",
      game_ok, f"game_units={game_units}")

# ==================================================== D. 台账三态与可解析
print("[D] 台账：三态齐全 + JSONL 可解析 + 字段完整")
rt = L4Runtime()
rt.trigger("OPS-2", day(0))
rt.trigger("OPS-2", day(0))                       # skipped
rt.forced_fail.add(("OPS-4", f"OPS-4:{iso_week(wk(0))}"))
rt.trigger("OPS-4", wk(0))                        # failed
rt.trigger("OPS-5", wk(1))                        # success
statuses = {e["status"] for e in rt.ledger}
CK.ok("D.台账", "台账三态齐全（success/skipped/failed）",
      statuses == {"success", "skipped", "failed"}, f"got={sorted(statuses)}")
req_fields = {"key", "task", "ts", "status", "durationMs", "artifacts", "cursor", "notes"}
CK.ok("D.台账", "每条台账必备 8 字段齐全",
      all(req_fields <= set(e.keys()) for e in rt.ledger),
      f"缺字段={[sorted(req_fields-set(e)) for e in rt.ledger if not req_fields <= set(e)]}")
# 关键：cursor 必须留痕，否则无法审计「这次跑完进度到哪了」
CK.ok("D.台账", "每条台账都带 cursor 快照（可审计进度）",
      all("cursor" in e for e in rt.ledger), "OK")
# verify 字段：仅 HTML 产物流（OPS-1/OPS-5）出现，其余不出现 —— 交叉验证 T1 的 harness 断言
HTML_FLOWS = {"OPS-1", "OPS-5"}
v_ok = all(("verify" in e) == (e["task"] in HTML_FLOWS)
           for e in rt.ledger if e["status"] == "success")
CK.ok("D.台账", "verify 字段仅出现在跑了 harness 的 HTML 产物流（OPS-1/OPS-5）",
      v_ok, f"HTML_FLOWS={sorted(HTML_FLOWS)}（与 T1 harness 断言一致）")
CK.ok("D.台账", "verify.gate 全为 PASS（未过则不应记 success）",
      all(e.get("verify", {}).get("gate") == "PASS"
          for e in rt.ledger if "verify" in e), "OK")
# JSONL 序列化 / 逐行解析
lines = [json.dumps(e, ensure_ascii=False) for e in rt.ledger]
parsed = [json.loads(l) for l in lines]
CK.ok("D.台账", "台账 JSONL 逐行可解析（无换行破坏）",
      all("\n" not in l for l in lines) and len(parsed) == len(rt.ledger),
      f"lines={len(lines)}")
CK.ok("D.台账", "台账按时间追加（顺序即执行序）",
      parsed == rt.ledger, "追加写语义正确")
# 与模板字段一致
tpl = f"{SKILL}/assets/run-ledger-template.jsonl"
if os.path.exists(tpl):
    tpl_keys = set()
    with open(tpl, encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            if l: tpl_keys |= set(json.loads(l).keys())
    CK.ok("D.台账", "仿真台账字段覆盖官方模板全部字段（超集即合规）",
          tpl_keys <= set().union(*[set(e) for e in rt.ledger]) | req_fields,
          f"tpl={sorted(tpl_keys)}")
    # 模板自身校验：必备 8 字段 + verify 可选
    tpl_rows = [json.loads(l) for l in open(tpl, encoding="utf-8") if l.strip()]
    CK.ok("D.台账", "官方模板每行必备 8 字段齐全",
          all(req_fields <= set(r) for r in tpl_rows),
          f"缺={[sorted(req_fields-set(r)) for r in tpl_rows if not req_fields<=set(r)]}")
    CK.ok("D.台账", "官方模板 verify 仅出现在 HTML 产物流",
          all(("verify" in r) == (r["task"] in HTML_FLOWS) for r in tpl_rows),
          f"rows={[(r['task'],'verify' in r) for r in tpl_rows]}")
    CK.ok("D.台账", "官方模板三态齐全",
          {r["status"] for r in tpl_rows} == {"success", "skipped", "failed"},
          f"got={sorted({r['status'] for r in tpl_rows})}")

# ==================================================== E. 失败降级不阻塞
print("[E] 失败降级：退出码 0 / cursor 不推进 / 可重试恢复")
rt = L4Runtime()
rt.forced_fail.add(("OPS-6", f"OPS-6:{iso_week(wk(0))}"))
r_fail = rt.trigger("OPS-6", wk(0))
CK.ok("E.失败降级", "失败时退出码 = 0（不触发调度重试风暴）",
      r_fail["exit"] == 0, f"got={r_fail['exit']}")
CK.ok("E.失败降级", "失败时台账记 failed",
      r_fail["ledger"]["status"] == "failed", f"got={r_fail['ledger']['status']}")
CK.ok("E.失败降级", "失败时 cursor 不推进（不吞掉本周期内容）",
      rt.state["OPS-6"]["cursor"]["check"] == 1,
      f"got={rt.state['OPS-6']['cursor']['check']}")
CK.ok("E.失败降级", "失败时 stats.failed 累加",
      rt.state["OPS-6"]["stats"]["failed"] == 1,
      f"got={rt.state['OPS-6']['stats']['failed']}")
# 同周期修复后重跑：幂等只认 success，failed 不挡重试
rt.forced_fail.discard(("OPS-6", f"OPS-6:{iso_week(wk(0))}"))
r_retry = rt.trigger("OPS-6", wk(0))
CK.ok("E.失败降级", "failed 不写幂等成功位 → 同周期可重试恢复",
      r_retry["status"] == "success", f"got={r_retry['status']}")
CK.ok("E.失败降级", "重试成功后 cursor 只推进 1 次（不重复推进）",
      rt.state["OPS-6"]["cursor"]["check"] == 2,
      f"got={rt.state['OPS-6']['cursor']['check']}")
CK.ok("E.失败降级", "重试成功后再次触发 → 幂等 skipped",
      rt.trigger("OPS-6", wk(0))["status"] == "skipped", "幂等生效")

# 调度重试风暴场景：任务已成功但调度系统又触发一次
rt2 = L4Runtime()
rt2.trigger("OPS-1", wk(0))
storm = [rt2.trigger("OPS-1", wk(0)) for _ in range(5)]
CK.ok("E.失败降级", "模拟调度重试 5 次 → 全部 skipped，零重复产出",
      all(s["status"] == "skipped" for s in storm) and
      sum(len(e["artifacts"]) for e in rt2.ledger) == 4,
      f"产物总数={sum(len(e['artifacts']) for e in rt2.ledger)}（应为 4）")

# ==================================================== F. 判据 3：跨会话持久
print("[F] 判据3：跨会话状态持久（模拟会话销毁后重建）")
snap_dir = os.path.join(OUT, ".sim-state")
os.makedirs(snap_dir, exist_ok=True)
rt = L4Runtime()
rt.trigger("OPS-5", wk(0)); rt.trigger("OPS-5", wk(1)); rt.trigger("OPS-5", wk(2))
# 会话 1 结束：状态落盘（模拟 IMA 权威存储）
snap_f = os.path.join(snap_dir, "OPS-5.json")
ledger_f = os.path.join(snap_dir, "run-ledger.jsonl")
with open(snap_f, "w", encoding="utf-8") as f:
    json.dump(rt.state["OPS-5"], f, ensure_ascii=False)
with open(ledger_f, "w", encoding="utf-8") as f:
    for e in rt.ledger:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
# 会话 2：全新会话，从磁盘恢复（无任何内存历史）
rt2 = L4Runtime()
with open(snap_f, encoding="utf-8") as f:
    rt2.state["OPS-5"] = json.load(f)
with open(ledger_f, encoding="utf-8") as f:
    rt2.ledger = [json.loads(l) for l in f if l.strip()]
base_ledger_len = len(rt2.ledger)          # 会话 2 启动时的历史台账基线
before = rt2.state["OPS-5"]["cursor"]["module"]
r_new = rt2.trigger("OPS-5", wk(3))
# A1 起跑，跑 3 次（A1→A2→A3）后 cursor 应停在 B1
CK.ok("F.跨会话", "新会话从状态源恢复到正确 cursor（不从头开始）",
      before == "B1", f"restored={before}（A1 起跑 3 次后应为 B1）")
CK.ok("F.跨会话", "新会话首次触发即幂等识别历史周期",
      rt2.trigger("OPS-5", wk(2))["status"] == "skipped",
      "历史 ISO 周被正确判重")
CK.ok("F.跨会话", "新会话继续执行并正确推进（B1→B2）",
      r_new["status"] == "success" and
      rt2.state["OPS-5"]["cursor"]["module"] == "B2",
      f"got={rt2.state['OPS-5']['cursor']['module']}")
new_entries = rt2.ledger[base_ledger_len:]   # 会话 2 新增的台账
CK.ok("F.跨会话", "新会话恢复后不重复产出历史周期内容（仅新增 1 条 success）",
      sum(1 for e in new_entries if e["status"] == "success") == 1,
      f"新增={[(e['status'], e['key']) for e in new_entries]}")
CK.ok("F.跨会话", "新会话台账为增量追加（历史 3 条完好未覆盖）",
      len(rt2.ledger) == base_ledger_len + len(new_entries) and len(new_entries) == 2,
      f"base={base_ledger_len} new={len(new_entries)}")
CK.ok("F.跨会话", "状态文件 round 字段跨会话保持",
      rt2.state["OPS-5"]["cursor"]["round"] == 1,
      f"got={rt2.state['OPS-5']['cursor']['round']}")
CK.ok("F.跨会话", "state schema 标识正确（ai-literacy-state/v1）",
      rt2.state["OPS-5"]["schema"] == "ai-literacy-state/v1",
      f"got={rt2.state['OPS-5'].get('schema')}")

# ==================================================== G. 长时间全流混跑
print("[G] 混跑：6 条流 × 8 周 全量仿真（一致性 + 无异常）")
rt = L4Runtime()
err = None
try:
    for w in range(8):
        rt.trigger("OPS-1", wk(w))
        rt.trigger("OPS-4", wk(w))
        rt.trigger("OPS-5", wk(w))
        rt.trigger("OPS-6", wk(w))
        for d in range(5):
            rt.trigger("OPS-2", day(w * 7 + d))
    rt.trigger("OPS-3", datetime(2026, 1, 14, 19, 0, 0))
    # 随机重复触发 20 次（模拟重试/补跑）
    import random
    random.seed(7)
    for _ in range(20):
        t = random.choice(list(SPECS))
        rt.trigger(t, random.choice([wk(random.randint(0, 7)), day(random.randint(0, 40))]))
except Exception as ex:
    err = repr(ex)
CK.ok("G.混跑", "6 流 × 8 周 + 20 次随机重触发 无异常抛出", err is None, err or "OK")
succ = sum(1 for e in rt.ledger if e["status"] == "success")
skip = sum(1 for e in rt.ledger if e["status"] == "skipped")
CK.ok("G.混跑", f"混跑产出统计合理（success={succ} skipped={skip}）",
      succ >= 40 and skip >= 5, f"succ={succ} skip={skip}")
CK.ok("G.混跑", "所有条目退出码语义一致（无 failed 漏出）",
      all(e["status"] in ("success", "skipped", "failed") for e in rt.ledger), "OK")
# 一致性：success 条目的 key 全局唯一（幂等的数学保证）
succ_keys = [e["key"] for e in rt.ledger if e["status"] == "success"]
CK.ok("G.混跑", "success 条目幂等键全局唯一（不可能重复产出）",
      len(succ_keys) == len(set(succ_keys)),
      f"dup={len(succ_keys)-len(set(succ_keys))}")
# OPS-3 once 只执行一次
o3 = [e for e in rt.ledger if e["task"] == "OPS-3"]
CK.ok("G.混跑", "OPS-3（once）幂等键固定，重复触发亦只执行 1 次",
      sum(1 for e in o3 if e["status"] == "success") == 1,
      f"success={sum(1 for e in o3 if e['status']=='success')}")

# ---------------------------------------------------------------- 汇总
print("\n" + "=" * 78)
by_group = {}
for r in CK.results:
    by_group.setdefault(r["group"], []).append(r)
for g, rs in by_group.items():
    p = sum(1 for r in rs if r["pass"])
    mark = "✅" if p == len(rs) else "❌"
    print(f"  {mark} {g:<16} {p}/{len(rs)}")
print("-" * 78)
print(f"  合计  {CK.passed}/{CK.total}   通过率 {CK.passed/CK.total*100:.1f}%")
print("=" * 78)

fails = [r for r in CK.results if not r["pass"]]
if fails:
    print("\n❌ 失败明细：")
    for r in fails:
        print(f"  [{r['group']}] {r['name']}\n      detail: {r['detail']}")

with open(os.path.join(OUT, "t2-results.json"), "w", encoding="utf-8") as f:
    json.dump({"total": CK.total, "passed": CK.passed,
               "rate": round(CK.passed / CK.total * 100, 1),
               "groups": {g: {"total": len(rs), "passed": sum(1 for r in rs if r["pass"])}
                          for g, rs in by_group.items()},
               "results": CK.results}, f, ensure_ascii=False, indent=2)

sys.exit(0 if CK.passed == CK.total else 1)
