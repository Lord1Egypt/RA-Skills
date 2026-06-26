#!/usr/bin/env python3
"""报价计算/验算脚本
Usage:
  python calculate.py --model YDV-75                              # 单型号快速报价
  python calculate.py --models YDV-75,YDV-D75 --quantity 2,1      # 多型号报价
  python calculate.py --model YDV-75 --with-accessories            # 含推荐后处理
  python calculate.py --validate "E:/path/to/quote.yaml"           # 验算已有报价单
"""

import argparse
import io
import os
import sys
import yaml

# UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(SKILL_DIR, "data", "products.yaml")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_product(data, model):
    for p in data["products"]:
        if p["model"] == model:
            return p
    return None


def find_accessories(data, model, accessory_type=None):
    """Find compatible accessories for a given model."""
    results = []
    for a in data["accessories"]:
        if model in a.get("compatible_with", []):
            if accessory_type is None or a["type"] == accessory_type:
                results.append(a)
    return results


def calc_discount(total_price_wan, rules):
    """Calculate discount based on tier rules."""
    for tier in rules["discount_tiers"]:
        if tier["min_total"] <= total_price_wan < tier["max_total"]:
            return total_price_wan * tier["discount_pct"] / 100, tier["discount_pct"]
    return 0, 0


def calc_freight(distance_km, rules):
    """Calculate freight cost."""
    freight_rules = rules["freight"]
    if distance_km <= freight_rules["included_km"]:
        return 0, f"距离 {distance_km}km，免运费"
    extra_km = distance_km - freight_rules["included_km"]
    fee = freight_rules["base_fee_wan"] + extra_km * freight_rules["per_km_rate_wan"]
    return fee, f"距离 {distance_km}km，超出 {extra_km}km"


def print_quote(models, quantities, distance_km=100, include_accessories=True,
                include_spares=False, extend_warranty=0):
    """Print formatted quotation."""
    data = load_data()
    rules = data["pricing_rules"]
    products = data["products"]
    accessories = data["accessories"]

    # Line items
    lines = []
    equipment_total = 0
    max_lead_time = 0

    for model, qty in zip(models, quantities):
        prod = find_product(data, model)
        if not prod:
            print(f"[ERROR] Unknown model: {model}")
            continue
        line_total = prod["price_exw"] * qty
        lines.append({
            "model": model,
            "name": prod.get("category", ""),
            "qty": qty,
            "unit_price": prod["price_exw"],
            "total": line_total,
        })
        equipment_total += line_total
        max_lead_time = max(max_lead_time, prod["lead_time_days"])

    # Accessories
    accessory_lines = []
    if include_accessories:
        seen_types = set()
        for model in models:
            accs = find_accessories(data, model)
            for a in accs:
                if a["id"] not in seen_types:
                    # Deduplicate: pick highest capacity if multiple models
                    seen_types.add(a["id"])
                    # Only add accessory once
                    a_line = {
                        "model": a["id"],
                        "name": a["type"],
                        "qty": 1,
                        "unit_price": a["price_exw"],
                        "total": a["price_exw"],
                    }
                    accessory_lines.append(a_line)
                    equipment_total += a["price_exw"]

    # Deduplicate accessories (keep highest capacity only)
    # For simplicity, just add recommended accessories
    all_lines = lines + accessory_lines

    # Discount
    discount_amount, discount_pct = calc_discount(equipment_total, rules)

    # Freight
    freight_amount, freight_note = calc_freight(distance_km, rules)

    # Installation
    install_rate = rules["installation"]["rate_pct"] / 100
    install_amount = max(
        (equipment_total - discount_amount) * install_rate,
        rules["installation"]["min_fee_wan"]
    )

    # Spare parts
    spare_amount = rules["spare_parts_kit"]["price_wan"] if include_spares else 0

    # Warranty extension
    warranty_amount = rules["warranty_extension"]["per_year_wan"] * extend_warranty

    # Totals
    after_discount = equipment_total - discount_amount
    subtotal = after_discount + freight_amount + install_amount + spare_amount + warranty_amount
    vat = subtotal * rules["tax"]["vat_rate"]
    grand_total = subtotal + vat

    # Print
    print()
    print("=" * 60)
    print("  萤火虫空压机 报价单 / Firefly Compressor Quotation")
    print("=" * 60)
    print()

    # Line items
    print("【设备清单】")
    print(f"  {'序号':<4} {'型号':<12} {'名称':<20} {'数量':<4} {'单价(万)':<10} {'金额(万)':<10}")
    print(f"  {'-'*4} {'-'*12} {'-'*20} {'-'*4} {'-'*10} {'-'*10}")
    for i, line in enumerate(all_lines, 1):
        print(f"  {i:<4} {line['model']:<12} {line['name']:<20} {line['qty']:<4} "
              f"{line['unit_price']:<10.2f} {line['total']:<10.2f}")
    print(f"  {'':>42} 设备总价: {equipment_total:.2f} 万元")

    # Fee breakdown
    print()
    print("【费用明细】")
    print(f"  设备总价            {equipment_total:>10.2f} 万元")
    if discount_amount > 0:
        print(f"  折扣 ({discount_pct}%)          -{discount_amount:>9.2f} 万元")
    print(f"  折后总价            {after_discount:>10.2f} 万元")
    print(f"  运费                {freight_amount:>10.2f} 万元  ({freight_note})")
    print(f"  安装调试费 (3%)     {install_amount:>10.2f} 万元")
    if spare_amount > 0:
        print(f"  备件包              {spare_amount:>10.2f} 万元")
    if warranty_amount > 0:
        print(f"  延保费 ({extend_warranty}年)        {warranty_amount:>10.2f} 万元")
    print(f"  {'─'*40}")
    print(f"  不含税合计          {subtotal:>10.2f} 万元")
    print(f"  增值税 (13%)        {vat:>10.2f} 万元")
    print(f"  {'─'*40}")
    print(f"  含税总价            {grand_total:>10.2f} 万元")

    print()
    print("【商务条款】")
    print(f"  交货期：{max_lead_time} 天")
    print(f"  质保期：{data['products'][0].get('warranty_years', 2)} 年（标准）")
    print(f"  付款方式：预付30% + 发货前60% + 验收后10%")
    print(f"  报价有效期：30 天")
    print()
    print(f"  📞 13825202084（邹先生）| 📧 aifirefly@163.com")
    print(f"  🌐 www.fireflies.net.cn")
    print()


def main():
    parser = argparse.ArgumentParser(description="萤火虫空压机报价计算")
    parser.add_argument("--model", help="单型号报价")
    parser.add_argument("--models", help="多型号报价，逗号分隔")
    parser.add_argument("--quantity", default="1", help="数量，逗号分隔（与models对应）")
    parser.add_argument("--distance", type=int, default=100, help="运距（公里），默认 100")
    parser.add_argument("--no-accessories", action="store_true", help="不含后处理设备")
    parser.add_argument("--with-spares", action="store_true", help="含备件包")
    parser.add_argument("--extend-warranty", type=int, default=0, help="延保年数")
    parser.add_argument("--validate", help="验算已有报价单 YAML")
    args = parser.parse_args()

    if args.validate:
        print("[验算模式] 读取报价单...")
        with open(args.validate, "r", encoding="utf-8") as f:
            quote = yaml.safe_load(f)
        print(f"  报价单号: {quote.get('quote_no', 'N/A')}")
        print(f"  含税总价: {quote.get('grand_total', 'N/A')} 万元")
        print("[验算] 功能开发中...")
        return

    if args.model:
        models = [args.model]
    elif args.models:
        models = [m.strip() for m in args.models.split(",")]
    else:
        parser.print_help()
        return

    quantities = [int(q.strip()) for q in args.quantity.split(",")]
    if len(quantities) < len(models):
        quantities += [1] * (len(models) - len(quantities))

    print_quote(
        models=models,
        quantities=quantities,
        distance_km=args.distance,
        include_accessories=not args.no_accessories,
        include_spares=args.with_spares,
        extend_warranty=args.extend_warranty,
    )


if __name__ == "__main__":
    main()
