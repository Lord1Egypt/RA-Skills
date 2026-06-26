#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面相学分析工具 v1.0
根据面部特征提供传统面相学解读（娱乐参考）

使用方法:
    python analyze.py "鼻子高挺"
    python analyze.py "眉毛浓密 眼睛大"
    python analyze.py --template
"""

import json
import sys

# 面相知识库
FACE_KNOWLEDGE = {
    # 鼻子相关
    "鼻子高挺": {"category": "财帛宫", "meaning": "财运较好，有领导能力，事业心强", "tags": ["财运", "事业"]},
    "鼻子塌陷": {"category": "财帛宫", "meaning": "财运一般，需努力积累财富", "tags": ["财运"]},
    "鼻头有肉": {"category": "财帛宫", "meaning": "聚财能力强，理财有道", "tags": ["财运"]},
    "鼻翼饱满": {"category": "财帛宫", "meaning": "守财能力强，有积蓄", "tags": ["财运"]},
    "鼻孔外露": {"category": "财帛宫", "meaning": "花钱大方，需注意理财", "tags": ["财运"]},
    
    # 眉毛相关
    "眉毛浓密": {"category": "兄弟宫", "meaning": "人缘好，朋友多，重情义", "tags": ["人际", "性格"]},
    "眉毛稀疏": {"category": "兄弟宫", "meaning": "独立自主，朋友较少", "tags": ["性格"]},
    "眉毛整齐": {"category": "兄弟宫", "meaning": "人际关系和谐，做事有条理", "tags": ["人际"]},
    "眉毛杂乱": {"category": "兄弟宫", "meaning": "思绪较多，人际关系复杂", "tags": ["性格"]},
    "断眉": {"category": "兄弟宫", "meaning": "兄弟姐妹缘薄或关系有波折", "tags": ["六亲"]},
    
    # 眼睛相关
    "眼睛大": {"category": "监察官", "meaning": "性格开朗，表达力强，感情丰富", "tags": ["性格", "感情"]},
    "眼睛小": {"category": "监察官", "meaning": "心思细腻，观察力强，内敛", "tags": ["性格"]},
    "眼睛有神": {"category": "监察官", "meaning": "精力充沛，运势正旺", "tags": ["运势"]},
    "眼睛无神": {"category": "监察官", "meaning": "近期疲劳，需注意休息", "tags": ["健康"]},
    "眼尾下垂": {"category": "夫妻宫", "meaning": "性格温和，感情细腻", "tags": ["性格", "感情"]},
    "眼尾上扬": {"category": "夫妻宫", "meaning": "性格外向，有魅力", "tags": ["性格"]},
    
    # 嘴巴相关
    "嘴巴大": {"category": "出纳官", "meaning": "表达能力强，社交能力好", "tags": ["性格", "社交"]},
    "嘴巴小": {"category": "出纳官", "meaning": "谨慎细心，言语保守", "tags": ["性格"]},
    "嘴唇厚": {"category": "出纳官", "meaning": "重感情，为人热情", "tags": ["性格", "感情"]},
    "嘴唇薄": {"category": "出纳官", "meaning": "理性冷静，善于分析", "tags": ["性格"]},
    "嘴角上扬": {"category": "出纳官", "meaning": "乐观积极，人缘好", "tags": ["性格"]},
    "嘴角下垂": {"category": "出纳官", "meaning": "易悲观，需注意心态调整", "tags": ["性格"]},
    
    # 耳朵相关
    "耳朵大": {"category": "采听官", "meaning": "福气好，肾气足，长寿相", "tags": ["福气", "健康"]},
    "耳朵小": {"category": "采听官", "meaning": "精明能干，注重细节", "tags": ["性格"]},
    "耳垂厚": {"category": "采听官", "meaning": "有福气，晚年运好", "tags": ["福气"]},
    "耳朵贴脑": {"category": "采听官", "meaning": "听话孝顺，传统保守", "tags": ["性格"]},
    "招风耳": {"category": "采听官", "meaning": "性格外向，好奇心强", "tags": ["性格"]},
    
    # 额头相关
    "额头高": {"category": "官禄宫", "meaning": "聪明智慧，早年运势好", "tags": ["智力", "运势"]},
    "额头低": {"category": "官禄宫", "meaning": "实际务实，大器晚成", "tags": ["性格"]},
    "额头饱满": {"category": "官禄宫", "meaning": "事业顺利，有贵人相助", "tags": ["事业"]},
    "额头凹陷": {"category": "官禄宫", "meaning": "早年辛苦，需努力", "tags": ["运势"]},
    "发际线整齐": {"category": "官禄宫", "meaning": "事业发展稳定", "tags": ["事业"]},
    
    # 下巴相关
    "下巴方圆": {"category": "奴仆宫", "meaning": "晚年运好，有领导力", "tags": ["运势", "性格"]},
    "下巴尖": {"category": "奴仆宫", "meaning": "艺术气质，晚年需规划", "tags": ["性格"]},
    "下巴短": {"category": "奴仆宫", "meaning": "行动力强，晚年需注意", "tags": ["性格"]},
    "双下巴": {"category": "奴仆宫", "meaning": "有福气，人缘好", "tags": ["福气"]},
    "下巴后缩": {"category": "奴仆宫", "meaning": "性格内向，晚年需注意健康", "tags": ["性格", "健康"]},
    
    # 颧骨相关
    "颧骨高": {"category": "权力", "meaning": "有权力欲，管理能力强", "tags": ["事业", "性格"]},
    "颧骨低平": {"category": "权力", "meaning": "性格温和，不争权", "tags": ["性格"]},
    "颧骨有肉": {"category": "权力", "meaning": "权力稳固，人缘好", "tags": ["事业"]},
    "颧骨无肉": {"category": "权力", "meaning": "权力易失，需注意人际", "tags": ["事业"]},
    
    # 痣相 - 十二宫位 (v1.4.0 新增)
    # 命宫痣
    "印堂有痣": {"category": "命宫痣", "meaning": "30岁前后运势有转折，贵人运与小人运并存，重大决策需谨慎", "tags": ["痣相", "运势", "注意"]},
    # 兄弟宫痣
    "眉中有痣": {"category": "兄弟宫痣", "meaning": "有贵人相助人缘好，但兄弟姐妹可能缘薄，合伙需谨慎", "tags": ["痣相", "人际", "贵人"]},
    "眉尾有痣": {"category": "兄弟宫痣", "meaning": "朋友多但知己少，易有财务纠纷", "tags": ["痣相", "人际", "财务"]},
    # 夫妻宫痣
    "眼尾有痣": {"category": "夫妻宫痣", "meaning": "感情易有波折，婚姻需经营，晚婚较稳", "tags": ["痣相", "感情", "婚姻"]},
    "眼下有痣": {"category": "夫妻宫痣", "meaning": "感情丰富易为情所困，需防烂桃花", "tags": ["痣相", "感情", "泪痣"]},
    # 子女宫痣
    "眼下卧蚕有痣": {"category": "子女宫痣", "meaning": "子女缘深但操心多，需注意子女健康", "tags": ["痣相", "子女", "健康"]},
    # 财帛宫痣
    "鼻头有痣": {"category": "财帛宫痣", "meaning": "有赚钱能力但易破财，需谨慎理财", "tags": ["痣相", "财运", "破财"]},
    "鼻翼有痣": {"category": "财帛宫痣", "meaning": "漏财难守积蓄，合伙财务需明确", "tags": ["痣相", "财运", "漏财"]},
    "鼻梁有痣": {"category": "财帛宫痣", "meaning": "中年财运有波折，健康需注意", "tags": ["痣相", "财运", "健康"]},
    # 疾厄宫痣
    "鼻梁中段有痣": {"category": "疾厄宫痣", "meaning": "脊椎肠胃需注意，健康预警", "tags": ["痣相", "健康", "注意"]},
    # 迁移宫痣
    "太阳穴有痣": {"category": "迁移宫痣", "meaning": "外出有机遇但需防意外，异地发展有利", "tags": ["痣相", "出行", "变动"]},
    # 奴仆宫痣
    "下巴中央有痣": {"category": "奴仆宫痣", "meaning": "晚年有福田宅旺，但需注意下属关系", "tags": ["痣相", "晚年", "福气"]},
    # 官禄宫痣
    "额头中央有痣": {"category": "官禄宫痣", "meaning": "事业有起伏，早成需防晚节", "tags": ["痣相", "事业", "起伏"]},
    # 福德宫痣
    "眉上有痣": {"category": "福德宫痣", "meaning": "有祖业或长辈助力，晚年有福", "tags": ["痣相", "福气", "长辈"]},
    # 父母宫痣
    "额头两侧有痣": {"category": "父母宫痣", "meaning": "与父母缘深但健康需注意", "tags": ["痣相", "父母", "健康"]},
    
    # 综合特征
    "三庭均等": {"category": "整体", "meaning": "一生运势平稳，各阶段发展均衡", "tags": ["运势"]},
    "五眼协调": {"category": "整体", "meaning": "面部比例好，人际关系和谐", "tags": ["人际"]},
    "面色红润": {"category": "气色", "meaning": "气血充足，运势正旺", "tags": ["健康", "运势"]},
    "面色苍白": {"category": "气色", "meaning": "气血不足，需注意休息", "tags": ["健康"]},
    "面色发黄": {"category": "气色", "meaning": "脾胃需调理，财运波动", "tags": ["健康", "财运"]},
}

# 组合分析
COMBO_ANALYSIS = {
    "富贵相": {
        "features": ["鼻子高挺", "鼻头有肉", "额头饱满", "下巴方圆", "眼睛有神"],
        "analysis": "传统富贵相特征：财运好、事业顺、晚年福"
    },
    "事业型": {
        "features": ["额头高", "鼻子高挺", "颧骨高", "眼睛有神"],
        "analysis": "事业心强，有领导能力，适合管理岗位"
    },
    "艺术型": {
        "features": ["下巴尖", "眼睛大", "眉毛整齐", "嘴唇薄"],
        "analysis": "艺术气质，感性思维，适合创意工作"
    },
    "温和型": {
        "features": ["眼睛小", "嘴唇厚", "下巴圆", "眉毛稀疏"],
        "analysis": "性格温和，重感情，适合服务型工作"
    }
}


def search_features(query: str) -> list:
    """搜索匹配的面相特征"""
    results = []
    query_lower = query.lower()
    
    for feature, info in FACE_KNOWLEDGE.items():
        if query_lower in feature.lower() or any(tag in query_lower for tag in info["tags"]):
            results.append({
                "feature": feature,
                "category": info["category"],
                "meaning": info["meaning"],
                "tags": info["tags"]
            })
    
    return results


def analyze_multiple_features(features: list) -> dict:
    """分析多个特征的组合"""
    analysis = {
        "features": [],
        "categories": {},
        "combo_type": None,
        "suggestions": []
    }
    
    # 分析每个特征
    for feature in features:
        results = search_features(feature)
        if results:
            analysis["features"].extend(results)
            for result in results:
                cat = result["category"]
                if cat not in analysis["categories"]:
                    analysis["categories"][cat] = []
                analysis["categories"][cat].append(result["meaning"])
    
    # 匹配组合类型
    for combo_name, combo_info in COMBO_ANALYSIS.items():
        match_count = sum(1 for f in features if any(f in cf for cf in combo_info["features"]))
        if match_count >= 2:
            analysis["combo_type"] = combo_name
            analysis["combo_analysis"] = combo_info["analysis"]
            break
    
    # 生成建议
    if "财运" in str(analysis["categories"]):
        analysis["suggestions"].append("财运不错，建议做好理财规划")
    if "事业" in str(analysis["categories"]):
        analysis["suggestions"].append("事业心强，注意平衡工作与生活")
    if "健康" in str(analysis["categories"]):
        analysis["suggestions"].append("注意身体健康，适当休息")
    
    return analysis


def generate_report(analysis: dict) -> str:
    """生成分析报告"""
    report = []
    report.append("👤 面相分析报告\n")
    report.append("=" * 50 + "\n")
    
    # 特征分析
    if analysis["features"]:
        report.append("📋 特征分析:\n")
        for item in analysis["features"]:
            report.append(f"  • {item['feature']} ({item['category']})")
            report.append(f"    含义：{item['meaning']}\n")
    
    # 宫位汇总
    if analysis["categories"]:
        report.append("🏛️ 宫位汇总:\n")
        for category, meanings in analysis["categories"].items():
            report.append(f"  {category}:")
            for meaning in meanings:
                report.append(f"    - {meaning}")
        report.append("")
    
    # 组合类型
    if analysis["combo_type"]:
        report.append(f"🎯 面相类型：{analysis['combo_type']}\n")
        report.append(f"   {analysis['combo_analysis']}\n")
    
    # 建议
    if analysis["suggestions"]:
        report.append("💡 建议:\n")
        for suggestion in analysis["suggestions"]:
            report.append(f"  • {suggestion}\n")
    
    report.append("=" * 50 + "\n")
    report.append("⚠️ 免责声明：本分析仅供娱乐参考，不具备科学依据")
    
    return "\n".join(report)


def print_template():
    """打印分析模板"""
    template = """
# 📝 面相分析模板

## 一、基本信息
- 分析对象：
- 分析日期：
- 分析目的：

## 二、三停分析
- 上停（额头）：[高/中/低] [饱满/标准/凹陷]
- 中停（眉眼鼻）：[长/中/短] [饱满/标准/凹陷]
- 下停（嘴下巴）：[长/中/短] [饱满/标准/凹陷]

## 三、五官分析
### 1. 眉毛（兄弟宫）
特征：
解读：

### 2. 眼睛（监察官）
特征：
解读：

### 3. 鼻子（财帛宫）
特征：
解读：

### 4. 嘴巴（出纳官）
特征：
解读：

### 5. 耳朵（采听官）
特征：
解读：

## 四、十二宫位速评
| 宫位 | 特征 | 解读 |
|------|------|------|
| 命宫 | | |
| 财帛宫 | | |
| 官禄宫 | | |
| 夫妻宫 | | |

## 五、综合分析
### 优势特征
1.
2.
3.

### 需注意特征
1.
2.
3.

## 六、建议
1.
2.
3.

---
*分析仅供参考，娱乐为主*
"""
    print(template)


def main():
    if len(sys.argv) < 2:
        print("👤 面相学分析工具 v1.0")
        print("\n使用方法:")
        print("  python analyze.py \"特征描述\"")
        print("  python analyze.py \"特征 1 特征 2 特征 3\"")
        print("  python analyze.py --template")
        print("\n示例:")
        print("  python analyze.py \"鼻子高挺\"")
        print("  python analyze.py \"眉毛浓密 眼睛大\"")
        print("  python analyze.py --template")
        print("\n可用特征关键词:")
        print("  鼻子：高挺、塌陷、鼻头有肉、鼻翼饱满")
        print("  眉毛：浓密、稀疏、整齐、杂乱")
        print("  眼睛：大、小、有神、无神")
        print("  嘴巴：大、小、嘴唇厚、嘴唇薄")
        print("  额头：高、低、饱满、凹陷")
        print("  下巴：方圆、尖、短、双下巴")
        sys.exit(0)
    
    if "--template" in sys.argv:
        print_template()
        sys.exit(0)
    
    query = " ".join(sys.argv[1:])
    features = query.split()
    
    if len(features) == 1:
        # 单个特征查询
        results = search_features(query)
        if results:
            print(f"🔍 查询：{query}\n")
            for result in results:
                print(f"📍 宫位：{result['category']}")
                print(f"💡 含义：{result['meaning']}")
                print(f"🏷️ 标签：{', '.join(result['tags'])}")
                print()
        else:
            print(f"❌ 未找到匹配的特征：{query}")
            print("\n提示：尝试使用以下关键词")
            print("  鼻子、眉毛、眼睛、嘴巴、耳朵、额头、下巴")
    else:
        # 多个特征分析
        analysis = analyze_multiple_features(features)
        report = generate_report(analysis)
        print(report)


if __name__ == "__main__":
    main()
