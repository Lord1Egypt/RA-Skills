#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
赤脚医生诊断辅助脚本

功能：
1. 症状分析与鉴别诊断
2. 病情严重程度评估
3. 中医辨证辅助

用法：
    python diagnose.py --symptoms "咳嗽,发热,头痛" --duration "3天" --age 35 --gender male
"""

import argparse
import json
import sys

# 症状与疾病关联数据库
SYMPTOM_DISEASE_MAP = {
    # 呼吸系统症状
    "咳嗽": {
        "常见疾病": ["感冒", "支气管炎", "肺炎", "肺结核"],
        "中医辨证": ["风寒犯肺", "风热犯肺", "痰湿阻肺", "肺阴虚"],
        "伴随症状询问": ["发热", "咳痰", "胸痛", "呼吸困难"]
    },
    "发热": {
        "常见疾病": ["感冒", "流感", "肺炎", "肺结核", "伤寒", "败血症"],
        "中医辨证": ["外感风寒", "外感风热", "湿热", "阴虚发热"],
        "伴随症状询问": ["畏寒", "出汗", "头痛", "咽痛"]
    },
    "胸痛": {
        "常见疾病": ["胸膜炎", "肺炎", "心绞痛", "肋间神经痛"],
        "中医辨证": ["气滞血瘀", "痰瘀互结"],
        "伴随症状询问": ["咳嗽", "呼吸困难", "心悸", "发热"]
    },
    
    # 消化系统症状
    "呕吐": {
        "常见疾病": ["胃炎", "食物中毒", "肠梗阻", "脑膜炎"],
        "中医辨证": ["胃寒", "胃热", "食积", "肝胃不和"],
        "伴随症状询问": ["腹泻", "腹痛", "发热", "头痛"]
    },
    "腹泻": {
        "常见疾病": ["急性肠炎", "痢疾", "食物中毒", "肠结核"],
        "中医辨证": ["寒湿", "湿热", "脾虚", "肾虚"],
        "伴随症状询问": ["发热", "腹痛", "脓血便", "脱水症状"]
    },
    "腹痛": {
        "常见疾病": ["急性阑尾炎", "胃肠炎", "胆石症", "胰腺炎", "肠梗阻"],
        "中医辨证": ["寒邪客胃", "湿热中阻", "食积", "气滞"],
        "伴随症状询问": ["呕吐", "腹泻", "发热", "腹胀"]
    },
    "黄疸": {
        "常见疾病": ["肝炎", "胆石症", "胆管炎", "溶血性疾病"],
        "中医辨证": ["阳黄（湿热）", "阴黄（寒湿）"],
        "伴随症状询问": ["发热", "腹痛", "尿色", "大便颜色"]
    },
    
    # 泌尿系统症状
    "血尿": {
        "常见疾病": ["泌尿系感染", "泌尿系结石", "肾炎", "肿瘤"],
        "中医辨证": ["下焦热盛", "阴虚火旺", "脾肾亏虚"],
        "伴随症状询问": ["尿频", "尿急", "尿痛", "腰痛"]
    },
    "水肿": {
        "常见疾病": ["心力衰竭", "肝硬化", "肾病综合征", "营养不良"],
        "中医辨证": ["阳水（风水泛滥）", "阴水（脾肾阳虚）"],
        "伴随症状询问": ["呼吸困难", "腹胀", "尿量", "心悸"]
    },
    
    # 神经系统症状
    "头痛": {
        "常见疾病": ["感冒", "高血压", "偏头痛", "脑膜炎", "脑血管病"],
        "中医辨证": ["外感头痛", "肝阳头痛", "血虚头痛", "瘀血头痛"],
        "伴随症状询问": ["发热", "恶心呕吐", "视力改变", "血压"]
    },
    "眩晕": {
        "常见疾病": ["高血压", "低血压", "贫血", "颈椎病", "美尼尔病"],
        "中医辨证": ["肝阳上亢", "气血亏虚", "肾精不足", "痰湿中阻"],
        "伴随症状询问": ["耳鸣", "恶心", "行走不稳", "血压"]
    },
    "昏迷": {
        "常见疾病": ["脑卒中", "糖尿病昏迷", "肝昏迷", "中毒"],
        "中医辨证": ["闭证", "脱证"],
        "伴随症状询问": ["发热", "瞳孔", "呼吸", "血压"]
    },
    
    # 其他症状
    "便血": {
        "常见疾病": ["痔疮", "痢疾", "肠息肉", "结肠癌", "上消化道出血"],
        "中医辨证": ["肠道湿热", "脾胃虚寒", "气虚不摄"],
        "伴随症状询问": ["腹痛", "大便性状", "贫血症状"]
    }
}

# 急症识别关键词
EMERGENCY_KEYWORDS = [
    "昏迷", "休克", "呼吸困难", "胸痛持续", "剧烈头痛",
    "呕血", "便血大量", "高热惊厥", "中毒", "溺水", "电击"
]

# 需要立即就医的症状
URGENT_SYMPTOMS = [
    "胸痛超过15分钟", "呼吸困难", "突然剧烈头痛", "意识障碍",
    "持续高热超过3天", "呕血", "黑便", "剧烈腹痛", "孕妇腹痛出血"
]


def analyze_symptoms(symptoms, duration, age, gender, pregnant=False):
    """
    分析症状，返回初步诊断建议
    """
    result = {
        "输入信息": {
            "症状": symptoms,
            "持续时间": duration,
            "年龄": age,
            "性别": gender,
            "是否怀孕": pregnant
        },
        "分析结果": {
            "严重程度": "mild",
            "可能诊断": [],
            "中医辨证": [],
            "需询问的伴随症状": [],
            "警示": [],
            "就医建议": []
        }
    }
    
    # 检查急症
    for symptom in symptoms:
        if symptom in EMERGENCY_KEYWORDS:
            result["分析结果"]["严重程度"] = "emergency"
            result["分析结果"]["警示"].append(f"⚠️ {symptom} 可能是急症，建议立即拨打 120 或就医")
    
    # 检查需紧急就医的症状
    urgent_found = False
    for urgent in URGENT_SYMPTOMS:
        if any(s in urgent for s in symptoms):
            if result["分析结果"]["严重程度"] not in ["emergency"]:
                result["分析结果"]["严重程度"] = "severe"
            urgent_found = True
            result["分析结果"]["就医建议"].append(f"建议尽快就医：{urgent}")
    
    # 症状分析
    for symptom in symptoms:
        if symptom in SYMPTOM_DISEASE_MAP:
            info = SYMPTOM_DISEASE_MAP[symptom]
            result["分析结果"]["可能诊断"].extend(info["常见疾病"])
            result["分析结果"]["中医辨证"].extend(info["中医辨证"])
            result["分析结果"]["需询问的伴随症状"].extend(info["伴随症状询问"])
    
    # 去重
    result["分析结果"]["可能诊断"] = list(set(result["分析结果"]["可能诊断"]))
    result["分析结果"]["中医辨证"] = list(set(result["分析结果"]["中医辨证"]))
    result["分析结果"]["需询问的伴随症状"] = list(set(result["分析结果"]["需询问的伴随症状"]))
    
    # 根据年龄和性别调整建议
    if age < 6 or age > 65:
        if result["分析结果"]["严重程度"] == "mild":
            result["分析结果"]["严重程度"] = "moderate"
        result["分析结果"]["就医建议"].append("儿童或老年人，建议密切观察，如有加重及时就医")
    
    if pregnant:
        result["分析结果"]["就医建议"].append("⚠️ 孕妇用药需特别谨慎，建议咨询产科医生")
        if "腹痛" in symptoms or "出血" in symptoms:
            result["分析结果"]["严重程度"] = "emergency"
            result["分析结果"]["警示"].append("⚠️ 孕妇腹痛或出血需立即就医")
    
    # 免责声明
    result["免责声明"] = "本分析仅供参考，不能替代专业医疗诊断。如有不适，请及时就医。"
    
    return result


def main():
    parser = argparse.ArgumentParser(description="赤脚医生诊断辅助工具")
    parser.add_argument("--symptoms", required=True, help="症状列表，逗号分隔")
    parser.add_argument("--duration", default="未知", help="症状持续时间")
    parser.add_argument("--age", type=int, default=30, help="年龄")
    parser.add_argument("--gender", choices=["male", "female"], default="male", help="性别")
    parser.add_argument("--pregnant", action="store_true", help="是否怀孕")
    
    args = parser.parse_args()
    
    symptoms = [s.strip() for s in args.symptoms.split(",")]
    
    result = analyze_symptoms(
        symptoms=symptoms,
        duration=args.duration,
        age=args.age,
        gender=args.gender,
        pregnant=args.pregnant
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
