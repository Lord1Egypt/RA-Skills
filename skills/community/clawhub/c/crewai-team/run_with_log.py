#!/usr/bin/env python3
"""
CrewAI 交互式运行脚本 - 显示详细讨论过程和模型配置
先生，这个版本会实时显示每个角色的思考过程、使用的模型、输入输出
"""

import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用已配置的 API Key
os.environ["OPENAI_API_KEY"] = "sk-sp-e0fb4e4a6dba43fb9bd707b8ef48bd6b"
os.environ["OPENAI_API_BASE"] = "https://coding.dashscope.aliyuncs.com/v1"

from team_config_multi_model import (
    market_analyst,
    design_expert,
    tech_director,
    fullstack_dev,
    qa_expert,
    create_product_team
)

def print_separator(title: str, char: str = "="):
    """打印分隔线"""
    width = 80
    print("\n" + char * width)
    if title:
        print(f"  {title}")
        print(char * width)

def print_agent_info(agent, model_name: str):
    """打印 Agent 信息"""
    print(f"\n👤 角色：{agent.role}")
    print(f"🎯 目标：{agent.goal}")
    print(f"🤖 使用模型：{model_name}")
    print(f"💬 详细输出：{'开启' if agent.verbose else '关闭'}")
    print(f"📋 允许委托：{'是' if agent.allow_delegation else '否'}")

def print_task_progress(task_name: str, status: str, agent_name: str):
    """打印任务进度"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{timestamp}] {status} - {task_name} ({agent_name})")

def run_with_discussion_log(product_idea: str):
    """运行并显示详细讨论日志"""
    
    print_separator("🚀 CrewAI 产品分析 - 详细讨论模式", "=")
    
    print(f"\n📝 产品创意：{product_idea}")
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 打印团队配置
    print_separator("👥 团队配置与模型映射", "=")
    
    agents_config = [
        (market_analyst, "市场调研分析师", "qwen3.5-plus", "¥0.004/1K tokens"),
        (design_expert, "产品设计专家", "qwen3-max-2026-01-23", "¥0.02/1K tokens"),
        (tech_director, "技术总监", "qwen3-coder-plus", "¥0.004/1K tokens"),
        (fullstack_dev, "全栈技术专家", "qwen3-coder-next", "¥0.004/1K tokens"),
        (qa_expert, "质量专家", "qwen3.5-plus", "¥0.004/1K tokens")
    ]
    
    print(f"\n{'角色':<20} {'模型':<25} {'成本':<20} {'特点':<15}")
    print("-" * 80)
    for agent, role, model, cost in agents_config:
        # 根据模型选择特点
        features = {
            "qwen3.5-plus": "均衡性价比",
            "qwen3-max-2026-01-23": "高质量创意",
            "qwen3-coder-plus": "架构设计专业",
            "qwen3-coder-next": "代码生成最强"
        }
        print(f"{role:<20} {model:<25} {cost:<20} {features.get(model, ''):<15}")
    
    print("\n💰 预估总成本：¥0.3-0.8 元/完整 PRD")
    print(f"⏱️  预计时间：5-10 分钟")
    
    # 打印工作流程
    print_separator("📋 工作流程", "=")
    workflow = [
        ("1️⃣", "市场调研", "📊 市场调研分析师", "用户画像、竞品分析、市场规模"),
        ("2️⃣", "产品设计", "🎨 产品设计专家", "功能列表、用户流程、验收标准"),
        ("3️⃣", "技术架构", "🏗️ 技术总监", "技术栈、架构设计、任务拆分"),
        ("4️⃣", "开发实现", "💻 全栈技术专家", "项目结构、代码示例"),
        ("5️⃣", "质量保障", "✅ 质量专家", "测试策略、用例设计"),
        ("6️⃣", "PRD 汇总", "🎨 产品设计专家", "整合所有输出")
    ]
    
    for step, task, agent, desc in workflow:
        print(f"\n{step} {task:<15} → {agent:<20}")
        print(f"   输出：{desc}")
    
    print_separator("🎬 开始执行", "=")
    
    try:
        # 创建团队（开启 verbose 模式）
        crew = create_product_team(product_idea, verbose=True)
        
        print(f"\n✅ 团队创建成功")
        print(f"   - Agent 数量：{len(crew.agents)}")
        print(f"   - 任务数量：{len(crew.tasks)}")
        print(f"   - 执行模式：Sequential（顺序执行）")
        
        print("\n" + "=" * 80)
        print("💬 实时讨论日志", "=" * 80)
        
        # 执行
        result = crew.kickoff()
        
        # 完成
        print("\n" + "=" * 80)
        print("✅ 分析完成！", "=" * 80)
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"prd_discussion_log_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# PRD: {product_idea}\n\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"模式：Sequential（多模型优化 + 详细日志）\n\n")
            f.write(str(result))
        
        print(f"\n💾 结果已保存到：{output_file}")
        
        # 打印摘要
        print_separator("📊 输出摘要", "=")
        result_str = str(result)
        print(result_str[:2000] + "...\n\n[内容过长，完整内容已保存到文件]" if len(result_str) > 2000 else result_str)
        
        # 打印统计
        print_separator("📈 执行统计", "=")
        print(f"总 Token 数：约 {len(result_str) / 4:.0f}（估算）")
        print(f"预估成本：¥0.3-0.8 元")
        print(f"执行时间：{(datetime.now() - datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')).seconds} 秒")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3.10 run_with_log.py <产品创意>")
        print("\n示例:")
        print('  python3.10 run_with_log.py "一个简化 OpenClaw 对接的 App"')
        sys.exit(1)
    
    product_idea = " ".join(sys.argv[1:])
    run_with_discussion_log(product_idea)
