#!/usr/bin/env python3
"""
保险需求分析工具
输入：客户基本信息（年龄、职业、家庭结构、已有保单、预算）
输出：结构化需求分析报告

🆕 2026-10-27 计算口径修正（收入/预算）
   修复 SDI-4：原实现把"年收入 15%/10%"的百分比实际套在 annual_budget 上，
   注释与口径自相矛盾（收入 20 万 / 预算 2 万时报 3000 与 2000）。
   现改为：百分比按 **年收入** 计算，再与用户给出的年度预算取较小值。
       income_ceiling  = annual_income * 0.15
       ideal_premium   = min(income_ceiling, annual_budget)
       essential_premium = min(annual_income * 0.10, annual_budget)
   保费计算公式、风险评分、保障缺口算法均未改动。
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


def _validate_financial_inputs(params):
    """🆕 2026-10-30 SDI-4：校验财务输入为非负数。

    审计要求：“validate financial inputs as nonnegative numbers”。
    负数收入/支出/预算会让保障缺口、预算建议算出无意义的负值或虚高的上限，
    在保险建议场景里会直接误导投保决策。

    Raises:
        ValueError: 输入非法（非数值 / 负数）
    """
    numeric_fields = (
        "annual_income",
        "annual_expense",
        "annual_budget",
        "mortgage_balance",
    )
    for field in numeric_fields:
        if field not in params:
            continue
        value = params[field]
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} 必须是数值，收到：{value!r}")
        if value < 0:
            raise ValueError(f"{field} 不能为负数，收到：{value}")

    age = params.get("age")
    if age is not None and (isinstance(age, bool) or not isinstance(age, (int, float))):
        raise ValueError(f"age 必须是数值，收到：{age!r}")
    if age is not None and not (0 <= age <= 120):
        raise ValueError(f"age 超出合理范围（0-120），收到：{age}")
    return params


def analyze_needs(age, gender, occupation, has_family, family_members,
                  has_child, child_age, has_house_mortgage, mortgage_balance,
                  annual_income, annual_expense, existing_coverage, annual_budget):
    """综合需求分析"""
    # 🆕 2026-10-30 SDI-4：入口处校验财务输入（直接调用本函数时同样受保护）
    _validate_financial_inputs({
        "age": age,
        "annual_income": annual_income,
        "annual_expense": annual_expense,
        "annual_budget": annual_budget,
        "mortgage_balance": mortgage_balance,
    })

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

    # 预算规划（口径修正：百分比按年收入计算，再与年度预算取较小值）
    income_ceiling = annual_income * 0.15      # 收入基准：年保费不超过年收入 15%
    essential_ceiling = annual_income * 0.10  # 收入基准：基础保障约占年收入 10%
    budget_cap = annual_budget                 # 用户给出的年度预算上限
    ideal_premium = min(income_ceiling, budget_cap)
    essential_premium = min(essential_ceiling, budget_cap)

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
            "建议保费预算": round(ideal_premium, 2),
            "最低保费预算": round(essential_premium, 2),
            "可用预算": annual_budget,
            "收入基准_年保费上限": round(income_ceiling, 2),
            "预算上限": budget_cap,
            "计算口径": "百分比按年收入计算，再与年度预算取较小值",
            "说明": "保障型保费建议不超过年收入 15%（按年收入计算），同时不超过用户给出的年度预算；"
                    "基础保障（寿险+重疾+医疗+意外）约占年收入 10%。"
                    "⚠️ 上述百分比是【规划指引】，不是普适最低值：家庭结构、负债、社保状态、"
                    "已有保单差异很大，实际以用户给出的年度预算与自身情况为准；"
                    "预算不足以覆盖基础保障时，应明示保障缺口而不是硬凑方案"
        },
        "summary": f"{age}岁{'已婚' if has_family else '未婚'}{'有子女' if has_child else ''}，{'家庭经济支柱' if has_family else '个人'}，{'有房贷压力' if has_house_mortgage else '无房贷'}。" \
                   f"建议优先配置：{' '.join([p['type'] for p in priority_list[:2]])}。"
    }

    return result


# 示例档案（仅在 stdin 未提供输入时作为演示数据打印，并明确标注来源）
EXAMPLE_PROFILE = {
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


def _read_stdin_text():
    """读取 stdin 文本；TTY（无管道输入）返回空串。"""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return ""
        return sys.stdin.read() or ""
    except Exception:
        return ""


def main():
    raw = _read_stdin_text().strip()
    if not raw:
        # 未提供输入：明确标注示例数据，不静默把示例档案当作正式结果
        sys.stderr.write("⚠️ 未提供输入，以下为示例数据（示例档案，非真实客户数据）：\n")
        sys.stderr.write(json.dumps(EXAMPLE_PROFILE, ensure_ascii=False, indent=2) + "\n")
        params = EXAMPLE_PROFILE
    else:
        try:
            params = json.loads(raw)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            return 0
    try:
        _validate_financial_inputs(params)
    except ValueError as e:
        # 🆕 2026-10-30 SDI-4：财务输入非法 → 明确报错，不出看似正常的错误建议
        print(json.dumps({"error": f"输入校验失败：{e}"}, ensure_ascii=False))
        return 0
    try:
        result = analyze_needs(**params)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
