#!/usr/bin/env python3
"""
深度研究引擎 v5.1 — 多源交叉验证+证据层次+三轮调研
集成到咨询总结报告生成器的 S3 内容扩增阶段
"""
import json

# ═══════════════════════════════════════════════
# 第一阶段：需求澄清
# ═══════════════════════════════════════════════

def identify_research_needs(extracted_text):
    """从提取的文本中识别需要深度研究的关键数据点
    
    返回: [(主题, 查询关键词, 优先级), ...]
    """
    needs = []
    
    # 识别数字指标（OEE、库存周转、生产周期等）
    metric_patterns = [
        ("OEE", ["OEE行业基准", "设备综合效率 制造业 基准"]),
        ("库存周转", ["库存周转率 行业平均", "制造业 库存周转 对标"]),
        ("生产周期", ["生产周期 行业标准", "制造周期 缩短 案例"]),
        ("良品率", ["良品率 行业标准", "直通率 制造业 基准"]),
        ("准时交付率", ["准时交付率 制造业 行业水平", "OTD 行业基准"]),
    ]
    
    for metric, keywords in metric_patterns:
        if metric in extracted_text:
            needs.append((f"{metric}行业对标", keywords[0], "high"))
    
    # 识别竞争对手/行业趋势
    trend_markers = ["行业趋势", "竞争对手", "市场规模", "增长", "政策"]
    if any(m in extracted_text for m in trend_markers):
        needs.append(("行业趋势与政策", "行业最新趋势 政策 2025 2026", "medium"))
    
    return needs

# ═══════════════════════════════════════════════
# 第二阶段：多源调研执行计划
# ═══════════════════════════════════════════════

def build_research_plan(topics):
    """根据研究方向生成调研执行计划
    
    每个主题执行三轮调研:
    第1轮: 广度搜索 → 5-10个来源
    第2轮: 深度提取 → 关键来源详细分析
    第3轮: 交叉验证 → 不同来源对比
    """
    plan = []
    for topic, query, priority in topics:
        plan.append({
            "topic": topic,
            "queries": [
                query,                                     # 第1轮: 主查询
                f"{query} 数据 报告 统计",                # 第2轮: 精确查询
                f"{query} 对比 分析 趋势",                 # 第3轮: 对比验证
            ],
            "priority": priority,
            "status": "pending"
        })
    return plan

# ═══════════════════════════════════════════════
# 第三阶段：数据融合
# ═══════════════════════════════════════════════

def merge_research_results(user_data, research_findings):
    """将用户数据与研究发现融合
    
    三级证据融合:
    L1: 用户原始数据 (最高优先级)
    L2: 权威来源数据 (中等优先级)  
    L3: 网络来源数据 (补充参考)
    """
    merged = {
        "user_data": user_data,
        "research_data": research_findings,
        "conclusions": []
    }
    
    # 对每个发现点生成综合结论
    for finding in research_findings:
        conclusion = {
            "topic": finding["topic"],
            "user_claim": finding.get("user_claim", ""),
            "research_support": finding.get("evidence", []),
            "consistency": "supported" if len(finding.get("evidence", [])) >= 2 else "insufficient",
            "source_level": "L2" if len(finding.get("evidence", [])) >= 3 else "L3"
        }
        merged["conclusions"].append(conclusion)
    
    return merged

# ═══════════════════════════════════════════════
# 数据点检查清单
# ═══════════════════════════════════════════════

def check_data_point(value, metric, industry_benchmark):
    """检查数据点是否需要标注或修正"""
    if not value or not industry_benchmark:
        return {"status": "unknown", "note": "数据不足，无法对标"}
    
    ratio = value / industry_benchmark
    if ratio > 2.0:
        return {"status": "warning", "note": f"显著偏离行业基准（{industry_benchmark}），建议核实"}
    elif ratio > 1.5:
        return {"status": "note", "note": f"高于行业基准（{industry_benchmark}），有改善空间"}
    else:
        return {"status": "good", "note": "数据合理"}

if __name__ == "__main__":
    print("深度研究引擎 v5.1 已加载")
    print("集成方式: 在 S3 内容扩增阶段调用")
    print("依赖: WebSearch + WebFetch 工具链")
