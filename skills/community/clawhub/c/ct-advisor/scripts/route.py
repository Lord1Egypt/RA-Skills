#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 确定性入口闸门（代码级，无 LLM · 二值判定）

设计目标（治本，不依赖 LLM 纪律）：
  - 把「是否发 Coze / 是否需澄清」的决策从主 Agent（本地 LLM）收归成**代码确定性分类**。
  - 主 Agent 永远不自己判断难度，只运行本脚本拿标签，从根上消除
    「本地模型先理解问题→顺手答题→抢答/3-5min 循环」的旧故障。

【2026-09-26 二值化改造】判定结果只回答一个问题：**是否 vague**。
  本模块不再输出 simple / middle / complex 三档标签。理由：
    ① Coze 服务端每次都用 LLM（config/judge_difficulty_cfg.json）**重新估计**
       difficulty 并忽略上游标签（generate_organized_problems_node._judge_difficulty），
       本地三档对答案长度与深度完全无效；
    ② 本地链路（entry.py）早已只消费 is_vague()，非 vague 统一标记 "forwarded"；
    ③ 三档标签的"兜底 complex"曾误导 Agent 与用户对"难度判定"的预期
       （未命中任何信号 ≠ 真复杂，只是默认转发）。

  本模块持续维护的两项能力：
    ① is_vague()     —— vague 是唯一「不转发 Coze、先本地澄清」的分支
    ② timeout_tier() —— 转发超时档位 short / long（内部信号，不是难度标签，
                         由 refiner 在 difficulty == "forwarded" 时调用）

用法：
  python scripts/route.py "用户问题原文"
        → 打印一个标签：vague | forwarded
  python scripts/route.py --json "用户问题原文"
        → 打印 {"vague": true|false, "route": "...", "timeout": "short|long"}
  python scripts/route.py --timeout "用户问题原文"
        → 打印 short | long（本地超时档位）
  python scripts/route.py --self-test
        → 跑内置二值自测，输出每例命中/预期与准确率

分类逻辑（确定性，瞬时，stdlib-only）：
  1. 空串 / is_vague（指代不明/过短/回指省略，判断**可偏多**）→ vague
       （进入 clarify_loop 启发式菜单；宁可多澄清也不漏发 Coze）
  2. 其余 → forwarded（一律 verbatim 转发 Coze；难度与深度由 Coze 端判定）

转发 payload 约定：query_meta.difficulty 填 "vague"（经澄清收敛后仍 vague 时）
或 "forwarded"；与 entry.py 行为一致，refiner 枚举已接受二者。
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# 信号词典（确定性、可单测）
# ---------------------------------------------------------------------------

# 受控术语（CDISC / 临床试验领域），仅作 vague 排除锚点（短问句含术语 → 不算含糊）
TERM = re.compile(
    r"(SDTM|ADaM|AE|SAE|CE|CM|DS|VS|LB|EG|RS|SV|SE|TA|TI|TV|"
    r"CSR|TLF|CRF|EDC|eCRF|SAP|ICH[- ]?GCP|GCP|CDISC|ADSL|BDS|OCCDS|ADTTE|"
    r"PK|PD|MedDRA|WHODrug|IB|SUSAR|DSUR|ICF|RBM|QbD|ALCOA|ITT)"
)

# 定义意图（vague 排除锚点：短问句含定义句式时不算含糊）
DEF = re.compile(
    r"(什么是|什么意思|的定义|定义是|定义是什么|精确定义|含义|全称|英文缩写|英文全称|英文是|"
    r"\bmeans\b|\bdefine\b|definition)"
)

# 标准操作句式（vague 排除锚点）
STOP = re.compile(
    r"(是否符合|正确做法|记录和处理|"
    r"需要完成哪些核心|需要完成哪些关键|哪些关键任务|哪些核心步骤|需要在何时|应在何时|"
    r"需要保留哪些|需要具备哪些资质|如何溯源|如何进行.*?核查|溯源|核对|"
    r"上报时限|报告时限|时限|规范|流程|步骤|"
    r"如何提交|如何上报|如何填写|填写.*?规范|"
    r"属于.*?还是|有何要求|有何规定|资质|"
    r"如何使用|如何回收|补填|翻译后签署|锁定.*?步骤|关闭.*?任务|"
    r"评估哪些|如何确定.*?频率|"
    r"谁必须参加|保存要求|签署.*?要求|如何管理|"
    r"需要提交哪些核心文件|提交哪些核心文件|年度报告|快速审查|"
    r"破盲|是否应退出|是否构成重大|"
    r"保存多久|保留多久|是否属于|算不算|是否算|什么手续|正式退出)"
)

# 标准操作主题白名单（vague 排除锚点）
SIMPLE_TOPICS = re.compile(
    r"(alcoa|sdv|isf\b|siv\b|"
    r"上报时限|报告时限|sa[e]?\s*报告|sae 报告|"
    r"药物计数|药物清点|药物回收|药物发放|"
    r"温度超标|温度偏离|温控|"
    r"急救揭盲|紧急揭盲|破盲|"
    r"快速审查|年度报告|跟踪审查|修正案|"
    r"受试者补偿|"
    r"妊娠报告|妊娠结局|怀孕|哺乳|"
    r"筛选日志|筛选失败|中心关闭|监查报告|启动会|"
    r"随机化分层|分层随机化|区组|"
    r"代扣代缴|进口药品注册证|进口药品批件|"
    r"会议法定人数|保存要求|签署要求|"
    r"知情同意撤回|撤回知情同意|"
    r"退药|退回药物|"
    r"数据质疑|crf\s*填写|"
    r"筛选号|随机号|药物编号)",
    re.IGNORECASE,
)

# 长耗时信号（仅供 timeout_tier 使用：多步检索/生成类问题放宽等待上限，与难度标签无关）
CPLX = re.compile(
    r"(设计终点|试验设计|随机化设计|体系设计|方案设计|如何设计|"
    r"工艺变更|CMC变更|生产变更|变更评估|"
    r"框架|体系|多重比较|动态|同时测试|主方案|篮子|平台试验|适应性|贝叶斯|"
    r"代际|灰色|前沿|跨学科|基因编辑|基因治疗|生殖系|放射性|CAR-T|CMC|同情用药|"
    r"儿科外推|区块链|联邦学习|AI聊天|AI辅助|AI算法|iRECIST|BICR|网络安全|欺诈|结构性胁迫|"
    r"弱势群体|豁免|紧急使用|供应链|跨境|数据保护|外推|"
    r"NDA|CDE|Pre-IND|CIOMS|AESI|敏感性分析|因果关系|突破性治疗|DSMB|"
    r"勒索软件|地震|RPSFT|交叉调整|继续治疗|维持治疗|退出条件|eCOA|ePRO|PRO数据|PRO终点|"
    r"统计|假设检验|检验效能|估算|计算|样本量|n\s*=|"
    r"文献|安全性信号|靶点|适应症|剂量)"
)

# vague 指代信号（显性代词 + 短句）
VAGUE_PRON = re.compile(r"(这个|那个|它|它们|这|那)")

# 回指 / 省略线索（指向前文未明说的对象）。偏宽松：用复合形式（如"之前提到"）
# 避免误伤"之前的药物"这类清晰短句；纯方位词（前面/后面/上面/下面/前者/后者）
# 几乎总是语篇指代，直接纳入。
ANAPHORA = re.compile(
    r"(前面|后面|上面|下面|前者|后者|前边|后边|前述|前述的|上述的|"
    r"之前提到|之前说|之前讨论|刚才说|刚才提到|刚才问|刚才讨论|"
    r"上一条|上一个问题|上轮|上一次|您说的|你说的|您讲的|我说的|"
    r"前面那个|后面那个|上面那个|下面那个)"
)

# 语义 vague（2026-08-20 修复）：用户明说「不确定/不知道需要什么」且无明确对象
# → 进入本地澄清。
VAGUE_UNCERTAIN = re.compile(
    r"(?:不.{0,2}(?:确定|清楚|知道|了解)|没想好|拿不准|没有头绪|毫无头绪)"
    r".{0,10}(需要什么|要什么|做什么|怎么办|怎么弄|该做什么|该问什么|问什么|"
    r"怎么开始|从哪(?:里)?开始|什么需求|需求是什么|怎么用|怎么提问)|"
    r"\b(not sure|not certain|unsure|don'?t know|no idea|not clear|no clue)"
    r".{0,24}\b(what|how|which|where)\b|"
    r"\bwhat (?:do|should|can) i (?:need|ask|do|get|want)\b",
    re.IGNORECASE,
)
# 有明确对象的判断句式（命中 → 不算语义 vague）
VAGUE_UNCERTAIN_EXCL = re.compile(
    r"(不确定|不清楚|不知道|not sure|not certain|unsure).{0,14}"
    r"(是否|能不能|可不可以|对不对|合理|合规|正确|appropriate|valid|acceptable|\bif\b)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# 分类函数
# ---------------------------------------------------------------------------

def is_vague(q: str) -> bool:
    """指代不明 / 过短无实体 / 回指省略 → vague。
    🔴 唯一闸门判据：vague 是唯一「不转发 Coze」的分支（判断**可偏多**——
    宁可进本地澄清菜单，也不漏发 Coze）。"""
    # 1) 显性指代代词 + 短句（上限放宽到 24，覆盖"这个样本量计算要考虑什么"）
    if VAGUE_PRON.search(q) and len(q) <= 24:
        return True
    # 2) 回指 / 省略线索（无具体动作信号时按 vague；上限 30）
    if ANAPHORA.search(q) and len(q) <= 30:
        return True
    # 3) 过短且无术语 / 定义 / 标准操作锚点 → 视为 vague（偏多：含糊短句进菜单）
    if len(q) <= 10 and not TERM.search(q) and not DEF.search(q) \
       and not STOP.search(q) and not SIMPLE_TOPICS.search(q):
        return True
    # 4) 语义 vague（2026-08-20 补）：明说「不确定/不知道需要什么」→ 进入澄清。
    #    排除「不确定 X 是否/能不能…」这类有明确对象的具体判断（不判 vague）。
    if VAGUE_UNCERTAIN.search(q) and not VAGUE_UNCERTAIN_EXCL.search(q):
        return True
    return False


# ---------------------------------------------------------------------------
# 超时档位（内部信号 · 与 vague 判定共同构成本模块全部职责）
# ---------------------------------------------------------------------------

LONG_TIMEOUT_CHARS = 80


def timeout_tier(q: str) -> str:
    """本地转发超时档位：返回 "short" | "long"。

    超时是网络等待上限（refiner.timeout vs refiner.long_timeout），与答案难度无关：
    判定为 long 只是放宽上限，不会让快请求变慢。refiner 在 difficulty == "forwarded"
    时调用本函数决定等待档位。

    判据（保守放宽，宁可长不可短，避免长问题被 90s 截断）：
      1. 命中 CPLX 长耗时信号（统计/样本量/设计/外部数据…）→ long
      2. 问题长度 >= LONG_TIMEOUT_CHARS（长问句通常需多步检索）→ long
      3. 其余 → short
    """
    q = (q or "").strip()
    if not q:
        return "short"
    if CPLX.search(q):
        return "long"
    if len(q) >= LONG_TIMEOUT_CHARS:
        return "long"
    return "short"


def route_question(q: str) -> str:
    """返回 vague | forwarded —— 本模块唯一对外判定结果。

    🔴 vague：不直接转发，先进本地澄清循环（clarify_loop.py），收敛后再转发。
       forwarded：一切非 vague 问题，verbatim 转发 Coze；难度与深度由 Coze 端判定。"""
    q = (q or "").strip()
    if not q:
        return "vague"
    return "vague" if is_vague(q) else "forwarded"


def route_with_signals(q: str) -> dict:
    """调试用：返回二值判定 + 超时档位。"""
    q = (q or "").strip()
    v = is_vague(q) if q else True
    return {
        "vague": v,
        "route": "vague" if v else "forwarded",
        "timeout": timeout_tier(q),
    }


# ---------------------------------------------------------------------------
# 内置二值自测（用 --self-test 运行）
# ---------------------------------------------------------------------------

SELF_TEST = [
    # (问题, 期望标签: vague | forwarded)
    # ---- forwarded：清晰可转发（不区分难度）----
    ("什么是 SDTM", "forwarded"),
    ("AE 的英文全称是什么", "forwarded"),
    ("如何提交不良事件报告", "forwarded"),
    ("CRF 填写步骤", "forwarded"),
    ("SAE 上报时限", "forwarded"),
    ("SDTM", "forwarded"),
    ("上报时限是多少", "forwarded"),
    ("ITT今年有什么进展？", "forwarded"),      # 曾因三档兜底误显 complex，二值化后清晰转发
    ("解释 SDTM 和 ADaM 的区别", "forwarded"),
    ("为什么 AE 需要分级", "forwarded"),
    ("如何设计一个抗肿瘤药的随机对照试验方案", "forwarded"),
    ("样本量计算要考虑哪些因素", "forwarded"),
    ("不确定下一步怎么办，做法是否合规", "forwarded"),  # 明确对象排除 → 不澄清
    ("I'm not sure if this design is appropriate", "forwarded"),  # EN 排除 vague
    # ---- vague：指代不明 / 过短 / 回指省略（判断偏多）----
    ("这个怎么弄", "vague"),
    ("那个是什么意思", "vague"),
    ("它是指什么", "vague"),
    ("这个样本量怎么算", "vague"),              # 含代词仍判 vague（宁可多澄清）
    ("那个试验设计要注意什么", "vague"),
    ("前面说的统计检验方法该怎么选", "vague"),    # 回指省略
    ("上一条说的不良事件要怎么报", "vague"),      # 复合回指
    ("怎么办", "vague"),
    ("我不太确定自己到底需要什么", "vague"),      # 语义 vague（README 示例 5 ZH）
    ("I'm not sure what I actually need", "vague"),  # 语义 vague（EN）
    ("我不知道该从哪里开始", "vague"),
    ("", "vague"),                             # 空串兜底进澄清
]


def run_self_test() -> int:
    print("route.py 二值自测（vague | forwarded）")
    print("=" * 56)
    ok = 0
    for q, expect in SELF_TEST:
        got = route_question(q)
        mark = "✓" if got == expect else "✗"
        if got == expect:
            ok += 1
        print(f"  {mark} [{got:<9}] 期望 {expect:<9} | {q}")
    total = len(SELF_TEST)
    print("-" * 56)
    print(f"  准确率: {ok}/{total} = {ok / total * 100:.1f}%")
    return 0 if ok == total else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="ct-advisor deterministic entry gate (vague | forwarded)")
    ap.add_argument("question", nargs="?", help="用户问题原文")
    ap.add_argument("--json", action="store_true", help="输出 JSON（含超时档位）")
    ap.add_argument("--timeout", action="store_true",
                    help="输出本地超时档位 short|long")
    ap.add_argument("--self-test", action="store_true", help="运行内置二值自测")
    args = ap.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.question:
        ap.print_help()
        return 2

    if args.timeout:
        print(timeout_tier(args.question))
    elif args.json:
        print(json.dumps(route_with_signals(args.question), ensure_ascii=False))
    else:
        print(route_question(args.question))
    return 0


if __name__ == "__main__":
    sys.exit(main())
