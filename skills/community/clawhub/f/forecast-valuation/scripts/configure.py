#!/usr/bin/env python3
"""
Forecast & Valuation Skill 配置脚本
"""
import json
import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def configure():
    """配置 Forecast & Valuation Skill"""
    print("=" * 60)
    print("Forecast & Valuation Skill 配置向导")
    print("=" * 60)
    
    # 加载现有配置或创建新配置
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"\n📂 检测到现有配置文件：{CONFIG_FILE}")
    else:
        config = {}
        print(f"\n📝 创建新配置文件：{CONFIG_FILE}")
    
    # 配置 Gangtise
    print("\n--- 刚投 (Gangtise) 配置 ---")
    gangtise_key = input(f"刚投 Access Key [{config.get('GANGTISE_ACCESS_KEY', '')}]: ").strip()
    gangtise_secret = input(f"刚投 Secret Key [{config.get('GANGTISE_SECRET_KEY', '')}]: ").strip()
    
    if gangtise_key:
        config['GANGTISE_ACCESS_KEY'] = gangtise_key
    if gangtise_secret:
        config['GANGTISE_SECRET_KEY'] = gangtise_secret
    
    # 配置 Tushare
    print("\n--- Tushare 配置 ---")
    tushare_token = input(f"Tushare Token [{config.get('TUSHARE_TOKEN', '')}]: ").strip()
    if tushare_token:
        config['TUSHARE_TOKEN'] = tushare_token
    
    # 配置默认参数
    print("\n--- 默认估值参数 ---")
    print(f"当前无风险利率：{config.get('WACC_DEFAULT', {}).get('risk_free_rate', 2.5)}%")
    print(f"当前市场风险溢价：{config.get('WACC_DEFAULT', {}).get('market_risk_premium', 7.0)}%")
    print(f"当前永续增长率：{config.get('VALUATION_DEFAULT', {}).get('terminal_growth', 2.0)}%")
    
    # 保存配置
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 配置已保存到：{CONFIG_FILE}")
    
    # 测试配置
    print("\n--- 配置测试 ---")
    if config.get('GANGTISE_ACCESS_KEY'):
        print("✅ 刚投 Access Key: 已配置")
    else:
        print("⚠️  刚投 Access Key: 未配置（将使用手动录入模式）")
    
    if config.get('TUSHARE_TOKEN'):
        print("✅ Tushare Token: 已配置")
    else:
        print("⚠️  Tushare Token: 未配置（将使用手动录入模式）")
    
    print("\n" + "=" * 60)
    print("配置完成！现在可以运行：")
    print("  python3 scripts/build_forecast.py \"公司名称\" \"股票代码\"")
    print("=" * 60)

if __name__ == '__main__':
    configure()
