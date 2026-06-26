#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Usage Examples
演示如何使用Agency Agents Caller
"""

import sys
sys.path.insert(0, '.')
from agent_caller import AgentCaller

def demo_basic_usage():
    """基本使用示例"""
    print("="*70)
    print("Example 1: Basic Usage")
    print("="*70)
    
    caller = AgentCaller()
    
    # 统计
    total = caller.count_agents()
    print(f"\nTotal agents: {total}")
    
    # 搜索
    agents = caller.search_agents('AI')
    print(f"\nAI-related agents: {len(agents)}")
    
    for agent in agents[:3]:
        print(f"  - {agent['name']}: {agent['description'][:60]}...")
    
    caller.close()

def demo_category_browse():
    """分类浏览示例"""
    print("\n" + "="*70)
    print("Example 2: Browse by Category")
    print("="*70)
    
    caller = AgentCaller()
    
    # 获取分类
    categories = caller.get_categories()
    print(f"\nCategories: {', '.join(categories)}")
    
    # 浏览engineering类别
    agents = caller.get_agents_by_category('engineering')
    print(f"\nEngineering agents ({len(agents)}):")
    
    for agent in agents[:5]:
        print(f"  - {agent['name']}")
    
    caller.close()

def demo_get_specific_agent():
    """获取特定Agent示例"""
    print("\n" + "="*70)
    print("Example 3: Get Specific Agent")
    print("="*70)
    
    caller = AgentCaller()
    
    # 获取Backend Architect
    agent = caller.get_agent_by_name('Backend Architect')
    
    if agent:
        print(f"\nName: {agent['name']}")
        print(f"Category: {agent['category']}")
        print(f"Description: {agent['description']}")
        print(f"\nFull prompt length: {len(agent['full_content'])} characters")
        
        # 保存完整prompt
        with open('backend_architect_prompt.md', 'w', encoding='utf-8') as f:
            f.write(agent['full_content'])
        
        print("Full prompt saved to: backend_architect_prompt.md")
    
    caller.close()

def demo_random_agent():
    """随机Agent示例"""
    print("\n" + "="*70)
    print("Example 4: Random Agent")
    print("="*70)
    
    caller = AgentCaller()
    
    # 随机获取3个Agent
    print("\nRandom agents:")
    for i in range(3):
        agent = caller.get_random_agent()
        print(f"{i+1}. {agent['name']} ({agent['category']})")
    
    caller.close()

def demo_multi_agent_collaboration():
    """多Agent协作示例"""
    print("\n" + "="*70)
    print("Example 5: Multi-Agent Collaboration")
    print("="*70)
    
    caller = AgentCaller()
    
    # 组建团队
    team = [
        'Product Manager',
        'Backend Architect',
        'Frontend Developer',
        'UI Designer',
        'QA Engineer'
    ]
    
    print("\nBuilding a feature with multi-agent collaboration:")
    for role in team:
        agent = caller.get_agent_by_name(role)
        if agent:
            print(f"  - {agent['name']}: {agent['description'][:50]}...")
    
    caller.close()

if __name__ == "__main__":
    demo_basic_usage()
    demo_category_browse()
    demo_get_specific_agent()
    demo_random_agent()
    demo_multi_agent_collaboration()
    
    print("\n" + "="*70)
    print("Examples Complete!")
    print("="*70)
