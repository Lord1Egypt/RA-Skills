#!/usr/bin/env python3
"""
check_consistency.py — A-stock-report 8 端一致性护栏（v3.3.0 — 含 H 段）脚本

检查 SKILL.md / templates/ / cron_jobs/ / ~/.hermes/cron/jobs.json 4 端
在"任务清单 / 文件路径 / prompt 内容"三方面是否一致。

设计目标：
- 单文件、无外部依赖（stdlib only）
- 退出码：0=全过，1=有错误，2=致命（路径错）
- 输出清晰：每条错误单独一行，附修复建议
- 不修改任何文件（只读）

用法：
  python3 scripts/check_consistency.py            # CI 模式，只看退出码
  python3 scripts/check_consistency.py --verbose  # 显示每条 ✅ 通过
  python3 scripts/check_consistency.py --fix-hint # 错误时打印修复建议

触发场景（v3.1.5+ 必须遵守）：
- 修改 templates/*.json 后：跑一次
- 修改 cron_jobs/cron_mirror.json 后：跑一次
- 修改 ~/.hermes/cron/jobs.json 中 3 个独立脚本任务后：跑一次
- 修改 SKILL.md 任务清单段后：跑一次
- release 前：跑一次

历史：
- v3.1.5 新建（解决"担心漏改"动机，根除 templates/intraday.json 那种幽灵模板的再发）
- v3.1.6 加 E 段（SKILL.md 主体禁 cron/.env/source+send 残留）
- v3.2.0 加 F 段（Changelog 单条长度硬上限 25 行）
- v3.2.5 加 G 段（独立脚本型 cron prompt 必走纯 bash）
- v3.3.0 加 H 段（templates 段标题 ↔ 「本段硬约束」锚定同步，1:1 同步护栏）
"""

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path("/root/.hermes/skills/A-stock-report")
TEMPLATES_DIR = SKILL_DIR / "templates"
CRON_MIRROR = SKILL_DIR / "cron_jobs" / "cron_mirror.json"
SKILL_MD = SKILL_DIR / "SKILL.md"
JOBS_JSON = Path.home() / ".hermes" / "cron" / "jobs.json"

# dispatcher 支持的 3 个 LLM 任务（来源：scripts/skill_dispatcher.py argparse choices）
DISPATCHER_TASKS = {"morning", "evening", "weekend"}

# 任务名 ↔ 人类可读名（来自 jobs.json 习惯）
HUMAN_NAME = {
    "close_summary": "A股收盘小结",
    "intraday": "A股盘中预警",
    "ipo_report": "A股IPO周报",
}


def header(s):
    print(f"\n=== {s} ===")


def ok(msg, verbose=False):
    if verbose:
        print(f"  ✅ {msg}")


def fail(msg, fix_hint=None):
    print(f"  ❌ {msg}")
    if fix_hint:
        print(f"     💡 修复：{fix_hint}")


def section_a(verbose=False):
    """A. templates/ ↔ cron_mirror：3 个 LLM 任务 ⊆ cron_mirror.tasks"""
    header("A. templates/ 与 cron_mirror 任务交集")
    if not CRON_MIRROR.exists():
        fail(f"{CRON_MIRROR} 不存在")
        return False
    mirror = json.loads(CRON_MIRROR.read_text())
    mirror_keys = set(mirror.get("tasks", {}).keys())

    templates_files = {f.stem for f in TEMPLATES_DIR.glob("*.json") if f.suffix == ".json"}
    llm_in_templates = templates_files & DISPATCHER_TASKS
    ok(f"templates/ 含 LLM 任务: {sorted(llm_in_templates)}", verbose)

    # 全部 LLM 任务应在 cron_mirror 之外（它们不是独立脚本），所以此处只确认 templates 存在性
    missing_in_templates = DISPATCHER_TASKS - templates_files
    if missing_in_templates:
        fail(f"dispatcher 期望的 LLM 任务 {missing_in_templates} 在 templates/ 缺失")
        return False
    ok("dispatcher 3 任务 ↔ templates/ 一致", verbose)
    return True


def section_b(verbose=False):
    """B. cron_mirror ↔ jobs.json：3 任务的 prompt 字段一字不差"""
    header("B. cron_mirror 与 jobs.json prompt 一致性")
    if not CRON_MIRROR.exists():
        fail(f"{CRON_MIRROR} 不存在")
        return False
    if not JOBS_JSON.exists():
        fail(f"{JOBS_JSON} 不存在")
        return False

    mirror = json.loads(CRON_MIRROR.read_text())
    jobs = json.loads(JOBS_JSON.read_text())
    jobs_by_name = {j["name"]: j for j in jobs.get("jobs", [])}

    all_ok = True
    for task_key, human_name in HUMAN_NAME.items():
        if task_key not in mirror["tasks"]:
            fail(f"cron_mirror.tasks 缺 {task_key}（{human_name}）")
            all_ok = False
            continue
        if human_name not in jobs_by_name:
            fail(f"jobs.json 缺 {human_name}（cron_mirror 里有 {task_key}）")
            all_ok = False
            continue

        mirror_prompt = mirror["tasks"][task_key]["prompt"]
        jobs_prompt = jobs_by_name[human_name]["prompt"]
        if mirror_prompt == jobs_prompt:
            ok(f"{human_name} prompt 一字不差", verbose)
        else:
            fail(f"{human_name} prompt 不一致")
            print(f"     jobs.json  ({len(jobs_prompt)} 字符): {jobs_prompt[:60]!r}...")
            print(f"     mirror     ({len(mirror_prompt)} 字符): {mirror_prompt[:60]!r}...")
            print(f"     💡 修复：改 jobs.json 或 mirror 中落后的那个")
            all_ok = False
    return all_ok


def section_c(verbose=False):
    """C. SKILL.md 任务清单段 ↔ 文件存在：3 模板 + 3 镜像引用都应真实存在"""
    header("C. SKILL.md 任务清单段引用有效性")
    if not SKILL_MD.exists():
        fail(f"{SKILL_MD} 不存在")
        return False

    skill_text = SKILL_MD.read_text()

    # 找形如 "### N. 任务名（详见 path）" 的标题行
    heading_re = re.compile(r"^### \d+\. (.+?)（详见 (.+?)）", re.MULTILINE)
    headings = heading_re.findall(skill_text)

    all_ok = True
    for task_name, ref in headings:
        # 解析 ref
        if ref.startswith("templates/") and ref.endswith(".json"):
            # 模板路径
            f = SKILL_DIR / ref
            if not f.exists():
                fail(f"SKILL.md 任务 '{task_name}' 引用 {ref} 但文件不存在")
                all_ok = False
            else:
                ok(f"任务 '{task_name}' → {ref} 存在", verbose)
        elif ref.startswith("cron_jobs/cron_mirror.json#"):
            # 镜像路径，格式：cron_jobs/cron_mirror.json#task_key
            task_key = ref.split("#", 1)[1]
            if not CRON_MIRROR.exists():
                fail(f"SKILL.md 任务 '{task_name}' 引用 {ref} 但 mirror 不存在")
                all_ok = False
                continue
            mirror = json.loads(CRON_MIRROR.read_text())
            if task_key not in mirror.get("tasks", {}):
                fail(f"SKILL.md 任务 '{task_name}' 引用 {ref} 但 mirror.tasks 缺 {task_key}")
                all_ok = False
            else:
                ok(f"任务 '{task_name}' → {ref} 存在", verbose)
        else:
            fail(f"SKILL.md 任务 '{task_name}' 引用 {ref} 格式无法识别（既不是 templates/ 也不是 cron_mirror.json#）")
            all_ok = False
    return all_ok


def section_d(verbose=False):
    """D. dispatcher 支持的 task ⊆ templates/ 实际文件"""
    header("D. dispatcher ↔ templates/ 实际文件")
    dispatcher_in_mirror_set = set()  # dispatcher 的 task 应不在 mirror（它们是 LLM 任务）
    if CRON_MIRROR.exists():
        mirror = json.loads(CRON_MIRROR.read_text())
        dispatcher_in_mirror_set = set(mirror.get("tasks", {}).keys())

    conflict = DISPATCHER_TASKS & dispatcher_in_mirror_set
    if conflict:
        fail(f"dispatcher 任务 {conflict} 不应出现在 cron_mirror（它们是 LLM 任务不是独立脚本）")
        return False
    ok(f"dispatcher 任务 {DISPATCHER_TASKS} 与 cron_mirror 任务无重叠", verbose)
    return True


def section_e(verbose=False):
    """E. SKILL.md 主体（任务清单段之外）禁止出现 cron 表达式和 source .env 命令

    v3.1.5 清理动机：v3.0 外置了 templates/ 和 cron_jobs/，但 SKILL.md 主体里
    仍残留「## 快速开始」11 条 source 命令、「## 定时任务」7 个 cron 表达式、
    「## 安装与验证」Step 1/3 重复表——v3.1.5 清理后用 E 段护栏机械锁。

    合法例外（不算违规）：
    - 任务清单段「### N. 任务名（详见 path）」只引用路径不写具体表达式
    - Changelog 段可追溯历史（v3.0 之前确实在 SKILL.md 里写过 cron）
    - 4 端一致性警告段举的「反例」（脚本注释里允许解释）

    实现：白名单段落放行，其余段落扫黑名单正则。
    """
    header("E. SKILL.md 主体禁止硬编码 cron 表达式和 .env 路径")
    if not SKILL_MD.exists():
        fail(f"{SKILL_MD} 不存在")
        return False

    text = SKILL_MD.read_text()
    lines = text.split("\n")

    # 黑名单：v3.1.5 之前在 SKILL.md 主体里出现过的"残留模式"
    # cron 表达式：用反引号包住 + 5 段 数字/*/,- 组合（嵌入行内或整行都算）
    # 注：必须 ≥3 段才算 cron（避免误伤 `0.8` 这种带反引号的小数）
    cron_pat = re.compile(r"`[\d\*\/\,\-]+\s+[\d\*\/\,\-]+\s+[\d\*\/\,\-]+[^`]*`")
    env_pat = re.compile(r"source /workspace/\.env")
    send_inline_pat = re.compile(r"source /workspace/\.env.*python3.*send_\w+\.py")

    # 段落白名单：这些段落允许出现黑名单模式
    # v3.1.6 修订：Changelog 段统一放行（任何版本号标题 + 任务清单段）
    # 注：不允许 ## / ### 标号写死某个具体版本号，否则每次 bump 都要改这里
    allowed_h2 = set()  # Changelog 已通过"## 版本历史（Changelog）"标志整体放行
    # ### 标题里识别 Changelog 版本（格式：### vX.Y.Z — ...）
    import re as _re
    changelog_h3_pat = _re.compile(r"^###\s+v\d+\.\d+\.\d+\s+—")

    # 标记当前段落是否在白名单内
    in_allowed_section = False
    current_section = None
    all_ok = True
    violations = []

    for i, line in enumerate(lines, 1):
        # 段落切换：检查 ## 或 ### 标题
        if line.startswith("## ") and not line.startswith("####"):
            current_section = line
            # 白名单：Changelog 大段 (## 版本历史) + ## 任务清单段（如 "## Cron 任务配置指引"）
            in_allowed_section = (
                current_section in allowed_h2
                or current_section.startswith("## 版本历史")
            )
            continue
        if line.startswith("### ") and not line.startswith("####"):
            # Changelog 段内的版本号标题（### vX.Y.Z — ...）= 放行
            in_allowed_section = changelog_h3_pat.match(line) is not None
            continue
        if line.startswith("#### "):
            # 4 级标题继承上一级 ### 的状态
            pass

        if in_allowed_section:
            continue

        # 扫黑名单
        if cron_pat.search(line):
            violations.append((i, "cron 表达式", line.strip()[:80]))
        if env_pat.search(line):
            violations.append((i, ".env 路径", line.strip()[:80]))
        if send_inline_pat.search(line):
            violations.append((i, "source+send 一行命令", line.strip()[:80]))

    if violations:
        for i, kind, snippet in violations:
            fail(f"L{i} 命中 '{kind}': {snippet}")
        print(f"     💡 修复：删掉 SKILL.md 主体里这些硬编码，改用「详见 cron_jobs/cron_mirror.json」的引用")
        print(f"     💡 任务清单段（L884~L906）允许出现，因为只引用路径不写具体表达式")
        print(f"     💡 Changelog 段允许出现，因为是历史追溯")
        all_ok = False
    else:
        ok("SKILL.md 主体（任务清单段 + Changelog 段之外）无 cron 表达式 / .env 路径 / source+send 残留", verbose)
    return all_ok


def section_g(verbose=False):
    """G. jobs.json 7 个独立脚本型 cron 的 prompt 必走纯 bash，禁止 LLM 调度关键词

    v3.2.5 修复动机：v3.1.4 已把收盘小结/IPO 周报改成 `source .env && python3 send_*.py`
    纯 bash prompt（不触发 LLM）。盘中预警漏改——旧 prompt 是 285 字符的"执行步骤+关键
    词路由"，脚本输出含"已推送"才汇报、含"已推送过跳过"就 [SILENT]。但脚本内部
    state 文件去重已 100% 拦掉重复推送，**LLM 这层"看门狗"是 100% 冗余**——每天 48 次
    × 30k token = ~1.46M token/日浪费。

    判别公式：
    - 任务名 ∈ DISPATCHER_TASKS (morning/evening/weekend) = LLM 驱动型 → prompt 含步骤合法
    - 任务名 ∉ DISPATCHER_TASKS = 独立脚本型 → prompt 必须是 bash 一行

    黑名单（独立脚本型 prompt 包含就 fail）：
    - `执行以下步骤` —— 步骤式 prompt 标志
    - `决定响应` / `决定汇报` —— LLM 决策关键词
    - `汇报这条` —— 显式 LLM 汇报指令
    - `[SILENT]` —— v3.1.4 已废弃
    - `看脚本输出` / `输出包含` —— LLM 看 stdout 模式

    合法例外（不算违规）：
    - LLM 驱动型任务（morning/evening/weekend）的 prompt 含步骤是设计意图
    - SKILL.md Changelog 段提到这些词是合理的历史记录
    """
    header("G. 独立脚本型 cron prompt 必走纯 bash（v3.2.5+ 护栏）")
    if not JOBS_JSON.exists():
        fail(f"{JOBS_JSON} 不存在")
        return False

    with open(JOBS_JSON, 'r', encoding='utf-8') as f:
        jobs_data = json.load(f)

    jobs_list = jobs_data.get('jobs', [])

    # 黑名单关键词（独立脚本型 prompt 必不含）
    blacklist_keywords = [
        ("执行以下步骤", "步骤式 prompt 标志"),
        ("决定响应", "LLM 决策关键词"),
        ("决定汇报", "LLM 决策关键词"),
        ("汇报这条", "显式 LLM 汇报指令"),
        ("[SILENT]", "v3.1.4 已废弃的 SILENT 模式"),
        ("看脚本输出", "LLM 看 stdout 模式"),
        ("输出包含", "关键词路由"),
    ]

    all_ok = True
    violations = []

    for job in jobs_list:
        job_name = job.get('name', '')
        # 用 HUMAN_NAME 反查任务 key（morning/evening/weekend 等）
        # jobs.json 里 name 是中文，需要从 prompt 里识别 task 类型
        # 简化策略：扫所有非 LLM 任务（即 prompt 不在 DISPATCHER_TASKS 的 4 个 + 每周 Skill 复盘）
        prompt = job.get('prompt', '')

        # 判别：是否为 LLM 驱动型任务
        # 策略：job prompt 含 `python3 scripts/skill_dispatcher.py` → LLM 驱动
        # 否则 → 独立脚本型（必须纯 bash）
        is_llm_driven = "skill_dispatcher" in prompt

        if is_llm_driven:
            # LLM 驱动型任务：prompt 含步骤合法
            ok(f"{job_name}（LLM 驱动型，dispatcher）跳过 G 段检查", verbose)
            continue

        # 独立脚本型任务：扫黑名单
        for keyword, description in blacklist_keywords:
            if keyword in prompt:
                violations.append((job_name, job.get('id', '?'), keyword, description))

    if violations:
        for job_name, job_id, keyword, description in violations:
            fail(f"任务「{job_name}」(id={job_id}) prompt 含 LLM 调度关键词 '{keyword}' ({description})")
        print(f"     💡 修复：独立脚本型 cron 的 prompt 必须是纯 bash 一行：")
        print(f"        source /workspace/.env && python3 /root/.hermes/skills/A-stock-report/scripts/send_XXX.py 2>&1")
        print(f"     💡 如果你想让 LLM 看脚本输出做汇报，说明你在写 LLM 驱动型任务——")
        print(f"        那应该改用 dispatcher 任务模板（morning/evening/weekend），而不是塞 LLM 到独立脚本 cron")
        print(f"     💡 例外：v3.1.4 已改完的 close_summary / ipo_report / intraday 都是纯 bash，应保持")
        all_ok = False
    else:
        n_independent = sum(1 for j in jobs_list if "skill_dispatcher" not in j.get('prompt', ''))
        ok(f"{n_independent} 个独立脚本型 cron 全部纯 bash，无 LLM 调度关键词", verbose)
    return all_ok





def section_h(verbose=False):
    """H. templates/*.json 段标题 ↔ 「本段硬约束」锚定同步（v3.3.0+ 护栏）

    v3.3.0 修复动机：v3.2.9 重构采用「约束即模板」一体化架构 —— 每个段标题
    （━━━ X、Y ━━━）后面必须紧跟【本段硬约束 — ...】锚点，**1:1 同步**。
    LLM 看到段标题 + 紧跟的硬约束 → 不会漏看约束。

    v3.2.9 之前的隐患：硬约束散落在 prompt 末尾，LLM 注意力容易漏掉 → 出现
    "已生成内容但违反约束"（"约 3200 点"、要闻挤一起、依据超 120 字符等）。

    机械检测：对每个 templates/*.json 的 prompt 字段：
    1. 找所有 `━━━ [^━]+? ━━━` 段标题
    2. 找所有【本段硬约束】锚点
    3. 段标题数 vs 硬约束数 必须相等
    4. 每个段标题后面（直到下一个段标题或 prompt 结束）必须含 ≥ 1 个【本段硬约束】

    例外（不算违规）：
    - 段标题 = "风险提示"（附加段）：硬约束数可 0 或 1
    """
    header("H. templates/*.json 段标题 ↔ 「本段硬约束」锚定同步（v3.3.0+ 护栏）")
    if not TEMPLATES_DIR.exists():
        fail(f"{TEMPLATES_DIR} 不存在")
        return False

    # 段标题正则（v3.4.1+ 三种格式兼容）:
    #   1. 老格式: ━━━ X ━━━ (段结构, 必须 1:1 配对硬约束)
    #   2. 新格式: --- X --- (v3.4.1 替代 ━━━, 避免 LLM 注意力漂移)
    #   3. ──── X ──── (自动注入段元标记, 4 字符, 跟 ━ 区别, 不算段标题)
    # 排除项:
    #   · markdown 表格分隔行: |---|---|...| (用 \|--- 开头)
    #   · dispatcher 注入的 5d 数据块: "5d 原始数据" (跟 "──── v3.4 数据驱动" 同级, 不算段标题)
    section_pat = re.compile(
        r"(?<!\|)(?:━━━|---)\s*([^━─|]+?)\s*(?:━━━|---)(?!─)"
    )
    # 段标题二次过滤: 排除 markdown 表格分隔 + dispatcher 注入段
    def is_real_section(name):
        n = name.strip()
        if n.startswith("|"):  # markdown 表格分隔
            return False
        if n == "5d 原始数据（v3.4 数据驱动）":  # dispatcher 注入, 跟 "──── v3.4 数据驱动" 同源
            return False
        return True
    # 本段硬约束锚点
    hard_anchor = "【本段硬约束"

    all_ok = True
    for tpl in sorted(TEMPLATES_DIR.glob("*.json")):
        try:
            d = json.loads(tpl.read_text())
        except Exception as e:
            fail(f"{tpl.name} JSON 解析失败: {e}")
            all_ok = False
            continue

        prompt = d.get("prompt", "")
        if not prompt:
            ok(f"{tpl.name} 无 prompt 字段（独立脚本型），跳过 H 段检查", verbose)
            continue

        # 1. 找所有段标题 + 位置（过滤掉 markdown 表格分隔 + dispatcher 注入段元标记）
        sections = [(m.group(1).strip(), m.start()) for m in section_pat.finditer(prompt) if is_real_section(m.group(1))]
        # 2. 找所有【本段硬约束】+ 位置
        anchors = [m.start() for m in re.finditer(re.escape(hard_anchor), prompt)]

        # 3. 检查段标题 vs 硬约束数
        sec_count = len(sections)
        anchor_count = len(anchors)

        # 段标题可以 0 个（如果模板无段结构）→ 此时硬约束也必须 0
        if sec_count == 0 and anchor_count == 0:
            ok(f"{tpl.name} 无段结构（无段标题 + 无硬约束）", verbose)
            continue

        if sec_count != anchor_count:
            fail(f"{tpl.name} 段标题 {sec_count} 个 vs 「本段硬约束」{anchor_count} 个 — 不一致")
            print(f"     段标题列表：{[s[0] for s in sections]}")
            print(f"     💡 修复：每个 ━━━ X ━━━ 段标题后必须紧跟 1 个【本段硬约束】锚点")
            print(f"     💡 例外：「风险提示」是附加段（无数字编号），硬约束数可 0 或 1")
            all_ok = False
            continue

        # 4. 检查每个段标题后是否含 ≥ 1 个硬约束锚点
        # 计算每个段标题位置之后的下一个段标题位置（如果是最后一个则到 prompt 末尾）
        per_sec_violations = []
        for i, (sec_name, sec_pos) in enumerate(sections):
            if i + 1 < len(sections):
                next_pos = sections[i + 1][1]
            else:
                next_pos = len(prompt)
            # 段内硬约束数
            sec_anchors = sum(1 for a in anchors if sec_pos < a < next_pos)
            # 「风险提示」是附加段：硬约束数允许 0 或 1
            if sec_name == "风险提示":
                if sec_anchors > 1:
                    per_sec_violations.append((sec_name, sec_anchors, "附加段「风险提示」硬约束 ≤ 1"))
            else:
                if sec_anchors < 1:
                    per_sec_violations.append((sec_name, sec_anchors, "段后缺【本段硬约束】锚点"))

        if per_sec_violations:
            fail(f"{tpl.name} 段标题 ↔ 硬约束位置错位")
            for sec_name, cnt, reason in per_sec_violations:
                print(f"     ❌ 段「{sec_name}」：硬约束 {cnt} 个 — {reason}")
            all_ok = False
        else:
            ok(f"{tpl.name} {sec_count} 段标题 ↔ {anchor_count} 个硬约束 1:1 同步", verbose)
            for sec_name, _ in sections:
                print(f"       · 段「{sec_name}」: ✅ 硬约束就位")

    return all_ok


# Changelog 单条硬上限（行数）—— v3.2.0 护栏
CHANGELOG_MAX_LINES = 25


def section_f(verbose=False):
    """F. SKILL.md Changelog 段每条 ### vX.Y.Z — 标题之间行数 ≤ 25（v3.2.0+ 硬上限）

    动机：v3.0 之前 Changelog 段自由膨胀，单条最大 86 行（v3.0.0 本身），整段
    488 行占 SKILL.md 48.8%。v3.2.0 拆分：精简版（≤18 行软目标、≤25 行硬上限）
    留 SKILL.md，完整细节外置到 knowledge/changelog/vX.Y.Z.md。

    机械检测：从 `## 版本历史` 之后到下一个 `## ` 之前，每段 `### vX.Y.Z — ...`
    标题起，到下一个 `### vX.Y.Z` 或段尾，计算总行数（含标题 + 空行 + 内容），
    超过 CHANGELOG_MAX_LINES 视为违规。
    """
    header(f"F. Changelog 段单条长度硬上限（≤ {CHANGELOG_MAX_LINES} 行）")
    if not SKILL_MD.exists():
        fail(f"{SKILL_MD} 不存在")
        return False

    text = SKILL_MD.read_text()
    lines = text.split("\n")

    # 找 Changelog 段起止
    cl_start = None
    cl_end = None
    for i, line in enumerate(lines):
        if line.startswith("## 版本历史"):
            cl_start = i
        elif cl_start is not None and line.startswith("## ") and not line.startswith("## 版本历史"):
            cl_end = i
            break

    if cl_start is None or cl_end is None:
        fail("未找到 Changelog 段（期望以「## 版本历史」开头）")
        return False

    # 找每个 ### vX.Y.Z — 标题
    ver_pat = re.compile(r"^###\s+v\d+\.\d+\.\d+\s+—")
    starts = []  # [(行号 0-indexed, 版本号段标题)]
    for i in range(cl_start + 1, cl_end):
        m = ver_pat.match(lines[i])
        if m:
            starts.append(i)

    if not starts:
        fail("Changelog 段内未发现任何 ### vX.Y.Z — 条目")
        return False

    # 计算每条行数（标题行 -> 下一条标题行 - 1；最后一条 -> 段尾 - 1）
    violations = []
    for idx, start in enumerate(starts):
        if idx + 1 < len(starts):
            end = starts[idx + 1]
        else:
            end = cl_end
        # 标题里取版本号
        m = re.search(r"v(\d+\.\d+\.\d+)", lines[start])
        ver = m.group(1) if m else f"L{start+1}"
        # 包含标题行、空行、内容
        line_count = end - start
        # 段尾空行不计（end 通常指向下一条标题；最后一条 end = cl_end，cl_end 是下个 ## 段首）
        if line_count > CHANGELOG_MAX_LINES:
            violations.append((ver, start + 1, end, line_count))
        else:
            ok(f"v{ver} (L{start+1}~L{end}): {line_count} 行", verbose)

    if violations:
        for ver, s, e, cnt in violations:
            fail(f"v{ver} (L{s}~L{e}): {cnt} 行 > 硬上限 {CHANGELOG_MAX_LINES} 行")
        print(f"     💡 修复：精简该条到 ≤ {CHANGELOG_MAX_LINES} 行（软目标 18 行）")
        print(f"     💡 完整细节外置到 knowledge/changelog/{ver}.md（v3.2.0 新建）")
        print(f"     💡 Changelog 段开头注释有精简规则和护栏说明")
        return False

    print(f"  📊 Changelog 段共 {len(starts)} 条，最长 {max(end - s for s, end in zip(starts, starts[1:] + [cl_end]))} 行")
    return True


def main():
    args = sys.argv[1:]
    verbose = "--verbose" in args
    fix_hint = "--fix-hint" in args

    print("=" * 60)
    print("A-stock-report 8 端一致性护栏（v3.3.0 — 含 H 段）")
    print("=" * 60)
    print(f"SKILL_DIR     = {SKILL_DIR}")
    print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")
    print(f"CRON_MIRROR   = {CRON_MIRROR}")
    print(f"SKILL_MD      = {SKILL_MD}")
    print(f"JOBS_JSON     = {JOBS_JSON}")
    print(f"模式          = {'verbose' if verbose else 'normal'}")

    # 检查关键路径
    if not SKILL_DIR.exists():
        print(f"\n❌ 致命：{SKILL_DIR} 不存在")
        return 2

    results = []
    for sec in [section_a, section_b, section_c, section_d, section_e, section_f, section_g, section_h]:
        try:
            results.append(sec(verbose=verbose))
        except Exception as e:
            fail(f"{sec.__name__} 抛异常: {e}")
            results.append(False)

    print()
    print("=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    if all(results):
        print(f"✅ 全部 {total}/{total} 项通过")
        return 0
    else:
        print(f"❌ {passed}/{total} 项通过，{total - passed} 项失败")
        if fix_hint:
            print("\n💡 通用修复建议：")
            print("  1. 修改了 templates/*.json？检查是否需要同步 cron_mirror 的 _meta.history")
            print("  2. 修改了 cron_mirror.json？跑这个脚本后看是否全过")
            print("  3. 修改了 jobs.json？必须同步 cron_mirror.json 的对应任务 prompt")
            print("  4. 修改了 SKILL.md 任务清单？引用路径必须真实存在（templates/X.json 或 cron_mirror.json#X）")
        return 1


if __name__ == "__main__":
    sys.exit(main())
