#!/usr/bin/env python3
"""技能写作规范校验门（Writing Gate）——对任意技能目录跑 SKILL.md 写作规范检查。

标准：references/skill-writing-guide.md 第 5、6 节（本技能随包分发）。
用于：S7 闸门（写作规范门）+ 发布前自检 + 发布 changelog 校验。

目录检查项（python writing_gate.py <技能目录>）：
  W1 规模：SKILL.md ≤250 行（硬上限 600）
  W2 无生产侧文案：无 Wave [A-Z] / Phase [0-9] / "v2.x 新增" / "本次重构" /
     内部模块代号（churn_reflector 等） / 内部编码（L2/L3/L4、C1–C7）
  W3 触发词：description 含 "Use when"；正文含"何时使用"表
  W4 红线内联：正文含"红线"或"纪律"速查
  W5 注入三件套：§零 进化燃料（opt-in 说明）+ footer + coverage.md 引用
  W6 引用完整性：SKILL.md 引用的 references/* 都存在（双向 + 孤儿）
  W7 按需加载声明：references 文件开头注明加载时机（抽查最大的 3 个）
  W8 无孤儿文档：references 下所有文件都有归属

发布版本说明检查（python writing_gate.py --changelog "文本"）：
  W9 版本说明用户侧：无生产侧禁词（阻断）+ 有价值说明（警告）

用法：
  python writing_gate.py <技能目录>
  python writing_gate.py --changelog "v2.x.x：..."
退出码：0=通过（可发布）；2=未通过（退回 S7 重写 / changelog 重写）
"""
import os
import re
import sys

# 生产侧文案模式（披露范围红线）
PROD_PATTERNS = [
    r"\bWave\s+[A-Z]\b",          # Wave A/B/C 迭代代号
    r"\bPhase\s+[0-9]\b",          # Phase 0/1/2
    r"v\d+\.\d+.*(?:新增|更新)",   # 版本更新史
    r"本次重构",                    # 内部更新日志
    r"churn_reflector",            # 内部模块代号
    r"关④",                        # 内部编号
    r"\bL[1-7]\b.*(?:跨设备|互惠)", # 内部编码上下文
    r"【v\d",                       # 版本标注
    r"★\s*v\d",                    # 版本标注
]
# 发布版本说明（changelog）禁词——站用户侧，命中即阻断发布
CHANGELOG_PROD_PATTERNS = [
    r"\bWave\s+[A-Z]\b",            # Wave A/B/C
    r"\bPhase\s+[0-9]\b",           # Phase 0/1/2
    r"\bL[1-7]\b",                  # L2/L3/L4 层码（用户侧不会出现）
    r"\bGAP[\s-]?\d+\b",            # GAP-1/2/3 内部缺口编号
    r"\bBug\s*#\d+",                # Bug#23 等
    r"\bT-CAP\b",                   # 测试用例编号
    r"\bP[0-2]\b(?=[\s。；;，,]|$)", # P0/P1/P2 优先级代号
    r"\bchurn_reflector\b",         # 内部模块代号
    r"关④",                          # 内部编号
    r"\bC[1-7]\b(?=[\s。；;，,]|$)", # 归因编码 C1–C7
    r"\bCJG-EVO\b",                 # 平台工程代号
    r"\bSCF\b|\bVPC\b",             # 云函数/网络开发词汇
    r"迁移|部署|环境变量|SQL|数据库", # 开发侧过程/细节
    r"本次重构|本次更新",             # 内部重构叙事
    r"\.py\b",                      # 脚本文件名（内部实现细节）
    r"--[a-z][a-z0-9\-]+",          # 命令行参数（内部实现细节）
    r"\bPII\b",                     # 内部隐私术语（用户侧应说"不记内容"）
    r"\bedit_capture\b|\bbaseline\b|\bsignals?-log\b",  # 信号链路内部词
    r"\bloop apply\b|\bLoop\s+is\s+the\s+product\b",     # 内部口号/机制
]
# 价值信号词（判定"是否说清了改了什么/价值"）
VALUE_WORDS = ["新增", "改进", "优化", "修复", "提升", "支持", "可以", "现在",
               "不再", "更", "方便", "好用", "省心", "快捷", "一键", "自动"]
DEFAULT_MARK = "自动化发布"  # 默认模板特征
MIN_CHANGELOG_LEN = 15
# 必须内联的引用（注入三件套/关键命令）
MUST_HAVE = [
    r"## 零、进化燃料",              # 燃料 §零
    r"开启云同步",                    # opt-in
    r"别传了",                        # opt-out
    r"记录.{0,6}信号|信号.{0,6}记录", # 信号记录触发指令（防"会记录"但无"何时记录"→交互点失效）
    r"(?:会话结束|结束时|每次使用后)[^。\n]{0,50}(?:信号|记录)",  # W5b 信号触发指令需含"何时"语义
    r"客观.{0,6}使用|使用.{0,6}客观|\[使用\]",                    # W5c 客观使用汇报（G1：调外部服务时汇报客观事实）
    r"⚙️.*锻造|锻造.*⚙️",            # footer
    r"coverage",                      # coverage.md 引用
    r"forge-publish|quick_validate",  # 关键命令
]
# 已知例外引用（引用语义为"产物命名约定"或"应剔除物"，非包内必备文件，不判缺失）
EXEMPT_REFS = {
    "benchmark",   # 锻造过程台账（竞品对标），纪律 13 明确"剔除不进包"；仅锻造时按需生成
}
MAX_LINES = 250
HARD_MAX_LINES = 600


def check(name, cond, detail=""):
    mark = "✅" if cond else "❌"
    print(f"  {mark} {name}" + (f"  {detail}" if detail and not cond else ""))
    return cond


def _extract_description(md):
    """从 frontmatter 提取 description（支持单行与块状 | 两种 YAML 写法，块状优先）。"""
    if not md.startswith("---"):
        return ""
    fm = md.split("---", 2)[1]
    m = re.search(r"^description:[ \t]*\|\n((?:  .*\n?)+)", fm, re.M)
    if m:
        return re.sub(r"^  ", "", m.group(1), flags=re.M).strip()
    m = re.search(r"^description:[ \t]*([^|\n].*)$", fm, re.M)
    if m:
        return m.group(1).strip().strip('"')
    return ""


def _table_triggers(md):
    """从「何时使用」表第三列抽触发词：引号内词 + 英文词。"""
    m = re.search(r"## 何时使用.*?\n((?:\|.*\n)+)", md, re.S)
    if not m:
        return []
    trigs = []
    for row in m.group(1).splitlines():
        cols = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cols) < 3 or set("".join(cols)) <= {"-", ":"}:
            continue  # 表头/分隔行
        cell = cols[2]
        trigs += [q for pair in re.findall(r'“([^”]+)”|"([^"]+)"', cell) for q in pair if q]
        trigs += [e.strip() for e in re.findall(r"\b[a-zA-Z][a-zA-Z\- ]{1,25}\b", cell)
                  if e.strip().lower() not in ("when", "use")]
    return [t for t in trigs if t and len(t) >= 2]


def check_changelog(text):
    """发布版本说明校验。返回 (hits, warns)：
    hits=生产侧禁词命中（阻断级，发布工具拒绝发布）；
    warns=价值性提示（警告级，不阻断）。"""
    hits = []
    # 版本史检测：剥离开头的当前版本号前缀（changelog 正常以 v2.x.x： 开头），
    # 剩余文本中再出现版本号+新增/更新/重构 才算"版本更新史"
    body = re.sub(r"^v\d+\.\d+\.\d+\s*[:：]?\s*", "", text.strip(), count=1)
    for m in re.finditer(r"v\d+\.\d+\.\d+.*(?:新增|更新|重构)", body, re.IGNORECASE):
        hits.append(f"{m.group(0)[:40]}  ← 命中「版本更新史」")
    # 其余禁词跑全文
    for pat in CHANGELOG_PROD_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            hits.append(f"{m.group(0)}  ← 命中「{pat}」")
    warns = []
    if DEFAULT_MARK in text:
        warns.append("内容像是默认模板（含「自动化发布」），建议补一句实际改动与价值")
    if len(text.strip()) < MIN_CHANGELOG_LEN:
        warns.append(f"过短（{len(text.strip())} 字），建议按模板写 2–5 条：改了什么 + 价值")
    elif not any(w in text for w in VALUE_WORDS):
        warns.append("未检测到价值词（新增/改进/修复/更…），建议说清「改了什么、有什么价值」")
    return hits, warns


def main():
    # -h/--help：打印用法并正常退出（不再被误判为技能目录）
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    # --changelog 模式：只校验发布版本说明，不依赖技能目录
    if len(sys.argv) >= 3 and sys.argv[1] == "--changelog":
        text = sys.argv[2]
        print("Writing Gate W9 · 发布版本说明（Release Notes）校验")
        hits, warns = check_changelog(text)
        ok = not hits
        results = [check("W9 无生产侧禁词（站用户侧）", ok,
                         "；".join(hits[:6]) if hits else "")]
        if not ok:
            print("\n  禁词提示：版本说明会展示给终端用户，请改写为「改了什么 + 有什么价值」，")
            print("  参考 references/skill-writing-guide.md 第 6 节模板与正反对照。")
            for w in warns:
                print(f"  ⚠ {w}")
            print("\nWriting Gate: 0/1 通过（changelog 需重写）")
            sys.exit(2)
        for w in warns:
            print(f"  ⚠ {w}")
        print("\nWriting Gate: 1/1 通过（changelog 可发布）")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("用法：python writing_gate.py <技能目录>")
        sys.exit(2)
    skill_dir = os.path.abspath(sys.argv[1])
    md_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(md_path):
        print(f"❌ SKILL.md 不存在: {md_path}")
        sys.exit(2)

    md = open(md_path, encoding="utf-8").read()
    lines = md.splitlines()
    results = []

    # W1 规模
    n = len(lines)
    results.append(check(f"W1 规模：{n} 行（目标 ≤{MAX_LINES}，硬上限 {HARD_MAX_LINES}）",
                         n <= HARD_MAX_LINES, f"超硬上限 {HARD_MAX_LINES}"))

    # W2 无生产侧文案
    hits = []
    for pat in PROD_PATTERNS:
        for m in re.finditer(pat, md, re.IGNORECASE):
            ln = md[:m.start()].count("\n") + 1
            hits.append(f"L{ln}:{m.group(0)}")
    results.append(check(f"W2 无生产侧文案（发现 {len(hits)} 处）", not hits,
                         "；".join(hits[:8])))

    # W3 触发词（含 SEO：W3a 描述长度 / W3b 描述与触发词表互文）
    has_use_when = "Use when" in md
    has_trigger_table = "何时使用" in md
    results.append(check("W3 触发词：description 含 Use when + 何时使用表",
                         has_use_when and has_trigger_table))

    desc = _extract_description(md)
    # W3a 描述 ≤1024 字符（跨平台安装 zip 兼容线）
    results.append(check(f"W3a description ≤1024 字符（当前 {len(desc)}）",
                         len(desc) <= 1024, f"超长 {len(desc) - 1024} 字符，平台安装 zip 可能报错"))

    # W3b 描述含触发词：从「何时使用」表抽触发词，description 命中 ≥3（表词互文 = SEO 一致）
    if has_trigger_table:
        trigs = _table_triggers(md)
        hits = [t for t in trigs if t and t.lower() in desc.lower()]
        results.append(check(f"W3b description 命中触发词 {len(hits)} 个（目标 ≥3，表内 {len(trigs)} 个）",
                             len(hits) >= 3, f"命中 {hits[:5]}；需 ≥3 个触发词自然嵌入 description"))
    else:
        results.append(check("W3b description 命中触发词（无何时使用表，跳过）", True))

    # W4 红线内联
    has_redline = ("红线" in md) or ("纪律" in md and "速查" in md)
    results.append(check("W4 红线内联（正文含红线/纪律速查）", has_redline))

    # W5 注入三件套
    missing = [p for p in MUST_HAVE if not re.search(p, md, re.IGNORECASE)]
    results.append(check(f"W5 注入三件套+关键命令（缺 {len(missing)}）", not missing,
                         "；".join(missing)))

    # W10 信号套件完整（闭环断点防线：产出技能必须有回传能力，防"会记录但不回传"）
    kit = ["scripts/upload_signals.py", "scripts/signal_control.py",
           "scripts/download_signals.py", "cloud_config.json", "references/signals.md"]
    miss_kit = [k for k in kit if not os.path.exists(os.path.join(skill_dir, k))]
    results.append(check(f"W10 信号套件完整（缺 {len(miss_kit)}）", not miss_kit,
                         "；".join(miss_kit) + "；运行 scripts/forge-signal-kit.py <目录> 注入"))

    # W6 引用完整性（双向：SKILL.md + 所有 references；排除已知例外）
    ref_dir = os.path.join(skill_dir, "references")
    docs = ["SKILL.md"] + [f"references/{f}" for f in os.listdir(ref_dir) if f.endswith(".md")]
    referenced = set()
    for doc in docs:
        p = os.path.join(skill_dir, doc)
        if os.path.exists(p):
            referenced.update(re.findall(r"references/([A-Za-z0-9_\-]+)\.md", open(p, encoding="utf-8").read()))
    missing_refs = sorted(r for r in referenced
                          if r not in EXEMPT_REFS and not os.path.exists(os.path.join(ref_dir, f"{r}.md")))
    results.append(check(f"W6 引用完整性（双向引用 {len(referenced)} 个文件，缺 {len(missing_refs)}）",
                         not missing_refs, "；".join(missing_refs)))

    # W7 按需加载声明（抽查最大的 3 个 references 文件——聚合文件最需要声明；小单点文件可无）
    sizes = []
    for r in (referenced - EXEMPT_REFS):
        p = os.path.join(ref_dir, f"{r}.md")
        if os.path.exists(p):
            sizes.append((os.path.getsize(p), r))
    sizes.sort(reverse=True)
    checked = []
    for _, r in sizes[:3]:
        head = open(os.path.join(ref_dir, f"{r}.md"), encoding="utf-8").read()[:200]
        checked.append(r if ("加载" in head or "读取" in head or "触发" in head) else f"{r}（缺声明）")
    ok_load = all("（缺声明）" not in c for c in checked)
    results.append(check(f"W7 按需加载声明（抽查最大文件：{'、'.join(checked)}）", ok_load))

    # W8 孤儿文档：references 下存在但从未被任何文档引用
    all_refs = {f[:-3] for f in os.listdir(ref_dir) if f.endswith(".md")}
    orphans = sorted(all_refs - referenced)
    results.append(check(f"W8 无孤儿文档（references 共 {len(all_refs)} 个，孤儿 {len(orphans)}）",
                         not orphans, "；".join(orphans)))

    passed = sum(1 for r in results if r)
    print(f"\nWriting Gate: {passed}/{len(results)} 通过")
    sys.exit(0 if passed == len(results) else 2)


if __name__ == "__main__":
    main()
