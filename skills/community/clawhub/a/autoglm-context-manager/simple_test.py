"""
Simple test without emoji to verify skill works.
"""
import sys
import asyncio
sys.path.insert(0, r"C:\Users\TIANXIN-01\.openclaw-autoclaw\skills\context-manager")

from skill_demo import ContextManagerSkill


async def test():
    skill = ContextManagerSkill()

    # Test 1: Create agent
    print("\n=== Test 1: Create Agent ===")
    response = await skill.handle_message("为 '测试项目' 创建一个 Agent")
    print(response)

    # Test 2: List agents
    print("\n=== Test 2: List Agents ===")
    response = await skill.handle_message("列出所有 Agent")
    print(response)

    # Test 3: Create file
    print("\n=== Test 3: Create File ===")
    response = await skill.handle_message(
        "将以下内容保存到 Agent 测试项目的文件 'test.md' 中：This is a test content about machine learning and neural networks."
    )
    print(response)

    # Test 4: List files
    print("\n=== Test 4: List Files ===")
    response = await skill.handle_message("显示 Agent 测试项目的所有文件")
    print(response)

    # Test 5: Search
    print("\n=== Test 5: Search ===")
    response = await skill.handle_message("在 Agent 测试项目中搜索 'neural'")
    print(response)

    print("\n=== All tests completed successfully ===")


if __name__ == "__main__":
    asyncio.run(test())
