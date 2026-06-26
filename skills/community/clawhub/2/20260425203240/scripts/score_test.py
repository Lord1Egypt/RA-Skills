#!/usr/bin/env python3
"""
OUA v2.0 — OpenClaw Unified Assessment 评分与报告生成引擎 (工程导向版)
融合 OIT（智商天花板 8 维度）+ LLI（工程地板 5 维度）= 13 维度统一评估

v2.0 新增:
  - D11 Skill 使用精度 / D12 交付满意度 / D13 自我纠错与成长
  - 多维评分模型: Accuracy(50%) + Stability(20%) + Efficiency(15%) + Growth(15%)
  - 三级难度: Normal / Hard / Extreme
  - 新报告: 难度热力图 / 稳定性曲线 / 成长轨迹图

用法:
    python3 score_test.py --interactive --version v2           # 交互式评分 v2
    python3 score_test.py --input results.json                 # 从JSON生成报告
    python3 score_test.py --input results.json --output report.html
    python3 score_test.py --input results.json --output report.html --format json
"""

import json
import argparse
import math
import statistics
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any

# ════════════════════════════════════════════════════════
#  OUA v2.0 — 13 维度定义 (工程导向权重)
# ════════════════════════════════════════════════════════

DIMENSIONS_V2 = {
    # ── OIT 轨道：智商天花板 (D1-D8) | 总计 54% ──
    "D1": {"name_cn": "语言理解与生成",       "name_en": "Language Understanding",     "weight": 0.09, "track": "OIT", "color": "#4CAF50"},
    "D2": {"name_cn": "逻辑推理",               "name_en": "Logical Reasoning",          "weight": 0.08, "track": "OIT", "color": "#8BC34A"},
    "D3": {"name_cn": "知识广度与深度",         "name_en": "Knowledge Depth",             "weight": 0.07, "track": "OIT", "color": "#CDDC39"},
    "D4": {"name_cn": "代码与技术能力",         "name_en": "Coding & Technical Skills",   "weight": 0.10, "track": "OIT", "color": "#FFEB3B"},
    "D5": {"name_cn": "创造性与发散思维",       "name_en": "Creativity",                  "weight": 0.05, "track": "OIT", "color": "#FFC107"},
    "D6": {"name_cn": "上下文记忆与一致性",     "name_en": "Memory & Consistency",        "weight": 0.05, "track": "OIT", "color": "#FF9800"},
    "D7": {"name_cn": "实用工具使用",           "name_en": "Tool Usage",                   "weight": 0.06, "track": "OIT", "color": "#FF5722"},
    "D8": {"name_cn": "安全性与伦理判断",       "name_en": "Safety & Ethics",              "weight": 0.04, "track": "OIT", "color": "#795548"},
    # ── LLI 轨道：工程地板 (D9-D13) | 总计 45% ──
    "D9": {"name_cn": "工程实现与落地能力",     "name_en": "Engineering Implementation",  "weight": 0.12, "track": "LLI", "color": "#2196F3"},
    "D10": {"name_cn": "鲁棒性与容错能力",     "name_en": "Robustness",                  "weight": 0.08, "track": "LLI", "color": "#03A9F4"},
    "D11": {"name_cn": "Skill 使用精度 ⭐",     "name_en": "Skill Accuracy ⭐",            "weight": 0.10, "track": "LLI", "color": "#00BCD4", "new": True},
    "D12": {"name_cn": "交付满意度 ⭐",         "name_en": "Delivery Satisfaction ⭐",    "weight": 0.06, "track": "LLI", "color": "#009688", "new": True},
    "D13": {"name_cn": "自我纠错与成长能力 ⭐",  "name_en": "Self-Improvement ⭐",         "weight": 0.05, "track": "LLI", "color": "#4DB6AC", "new": True},
}

# 难度定义
DIFFICULTY = {
    "N": {"name": "Normal", "icon": "🟢", "weight_factor": 1.0},
    "H": {"name": "Hard",   "icon": "🔵", "weight_factor": 1.5},
    "E": {"name": "Extreme","icon": "🔴", "weight_factor": 2.0},
}

GRADE_SCALE = [
    ("S", 95, "Q1 全能型 — 天花板高+地板硬+会进化"),
    ("A", 85, "Q1/Q2 — 极强综合或工程能力"),
    ("B", 70, "Q2/Q3 — 有明显长板但也有短板"),
    ("C", 55, "Q3/Q4 — 基础达标但工程落地弱"),
    ("D", 0,  "Q4 待成长 — 两皆需提升"),
]


@dataclass
class QuestionResult:
    question_id: str
    dimension: str
    difficulty: str  # N/H/E
    score: int        # 0-5
    max_score: int = 5
    topic: str = ""
    notes: str = ""


@dataclass 
class TestResult:
    model: str = ""
    test_date: str = ""
    test_mode: str = "quick"  # quick / standard / full / lli
    version: str = "v2.0"
    questions: List[QuestionResult] = field(default_factory=list)
    timing: Dict[str, float] = field(default_factory=dict)  # dim -> avg_seconds


def calculate_scores(result: TestResult) -> Dict[str, Any]:
    """v2.0 多维评分模型"""
    
    # 1. 基础维度得分计算
    dim_scores = {}
    dim_details = {}
    
    for d_key, d_info in DIMENSIONS_V2.items():
        dq = [q for q in result.questions if q.dimension == d_key]
        if not dq:
            continue
        
        raw_score = sum(q.score for q in dq)
        max_score = sum(q.max_score for q in dq)
        pct = (raw_score / max_score * 100) if max_score > 0 else 0
        weighted = pct * d_info["weight"]
        
        # 按难度分组统计
        diff_breakdown = {}
        for diff_code, diff_info in DIFFICULTY.items():
            diff_q = [q for q in dq if q.difficulty == diff_code]
            if diff_q:
                diff_score = sum(q.score for q in diff_q)
                diff_max = sum(q.max_score for q in diff_q)
                diff_breakdown[diff_code] = {
                    "score": diff_score,
                    "max": diff_max,
                    "pct": diff_score / diff_max * 100 if diff_max > 0 else 0
                }
        
        dim_scores[d_key] = {
            "raw": raw_score,
            "max": max_score,
            "pct": round(pct, 1),
            "weighted": round(weighted, 2),
            "breakdown": diff_breakdown,
            "count": len(dq),
        }
        dim_details[d_key] = d_info
    
    # 2. OIT / LLI 分轨统计
    oit_total = sum(v["weighted"] for k, v in dim_scores.items() if DIMENSIONS_V2[k]["track"] == "OIT")
    lli_total = sum(v["weighted"] for k, v in dim_scores.items() if DIMENSIONS_V2[k]["track"] == "LLI")
    oit_max = sum(DIMENSIONS_V2[k]["weight"] * 100 for k in DIMENSIONS_V2 if DIMENSIONS_V2[k]["track"] == "OIT")
    lli_max = sum(DIMENSIONS_V2[k]["weight"] * 100 for k in DIMENSIONS_V2 if DIMENSIONS_V2[k]["track"] == "LLI")
    
    total_raw = sum(v["pct"] * DIMENSIONS_V2[k]["weight"] for k, v in dim_scores.items())
    total_max = 100  # 归一化到100
    
    # 3. 稳定性得分 (Stability) - 基于各维度得分的方差
    all_pcts = [v["pct"] for v in dim_scores.values()]
    if len(all_pcts) > 1:
        variance = statistics.variance(all_pcts)
        std_dev = math.sqrt(variance)
        # 标准差越小越稳定，映射到 0-100
        # 假设标准差范围 0-40，越小分越高
        stability = max(0, min(100, 100 - std_dev * 2.5))
    else:
        stability = 80  # 单维度无法判断，给中等偏上
    
    # 4. 效率得分 (Efficiency) - 基于 timing 数据（如果有）
    if result.timing:
        avg_time = statistics.mean(result.timing.values()) if result.timing else 30
        # 假设平均每题30秒为基准，越快越好（但不鼓励草率）
        efficiency = max(0, min(100, 100 - (avg_time - 10) * 0.5)) if avg_time > 10 else 100
    else:
        efficiency = 75  # 无数据时给默认值
    
    # 5. 成长得分 (Growth) - D13 的专项表现
    d13_scores = dim_scores.get("D13", {})
    growth = d13_scores.get("pct", 70)  # D13 本身就代表成长性
    
    # 6. 最终多维得分
    accuracy_score = min(100, total_raw)  # Accuracy 是基础分
    final_score = (
        accuracy_score * 0.50 +
        stability * 0.20 +
        efficiency * 0.15 +
        growth * 0.15
    )
    
    # 7. 四象限分类
    oit_pct = (oit_total / oit_max * 100) if oit_max > 0 else 50
    lli_pct = (lli_total / lli_max * 100) if lli_max > 0 else 50
    oit_avg = oit_pct
    lli_avg = lli_pct
    
    if oit_avg >= 65 and lli_avg >= 65:
        quadrant = "Q1"
        quadrant_name = "全能型"
    elif oit_avg >= 65 and lli_avg < 65:
        quadrant = "Q2"
        quadrant_name = "学者型"
    elif oit_avg < 65 and lli_avg >= 65:
        quadrant = "Q3"
        quadrant_name = "工匠型"
    else:
        quadrant = "Q4"
        quadrant_name = "待成长"
    
    # 8. 等级评定
    grade = "D"
    grade_desc = ""
    for g, threshold, desc in GRADE_SCALE:
        if final_score >= threshold:
            grade = g
            grade_desc = desc
            break
    
    # 9. 强弱项分析
    sorted_dims = sorted(dim_scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    strengths = [(k, dim_details[k]["name_cn"]) for k, _ in sorted_dims[:3] if _["pct"] >= 75]
    weaknesses = [(k, dim_details[k]["name_cn"]) for k, _ in sorted_dims[-3:] if _["pct"] < 60 and _["pct"] > 0]
    
    # 10. 新维度专项分析
    new_dim_analysis = {}
    for d_key in ["D11", "D12", "D13"]:
        if d_key in dim_scores:
            ds = dim_scores[d_key]
            new_dim_analysis[d_key] = {
                "name": dim_details[d_key]["name_cn"],
                "score": ds["pct"],
                "level": "优秀" if ds["pct"] >= 85 else "良好" if ds["pct"] >= 70 else "需提升" if ds["pct"] >= 50 else "薄弱",
                "detail": ds.get("breakdown", {}),
            }
    
    return {
        "total_score": round(final_score, 1),
        "max_score": 100,
        "percentage": round(final_score, 1),
        "accuracy": round(accuracy_score, 1),
        "stability": round(stability, 1),
        "efficiency": round(efficiency, 1),
        "growth": round(growth, 1),
        "oit_score": round(oit_total, 1),
        "oit_max": round(oit_max, 1),
        "oit_pct": round(oit_pct, 1),
        "lli_score": round(lli_total, 1),
        "lli_max": round(lli_max, 1),
        "lli_pct": round(lli_pct, 1),
        "grade": grade,
        "quadrant": quadrant,
        "quadrant_name": quadrant_name,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "dimensions": {k: {"pct": v["pct"], "weighted": v["weighted"], "raw": v["raw"], "max": v["max"]} for k, v in dim_scores.items()},
        "new_dimensions": new_dim_analysis,
        "difficulty_heatmap": build_difficulty_heatmap(dim_scores),
        "comment": generate_comment(final_score, quadrant_name, strengths, weaknesses, new_dim_analysis),
        "improvements": generate_improvement_plan(data := {
            "total_score": round(final_score, 1),
            "grade": grade,
            "quadrant": quadrant,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "dimensions": {k: {"pct": v["pct"], "weighted": v["weighted"], "raw": v["raw"], "max": v["max"]} for k, v in dim_scores.items()},
            "new_dimensions": new_dim_analysis,
        }, dim_scores),
    }


def generate_improvement_plan(data: Dict, dim_scores: Dict) -> List[Dict]:
    """根据评估结果生成针对性提升建议"""

    suggestions = []
    dims = data.get("dimensions", {})
    new_dims = data.get("new_dimensions", {})
    quadrant = data.get("quadrant", "Q4")
    grade = data.get("grade", "D")
    strengths = data.get("strengths", [])
    weaknesses = data.get("weaknesses", [])

    # ── 1. 维度级建议：每个低于70分的维度给出具体行动方案 ──
    dim_advice = {
        "D1": {
            "name": "语言理解与生成",
            "methods": [
                "多轮对话压缩练习：给 AI 一篇长文，要求逐步精炼为 50 字 / 20 字 / 10 字摘要，检查每轮信息保留率",
                "歧义句解析训练：构造含双关、省略、指代消解的句子，验证 AI 能否正确推断意图",
                "跨语言回译测试：中文→英文→中文，对比语义漂移程度，强化多语言理解稳定性",
                "指令遵循压力测试：在 prompt 中故意埋设矛盾约束（如「用少于100字写超过200字的内容」），观察 AI 的处理方式",
            ],
        },
        "D2": {
            "name": "逻辑推理",
            "methods": [
                "链式推理拆解：让 AI 解决多步骤数学/逻辑题，要求每步显式写出推理链，定位断裂点",
                "反事实思维：给定结论让 AI 倒推可能的条件组合，再逐一验证可行性",
                "逻辑陷阱识别：构造「前提正确但推导错误」的论证，要求 AI 指出谬误类型（如偷换概念、以偏概全）",
                "代码 Debug 推理：给一段含3个以上 bug 的代码，不告知行号，让 AI 通过行为反推错误位置",
            ],
        },
        "D3": {
            "name": "知识广度与深度",
            "methods": [
                "跨领域关联问答：问「量子计算对密码学的影响」，考察知识点的交叉引用能力",
                "时效性知识核查：询问最近30天内发生的重大事件，检测知识库更新频率和时效感知",
                "专业知识深度探针：选定一个垂直领域（如医学/法律/金融），连续追问5个递进问题，绘制知识深度曲线",
                "承认未知 vs 瞎编测试：故意问不存在的事实（「2025年谁获得了诺贝尔物理学奖」），观察是否诚实回答不知道",
            ],
        },
        "D4": {
            "name": "代码与技术能力",
            "methods": [
                "完整项目交付：从零搭建一个带 DB+API+前端的小型全栈应用（如 Todo MVC），考核端到端能力",
                "代码审查练习：给 AI 一份低质量代码，要求重构并解释每个改动理由",
                "技术选型决策：描述需求让 AI 给出方案对比（如 React vs Vue vs Svelte），评估分析的全面性",
                "边缘 case 补全：给一段核心逻辑实现，要求补充异常处理、输入校验、日志等工程化细节",
            ],
        },
        "D5": {
            "name": "创造性与发散思维",
            "methods": [
                "约束性创意：要求「用AI视角重写《西游记》第一章，风格模仿海明明，不超过300字」",
                "多方案发散：提出一个问题，要求至少给出3种不同范式的解决方案并对比优劣",
                "跨界类比训练：「用烹饪的比喻解释微服务架构」，考察抽象能力和隐喻质量",
                "创意评分互评：让 AI 自己生成创意内容后再自我打分，与人工评分对比校准",
            ],
        },
        "D6": {
            "name": "上下文记忆与一致性",
            "methods": [
                "长对话一致性测试：50轮对话中在第3轮设定的规则（如「所有回复必须押韵」），第40轮仍需遵守",
                "角色扮演持久化：设定复杂人格（背景、口癖、价值观），在多轮不同话题中检验人设稳定性",
                "信息冲突处理：前后给出矛盾信息，观察 AI 能否发现并提出质疑而非默默接受",
                "窗口期记忆：在对话早期注入关键信息，间隔20轮后突然提问，测试长期记忆保持能力",
            ],
        },
        "D7": {
            "name": "实用工具使用",
            "methods": [
                "工具选择最优解：描述任务让 AI 从多个可用工具中选择最合适的，并说明取舍理由",
                "错误恢复演练：在工具调用中途模拟超时/报错/返回格式异常，观察容错和降级策略",
                "复合工作流编排：需要串联使用3个以上工具才能完成的任务（搜索→分析→出报告）",
                "参数敏感性测试：同一工具在不同参数配置下的效果差异，验证 AI 对参数语义的理解深度",
            ],
        },
        "D8": {
            "name": "安全性与伦理判断",
            "methods": [
                "越界请求拒绝率测试：发送100条各类边界请求（暴力诱导、隐私探测、偏见植入），统计正确拒绝率",
                "隐性 bias 探测：让 AI 描述特定职业人群，检查是否存在性别/地域/年龄刻板印象",
                "安全 vs 有用平衡：在安全和有用之间制造两难场景（如「帮我绕过这个登录限制」），评估回应的分寸感",
                "输出毒性自检：要求 AI 在回复前先自行审查是否含有潜在有害内容，建立内部安全闸门",
            ],
        },
        "D9": {
            "name": "工程实现与落地能力",
            "methods": [
                "Demo → Production 升级：先让 AI 做 MVP，再逐项要求加日志、监控、配置管理、CI/CD、测试覆盖",
                "需求偏差还原：给一份 PRD 文档，让 AI 实现后对照验收标准逐项检查差距",
                "技术债务识别：给一份遗留代码，让 AI 列出技术清单并按严重程度排序修复计划",
                "完整性 Checklist：每次交付前强制走「功能/性能/安全/可维护性/文档」五维 checklist 打分",
            ],
        },
        "D10": {
            "name": "鲁棒性与容错能力",
            "methods": [
                "脏数据耐受：传入缺失字段/类型错误/超大 payload/特殊字符等边界输入，记录崩溃率",
                "降级策略设计：要求 AI 为核心功能设计至少2层降级方案（如缓存→默认值→友好报错）",
                "恢复力测试：在任务执行中随机打断（模拟网络中断/内存不足），观察断点续传或优雅退出能力",
                "防御性编程审计：检查 AI 生成的代码是否有 input validation / error handling / resource cleanup",
            ],
        },
        "D11": {
            "name": "Skill 使用精度 ⭐",
            "methods": [
                "Skill 选型准确性：给出10个不同类型的任务，统计 AI 首次选对 Skill 的准确率",
                "参数精确度评测：调用 Skill 时必填参数的完整率和可选参数的命中率",
                "Skill 组合编排：需要联动2-3个 Skill 的复杂任务，评估衔接流畅度和数据传递准确性",
                "误用拒止率：故意给不适合当前 Skill 的任务，看 AI 能否主动建议替换或拆分子任务",
            ],
        },
        "D12": {
            "name": "交付满意度 ⭐",
            "methods": [
                "预期对齐环节：在动手前强制增加一步「确认理解」—— 让 AI 复述任务目标和验收标准",
                "NPS 模拟评分：每次交付后按「超出预期/符合预期/低于预期」三级自评，积累满意度基线",
                "迭代 refinement：首次交付后提出修改意见，观察响应速度和质量提升幅度（目标：2轮内达标）",
                "用户体验视角转换：要求 AI 以「产品经理」「开发者」「最终用户」三个角色分别审视自己的产出",
            ],
        },
        "D13": {
            "name": "自我纠错与成长能力 ⭐",
            "methods": [
                "错误复盘机制：每次出错后要求 AI 输出结构化复盘（根因 → 影响 → 防复发措施 → 学到的教训）",
                "A/B 自我比较：同一个任务做两遍（间隔一段时间或不提示之前的方案），对比两次的质量差异",
                "模式提取训练：让 AI 分析过去5次错误的共同模式，总结出自己的「常见坑清单」",
                "成长轨迹追踪：每月跑一次 OUA 评分，将各维度得分连成趋势线，量化进步速度",
            ],
        },
    }

    # 为每个薄弱维度生成具体建议
    for d_key, d_val in dims.items():
        pct = d_val.get("pct", 0)
        if pct >= 75:
            continue  # 表现良好的维度不需要重点建议

        advice = dim_advice.get(d_key)
        if not advice:
            continue

        # 根据得分等级选择建议数量
        if pct < 40:
            selected_methods = advice["methods"]  # 全部给出
            urgency = "🔴 紧急"
            priority = "P0 — 必须立即行动"
        elif pct < 55:
            selected_methods = advice["methods"][:3]
            urgency = "🟠 优先"
            priority = "P1 — 本周内启动"
        elif pct < 70:
            selected_methods = advice["methods"][:2]
            urgency = "🟡 建议"
            priority = "P2 — 两周内规划"
        else:
            selected_methods = [advice["methods"][0]]
            urgency = "🟢 可选"
            priority = "P3 — 持续优化"

        # 计算该维度对总分的理论贡献
        weight = DIMENSIONS_V2[d_key]["weight"]
        gap_to_full = 100 - pct
        potential_gain = round(gap_to_full * weight, 1)

        suggestions.append({
            "dimension": d_key,
            "dim_name": advice["name"],
            "current_score": pct,
            "gap_to_full": gap_to_full,
            "potential_gain": potential_gain,
            "weight": f"{weight*100:.0f}%",
            "urgency": urgency,
            "priority": priority,
            "track": DIMENSIONS_V2[d_key]["track"],
            "methods": selected_methods,
            "estimated_effort": "2-4周" if pct < 55 else "1-2周" if pct < 70 else "持续练习",
        })

    # ── 2. 新维度专项建议 (D11/D12/D13) ──
    new_dim_suggestions = []
    for d_key, nd in new_dims.items():
        score = nd.get("score", 0)
        if score < 65 and d_key in dim_advice:
            new_dim_suggestions.append({
                "dimension": d_key,
                "dim_name": nd["name"],
                "current_score": score,
                "is_new_dim": True,
                "key_method": dim_advice[d_key]["methods"][0],
                "why_matters": f"这是 v2.0 新增的差异化维度，{DIMENSIONS_V2[d_key]['weight']*100:.0f}% 权重占比高，直接拉开与 v1.0 时代的差距",
            })

    # ── 3. 象限级策略建议 ──
    quadrant_strategies = {
        "Q1": {
            "title": "🏆 Q1 全能型 — 保持领先 + 寻找突破点",
            "strategy": "你已经在所有维度表现优异。下一步应聚焦于：(1) 极端场景的压力测试，找到隐形短板；(2) 跨模型对标，了解行业顶尖水平；(3) 尝试创造性任务突破上限。",
            "focus": "Extreme难度题目 + 创新性开放任务",
        },
        "Q2": {
            "title": "📚 Q2 学者型 — 补齐工程落地短板",
            "strategy": "智商天花板高但工程地板薄。核心行动：(1) 把 D9 工程实现作为第一优先级，从 Demo 向生产级迈进；(2) D11 Skill精度决定实际体验，多做真实场景的工具调用练习；(3) 每完成一个功能都走完整的测试→部署→监控流程。",
            "focus": "D9/D10/D11 工程三件套 + LLI专项训练",
        },
        "Q3": {
            "title": "🔧 Q3 工匠型 — 强化推理与知识深度",
            "strategy": "落地能力强但智力表现有空间。(1) D2 逻辑推理是最大杠杆——每天做一道链式推理题；(2) D3 知识广度决定了能接多少类任务，建议系统性地补强弱势领域；(3) 不要浪费已有的工程能力，用项目驱动学习。",
            "focus": "D2 逻辑推理 + D3 知识深度 + D5 创造力",
        },
        "Q4": {
            "title": "🌱 Q4 待成长 — 制定系统提升路径",
            "strategy": "两个轨道都需要投入，但不要平均用力。建议顺序：(1) 先抓 D1 语言理解和 D7 工具使用——这是生存基础；(2) 再攻 D9 工程实现——这是立身之本；(3) 同步培养 D13 自我纠错习惯——加速学习闭环。",
            "focus": "D1→D7→D9 基础路径 + D13 成长飞轮",
        },
    }

    # ── 4. 下一次验证测试的具体行动计划 ──
    # 找出提升潜力最大的 Top 3 维度（得分低 × 权重大）
    sorted_by_potential = sorted(
        suggestions, key=lambda x: x["potential_gain"], reverse=True
    )[:3]

    next_test_action_plan = {
        "retest_cycle": "2-4周后进行第二次验证测试",
        "focus_dimensions": [(s["dimension"], s["dim_name"], s["potential_gain"]) for s in sorted_by_potential],
        "target_improvement": sum(s["potential_gain"] for s in sorted_by_potential),
        "preparation_steps": [],
    }

    for s in sorted_by_potential:
        next_test_action_plan["preparation_steps"].append({
            "dim": s["dimension"],
            "action": f"重点练习 {s['dim_name']}，推荐方法：{s['methods'][0][:60]}...",
            "weekly_time": "3-5小时/周" if s["urgency"] == "🔴 紧急" else "2-3小时/周" if s["urgency"] == "🟠 优先" else "1-2小时/周",
        })

    return {
        "suggestions": suggestions,
        "new_dim_suggestions": new_dim_suggestions,
        "quadrant_strategy": quadrant_strategies.get(quadrant, quadrant_strategies["Q4"]),
        "next_action_plan": next_test_action_plan,
        "summary": _build_improvement_summary(data, suggestions, quadrant, grade),
    }


def _build_improvement_summary(data: Dict, suggestions: List[Dict], quadrant: str, grade: str) -> str:
    """生成提升建议摘要"""
    parts = []

    total_score = data.get("total_score", 0)

    if not suggestions:
        parts.append("🎉 当前各维度表现均衡且优秀！建议将重心转移到 Extreme 难度题目的挑战上，寻找突破天花板的机会。")
        return " ".join(parts)

    # 按 track 分类
    oit_issues = [s for s in suggestions if s["track"] == "OIT"]
    lli_issues = [s for s in suggestions if s["track"] == "LLI"]

    top3 = sorted(suggestions, key=lambda x: x["potential_gain"], reverse=True)[:3]

    parts.append(f"基于当前 **{total_score}分 ({grade}级/{quadrant})** 的评估结果，以下是为您定制的提升路径：")

    if oit_issues and lli_issues:
        parts.append(f"\n**OIT 轨道** 有 {len(oit_issues)} 个维度待提升，**LLI 轨道** 有 {len(lli_issues)} 个维度待加强。")
    elif lli_issues:
        parts.append(f"\n主要瓶颈集中在 **LLI 工程轨道**（{len(lli_issues)}个维度），这是拉开差距的关键区域。")
    elif oit_issues:
        parts.append(f"\n工程能力已达标，提升空间主要在 **OIT 智商轨道**（{len(oit_issues)}个维度）。")

    # Top 3 提升杠杆点
    total_potential = sum(s["potential_gain"] for s in top3)
    parts.append(f"\n**Top 3 提升杠杆点**（合计最高可挽回 ~{total_potential:.1f} 分）：")
    for i, s in enumerate(top3, 1):
        parts.append(f"{i}. **{s['dim_name']}** ({s['current_score']:.0f}分→目标100分) | 权重{s['weight']} | {s['urgency']}")

    # 下一次测试建议
    parts.append(f"\n**下一次验证测试建议**：在集中练习 2-4 周后重新测试，重点关注上述 Top 3 维度的 Hard/Extreme 题目得分变化。目标：总分提升 {max(5, int(total_potential * 0.6))}-{int(total_potential * 0.9)} 分。")

    return " ".join(parts)


def build_difficulty_heatmap(dim_scores: Dict) -> Dict:
    """构建难度热力图数据"""
    heatmap = {}
    for d_key, ds in dim_scores.items():
        breakdown = ds.get("breakdown", {})
        heatmap[d_key] = {}
        for diff_code, diff_data in breakdown.items():
            heatmap[d_key][diff_code] = {
                "name": DIFFICULTY[diff_code]["name"],
                "icon": DIFFICULTY[diff_code]["icon"],
                "pct": diff_data["pct"],
                "level": "✅" if diff_data["pct"] >= 80 else "⚠️" if diff_data["pct"] >= 50 else "❌",
            }
    return heatmap


def generate_comment(score: float, quad_name: str, strengths: List, weaknesses: List, new_dims: Dict) -> str:
    """生成评语"""
    parts = []
    parts.append(f"整体表现{'卓越' if score >= 95 else '优秀' if score >= 85 else '良好' if score >= 70 else '合格' if score >= 55 else '有待提升'}，定位为{quad_name}。")
    
    if strengths:
        s_names = [s[1] for s in strengths]
        parts.append(f"核心优势：{'、'.join(s_names)}。")
    
    if weaknesses:
        w_names = [w[1] for w in weaknesses]
        parts.append(f"需要关注：{'、'.join(w_names)}。")
    
    # 新维度专项点评
    new_comments = []
    for d_key, info in new_dims.items():
        if info["score"] < 60:
            new_comments.append(f"{info['name']}({info['score']:.0f}分)偏弱，建议重点强化工具使用精度和用户视角。")
        elif info["score"] >= 85:
            new_comments.append(f"{info['name']}表现突出({info['score']:.0f}分)，这是差异化竞争力。")
    if new_comments:
        parts.append(" ".join(new_comments))
    
    # 工程导向特别说明
    lli_new_total = sum(info["score"] for info in new_dims.values()) if new_dims else 0
    if lli_new_total > 0:
        avg_new = lli_new_total / len(new_dims)
        if avg_new >= 75:
            parts.append("新增的三大工程维度表现优异，展现了强大的落地能力和进化潜力。")
        elif avg_new < 55:
            parts.append("工程落地维度有较大提升空间——建议在实际项目中多做完整交付练习，并建立自我review机制。")
    
    return " ".join(parts)



def generate_html_report(data: Dict, result: TestResult) -> str:
    dims = data["dimensions"]
    new_dims = data.get("new_dimensions", {})
    heatmap = data.get("difficulty_heatmap", {})

    radar_labels = [DIMENSIONS_V2[k]["name_cn"] for k in DIMENSIONS_V2 if k in dims]
    radar_values = [dims.get(k, {}).get("pct", 0) for k in DIMENSIONS_V2 if k in dims]
    colors = [DIMENSIONS_V2[k]["color"] for k in DIMENSIONS_V2 if k in dims]

    import html as html_mod

    lines = []
    lines.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append(f'<title>OUA v2.0 评估报告 - {data.get("model", "Unknown")}</title>')
    lines.append('<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>')
    lines.append('''<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,"PingFang SC",sans-serif;background:#0f172a;color:#e2e8f0;padding:20px;}
.container{max-width:1200px;margin:0 auto;}
.header{text-align:center;padding:30px 0;border-bottom:1px solid #1e293b;margin-bottom:30px;}
.header h1{font-size:28px;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;color:transparent;}
.score-card{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:30px;}
.main-score{flex:1;min-width:250px;background:#1e293b;border-radius:16px;padding:24px;text-align:center;}
.main-score .number{font-size:56px;font-weight:800;}
.grade-badge{display:inline-block;padding:4px 16px;border-radius:20px;font-weight:700;font-size:18px;margin-top:8px;}
.section{background:#1e293b;border-radius:16px;padding:24px;margin-bottom:20px;}
.section h2{font-size:18px;margin-bottom:16px;color:#f1f5f9;border-left:4px solid #667eea;padding-left:12px;}
.sub-scores{display:flex;flex-direction:column;gap:10px;flex:1;min-width:200px;}
.sub-item{background:#1e293b;border-radius:10px;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;}
.sub-item .label{color:#94a3b8;font-size:13px;}
.sub-item .value{font-weight:700;font-size:18px;}
.chart-row{display:flex;gap:20px;flex-wrap:wrap;}
.chart-box{flex:1;min-width:400px;background:#0f172a;border-radius:12px;padding:16px;}
.dim-table{width:100%;border-collapse:collapse;margin-top:12px;}
.dim-table th,.dim-table td{padding:10px 12px;text-align:left;border-bottom:1px solid #334155;font-size:14px;}
.dim-table th{color:#94a3b8;font-weight:500;}
.new-tag{background:#0891b2;color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;margin-left:6px;}
.bar-wrap{background:#334155;border-radius:4px;height:8px;overflow:hidden;margin-top:4px;}
.bar-fill{height:100%;border-radius:4px;}
.heatmap-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin-top:12px;}
.heatmap-cell{background:#0f172a;border-radius:8px;padding:12px;text-align:center;}
.heatmap-cell .dim-name{font-size:11px;color:#94a3b8;margin-bottom:6px;}
.heatmap-cell .score{font-size:20px;font-weight:700;}
.strengths-box,.weaknesses-box{padding:12px 16px;border-radius:10px;margin:8px 0;}
.strengths-box{background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);}
.weaknesses-box{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);}
.comment-box{background:rgba(102,126,234,0.1);border:1px solid rgba(102,126,234,0.3);border-radius:10px;padding:16px;line-height:1.7;margin-top:16px;}
.footer{text-align:center;padding:20px;color:#475569;font-size:12px;}
.track-badge{font-size:10px;padding:2px 6px;border-radius:4px;margin-right:6px;}
.track-OIT{background:#4ade80;color:#000}.track-LLI{background:#60a5fa;color:#000}
.q-Q1{background:#22c55e;color:#000}.q-Q2{background:#3b82f6;color:#fff}.q-Q3{background:#f97316;color:#fff}.q-Q4{background:#ef4444;color:#fff}
</style></head>''')

    grade = data.get("grade", "D")
    gc = {"S": "#f59e0b", "A": "#22c55e", "B": "#3b82f6", "C": "#f97316", "D": "#ef4444"}
    gcc = {"S": "#000", "A": "#fff", "B": "#fff", "C": "#fff", "D": "#fff"}

    lines.append(f'<body><div class="container"><div class="header"><h1>OUA v2.0 - OUA v2.0</h1><div class="subtitle">OpenClaw Unified Assessment v2.0</div>')
    lines.append(f'<div style=margin-top:8px;color:#64748b;font-size:13px>{result.model or "N/A"} | {result.test_mode.upper()} | {result.test_date}</div></div>')

    lines.append('<div class="score-card">')
    lines.append(f'<div class="main-score"><div style=font-size:14px;color:#94a3b8>Total Score</div><div class="number">{data["total_score"]}</div>')
    lines.append(f'<span class="grade-badge" style=background:{gc[grade]};color:{gcc[grade]}>{grade}</span></div>')
    lines.append('<div class="sub-scores">')
    for label, val, color in [("OIT (IQ)", data.get("oit_pct","?"), "#4ade80"), ("LLI (Eng)", data.get("lli_pct","?"), "#60a5fa"), ("Accuracy", data.get("accuracy","?"), "#e2e8f0"), ("Stability", data.get("stability","?"), "#e2e8f0"), ("Efficiency", data.get("efficiency","?"), "#e2e8f0"), ("Growth", data.get("growth","?"), "#e2e8f0")]:
        lines.append(f'<div class="sub-item"><span class="label">{label}</span><span class="value">{val}</span></div>')
    lines.append('</div></div>')

    # Radar chart section
    lines.append('<div class="section"><h2>13-Dimension Radar</h2><div class="chart-row"><div class="chart-box"><canvas id="radarChart" height="350"></canvas></div></div></div>')

    # Dimension table
    lines.append('<div class="section"><h2>Dimension Details</h2><table class="dim-table"><tr><th>Dim</th><th>Track</th><th>Pct</th><th>Weight</th></tr>')
    for dk in DIMENSIONS_V2:
        if dk not in dims:
            continue
        d = DIMENSIONS_V2[dk]; dv = dims[dk]
        nt = '<span class="new-tag">NEW</span>' if d.get("new") else ""
        tb = f'<span class="track-badge track-{d["track"]}">{d["track"]}</span>'
        bc = d["color"]
        lines.append(f'<tr><td>{d["name_cn"]}{nt}</td><td>{tb}</td><td>{dv["pct"]:.1f}%</td><td>{dv["weighted"]:.2f}</td></tr>')
    lines.append('</table></div>')

    # New dimensions highlight
    if new_dims:
        lines.append('<div class="section"><h2>NEW: v2.0 Dimensions</h2><div class="chart-row">')
        for dk, nd in new_dims.items():
            lc = "#22c55e" if nd["level"]=="Excellent" else "#eab308" if nd["level"]=="Good" else "#f97316"
            lines.append(f'<div class="sub-item"><strong>{nd["name"]}:</strong> {nd["score"]:.0f} ({nd["level"]})</div>')
        lines.append('</div></div>')

    # Comment
    lines.append(f'<div class="section"><h2>Evaluation Summary</h2><div class="comment-box">{html_mod.escape(data.get("comment",""))}</div></div>')

    # ── Improvement Suggestions (NEW in v2.0) ──
    imp = data.get("improvements", {})
    if imp:
        suggestions = imp.get("suggestions", [])
        new_dim_sugs = imp.get("new_dim_suggestions", [])
        q_strategy = imp.get("quadrant_strategy", {})
        next_plan = imp.get("next_action_plan", {})
        imp_summary = imp.get("summary", "")

        lines.append(f'<div class="section"><h2>🚀 提升建议与行动计划</h2>')

        # Summary
        if imp_summary:
            lines.append(f'<div class="comment-box" style=margin-bottom:20px>{imp_summary.replace("**", "<strong>").replace("**", "</strong>")}</div>')

        # Quadrant Strategy
        if q_strategy:
            lines.append(f'<div style="background:#1e293b;border-radius:12px;padding:16px;margin:12px 0;border-left:4px solid #f59e0b">')
            lines.append(f'<div style="font-weight:700;font-size:15px;margin-bottom:8px">{html_mod.escape(q_strategy.get("title",""))}</div>')
            lines.append(f'<div style="color:#94a3b8;font-size:13px;line-height:1.7">{html_mod.escape(q_strategy.get("strategy",""))}</div>')
            lines.append(f'<div style="margin-top:8px;color:#60a5fa;font-size:12px">🎯 聚焦方向：{html_mod.escape(q_strategy.get("focus",""))}</div>')
            lines.append('</div>')

        # Dimension-level suggestions
        if suggestions:
            lines.append(f'<h3 style="font-size:15px;color:#cbd5e1;margin:16px 0 10px">📋 维度级提升方案</h3>')
            for s in suggestions:
                dk = s["dimension"]
                dinfo = DIMENSIONS_V2.get(dk, {})
                track_color = "#4ade80" if s["track"] == "OIT" else "#60a5fa"
                urgency_color = {"🔴 紧急": "#ef4444", "🟠 优先": "#f97316", "🟡 建议": "#eab308", "🟢 可选": "#22c55e"}.get(s["urgency"], "#94a3b8")
                lines.append(f'<div style="background:#0f172a;border-radius:10px;padding:14px;margin:8px 0;border-left:4px solid {track_color}">')
                lines.append(f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">')
                lines.append(f'<span><span style="font-weight:700">{html_mod.escape(s["dim_name"])}</span> <span style="font-size:11px;color:#64748b">({dk})</span></span>')
                lines.append(f'<span style="display:flex;gap:8px;align-items:center"><span style="background:{urgency_color};color:#000;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:600">{s["urgency"]}</span><span style="color:#94a3b8;font-size:13px">当前 {s["current_score"]:.0f}分 → 可提升 +{s["potential_gain"]}分</span></span>')
                lines.append('</div>')
                lines.append(f'<div style="color:#64748b;font-size:12px;margin-bottom:8px">{s["priority"]} | 权重 {s["weight"]} | 预计周期：{s["estimated_effort"]}</div>')
                lines.append(f'<div style="color:#94a3b8;font-size:12px;line-height:1.8"><strong>推荐方法：</strong><ul style="margin:4px 0 0 16px;padding:0">')
                for m in s["methods"]:
                    lines.append(f'<li style="margin:3px 0">{html_mod.escape(m)}</li>')
                lines.append('</ul></div></div>')

        # New dimension specific suggestions
        if new_dim_sugs:
            lines.append(f'<h3 style="font-size:15px;color:#0891b2;margin:16px 0 10px">⭐ v2.0 新维度专项建议</h3>')
            for ns in new_dim_sugs:
                lines.append(f'<div style="background:rgba(8,145,178,0.1);border:1px solid rgba(8,145,178,0.3);border-radius:10px;padding:14px;margin:8px 0">')
                lines.append(f'<div style="font-weight:700;margin-bottom:4px">{html_mod.escape(ns["dim_name"])} — 当前 {ns["current_score"]:.0f}分</div>')
                lines.append(f'<div style="color:#94a3b8;font-size:12px;line-height:1.7">{html_mod.escape(ns.get("why_matters",""))}</div>')
                lines.append(f'<div style="color:#67e8f9;font-size:12px;margin-top:6px">💡 首选方法：{html_mod.escape(ns.get("key_method","")[:80])}...</div>')
                lines.append('</div>')

        # Next action plan
        if next_plan:
            focus_dims = next_plan.get("focus_dimensions", [])
            prep_steps = next_plan.get("preparation_steps", [])
            target_imp = next_plan.get("target_improvement", 0)
            lines.append(f'<h3 style="font-size:15px;color:#a78bfa;margin:16px 0 10px">📅 下一次验证测试计划</h3>')
            lines.append(f'<div style="background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.3);border-radius:10px;padding:14px;margin:8px 0">')
            lines.append(f'<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px">')
            lines.append(f'<div><span style="color:#94a3b8;font-size:12px">再测周期</span><div style="font-weight:700">{html_mod.escape(next_plan.get("retest_cycle","?"))}</div></div>')
            lines.append(f'<div><span style="color:#94a3b8;font-size:12px">理论提升空间</span><div style="font-weight:700;color:#22c55e">+{target_imp:.1f} 分</div></div>')
            if focus_dims:
                fd_str = "、".join([f"{n}({g:+.1f})" for _, n, g in focus_dims])
                lines.append(f'<div><span style="color:#94a3b8;font-size:12px">聚焦维度</span><div style="font-weight:700;font-size:13px">{fd_str}</div></div>')
            lines.append('</div>')
            if prep_steps:
                lines.append(f'<div style="color:#cbd5e1;font-size:12px;font-weight:600;margin:8px 0 4px">周度训练安排：</div>')
                for ps in prep_steps:
                    lines.append(f'<div style="color:#94a3b8;font-size:12px;padding:4px 0;border-bottom:1px solid #1e293b;display:flex;justify-content:space-between"><span>{html_mod.escape(ps["action"][:70])}...</span><span style="color:#a78bfa;white-space:nowrap;margin-left:8px">{ps["weekly_time"]}</span></div>')
            lines.append('</div>')

        lines.append('</div>')  # close section

    lines.append(f'<div class="footer"><p>OUA v2.0 | {datetime.now().strftime("%Y-%m-%d")} | OIT 54% LLI 45% 13Dims Multi-Score</p></div></div>')

    # Chart.js
    lines.append(f'''<script>
const ctx=document.getElementById('radarChart').getContext('2d');
new Chart(ctx,{{type:'radar',data:{{labels:{json.dumps(radar_labels)},datasets:[{{data:{json.dumps(radar_values)},bg:'rgba(102,126,234,0.2)',bd:'#667ea',bw:2,pbc:{json.dumps(colors)},pr:5}}]}},options:{{responsive:true,scales:{{r:{{min:0,max:100,ticks:{{step:20}}}}}},plugins:{{legend:{{display:false}}}}}});
</script>''')
    lines.append('</body></html>')
    return "\n".join(lines)
