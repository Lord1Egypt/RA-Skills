#!/usr/bin/env python3
"""
中国安装工程造价 - 取费计算引擎
适用标准：
  - GB/T 50500-2024《建设工程工程量清单计价标准》（2025年9月1日起山东实施）
  - 《山东省建设工程费用项目组成及计算规则》（2025年版，2025年11月1日起施行）
  - 《山东省安装工程消耗量定额》（2025版）
  - 《济南市价目表(2026版)》

【重大变化】GB/T 50500-2024 取消"规费"科目。
  社会保险费、住房公积金并入人工费和企业管理费。
  费用结构：人工费 + 管理费（含统筹） + 利润 + 税金

管理费费率：48.08%（以人工费为基数）
利润费率：  29.15%（以人工费+管理费为基数）
税率：      9%（增值税一般纳税人）

【重要】计费基础：
  管理费和利润的计费基础均为"人工费"，不是"基价"。
  基价 = 人工费 + 材料费 + 机械费（定额单价全口径）。
  依据：《山东省建设工程费用项目组成及计算规则》2025年版
        第三章 费率表说明：计费基础1 = 分部分项工程量清单综合单价中的"人工费"

综合费率（仅人工费口径）： 91.25%  （(1+48.08%)×(1+29.15%)-1）
含税系数（仅人工费口径）：   2.0846  （1.9125×1.09）

注意：综合费率和含税系数只能乘以"人工费"，不能乘以"基价"。
      基价口径的综合单价 = 基价 + 人工费×综合费率（非 基价×综合费率）
"""

import sys
from typing import Dict, List, Optional

# ──────────────────────────────────────────────
# 取费参数（2025版山东省安装工程标准）
# ──────────────────────────────────────────────
MANAGEMENT_FEE_RATE = 0.4808   # 管理费 48.08%（以人工费为基数）
PROFIT_RATE = 0.2915           # 利润 29.15%（以人工费+管理费为基数）
TAX_RATE = 0.09                # 增值税 9%（一般纳税人）

# 注：规费已取消（GB/T 50500-2024），社会保险费、住房公积金
# 并入人工费和企业管理费，不再单独计取规费费率。


def calc_comprehensive_price(
    base_price: float,
    labor_fee: Optional[float] = None
) -> Dict[str, float]:
    """
    根据基价和人工费计算含税综合单价（2025版规则）。

    计算公式（规费已取消）：
    Step 1: 管理费  = 人工费 × 48.08%
    Step 2: 利润    = (人工费 + 管理费) × 29.15%
    Step 3: 税前综合单价 = 基价 + 管理费 + 利润
    Step 4: 税金    = 税前综合单价 × 9%
    Step 5: 含税综合单价 = 税前综合单价 + 税金

    Args:
        base_price: 济南市价目表2026版基价（元）= 人工费 + 材料费 + 机械费
        labor_fee:  人工费（元）。如为 None，则默认等于 base_price（向后兼容）。

    Returns:
        dict，含 keys:
          - base_price            基价
          - labor_fee             人工费
          - management_fee        管理费（元）
          - profit                利润（元）
          - subtotal_before_tax   税前综合单价
          - tax                   税金（元）
          - total_with_tax        含税综合单价
          - comprehensive_rate    综合费率（91.25%，仅适用于人工费口径）
          - tax_included_rate     含税综合系数（2.0846，仅适用于人工费口径）
    """
    # 向后兼容：未传人工费时，按旧逻辑（基价=人工费）计算，并发出提示
    if labor_fee is None:
        labor_fee = base_price

    management_fee = labor_fee * MANAGEMENT_FEE_RATE
    subtotal = labor_fee + management_fee
    profit = subtotal * PROFIT_RATE
    subtotal_before_tax = base_price + management_fee + profit
    tax = subtotal_before_tax * TAX_RATE
    total_with_tax = subtotal_before_tax + tax

    return {
        "base_price": round(base_price, 4),
        "labor_fee": round(labor_fee, 4),
        "management_fee": round(management_fee, 4),
        "profit": round(profit, 4),
        "subtotal_before_tax": round(subtotal_before_tax, 4),
        "tax": round(tax, 4),
        "total_with_tax": round(total_with_tax, 4),
        # 综合费率：仅适用于人工费口径（人工费×综合费率 = 管理费+利润）
        "comprehensive_rate": round(
            (1 + MANAGEMENT_FEE_RATE) * (1 + PROFIT_RATE) - 1, 6
        ),
        # 含税综合系数：仅适用于人工费口径（人工费×含税系数 = 含税综合单价-材料费-机械费）
        "tax_included_rate": round(
            (1 + MANAGEMENT_FEE_RATE) * (1 + PROFIT_RATE) * (1 + TAX_RATE), 6
        ),
    }


def calc_line_total(
    base_price: float,
    quantity: float,
    labor_fee: Optional[float] = None,
    include_tax: bool = True
) -> Dict[str, float]:
    """
    计算单行合价。

    Args:
        base_price:   基价（元）
        quantity:     工程量
        labor_fee:    人工费（元），如为None则默认等于base_price
        include_tax:  是否含税（默认含税）

    Returns:
        dict，含 keys:
          - unit_comprehensive_price  单位综合单价
          - line_total                 单行合价
    """
    cp = calc_comprehensive_price(base_price, labor_fee)
    if include_tax:
        unit_price = cp["total_with_tax"]
    else:
        unit_price = cp["subtotal_before_tax"]

    return {
        "unit_comprehensive_price": round(unit_price, 4),
        "line_total": round(unit_price * quantity, 2),
    }


def build_estimate_table(items: List[Dict]) -> Dict:
    """
    为一组定额子目批量计算取费。

    Args:
        items: list of dict，每个 dict 至少含：
               - code:       定额编号（如 "8-3-28"）
               - name:       子目名称
               - unit:       计量单位
               - quantity:   工程量
               - base_price: 基价（济南市价目表2026版）
               - labor_fee:  人工费（元，可选，默认等于base_price）

    Returns:
        dict，含 keys:
          - items:   list of dict，含全部计算字段
          - summary: dict，含各费用合计
          - comprehensive_rate: 综合费率（0.9125）
          - tax_included_rate:  含税综合系数（2.0846）
    """
    results = []
    grand_total = 0.0          # 含税合价总计
    grand_total_no_tax = 0.0  # 税前合价总计
    total_mgmt_fee = 0.0
    total_profit = 0.0
    total_tax = 0.0

    for i, item in enumerate(items):
        labor = item.get("labor_fee", item["base_price"])
        cp = calc_comprehensive_price(item["base_price"], labor)
        qty = item.get("quantity", 1)

        line_no_tax = cp["subtotal_before_tax"] * qty
        line_tax = cp["total_with_tax"] * qty
        grand_total += line_tax
        grand_total_no_tax += line_no_tax
        total_mgmt_fee += cp["management_fee"] * qty
        total_profit += cp["profit"] * qty
        total_tax += cp["tax"] * qty

        results.append({
            "序号": i + 1,
            "定额编号": item.get("code", ""),
            "子目名称": item.get("name", ""),
            "章节": item.get("chapter", ""),
            "条款": item.get("clause", ""),
            "工作内容": item.get("description", ""),
            "单位": item.get("unit", ""),
            "工程量": qty,
            "基价": cp["base_price"],
            "人工费": cp["labor_fee"],
            "管理费(48.08%)": cp["management_fee"],
            "利润(29.15%)": cp["profit"],
            "税前综合单价": cp["subtotal_before_tax"],
            "税金(9%)": cp["tax"],
            "含税综合单价": cp["total_with_tax"],
            "合价(不含税)": round(line_no_tax, 2),
            "合价(含税)": round(line_tax, 2),
        })

    return {
        "items": results,
        "summary": {
            "合计(不含税)": round(grand_total_no_tax, 2),
            "合计(含税)": round(grand_total, 2),
            "管理费合计": round(total_mgmt_fee, 2),
            "利润合计": round(total_profit, 2),
            "税金合计": round(total_tax, 2),
        },
        "comprehensive_rate": calc_comprehensive_price(0)["comprehensive_rate"],
        "tax_included_rate": calc_comprehensive_price(0)["tax_included_rate"],
    }


def print_estimate(result: Dict):
    """打印估算结果到终端（调试用）。"""
    cp0 = calc_comprehensive_price(0)
    print("\n========== 取费计算结果 ==========")
    print(f"适用标准：GB/T 50500-2024 / 山东省2025版费用规则")
    print(f"管理费: {MANAGEMENT_FEE_RATE:.2%}  利润: {PROFIT_RATE:.2%}  税金: {TAX_RATE:.2%}")
    print(f"综合费率: {cp0['comprehensive_rate']:.4%}  含税系数: {cp0['tax_included_rate']:.4f}")
    print()
    print(f"{'序号':>4} {'定额编号':>10} {'子目名称':<20} {'单位':>4} "
          f"{'工程量':>8} {'基价':>10} {'人工费':>10} {'含税单价':>12} {'含税合价':>12}")
    print("-" * 110)

    for r in result["items"]:
        print(
            f"{r['序号']:>4} {r['定额编号']:>10} {r['子目名称']:<20} "
            f"{r['单位']:>4} {r['工程量']:>8.3f} {r['基价']:>10.4f} "
            f"{r['人工费']:>10.4f} "
            f"{r['含税综合单价']:>12.4f} {r['合价(含税)']:>12.2f}"
        )

    s = result["summary"]
    print("-" * 95)
    print(f"{'管理费合计':>74} {s['管理费合计']:>12.2f}")
    print(f"{'利润合计':>74} {s['利润合计']:>12.2f}")
    print(f"{'税金合计':>74} {s['税金合计']:>12.2f}")
    print(f"{'合计(不含税)':>74} {s['合计(不含税)']:>12.2f}")
    print(f"{'合计(含税)':>74} {s['合计(含税)']:>12.2f}")
    print(f"{'含税综合系数':>74} {result['tax_included_rate']:.4f}")
    print()


# ──────────────────────────────────────────────
# Excel 公式参考（用于粘贴到 Excel 单元格）
# ──────────────────────────────────────────────
EXCEL_FORMULAS = {
    # 管理费 = 人工费 × 48.08%
    "管理费": '=[@人工费]*48.08%',
    # 利润 = (人工费 + 管理费) × 29.15%
    "利润": '=([@人工费]+[@管理费])*29.15%',
    # 税前综合单价 = 基价 + 管理费 + 利润
    "税前综合单价": '=[@基价]+[@管理费]+[@利润]',
    # 含税综合单价 = 税前综合单价 × (1+9%)
    "含税综合单价": '=[@税前综合单价]*(1+9%)',
    # 税金 = 税前综合单价 × 9%
    "税金": '=[@税前综合单价]*9%',
    # 合价（不含税）= 工程量 × 税前综合单价
    "合价(不含税)": '=[@工程量]*[@税前综合单价]',
    # 合价（含税）= 工程量 × 含税综合单价
    "合价(含税)": '=[@工程量]*[@含税综合单价]',
    # 小计（筛选时保留可见性）
    "小计": '=SUBTOTAL(109,[合价(含税)])',
}


if __name__ == "__main__":
    # ── 示例数据 ──
    sample_items = [
        {
            "code": "8-3-28",
            "name": "低压钢管焊接安装",
            "chapter": "第8章 管道安装",
            "clause": "8.3.2",
            "description": "低压碳钢管电弧焊安装，φ57×3.5，不含压力试验",
            "unit": "m",
            "quantity": 150,
            "base_price": 28.50,   # 济南市价目表2026版基价（元/m）
            "labor_fee": 22.80,    # 人工费（元/m），基价=人工费+材料费+机械费
        },
        {
            "code": "8-4-15",
            "name": "管道压力试验",
            "chapter": "第8章 管道安装",
            "clause": "8.4.1",
            "description": "管道压力试验，水压试验，工作压力≤1.6MPa",
            "unit": "m",
            "quantity": 150,
            "base_price": 3.80,
            "labor_fee": 2.66,
        },
    ]

    result = build_estimate_table(sample_items)
    print_estimate(result)
    print("Excel 公式参考：")
    for k, v in EXCEL_FORMULAS.items():
        print(f"  {k}: {v}")
