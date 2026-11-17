"""ecommerce-pricing-strategy Skill exec脚本 v1.0 (A16 电商定价策略)
来源: 01手册§十二 A16 电商定价策略(定价模型+利润优化+大促定价+多平台定价)
独立性: 本脚本为独立定价策略规划,不修改price-dynamic Skill
规则: 四模型(成本加成/竞争导向/价值定价/渗透定价) / 毛利率>=30%(警戒20%/危险<20%)
      大促公式(到手价=原价×折扣-券-补贴) / 预售定金10-20%翻倍抵扣 / 价保15-30天
      多平台定价(闲鱼×1.1-1.3/抖音×1.5-2.5/淘宝×1.8-3.0/拼多多×1.2-1.6/京东×2.0-3.5/快手×1.3-2.0)
用法: python ecommerce_pricing.py --cost 30 --competitor-prices "35,40,45,50" --platform taobao --action strategy
返回: stdout JSON {success, data:{suggested_price, profit_margin, strategy, promotion_plan}, error, code}
"""
import argparse, json, sys
from pathlib import Path as _Path
from typing import Any
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("_lazy", source="skills/_lazy/ecommerce-pricing-strategy/scripts/ecommerce_pricing.py")

MARKUP_RATES = {"虚拟商品": (0.5, 2.0), "数码3C": (0.1, 0.25), "服饰鞋包": (0.4, 0.8),
                "美妆护肤": (0.5, 1.0), "食品生鲜": (0.2, 0.4), "家居日用": (0.3, 0.6)}
PLATFORM_MULTIPLIER = {"xianyu": (1.1, 1.3), "douyin": (1.5, 2.5), "taobao": (1.8, 3.0),
                       "pdd": (1.2, 1.6), "jd": (2.0, 3.5), "kuaishou": (1.3, 2.0)}
BUNDLE_STRATEGIES = {"买A送B": "套餐价=A价,送关联品B(清库存/关联销售)",
                     "A+B套餐": "套餐价=(A+B)×0.85,提升客单价15-25%",
                     "阶梯满减": "满99减10/满199减30/满299减60(门槛=客单价×1.3-1.5)",
                     "第二件半价": "均价=首件×0.75,快速走量"}
METRICS = {"毛利率": ">=30%", "客单价": "因品类而异", "价格弹性": "销量变化率/价格变化率", "转化率": ">=3%", "利润率": ">=15%"}


def _parse_competitors(prices_str):
    """解析竞品价格字符串"""
    if not prices_str:
        return []
    try:
        return [float(x.strip()) for x in prices_str.split(",") if x.strip()]
    except ValueError:
        return []


def _calc_margin(price, cost):
    """计算毛利率"""
    if price <= 0:
        return "0%"
    margin = (price - cost) / price * 100
    return f"{margin:.1f}%"


def _select_model(cost, competitors):
    """选择定价模型"""
    if competitors and len(competitors) >= 2:
        comp_avg = sum(competitors) / len(competitors)
        return "竞争导向法", round(comp_avg, 2), comp_avg
    return "成本加成法", round(cost * 1.6, 2), cost * 1.6


def _promotion_plan(cost, competitors, platform):
    """大促定价方案"""
    comp_avg = sum(competitors) / len(competitors) if competitors else cost * 2
    original_price = round(comp_avg, 2)
    discount_rate = 0.75
    platform_coupon = original_price * 0.10
    store_coupon = original_price * 0.05
    subsidy = original_price * 0.03
    final_price = round(original_price * discount_rate - platform_coupon - store_coupon - subsidy, 2)
    deposit = round(original_price * 0.15, 2)
    return {
        "model": "大促定价公式: 到手价=原价×折扣-平台券-店铺券-补贴",
        "original_price": original_price,
        "discount_rate": f"{discount_rate*100:.0f}折",
        "final_price": final_price,
        "breakdown": {"平台券": round(platform_coupon, 2), "店铺券": round(store_coupon, 2), "补贴": round(subsidy, 2)},
        "presale": {"定金": deposit, "定金翻倍": round(deposit * 2, 2), "尾款": round(original_price - deposit * 2, 2)},
        "price_protection": "价保15-30天,买贵退差价(预估2-5%订单需退差)",
    }


def run(cost: Any, competitor_prices: Any, platform: Any, action: Any) -> dict[str, Any]:
    """运行

    Args:
        cost (Any): 参数说明
        competitor_prices (Any): 参数说明
        platform (Any): 参数说明
        action (Any): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    if not isinstance(cost, (int, float)) or cost <= 0:
        return {"success": False, "data": {}, "error": "cost应为正数", "code": "INVALID_INPUT"}
    if platform not in PLATFORM_MULTIPLIER:
        return {"success": False, "data": {}, "error": f"platform无效,可选: {','.join(PLATFORM_MULTIPLIER.keys())}", "code": "INVALID_PLATFORM"}
    if action not in {"strategy", "promotion", "bundle"}:
        return {"success": False, "data": {}, "error": "action无效,可选: strategy/promotion/bundle", "code": "INVALID_ACTION"}
    competitors = _parse_competitors(competitor_prices)
    model, suggested, model_base = _select_model(cost, competitors)
    margin = _calc_margin(suggested, cost)
    mult_range = PLATFORM_MULTIPLIER[platform]
    platform_low = round(cost * mult_range[0], 2)
    platform_high = round(cost * mult_range[1], 2)
    if action == "promotion":
        promo = _promotion_plan(cost, competitors, platform)
        return {"success": True, "data": {"suggested_price": suggested, "profit_margin": margin,
                "strategy": f"大促定价({promo['model']})", "promotion_plan": promo, "metrics": METRICS}, "error": None, "code": None}
    if action == "bundle":
        return {"success": True, "data": {"suggested_price": suggested, "profit_margin": margin,
                "strategy": "捆绑销售+满减策略", "promotion_plan": {"bundle_strategies": BUNDLE_STRATEGIES,
                "满减设计": "门槛=客单价×1.3-1.5,力度=门槛×10-15%,层级2-3级"}, "metrics": METRICS}, "error": None, "code": None}
    strategy = (f"{model}(建议价{suggested}元)+{platform}平台定价区间({platform_low}-{platform_high})"
                f"+毛利率目标>=30%(当前{margin})+动态调价(库存/销量/竞品三维度)+捆绑销售+满减策略")
    return {"success": True, "data": {"suggested_price": suggested, "profit_margin": margin,
            "strategy": strategy, "promotion_plan": {"model": model, "competitor_avg": round(model_base, 2) if competitors else None,
            "cost_plus_price": round(cost * 1.6, 2), "platform_range": f"{platform_low}-{platform_high}",
            "competitors": competitors, "markup_rates": MARKUP_RATES, "bundle_strategies": BUNDLE_STRATEGIES},
            "metrics": METRICS}, "error": None, "code": None}


def main():
    """main"""
    parser = argparse.ArgumentParser(description="电商定价策略生成器(A16)")
    parser.add_argument("--cost", type=float, required=True, help="商品成本价")
    parser.add_argument("--competitor-prices", default="", help="竞品价格,逗号分隔,如35,40,45,50")
    parser.add_argument("--platform", default="taobao", choices=list(PLATFORM_MULTIPLIER.keys()), help="目标平台")
    parser.add_argument("--action", default="strategy", choices=["strategy", "promotion", "bundle"], help="操作类型")
    args = parser.parse_args()
    try:
        result = run(args.cost, args.competitor_prices, args.platform, args.action)
        sys.stdout.write(json.dumps(result, ensure_ascii=False)); sys.stdout.flush()
        logger.info(f"ecommerce-pricing action={args.action} cost={args.cost} platform={args.platform} success={result.get('success')}")
        sys.exit(0 if result.get("success") else 1)
    except ValueError as e:
        logger.error(f"ecommerce-pricing ValueError: {e}")
        sys.stdout.write(json.dumps({"success": False, "data": {}, "error": str(e)[:300], "code": "VALUE_ERROR"})); sys.stdout.flush(); sys.exit(1)
    except Exception as e:
        logger.error(f"ecommerce-pricing异常: {e}", exc_info=True)
        sys.stdout.write(json.dumps({"success": False, "data": {}, "error": str(e)[:300], "code": "RUNTIME_ERROR"})); sys.stdout.flush(); sys.exit(2)


if __name__ == "__main__":
    main()
