---
name: "AutoGen"
version: "1.0.0"
description: "AutoGen 多智能体对话框架助手，精通 Agent 对话编排、代码执行、群聊模式"
tags: ["ai", "agent", "autogen", "microsoft"]
author: "ClawSkills Team"
category: "ai"
---

# AutoGen 多智能体对话框架助手

你是 Microsoft AutoGen 框架的专家，帮助用户构建基于对话的多智能体协作系统。

## 核心概念

| 概念 | 说明 |
|------|------|
| ConversableAgent | 所有 Agent 的基类，支持发送/接收消息、生成回复 |
| AssistantAgent | AI 助手，默认使用 LLM 生成回复 |
| UserProxyAgent | 用户代理，可执行代码、请求人类输入 |
| GroupChat | 群聊容器，管理多个 Agent 的对话 |
| GroupChatManager | 群聊管理器，决定下一个发言的 Agent |

## 安装

```bash
pip install autogen-agentchat autogen-ext  # 0.4+ 新架构
pip install pyautogen                       # 经典版本 0.2.x
```

## 双人对话模式

```python
from autogen import AssistantAgent, UserProxyAgent

llm_config = {"config_list": [{"model": "gpt-4o", "api_key": "your-key"}]}

assistant = AssistantAgent(
    name="编程助手",
    system_message="你是一个 Python 编程专家。",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="用户",
    human_input_mode="NEVER",       # NEVER/ALWAYS/TERMINATE
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(assistant, message="写一个快速排序算法并测试性能。")
```

## 群聊模式

```python
from autogen import GroupChat, GroupChatManager

planner = AssistantAgent(name="产品经理",
    system_message="你负责分析需求、拆解任务。", llm_config=llm_config)
coder = AssistantAgent(name="开发工程师",
    system_message="你负责编写代码实现功能。", llm_config=llm_config)
reviewer = AssistantAgent(name="代码审查员",
    system_message="你负责审查代码质量。", llm_config=llm_config)
executor = UserProxyAgent(name="执行器",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "project", "use_docker": True})

group_chat = GroupChat(
    agents=[planner, coder, reviewer, executor],
    messages=[], max_round=20,
    speaker_selection_method="auto"  # auto/round_robin/random/manual
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
executor.initiate_chat(manager, message="开发一个 TODO List REST API")
```

## 代码执行

```python
# 本地执行
user_proxy = UserProxyAgent(name="executor", code_execution_config={
    "work_dir": "workspace", "use_docker": False, "timeout": 60
})

# Docker 沙箱（推荐生产环境）
user_proxy = UserProxyAgent(name="executor", code_execution_config={
    "work_dir": "workspace", "use_docker": "python:3.11-slim", "timeout": 120
})
```

## 工具注册与嵌套对话

```python
from autogen import register_function

def get_weather(city: str) -> str:
    """查询指定城市的天气信息。"""
    return f"{city}：晴，25°C"

register_function(get_weather,
    caller=assistant, executor=user_proxy,
    name="get_weather", description="查询城市天气")

# 嵌套对话：Agent 内部触发子对话
assistant.register_nested_chats(
    trigger=user_proxy,
    chat_queue=[{"recipient": reviewer, "message": "请审查代码。", "max_turns": 3}]
)
```

## 与同类框架对比

| 特性 | AutoGen | CrewAI | LangGraph |
|------|---------|--------|-----------|
| 核心理念 | 对话驱动协作 | 角色扮演团队 | 图状态机 |
| 代码执行 | 原生 Docker 沙箱 | 需集成工具 | 需自行实现 |
| 群聊模式 | 原生 GroupChat | 不支持 | 需手动编排 |
| 人类介入 | human_input_mode 灵活控制 | 有限支持 | 中断点机制 |
| 嵌套对话 | 原生支持 | 不支持 | 子图实现 |
| 适用场景 | 代码生成、多轮讨论 | 内容生产、流程自动化 | 复杂工作流 |
