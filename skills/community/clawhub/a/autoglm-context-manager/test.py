"""
Test script for Context Manager Skill integration.
"""
import sys
import asyncio
from pathlib import Path

# Add skill to path
SKILL_DIR = Path.home() / ".openclaw-autoclaw" / "skills" / "context-manager"
sys.path.insert(0, str(SKILL_DIR))

from skill import ContextManagerSkill


async def test_skill():
    """Test Context Manager skill."""
    print("=" * 60)
    print("Context Manager Skill Integration Test")
    print("=" * 60)

    skill = ContextManagerSkill()

    # Test 1: Help
    print("\n📋 Test 1: Help")
    response = await skill.handle_message("帮助")
    print(response[:500] + "..." if len(response) > 500 else response)

    # Test 2: Create Agent
    print("\n" + "=" * 60)
    print("🤖 Test 2: Create Agent")
    response = await skill.handle_message("为 '测试项目' 创建一个 Agent")
    print(response)

    # Test 3: List Agents
    print("\n" + "=" * 60)
    print("📋 Test 3: List Agents")
    response = await skill.handle_message("列出所有 Agent")
    print(response)

    # Test 4: Create File
    print("\n" + "=" * 60)
    print("📄 Test 4: Create File")
    test_content = """
# Context Manager 测试

这是一个测试文档，用于验证 Context Manager skill 的功能。

Context Manager 提供以下功能：
1. 向量索引 - 基于语义相似度的快速检索
2. 时间轴管理 - 按时间维度组织内容
3. 智能命中判断 - 双重阈值减少 LLM 调用
4. 多 Agent 支持 - 独立的命名空间

这个系统可以显著提高大型项目的完成度，同时降低成本。
"""
    response = await skill.handle_message(
        f"将以下内容保存到 Agent 测试项目的文件 'test_doc.md' 中：{test_content}"
    )
    print(response)

    # Test 5: List Files
    print("\n" + "=" * 60)
    print("📄 Test 5: List Files")
    response = await skill.handle_message("显示 Agent 测试项目的所有文件")
    print(response)

    # Test 6: Search (without details)
    print("\n" + "=" * 60)
    print("🔍 Test 6: Search (without details)")
    response = await skill.handle_message("在 Agent 测试项目中搜索 '向量索引'")
    print(response)

    # Test 7: Search (with details)
    print("\n" + "=" * 60)
    print("🔍 Test 7: Search (with details)")
    response = await skill.handle_message("查找 '语义相似度' 相关内容，并获取详情")
    print(response)

    # Test 8: Cross-agent search
    print("\n" + "=" * 60)
    print("🔍 Test 8: Cross-agent search")
    response = await skill.handle_message("在所有 Agent 中搜索 'Context Manager'")
    print(response)

    # Test 9: Get stats
    print("\n" + "=" * 60)
    print("📊 Test 9: System Statistics")
    from skill import context_manager
    stats = await context_manager.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    import json
    asyncio.run(test_skill())
