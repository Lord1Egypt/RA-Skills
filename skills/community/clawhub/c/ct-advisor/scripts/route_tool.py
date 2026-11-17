#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 入口代码级 ct 技能预判（确定性，无 LLM）

设计目标（2026-08-15，模式 B 编排器前置）：
  在问题进入时（route.py 判定难度之后、转发 Coze 之前），用确定性正则
  预判「是否需要调用 ct 系列技能补充信息」，作为 Coze need_tool 判断的
  **前端高置信预取**信号。

  - 高置信才输出 need_tool（命中明确工具触发词 + 非 vague + 非定义/标准操作）。
  - 漏判由 Coze 的 need_tool 判断兜底（本脚本**不替代** Coze，仅预取）。
  - 参数尽力抽取：test 类用 tool_mapping.json 的 test_hints 推断；百分比
    自动转比例；其余留空，由 handle_need_tool.py 补全或 need_params 追问。

  ⚠️ 与 route.py 的分工：route.py 判「难度」（vague 偏多），本脚本判「是否
  需调 ct 技能」（高置信才触发）。两者都确定性、都无 LLM。

用法：
  python scripts/route_tool.py "用户问题原文"
        → 打印一个标签：none | ct-samplesize | ct-registry | ct-safety | ct-literature
  python scripts/route_tool.py --json "用户问题原文"
        → 打印 {"need_tool": "...", "params": {...}, "confidence": "high"}
  python scripts/route_tool.py --self-test
        → 跑内置预判自测，输出每例命中/预期与准确率
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# 复用 route.py 的入口信号（同目录 import；route.py 的 main 在 __main__ 守卫内，import 安全）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import is_vague, DEF as DEF_ZH  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _load_mapping() -> dict:
    try:
        return json.loads((ROOT / "scripts" / "tool_mapping.json").read_text(encoding="utf-8"))
    except Exception:
        return {"skills": {}}


# ---------------------------------------------------------------------------
# 工具触发词（从 route.py CPLX + tool_mapping.json 提取，确定性、可单测）
#
# 🔴 2026-09-10（第十四轮，用户要求）：由「宽词表」收紧为「强触发词」——
#   起因：关键词误报导致把方法学 / 定义 / 法规判断题误判为「需取数」并弹参追问。
#   用户口径：**只有需求关联非常明确时才调用**兄弟技能；其余一律「先自身作答 + 末尾建议」。
#
#   分层：
#     TOOL_TRIGGERS（强）：唯一指向 → 命中即高置信自动调用。
#       满足其一即可：① 具名数据源（FAERS / ClinicalTrials.gov / NCT 号 / PubMed…）；
#                     ② 具名统计量或高特异性方法（PRR / ROR / EBGM / 去激发 / 病例报告…）；
#                     ③「检索动词 + 注册试验/文献」完整句式（中英各一条）。
#     WEAK_TRIGGERS（弱）：歧义大（信号 / 文献 / 试验 / 安全性 / 设计…）→ **不再自动调用**，
#       仅在答案末尾追加一行软建议（见 suggest_footer），由用户决定是否真要取数。
#
#   一律受「咨询意图护栏」约束（DEF / METHOD / DOC，见下方）：问「是什么 / 怎么做 / 要模板」
#   且无明确取数动作（RETRIEVAL）时，不作取数请求。
# ---------------------------------------------------------------------------

# 强触发词：具名数据源 / 具名统计量 / 高特异性方法 /「检索动词 + 明确对象」句式
TOOL_TRIGGERS = {
    "ct-samplesize": re.compile(
        r"样本量|检验效能|把握度|样本数|估算样本|需要多少例|需要多少受试者|需要多少患者|"
        r"样本量估算|样本量规划|所需例数|需要多少例数|把握度计算|效应量估算|效应量|检出差异|"
        r"sample size|sample-size|how many (?:subjects|patients|participants)|\bpower\b|"
        r"sample size (?:calculation|estimation|planning)|power (?:calculation|analysis)"),
    "ct-registry": re.compile(
        # ① 具名注册库 / 登记号（词边界由正则自带，避免 nct 命中 distinct 之类）
        r"\bnct\s*\d|clinicaltrials\.gov|\bchictr\b|chinadrugtrials|药物临床试验登记|"
        # ② 高特异性检索对象（2026-09-10：裸「在研」改「在研(?!究)」防命中「在研|究者手册」）
        r"在研(?!究)(?:药物|试验|项目|管线|产品)|试验数量|pipeline|competitive[- ]intel|landscape|"
        # ②′ 高特异性格局类同义表述（2026-11-10 P1-2，零歧义才进强触发）
        r"竞争格局|竞品格局|在研格局|试验格局|同适应症在研|在研管线|管线分析|"
        r"registered trials?|"
        # ③ 「检索动词 + 注册/临床试验」完整句式（中文）
        r"(?:检索|查询|查找|搜索|列出|统计|整理|拉一下|查一下|搜一下|找一下|帮我查|帮我找|给我查)"
        r"[^。；;，,]{0,18}?"
        r"(?:注册试验|登记试验|临床试验|试验注册|试验登记|注册临床试验|注册库|登记库|三期|二期)|"
        # ③′ 英文同型句式
        r"(?:find|search|list|retrieve|pull|fetch|give me|show me|how many|get)\b[^.;]{0,40}?"
        r"(?:registered trials?|clinical trials?|trials?\b|landscape|pipeline|competitive[- ]intel)"),
    "ct-safety": re.compile(
        # 具名数据源 / 统计量 / 高特异性方法（因果判定、去激发再激发、具体 irAE）
        r"faers|disproportionality|\bprr\b|\bror\b|\bebgm\b|"
        r"去激发|再激发|dechallenge|rechallenge|因果关系判定|相关性评价|"
        r"不良反应因果关系|ae因果关系|免疫相关不良事件|\birae\b|"
        r"带状疱疹|vzv|水痘-带状疱疹|herpes zoster|"
        r"间质性肺炎|免疫性肺炎|心肌炎|免疫性肝炎|甲状腺炎|垂体炎|免疫性肾炎|"
        r"pneumonitis|myocarditis|nephritis|thyroiditis|hypophysitis|causality assessment"),
    "ct-literature": re.compile(
        # 具名文献源 / 高特异性研究类型 / 「检索动词 + 文献」句式
        r"pubmed|openalex|\bmeta\s*[- ]?分析|meta[- ]analysis|系统综述|系统评价|"
        r"systematic[- ]reviews?|病例报告|个案报告|case reports?|evidence summary|证据摘要|"
        r"文献检索|文献调研|文献梳理|证据检索|已发表证据|相关文献|"
        r"已发表文献|published literature|"
        r"(?:检索|查询|查找|搜索|列出|查|搜|找)[^。；;]{0,12}?(?:文献|论文|综述|证据)|"
        r"(?:find|search|list|retrieve|pull|fetch)\b[^.;]{0,24}?"
        r"(?:literature|papers?|publications?|reviews?)|"
        # 外用 JAK 抑制剂 MUsT / 最大用量 / 系统暴露类问题（具名药物 + 暴露场景）→ 强触发文献核验
        r"(?=.*(?:ruxolitinib|芦可替尼|opzelura|pg-011|普美昔替尼|pumecitinib))"
        r"(?=.*(?:must|最大用量|系统暴露|maximum[- ]use|pk暴露|暴露安全))"),
}

# 弱触发词（2026-09-10 新增）：歧义大，**不自动调用**，仅作答案末尾的软建议。
# 出现「信号 / 文献 / 试验 / 安全性 / 设计」这类泛词时，先由本技能自身作答，
# 再提示「如需真实数据可直接调用 @skill:ct-XXX」——把「要不要取数」的决定权交还用户。
WEAK_TRIGGERS = {
    "ct-registry": re.compile(
        r"临床试验|注册试验|登记试验|注册库|登记库|在研(?!究)|适应症|招募|试验数量|竞品|管线|"
        r"三期|二期|\btrials?\b|\bregistry\b|landscape|pipeline"),
    "ct-safety": re.compile(
        r"不良事件|信号|安全性|药物警戒|pharmacovigilance|safety signal|adverse events?|\bsafety\b"),
    "ct-literature": re.compile(
        r"文献|论文|综述|发表|\bliterature\b|published|systematic review|evidence"),
    "ct-samplesize": re.compile(
        r"样本|效能|把握度|\bpower\b|sample|effect size"),
    # 2026-11-05（B7）：方案评阅意图（方案 + 评阅/审阅/评审/审查/批注/修订/修改意见）。
    #   收得较紧（要求「方案」与「审阅动词」同现），避免把「方案修改后要重新伦理审查吗」
    #   这类合规题误建议到 ct-protocol。仅作软建议，不自动调用。
    "ct-protocol": re.compile(
        r"(?:评阅|审阅|评审|审查|审一下|审下|批注|修订)(?:一下|下)?"
        r"(?:这个|该|此|这份)?(?:试验|研究)?方案"
        r"|(?:试验|研究)?方案(?:的)?(?:评阅|审阅|评审|审查|批注|修订|修改意见|修改建议)"
        r"|protocol\s+(?:review|audit|assessment)|review\s+(?:the\s+)?protocol",
        re.I),
    # 2026-11-11：SAS→R 迁移/移植意图 → 建议本地 ct-sas2r（枢纽）。
    #   动因：用户把 SAS 程序/宏/数据集迁到 R、或要 SAS 等价 R 版（SDTM/ADaM/TLF 分析/递交）时，
    #   ct-sas2r 提供等价层 + 验证 SOP + 隐式业务规则恢复 + 分域编排。ct-sas2r 不自动调用，仅软建议（用户决定切换）。
    "ct-sas2r": re.compile(
        r"SAS\s*→\s*R|SAS to R|把 SAS|SAS 程序|SAS 宏|SAS 数据|SAS 数据集|"
        r"迁(?:移|到|移到 R)|移植|复刻|"
        r"SDTM.{0,6}?R\s*版|ADaM.{0,6}?R\s*版|TLF.{0,6}?R\s*版|"
        r"(?:R\s*版|SAS\s*版).{0,12}?(?:SDTM|ADaM|TLF|分析|递交)|"
        r"port\s+(?:SAS|the\s+SAS)|replicate\s+SAS|migrate\s+SAS|"
        r"R\s+(?:port|version|equivalent)\s+of\s+(?:SAS|the\s+SAS)|"
        r"SAS\s+(?:migration|to\s+R|equivalent\s+in\s+R)",
        re.I),
}

# 文献检索意图优先规则（2026-08-20）：当 ct-literature 与 ct-safety 同时命中时，
# 若问题含强文献检索意图词（已发表/病例报告/综述/检索…），优先文献（定性证据）
# 而非 FAERS 信号统计——README 示例 7 场景（QA 要「检索已发表文献评估支持度」）。
LIT_FIRST = re.compile(
    r"检索|搜索|查找|已发表|病例报告|个案报告|综述|系统综述|meta\s*分析|证据摘要|引用|"
    r"search|published|case reports?|systematic reviews?|\bliterature\b")  # 2026-08-21：英文等价词

# 试验格局意图（registry 主导，2026-08-21）：出现时文献优先规则让位、按字典序（registry 在前）
# 预判——避免英文示例 3（trials+safety+literature 竞品情报）被文献意图抢走 registry 主判。
REG_INTENT = re.compile(
    r"\btrials?\b|landscape|competitive.?intel|在研(?!究)|注册|登记|试验数量|pipeline")

# 方法论询问（仅问注意事项/因素/步骤，无明确数值或计算动作）→ 不预判，
# 避免对"样本量计算要注意什么"这类题突兀地追问效应量参数。明确查询（含动作/数值）
# 即使带"这个/文献/vs"也预判——工具触发词盖过代词歧义。
#
# 🔴 2026-09-10（第十四轮）：补齐**英文**等价词（此前只有中文 → 英文方法学问句直接穿透，
#   实测「…how do I keep the overall type I error rate at 0.05?」被裸词 "trial" 判成检索注册试验）。
#   与云端 `tool_router_node._consultation_intent` 保持同义（两处需同步改）。
METHOD = re.compile(
    r"要注意|注意什么|注意事项|哪些因素|需要考虑|如何做|怎么做|如何考虑|如何评估|如何判断|"
    r"如何保证|怎么看|怎么理解|有什么区别|有何区别|区别是什么|"
    r"\bhow (?:do|does|should|can|to|would)\b|\bwhat should i\b|\bwhich factors\b|"
    r"\bconsiderations?\b|\bdifference between\b|\bwhat(?:'s| is) the difference\b|\bbest practice\b")

# 定义意图（中文复用语 route.DEF；英文补等价词）→ 纯「是什么」不取数。
DEF = re.compile(
    DEF_ZH.pattern + r"|"
    r"\bwhat(?:'s| is| are)\b|\bdefine\b|\bdefinition\b|\bmeaning\b|\bstands? for\b|\babbreviation\b")

# 文档类请求（模板/规范/格式/小结/一览表等）→ 不预判任何工具。
# 2026-08-15 修复：裸词"临床试验/注册"命中《临床试验项目分中心小结》模板类问题，
# 被误判为 ct-registry 检索（输出 "撰写一份完整的药物" 污染）。文档类请求本就不该触发
# 数据检索/计算类工具，统一拦截；真实检索意图（在研/三期/招募等）仍正常预判。
DOC = re.compile(
    r"模板|撰写规范|格式|小结|总结报告|填写|一览表|doc\s*文件|提取的文本|审批表|签章|存档|"
    r"\btemplate\b|\bformat\b|\bchecklist\b|\bwrite (?:a|the|up)\b|\bdraft (?:a|the)\b|\bfill (?:in|out)\b")

# 明确取数动作（2026-09-10）：命中 → 咨询意图护栏让位（用户是在「要数据」而非「问怎么做」）。
# 与云端 `_RETRIEVAL_INTENT` 同义。
RETRIEVAL = re.compile(
    r"检索|搜索|查找|查询|列出|统计|拉一下|查一下|搜一下|找一下|列一下|帮我查|帮我找|给我查|"
    r"有哪些|哪几个|数量|多少家|"
    r"\bfind\b|\bsearch\b|\blist\b|\bretrieve\b|\bpull\b|\bfetch\b|\bgive me\b|\bshow me\b|"
    r"\bhow many\b|\bget (?:the|me)\b")

# ── 数据运营类护栏（2026-11-11 Fix B 配套，mirror 云端 tool_router_node._DATA_OPS）──
# 裸动词「查」此前命中「核*查*/稽*查*」+「临床试验」→ EDC/数据核查/稽查误判 ct-registry；
# 即便含合法检索动词 + 临床试验，EDC/数据运营也非注册库检索，一律原生作答。
_DATA_OPS = re.compile(
    r"(?<![A-Za-z])edc(?![A-Za-z])|电子数据采集|数据核查|数据管理|数据库锁|数据清理|数据质量|"
    r"源数据核查|(?<![A-Za-z])sdv(?![A-Za-z])|病例报告表|(?<![A-Za-z])crf(?![A-Za-z])|"
    r"中央随机|(?<![A-Za-z])iwrs(?![A-Za-z])|随机化系统|"
    r"稽查|监查|稽查轨迹|数据录入|双录入|(?<![A-Za-z])eclinical(?![A-Za-z])|临床数据库|"
    r"质疑\s*\(?数据\)?|数据质疑",
    re.IGNORECASE)

# 否定 / 范围词（2026-11-10 P0-3）：用于「弱触发词紧邻否定词」时剔除该弱建议。
# 仅作词边界判定，不做语义范围解析——精确性来自「否定词必须紧邻工具自身触发词」的窗口约束。
_NEGATION = re.compile(
    r"除了|除外|不用|无需|不必|忽略|排除|不要|别|除非|"
    r"except|excluding|excluded|without|ignore|other than")


# ---------------------------------------------------------------------------
# 咨询深度 / 执行意图（2026-11-09）
#
# 契约单一真相源：config/intent_contract.json。云端
# adapters/coze/src/graphs/nodes/tool_router_node.py 持有同名同值内嵌副本，
# scripts/check_route_drift.py 用 AST 断言 JSON + 本地 + 云端三份逐字一致。
# 🔴 改词表必须三处同改，否则会出现「本地不预判、云端仍委托」的不一致。
#
# 背景：旧护栏只认「是什么 / 怎么做 / 要模板」，技术细节问答
# （α 消耗函数、95%CI 解释、estimand 五属性、字段语义）会被误派给
# 计算/检索型兄弟技能；RETRIEVAL 里的裸词「统计」还会误让位。
# ---------------------------------------------------------------------------
_INTENT_CONSULT_DEPTH = r"原理|机制|为什么|为何|依据|理论上|如何确定|如何界定|如何解释|如何理解|如何影响|有何影响|影响是什么|怎么解释|怎么理解|解释一下|解释下|说明一下|怎么定|如何定|先说明|先解释|取决于|受什么影响|影响因素|关系是什么|有何关系|含义|涵义|前提假设|适用条件|适用边界|局限性|优缺点|选择依据|怎么选|如何选|为什么用|为何要|代表什么|说明什么|反映什么|\bwhy\b|\brationale\b|\bunderlying\b|\bprinciple\b|\bmechanism\b|\bassumption\b|\bpremise\b|\binterpret(?:ation|ed)?\b|\bdepends? on\b|\btrade-?off\b|\bapplicability\b|\blimitation\b|\bderived? from\b|\bchoice of\b|\bwhy use\b|\bsignificance of\b"
_INTENT_EXEC = r"(?:帮我|请)?(?:算一下|算下|计算一下|帮我算|求|跑一下|跑个|导出|下载|生成|检索|查询|查找|列出|拉一下|查一下|搜一下|找一下)(?:样本量|例数|把握度|报告|结果|试验|文献|信号|数据|指标)?|\b(?:compute|calculate|run|fetch|export|pull|retrieve|list|search)\b"
_INTENT_RETRIEVAL = r"检索|搜索|查找|查询|列出|拉一下|查一下|搜一下|找一下|列一下|帮我查|帮我找|给我查|有哪些|哪几个|数量|多少家|\bfind\b|\bsearch\b|\blist\b|\bretrieve\b|\bpull\b|\bfetch\b|\bgive me\b|\bshow me\b|\bhow many\b|\bget (?:the|me)\b"

_CONSULT_DEPTH_RE = re.compile(_INTENT_CONSULT_DEPTH)
_EXEC_INTENT_RE = re.compile(_INTENT_EXEC)
_INTENT_RETRIEVAL_RE = re.compile(_INTENT_RETRIEVAL)
_INTENT_OFF = {"0", "false", "no", "off"}


def _intent_depth_enabled() -> bool:
    """本地应急开关：CT_ADVISOR_INTENT_DEPTH=0 回到旧护栏（不含 CONSULT_DEPTH）。"""
    return os.environ.get("CT_ADVISOR_INTENT_DEPTH", "").strip().lower() \
        not in _INTENT_OFF


def _intent_flags(q: str) -> tuple:
    """双标志意图判定（纯代码）：返回 (consult, exec)。

    consult：原理 / 机制 / 为什么 / 依据 / 定义 / 方法论 / 文档类询问
             （CONSULT_DEPTH 部分受 CT_ADVISOR_INTENT_DEPTH 开关约束）。
    exec：显式执行 / 取数动词（帮我算 / 检索 / 查 / compute / find …）。

    两者可同真（混合意图）——旧 _intent_verdict 会把混合整体判 consult 再降级，
    现由 predict 分别处理：exec 照常下发 need_tool，consult 由 Coze 端点答原理，
    两者经 orchestrate 合并共存（2026-11-10 P0-1）。
    """
    ql = (q or "").lower()
    consult = False
    if _intent_depth_enabled():
        consult = bool(_CONSULT_DEPTH_RE.search(ql))
    consult = consult or bool(METHOD.search(ql) or DEF.search(ql) or DOC.search(ql))
    exec_ = bool(_EXEC_INTENT_RE.search(ql) or _INTENT_RETRIEVAL_RE.search(ql))
    return consult, exec_


def _rank_hits(hits: list, q: str) -> list:
    """多强命中排序（2026-11-10 P0-2，纯代码 / 确定性）。

    1) 保留既有领域启发式 LIT_FIRST / REG_INTENT 的硬优先级（与旧行为逐字一致）；
    2) 当上述硬约束未触发且候选 >1 时，按证据加权（带真实参数 > 近检索动词）
       排序，替代原字典序硬选；同分回落字典序。
    """
    ordered = list(hits)
    # —— 1) 文献优先规则（README 示例 7）：同时含 literature + safety 且文献意图强、
    #        无明确试验格局意图时，剔除 safety 并把 literature 置顶 ——
    if ("ct-literature" in ordered and "ct-safety" in ordered
            and LIT_FIRST.search(q) and not REG_INTENT.search(q)):
        ordered = [t for t in ordered if t != "ct-safety"]
        ordered.insert(0, "ct-literature")
    # —— 2) 证据加权（仅当无 LIT_FIRST 硬约束且多候选）——
    lit_special = ("ct-literature" in hits and "ct-safety" in hits
                   and LIT_FIRST.search(q))
    if len(ordered) > 1 and not lit_special:
        def _score(t):
            s = 0
            p = _extract_params(t, q)
            # 仅以「可靠参数」加权：数值 p1/p2 或中文实体（英文实体抽取噪声大，不计入），
            # 避免长英文句里的 "protocol"/"introduction" 之类被误当真实参数、反向压过真正执行动作。
            if p.get("p1") is not None or p.get("p2") is not None:
                s += 2
            cond = p.get("cond") or p.get("drug") or ""
            if cond and _has_cjk(cond):
                s += 2
            if RETRIEVAL.search(q) or _EXEC_INTENT_RE.search(q):
                s += 1
            return s
        ordered.sort(key=lambda t: -_score(t))
    return ordered


def _negation_suppresses(q: str, rx) -> bool:
    """P0-3：工具的弱触发词是否紧邻否定词（如「除了文献」）。

    仅当该工具自身的弱触发正则命中位置前 ~6 字符内出现否定词才剔除，
    避免「除了文献，查安全性信号」误删安全性（安全性未紧邻否定词）。
    """
    m = rx.search(q)
    if not m:
        return False
    window = q[max(0, m.start() - 6):m.start()]
    return bool(_NEGATION.search(window))


def _candidate_evidence(tools, q: str) -> list:
    """P1-1：列出各候选工具的证据标签（has_params / retrieval_verb），供云端兜底参考。"""
    out = []
    for t in (tools or []):
        ev = []
        if _extract_params(t, q):
            ev.append("has_params")
        if RETRIEVAL.search(q) or _EXEC_INTENT_RE.search(q):
            ev.append("retrieval_verb")
        out.append({"tool": t, "evidence": ev})
    return out


# 英文抽取停用词（避免把「registered trials for…」这类结构词当实体）
_EN_STOP = {
    "the", "a", "an", "our", "one", "registered", "trials", "trial",
    "case", "reports", "report", "published", "literature", "safety",
    "signal", "signals", "full", "picture", "help", "introduction",
}


def _extract_english_entity(q: str) -> str:
    """尽力抽取英文药名/靶点实体（route_tool 预取参数兜底）。

    2026-08-21：README 示例 2/3/7/8 实测——英文提示词在中文 SUFFIX 逻辑下抽不到
    cond/topic/drug，预取退化 need_params（只给检索指引、不出格局）。此处补英文
    抽取：已知靶点 > 「for X」> 「X in/of/with Y」。仅英文问题生效（CJK 占比守卫），
    中文问题不受影响。抽不到返回空串（由 handle_need_tool 追问）。
    """
    q = q or ""
    if len(re.findall(r"[\u4e00-\u9fff]", q)) >= max(1, len(q) * 0.15):
        return ""  # 中文主导，跳过英文抽取
    # 1) 已知靶点/药物形态（PD-1、GLP-1 RA 等）
    KNOWN = re.compile(
        r"\b(PD-1|PD-L1|CTLA-4|GLP-1(?:\s*RA)?|HER2|EGFR|ALK|ROS1|BRCA1|BRCA2|VEGF|CD20)\b",
        re.I)
    m = KNOWN.search(q)
    if m:
        return m.group(1).upper()
    # 2) 「for X」捕获（Pull the registered trials for semaglutide → semaglutide；
    #    介词/逗号/结尾处截断，避免吞入后续词）
    m = re.search(
        r"\bfor\s+((?:[A-Za-z][A-Za-z0-9\-]*\s+){0,2}[A-Za-z][A-Za-z0-9\-]*)"
        r"(?=\s+(?:in|among|of|with)\b|\s*[,.;]|$)", q)
    if m:
        cand = re.sub(r"^(?:the|a|an)\s+", "", m.group(1).strip(), flags=re.I)
        if cand and cand.lower() not in _EN_STOP:
            return cand
    # 3) 「X in/among/of/with Y」捕获（semaglutide in T2D → semaglutide）
    m = re.search(
        r"\b([A-Za-z][A-Za-z0-9\-]*(?:\s+[A-Za-z][A-Za-z0-9\-]+){0,2})\s+(?:in|among|of|with)\s+",
        q)
    if m:
        cand = re.sub(r"^(?:the|a|an)\s+", "", m.group(1).strip(), flags=re.I)
        if cand and cand.lower() not in _EN_STOP:
            return cand
    return ""


def _extract_params(tool: str, q: str) -> dict:
    """尽力抽取执行卡参数；抽不到的留空（handle_need_tool 补全/追问）。"""
    params: dict = {}
    mapping = _load_mapping()
    cfg = mapping.get("skills", {}).get(tool, {})

    if tool == "ct-samplesize":
        # test 类：复用 tool_mapping 的 test_hints（单一数据源，避免漂移）
        hints = cfg.get("test_hints", {})
        for pattern, value in hints.items():
            if any(kw in q for kw in pattern.split("|")):
                params["test"] = value
                break
        # 百分比 → 比例：ORR 30% vs 45% → p1=0.3, p2=0.45
        m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:vs|对|比|～|~)\s*(\d+(?:\.\d+)?)\s*%", q, re.I)
        if m:
            try:
                params["p1"] = round(float(m.group(1)) / 100, 4)
                params["p2"] = round(float(m.group(2)) / 100, 4)
            except ValueError:
                pass
    elif tool == "ct-registry":
        # 抽取检索主词 cond（覆盖 药/抑制剂/单抗/药物/化合物/制剂/类 等形态）。
        # 取 drug 后缀前紧邻的实体、并裁剪前导动词（检索/查/针对…），避免把动词当检索词。
        # ⚠️ 键必须是 tool_mapping.json 的 required_params 值「cond」（非 drug）：
        #   抽成 drug 会与 required_params 对不上 → handle_need_tool 仍判 need_params，
        #   前端预判对 registry 形同虚设（已踩过 REKEY 坑，详见 v0.9.68 修复记录）。
        SUFFIX = r"(?:抑制剂|单抗|药物|药|化合物|制剂|类|肽|抗体)"
        m = re.search(SUFFIX, q)
        if m:
            pre = q[: m.start()].strip()
            # 2026-08-20：剥离前导口语动词/请求短语（拉一下/帮我查…），
            # 避免连续中文合成一个 run 时把"拉一下"当 cond 的一部分。
            LEAD = re.compile(
                r"^(?:请|麻烦)?(?:(?:帮我|给我|帮|拉一下|查一下|搜一下|找一下|看一下|"
                r"检索|查询|查|看|拉|搜|找|了解|关于|针对|整理|列一下|列出|给我列)\s*)+")
            pre = LEAD.sub("", pre)
            runs = re.findall(r"[\u4e00-\u9fa5A-Za-z0-9]+(?:[-][\u4e00-\u9fa5A-Za-z0-9]+)*", pre)
            BLACK = {"检索", "查询", "查", "看", "关于", "针对", "治疗", "了解",
                     "找", "这个", "该", "那", "适应症", "在研", "试验", "有", "哪些",
                     "撰写", "完整", "一份", "请", "根据", "以下", "模板",
                     "提取", "文本", "内容", "doc", "文件"}
            ent = ""
            for r in reversed(runs):
                if r not in BLACK:
                    ent = r
                    break
            if ent:
                params["cond"] = ent + m.group(0)
        if not params.get("cond"):
            # 2026-08-21：英文药名/靶点兜底（README 示例 2/3 实测根因：
            # 英文问题无中文 SUFFIX → m=None 整块跳过；此处独立于 if m 块执行）
            en = _extract_english_entity(q)
            if en:
                params["cond"] = en
    elif tool == "ct-literature":
        # 2026-08-21：英文 topic 尽力抽取（示例 3/8）；中文仍留空由 need_params 追问
        en = _extract_english_entity(q)
        if en:
            params["topic"] = en
    elif tool == "ct-safety":
        # 2026-08-21：英文 drug 尽力抽取（示例 7）；中文仍留空由 need_params 追问
        en = _extract_english_entity(q)
        if en:
            params["drug"] = en
    return params


# ---------------------------------------------------------------------------
# 中文混合问句实体抽取（2026-11-09，仅多技能路径使用）
#
# 🔴 刻意不改单技能 `_extract_params`：那是 route_tool --self-test 37/37
#    词表回归的稳定区。中文增强只作用于新增的 extract_params_for_tools，
#    因此纯方法论 / 定义 / 咨询护栏等既有断言一条都不受影响。
# ---------------------------------------------------------------------------
_CJK_DISEASE = re.compile(
    r"[\u4e00-\u9fa5A-Za-z0-9\-]{1,14}(?:癌|瘤|症|病|综合征|适应症)")
_CJK_DRUG = re.compile(
    r"[\u4e00-\u9fa5A-Za-z0-9\-]{1,14}(?:抑制剂|单抗|抗体|肽|类药物|类似物)")
_LATIN = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*\b")
_LATIN_DISEASE = {"NSCLC", "SCLC", "HCC", "CRC", "T2DM", "COPD", "AML", "CLL"}
_ENTITY_BLACK = {
    "FAERS", "PRR", "ROR", "EBGM", "PubMed", "ORR", "PFS", "OS", "NCT", "CDE",
    "GCP", "ICH", "AE", "SAE", "IB", "CSR", "SAP", "ITT", "CI", "HR", "FDA",
    "EMA", "NMPA", "WHO", "CT", "RA", "MedDRA", "PT", "XX", "III", "II", "I",
    "Pull", "Give", "Find", "Search", "Compute", "Check", "How", "What",
}


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= c <= "\u9fff" for c in (text or ""))


def _extract_cjk_mixed_entities(q: str) -> dict:
    """从中文/中英混合问句抽适应症、靶点与文献主题（尽力而为，不编造）。

    返回 {condition, target, drug_cjk, topic}。仅用于给 ct-registry 的
    `cond` 与 ct-literature 的 `topic` 兜底 —— 两者接受中文检索词。
    ct-safety 的 `drug` **绝不**填中文：openFDA 只认英文通用名，
    硬填会导致零命中，属有害参数；改为在副卡给出面向用户的提示。
    """
    q = q or ""
    disease = ""
    m = _CJK_DISEASE.search(q)
    if m:
        disease = m.group(0)
    else:
        for tok in _LATIN.findall(q):
            if tok.upper() in _LATIN_DISEASE:
                disease = tok
                break
    m2 = _CJK_DRUG.search(q)
    drug_cjk = m2.group(0) if m2 else ""
    targets = [t for t in _LATIN.findall(q)
               if t.upper() not in _ENTITY_BLACK
               and t.upper() not in _LATIN_DISEASE
               and len(t) >= 2]
    target = targets[0] if targets else ""
    topic = " ".join(x for x in (target or drug_cjk, disease) if x).strip()
    return {"condition": disease or target, "target": target,
            "drug_cjk": drug_cjk, "topic": topic}


def extract_params_for_tools(tools, q: str) -> dict:
    """多技能命中时，为每个技能分别抽参数并合并（2026-11-09，纯代码 / 确定性）。

    此前主流程只给主判技能抽参数，混合问题的副卡片全是「需补齐」。
    本函数对每个命中技能各调一次 `_extract_params`；键名可能重叠
    （如 `drug` 同属 ct-registry / ct-safety），setdefault 保留先出现的值。
    下游 `_handoff_result` / `_build_deferred` 各自按技能白名单过滤，
    因此合并**不会**造成串参。未知技能返回空字典，不抛异常。

    中文/中英混合问句额外用 `_extract_cjk_mixed_entities` 给 registry 的
    `cond` 与 literature 的 `topic` 兜底；英文问句完全走原逻辑，不受影响。
    """
    merged = {}
    for t in tools or []:
        for k, v in (_extract_params(t, q) or {}).items():
            if v not in (None, ""):
                merged.setdefault(k, v)
    if _has_cjk(q):
        ent = _extract_cjk_mixed_entities(q)
        if "ct-registry" in (tools or []) and ent.get("condition"):
            merged.setdefault("cond", ent["condition"])
        if "ct-literature" in (tools or []) and ent.get("topic"):
            merged.setdefault("topic", ent["topic"])
    return merged


# 2026-11-10（安全提示）：复杂混合调用（多强命中）时，向用户给出「拆分问题」的安全提示。
# 纯代码确定性生成，无 LLM。多工具信号 = len(need_tools) > 1（由 predict 判定）。
def complexity_hint_text(tools: list, lang: str = "zh-CN") -> str:
    """复杂混合调用的安全提示文本（纯代码，无 LLM）。tools 为全部涉及的兄弟技能列表。"""
    tools = list(tools or [])
    if len(tools) <= 1:
        return ""
    names = "、".join(tools) if lang == "zh-CN" else ", ".join(tools)
    if lang == "zh-CN":
        return ("\n\n---\n\n⚠️ **安全提示**：本次问题涉及多个兄弟技能（%s），属于复杂混合调用。"
                "建议将其拆分为几个独立问题分别询问，以获得更准确、可核验的结果。"
                "若调用后**长时间无反馈**，请主动终止当前请求，将问题拆分后重新提问。" % names)
    return ("\n\n---\n\n⚠️ **Safety note**: this question spans multiple sibling skills (%s); "
            "it is a complex combined call. Consider splitting it into a few separate questions "
            "asked one at a time for more accurate, verifiable results. If there is **no response "
            "for a long time**, please abort the current request and re-ask by splitting the "
            "question." % names)


# 提示正文的固定起始短语：出口层幂等去重的判据（措辞与上面唯一真相源同步）。
COMPLEXITY_HINT_MARK_ZH = "⚠️ **安全提示**"
COMPLEXITY_HINT_MARK_EN = "⚠️ **Safety note**"
_COMPLEXITY_HINT_SEP = "\n\n---\n\n"


def has_complexity_hint(text: str, at_start: bool = False) -> bool:
    """答案正文是否已含复杂混合调用安全提示（entry / refine_answer 幂等去重共用）。

    at_start=True 只判「答案是否已以提示开头」——出口层用这个精确判据：既避免
    --card-inline 子进程已前置时重复添加，又不会因答案正文里偶然提到同样措辞
    而漏加（漏加会让提示回到「用户看不到」的老问题）。
    at_start=False 为全文匹配，供测试 / 内容检查使用。
    """
    s = (text or "").lstrip() if at_start else (text or "")
    if at_start:
        return (s.startswith(COMPLEXITY_HINT_MARK_ZH)
                or s.startswith(COMPLEXITY_HINT_MARK_EN))
    return COMPLEXITY_HINT_MARK_ZH in s or COMPLEXITY_HINT_MARK_EN in s


# 出口去重：剥掉答案正文里任何「同款安全提示段」及其紧邻的分隔线。提示是单行
# 文本，中英两版共用固定起始短语（两端措辞逐字一致，见 complexity_hint_text）。
# 覆盖三种来源：云端字段被消费端渲染到末尾、--card-inline 子进程已前置、以及
# 前后两份同现。剥净后由出口统一前置一次，用户全文恰好看到一次且位于最前。
_HINT_STRIP_RE = re.compile(
    r"(?:[ \t]*\n\n---\n\n)?⚠️ \*\*(?:安全提示|Safety note)\*\*[^\n]*(?:\n\n---\n\n)?"
)


def strip_complexity_hint(text: str) -> str:
    """剥净答案正文里的同款安全提示段（出口层去重，纯代码、无 LLM）。

    未含提示时原样返回（仅去首尾换行，与 ``entry._answer_body`` 归一一致）。
    配合 ``complexity_hint_prefix`` 使用：先剥净、再前置，保证幂等且位置唯一。
    v1.63 起云端只回布尔标记，本函数保留用于兼容 v1.62 旧端点 / 历史缓存答案。
    """
    return _HINT_STRIP_RE.sub("", text or "").strip("\n")


def _complexity_hint_body(tools: list, lang: str) -> str:
    """纯提示正文（无分隔线）：剥掉 complexity_hint_text 的「末尾追加式」前导。"""
    hint = complexity_hint_text(tools, lang)
    if not hint:
        return ""
    return (hint[len(_COMPLEXITY_HINT_SEP):]
            if hint.startswith(_COMPLEXITY_HINT_SEP) else hint).strip()


def complexity_hint_prefix(tools: list, lang: str = "zh-CN",
                           with_separator: bool = True) -> str:
    """「答案最前 / 调用之前」版安全提示，供出口层共用（单一真相源）。

    2026-11-10 修复：原 complexity_hint_text 以 ``\\n\\n---\\n\\n`` 起头，是「末尾
    追加」时代的格式；直接前置会在答案最前留下无意义的分隔线。更关键的是，提示
    只在缝合答案末尾出现时，一旦混合调用在扣子端卡死 / 超时回落，``_merge_answer``
    根本不执行，用户就永远看不到「长时间无反馈请拆分重问」的引导。

    改为出口层前置后：无论 Coze 成功慢回、超时回落、未授权还是独立 CLI，提示都随
    答案最前一并返回；并另在**调用之前**用 with_separator=False 写 stderr 预警。

    with_separator=True  → 正文 + 分隔线（可直接 + 答案）
    with_separator=False → 纯正文（stderr 实时预警用）
    """
    body = _complexity_hint_body(tools, lang)
    if not body:
        return ""
    return body + _COMPLEXITY_HINT_SEP if with_separator else body


def _none(suggest=None, confidence=None, ambiguity="none", candidates=None) -> dict:
    """统一的「不调用」返回（可携带软建议 + P1-1 分级信号）。"""
    return {"need_tool": None, "need_tools": [], "suggest_tools": list(suggest or []),
            "params": {}, "confidence": confidence, "ambiguity": ambiguity,
            "candidates": list(candidates or [])}


def predict(q: str) -> dict:
    """返回 {'need_tool', 'need_tools', 'suggest_tools', 'params', 'confidence',
    'ambiguity', 'candidates'}。

    🔴 2026-09-10（第十四轮，用户要求）三层语义：
      - need_tool 非空   → **强命中**（唯一指向）→ 自动调用该技能取真实数据；
      - need_tool 空 + suggest_tools 非空 → **弱命中 / 咨询意图** → 不调用，先自身作答，
        答案末尾追加一行软建议（suggest_footer），把「要不要取数 / 安装」交回用户；
      - 两者皆空         → 与兄弟技能无关，直接自身作答。

    高置信约束（保留）：强命中 AND 非纯代词短句 AND 非纯定义 / 方法论 / 文档类询问
    （咨询意图护栏，且无明确取数动作）。

    2026-11-10（本地链路优化，纯代码 / 无 LLM）：
      - P0-1 混合意图拆分：咨询信号词 + 执行动词同现时**不再整体降级**——仍下发执行工具
        的 need_tool（handoff），原理部分由 Coze 端点自身作答，两者经 orchestrate 合并共存。
      - P0-2 证据加权多工具排序：多强命中按「带真实参数 > 近检索动词」加权，替代字典序硬选；
        LIT_FIRST / REG_INTENT 领域启发式仍优先。
      - P0-3 否定 / 范围过滤：工具的弱触发词紧邻否定词（如「除了文献」）时剔除该弱建议。
      - P1-1 置信 / 歧义分级：所有分支均带 confidence / ambiguity / candidates，
        供 orchestrate 透传 query_meta 辅助云端兜底。
    """
    q = (q or "").strip()
    if not q:
        return _none()
    # 数据运营类护栏（2026-11-11 Fix B 配套，mirror 云端 tool_router_node._match_tool）：
    # EDC/数据核查/稽查/监查/CRF/SDV/IWRS 等属临床试验运营/方法学，非「检索注册库」意图，
    # 一律原生作答（不委托），兜底防裸动词误路由 ct-registry。
    if _DATA_OPS.search(q):
        return _none()
    ql = q.lower()
    strong = [t for t, rx in TOOL_TRIGGERS.items() if rx.search(ql)]
    weak = [t for t, rx in WEAK_TRIGGERS.items() if rx.search(ql)]

    # P0-3：否定 / 范围过滤——仅剔除「弱触发词紧邻否定词」的弱候选
    # （如「除了文献之外」→ 不软建议文献；「除了文献，查安全性信号」→ 文献剔除、安全性保留）
    weak = [t for t in weak if not _negation_suppresses(q, WEAK_TRIGGERS[t])]

    consult, exec_ = _intent_flags(q)

    # 咨询意图护栏：问「是什么 / 怎么做 / 要模板」且**无明确取数动作** → 不作取数请求。
    # 明确取数动作（RETRIEVAL / EXEC，如「检索…」「帮我查…」「帮我算…」）时护栏让位——
    # P0-1：咨询 + 执行同现**不再整体降级**，执行部分照常下发 need_tool，原理由 Coze 答。
    # 🔴 2026-09-10（第十四轮·补丁，用户要求）：护栏命中时**只保留强命中**作为建议，
    #   不再回落弱词表。否则裸弱词（ct-registry 的 `\btrials?\b`）会给纯定义 / 方法论题
    #   附一条题不对路的「可调用 ct-registry」提示——即已消灭的误报换了位置继续出现。
    #   实测回归：「A confirmatory Phase III trial plans one interim analysis — how do I
    #   keep the overall type I error rate at 0.05?」「…ITT and mITT…trial?」此前均建议
    #   ct-registry，现应为 []。与云端 `_suggest_tools(..., strong_only=True)` 同义。
    #
    #   2026-11-05（B7）例外：方案评阅类问题即使命中咨询护栏，也保留 ct-protocol 软建议——
    #   「如何评审这个方案」正是该切到结构化评审框架的场景（题是对路的），不应被护栏清空。
    if consult and not exec_:
        extra_review = [t for t in weak if t == "ct-protocol"]
        return _none(strong + extra_review)

    # 纯代词短句且无强命中 → 不预判（交给 vague 流程或 Coze）；弱命中保留为软建议
    if is_vague(q) and not strong:
        return _none(weak)

    if strong:
        # P0-2：证据加权排序（LIT_FIRST / REG_INTENT 领域启发式已在 _rank_hits 内优先）
        raw_hits = list(strong)
        hits = _rank_hits(raw_hits, q)
        tool = hits[0]
        params = _extract_params(tool, q)
        ambiguity = "multi" if len(raw_hits) > 1 else "single"
        # 2026-11-10（安全提示）：多强命中 = 复杂混合调用 → 标记 split_advice 并生成提示文本，
        # 供本地渲染层（refine_answer._merge_answer）注入答案，提示用户拆分问题。
        split_advice = len(raw_hits) > 1
        hint = complexity_hint_text(raw_hits, "zh-CN") if split_advice else None
        return {"need_tool": tool, "need_tools": raw_hits, "suggest_tools": [],
                "params": params, "confidence": "high", "ambiguity": ambiguity,
                "candidates": _candidate_evidence(raw_hits, q),
                "split_advice": split_advice, "complexity_hint": hint}

    # 弱命中 → 不调用；答案末尾软建议
    ambiguity = "single" if weak else "none"
    conf = "medium" if weak else "low"
    return _none(weak, confidence=conf, ambiguity=ambiguity,
                 candidates=_candidate_evidence(weak, q))


def predict_tool(q: str):
    """兼容接口：仅返回 need_tool 字符串或 None（供编排器快速判定）。"""
    return predict(q).get("need_tool")


# ---------------------------------------------------------------------------
# 软建议页脚（2026-09-10 第十四轮，用户要求）
#
# 姿态：**先自身作答，末尾再建议**。当问题与兄弟技能沾边、但「需求关联不够明确」
# （弱命中）或属咨询意图（定义 / 方法论 / 文档）时，不再阻断答案去要参数或要安装，
# 而是在答案**最后**追加一行建议，把「是否安装 / 是否调用」交给用户决定。
#
# 文案随提问语言切换；工具名保持 id 原文。供 orchestrate.build_output /
# refine_answer --ship 复用（单一数据源，避免两处文案漂移）。
#
# 2026-09-29（B 项）：suggest_footer 支持动态注册表驱动。
#   若 sibling_registry.json 存在，则从中读取技能摘要和能力描述，
#   仅对**已安装**的技能生成建议；未安装技能不主动推荐（避免建议空壳）。
# 2026-11-09：客户端已可直接调用本机注册技能，文案由「可安装 / 调用」统一改为
#   可直接执行的 `@skill:<slug>` 形态，与 brief_contract.json 的 suggest_text 对齐；
#   _TOOL_DESC 扩到 B 档与未上架 A 档。注册表的作用从「避免建议空壳」变为
#   「确认本机可调用」，语义不变但话术不再暗示要安装。
# ---------------------------------------------------------------------------

_TOOL_DESC = {
    "ct-registry": {"zh": "试验注册库检索（试验格局 / 分期 / 申办方 / 时间线）",
                    "en": "trial-registry search (landscape / phase / sponsor / timeline)"},
    "ct-safety": {"zh": "FAERS 药物警戒信号（PRR / ROR / EBGM + 95%CI）",
                  "en": "FAERS pharmacovigilance signals (PRR / ROR / EBGM + 95% CI)"},
    "ct-literature": {"zh": "学术文献检索（含临床指南 / 病例报告 / 综述 / 证据摘要）",
                      "en": "literature search (guidelines / case reports / reviews / evidence)"},
    "ct-samplesize": {"zh": "样本量 / 检验效能计算",
                      "en": "sample size / power calculation"},
    # 2026-11-05（B7）：方案评阅意图 → 建议本地 ct-protocol。
    #   动因：用户反馈 ct-advisor 对「方案评阅 / 修改意见」类问题「输出笼统」，
    #   而 ct-protocol 有结构化评审框架（U1–U12 / D1–D9 / 批注版输出）。
    #   ct-protocol 为 B 档本地技能（不在 tool_mapping 自动执行表），故只作**软建议**，
    #   不自动调用——把「是否切换」决定权交回用户（与 WEAK_TRIGGERS 姿态一致）。
    "ct-protocol": {"zh": "方案深度审阅（多角色评审 / 立论与逻辑一致性 / 修订风险 / 批注版输出）",
                    "en": "in-depth protocol review (multi-role review / rationale & logic consistency / revision risk / annotated output)"},
    # 2026-11-11：SAS→R 迁移意图 → 建议本地 ct-sas2r（枢纽，不自动调用，仅软建议）。
    "ct-sas2r": {"zh": "SAS→R 临床试验统计移植枢纽（等价层 + 验证 + 隐式规则恢复 + 分域编排）",
                 "en": "SAS→R clinical-trial stats migration hub (equivalence + validation + implicit-rule recovery + domain orchestration)"},
    # 2026-11-09：客户端已可直接调用本机注册的全部 ct-* 技能，软建议表同步扩到
    # B 档与未上架 A 档。suggest_footer 只对 predict() 命中的工具出建议，扩表不会
    # 凭空增加建议条数；仅让原本会被 `_TOOL_DESC` 过滤掉的建议能正常渲染。
    "ct-csr": {"zh": "ICH E3 / NMPA 双模板 CSR 撰写", "en": "ICH E3 / NMPA CSR authoring"},
    "ct-sdtm": {"zh": "CDISC SDTM 映射与合规校验", "en": "CDISC SDTM mapping & compliance"},
    "ct-adam": {"zh": "ADaM 数据集派生", "en": "ADaM dataset derivation"},
    "ct-analysis": {"zh": "试验内统计分析（ARD）", "en": "within-trial statistical analysis (ARD)"},
    "ct-tlf": {"zh": "Tables / Listings / Figures 产出", "en": "Tables / Listings / Figures"},
    "ct-statrev": {"zh": "独立统计审阅（人群 / 终点复现）", "en": "independent statistical review"},
    "ct-datacheck": {"zh": "数据质控与 CDISC 规则检查", "en": "data QC & CDISC rule checks"},
    "ct-eligibility": {"zh": "受试者↔方案入组匹配", "en": "subject-to-protocol eligibility matching"},
    "ct-ecrf": {"zh": "eCRF 设计规格生成", "en": "eCRF design specification"},
    "ct-submission": {"zh": "CTD / eCTD 申报包组装", "en": "CTD / eCTD submission packaging"},
    "ct-congress": {"zh": "会议摘要疗效 / 安全性结构化提取", "en": "congress abstract efficacy / safety extraction"},
    "ct-pipeline": {"zh": "公开情报 / 竞品监测编排", "en": "public-intel / competitive monitoring pipeline"},
    "ct-synthdata": {"zh": "合成 CDISC 测试数据集", "en": "synthetic CDISC test datasets"},
    "meta-analysis": {"zh": "医学 Meta 分析与网状 Meta", "en": "medical meta-analysis / NMA"},
}


def _load_sibling_registry() -> dict:
    """加载 sibling_registry.json（若存在且新鲜）。

    调用时惰性检查：若注册表过期（>24h 或技能数量变化），自动刷新。
    刷新开销 ~50ms（20 技能目录 × frontmatter 解析），可接受。
    """
    try:
        # 延迟导入（避免循环：discover_siblings 依赖 route_tool 的 ROOT 常量）
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from discover_siblings import ensure_fresh
        return ensure_fresh(max_age_hours=24)
    except Exception:
        pass
    return {}


def _get_installed_skills(registry: dict) -> set:
    """从注册表获取已安装的技能名集合。"""
    skills = registry.get("skills", {})
    return {name for name, info in skills.items() if info.get("installed", False)}


def _build_dynamic_desc(tool: str, registry: dict, lang: str = "zh-CN") -> str | None:
    """从注册表构建技能描述（优先使用，fallback 到 _TOOL_DESC）。"""
    skills = registry.get("skills", {})
    info = skills.get(tool)
    if not info or not info.get("installed", False):
        return None
    summary = info.get("summary", "")
    # summary 格式可能为 "中文 / English" 或纯中文或纯英文
    parts = summary.split(" / ")
    if lang == "zh-CN":
        desc = parts[0] if parts else summary
    else:
        desc = parts[1] if len(parts) > 1 else summary
    # 智能截断（不超过 60 字符，不在词中间截断）
    max_len = 60
    if len(desc) > max_len:
        desc = desc[:max_len].rsplit(" ", 1)[0].rsplit("，", 1)[0].rsplit("/", 1)[0]
    return desc if desc else info.get("display_name", tool)


def suggest_footer(tools, lang: str = "zh-CN") -> str:
    """构造答案末尾的兄弟技能软建议（无匹配则返回空串）。

    🔴 只建议、不阻断：本函数产出的文本追加在**答案之后**，不改变答案本身，
    也不要求用户先补参数 / 先安装。用户想取数时再显式发起。

    2026-09-29：优先使用 sibling_registry.json 动态生成，仅建议已安装技能。
    """
    tools = [t for t in (tools or ()) if t in _TOOL_DESC]
    if not tools:
        return ""

    registry = _load_sibling_registry()
    installed = _get_installed_skills(registry) if registry else set()

    if lang == "zh-CN":
        items_parts = []
        for t in tools:
            # 检查是否已安装（若有注册表）
            if registry and t not in installed:
                continue
            desc = _build_dynamic_desc(t, registry, "zh-CN") or _TOOL_DESC.get(t, {}).get("zh", t)
            items_parts.append(f"- `@skill:{t}`：{desc}")
        if not items_parts:
            return ""
        items = "\n".join(items_parts)
        return ("\n\n---\n\n💡 *补充：以上已按本技能自身能力作答。本问题还涉及下列兄弟技能，"
                "它们已在本机注册、客户端可直接调用；如需**真实数据、可复算结果或文件交付物**，"
                "直接调用即可：*\n" + items)
    else:
        items_parts = []
        for t in tools:
            if registry and t not in installed:
                continue
            # 英文路径优先用 _TOOL_DESC 的英文文案：sibling_registry 的 summary 恒含中文，
            # 复用会让英文答案夹中文（2026-11-09 修正）。
            desc = _TOOL_DESC.get(t, {}).get("en") or _build_dynamic_desc(t, registry, "en") or t
            items_parts.append(f"- `@skill:{t}`: {desc}")
        if not items_parts:
            return ""
        items = "\n".join(items_parts)
        return ("\n\n---\n\n💡 *Note: the answer above is ct-advisor's own. The sibling skills "
                "below are registered locally and can be invoked directly from the client — "
                "call them for **real data, reproducible results or file deliverables**:*\n" + items)


# ---------------------------------------------------------------------------
# 内置自测
# ---------------------------------------------------------------------------

SELF_TEST = [
    # (问题, 期望 need_tool) — 明确查询应高置信命中；定义/方法论/隐晦需求应 none
    ("算下样本量，ORR 30% vs 45%", "ct-samplesize"),
    ("检索 PD-1 抑制剂三期试验有哪些", "ct-registry"),
    ("拉一下司美格鲁肽在 2 型糖尿病的注册试验", "ct-registry"),   # 2026-08-20：README 示例 2 ZH
    ("Pull the registered trials for semaglutide in T2D", "ct-registry"),  # 2026-08-20：README 示例 2 EN
    ("computing sample size with power 80%", "ct-samplesize"),
    ("Give me the full competitive-intel picture for GLP-1 RA in obesity — trials, safety signals, and literature", "ct-registry"),  # 2026-08-21：README 示例 3 EN（REG_INTENT 让 registry 主判）
    ("I'm planning a Phase II oncology trial and also need the sample size — help me decide the design", "ct-samplesize"),  # 2026-08-21：README 示例 4 EN
    ("One of our PD-1 products has case reports of interstitial lung disease; QA suspects a new safety signal. Search the published literature (case reports, pharmacovigilance studies, reviews) for how much support this signal has, and give me a citable evidence summary for the signal-evaluation meeting", "ct-literature"),  # 2026-08-21：README 示例 7 EN（LIT_FIRST 文献优先）
    ("We're drafting a phase-3 protocol in this indication. Give me the published RCT + systematic-review evidence from the last 5 years for the introduction, then compute the sample size for a superiority design using the key assumptions I'll provide", "ct-samplesize"),  # 2026-08-21：README 示例 8 EN
    ("FAERS 里 XX 药心血管信号", "ct-safety"),
    ("查 XX 药的文献", "ct-literature"),
    ("我们一款 PD-1 产品有间质性肺炎个案报告，请检索已发表文献（病例报告、药物警戒研究、综述）评估信号支持度", "ct-literature"),  # 2026-08-20：README 示例 7（文献意图优先于 safety）
    ("估算检验效能 power 80%", "ct-samplesize"),
    ("这个适应症在研药物有哪几个", "ct-registry"),
    # 定义 / 标准操作 / 方法论 → none（不误触发）
    ("什么是样本量", "none"),
    ("样本量的定义", "none"),
    ("样本量计算要注意什么", "none"),
    ("SAE 上报时限是多少", "none"),
    ("为什么 AE 需要分级", "none"),
    # 2026-09-10：英文方法学问句含 "trial" 不得误判为 registry（README 示例 1 EN 实测回归）
    ("A confirmatory Phase III trial plans one interim analysis — how do I keep the overall type I error rate at 0.05?", "none"),
    ("How do I design a Phase III clinical trial?", "none"),
    # 2026-09-10（第十二轮续）：中文短词「在研」不得命中「在研|究者」——
    # README 新增实操例（GCP 受试者补偿 / PV 预期性判断）实测误判回归。
    ("方案规定完成全部访视的受试者可获得 5000 元交通补贴。某受试者因 SAE 提前退出，研究者是否应支付全额补偿？GCP 对此有何要求？", "none"),
    ("某不良反应在研究者手册（IB）中列为“少见”，但实际发生率在试验中达到 15%。PV 应如何评估是否需要更新 IB 和标签？", "none"),
    ("研究者发起的临床试验（IIT）与药企申办试验在监管上有何区别？", "none"),
    # 隐晦需求 → none（漏判由 Coze need_tool 兜底，不强行放宽）
    ("XX 药在肺癌的疗效如何", "none"),
    ("鼻咽癌目前的治疗手段", "none"),
    ("评估下这个方案的可行性", "none"),
    # 🔴 2026-09-10（第十四轮·关键词收紧）：以下为「泛词不再自动触发」回归——
    #   这些问句含「信号 / 文献 / 试验 / 设计 / 安全性」等弱词，但需求关联不明确，
    #   一律不自动调用（need_tool=None），仅由 suggest_footer 在答案末尾软建议。
    ("查 XX 药的安全性信号有哪些", "none"),                       # 弱词「安全性信号」→ 不触发
    ("帮我设计一个三期临床试验方案，要注意什么", "none"),             # 弱词「三期/临床试验」+ 方法论
    ("纸质 CRF 迁移到 EDC 要注意什么数据完整性？", "none"),          # 方法论（F1 流程）
    ("帮我找 XX 药治疗肺癌的最新文献", "ct-literature"),             # 「找…文献」句式 → 仍强命中
    ("How should I handle missing data when the endpoint cannot be interpreted?", "none"),
    ("What is the difference between a screening failure and a withdrawal?", "none"),
    ("我们的药物管线里有哪些在研项目", "ct-registry"),               # 高特异性「在研项目」
    # 2026-11-05（B7）：方案评阅意图 → 不自动调用（ct-protocol 为 B 档本地技能），仅软建议
    ("帮我评阅这份方案，给出修改意见", "none"),
    ("如何评审这个方案", "none"),
    # 合规题不得被误建议到 ct-protocol（「方案修改后…审查」非评阅意图）
    ("方案修改后需要重新伦理审查吗", "none"),
    # —— 2026-11-10 本地链路优化回归 ——
    # P0-1 混合意图拆分：咨询 + 执行同现 → 仍下发执行工具 need_tool（不再整体降级）
    ("解释一下为什么用双侧检验，并帮我算下样本量 ORR 30% vs 45%", "ct-samplesize"),
    ("说明样本量计算依据，并检索 PD-1 抑制剂三期试验", "ct-registry"),  # 同时验证 P0-2：registry 带参数胜出（字典序本应 samplesize 在前）
    ("解释一下 estimand 五属性，并检索 PD-1 抑制剂三期试验", "ct-registry"),
    # P0-2 证据加权：无参数者让位于带真实参数者（字典序本应 samplesize 在前）
    ("样本量一般怎么定，检索 PD-1 抑制剂三期试验有哪些", "ct-registry"),
    # P0-3 否定过滤：弱触发词紧邻否定词时被剔除（不影响强命中 / 未紧邻否定的弱候选）
    ("除了文献，帮我查 XX 药的安全性信号", "none"),  # 安全性为弱触发，否定下不软建议；need_tool 仍 none
    # P1-2 高精同义词：扩充后仍能高置信命中
    ("效应量怎么估算才够检出差异", "ct-samplesize"),
    ("同适应症在研药物竞争格局如何", "ct-registry"),
    ("相关文献里 PD-1 抑制剂有哪些关键研究", "ct-literature"),
    # —— 2026-11-10 复杂混合调用安全提示：多强命中应标记 split_advice 并生成提示（见 SPLIT_TEST）——
    ("检索 PD-1 抑制剂三期注册试验，并查一下相关文献", "ct-registry"),
    ("FAERS 里 XX 药肝损伤的 PRR 是多少，并算下样本量 ORR 30% vs 45%", "ct-samplesize"),
]

# 软建议断言（2026-09-10 第十四轮）：need_tool 必须为 None，且 suggest_tools 应包含预期技能
# （或 None 表示「不应给出建议」）。用于锁住「先自身作答 + 末尾建议」的新姿态。
SUGGEST_TEST = [
    # (问题, 期望 suggest_tools 至少包含 [tool...]，None/[] = 不应建议)
    ("样本量计算要注意什么", ["ct-samplesize"]),        # 咨询意图 + 强词 → 不调用，但建议
    ("什么是 FAERS 信号", ["ct-safety"]),              # 定义题 + 具名数据源 → 不调用，但建议
    ("查 XX 药的安全性信号有哪些", ["ct-safety"]),      # 弱命中 → 仅建议
    ("纸质 CRF 迁移到 EDC 要注意什么数据完整性？", []),  # 与兄弟技能无关 → 不建议
    ("某不良反应在研究者手册（IB）中列为“少见”，但实际发生率在试验中达到 15%。"
     "PV 应如何评估是否需要更新 IB 和标签？", []),        # PV 实操题 → 不建议（回归）
    ("为什么 AE 需要分级", []),                        # 与兄弟技能无关 → 不调用也不建议
    # —— 2026-09-10 修补（用户要求）：咨询护栏命中时**只建议强命中**，裸弱词不再溢出建议 ——
    #   回归来源：以下英文方法学 / 定义题此前均建议 ct-registry（裸词 `trials?`），题不对路。
    ("A confirmatory Phase III trial plans one interim analysis — "
     "how do I keep the overall type I error rate at 0.05?", []),
    ("What is the difference between ITT and mITT in a confirmatory trial?", []),
    ("How do I design a Phase III clinical trial?", []),
    ("样本量的定义", ["ct-samplesize"]),                # 护栏 + 强词 → 建议保留
    # —— 2026-11-05（B7）：方案评阅意图 → 建议本地 ct-protocol（结构化评审框架）——
    #   含「如何评审这个方案」：命中咨询护栏仍保留建议（护栏例外，题是对路的）。
    ("帮我评阅这份方案，给出修改意见", ["ct-protocol"]),
    ("如何评审这个方案", ["ct-protocol"]),
    # 合规题不得被误建议（「方案修改后…审查」非评阅意图）
    ("方案修改后需要重新伦理审查吗", []),
    # —— 2026-11-10 P0-3 否定过滤：弱触发词紧邻否定词时被剔除，未紧邻者保留 ——
    ("除了文献，方案里还要写哪些安全性内容", ["ct-safety"]),  # 文献紧邻「除了」被剔除，安全性保留
]

# 参数抽取断言（REKEY 防护）：确认前端预判抽到的键与 tool_mapping.required_params 对齐。
# registry 必须抽「cond」（非 drug）；samplesize 必须抽 p1/p2；无真实参数可抽时为空。
PARAM_TEST = [
    ("算下样本量，ORR 30% vs 45%", {"p1": 0.3, "p2": 0.45}),
    ("检索 PD-1 抑制剂三期试验有哪些", {"cond": "PD-1抑制剂"}),
    ("computing sample size with power 80%", {}),  # 仅预设，无真实参数可抽
    # 2026-08-21：英文药名/靶点抽取断言（README 示例 2/3/7 修复回归）
    ("Pull the registered trials for semaglutide in type-2 diabetes", {"cond": "semaglutide"}),
    ("Give me the full competitive-intel picture for GLP-1 RA in obesity — trials, safety signals, and literature", {"cond": "GLP-1 RA"}),
    ("One of our PD-1 products has case reports of interstitial lung disease; QA suspects a new safety signal. Search the published literature for how much support this signal has", {"topic": "PD-1"}),
]

# 复杂混合调用安全提示断言（2026-11-10）：多强命中 → split_advice=True 且 complexity_hint 非空；
# 单工具 / 无命中 → split_advice=False 且 hint 为空。用于锁住「复杂混合调用给安全提示」的新行为。
SPLIT_TEST = [
    ("检索 PD-1 抑制剂三期注册试验，并查一下相关文献", True),
    ("FAERS 里 XX 药肝损伤的 PRR 是多少，并算下样本量 ORR 30% vs 45%", True),
    ("检索 XX 药的三期注册试验", False),   # 单工具 → 不提示
    ("什么是样本量", False),                 # 咨询 → 不提示
]


def run_self_test() -> int:
    print("route_tool.py 预判自测")
    print("=" * 56)
    ok = 0
    for q, expect in SELF_TEST:
        got = predict_tool(q) or "none"
        mark = "✓" if got == expect else "✗"
        if got == expect:
            ok += 1
        print(f"  {mark} [{got:<13}] 期望 {expect:<13} | {q}")
    total = len(SELF_TEST)
    print("-" * 56)
    print(f"  工具命中准确率: {ok}/{total} = {ok / total * 100:.1f}%")

    # 软建议断言（2026-09-10 第十四轮）：不调用时是否给出恰当建议
    print("软建议断言（先自身作答 + 末尾建议）")
    print("-" * 56)
    sok = 0
    for q, expect in SUGGEST_TEST:
        res = predict(q)
        got = res.get("suggest_tools") or []
        # 期望非空 ⇒ 需包含；期望为空 ⇒ 结果必须为空（否则「不建议」断言形同虚设）
        ok_s = ((res.get("need_tool") is None)
                and all(e in got for e in expect)
                and (bool(expect) or not got))
        if ok_s:
            sok += 1
            sm = "✓"
        else:
            sm = "✗"
        print(f"  {sm} need={res.get('need_tool')} suggest={got} 期望含 {expect} | {q[:40]}")
    stotal = len(SUGGEST_TEST)
    print("-" * 56)
    print(f"  软建议准确率: {sok}/{stotal} = {sok / stotal * 100:.1f}%")

    # 参数抽取断言（REKEY 防护）
    print("参数抽取断言（REKEY 防护）")
    print("-" * 56)
    pok = 0
    for q, expect_params in PARAM_TEST:
        got_params = predict(q).get("params") or {}
        okp = all(got_params.get(k) == v for k, v in expect_params.items())
        # 额外防护：registry 绝不能再抽出已废弃的 "drug" 键（会导致与 required_params 失配）
        no_drug = "drug" not in got_params
        if okp and no_drug:
            pok += 1
            pm = "✓"
        else:
            pm = "✗"
        print(f"  {pm} [{got_params}] 期望含 {expect_params} | {q}")
    ptotal = len(PARAM_TEST)
    print("-" * 56)
    print(f"  参数断言准确率: {pok}/{ptotal} = {pok / ptotal * 100:.1f}%")

    # 复杂混合调用安全提示断言（2026-11-10）
    print("复杂混合调用安全提示断言（多强命中 → 拆分提示）")
    print("-" * 56)
    spok = 0
    for q, expect in SPLIT_TEST:
        res = predict(q)
        got = bool(res.get("split_advice"))
        hint = res.get("complexity_hint") or ""
        ok_s = (got == expect) and (bool(hint) == expect)
        if ok_s:
            spok += 1
            sm = "✓"
        else:
            sm = "✗"
        print(f"  {sm} split={got} hint_len={len(hint)} 期望={expect} | {q[:40]}")
    sptotal = len(SPLIT_TEST)
    print("-" * 56)
    print(f"  安全提示准确率: {spok}/{sptotal} = {spok / sptotal * 100:.1f}%")
    return 0 if (ok == total and sok == stotal and pok == ptotal and spok == sptotal) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="ct-advisor deterministic ct-tool predictor (Mode B prefetch)")
    ap.add_argument("question", nargs="?", help="用户问题原文")
    ap.add_argument("--json", action="store_true", help="输出 JSON（含 params / confidence）")
    ap.add_argument("--self-test", action="store_true", help="运行内置预判自测")
    args = ap.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.question:
        ap.print_help()
        return 2

    res = predict(args.question)
    if args.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(res.get("need_tool") or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
