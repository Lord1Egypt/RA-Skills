#!/usr/bin/env python3
"""
CrewAI 讨论版运行脚本
先生，这个版本会运行带评审会议的完整流程
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_discussion import create_discussion_team

def run_discussion(product_idea: str):
    """运行带评审会议的完整流程"""
    
    print("=" * 70)
    print("🚀 CrewAI 产品分析 - 讨论版")
    print("=" * 70)
    print(f"\n📝 产品创意：{product_idea}")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n👥 参与角色:")
    print("  📊 市场调研分析师")
    print("  🎨 产品设计专家")
    print("  🏗️ 技术总监")
    print("  💻 全栈技术专家")
    print("  ✅ 质量专家")
    
    print("\n📋 工作流程:")
    print("  1️⃣  市场调研")
    print("  2️⃣  产品设计")
    print("  3️⃣  技术架构")
    print("  4️⃣  开发实现")
    print("  5️⃣  质量保障")
    print("  6️⃣  评审会议（所有角色讨论）⭐")
    
    print("\n" + "=" * 70)
    print("开始执行...")
    print("=" * 70 + "\n")
    
    try:
        # 创建团队
        crew = create_discussion_team(product_idea, verbose=True)
        
        # 执行
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ 分析完成！")
        print("=" * 70)
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"prd_discussion_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# PRD: {product_idea}\n\n")
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
        print("用法：python3.10 run_discussion.py <产品创意>")
        print("\n示例:")
        print('  python3.10 run_discussion.py "一个 AI 驱动的需求收集机器人"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_discussion(product_idea)
