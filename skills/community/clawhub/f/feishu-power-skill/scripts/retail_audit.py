#!/usr/bin/env python3
"""
retail_audit.py — 零售运营审计内核
从多维表格数据中自动识别异常，生成诊断报告
支持 YAML 配置化规则（不同行业不同阈值）
"""

import json
import os
import sys
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

# 添加脚本目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feishu_api as api

# 默认配置路径
CONFIGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "configs")
DEFAULT_CONFIG = os.path.join(CONFIGS_DIR, "retail_default.yaml")


# ============================================================
# 配置加载
# ============================================================

def load_config(config_path: Optional[str] = None) -> Dict:
    """加载审计规则配置（YAML）"""
    path = config_path or DEFAULT_CONFIG
    if not os.path.exists(path):
        print(f"⚠️ 配置文件不存在: {path}，使用内置默认值", file=sys.stderr)
        return _builtin_defaults()
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _builtin_defaults() -> Dict:
    """内置默认配置（无 YAML 文件时的兜底）"""
    return {
        "industry": "通用零售",
        "rules": {
            "sell_through_high": {"enabled": True, "level": "critical", "name": "售罄率过高", "description": "库存即将售罄", "thresholds": {"sell_through_min": 0.85, "days_left_max": 3}},
            "sell_through_low": {"enabled": True, "level": "warning", "name": "售罄率过低", "description": "商品滞销", "thresholds": {"sell_through_max": 0.20, "days_on_shelf_min": 14}},
            "target_achievement_low": {"enabled": True, "level": "critical", "name": "目标达成率不足", "description": "销售严重落后于目标", "thresholds": {"achievement_min": 0.60}},
            "negative_inventory": {"enabled": True, "level": "critical", "name": "负库存", "description": "系统库存为负", "thresholds": {}},
            "zero_sales": {"enabled": True, "level": "critical", "name": "零销售", "description": "营业日无任何销售", "thresholds": {}},
            "inventory_turnover_slow": {"enabled": True, "level": "warning", "name": "库存周转过慢", "description": "资金占用过大", "thresholds": {"turnover_days_max": 45}},
            "low_sell_rate": {"enabled": True, "level": "warning", "name": "动销率过低", "description": "大量SKU无销售", "thresholds": {"sell_rate_min": 0.60}},
        },
        "field_mapping": {
            "store_name": "门店名称", "initial_stock": "期初库存", "sold_qty": "销售数量",
            "current_stock": "当前库存", "days_on_shelf": "上架天数", "actual_sales": "实际销售额",
            "target_sales": "目标销售额", "total_sku": "总SKU数", "active_sku": "有销SKU数",
            "avg_inventory_value": "平均库存金额", "daily_cogs": "日均销售成本", "status": "营业状态",
        },
        "scoring": {"critical_penalty": 25, "warning_penalty": 10, "info_penalty": 3},
    }


def _field(store: Dict, fm: Dict, key: str, default=0):
    """通过字段映射从门店数据中取值"""
    field_name = fm.get(key, key)
    return store.get(field_name, default)


# ============================================================
# 可配置审计规则（从 YAML 驱动）
# ============================================================

RULE_CHECKERS: Dict[str, Any] = {}


def rule_checker(key: str):
    """装饰器：注册规则检查函数"""
    def decorator(fn):
        RULE_CHECKERS[key] = fn
        return fn
    return decorator


@rule_checker("sell_through_high")
def _check_sell_through_high(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    initial_stock = _field(store, fm, "initial_stock")
    sold = _field(store, fm, "sold_qty")
    current_stock = _field(store, fm, "current_stock", initial_stock - sold)
    if initial_stock <= 0:
        return None
    sell_through = sold / initial_stock
    daily_avg = ctx.get("daily_avg_sold", sold)
    days_left = current_stock / daily_avg if daily_avg > 0 else 999
    if sell_through > t.get("sell_through_min", 0.85) and days_left < t.get("days_left_max", 3):
        return {
            "指标": f"售罄率 {sell_through:.0%}",
            "详情": f"剩余库存 {current_stock} 件，预计 {days_left:.1f} 天售罄",
            "建议": "⚠️ 立即补货或从低动销门店调拨",
        }
    return None


@rule_checker("sell_through_low")
def _check_sell_through_low(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    initial_stock = _field(store, fm, "initial_stock")
    sold = _field(store, fm, "sold_qty")
    days_on_shelf = _field(store, fm, "days_on_shelf", 14)
    if initial_stock <= 0:
        return None
    sell_through = sold / initial_stock
    if sell_through < t.get("sell_through_max", 0.20) and days_on_shelf >= t.get("days_on_shelf_min", 14):
        return {
            "指标": f"售罄率 {sell_through:.0%}（上架 {days_on_shelf} 天）",
            "详情": f"已售 {sold} / 期初 {initial_stock}",
            "建议": "⚠️ 滞销预警，建议促销清仓或调拨至高动销门店",
        }
    return None


@rule_checker("target_achievement_low")
def _check_target_achievement_low(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    actual = _field(store, fm, "actual_sales")
    target = _field(store, fm, "target_sales")
    if target <= 0:
        return None
    achievement = actual / target
    if achievement < t.get("achievement_min", 0.60):
        gap = target - actual
        return {
            "指标": f"达成率 {achievement:.0%}",
            "详情": f"实际 ¥{actual:,.0f} / 目标 ¥{target:,.0f}，差距 ¥{gap:,.0f}",
            "建议": "🔴 严重落后，排查：客流下降？转化率低？客单价异常？",
        }
    return None


@rule_checker("negative_inventory")
def _check_negative_inventory(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    stock = _field(store, fm, "current_stock")
    if stock < 0:
        return {
            "指标": f"库存 {stock}",
            "详情": "系统库存为负数，存在数据错误",
            "建议": "🔴 立即盘点核实，检查出入库记录",
        }
    return None


@rule_checker("zero_sales")
def _check_zero_sales(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    sales = _field(store, fm, "actual_sales")
    status_field = fm.get("status", "营业状态")
    is_open = store.get(status_field, "营业") == "营业"
    if sales == 0 and is_open:
        return {
            "指标": "当日销售额 ¥0",
            "详情": "门店处于营业状态但无任何销售记录",
            "建议": "🔴 确认：是否停业？POS系统是否故障？数据是否上传？",
        }
    return None


@rule_checker("inventory_turnover_slow")
def _check_inventory_turnover_slow(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    avg_inventory = _field(store, fm, "avg_inventory_value")
    daily_cogs = _field(store, fm, "daily_cogs")
    threshold = t.get("turnover_days_max", 45)
    if daily_cogs <= 0 or avg_inventory <= 0:
        return None
    turnover_days = avg_inventory / daily_cogs
    if turnover_days > threshold:
        return {
            "指标": f"周转天数 {turnover_days:.0f} 天",
            "详情": f"平均库存 ¥{avg_inventory:,.0f}，日均成本 ¥{daily_cogs:,.0f}",
            "建议": f"⚠️ 超过 {threshold} 天阈值，需清理慢动销商品释放资金",
        }
    return None


@rule_checker("low_sell_rate")
def _check_low_sell_rate(store: Dict, ctx: Dict, t: Dict, fm: Dict) -> Optional[Dict]:
    active_sku = _field(store, fm, "active_sku")
    total_sku = _field(store, fm, "total_sku")
    if total_sku <= 0:
        return None
    sell_rate = active_sku / total_sku
    min_rate = t.get("sell_rate_min", 0.60)
    if sell_rate < min_rate:
        sleeping = total_sku - active_sku
        return {
            "指标": f"动销率 {sell_rate:.0%}",
            "详情": f"{sleeping} 个 SKU 无销售（共 {total_sku} 个）",
            "建议": f"⚠️ {sleeping} 个 SKU 在睡觉，检查品类结构和陈列",
        }
    return None


# ============================================================
# 审计引擎
# ============================================================

def run_audit(stores: List[Dict], context: Optional[Dict] = None, config: Optional[Dict] = None) -> Dict:
    """对所有门店运行审计规则，返回异常报告
    
    Args:
        stores: 门店数据列表
        context: 额外上下文（如 daily_avg_sold）
        config: 审计配置（从 load_config 加载，None 则用默认）
    """
    ctx = context or {}
    cfg = config or load_config()
    rules_cfg = cfg.get("rules", {})
    fm = cfg.get("field_mapping", _builtin_defaults()["field_mapping"])
    scoring = cfg.get("scoring", {"critical_penalty": 25, "warning_penalty": 10, "info_penalty": 3})

    report = {
        "audit_time": datetime.now().isoformat(),
        "industry": cfg.get("industry", "未知"),
        "total_stores": len(stores),
        "summary": {"critical": 0, "warning": 0, "info": 0, "healthy": 0},
        "alerts": [],
        "store_scores": [],
    }

    for store in stores:
        store_name = _field(store, fm, "store_name", store.get("name", "未知"))
        store_alerts = []

        for rule_key, rule_cfg in rules_cfg.items():
            if not rule_cfg.get("enabled", True):
                continue
            checker = RULE_CHECKERS.get(rule_key)
            if not checker:
                continue
            thresholds = rule_cfg.get("thresholds", {})
            result = checker(store, ctx, thresholds, fm)
            if result:
                alert = {
                    "门店": store_name,
                    "异常类型": rule_cfg.get("name", rule_key),
                    "级别": rule_cfg.get("level", "warning"),
                    "描述": rule_cfg.get("description", ""),
                    **result,
                }
                store_alerts.append(alert)
                level = rule_cfg.get("level", "warning")
                report["summary"][level] = report["summary"].get(level, 0) + 1

        if store_alerts:
            report["alerts"].extend(store_alerts)
        else:
            report["summary"]["healthy"] += 1

        # 门店健康评分（100分制）
        score = 100
        for a in store_alerts:
            level = a["级别"]
            score -= scoring.get(f"{level}_penalty", 10)
        report["store_scores"].append({
            "门店": store_name,
            "评分": max(0, score),
            "异常数": len(store_alerts),
        })

    # 按评分排序
    report["store_scores"].sort(key=lambda x: x["评分"])

    return report


# ============================================================
# 报告生成（Markdown → 飞书文档）
# ============================================================

def generate_report_markdown(audit_result: Dict) -> str:
    """从审计结果生成 Markdown 报告"""
    s = audit_result["summary"]
    lines = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    industry = audit_result.get("industry", "")
    lines.append(f"# 门店运营诊断报告 {date_str}")
    if industry:
        lines.append(f"> 行业配置：{industry}")
    lines.append("")

    # 总览
    lines.append("## 📊 总览")
    lines.append("")
    total = audit_result["total_stores"]
    lines.append(f"- 门店总数：{total}")
    lines.append(f"- 🟢 健康门店：{s['healthy']} ({s['healthy']/total:.0%})")
    lines.append(f"- 🔴 严重异常：{s['critical']} 条")
    lines.append(f"- 🟡 警告：{s['warning']} 条")
    lines.append("")

    critical_alerts = [a for a in audit_result["alerts"] if a["级别"] == "critical"]
    if critical_alerts:
        lines.append("## 🔴 严重异常（需立即处理）")
        lines.append("")
        for a in critical_alerts:
            lines.append(f"### {a['门店']} — {a['异常类型']}")
            lines.append(f"- **指标**：{a['指标']}")
            lines.append(f"- **详情**：{a['详情']}")
            lines.append(f"- **建议**：{a['建议']}")
            lines.append("")

    warning_alerts = [a for a in audit_result["alerts"] if a["级别"] == "warning"]
    if warning_alerts:
        lines.append("## 🟡 警告（需关注）")
        lines.append("")
        for a in warning_alerts:
            lines.append(f"### {a['门店']} — {a['异常类型']}")
            lines.append(f"- **指标**：{a['指标']}")
            lines.append(f"- **详情**：{a['详情']}")
            lines.append(f"- **建议**：{a['建议']}")
            lines.append("")

    lines.append("## 📋 门店健康排名")
    lines.append("")
    lines.append("| 排名 | 门店 | 健康评分 | 异常数 |")
    lines.append("|------|------|---------|--------|")
    for i, ss in enumerate(audit_result["store_scores"], 1):
        score = ss["评分"]
        emoji = "🔴" if score < 50 else "🟡" if score < 75 else "🟢"
        lines.append(f"| {i} | {ss['门店']} | {emoji} {score} | {ss['异常数']} |")
    lines.append("")

    return "\n".join(lines)


def publish_report_to_feishu(markdown: str, doc_token: Optional[str] = None, folder_token: Optional[str] = None) -> str:
    """将报告发布到飞书文档，分批写入避免 API 限制"""
    import time as _time

    if not doc_token:
        date_str = datetime.now().strftime("%Y-%m-%d")
        title = f"门店运营诊断报告 {date_str}"
        result = api.docx_create_document(title, folder_token)
        doc_token = result.get("document", {}).get("document_id", "")

    if not doc_token:
        raise Exception("无法创建文档")

    blocks = _markdown_to_blocks(markdown)

    batch_size = 5
    for i in range(0, len(blocks), batch_size):
        chunk = blocks[i : i + batch_size]
        try:
            api._post(f"/docx/v1/documents/{doc_token}/blocks/{doc_token}/children", {
                "children": chunk,
            })
        except Exception as e:
            for block in chunk:
                try:
                    api._post(f"/docx/v1/documents/{doc_token}/blocks/{doc_token}/children", {
                        "children": [block],
                    })
                except Exception:
                    pass
        if i + batch_size < len(blocks):
            _time.sleep(0.3)

    return doc_token


def _markdown_to_blocks(md: str) -> List[Dict]:
    """简易 Markdown → 飞书 Block 转换"""
    blocks = []
    for line in md.split("\n"):
        if not line.strip():
            continue
        if line.startswith("# "):
            blocks.append(_heading_block(1, line[2:]))
        elif line.startswith("## "):
            blocks.append(_heading_block(2, line[3:]))
        elif line.startswith("### "):
            blocks.append(_heading_block(3, line[4:]))
        elif line.startswith("| "):
            blocks.append(_text_block(line))
        elif line.startswith("- "):
            blocks.append(_bullet_block(line[2:]))
        elif line.startswith("> "):
            blocks.append(_text_block(line[2:]))
        else:
            blocks.append(_text_block(line))
    return blocks


def _heading_block(level: int, text: str) -> Dict:
    block_type = level + 2
    key = f"heading{level}"
    return {
        "block_type": block_type,
        key: {"elements": [_text_element(text)]},
    }


def _text_block(text: str) -> Dict:
    return {
        "block_type": 2,
        "text": {"elements": _parse_inline(text)},
    }


def _bullet_block(text: str) -> Dict:
    return {
        "block_type": 12,
        "bullet": {"elements": _parse_inline(text)},
    }


def _parse_inline(text: str) -> List[Dict]:
    """解析加粗等内联格式"""
    elements = []
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 1:
            elements.append(_text_element(part, bold=True))
        else:
            elements.append(_text_element(part))
    return elements if elements else [_text_element(text)]


def _text_element(text: str, bold: bool = False) -> Dict:
    el = {"text_run": {"content": text}}
    if bold:
        el["text_run"]["text_element_style"] = {"bold": True}
    return el


# ============================================================
# Demo 数据生成
# ============================================================

def generate_demo_data(num_stores: int = 50) -> List[Dict]:
    """生成模拟的50家门店数据"""
    import random
    random.seed(42)

    regions = ["华东", "华南", "华北", "西南", "华中"]
    cities = {
        "华东": ["上海", "杭州", "南京", "苏州", "宁波"],
        "华南": ["广州", "深圳", "东莞", "佛山", "珠海"],
        "华北": ["北京", "天津", "石家庄", "济南", "青岛"],
        "西南": ["成都", "重庆", "昆明", "贵阳", "南宁"],
        "华中": ["武汉", "长沙", "郑州", "合肥", "南昌"],
    }

    stores = []
    for i in range(num_stores):
        region = regions[i % 5]
        city = cities[region][i // 10 % 5]
        store_name = f"{city}{i+1:02d}店"

        target = random.randint(8000, 50000)
        if i < 5:
            actual = int(target * random.uniform(0.25, 0.55))
        elif i < 10:
            actual = int(target * random.uniform(0.90, 1.20))
        elif i < 13:
            actual = 0
        elif i < 16:
            actual = int(target * random.uniform(0.60, 0.90))
        else:
            actual = int(target * random.uniform(0.65, 1.15))

        initial_stock = random.randint(200, 800)
        if i < 10 and i >= 5:
            sold = int(initial_stock * random.uniform(0.88, 0.97))
        elif i >= 16 and i < 25:
            sold = int(initial_stock * random.uniform(0.05, 0.18))
        else:
            sold = int(initial_stock * random.uniform(0.30, 0.75))

        current_stock = initial_stock - sold
        if 13 <= i < 16:
            current_stock = random.randint(-50, -5)

        total_sku = random.randint(80, 200)
        if i >= 30 and i < 35:
            active_sku = int(total_sku * random.uniform(0.30, 0.55))
        else:
            active_sku = int(total_sku * random.uniform(0.62, 0.92))

        daily_avg_sold = max(1, sold // 7)
        avg_inventory_value = current_stock * random.randint(80, 300)
        daily_cogs = max(1, actual * 0.6 / 7)

        stores.append({
            "门店名称": store_name,
            "区域": region,
            "城市": city,
            "目标销售额": target,
            "实际销售额": actual,
            "期初库存": initial_stock,
            "销售数量": sold,
            "当前库存": current_stock,
            "上架天数": random.randint(7, 30),
            "总SKU数": total_sku,
            "有销SKU数": active_sku,
            "平均库存金额": avg_inventory_value,
            "日均销售成本": daily_cogs,
            "营业状态": "营业",
        })

    return stores


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="零售运营审计引擎")
    sub = parser.add_subparsers(dest="command", required=True)

    # demo
    p_demo = sub.add_parser("demo", help="运行 Demo（50家门店模拟数据）")
    p_demo.add_argument("--config", help="审计规则配置文件路径 (YAML)")
    p_demo.add_argument("--publish", action="store_true", help="发布到飞书文档")
    p_demo.add_argument("--folder", help="飞书文件夹 token")
    p_demo.add_argument("--output", help="输出 Markdown 文件路径")

    # audit
    p_audit = sub.add_parser("audit", help="从 bitable 读取数据并审计")
    p_audit.add_argument("--app", required=True, help="Bitable app token")
    p_audit.add_argument("--sales-table", required=True, help="销售数据表 ID")
    p_audit.add_argument("--target-table", help="目标数据表 ID（可选，用于跨表 JOIN）")
    p_audit.add_argument("--inventory-table", help="库存数据表 ID（可选）")
    p_audit.add_argument("--config", help="审计规则配置文件路径 (YAML)")
    p_audit.add_argument("--publish", action="store_true", help="发布到飞书文档")
    p_audit.add_argument("--folder", help="飞书文件夹 token")

    # list-configs
    p_list = sub.add_parser("list-configs", help="列出可用的配置文件")

    args = parser.parse_args()

    if args.command == "list-configs":
        if os.path.isdir(CONFIGS_DIR):
            configs = [f for f in os.listdir(CONFIGS_DIR) if f.endswith((".yaml", ".yml"))]
            if configs:
                print("可用配置文件：")
                for c in sorted(configs):
                    cfg = load_config(os.path.join(CONFIGS_DIR, c))
                    industry = cfg.get("industry", "未知")
                    enabled = sum(1 for r in cfg.get("rules", {}).values() if r.get("enabled", True))
                    print(f"  {c} — {industry}（{enabled} 条规则）")
            else:
                print("configs/ 目录下没有配置文件")
        else:
            print(f"配置目录不存在: {CONFIGS_DIR}")
        return

    cfg = load_config(args.config) if hasattr(args, 'config') and args.config else load_config()

    if args.command == "demo":
        print(f"配置: {cfg.get('industry', '默认')}", flush=True)
        print("生成 50 家门店模拟数据...", flush=True)
        stores = generate_demo_data(50)

        print("运行审计引擎...", flush=True)
        result = run_audit(stores, config=cfg)

        print(f"\n审计完成:")
        print(f"  🔴 严重异常: {result['summary']['critical']} 条")
        print(f"  🟡 警告: {result['summary']['warning']} 条")
        print(f"  🟢 健康门店: {result['summary']['healthy']} 家")

        md = generate_report_markdown(result)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"\n报告已保存: {args.output}")

        if args.publish:
            print("\n发布到飞书...", flush=True)
            doc_id = publish_report_to_feishu(md, folder_token=args.folder)
            print(f"飞书文档已创建: https://my.feishu.cn/docx/{doc_id}")
        elif not args.output:
            print("\n" + md)

    elif args.command == "audit":
        print(f"配置: {cfg.get('industry', '默认')}", flush=True)
        print("从 bitable 读取数据...", flush=True)
        records = api.bitable_list_all_records(args.app, args.sales_table)
        stores = [r.get("fields", {}) for r in records]

        if args.target_table:
            import bitable_engine as engine
            joined = engine.cross_table_join(
                args.app, args.sales_table, args.target_table, "门店名称"
            )
            if joined:
                stores = joined

        print(f"读取到 {len(stores)} 家门店数据", flush=True)
        result = run_audit(stores, config=cfg)

        md = generate_report_markdown(result)

        if args.publish:
            doc_id = publish_report_to_feishu(md, folder_token=args.folder)
            print(f"飞书文档已创建: https://my.feishu.cn/docx/{doc_id}")
        else:
            print(md)


if __name__ == "__main__":
    main()
