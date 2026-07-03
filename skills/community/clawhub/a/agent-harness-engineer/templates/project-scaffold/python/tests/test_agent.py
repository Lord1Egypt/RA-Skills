#!/usr/bin/env python3
"""
测试Agent核心功能
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.agent.core import AgentCore
from src.llm.client import LLMResponse, Message


@pytest.fixture
def mock_llm_client():
    """创建模拟的LLM客户端"""
    client = MagicMock()
    client.chat = AsyncMock(return_value=LLMResponse(
        content="Test response",
        tool_calls=[],
        usage={},
        model="test-model"
    ))
    return client


@pytest.fixture
def agent(mock_llm_client):
    """创建Agent实例"""
    agent = AgentCore(llm_config={
        "provider": "anthropic",
        "model": "test-model",
        "api_key": "test-key"
    })
    agent.llm_client = mock_llm_client
    return agent


@pytest.mark.asyncio
async def test_agent_run(agent, mock_llm_client):
    """测试Agent运行"""
    result = await agent.run("Hello")
    assert result == "Test response"
    mock_llm_client.chat.assert_called_once()


@pytest.mark.asyncio
async def test_agent_reset(agent):
    """测试Agent重置"""
    agent.state.messages.append(Message(role="user", content="test"))
    agent.reset()
    assert len(agent.state.messages) == 0
    assert agent.state.turn_count == 0
