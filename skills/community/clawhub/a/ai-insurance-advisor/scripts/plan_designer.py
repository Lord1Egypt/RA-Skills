#!/usr/bin/env python3
"""
方案设计工具
根据需求分析结果，自动生成2-3套方案（基础版/标准版/全面版）
"""

import json
import sys
import os

def load_products():
    """加载产品数据"""
    product_file = os.path.join(os.path.dirname(__file__), "../references/products.json")
    with open(product_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["products"]

def select_products(products, product_type, criteria="recommended"):
    """按类型筛选产品"""
    filtered = [p for p in products if p["type"] == product_type]
    if not filtered:
        return []
    # 按保费排序（性价比）
    if criteria == "cheapest":
        return sorted(filtered, key=lambda x: x.get("premium_per_10k", 999))
    elif criteria == "recommended":
        # 推荐中等价位产品
        return sorted(filtered, key=lambda x: x.get("premium_per_10k", 999))
    return filtered

def design_plan(plan_type, age, gender, annual_income, annual_budget, coverage_needs):
    """设计保险方案"""
    products = load_products()

    if plan_type == "基础版":
        return design_basic_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    elif plan_type == "标准版":
        return design_standard_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    elif plan_type == "全面版":
        return design_premium_plan(age, gender, annual_income, annual_budget, coverage_needs, products)
    else:
        return None


def calculate_product_premium(product, age, gender, coverage, payment_term):
    """计算产品保费"""
    age_factor = 1.0
    if age >= 18 and age <= 30:
        age_factor = 0.8
    elif age >= 31 and age <= 40:
        age_factor = 1.0
    elif age >= 41 and age <= 50:
        age_factor = 1.3
    elif age >= 51 and age <= 55:
        age_factor = 1.6

    gender_factor = 1.0 if gender in ["男", "男性"] else 0.85

    if product["type"] == "医疗险":
        if age <= 30:
            return max(coverage * 0.0003, 200)
        elif age <= 40:
            return max(coverage * 0.0004, 200)
        elif age <= 50:
            return max(coverage * 0.0006, 200)
        else:
            return max(coverage * 0.001, 200)

    if product["type"] == "意外险":
        return max(coverage * 0.001, 100)

    payment_factor = 1.0
    if payment_term == "趸交":
        payment_factor = 0.85
    elif payment_term == "3年":
        payment_factor = 0.95
    elif payment_term == "5年":
        payment_factor = 1.0
    elif payment_term == "10年":
        payment_factor = 1.05
    elif payment_term == "20年":
        payment_factor = 1.15

    base = (coverage / 10000) * product.get("premium_per_10k", 250)
    return round(base * age_factor * gender_factor * payment_factor, 2)


def design_basic_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """基础版方案：低保费基本保障"""
    budget = min(annual_budget * 0.10, annual_income * 0.10)  # 不超过年收入10%
    plan = {
        "plan_name": "基础版",
        "description": "以最低成本建立基础保障，覆盖核心风险",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 选择性价比高的
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    tl_product = min(tl_products, key=lambda x: x.get("premium_per_10k", 999))
    tl_coverage = min(coverage_needs.get("death", 500000), 1000000)
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    if plan["annual_premium"] + tl_premium <= budget:
        plan["products"].append({
            "type": "定期寿险",
            "product_name": tl_product["name"],
            "company": tl_product["company"],
            "coverage": tl_coverage,
            "annual_premium": tl_premium,
            "payment_term": "20年",
            "coverage_period": "至60周岁",
            "key_benefits": "身故/全残保障，保护家人"
        })
        plan["annual_premium"] += tl_premium
        plan["total_coverage"] += tl_coverage

    # 意外险
    ac_products = [p for p in products if p["type"] == "意外险"]
    ac_product = min(ac_products, key=lambda x: x.get("premium_per_10k", 999))
    ac_coverage = min(annual_income * 5, 3000000)
    ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
    if plan["annual_premium"] + ac_premium <= budget * 1.2:
        plan["products"].append({
            "type": "意外险",
            "product_name": ac_product["name"],
            "company": ac_product["company"],
            "coverage": ac_coverage,
            "annual_premium": ac_premium,
            "payment_term": "年交",
            "coverage_period": "1年",
            "key_benefits": "意外身故/伤残/医疗，100万保额仅需几百元"
        })
        plan["annual_premium"] += ac_premium
        plan["total_coverage"] += ac_coverage

    # 医疗险
    mi_products = [p for p in products if p["type"] == "医疗险" and "保证续保" in p.get("notes", "")]
    if not mi_products:
        mi_products = [p for p in products if p["type"] == "医疗险"]
    mi_product = mi_products[0] if mi_products else None
    if mi_product:
        mi_coverage = 2000000
        mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
        plan["products"].append({
            "type": "医疗险",
            "product_name": mi_product["name"],
            "company": mi_product["company"],
            "coverage": mi_coverage,
            "annual_premium": mi_premium,
            "payment_term": "年交",
            "coverage_period": "1年",
            "key_benefits": "百万医疗，不限社保，进口药/靶向药均可报销"
        })
        plan["annual_premium"] += mi_premium
        plan["total_coverage"] += mi_coverage

    plan["features"] = [
        "保费低廉，适合预算有限的年轻人",
        "核心保障：身故、意外、大病医疗",
        "定期寿险覆盖家庭责任最重时期",
        "医疗险补充社保不足"
    ]

    return plan


def design_standard_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """标准版方案：全面基础保障+重疾"""
    budget = min(annual_budget * 0.15, annual_income * 0.15)
    plan = {
        "plan_name": "标准版",
        "description": "保障全面，含重疾保障，适合大多数家庭",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 推荐中国人寿星Combo
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    tl_product = next((p for p in tl_products if "星" in p["name"]), tl_products[0])
    tl_coverage = min(coverage_needs.get("death", 1000000), 2000000)
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    plan["products"].append({
        "type": "定期寿险",
        "product_name": tl_product["name"],
        "company": tl_product["company"],
        "coverage": tl_coverage,
        "annual_premium": tl_premium,
        "payment_term": "20年",
        "coverage_period": "至60周岁",
        "key_benefits": "身故/全残保障，保费低保障高"
    })
    plan["annual_premium"] += tl_premium
    plan["total_coverage"] += tl_coverage

    # 重疾险 - 推荐平安福或国寿福
    crx_products = [p for p in products if p["type"] == "重疾险"]
    crx_product = next((p for p in crx_products if "福" in p["name"] and "终身" in p["coverage_period"]), crx_products[0])
    crx_coverage = min(coverage_needs.get("critical_illness", annual_income * 3), 500000)
    crx_premium = calculate_product_premium(crx_product, age, gender, crx_coverage, "20年")
    plan["products"].append({
        "type": "重疾险",
        "product_name": crx_product["name"],
        "company": crx_product["company"],
        "coverage": crx_coverage,
        "annual_premium": crx_premium,
        "payment_term": "20年",
        "coverage_period": "终身",
        "key_benefits": f"120种重疾+轻症保障，确诊即赔付{crx_coverage//10000}万"
    })
    plan["annual_premium"] += crx_premium
    plan["total_coverage"] += crx_coverage

    # 医疗险 - 选保证续保20年的
    mi_products = [p for p in products if p["type"] == "医疗险" and "20年" in p.get("coverage_period", "")]
    if not mi_products:
        mi_products = [p for p in products if p["type"] == "医疗险"]
    mi_product = mi_products[0]
    mi_coverage = 4000000
    mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
    plan["products"].append({
        "type": "医疗险",
        "product_name": mi_product["name"],
        "company": mi_product["company"],
        "coverage": mi_coverage,
        "annual_premium": mi_premium,
        "payment_term": "年交",
        "coverage_period": "保证续保20年",
        "key_benefits": "长期医疗保障，20年续保稳定"
    })
    plan["annual_premium"] += mi_premium
    plan["total_coverage"] += mi_coverage

    # 意外险
    ac_products = [p for p in products if p["type"] == "意外险"]
    ac_product = next((p for p in ac_products if "百万" in p["name"]), ac_products[0])
    ac_coverage = min(annual_income * 5, 3000000)
    ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
    plan["products"].append({
        "type": "意外险",
        "product_name": ac_product["name"],
        "company": ac_product["company"],
        "coverage": ac_coverage,
        "annual_premium": ac_premium,
        "payment_term": "年交",
        "coverage_period": "1年",
        "key_benefits": "含猝死保障，意外医疗不限社保"
    })
    plan["annual_premium"] += ac_premium
    plan["total_coverage"] += ac_coverage

    plan["features"] = [
        "保障全面：寿险+重疾+医疗+意外",
        "重疾险提供终身保障，确诊即赔付",
        "医疗险保证续保20年，长期稳定",
        "定期寿险覆盖家庭经济责任期",
        "总保费约占年收入的10-15%"
    ]

    return plan


def design_premium_plan(age, gender, annual_income, annual_budget, coverage_needs, products):
    """全面版方案：高保额全面保障+储蓄"""
    budget = min(annual_budget * 0.20, annual_income * 0.20)
    plan = {
        "plan_name": "全面版",
        "description": "高保额全方位保障，另含养老储蓄规划",
        "annual_premium": 0,
        "total_coverage": 0,
        "products": []
    }

    # 定期寿险 - 高保额
    tl_products = [p for p in products if p["type"] == "定期寿险"]
    tl_product = tl_products[0]
    tl_coverage = min(coverage_needs.get("death", 2000000), 5000000)
    tl_premium = calculate_product_premium(tl_product, age, gender, tl_coverage, "20年")
    plan["products"].append({
        "type": "定期寿险",
        "product_name": tl_product["name"],
        "company": tl_product["company"],
        "coverage": tl_coverage,
        "annual_premium": tl_premium,
        "payment_term": "20年",
        "coverage_period": "至60/65周岁",
        "key_benefits": f"高保额{tl_coverage//10000}万，覆盖所有家庭责任"
    })
    plan["annual_premium"] += tl_premium
    plan["total_coverage"] += tl_coverage

    # 重疾险 - 多次赔付型
    crx_products = [p for p in products if p["type"] == "重疾险" and "多次" in p.get("core_coverage", "")]
    if not crx_products:
        crx_products = [p for p in products if p["type"] == "重疾险"]
    crx_product = crx_products[0]
    crx_coverage = min(coverage_needs.get("critical_illness", annual_income * 5), 500000)
    crx_premium = calculate_product_premium(crx_product, age, gender, crx_coverage, "20年")
    plan["products"].append({
        "type": "重疾险",
        "product_name": crx_product["name"],
        "company": crx_product["company"],
        "coverage": crx_coverage,
        "annual_premium": crx_premium,
        "payment_term": "20年",
        "coverage_period": "终身",
        "key_benefits": f"重疾多次赔付，终身保障，保额{crx_coverage//10000}万"
    })
    plan["annual_premium"] += crx_premium
    plan["total_coverage"] += crx_coverage

    # 医疗险 - 600万高保额
    mi_products = [p for p in products if p["type"] == "医疗险"]
    mi_product = next((p for p in mi_products if "600" in p.get("core_coverage", "")), mi_products[0])
    mi_coverage = 6000000
    mi_premium = calculate_product_premium(mi_product, age, gender, mi_coverage, "年交")
    plan["products"].append({
        "type": "医疗险",
        "product_name": mi_product["name"],
        "company": mi_product["company"],
        "coverage": mi_coverage,
        "annual_premium": mi_premium,
        "payment_term": "年交",
        "coverage_period": "1年可续保",
        "key_benefits": "600万高保额，含质子重离子、CAR-T治疗"
    })
    plan["annual_premium"] += mi_premium
    plan["total_coverage"] += mi_coverage

    # 意外险 - 100万
    ac_products = [p for p in products if p["type"] == "意外险"]
    ac_product = next((p for p in ac_products if "百万" in p["name"]), ac_products[0])
    ac_coverage = 1000000
    ac_premium = calculate_product_premium(ac_product, age, gender, ac_coverage, "年交")
    plan["products"].append({
        "type": "意外险",
        "product_name": ac_product["name"],
        "company": ac_product["company"],
        "coverage": ac_coverage,
        "annual_premium": ac_premium,
        "payment_term": "年交",
        "coverage_period": "1年",
        "key_benefits": "100万意外+猝死保障，意外医疗不限社保"
    })
    plan["annual_premium"] += ac_premium
    plan["total_coverage"] += ac_coverage

    # 储蓄险 - 养老规划（可选）
    if age <= 45:
        sa_products = [p for p in products if p["type"] == "储蓄险" and "养老" in p.get("notes", "")]
        if not sa_products:
            sa_products = [p for p in products if p["type"] == "储蓄险"]
        if sa_products and plan["annual_premium"] + 10000 <= budget:
            sa_product = sa_products[0]
            sa_coverage = 100000
            sa_premium = calculate_product_premium(sa_product, age, gender, sa_coverage, "10年")
            plan["products"].append({
                "type": "储蓄险",
                "product_name": sa_product["name"],
                "company": sa_product["company"],
                "coverage": sa_coverage,
                "annual_premium": sa_premium,
                "payment_term": "10年",
                "coverage_period": "至60/65周岁",
                "key_benefits": "强制储蓄，养老规划，兼具保障和收益"
            })
            plan["annual_premium"] += sa_premium

    plan["features"] = [
        "全方位高保额保障：寿险+重疾+医疗+意外",
        "重疾险保额高达年收入5倍",
        "医疗险600万保额，涵盖最新治疗手段",
        "定期寿险高保额，覆盖所有家庭财务责任",
        "可选储蓄险，为养老做准备",
        f"总保费约{plan['annual_premium']}元，占年收入约{round(plan['annual_premium']/annual_income*100,1)}%"
    ]

    return plan


def generate_all_plans(age, gender, annual_income, annual_budget, coverage_needs):
    """生成三套方案"""
    plans = {
        "基础版": design_plan("基础版", age, gender, annual_income, annual_budget, coverage_needs),
        "标准版": design_plan("标准版", age, gender, annual_income, annual_budget, coverage_needs),
        "全面版": design_plan("全面版", age, gender, annual_income, annual_budget, coverage_needs)
    }

    return plans


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 默认测试
        coverage_needs = {
            "death": 2000000,
            "critical_illness": 1500000,
            "hospital": 4000000
        }
        plans = generate_all_plans(35, "男", 500000, 500000, coverage_needs)
        print(json.dumps(plans, ensure_ascii=False, indent=2))
    else:
        try:
            params = json.loads(sys.stdin.read())
            plans = generate_all_plans(
                params.get("age", 35),
                params.get("gender", "男"),
                params.get("annual_income", 500000),
                params.get("annual_budget", 500000),
                params.get("coverage_needs", {})
            )
            print(json.dumps(plans, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
