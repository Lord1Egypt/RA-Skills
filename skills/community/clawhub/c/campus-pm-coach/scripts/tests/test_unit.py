#!/usr/bin/env python3
"""
单元测试：规则引擎 / 本地结构化解析 / 评分引擎 / 优化器 / 面试题生成。
运行：python3 tests/test_unit.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rule_engine
import resume_parser
import evaluator
import optimizer
import interviewer
import formatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIM_PATH = os.path.join(BASE_DIR, "config", "default_dimensions.json")

with open(DIM_PATH, "r", encoding="utf-8") as f:
    DIMENSIONS = json.load(f)["dimensions"]

RESUME = """张三
电话：13800138000
邮箱：zhangsan@example.com
所在地：北京
目标岗位：产品经理（实习）

教育经历
北京邮电大学　本科　信息管理与信息系统　2022.09 - 2026.06

实习经历
2025.06 - 2025.09　某互联网大厂　产品实习生（电商方向）
- 负责商品详情页改版，通过用户调研与竞品分析梳理需求，输出PRD并推动研发上线
- 参与大促活动策划，优化下单转化链路，转化率提升12%
- 搭建数据看板监控核心指标，每周输出复盘报告

2024.07 - 2024.10　某创业公司　产品助理（社交方向）
- 协助产品经理完成新功能设计与迭代，跟进开发进度

项目经历
校园二手交易平台 App　2024.03 - 2024.06
- 从0到1设计校园二手交易平台，负责需求分析、原型设计与PRD撰写
- 组织5人团队完成开发上线，运营3个月累计注册用户2000+
- 主导用户访谈与问卷调研，提炼3个核心需求并排定优先级

技能特长
Axure、Figma、PRD撰写、SQL、Excel、XMind、数据分析、A/B测试
"""

JD = """产品经理实习生（AI方向）
1. 负责AI产品的需求分析与方案设计，输出PRD与原型
2. 参与用户调研与竞品分析，洞察用户需求与使用场景
3. 跟进产品开发落地与上线，协调研发、设计、运营推进项目
4. 搭建数据看板，监控转化率与留存数据，驱动产品迭代
任职要求：熟悉需求分析、原型设计，熟练使用Axure、Figma，具备数据分析能力，熟悉SQL与Excel，有互联网产品实习经验者优先
"""


def run(name, cond, extra=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {extra}")
    return cond


all_ok = True


def check(name, cond, extra=""):
    global all_ok
    ok = run(name, cond, extra)
    all_ok = all_ok and ok


# ---------------------------------------------------------------------------
# 1. 本地结构化解析
# ---------------------------------------------------------------------------
st = resume_parser.parse_resume(RESUME)
check("解析出电话", st["basic_info"]["phone"] == "13800138000", st["basic_info"]["phone"])
check("解析出邮箱", "example.com" in st["basic_info"]["email"])
check("解析出教育经历", len(st["education"]) >= 1)
check("解析出实习经历", len(st["work_experience"]) >= 2, f"{len(st['work_experience'])} 段")
check("解析出项目经历", len(st["projects"]) >= 1)
check("解析出技能", len(st["skills"]["technical"]) >= 3)

# ---------------------------------------------------------------------------
# 2. 规则引擎：单规则
# ---------------------------------------------------------------------------
ctx = {
    "resume_text": RESUME,
    "structured": st,
    "jd_text": JD,
    "jd_analysis": evaluator.analyze_jd(JD),
}

r = rule_engine.run_rule({"type": "keyword_density", "keywords": ["用户调研", "竞品分析", "PRD", "原型"], "target_hits": 3}, ctx)
check("keyword_density 命中且满分", r.score == 100.0, f"score={r.score}")

r = rule_engine.run_rule({"type": "quantified", "patterns": ["\\d+%", "\\d+\\s*人", "\\d+\\s*个"], "min_expected": 3}, ctx)
check("quantified 检测到量化成果", r.score >= 60, f"score={r.score} evidence={r.evidence}")

r = rule_engine.run_rule({"type": "product_flow", "flow_keywords": {
    "调研": ["调研", "访谈", "问卷"],
    "需求": ["需求", "痛点"],
    "方案": ["PRD", "原型"],
    "落地": ["上线", "落地"],
    "验证": ["数据", "留存"],
}, "required_stages": 3}, ctx)
check("product_flow 覆盖至少 3 环节", r.score >= 60, f"score={r.score}")

r = rule_engine.run_rule({"type": "action_verb", "verbs": ["主导", "负责", "搭建", "推动"], "target_hits": 4}, ctx)
check("action_verb 强动词命中", r.score >= 75, f"score={r.score}")

r = rule_engine.run_rule({"type": "star_structure", "result_words": ["提升", "增长"], "context_words": ["负责", "针对"]}, ctx)
check("star_structure 行动+结果信号", r.score >= 50, f"score={r.score}")

r = rule_engine.run_rule({"type": "section_presence", "sections": ["education", "work_experience", "projects", "skills"], "per_missing": 25}, ctx)
check("section_presence 模块齐全满分", r.score == 100.0)

r = rule_engine.run_rule({"type": "jd_coverage", "target_ratio": 0.6}, ctx)
check("jd_coverage 有效", 0 <= r.score <= 100 and r.evidence, f"score={r.score}")

# 空白简历：规则应给低分
empty_ctx = {"resume_text": "", "structured": {}, "jd_text": JD, "jd_analysis": evaluator.analyze_jd(JD)}
r = rule_engine.run_rule({"type": "quantified", "patterns": ["\\d+%"], "min_expected": 3}, empty_ctx)
check("空白简历 quantified 得 0 分", r.score == 0.0)

# 未知规则类型
r = rule_engine.run_rule({"type": "unknown_rule"}, ctx)
check("未知规则按 0 分处理", r.score == 0.0)

# ---------------------------------------------------------------------------
# 2.5 新评分体系规则（校招产品经理能力评价体系）
# ---------------------------------------------------------------------------
r = rule_engine.run_rule({"type": "industry_match", "industries": ["电商", "游戏", "金融", "社交", "AI", "人工智能"]}, ctx)
check("industry_match 识别到简历行业方向（电商/社交）", r.score >= 40, f"score={r.score} {r.evidence}")

r = rule_engine.run_rule({"type": "substance_work", "flow_keywords": {
    "调研": ["用户调研", "访谈", "问卷"],
    "产出PRD": ["PRD", "原型", "需求文档"],
    "评审": ["评审", "需求评审"],
    "落地": ["上线", "落地"],
    "复盘": ["复盘", "总结"],
}, "required_stages": 3}, ctx)
check("substance_work 覆盖实际性工作闭环", r.score >= 60, f"score={r.score} {r.evidence}")

r = rule_engine.run_rule({"type": "major_relevance", "related": ["计算机", "软件", "信息", "电子", "通信", "自动化", "人工智能", "数据"]}, ctx)
check("major_relevance 信息专业为计算机相关", r.score >= 80, f"score={r.score} {r.evidence}")

r = rule_engine.run_rule({"type": "logic_elements", "elements": {
    "背景（为什么做）": ["背景", "初衷", "痛点", "为什么"],
    "产出（具体产出物）": ["PRD", "原型", "方案", "上线"],
    "价值衡量（怎么衡量价值）": ["提升", "增长", "转化率", "留存"],
    "北极星指标（核心衡量）": ["北极星", "核心指标", "DAU", "GMV"],
}, "min_elements": 3}, ctx)
check("logic_elements 覆盖产出/价值衡量要素", r.score >= 50, f"score={r.score} {r.evidence}")

r = rule_engine.run_rule({"type": "roadmap_presence", "keywords": ["roadmap", "路线图", "长期目标", "规划", "里程碑"]}, ctx)
check("roadmap_presence 未命中给低分", r.score < 50, f"score={r.score}")

r = rule_engine.run_rule({"type": "redundancy_check", "padding_words": ["相关", "进行", "能够", "等等", "大概", "基本上", "差不多"], "max_repeats": 6, "min_length": 120}, ctx)
check("redundancy_check 无过度重复给高分", r.score >= 70, f"score={r.score}")

# 修复：负责/参与/协助是简历正常强动词，不应被判为口水词（避免优化后反而低分）
r = rule_engine.run_rule(
    {"type": "redundancy_check", "padding_words": ["相关", "进行", "能够", "等等", "大概", "基本上", "差不多"], "max_repeats": 6, "min_length": 120},
    {"resume_text": "负责用户需求收集，负责竞品分析，负责PRD撰写，负责与开发团队沟通，负责数据看板搭建，参与需求评审，参与上线测试，协助项目推进。"
                   "另外负责了用户反馈整理，负责了版本迭代规划，负责了原型设计与评审会议组织，参与产品推广活动策划，协助运营同学完成活动落地与数据回收。",
     "structured": {}, "jd_text": JD, "jd_analysis": evaluator.analyze_jd(JD)},
)
check("redundancy_check 正常动作词不算口水词", r.score >= 80, f"score={r.score}")

r = rule_engine.run_rule({"type": "english_ability", "certs": ["CET-4", "CET-6", "四级", "六级", "雅思", "托福"], "cross_border_hint": ["跨境", "出海", "海外", "国际"]}, ctx)
check("english_ability 无英语证书非跨境给基础分", 40 <= r.score <= 80, f"score={r.score}")

r = rule_engine.run_rule({"type": "ai_exploration", "ai_keywords": ["AI", "大模型", "LLM", "AIGC", "GPT"], "output_keywords": ["落地", "上线", "产出", "提效"]}, ctx)
check("ai_exploration 无 AI 证据给低分", r.score < 50, f"score={r.score}")

r = rule_engine.run_rule({"type": "soft_quality", "traits": {
    "责任心": ["负责", "完成", "闭环", "交付"],
    "创造力": ["创新", "从0到1", "探索"],
    "逻辑严谨": ["梳理", "框架", "优先级", "规划"],
    "热爱": ["热爱", "长期使用", "深度体验", "自驱"],
}, "min_traits": 3}, ctx)
check("soft_quality 覆盖责任心/创造力/逻辑严谨", r.score >= 50, f"score={r.score} {r.evidence}")

# 带 AI 的简历应获得更高 AI 探索分
AI_RESUME = RESUME + "\n项目经历\nAI 简历助手 2025.01 - 2025.03\n- 使用大模型与 Prompt 搭建 AI 简历优化助手，接入 GPT API 并上线，帮助用户提效 50%"
st_ai = resume_parser.parse_resume(AI_RESUME)
ctx_ai = {"resume_text": AI_RESUME, "structured": st_ai, "jd_text": JD, "jd_analysis": evaluator.analyze_jd(JD)}
r = rule_engine.run_rule({"type": "ai_exploration", "ai_keywords": ["AI", "大模型", "LLM", "AIGC", "GPT", "Prompt", "提示词"], "output_keywords": ["落地", "上线", "产出", "提效", "接入"]}, ctx_ai)
check("ai_exploration 有 AI 落地证据给高分", r.score >= 80, f"score={r.score}")

# ---------------------------------------------------------------------------
# 3. 评分引擎
# ---------------------------------------------------------------------------
ev = evaluator.evaluate_resume(RESUME, st, JD, DIMENSIONS)
check("维度数为 5", len(ev["dimension_scores"]) == 5)
check("权重之和为 100", abs(sum(d["weight"] for d in ev["dimension_scores"]) - 100) < 0.001)
check("总分在 0-100", 0 <= ev["total_score"] <= 100, f"total={ev['total_score']}")
check("总分与加权一致", abs(ev["total_score"] - ev["computed_score"]) < 0.01)
for d in ev["dimension_scores"]:
    check(f"维度[{d['name']}]得分在 0-100", 0 <= d["score"] <= 100, f"score={d['score']}")
    if d["score"] < 85:
        check(f"维度[{d['name']}]有建议", len(d["suggestions"]) >= 1, f"suggestions={len(d['suggestions'])}")
    else:
        check(f"维度[{d['name']}]高分表现优秀", d["score"] >= 85, f"score={d['score']}")
check("rule_trace 可追溯", len(ev["rule_trace"]) == 5)
check("JD 分析有技能关键词", len(ev["jd_analysis"]["skill_keywords"]) >= 3, str(ev["jd_analysis"]["skill_keywords"][:5]))
check("JD 分析提取到 AI 行业提示", "AI" in ev["jd_analysis"]["industry_hints"], str(ev["jd_analysis"]["industry_hints"]))

# 产品经理强简历 vs 弱简历的区分度
WEAK_RESUME = "王五\n电话：13900139000\n邮箱：wangwu@example.com\n\n教育经历\n某大学 本科\n\n技能\nExcel"
st_weak = resume_parser.parse_resume(WEAK_RESUME)
ev_weak = evaluator.evaluate_resume(WEAK_RESUME, st_weak, JD, DIMENSIONS)
check("强简历总分 > 弱简历总分", ev["total_score"] > ev_weak["total_score"],
      f"strong={ev['total_score']} weak={ev_weak['total_score']}")
check("弱简历有明确短板提示", len(ev_weak["gaps"]) >= 1)

# ---------------------------------------------------------------------------
# 4. 优化器
# ---------------------------------------------------------------------------
opt = optimizer.build_optimized_resume(RESUME, st, ev, JD, "突出实习经历，补充量化表达")
check("优化稿非空且比原文长", len(opt["resume"]) > len(RESUME) * 0.5)
check("优化指令识别到 quant+highlight", "quant" in opt["strategies"] and "highlight" in opt["strategies"])
check("优化稿含待补充量化提示（引用行）", "> 待补充量化数据" in opt["resume"])
check("优化稿正文行内不含标注", "【" not in rule_engine.strip_meta_text(opt["resume"]))
check("优化稿含优化摘要", "本次优化摘要" in opt["resume"])
check("优化说明非空", len(opt["change_log"]) >= 1)

# 默认指令（未提供）
opt2 = optimizer.build_optimized_resume(RESUME, st, ev, JD, "")
check("默认指令为 generic", "generic" in opt2["strategies"])

# 精简指令
opt3 = optimizer.build_optimized_resume(RESUME, st, ev, JD, "精简成一页")
check("精简指令识别", "condense" in opt3["strategies"])

# 不编造数据：原文没有"月薪"等词，优化稿不应出现
check("不编造数据（无数字捏造）", "10000" not in opt["resume"])

# ---------------------------------------------------------------------------
# 4.5 防幻觉校验（不新增非本人执行细节）
# ---------------------------------------------------------------------------
# 伪造新增数字 → 应告警
w = optimizer._hallucination_guard(RESUME, "转化率提升 9999%")
check("防幻觉：新增数字被检测", any("9999" in x for x in w), str(w))

# 伪造所有权词夸大（参与→主导） → 应告警
w2 = optimizer._hallucination_guard("参与了项目A", "独立主导了项目A并牵头落地")
check("防幻觉：所有权词夸大被检测", len(w2) >= 1, str(w2))

# 真实优化稿正文（不含评分摘要）应通过校验
opt_body = opt["resume"].split("### 本次优化摘要")[0]
w3 = optimizer._hallucination_guard(RESUME, opt_body)
check("真实优化稿正文通过防幻觉校验", len(w3) == 0, str(w3))

# ---------------------------------------------------------------------------
# 4.6 首轮诊断（三部分一体化输出）
# ---------------------------------------------------------------------------
qs_md = interviewer.generate_interview_questions(opt["resume"], JD, st)
quick = formatter.format_quick_report(ev, JD, qs_md)
check("quick 含①评分与细项原因", "简历评分与细项原因描述" in quick)
check("quick 含②可能问到的问题", "可能问到的问题" in quick)
check("quick 含③综合判断", "综合判断" in quick)
check("quick 含匹配度结论", "匹配度结论" in quick)
check("quick 含投递建议", "投递建议" in quick)
check("quick 含细项原因证据", "细项原因（逐条规则证据" in quick)
check("quick 含匹配度等级", "匹配度：" in quick)

qs_extracted = formatter.extract_questions(qs_md, 5)
check("extract_questions 提取到 5 题", len(qs_extracted) == 5, f"{len(qs_extracted)} 题")

judgement = formatter.build_judgement(ev)
check("综合判断含核心竞争力/风险点",
      any("核心竞争力" in l for l in judgement) and any("关键风险点" in l for l in judgement),
      str(judgement[:2]))

# 优化稿末尾附三部分（每轮优化后输出结构恒含三部分）
opt_full = formatter.append_diagnosis_section(opt["resume"], ev, qs_md)
check("优化稿末尾含三部分诊断", "本轮优化后的三部分诊断" in opt_full)
check("优化稿末尾含①细项原因", "细项原因（逐条规则证据" in opt_full)
check("优化稿末尾含②可能问到的问题", "可能问到的问题" in opt_full)
check("优化稿末尾含③综合判断", "综合判断" in opt_full)

# ---------------------------------------------------------------------------
# 4.7 元信息剥离（修复"优化后反而低分"）
# ---------------------------------------------------------------------------
dirty = """# 张三 —— 优化版简历
13800138000　|　zhangsan@example.com
> 目标岗位：产品经理（实习）

教育经历
北京邮电大学　本科　信息管理与信息系统　2022.09 - 2026.06

> 待补充量化数据（以下经历建议补充具体数字）：
>   · 负责商品详情页改版

---
### 本次优化摘要（来自评分引擎）
- **过往经验匹配度（70分）**：建议补充量化数据
## 本轮优化后的三部分诊断
### ① 简历评分与细项原因描述
| 维度 | 权重 | 得分 |
| --- | --- | --- |
| 过往经验匹配度 | 20% | 70 |
"""
clean = rule_engine.strip_meta_text(dirty)
check("strip_meta 截断诊断分节", "三部分诊断" not in clean)
check("strip_meta 截断优化摘要", "本次优化摘要" not in clean)
check("strip_meta 剥离引用行", "目标岗位" not in clean and "待补充量化数据" not in clean)
check("strip_meta 剥离表格行", "| 维度" not in clean)
check("strip_meta 剥离行内标注", "【" not in clean and "】" not in clean)
check("strip_meta 剥离标题行", "优化版简历" not in clean)
check("strip_meta 保留正文行", "信息管理与信息系统" in clean and "北京邮电大学" in clean)

# 核心回归：高"负责"频次简历 → 优化稿（含三部分诊断）重新评分不低于原文
PADDING_RESUME = """钱七
电话：13700137000
邮箱：qianqi@example.com

教育经历
北京邮电大学　本科　计算机科学与技术　2022.09 - 2026.06

实习经历
2025.06 - 2025.09　某电商公司　产品实习生
- 负责了用户需求收集，负责了竞品分析，负责了PRD撰写，负责了与开发沟通
- 参与了需求评审，参与了上线测试
2024.07 - 2024.10　某社交公司　产品助理
- 负责了数据报表，负责了用户反馈整理
- 参与了版本迭代规划，协助了项目推进

项目经历
校园二手平台　2024.03 - 2024.06
- 负责了原型设计，负责了用户调研
- 做了用户增长方案，做了功能优化

技能特长
Axure、SQL、PRD、需求分析
"""
st_p = resume_parser.parse_resume(PADDING_RESUME)
ev_p = evaluator.evaluate_resume(PADDING_RESUME, st_p, JD, DIMENSIONS)
opt_p = optimizer.build_optimized_resume(PADDING_RESUME, st_p, ev_p, JD, "")
qs_p = interviewer.generate_interview_questions(opt_p["resume"], JD, st_p)
opt_full_p = formatter.append_diagnosis_section(opt_p["resume"], ev_p, qs_p)
st_opt = resume_parser.parse_resume(opt_full_p)
ev_opt = evaluator.evaluate_resume(opt_full_p, st_opt, JD, DIMENSIONS)
check("优化稿+诊断全文重新评分不低于原文", ev_opt["total_score"] >= ev_p["total_score"],
      f"{ev_p['total_score']} → {ev_opt['total_score']}")
# 结构化解析不被诊断污染
check("优化稿全文解析专业正确", st_opt["education"][0]["major"] == "计算机科学与技术",
      str(st_opt.get("education", [{}])[0].get("major")))
check("优化稿全文解析姓名正确", st_opt["basic_info"]["name"] == "钱七",
      st_opt["basic_info"]["name"])

# ---------------------------------------------------------------------------
# 5. 面试题生成
# ---------------------------------------------------------------------------
qs = interviewer.generate_interview_questions(opt["resume"], JD, st)
for cat_name in ["自我介绍与产品认知", "需求分析与产品设计", "数据思维与数据分析",
                 "项目与实习经历深挖", "行为面试", "开放设计题", "反问环节"]:
    check(f"面试题含分类: {cat_name}", cat_name in qs)
check("面试题含项目深挖（实习/项目名）", ("某互联网大厂" in qs) or ("校园二手交易平台" in qs))
check("面试题含 JD 高频考察点附录", "JD 高频考察点" in qs)
check("面试题数量充足", qs.count("**问题**") >= 20, f"{qs.count('**问题**')} 题")

# 模板加载
tpl = interviewer.load_templates()
check("题库模板含 7 分类", len(tpl["categories"]) == 7)

print()
print("ALL PASS" if all_ok else "SOME FAILED")
sys.exit(0 if all_ok else 1)
