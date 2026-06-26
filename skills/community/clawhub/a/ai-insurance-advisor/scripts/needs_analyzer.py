#!/usr/bin/env python3
"""
保险需求分析工具
输入：客户基本信息（年龄、职业、家庭结构、已有保单、预算）
输出：结构化需求分析报告
"""

import json
import sys

def analyze_risks(age, has_family, has_house_mortgage, existing_coverage, annual_income):
    """分析四大风险"""
    risks = {
        "death_risk": {
            "score": 0,
            "description": "",
            "recommendations": []
        },
        "critical_illness_risk": {
            "score": 0,
            "description": "",
            "recommendations": []
        },
        "accident_risk": {
            "score": 0,
            "description": "",
            "recommendations": []
        },
        "hospitalization_risk": {
            "score": 0,
            "description": "",
            "recommendations": []
        }
    }

    # 身故风险评分
    if has_family:
        risks["death_risk"]["score"] += 40
        risks["death_risk"]["recommendations"].append("定期寿险：覆盖家庭责任，保护家人")
    if has_house_mortgage:
        risks["death_risk"]["score"] += 30
        risks["death_risk"]["recommendations"].append(f"房贷险：保额建议覆盖剩余房贷余额")
    if age <= 50:
        risks["death_risk"]["score"] += 20
    if existing_coverage.get("定期寿险", 0) == 0:
        risks["death_risk"]["recommendations"].append("优先配置定期寿险，保费低保障高")

    # 大病风险评分
    risks["critical_illness_risk"]["score"] = 60 + (1 if age > 35 else 0) * 10 + (1 if age > 45 else 0) * 10
    risks["critical_illness_risk"]["recommendations"].append("重疾险：确诊即赔付，弥补收入损失")
    if existing_coverage.get("重疾险", 0) == 0:
        risks["critical_illness_risk"]["recommendations"].append("建议重疾险保额 = 年收入 × 3-5倍")

    # 意外风险评分
    risks["accident_risk"]["score"] = 40 + (1 if age < 40 else 0) * 20
    risks["accident_risk"]["recommendations"].append("意外险：保费低保障高，1年期消费型")
    if existing_coverage.get("意外险", 0) == 0:
        risks["accident_risk"]["recommendations"].append("意外险保额建议：年收入5-10倍")

    # 住院风险评分
    risks["hospitalization_risk"]["score"] = 50 + (1 if age > 30 else 0) * 10
    risks["hospitalization_risk"]["recommendations"].append("医疗险：报销高额医疗费用")
    if existing_coverage.get("医疗险", 0) == 0:
        risks["hospitalization_risk"]["recommendations"].append("优先选择保证续保的百万医疗险")

    # 生成描述
    for risk_name, risk_data in risks.items():
        if risk_data["score"] >= 80:
            risk_data["level"] = "极高"
        elif risk_data["score"] >= 60:
            risk_data["level"] = "高"
        elif risk_data["score"] >= 40:
            risk_data["level"] = "中等"
        else:
            risk_data["level"] = "较低"

    return risks


def analyze_needs(age, gender, occupation, has_family, family_members,
                  has_child, child_age, has_house_mortgage, mortgage_balance,
                  annual_income, annual_expense, existing_coverage, annual_budget):
    """综合需求分析"""

    # 风险分析
    risks = analyze_risks(age, has_family, has_house_mortgage, existing_coverage, annual_income)

    # 保障缺口计算
    death_coverage_needed = 0
    if has_family:
        death_coverage_needed += annual_expense * 10  # 10年家庭支出
    if has_child:
        death_coverage_needed += (22 - child_age) * 20000  # 子女教育费
    if has_house_mortgage:
        death_coverage_needed += mortgage_balance  # 房贷余额
    death_coverage_needed += 200000  # 父母赡养

    ci_coverage_needed = annual_income * 3  # 3年收入
    if age > 40:
        ci_coverage_needed = annual_income * 5  # 40岁以上建议5年收入

    hospital_coverage_needed = 2000000  # 200万医疗险

    # 优先级排序
    priority_list = []
    if existing_coverage.get("定期寿险", 0) < death_coverage_needed:
        priority_list.append({"type": "定期寿险", "priority": 1, "gap": death_coverage_needed - existing_coverage.get("定期寿险", 0)})
    if existing_coverage.get("重疾险", 0) < ci_coverage_needed:
        priority_list.append({"type": "重疾险", "priority": 2, "gap": ci_coverage_needed - existing_coverage.get("重疾险", 0)})
    if existing_coverage.get("医疗险", 0) == 0:
        priority_list.append({"type": "医疗险", "priority": 3, "gap": hospital_coverage_needed})
    if existing_coverage.get("意外险", 0) == 0:
        priority_list.append({"type": "意外险", "priority": 4, "gap": annual_income * 5})

    # 预算规划
    ideal_premium = annual_budget * 0.15  # 建议保费支出不超过年收入15%
    essential_premium = annual_budget * 0.10  # 最低10%

    result = {
        "customer_info": {
            "年龄": age,
            "性别": gender,
            "职业": occupation,
            "家庭结构": {
                "已婚": has_family,
                "家庭成员数": family_members,
                "子女": has_child,
                "子女年龄": child_age if has_child else None
            },
            "财务状况": {
                "年收入": annual_income,
                "年支出": annual_expense,
                "房贷余额": mortgage_balance if has_house_mortgage else 0
            },
            "已有保障": existing_coverage,
            "年度预算": annual_budget
        },
        "risk_analysis": risks,
        "coverage_gap": {
            "身故保障缺口": {
                "建议保额": death_coverage_needed,
                "现有保额": existing_coverage.get("定期寿险", 0),
                "保障缺口": max(0, death_coverage_needed - existing_coverage.get("定期寿险", 0))
            },
            "重疾保障缺口": {
                "建议保额": ci_coverage_needed,
                "现有保额": existing_coverage.get("重疾险", 0),
                "保障缺口": max(0, ci_coverage_needed - existing_coverage.get("重疾险", 0))
            },
            "医疗保障建议": {
                "建议保额": hospital_coverage_needed,
                "现有保额": existing_coverage.get("医疗险", 0),
                "保障缺口": max(0, hospital_coverage_needed - existing_coverage.get("医疗险", 0))
            },
            "意外保障建议": {
                "建议保额": annual_income * 5,
                "现有保额": existing_coverage.get("意外险", 0),
                "保障缺口": max(0, annual_income * 5 - existing_coverage.get("意外险", 0))
            }
        },
        "priority_list": priority_list,
        "budget_planning": {
            "建议保费预算": ideal_premium,
            "最低保费预算": essential_premium,
            "可用预算": annual_budget,
            "说明": "保障型保费建议不超过年收入15%，其中基础保障（寿险+重疾+医疗+意外）约占10%"
        },
        "summary": f"{age}岁{'已婚' if has_family else '未婚'}{'有子女' if has_child else ''}，{'家庭经济支柱' if has_family else '个人'}，{'有房贷压力' if has_house_mortgage else '无房贷'}。" \
                   f"建议优先配置：{' '.join([p['type'] for p in priority_list[:2]])}。"
    }

    return result


if __name__ == "__main__":
    # 默认测试数据
    if len(sys.argv) == 1:
        test_data = {
            "age": 35,
            "gender": "男",
            "occupation": "企业主",
            "has_family": True,
            "family_members": 4,
            "has_child": True,
            "child_age": 8,
            "has_house_mortgage": True,
            "mortgage_balance": 1500000,
            "annual_income": 500000,
            "annual_expense": 200000,
            "existing_coverage": {"重疾险": 0, "医疗险": 0, "定期寿险": 0, "意外险": 0},
            "annual_budget": 500000
        }
        result = analyze_needs(**test_data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 从stdin读取JSON参数
        try:
            import sys
            params = json.loads(sys.stdin.read())
            result = analyze_needs(**params)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
