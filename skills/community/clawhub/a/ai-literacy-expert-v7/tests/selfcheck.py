#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V7 · 技能自身自检（selfcheck）
=============================
与 T1~T5 的区别：
  · T1~T5 验证「L4 调度行为与产物质量」，偏运行时与产物级；
  · selfcheck 验证「技能包自身是否健康」，偏静态结构，秒级完成、无外部依赖。

分组：
  A. frontmatter 合规          B. meta.json 合规
  C. 数字一致性（防跨版本表述滞后）
  D. 引用完整性                E. 目录与卫生
  F. L4 资产齐备               G. 自包含契约
  H. 测试资产齐备（可验证性）

用法：
  python3 tests/selfcheck.py                      # 输出目录默认 tests/out
  V7_TEST_OUT=/tmp/x python3 tests/selfcheck.py   # 自定义输出目录
  python3 tests/selfcheck.py --quiet              # 只打印汇总

退出码：0 = 全部通过；1 = 存在未通过项（可接入 CI 做门禁）
"""
import json, os, re, sys, glob, pathlib

# 路径自适应：技能根目录由脚本位置推导（本脚本位于 <skill>/tests/）
SKILL = str(pathlib.Path(__file__).resolve().parent.parent)
OUT = os.environ.get("V7_TEST_OUT") or str(pathlib.Path(__file__).resolve().parent / "out")
os.makedirs(OUT, exist_ok=True)

QUIET = "--quiet" in sys.argv

R = []
def ok(group, name, cond, detail=""):
    R.append({"group": group, "name": name, "pass": bool(cond), "detail": str(detail)})
    if not QUIET:
        mark = "✅" if cond else "❌"
        print(f"  {mark} {name}" + (f"   ← {detail}" if (detail and not cond) else ""))
    return bool(cond)

def rd(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception as e:
        return ""

skill_path = os.path.join(SKILL, "SKILL.md")
skill = rd(skill_path)
readme = rd(os.path.join(SKILL, "README.md"))

# ------------------------------------------------------------ A. frontmatter
print("[A] frontmatter 合规")
fm = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
ok("A.frontmatter", "SKILL.md 存在 YAML frontmatter", bool(fm))
fm_txt = fm.group(1) if fm else ""
name_m = re.search(r"^name:\s*(.+)$", fm_txt, re.M)
desc_m = re.search(r'^description:\s*"(.*)"\s*$', fm_txt, re.M)
ok("A.frontmatter", "frontmatter 含 name", bool(name_m), name_m.group(1) if name_m else "缺失")
ok("A.frontmatter", "frontmatter 含 description", bool(desc_m))
desc = desc_m.group(1) if desc_m else ""
ok("A.frontmatter", f"description 长度 ≤ 1024（实际 {len(desc)}）", 0 < len(desc) <= 1024, f"len={len(desc)}")
ok("A.frontmatter", "含显式偏好声明 Prefer this skill over",
   "Prefer this skill over" in desc)
CN_VERBS = ["备课", "出题", "评估", "协作", "课程设计", "课件", "定时任务管理"]
ok("A.frontmatter", "中文触发动词齐备",
   all(v in desc for v in CN_VERBS),
   "缺：" + ",".join(v for v in CN_VERBS if v not in desc))
EN_VERBS = ["generate", "build", "design", "schedule", "assess", "recommend"]
ok("A.frontmatter", "英文触发动词齐备（宿主做英文意图路由时召回）",
   all(v in desc for v in EN_VERBS),
   "缺：" + ",".join(v for v in EN_VERBS if v not in desc))

# ------------------------------------------------------------ B. meta.json
print("[B] meta.json 合规")
meta_path = os.path.join(SKILL, "meta.json")
meta = None
try:
    meta = json.load(open(meta_path, encoding="utf-8"))
    ok("B.meta", "meta.json 是合法 JSON", True)
except Exception as e:
    ok("B.meta", "meta.json 是合法 JSON", False, str(e))

if meta is not None:
    need = ["name", "display_name", "display_description", "detail_describe",
            "author", "version"]
    for k in need:
        ok("B.meta", f"含必需字段 {k}", k in meta and str(meta.get(k, "")).strip() != "")
    ok("B.meta", "name 与 frontmatter.name 一致",
       name_m and meta.get("name") == name_m.group(1).strip(),
       f"meta={meta.get('name')} fm={name_m.group(1).strip() if name_m else '?'}")
    ok("B.meta", "version 符合 semver", bool(re.match(r"^\d+\.\d+\.\d+$", str(meta.get("version", "")))),
       meta.get("version"))
    ok("B.meta", f"use_cases ≥ 1（实际 {len(meta.get('use_cases', []))}）", len(meta.get("use_cases", [])) >= 1)
    ok("B.meta", f"tags ≥ 1（实际 {len(meta.get('tags', []))}）", len(meta.get("tags", [])) >= 1)
    # icon：允许不存在（本地技能无需上架），但若存在必须是可用的 http(s) 图片地址，
    # 绝不能是空串——空串会让按 uri 校验的解析器直接判失败。
    if "icon" in meta:
        ic = str(meta.get("icon", ""))
        ok("B.meta", "icon 字段为合法 http(s) 图片地址（存在即不可为空串）",
           ic.startswith("http://") or ic.startswith("https://"), f"icon={ic!r}")
    else:
        ok("B.meta", "icon 未设置（本地技能无需上架，合规）", True, "字段已移除")
    # 版本一致性：必须以「标题/版本说明中声明的当前版本」为准，
    # 不能用「SKILL.md 里出现过 Vx.0」来判断——文档里必然残留大量历史版本号。
    def vtuple(s):
        p = str(s).split(".")
        try:
            return (int(p[0]), int(p[1]) if len(p) > 1 else 0)
        except ValueError:
            return None
    doc_v = None
    m_title = re.search(r"^#\s*.*?V(\d+)\.(\d+)", skill, re.M)
    if m_title:
        doc_v = (int(m_title.group(1)), int(m_title.group(2)))
    meta_v = vtuple(meta.get("version", "0"))
    if doc_v:
        ok("B.meta", f"meta.version 与 SKILL.md 标题声明版本一致（V{doc_v[0]}.{doc_v[1]}）",
           meta_v == doc_v, f"SKILL.md=V{doc_v[0]}.{doc_v[1]} meta={meta.get('version')}")
        m_readme = re.search(r"V(\d+)\.(\d+)", readme)
        if m_readme:
            rv = (int(m_readme.group(1)), int(m_readme.group(2)))
            ok("B.meta", f"README.md 声明版本与 meta 一致（V{doc_v[0]}.{doc_v[1]}）",
               rv == doc_v, f"README=V{rv[0]}.{rv[1]} 期望=V{doc_v[0]}.{doc_v[1]}")

# ------------------------------------------------------------ C. 数字一致性
# 跨版本演进时，标题性表述（身份数/维数/条目数）最容易滞后于正文。
# 本组逐项做「文档声明值 vs 正文实测值」对照，把这类滞后变成可自动捕获的失败。
print("[C] 数字一致性（声明值 vs 正文实测值）")

CN = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}
def cn2num(s):
    if s.isdigit():
        return int(s)
    if s in CN:
        return CN[s]
    if s.startswith("十") and len(s) > 1 and s[1] in CN:
        return 10 + CN[s[1]]
    m = re.match(r"^([二三四五六七八九])十([一二三四五六七八九])?$", s)
    if m:
        return CN[m.group(1)] * 10 + (CN.get(m.group(2), 0) if m.group(2) else 0)
    return None

# C1 · 身份数
ids_found = re.findall(r"^\*\*身份([一二三四五六七八九十]+) —", skill, re.M)
n_ids = len(ids_found)
m = re.search(r"角色定位（([一二三四五六七八九十\d]+)重?专业身份）", skill)
if m:
    n_decl = cn2num(m.group(1))
    ok("C.数字", f"「{m.group(1)}专业身份」与正文实际身份数一致（实际 {n_ids}）",
       n_decl == n_ids, f"声明={n_decl} 实际={n_ids}")
else:
    ok("C.数字", "找到角色定位标题", False, "未匹配到「角色定位（N重专业身份）」")

# C2 · 门控维数
gate_rows = re.findall(r"^\|\s*\**(\d+)\.\s*([^|]+?)\**\s*\|(.+)$", skill, re.M)
n_gate = len([r for r in gate_rows if int(r[0]) <= 20])
max_gate = max((int(r[0]) for r in gate_rows if int(r[0]) <= 20), default=0)
ok("C.数字", f"门控表格可解析且编号连续（最大 {max_gate} 维）",
   max_gate > 0 and sorted(int(r[0]) for r in gate_rows if int(r[0]) <= 20) == list(range(1, max_gate + 1)),
   f"rows={n_gate}")
# 扫描全文「N 维」表述：与实测不符者必须带历史语境说明，否则视为表述滞后
HIST = re.compile(r"V\d\.\d|继承|升级|已升|升至|原|历史|新增|新增至|此前|早前")
bad_dims = []
for mm in re.finditer(r"(\d+)\s*维(?:度)?(?!\s*门控检查点)", skill):
    v = int(mm.group(1))
    if v == max_gate or v < 5:      # 小数字多为「3D/2D」之类，跳过
        continue
    ctx = skill[max(0, mm.start() - 60):mm.end() + 60]
    if not HIST.search(ctx):
        bad_dims.append(mm.group(0))
ok("C.数字", f"全文「N 维」表述与实测 {max_gate} 维一致（无孤立滞后表述）",
   not bad_dims, f"可疑：{bad_dims}")

# C3 · 运营流数量
ops_path = os.path.join(SKILL, "references", "automation-ops.md")
ops = rd(ops_path)
if ops:
    n_ops = len(re.findall(r"^## OPS-\d", ops, re.M))
    m = re.search(r"([一二三四五六七八九十\d]+)\s*类运营流", skill)
    n_decl = cn2num(m.group(1)) if m else None
    ok("C.数字", f"「{m.group(1) if m else '?'}类运营流」与 OPS 区块数一致（实际 {n_ops}）",
       n_decl == n_ops, f"声明={n_decl} 实际={n_ops}")
    ok("C.数字", "OPS 编号连续（OPS-1..N）",
       n_ops > 0 and [f"OPS-{i}" for i in range(1, n_ops + 1)] == re.findall(r"^## (OPS-\d)", ops, re.M),
       re.findall(r"^## (OPS-\d)", ops, re.M))

# C4 · 模块数与单元数
mod_files = sorted(glob.glob(os.path.join(SKILL, "references", "module-*.md")))
inv = set()
for f in mod_files:
    for mm in re.finditer(r"^#{1,3}\s*(模块\s*)?(E·N|[A-G]\d)(?=\s|[·:：\-]|$)", rd(f), re.M):
        inv.add(mm.group(2))
ok("C.数字", f"模块文档数 = {len(mod_files)}（A→G + E·N 共 8 个）", len(mod_files) == 8, f"got={len(mod_files)}")
ok("C.数字", f"单元清册可解析（实际 {len(inv)} 个单元）", len(inv) >= 20, f"got={len(inv)}")
m = re.search(r"(\d+)\s*个单元", skill)
if m:
    ok("C.数字", f"SKILL.md 声明的单元数与实际一致（实际 {len(inv)}）",
       int(m.group(1)) == len(inv), f"声明={m.group(1)} 实际={len(inv)}")

# C5 · 样例数量
ex_dir = os.path.join(SKILL, "examples")
ex_html = sorted(glob.glob(os.path.join(ex_dir, "**", "*.html"), recursive=True))
idx = rd(os.path.join(ex_dir, "INDEX.md"))
idx_files = set(re.findall(r"([\w\-.]+\.html)", idx)) if idx else set()
disk_files = set(os.path.basename(p) for p in ex_html)
if idx:
    ok("C.数字", f"examples/INDEX.md 条目与磁盘文件 100% 匹配（{len(disk_files)} 件）",
       idx_files == disk_files,
       f"仅索引={sorted(idx_files - disk_files)} 仅磁盘={sorted(disk_files - idx_files)}")
m = re.search(r"(\d+)\s*个已通过|(\d+)\s*件", skill)
if m and disk_files:
    declared = int(m.group(1) or m.group(2))
    ok("C.数字", f"SKILL.md 声明的样例数与实际一致（实际 {len(disk_files)}）",
       declared == len(disk_files), f"声明={declared} 实际={len(disk_files)}")

# C6 · 管线阶段数
orc = rd(os.path.join(SKILL, "references", "workflow-orchestrator.md"))
stages = ["INTENT", "PLAN", "BUILD", "VERIFY", "ASSEMBLE", "DELIVER", "REPORT", "LEARN"]
ok("C.数字", f"八阶段管线在 orchestrator 中齐备（{len(stages)} 阶段）",
   all(s in orc for s in stages),
   "缺：" + ",".join(s for s in stages if s not in orc))
m = re.search(r"(\d+)\s*阶段管线", skill)
if m:
    ok("C.数字", f"SKILL.md 声明的阶段数与管线定义一致（实际 {len(stages)}）",
       int(m.group(1)) == len(stages), f"声明={m.group(1)} 实际={len(stages)}")

# C7 · QA 门控项数
# 权威清册在 commercial-production-standards.md §8。检查两件事：
#   ① 清册「声称 N 项」与「实际列出几条」是否一致（清单增减后计数最容易忘改）
#   ② SKILL.md / README.md 声明的 QA 项数是否与清册实测条数一致（跨文档滞后）
cps = rd(os.path.join(SKILL, "references", "commercial-production-standards.md"))
QA_N = None
m = re.search(r"每个交付物必须通过以下\s*(\d+)\s*项检查：\s*\n(.*?)(?=\n任一项未通过)", cps, re.S)
if m:
    n_decl, body = int(m.group(1)), m.group(2)
    items = [l for l in body.splitlines() if l.strip().startswith("-")]
    QA_N = len(items)
    ok("C.数字", f"QA 清册：声称 {n_decl} 项与清单实际 {QA_N} 条一致",
       n_decl == QA_N, f"声称={n_decl} 实际={QA_N}")
else:
    ok("C.数字", "QA 清册可解析（commercial-production-standards.md §8）", False,
       "未匹配到「每个交付物必须通过以下 N 项检查」清单")

if QA_N:
    seen = set()
    # README：只取「质量保证」章节——那是当前标准的声明区，可避开「版本历史」里的旧值。
    # 不能用「邻近是否出现历史版本号」来判断：README 的当前声明
    # 「15 项 QA 门控（V4.3 的 12 项 + V5 新增 3 项）」本身就紧挨着 V4.3，会被误排除。
    i = readme.find("## 质量保证")
    rd_cur = readme[i:] if i >= 0 else readme
    # SKILL.md：无独立「质量保证」章节，改用历史语境排除
    for src_name, src, use_hist in (("README.md", rd_cur, False), ("SKILL.md", skill, True)):
        for mm in re.finditer(r"(\d+)\s*项\s*(?:标准\s*)?QA", src):
            v = int(mm.group(1))
            if use_hist:
                ctx = src[max(0, mm.start() - 60):mm.end() + 60]
                if HIST.search(ctx):
                    continue
            seen.add((src_name, v))
    for src_name, v in sorted(seen):
        ok("C.数字", f"{src_name} 声明的 QA 项数（{v}）与清册实测一致（{QA_N} 项）",
           v == QA_N, f"{src_name}={v} 清册={QA_N}")

# ------------------------------------------------------------ D. 引用完整性
print("[D] 引用完整性")
dangling = []
for src in [skill, readme] + [rd(p) for p in glob.glob(os.path.join(SKILL, "references", "*.md"))]:
    for mm in re.finditer(r"`((?:references|assets|examples|tests)/[\w\-./]+?\.(?:md|jsonl|json|js|py|sh|html))`", src):
        rel = mm.group(1)
        if not os.path.exists(os.path.join(SKILL, rel)):
            dangling.append(rel)
ok("D.引用", f"无悬空引用（扫描 {len(set(dangling))} 个疑似）", not dangling, f"悬空：{sorted(set(dangling))}")

# ------------------------------------------------------------ E. 目录与卫生
print("[E] 目录与卫生")
root_items = sorted(os.listdir(SKILL))
ALLOW = {"SKILL.md", "README.md", "meta.json", "references", "assets", "examples", "tests",
         "__pycache__", ".DS_Store"}
stray = [i for i in root_items if i not in ALLOW]
ok("E.卫生", f"根目录整洁（无临时/运行时文件）", not stray, f"多余：{stray}")

hc = []
for dirpath, dirnames, filenames in os.walk(SKILL):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git", "out")]
    for fn in filenames:
        if not fn.endswith((".md", ".json", ".jsonl", ".js", ".py", ".sh", ".html")):
            continue
        p = os.path.join(dirpath, fn)
        txt = rd(p)
        if "/root/.codebuddy" in txt and "tests/" not in os.path.relpath(p, SKILL):
            hc.append(os.path.relpath(p, SKILL))
ok("E.卫生", "零硬编码安装目录（/root/.codebuddy）", not hc, f"命中：{hc[:5]}")

SECRET = re.compile(r"(api[_-]?key|secret|password|passwd|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.I)
sec = []
for dirpath, dirnames, filenames in os.walk(SKILL):
    # 跳过 tests/：测试脚本里必然包含用于验证检测规则的「样例凭证」字符串，
    # 与硬编码路径检查同理，属测试代码而非交付内容。
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git", "out", "tests")]
    for fn in filenames:
        if fn.endswith((".md", ".json", ".js", ".py", ".sh", ".jsonl")):
            p = os.path.join(dirpath, fn)
            if SECRET.search(rd(p)):
                sec.append(os.path.relpath(p, SKILL))
ok("E.卫生", "零敏感信息（api_key/secret/password/token 字面量，tests/ 样例除外）",
   not sec, f"命中：{sec[:5]}")

bad_enc = []
for dirpath, dirnames, filenames in os.walk(SKILL):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git", "out")]
    for fn in filenames:
        if fn.endswith((".md", ".json", ".py", ".sh", ".jsonl", ".js")):
            p = os.path.join(dirpath, fn)
            try:
                open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                bad_enc.append(os.path.relpath(p, SKILL))
ok("E.卫生", "全部文本文件为 UTF-8", not bad_enc, f"非 UTF-8：{bad_enc[:5]}")

# ------------------------------------------------------------ F. L4 资产
print("[F] L4 资产齐备")
L4_ASSETS = ["references/automation-l4-scheduler.md", "references/automation-ops.md",
             "assets/automation-registry.json", "assets/run-ledger-template.jsonl",
             "assets/self-contained-prompt-template.md",
             "assets/playwright-control-test-harness.js"]
for rel in L4_ASSETS:
    ok("F.L4资产", f"存在 {rel}", os.path.exists(os.path.join(SKILL, rel)))
try:
    reg = json.load(open(os.path.join(SKILL, "assets", "automation-registry.json"), encoding="utf-8"))
    ok("F.L4资产", "automation-registry.json 是合法 JSON", True)
    ok("F.L4资产", "registry 含 stateSource 三层状态定义", "stateSource" in reg, list(reg.keys()))
    cache = str(reg.get("stateSource", {}).get("cache", ""))
    ok("F.L4资产", "状态缓存路径为平台无关表述（未硬编码 /workspace 等绝对前缀）",
       bool(cache) and not re.match(r"^/(workspace|home|Users|root)", cache), f"cache={cache}")
except Exception as e:
    ok("F.L4资产", "automation-registry.json 是合法 JSON", False, str(e))
ledger = os.path.join(SKILL, "assets", "run-ledger-template.jsonl")
if os.path.exists(ledger):
    lines = [l for l in rd(ledger).splitlines() if l.strip()]
    bad = []
    for i, l in enumerate(lines):
        try:
            json.loads(l)
        except Exception:
            bad.append(i + 1)
    ok("F.L4资产", f"run-ledger-template.jsonl 每行均为合法 JSON（{len(lines)} 行）", not bad, f"坏行：{bad}")

# ------------------------------------------------------------ G. 自包含契约
print("[G] 自包含契约")
tpl = rd(os.path.join(SKILL, "assets", "self-contained-prompt-template.md"))
SECTIONS = ["【角色】", "【会话】", "【任务】", "【状态】", "【幂等】",
            "【执行】", "【验证】", "【落点】", "【留痕】", "【失败】"]
miss = [s for s in SECTIONS if s not in tpl]
ok("G.契约", f"指令模板含全部 {len(SECTIONS)} 个必备段", not miss, f"缺：{miss}")
if ops:
    bad_cron = []
    for mm in re.finditer(r"--cron\s+[\"']?([0-9*\-\/, ]+)[\"']?", ops):
        c = mm.group(1).strip().split()
        if len(c) != 6 or c[0] != "0":
            bad_cron.append(mm.group(1))
    ok("G.契约", "OPS 注册命令中 cron 均为 6 位且秒位为 0", not bad_cron, f"违规：{bad_cron}")
    ok("G.契约", "OPS 命令均声明 frequency-type",
       ops.count("--frequency-type") >= len(re.findall(r"^## OPS-\d", ops, re.M)),
       f"count={ops.count('--frequency-type')}")

# ------------------------------------------------------------ H. 测试资产
print("[H] 测试资产齐备（可验证性）")
TESTS = ["t1-schedule-contract.py", "t2-idempotent-sim.py", "t3-scheduler-api.sh",
         "t4-artifact-regression.sh", "t4-build-ops5-artifacts.py",
         "t5-consistency-coverage.py", "selfcheck.py", "mutation-test.py"]
t_dir = os.path.join(SKILL, "tests")
for t in TESTS:
    ok("H.测试", f"存在 tests/{t}", os.path.exists(os.path.join(t_dir, t)))
# 只检测「变量被赋值为绝对安装路径」这种模式，而不是字符串里出现过该路径——
# 否则本文件（以及 T5）里用于检测硬编码的规则串本身会被误判成硬编码。
ASSIGN_HARD = re.compile(
    r"^\s*[A-Z_]+\s*=\s*[\"']?(?:/workspace|/root/|/home/|[A-Za-z]:\\\\)", re.M)
thc = []
for p in glob.glob(os.path.join(t_dir, "*.py")) + glob.glob(os.path.join(t_dir, "*.sh")):
    if ASSIGN_HARD.search(rd(p)):
        thc.append(os.path.basename(p))
ok("H.测试", "测试脚本零硬编码路径（可随包分发到任意机器）", not thc, f"命中：{thc}")

# ------------------------------------------------------------ 汇总
print("\n" + "=" * 78)
by = {}
for r in R:
    by.setdefault(r["group"], []).append(r)
for g, rs in by.items():
    p = sum(1 for r in rs if r["pass"])
    print(f"  {'✅' if p == len(rs) else '❌'} {g:<14} {p}/{len(rs)}")
print("-" * 78)
P = sum(1 for r in R if r["pass"])
print(f"  合计  {P}/{len(R)}   通过率 {P / len(R) * 100:.1f}%")
print("=" * 78)
fails = [r for r in R if not r["pass"]]
if fails:
    print("❌ 未通过明细：")
    for r in fails:
        print(f"  - [{r['group']}] {r['name']}  {r['detail']}")

rep = os.path.join(OUT, "selfcheck-results.json")
json.dump({"skill": SKILL, "total": len(R), "passed": P,
           "rate": round(P / len(R) * 100, 1), "results": R},
          open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
if not QUIET:
    print(f"\n明细已写入 {rep}")
sys.exit(0 if not fails else 1)
