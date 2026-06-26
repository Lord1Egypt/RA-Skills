#!/usr/bin/env python3
"""
CrewAI 极简实用版运行脚本
先生，这个版本只关注核心功能，去掉所有花里胡哨的东西
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_minimal import create_minimal_team

def run_minimal(product_idea: str):
    """运行极简版产品分析"""
    
    print("=" * 70)
    print("🚀 CrewAI 极简实用版 - 只保留核心功能")
    print("=" * 70)
    print(f"\n📝 产品创意：{product_idea}")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n👥 团队（只保留核心角色）:")
    print("  📋 产品经理 - 定义核心功能，砍掉不必要的")
    print("  🛠️ 技术负责人 - 简单技术方案，不整花活")
    print("  ✅ 测试工程师 - 只测主流程，能用就行")
    
    print("\n📋 任务（只关注核心）:")
    print("  1️⃣  核心功能（不超过 5 个）")
    print("  2️⃣  技术方案（越简单越好）")
    print("  3️⃣  核心测试（只测主流程）")
    print("  4️⃣  一页纸 PRD（总结所有）")
    
    print("\n🎯 极简原则:")
    print("  - 功能不超过 5 个")
    print("  - 数据表不超过 5 张")
    print("  - API 不超过 10 个")
    print("  - 输出一页纸 PRD")
    print("  - 预计时间：2-4 分钟")
    
    print("\n" + "=" * 70)
    print("开始执行...")
    print("=" * 70 + "\n")
    
    try:
        # 创建团队
        crew = create_minimal_team(product_idea, verbose=True)
        
        # 执行
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ 分析完成！")
        print("=" * 70)
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"prd_minimal_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# 极简 PRD: {product_idea}\n\n")
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
        print("用法：python3.10 run_minimal.py <产品创意>")
        print("\n示例:")
        print('  python3.10 run_minimal.py "一个简化 OpenClaw 对接的 App"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_minimal(product_idea)
