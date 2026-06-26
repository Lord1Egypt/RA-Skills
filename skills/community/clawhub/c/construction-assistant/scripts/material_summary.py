#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
材料需求统计与采购计划
根据进度计划计算材料需求，生成采购建议
"""

import argparse
import json
from datetime import datetime, timedelta


# 材料消耗定额参考（每单位工程量）
MATERIAL_QUOTAS = {
    # 混凝土工程 (m³混凝土的材料用量)
    "concrete_C20": {"cement_kg": 300, "sand_m3": 0.5, "gravel_m3": 0.8, "water_m3": 0.18},
    "concrete_C25": {"cement_kg": 330, "sand_m3": 0.5, "gravel_m3": 0.8, "water_m3": 0.18},
    "concrete_C30": {"cement_kg": 370, "sand_m3": 0.5, "gravel_m3": 0.8, "water_m3": 0.18},
    "concrete_C35": {"cement_kg": 410, "sand_m3": 0.5, "gravel_m3": 0.8, "water_m3": 0.18},
    
    # 钢筋工程 (每吨钢筋的辅材)
    "rebar_binding": {"wire_kg": 5, "pad_block": 50},  # 绑扎丝 kg，垫块个
    
    # 模板工程 (每 10m²模板)
    "formwork_wood": {"plywood_m2": 12, "wood_m3": 0.15, "nail_kg": 2},
    "formwork_steel": {"steel_t": 0.25, "oil_kg": 1},
}


def load_schedule(schedule_path):
    """加载进度计划"""
    with open(schedule_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_inventory(inventory_path=None):
    """加载库存数据"""
    if inventory_path:
        try:
            with open(inventory_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    return {}


def calculate_period_tasks(schedule, period="next_week", reference_date=None):
    """计算指定时间段的工序"""
    if reference_date is None:
        reference_date = datetime.now()
    else:
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
    
    if period == "next_week":
        start_date = reference_date
        end_date = reference_date + timedelta(days=7)
    elif period == "next_month":
        start_date = reference_date
        end_date = reference_date + timedelta(days=30)
    elif period == "this_week":
        # 本周一到周日
        days_to_monday = reference_date.weekday()
        start_date = reference_date - timedelta(days=days_to_monday)
        end_date = start_date + timedelta(days=7)
    else:
        raise ValueError(f"未知的时间段：{period}")
    
    period_tasks = []
    
    for task in schedule["tasks"]:
        task_start = datetime.strptime(task["start_date"], "%Y-%m-%d")
        task_end = datetime.strptime(task["end_date"], "%Y-%m-%d")
        
        # 判断工序是否与时间段有交集
        if task_start <= end_date and task_end >= start_date:
            if task["status"] != "completed":
                period_tasks.append({
                    "task": task,
                    "overlap_days": min(task_end, end_date) - max(task_start, start_date)
                })
    
    return period_tasks, start_date, end_date


def estimate_materials(period_tasks, material_quantities=None):
    """估算材料需求"""
    materials = {}
    
    for pt in period_tasks:
        task = pt["task"]
        task_name = task["name"].lower()
        
        # 根据工序名称估算材料（简化版，实际应关联工程量）
        if "混凝土" in task["name"] or "砼" in task["name"]:
            # 假设每道工序平均 50m³混凝土（实际应从工程量清单获取）
            concrete_volume = 50
            materials.setdefault("混凝土 C30", {"unit": "m³", "quantity": 0})
            materials["混凝土 C30"]["quantity"] += concrete_volume
            
        elif "钢筋" in task["name"]:
            # 假设每道工序平均 10 吨钢筋
            rebar_weight = 10
            materials.setdefault("钢筋 HRB400", {"unit": "吨", "quantity": 0})
            materials["钢筋 HRB400"]["quantity"] += rebar_weight
            
        elif "模板" in task["name"]:
            # 假设每道工序平均 200m²模板
            formwork_area = 200
            materials.setdefault("模板 plywood", {"unit": "m²", "quantity": 0})
            materials["模板 plywood"]["quantity"] += formwork_area
            
        elif "砌体" in task["name"] or "砌筑" in task["name"]:
            # 假设每道工序平均 100m³砌体
            masonry_volume = 100
            materials.setdefault("标准砖", {"unit": "千块", "quantity": 0})
            materials["标准砖"]["quantity"] += masonry_volume * 0.512
            materials.setdefault("水泥", {"unit": "吨", "quantity": 0})
            materials["水泥"]["quantity"] += masonry_volume * 0.1
    
    return materials


def generate_purchase_plan(materials, inventory, lead_days=3):
    """生成采购计划"""
    purchase_plan = []
    
    today = datetime.now()
    suggested_order_date = (today + timedelta(days=lead_days)).strftime("%Y-%m-%d")
    
    for material_name, info in materials.items():
        required = info["quantity"]
        stock = inventory.get(material_name, {}).get("stock", 0)
        gap = required - stock
        
        if gap > 0:
            purchase_plan.append({
                "material": material_name,
                "unit": info["unit"],
                "required": round(required, 2),
                "stock": round(stock, 2),
                "gap": round(gap, 2),
                "suggested_order_date": suggested_order_date,
                "priority": "high" if gap > required * 0.5 else "normal"
            })
    
    # 按优先级排序
    purchase_plan.sort(key=lambda x: (0 if x["priority"] == "high" else 1, -x["gap"]))
    
    return purchase_plan


def generate_material_report(materials, inventory, purchase_plan, period_start, period_end):
    """生成材料报告"""
    report = []
    report.append("# 材料需求统计报告")
    report.append(f"\n**统计周期**: {period_start.strftime('%Y-%m-%d')} 至 {period_end.strftime('%Y-%m-%d')}")
    report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    report.append(f"\n## 一、材料需求汇总")
    report.append("\n| 材料名称 | 单位 | 需求数量 | 当前库存 | 缺口 | 备注 |")
    report.append("|---------|------|---------|---------|------|------|")
    
    for name, info in materials.items():
        stock = inventory.get(name, {}).get("stock", 0)
        gap = info["quantity"] - stock
        remark = "⚠️ 需采购" if gap > 0 else "✅ 充足"
        report.append(f"| {name} | {info['unit']} | {info['quantity']:.2f} | {stock:.2f} | "
                     f"{gap:.2f} | {remark} |")
    
    if purchase_plan:
        report.append(f"\n## 二、采购建议")
        report.append(f"\n建议下单日期：**{(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')}**\n")
        report.append("| 优先级 | 材料名称 | 单位 | 采购数量 | 备注 |")
        report.append("|-------|---------|------|---------|------|")
        
        for item in purchase_plan:
            priority_mark = "🔴" if item["priority"] == "high" else "🟡"
            report.append(f"| {priority_mark} {item['priority']} | {item['material']} | "
                         f"{item['unit']} | {item['gap']:.2f} | 建议提前备料 |")
    else:
        report.append(f"\n## 二、采购建议")
        report.append("\n✅ 当前库存充足，暂无采购需求。")
    
    report.append(f"\n## 三、使用说明")
    report.append("""
1. 本报告根据进度计划自动估算材料需求
2. 实际用量请根据施工图纸和现场情况调整
3. 建议提前 3-7 天下单，确保材料及时到场
4. 特殊材料（如定制构件）需提前更长时间预订
""")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="材料需求统计与采购计划")
    parser.add_argument("--schedule", required=True, help="进度计划文件路径")
    parser.add_argument("--period", default="next_week", 
                       choices=["this_week", "next_week", "next_month"],
                       help="统计周期")
    parser.add_argument("--reference-date", help="参考日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--inventory", help="库存文件路径 (JSON)")
    parser.add_argument("--output", help="报告输出路径")
    
    args = parser.parse_args()
    
    # 加载进度计划
    schedule = load_schedule(args.schedule)
    
    # 加载库存
    inventory = load_inventory(args.inventory)
    
    # 计算周期内的工序
    period_tasks, period_start, period_end = calculate_period_tasks(
        schedule, 
        args.period, 
        args.reference_date
    )
    
    print(f"📊 统计周期：{period_start.strftime('%Y-%m-%d')} 至 {period_end.strftime('%Y-%m-%d')}")
    print(f"📋 计划工序：{len(period_tasks)} 项")
    
    # 估算材料需求
    materials = estimate_materials(period_tasks)
    
    if not materials:
        print("ℹ️  该周期内无材料需求或无法估算")
        return
    
    # 生成采购计划
    purchase_plan = generate_purchase_plan(materials, inventory)
    
    # 生成报告
    report = generate_material_report(materials, inventory, purchase_plan, period_start, period_end)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✓ 材料报告已保存：{args.output}")
    else:
        print(report)
    
    # 同时输出 JSON 格式便于程序处理
    json_output = {
        "period": {
            "start": period_start.strftime("%Y-%m-%d"),
            "end": period_end.strftime("%Y-%m-%d")
        },
        "materials": materials,
        "purchase_plan": purchase_plan
    }
    
    if args.output:
        json_path = args.output.replace(".md", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_output, f, ensure_ascii=False, indent=2)
        print(f"✓ JSON 数据已保存：{json_path}")


if __name__ == "__main__":
    main()
