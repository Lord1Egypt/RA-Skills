#!/usr/bin/env python3
"""
AI 市场日报 — 蜂巢主控

工作流：
  1. 花园感知（scanner） → 动态厂商清单 + bloom 评分
  2. 采蜜（forager）     → 新闻+计费数据
  3. 酿蜜（brewer）      → 性价比+排名+日报
  4. 输出（report）      → Markdown + 可选飞书推送
"""

import asyncio
import json
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from garden.scanner import GardenScanner, VendorRegistry, init_registry_from_config
from forager.forager import Forager
from brewer.brewer import brew


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config.yaml"
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f)
    except ImportError:
        # 无 yaml 模块，手动解析
        print("⚠️  yaml 模块未安装，使用默认配置")
        return {}


async def run_daily():
    """运行每日蜂巢工作流"""
    today = date.today().isoformat()
    print(f"🐝 蜂巢日报工作流 — {today}")
    print("=" * 50)
    
    # Step 1: 加载配置
    print("\n📋 Step 1: 加载配置...")
    config = load_config()
    
    # Step 2: 花园感知
    print("\n🌸 Step 2: 花园感知...")
    registry = init_registry_from_config(config)
    scanner = GardenScanner(registry, config)
    garden_results = scanner.scan()
    
    # 保存花园扫描结果
    from brewer.brewer import OUTPUT_DIR
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    garden_path = OUTPUT_DIR / f"garden_{today}.json"
    with open(garden_path, "w") as f:
        json.dump(garden_results, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 花园扫描完成: {garden_path}")
    print(f"  厂商更新: {len(garden_results.get('vendors_updated', []))} 家")
    print(f"  新发现: {len(garden_results.get('new_vendors', []))} 家")
    
    # Step 3: 采蜜
    print("\n🍯 Step 3: 采蜜...")
    with open(OUTPUT_DIR / "vendor_registry.json") as f:
        registry_data = json.load(f)
    
    forager = Forager(registry_data)
    plan = forager.get_forage_plan()
    print(f"  采蜜计划: 全量 {len(plan['full'])} / 标准 {len(plan['standard'])} / 轻量 {len(plan['light'])} / 跳过 {len(plan['skip'])}")
    
    forage_results = await forager.forage_all()
    
    forage_path = OUTPUT_DIR / f"forage_{today}.json"
    with open(forage_path, "w") as f:
        json.dump(forage_results, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 采蜜完成: {forage_path}")
    
    # Step 4: 酿蜜
    print("\n🍼 Step 4: 酿蜜...")
    report = brew(garden_path, forage_path)
    
    print("\n" + "=" * 50)
    print("🐝 蜂巢日报工作流完成！")
    print(f"  日报: {OUTPUT_DIR / f'daily_report_{today}.md'}")
    
    return report


if __name__ == "__main__":
    asyncio.run(run_daily())
