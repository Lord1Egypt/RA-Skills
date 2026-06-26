#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册AI量化交易助手到OpenClaw
"""

import os
import json
import shutil
from pathlib import Path

def register_skill():
    """注册技能到OpenClaw"""
    
    print("🎯 注册AI量化交易助手到OpenClaw")
    print("=" * 60)
    
    # OpenClaw技能目录
    openclaw_skills_dir = Path("C:/Users/Administrator/.openclaw/workspace/skills")
    
    if not openclaw_skills_dir.exists():
        print(f"❌ OpenClaw技能目录不存在: {openclaw_skills_dir}")
        return False
    
    # 当前技能目录
    current_skill_dir = Path(__file__).parent
    
    # 目标目录
    target_dir = openclaw_skills_dir / "ai-quant-trader"
    
    print(f"📁 当前技能目录: {current_skill_dir}")
    print(f"📁 目标目录: {target_dir}")
    
    try:
        # 如果目标目录已存在，先备份
        if target_dir.exists():
            backup_dir = target_dir.with_name(f"{target_dir.name}_backup")
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.move(target_dir, backup_dir)
            print(f"📦 已备份旧版本到: {backup_dir}")
        
        # 复制技能文件
        print("📋 复制技能文件...")
        
        # 创建目标目录
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 需要复制的文件
        files_to_copy = [
            "__init__.py",
            "main.py",
            "broker.py",
            "data_provider.py",
            "strategy_gen.py",
            "auto_trader.py",
            "risk_manager.py",
            "stock_screener.py",
            "SKILL.md",
            "openclaw_integration.py"
        ]
        
        for file_name in files_to_copy:
            src_file = current_skill_dir / file_name
            if src_file.exists():
                shutil.copy2(src_file, target_dir / file_name)
                print(f"  ✅ {file_name}")
            else:
                print(f"  ⚠️  {file_name} (未找到)")
        
        # 创建用户数据目录
        user_data_dir = target_dir / "user_data"
        user_data_dir.mkdir(exist_ok=True)
        
        # 创建缓存目录
        cache_dirs = ["data_cache", "screener_cache", "screening_results"]
        for cache_dir in cache_dirs:
            (target_dir / cache_dir).mkdir(exist_ok=True)
        
        # 创建技能配置文件
        skill_config = {
            "name": "ai-quant-trader",
            "display_name": "AI量化交易助手",
            "version": "1.0.0",
            "description": "基于AKShare的AI驱动量化交易模拟系统",
            "author": "小火马",
            "entry_point": "openclaw_integration.openclaw_handler",
            "commands": [
                "/交易",
                "/策略", 
                "/自动",
                "/风控",
                "/选股",
                "/统计",
                "/数据",
                "/帮助"
            ],
            "dependencies": ["akshare", "pandas", "numpy"],
            "enabled": True,
            "registered_at": str(os.path.getmtime(__file__))
        }
        
        config_file = target_dir / "skill_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(skill_config, f, ensure_ascii=False, indent=2)
        
        print(f"📄 创建配置文件: {config_file}")
        
        # 创建README
        readme_content = """# AI量化交易助手 - OpenClaw技能

## 功能概述
基于AKShare的AI驱动量化交易模拟系统，支持7大核心功能：

1. 📈 模拟实时交易（蜻蜓点金手续费规则）
2. 🤖 AI策略生成（自然语言描述生成策略）
3. ⚡ AI策略优化（自动优化参数）
4. 🔄 自动交易执行（策略绑定自动交易）
5. 🛡️ 止盈止损管理（多层次风控）
6. 📊 策略胜率统计（专业绩效分析）
7. 🔍 AI实时选股（智能筛选推荐）

## 快速开始

### 1. 安装依赖
```bash
pip install akshare pandas numpy
```

### 2. 基本使用
```
/帮助                    # 查看所有命令
/交易 设置本金 100000    # 设置初始资金
/选股 今日推荐           # AI推荐今日股票
/数据 分析 600519       # 技术分析贵州茅台
```

### 3. 完整投资流程
```
1. /交易 设置本金 100000
2. /选股 今日推荐
3. /策略 生成 '价值投资策略'
4. /自动 启用 价值策略 600519
5. /风控 设置止损 600519 5%
6. /持仓                 # 监控持仓
7. /统计 价值策略        # 分析表现
```

## 命令参考

### 交易命令
- `/交易 设置本金 [金额]`   设置初始资金
- `/交易 买入 [代码] [数量]` 买入股票
- `/交易 卖出 [代码] [数量]` 卖出股票
- `/持仓`                   查看持仓

### 策略命令
- `/策略 生成 [描述]`       AI生成策略
- `/策略 优化 [策略名]`     优化策略参数
- `/策略 列表`             查看所有策略

### 选股命令
- `/选股 今日推荐`          AI推荐今日股票
- `/选股 筛选 [条件]`       按条件筛选股票

### 数据命令
- `/数据 价格 [代码]`       查看股票价格
- `/数据 分析 [代码]`       技术分析

## 注意事项
1. 所有交易均为模拟，不涉及真实资金
2. AI策略仅供参考，投资有风险
3. 数据来自AKShare，可能有延迟
4. 建议先小额测试，熟悉系统

## 技术支持
如有问题，请联系小火马AI助手。
"""
        
        readme_file = target_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📖 创建README: {readme_file}")
        
        print("\n" + "=" * 60)
        print("🎉 技能注册成功！")
        print("=" * 60)
        print("\n📋 下一步:")
        print("1. 重启OpenClaw网关")
        print("2. 在OpenClaw中使用命令:")
        print("   /交易 设置本金 100000")
        print("   /选股 今日推荐")
        print("3. 或直接调用: openclaw_integration.openclaw_handler()")
        
        return True
        
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    register_skill()