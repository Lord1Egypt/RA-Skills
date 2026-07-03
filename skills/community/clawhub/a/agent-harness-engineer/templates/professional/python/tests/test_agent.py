"""
Agent 核心测试
规模: Professional
预期行数: ~100行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. 测试 AgentCore.run() 正常流程
2. 测试工具调用循环 (LLM 返回工具调用 → 执行 → 返回结果 → 继续)
3. 测试错误恢复 (模拟 LLM 错误, 验证重试/截断等策略)
4. 测试停止条件 (max_turns, manual stop)
5. 使用 pytest-asyncio 进行异步测试 (如果需要)

⚠ 使用 mock 模拟 LLM 客户端, 避免真实 API 调用
⚠ 测试应覆盖 7 个 Continue 站点
⚠ 使用 conftest.py 定义共享 fixtures (如有多个测试文件)
"""

import pytest

# TODO: 导入待测试模块
# from agent.core import AgentCore, AgentState, AgentStopReason

# TODO: 实现测试用例
# def test_agent_basic_run(): ...
# def test_agent_tool_loop(): ...
# def test_agent_error_recovery(): ...
# def test_agent_max_turns(): ...
# def test_agent_reset(): ...
pass