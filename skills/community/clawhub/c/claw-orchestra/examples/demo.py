#!/usr/bin/env python3
"""
ClawOrchestra Demo - 展示完整用法

包含：
1. 四元组抽象
2. 动作空间
3. 编排器
4. 路由器（上下文、模型、工具）
"""

import sys
sys.path.insert(0, '.')

from core import AgentTuple, Orchestrator, Delegate, Finish, orchestrate, OpenClawAdapter
from router import ContextRouter, ModelRouter, ToolRouter, route_context, select_model, select_tools


def demo_four_tuple():
    """演示四元组抽象"""
    print("\n" + "="*60)
    print("📦 四元组抽象演示")
    print("="*60)
    
    # 创建四元组
    phi = AgentTuple(
        instruction="搜索 AOrchestra 论文的引用情况",
        context=["论文标题: AOrchestra", "作者: Xu et al.", "年份: 2026"],
        tools=["web_search", "web_fetch"],
        model="glm",
        role="🔍 researcher",
    )
    
    print(f"\n四元组: Φ = (I, C, T, M)")
    print(f"  I (Instruction): {phi.I}")
    print(f"  C (Context): {phi.C}")
    print(f"  T (Tools): {phi.T}")
    print(f"  M (Model): {phi.M}")
    
    print(f"\n转换为 sessions_spawn 参数:")
    params = phi.to_spawn_params(label="demo-agent")
    print(f"  task: {params['task'][:100]}...")
    print(f"  model: {params['model']}")
    print(f"  label: {params['label']}")


def demo_action_space():
    """演示动作空间"""
    print("\n" + "="*60)
    print("🎯 动作空间演示")
    print("="*60)
    
    # Delegate 动作
    delegate_action = Delegate(
        phi=AgentTuple.researcher("搜索 LangChain 最新版本"),
        reasoning="需要先收集 LangChain 的信息",
    )
    print(f"\nDelegate 动作:")
    print(f"  {delegate_action}")
    
    # Finish 动作
    finish_action = Finish(
        answer="LangChain 0.1.0 发布于 2024年1月",
        reasoning="所有子任务都已完成",
        confidence=0.95,
    )
    print(f"\nFinish 动作:")
    print(f"  {finish_action}")


def demo_context_router():
    """演示上下文路由器"""
    print("\n" + "="*60)
    print("🔀 上下文路由器演示")
    print("="*60)
    
    # 模拟历史
    history = [
        "搜索了 LangChain，发现它是一个 LLM 应用框架",
        "LangChain 的核心特性是链式调用",
        "CrewAI 是另一个框架，特点是角色扮演",
        "AutoGen 是微软的框架，支持多智能体",
        "这三个框架各有特点",
        "LangChain 的 GitHub stars 最多",
        "CrewAI 的文档最友好",
    ]
    
    router = ContextRouter(max_items=3, verbose=True)
    
    # 路由上下文
    task = "对比 LangChain 和 CrewAI 的优缺点"
    selected = router.route(task, history)
    
    print(f"\n任务: {task}")
    print(f"选择的上下文:")
    for i, ctx in enumerate(selected, 1):
        print(f"  [{i}] {ctx}")


def demo_model_router():
    """演示模型选择路由器"""
    print("\n" + "="*60)
    print("🤖 模型选择路由器演示")
    print("="*60)
    
    router = ModelRouter(
        available_models=["glm", "kimi", "sonnet", "gemini"],
        verbose=True,
    )
    
    # 测试不同任务类型
    tasks = [
        "搜索 LangChain 的最新版本",
        "实现一个排序算法",
        "对比三个 AI 框架的优缺点",
        "写一篇关于 AI 的博客文章",
        "规划一个复杂的项目架构",
    ]
    
    print("\n不同任务的模型选择:")
    for task in tasks:
        model = router.select(task)
        info = router.get_model_info(model)
        print(f"\n任务: {task[:30]}...")
        print(f"选择: {model} (层级: {info.tier.value if info else 'unknown'})")


def demo_tool_router():
    """演示工具选择路由器"""
    print("\n" + "="*60)
    print("🔧 工具选择路由器演示")
    print("="*60)
    
    router = ToolRouter(verbose=True)
    
    # 测试不同任务类型
    tasks = [
        "搜索 LangChain 的最新版本",
        "读取配置文件并修改",
        "运行测试脚本",
        "打开网页并截图",
    ]
    
    print("\n不同任务的工具选择:")
    for task in tasks:
        tools = router.select(task)
        print(f"\n任务: {task}")
        print(f"工具: {tools}")


def demo_orchestrator():
    """演示编排器"""
    print("\n" + "="*60)
    print("🎼 编排器演示（启发式模式）")
    print("="*60)
    
    # 创建编排器
    orchestrator = Orchestrator(
        main_model="sonnet",
        sub_models=["glm", "kimi", "gemini"],
        max_attempts=3,
        verbose=True,
    )
    
    # 执行任务
    result = orchestrator.run("帮我调研 LangChain 框架")
    
    print(f"\n{'='*60}")
    print(f"📋 最终结果:")
    print(f"{'='*60}")
    print(result[:500])


def demo_integrated_routing():
    """演示集成路由"""
    print("\n" + "="*60)
    print("🔗 集成路由演示")
    print("="*60)
    
    # 模拟场景：编排器收到一个任务
    task = "搜索并对比 LangChain 和 CrewAI"
    history = [
        "之前调研过 AutoGen 框架",
        "AutoGen 的特点是多智能体协作",
    ]
    
    print(f"\n任务: {task}")
    
    # 1. 上下文路由
    print("\n1️⃣ 上下文路由:")
    context = route_context(task, history, max_items=2)
    print(f"   精选上下文: {context}")
    
    # 2. 模型选择
    print("\n2️⃣ 模型选择:")
    model = select_model(task, available_models=["glm", "kimi", "sonnet"])
    print(f"   选择模型: {model}")
    
    # 3. 工具选择
    print("\n3️⃣ 工具选择:")
    tools = select_tools(task)
    print(f"   选择工具: {tools}")
    
    # 4. 构建四元组
    print("\n4️⃣ 构建四元组:")
    phi = AgentTuple(
        instruction=task,
        context=context,
        tools=tools,
        model=model,
        role="🔍 researcher",
    )
    print(f"   {phi}")


def main():
    """运行所有 demo"""
    print("\n" + "🎭 ClawOrchestra 完整 Demo " + "="*50)
    
    demo_four_tuple()
    demo_action_space()
    demo_context_router()
    demo_model_router()
    demo_tool_router()
    demo_orchestrator()
    demo_integrated_routing()
    
    print("\n" + "="*60)
    print("✅ Demo 完成!")
    print("="*60)
    print("\n已完成:")
    print("  ✅ 四元组抽象 (AgentTuple)")
    print("  ✅ 动作空间 (Delegate + Finish)")
    print("  ✅ 编排器骨架 (Orchestrator)")
    print("  ✅ 上下文路由器 (ContextRouter)")
    print("  ✅ 模型选择路由器 (ModelRouter)")
    print("  ✅ 工具选择路由器 (ToolRouter)")
    print("  ✅ OpenClaw 适配器 (OpenClawAdapter)")
    print("\n待完成:")
    print("  ⏳ 真正调用 sessions_spawn（需要在 OpenClaw 环境中测试）")
    print("  ⏳ LLM 决策集成（用于编排器的决策循环）")
    print("  ⏳ GAIA benchmark 适配")


if __name__ == "__main__":
    main()