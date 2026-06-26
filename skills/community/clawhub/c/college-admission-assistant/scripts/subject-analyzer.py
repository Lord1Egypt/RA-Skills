#!/usr/bin/env python3
"""
选科组合覆盖率分析工具
分析不同选科组合在3+1+2模式下的专业覆盖率
"""

import json

# 3+1+2模式下的12种组合及专业覆盖率
SUBJECT_COMBINATIONS = [
    {"id": 1, "combination": "物理+化学+生物", "coverage": "97%+", 
     "target": "理工农医全领域", "difficulty": "高",
     "summary": "最强组合，覆盖绝大多数理工农医专业，但学习压力大"},
    {"id": 2, "combination": "物理+化学+地理", "coverage": "95%+",
     "target": "理工类+地学类", "difficulty": "高",
     "summary": "理工覆盖率极高，适合对地理有把握的学生"},
    {"id": 3, "combination": "物理+化学+政治", "coverage": "96%+",
     "target": "理工+军警政治类", "difficulty": "高",
     "summary": "理工+军警政法的黄金组合，专业选择面最广"},
    {"id": 4, "combination": "物理+生物+地理", "coverage": "90%",
     "target": "医学+地学+农林", "difficulty": "中等",
     "summary": "化学不强者选择，可报医学但受限较多"},
    {"id": 5, "combination": "物理+生物+政治", "coverage": "91%",
     "target": "医学+军警+教育", "difficulty": "中等",
     "summary": "文理兼备组合，适合目标军警或教育类"},
    {"id": 6, "combination": "物理+地理+政治", "coverage": "86%",
     "target": "地理信息+规划+公共管理", "difficulty": "中等",
     "summary": "偏文理科思维，适合目标地理/规划类"},
    {"id": 7, "combination": "历史+政治+地理", "coverage": "52%",
     "target": "文史哲法经管", "difficulty": "中等",
     "summary": "传统文科组合，专业选择面较窄"},
    {"id": 8, "combination": "历史+政治+生物", "coverage": "50%",
     "target": "文科+生命科学", "difficulty": "中等",
     "summary": "文科思维+生物兴趣，适合文理兼收专业"},
    {"id": 9, "combination": "历史+生物+地理", "coverage": "49%",
     "target": "偏记忆型专业", "difficulty": "中等",
     "summary": "不想选政治的替代选择"},
    {"id": 10, "combination": "历史+化学+地理", "coverage": "50%",
     "target": "考古文保+地学", "difficulty": "较高",
     "summary": "文科+化学思维，较少见组合"},
    {"id": 11, "combination": "历史+化学+政治", "coverage": "51%",
     "target": "法学+文保", "difficulty": "较高",
     "summary": "目标考古/文保/法等专业"},
    {"id": 12, "combination": "历史+化学+生物", "coverage": "50%",
     "target": "医学护理（文科倾向）", "difficulty": "较高",
     "summary": "想学医但理科不够的替代方案"},
]

# 2024年选科要求改革后的"物化绑定"影响
MUST_PAIR_PHYSICS_CHEMISTRY = [
    "临床医学", "口腔医学", "基础医学", "预防医学",
    "计算机科学与技术", "软件工程", "人工智能", "数据科学与大数据技术",
    "自动化", "电子信息工程", "通信工程",
    "机械工程", "车辆工程", "智能制造工程",
    "材料科学与工程", "新能源科学与工程",
    "土木工程", "水利工程", "建筑环境与能源应用工程",
    "化学工程与工艺", "制药工程",
    "生物工程", "生物医学工程",
    "电气工程及其自动化", "能源与动力工程",
    "核工程与核技术",
]


def analyze_combination(combo_name: str) -> dict:
    """
    分析指定选科组合

    Args:
        combo_name: 如 "物化生", "物化地", "史政地" 等
    
    Returns:
        组合分析结果
    """
    # 简写映射
    shorthand_map = {
        "物化生": "物理+化学+生物",
        "物化地": "物理+化学+地理",
        "物化政": "物理+化学+政治",
        "物生地": "物理+生物+地理",
        "物生政": "物理+生物+政治",
        "物地政": "物理+地理+政治",
        "史政地": "历史+政治+地理",
        "史政生": "历史+政治+生物",
        "史生地": "历史+生物+地理",
        "史化地": "历史+化学+地理",
        "史化政": "历史+化学+政治",
        "史化生": "历史+化学+生物",
    }

    full_name = shorthand_map.get(combo_name, combo_name)
    
    for combo in SUBJECT_COMBINATIONS:
        if combo["combination"] == full_name:
            return combo
    
    return {"error": f"未找到组合: {combo_name}"}


def recommend_combination(target: str, is_strong_physics: bool = True) -> dict:
    """
    根据目标专业推荐最佳选科组合

    Args:
        target: 目标专业方向描述
        is_strong_physics: 物理是否强势
    
    Returns:
        推荐结果
    """
    # 判断专业大类
    goal_lower = target.lower()
    
    # 医学类
    if any(kw in goal_lower for kw in ["医", "药", "临床", "生"]):
        if is_strong_physics:
            return {
                "recommendation": "物理+化学+生物",
                "reason": "医学类专业普遍要求物化，生物是医学基础，物化生组合最优",
            }
        else:
            return {
                "recommendation": "历史+化学+生物",
                "reason": "部分医学护理类接受历史，但专业选择面较窄",
            }
    
    # 理工类
    if any(kw in goal_lower for kw in ["工", "计算", "机械", "电子", "自动化", "建筑", "土木"]):
        return {
            "recommendation": "物理+化学+生物（或物理+化学+地理）",
            "reason": "理工类专业普遍要求物化绑定，选生物或地理视兴趣而定",
        }
    
    # 军警政法
    if any(kw in goal_lower for kw in ["军", "警", "法", "政"]):
        return {
            "recommendation": "物理+化学+政治（或历史+政治+地理）",
            "reason": "军警政法类专业要求政治，结合物理或历史均可",
        }
    
    # 文史哲
    if any(kw in goal_lower for kw in ["文", "史", "哲", "语言", "新闻", "教育"]):
        return {
            "recommendation": "历史+政治+地理",
            "reason": "传统文科组合，文史哲法经管全覆盖",
        }
    
    # 经济管理
    if any(kw in goal_lower for kw in ["经", "管", "商", "金融", "会计"]):
        return {
            "recommendation": "物理+化学+地理（或历史+政治+地理）",
            "reason": "经管类文理兼收，选物理可获得更大专业选择面",
        }
    
    # 无明确目标
    if is_strong_physics:
        return {
            "recommendation": "物理+化学+生物",
            "reason": "无明确目标时，选择覆盖率最高的组合保留最大选择空间",
        }
    else:
        return {
            "recommendation": "历史+政治+地理",
            "reason": "无明确目标时选择传统文科组合，保证文史哲法经管覆盖率",
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("功能: 分析选科组合和专业覆盖率")
        print("用法1: python subject-analyzer.py combo <组合名>")
        print("      示例: python subject-analyzer.py combo 物化生")
        print("用法2: python subject-analyzer.py recommend <目标专业> <物理强? true/false>")
        print("      示例: python subject-analyzer.py recommend 计算机 true")
        print("用法3: python subject-analyzer.py list")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "combo" and len(sys.argv) >= 3:
        result = analyze_combination(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "recommend" and len(sys.argv) >= 3:
        is_strong = len(sys.argv) < 4 or sys.argv[3].lower() in ("true", "yes", "1")
        result = recommend_combination(sys.argv[2], is_strong)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "list":
        for combo in SUBJECT_COMBINATIONS:
            print(f"  {combo['combination']:20s}  覆盖率: {combo['coverage']:5s}  难度: {combo['difficulty']}")
    else:
        print("未知参数")
        sys.exit(1)
