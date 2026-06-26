#!/usr/bin/env python3
"""
CrewAI 移动端极简版运行脚本
先生，这个版本专注于移动端 App，连接自建 OpenClaw
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_mobile import create_mobile_team

def run_mobile(product_idea: str):
    """运行移动端产品分析"""
    
    print("=" * 70)
    print("🚀 CrewAI 移动端极简版 - 连接自建 OpenClaw")
    print("=" * 70)
    print(f"\n📝 产品创意：{product_idea}")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n👥 团队（移动端专属）:")
    print("  📱 移动端产品经理 - 定义核心场景")
    print("  🛠️ 移动端技术负责人 - 跨平台方案")
    print("  🎨 UX 设计师 - 简单直观界面")
    
    print("\n📋 任务（只关注移动端核心）:")
    print("  1️⃣  移动端核心功能（不超过 5 个）")
    print("  2️⃣  跨平台技术方案（Flutter/React Native）")
    print("  3️⃣  移动端 UX 设计（大按钮，少输入）")
    print("  4️⃣  一页纸 PRD 总结")
    
    print("\n🎯 移动端原则:")
    print("  - 功能不超过 5 个（移动端特有场景）")
    print("  - 页面不超过 5 个")
    print("  - API 不超过 10 个（考虑弱网）")
    print("  - 跨平台框架（一套代码多端运行）")
    print("  - 预计时间：2-4 分钟")
    
    print("\n" + "=" * 70)
    print("开始执行...")
    print("=" * 70 + "\n")
    
    try:
        # 创建团队
        crew = create_mobile_team(product_idea, verbose=True)
        
        # 执行
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ 分析完成！")
        print("=" * 70)
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"prd_mobile_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# 移动端 PRD: {product_idea}\n\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(str(result))
        
        print(f"\n💾 结果已保存到：{output_file}")
        print(f"\n📊 输出预览:")
        print("-" * 70)
        result_str = str(result)
        print(result_str[:1500] + "..." if len(result_str) > 1500 else result_str)
        
        return result
        
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3.10 run_mobile.py <产品创意>")
        print("\n示例:")
        print('  python3.10 run_mobile.py "移动端 OpenClaw 连接 App"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_mobile(product_idea)
