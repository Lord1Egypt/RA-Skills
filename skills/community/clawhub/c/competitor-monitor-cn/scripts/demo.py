#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控 - 演示版
用模拟数据展示功能（无需真实网络请求）
"""

import json
import random
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 模拟竞品数据
DEMO_PRODUCTS = [
    {
        "name": "罗技 G102 鼠标 - 京东自营",
        "url": "https://item.jd.com/100001.html",
        "platform": "jd",
        "current_price": 99.0,
        "original_price": 129.0,
        "in_stock": True,
        "sales": "月销 10 万+"
    },
    {
        "name": "罗技 G102 鼠标 - 淘宝专卖店",
        "url": "https://item.taobao.com/item.htm?id=520123456",
        "platform": "taobao",
        "current_price": 89.0,
        "original_price": 99.0,
        "in_stock": True,
        "sales": "月销 5000+"
    },
    {
        "name": "雷蛇毒蝰鼠标 - 京东自营",
        "url": "https://item.jd.com/100002.html",
        "platform": "jd",
        "current_price": 199.0,
        "original_price": 299.0,
        "in_stock": False,
        "sales": "月销 2 万+"
    }
]

def generate_alert(product, price_change=None):
    """生成告警消息"""
    msg = []
    msg.append("👀 竞品监控提醒")
    msg.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    msg.append("")
    
    msg.append(f"【商品】{product['name']}")
    msg.append(f"【平台】{product['platform'].upper()}")
    msg.append(f"【链接】{product['url']}")
    msg.append("")
    
    if price_change:
        msg.append("💰 价格变动！")
        msg.append(f"├ 原价：{price_change['old']:.2f} 元")
        msg.append(f"├ 现价：{price_change['new']:.2f} 元")
        msg.append(f"└ 变化：{price_change['diff']:+.2f} 元 ({price_change['pct']:+.1f}%)")
    else:
        msg.append("💰 当前价格")
        msg.append(f"├ 售价：{product['current_price']:.2f} 元")
        msg.append(f"├ 原价：{product['original_price']:.2f} 元")
        msg.append(f"└ 折扣：{product['current_price']/product['original_price']*10:.1f}折")
    
    msg.append("")
    msg.append("📊 库存状态")
    status = "✅ 有货" if product['in_stock'] else "❌ 缺货"
    msg.append(f"└ {status}")
    
    if product.get('sales'):
        msg.append("")
        msg.append("📈 销量估算")
        msg.append(f"└ {product['sales']}")
    
    if price_change and price_change['diff'] < 0:
        msg.append("")
        msg.append("🎯 建议操作")
        msg.append(f"├ 是否跟进：是")
        msg.append(f"├ 建议价格：{product['current_price'] - 2:.2f} 元（略低于竞品）")
        msg.append(f"└ 毛利测算：根据成本计算")
    
    msg.append("")
    msg.append("---")
    msg.append("💡 竞品监控 | 30 分钟更新一次")
    
    return "\n".join(msg)

def main():
    print("👀 竞品价格监控 - 演示版")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    # 模拟价格变化
    print("正在检查竞品价格...")
    print("")
    
    for i, product in enumerate(DEMO_PRODUCTS):
        print(f"[{i+1}/{len(DEMO_PRODUCTS)}] 检查：{product['name']}")
        
        # 随机生成价格变化（30% 概率）
        if random.random() < 0.3:
            old_price = product['current_price']
            # 新价格随机波动 -5% 到 +5%
            change_pct = random.uniform(-0.05, 0.05)
            new_price = old_price * (1 + change_pct)
            
            price_change = {
                "old": old_price,
                "new": new_price,
                "diff": new_price - old_price,
                "pct": (new_price - old_price) / old_price * 100
            }
            
            # 生成告警
            msg = generate_alert(product, price_change)
            
            print(f"  💰 价格变动：{old_price:.2f} → {new_price:.2f} ({price_change['diff']:+.2f}元)")
            
            # 保存到文件
            filename = f"demo_alert_{product['name'][:10]}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            output_file = OUTPUT_DIR / filename
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(msg)
            
            print(f"  ✅ 告警已保存：{output_file}")
        else:
            print(f"  ⚠️ 价格无变化")
        
        print("")
    
    # 生成汇总报告
    print("="*60)
    print("📊 竞品监控汇总报告")
    print("="*60)
    print("")
    
    for product in DEMO_PRODUCTS:
        status = "✅" if product['in_stock'] else "❌"
        print(f"{status} {product['name']}")
        print(f"   价格：¥{product['current_price']:.2f} (原价¥{product['original_price']:.2f})")
        print(f"   链接：{product['url']}")
        print("")
    
    print("="*60)
    print("💡 提示：这是演示版，使用模拟数据")
    print("   正式版会实时抓取真实价格")
    print("="*60)
    
    # 保存汇总报告
    report_file = OUTPUT_DIR / f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# 竞品监控演示报告\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 监控商品列表\n\n")
        for product in DEMO_PRODUCTS:
            status = "✅ 有货" if product['in_stock'] else "❌ 缺货"
            f.write(f"- {product['name']}\n")
            f.write(f"  - 价格：¥{product['current_price']:.2f}\n")
            f.write(f"  - 状态：{status}\n")
            f.write(f"  - 链接：{product['url']}\n\n")
    
    print(f"\n✅ 报告已保存：{report_file}")

if __name__ == "__main__":
    main()
