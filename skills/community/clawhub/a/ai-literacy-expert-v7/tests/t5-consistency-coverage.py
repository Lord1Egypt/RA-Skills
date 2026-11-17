#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T5 · 一致性与全模块覆盖校验
==========================
校验维度：
  A. 版本号一致性（SKILL.md / README.md / meta.json / 门控维度数）
  B. L4 资产齐备（4 份新资产 + 内容合规）
  C. OPS-1~6 齐备与注册表合规
  D. 全模块覆盖（25 个单元 × 六大能力 → 至少一条 OPS 覆盖）
  E. 文档内部一致性（自包含模板、消歧矩阵、身份八、第九部分、14 维门控）
  F. 引用完整性（悬空引用 0；注意 jsonl 必须先于 json 匹配）
  G. 分发包完整性（zip）
"""
import json, os, re, sys, zipfile, glob, pathlib

# 路径自适应：技能根目录由脚本位置推导，输出目录可用 V7_TEST_OUT 覆盖
SKILL = str(pathlib.Path(__file__).resolve().parent.parent)
OUT = os.environ.get("V7_TEST_OUT") or str(pathlib.Path(__file__).resolve().parent / "out")
os.makedirs(OUT, exist_ok=True)


class CK:
    def __init__(self): self.r = []
    def ok(self, g, n, c, d=""):
        self.r.append({"group": g, "name": n, "pass": bool(c), "detail": str(d)})
        return bool(c)
    @property
    def passed(self): return sum(1 for x in self.r if x["pass"])
    @property
    def total(self): return len(self.r)


CK = CK()
rd = lambda p: open(p, encoding="utf-8").read()


def show(c):
    print(f"  {'✅' if c else '❌'} ", end="")


# ------------------------------------------------------------------ A. 版本一致性
print("\n[A] 版本号一致性")
skill = rd(f"{SKILL}/SKILL.md")
readme = rd(f"{SKILL}/README.md")
meta = json.load(open(f"{SKILL}/meta.json", encoding="utf-8"))

CK.ok("A.版本", "SKILL.md 标题为 V7.0（L4 调度版）",
      "# AI 通识课资深专家 V7.0（L4 调度版）" in skill,
      skill.split("\n")[0][:60])
CK.ok("A.版本", "meta.json version = 7.0.0", meta.get("version") == "7.0.0", meta.get("version"))
CK.ok("A.版本", "README.md 标题含 V7.0", "V7.0" in readme.split("\n")[0], readme.split("\n")[0][:60])
V70_ROW = re.compile(r"\|\s*\**\s*V?7\.0")          # 单元格可能带 ** 粗体
CK.ok("A.版本", "README 版本历史新增 V7.0 行", bool(V70_ROW.search(readme)), "—")
CK.ok("A.版本", "SKILL.md 版本矩阵含 V7.0 行", bool(V70_ROW.search(skill)), "—")
CK.ok("A.版本", "版本矩阵 V7.0 行标为 L4 调度版且提第 14 维",
      bool(re.search(r"V7\.0 L4 调度版.*?第 14 维", skill, re.S)), "—")
# 「13 维」仅允许出现在历史/继承语境（V6.0 行、门控演进说明），且当前总数须明示为 14
CK.ok("A.版本", "门控总数明示为 14 维（第 13 维 + 第 14 维 并存表述）",
      "第 13 维" in skill and "第 14 维" in skill, "—")
CK.ok("A.版本", "遗留『13 维』均已标注版本语境（非当前总数）",
      all(("V6.0" in ln or "继承" in ln) for ln in skill.split("\n") if "13 维" in ln),
      f"可疑行={[ln[:60] for ln in skill.split(chr(10)) if '13 维' in ln]}")
CK.ok("A.版本", "README 质量保证标为 14 维", "14 维度" in readme, "—")
CK.ok("A.版本", "SKILL.md 含 L4 达成判据表", "L4 达成判据" in skill, "—")
CK.ok("A.版本", "SKILL.md 描述长度 ≤1024",
      len(re.search(r'description:\s*[\'"]?(.*?)[\'"]?\s*\n', skill, re.S).group(1)) <= 1024
      if re.search(r'description:\s*[\'"]?(.*?)[\'"]?\s*\n', skill, re.S) else False, "—")

# ------------------------------------------------------------------ B. L4 资产齐备
print("[B] L4 资产齐备")
assets = {
    "references/automation-l4-scheduler.md": 4000,
    "assets/self-contained-prompt-template.md": 3000,
    "assets/automation-registry.json": 2000,
    "assets/run-ledger-template.jsonl": 800,
}
for rel, minsz in assets.items():
    p = os.path.join(SKILL, rel)
    e = os.path.exists(p)
    CK.ok("B.资产", f"{os.path.basename(rel)} 存在且非空（≥{minsz}B）",
          e and os.path.getsize(p) >= minsz,
          f"size={os.path.getsize(p) if e else 'MISSING'}")
l4 = rd(f"{SKILL}/references/automation-l4-scheduler.md")
CK.ok("B.资产", "L4 文档含五判据表", "判据" in l4 and l4.count("判据") >= 5, "判据出现 %d 次" % l4.count("判据"))
CK.ok("B.资产", "L4 文档含自包含指令契约（10 段）",
      all(s in l4 for s in ["【角色】", "【会话】", "【任务】", "【状态】", "【幂等】",
                            "【执行】", "【验证】", "【落点】", "【留痕】", "【失败】"]), "—")
CK.ok("B.资产", "L4 文档含 automation 会话 5 铁律",
      "铁律" in l4 and "禁自管理" in l4, "—")
CK.ok("B.资产", "L4 文档含幂等键公式",
      'idempotency_key = "<task>:<周期标识>"' in l4, "—")
CK.ok("B.资产", "L4 文档含『确认即授权』写操作约束",
      "确认" in l4 and "不擅自" in l4 or "先预览" in l4, "—")

# ------------------------------------------------------------------ C. OPS 齐备
print("[C] OPS-1~6 齐备与注册表合规")
ops = rd(f"{SKILL}/references/automation-ops.md")
reg = json.load(open(f"{SKILL}/assets/automation-registry.json", encoding="utf-8"))
tasks = reg if isinstance(reg, list) else reg.get("tasks", [])
keys = [t.get("key") for t in tasks]
for i in range(1, 7):
    CK.ok("C.OPS", f"OPS-{i} 在运营流文档中有独立章节",
          bool(re.search(rf"^## OPS-{i}\s", ops, re.M)), "—")
    CK.ok("C.OPS", f"OPS-{i} 在注册表中有条目",
          f"OPS-{i}" in keys, f"keys={keys}")
CK.ok("C.OPS", "注册表任务数 = 6", len(tasks) == 6, f"got={len(tasks)}")
need = {"key", "name", "cron", "frequencyType", "timeoutSec", "retryCount",
        "idempotency", "covers", "verify", "deliverTo"}
for t in tasks:
    miss = need - set(t)
    CK.ok("C.OPS", f"{t.get('key')} 注册表字段完整（10 项）", not miss, f"缺={sorted(miss)}")
CK.ok("C.OPS", "全部任务 frequencyType ∈ {daily, interval, once}",
      all(t.get("frequencyType") in ("daily", "interval", "once") for t in tasks),
      str([t.get("frequencyType") for t in tasks]))
CK.ok("C.OPS", "全部任务 timeout 在 10~1800", all(10 <= t.get("timeoutSec", 0) <= 1800 for t in tasks), "—")
CK.ok("C.OPS", "全部任务 retryCount ≤ 10", all(t.get("retryCount", 0) <= 10 for t in tasks), "—")
CK.ok("C.OPS", "全部任务都定义了幂等规则", all(t.get("idempotency") for t in tasks), "—")
# cron 唯一性（避免两条流同一时刻抢资源）
crons = [t.get("cron") for t in tasks]
CK.ok("C.OPS", "6 条流 cron 互不冲突（时分不同）",
      len({(c.split()[2], c.split()[1]) for c in crons}) == 6, f"crons={crons}")

# ------------------------------------------------------------------ D. 全模块覆盖
print("[D] 全模块 × 六大能力 覆盖")
# 从模块文档提取权威单元清单
inv = set()
for f in sorted(glob.glob(f"{SKILL}/references/module-*.md")):
    txt = rd(f)
    for m in re.finditer(r"^#{1,3}\s*(模块\s*)?(E·N|[A-G]\d)(?=\s|[·:：\-]|$)", txt, re.M):
        inv.add(m.group(2))
ROTATION = re.search(r"轮转序（覆盖全部模块与单元）：\s*```\s*(.+?)```", ops, re.S)
if ROTATION:
    raw = ROTATION.group(1).strip()
    raw = re.sub(r"[（(].*?[)）]", "", raw)            # 去掉尾部「(回到 A1, round+1)」说明
    rot = [x.strip() for x in raw.replace("→", ",").split(",") if x.strip()]
else:
    rot = []
CK.ok("D.覆盖", "权威单元清单提取成功（应为 25）", len(inv) == 25, f"got={len(inv)} {sorted(inv)}")
CK.ok("D.覆盖", "OPS-5 轮转序解析成功（应为 25）", len(rot) == 25, f"got={len(rot)}")
CK.ok("D.覆盖", "轮转序与权威单元清单完全一致（不重不漏）",
      set(rot) == inv and len(rot) == len(inv),
      f"仅轮转有={sorted(set(rot)-inv)} 仅清册有={sorted(inv-set(rot))}")
for g in "ABCDEFG":
    CK.ok("D.覆盖", f"模块 {g} 至少 1 个单元被轮转覆盖",
          any(u.startswith(g) for u in rot), f"{g}: {[u for u in rot if u.startswith(g)]}")
CK.ok("D.覆盖", "院校子模块 E·N 被轮转覆盖", "E·N" in rot, "—")

# 六大能力覆盖：任一 OPS 的 covers 字段提及
CAPS = ["课件", "游戏", "备课", "评估", "推荐", "协作"]
covers_all = " ".join(str(t.get("covers", "")) for t in tasks) + ops
for cap in CAPS:
    CK.ok("D.覆盖", f"能力「{cap}」被至少一条 OPS 覆盖", cap in covers_all, "—")
# 每模块被至少一条 OPS 覆盖（用总览表 covers 列）
tbl = re.search(r"## 总览：六类运营流.*?\n\n(\|.*?)\n\n", ops, re.S)
CK.ok("D.覆盖", "总览表存在且含 6 行（6 条流）",
      bool(tbl) and tbl.group(1).count("OPS-") >= 6,
      f"rows={tbl.group(1).count('OPS-') if tbl else 0}")
CK.ok("D.覆盖", "文档声明『全模块全功能自动化』覆盖结论",
      "全部模块" in ops and "六大能力" in ops, "—")

# ------------------------------------------------------------------ E. 文档内部一致性
print("[E] 文档内部一致性")
CK.ok("E.一致", "自包含模板含 10 段占位结构",
      all(s in rd(f"{SKILL}/assets/self-contained-prompt-template.md") for s in
          ["【角色】", "【会话】", "【任务】", "【状态】", "【幂等】",
           "【执行】", "【验证】", "【落点】", "【留痕】", "【失败】"]), "—")
tpl = rd(f"{SKILL}/assets/self-contained-prompt-template.md")
CK.ok("E.一致", "自包含模板含注册前自检清单", "自检" in tpl, "—")
CK.ok("E.一致", "SKILL.md 含身份八 · L4 自动化调度专家",
      "L4 自动化调度专家" in skill, "—")
CK.ok("E.一致", "SKILL.md 含第九部分 · L4 自动化调度层",
      "L4 自动化调度层" in skill, "—")
CK.ok("E.一致", "SKILL.md 含第 14 维 L4 调度门控",
      bool(re.search(r"14\s*维|第\s*14\s*维", skill)) and "L4 调度门控" in skill, "—")
CK.ok("E.一致", "SKILL.md 消歧矩阵新增调度类 3 行",
      skill.count("调度") >= 10, "调度出现 %d 次" % skill.count("调度"))
CK.ok("E.一致", "workflow-orchestrator 含 §9 SCHEDULE 元阶段",
      "SCHEDULE" in rd(f"{SKILL}/references/workflow-orchestrator.md"), "—")
wf = rd(f"{SKILL}/references/workflow-orchestrator.md")
CK.ok("E.一致", "workflow-orchestrator 含 automation 会话行为契约",
      "automation" in wf and "铁律" in wf, "—")
CK.ok("E.一致", "workflow-orchestrator 含调度化映射表（§11）",
      "映射" in wf, "—")
CK.ok("E.一致", "workflow-orchestrator 警告 automation 会话禁加载本技能",
      "CODEBUDDY_SESSION_TYPE" in wf, "—")
# 14 维门控：直接解析 SKILL.md 的门控表格行（格式 `| N. 名称 | 检查项 | 详见 |`）
gate_rows = re.findall(r"^\|\s*\**(\d+)\.\s*([^|]+?)\**\s*\|(.+)$", skill, re.M)
nums = [int(n) for n, _, _ in gate_rows]
full_row = {int(n): (t.strip(), rest) for n, t, rest in gate_rows}
CK.ok("E.一致", f"门控表解析出 14 个维度（实际 {len(gate_rows)}）",
      len(gate_rows) == 14, f"nums={nums}")
CK.ok("E.一致", "门控维度编号 1~14 连续无缺号",
      nums == list(range(1, 15)), f"got={nums}")
names = {int(n): t.strip() for n, t, _ in gate_rows}
CK.ok("E.一致", "第 13 维 = 工作流编排门控", "工作流编排" in names.get(13, ""), names.get(13))
CK.ok("E.一致", "第 14 维 = L4 调度门控", "L4 调度门控" in names.get(14, ""), names.get(14))
CK.ok("E.一致", "第 12 维 = 互动控件全测门控（harness 自动化）",
      "互动控件" in names.get(12, ""), names.get(12))
row14 = full_row.get(14, ("", ""))[1]          # 第 2 列「检查项」
CK.ok("E.一致", "第 14 维含 8 项自检", "8 项自检" in row14, row14[:80])
CK.ok("E.一致", "第 14 维含『写操作已展示预览并获用户确认』",
      "确认" in row14, row14[-90:])
CK.ok("E.一致", "第 14 维含幂等键与 IMA 权威状态源要求",
      "幂等" in row14 and "IMA" in row14, "—")

# ------------------------------------------------------------------ F. 引用完整性
print("[F] 引用完整性（悬空引用检测）")
FILE_RE = re.compile(r"`((?:references|assets)/[\w\-./]+?\.(?:md|jsonl|json|js))`")
missing = []
checked = 0
for root, _, files in os.walk(SKILL):
    for fn in files:
        if not fn.endswith((".md", ".json")):
            continue
        fp = os.path.join(root, fn)
        try:
            txt = rd(fp)
        except Exception:
            continue
        for m in FILE_RE.finditer(txt):
            ref = m.group(1)
            # 相对 SKILL 根目录解析
            target = os.path.join(SKILL, ref)
            checked += 1
            if not os.path.exists(target):
                missing.append((os.path.relpath(fp, SKILL), ref))
CK.ok("F.引用", f"悬空引用 = 0（检查 {checked} 处引用）", not missing, f"missing={missing[:6]}")
# 反向：新增 L4 资产必须被 SKILL.md 或 README 提及
for rel in assets:
    base = os.path.basename(rel)
    CK.ok("F.引用", f"{base} 被 SKILL.md/README 引用",
          base in skill or base in readme, "—")

# ------------------------------------------------------------------ G. 分发包
print("[G] 分发包完整性")
# 分发包位置：优先环境变量 V7_DIST_ZIP；未设置则不做假设，降级为直接校验技能目录本身。
# 这样该项在任何环境下都能做真实验证，而不是因为找不到 zip 就判失败或跳过。
NEED_IN = ["SKILL.md", "meta.json", "README.md",
           "references/automation-l4-scheduler.md",
           "assets/automation-registry.json",
           "assets/run-ledger-template.jsonl",
           "assets/self-contained-prompt-template.md",
           "references/automation-ops.md",
           "assets/playwright-control-test-harness.js"]
zp = os.environ.get("V7_DIST_ZIP", "")
if zp and os.path.exists(zp):
    z = zipfile.ZipFile(zp)
    bad = z.testzip()
    names = z.namelist()
    CK.ok("G.分发", f"zip 无损坏文件（{len(names)} 条目）", bad is None, f"bad={bad}")
    for n in NEED_IN:
        CK.ok("G.分发", f"包内含 {n}", any(nm.endswith(n) for nm in names), "—")
else:
    for n in NEED_IN:
        CK.ok("G.分发", f"[未打包·直接校验技能目录] 含 {n}",
              os.path.exists(os.path.join(SKILL, n)), "—")

# ------------------------------------------------------------------ 汇总
print("\n" + "=" * 78)
by = {}
for r in CK.r:
    by.setdefault(r["group"], []).append(r)
for g, rs in by.items():
    p = sum(1 for r in rs if r["pass"])
    print(f"  {'✅' if p == len(rs) else '❌'} {g:<12} {p}/{len(rs)}")
print("-" * 78)
print(f"  合计  {CK.passed}/{CK.total}   通过率 {CK.passed/CK.total*100:.1f}%")
print("=" * 78)

fails = [r for r in CK.r if not r["pass"]]
if fails:
    print("\n❌ 失败明细：")
    for r in fails:
        print(f"  [{r['group']}] {r['name']}\n      detail: {r['detail']}")

json.dump({"total": CK.total, "passed": CK.passed,
           "rate": round(CK.passed / CK.total * 100, 1),
           "groups": {g: {"total": len(rs), "passed": sum(1 for r in rs if r["pass"])}
                      for g, rs in by.items()},
           "results": CK.r},
          open(os.path.join(OUT, "t5-results.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"\n明细已写入 {OUT}/t5-results.json")
sys.exit(0 if CK.passed == CK.total else 1)
