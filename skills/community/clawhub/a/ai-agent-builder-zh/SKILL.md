---
name: ai-agent-builder-zh
description: >
  AI智能体开发 / AI Agent构建 / 智能体工作流 / agent builder。掌握工具调用、记忆管理、多步推理等核心能力，快速搭建客服机器人、数据分析代理、内容生成助手。适合工程师、产品经理、运营主管在企业自动化办公中应用，支持ChatGPT、Claude、文心一言等大模型集成。替代RPA重复劳动，提升团队研发效率30%+。常见搜索：怎样构建AI Agent、智能体开发教程、工作流自动化、大模型应用落地、客服机器人搭建、企业AI解决方案。
tags: [AI智能体, ai-agent, agent开发, 智能体构建, 工作流自动化, automation, 大模型集成, llm-integration, 工具调用, tool-calling, 多步推理, 企业自动化, RPA替代, 客服机器人]
---

# AI 智能体构建指南

帮助工程师和产品经理设计、开发具备工具调用、记忆管理与多步骤推理能力的 AI 智能体（AI Agent），覆盖主流大模型（ChatGPT、Claude、文心一言等）集成模式，适配钉钉、企业微信、Web 等平台部署场景。

## Tools Required
- 代码编辑器（VS Code / Cursor）
- LLM API（OpenAI / Anthropic / 百度千帆 / 阿里通义）
- 工作流平台（n8n / Dify / FastGPT，可选）
- 向量数据库（Milvus / Chroma，记忆模块可选）

## Usage
- "帮我设计一个能自动查询数据库并生成报表的 AI 智能体架构"
- "我想用 Claude API 搭建一个客服机器人，支持多轮对话和工单创建，怎么设计工具调用流程？"
- "如何给智能体加上长期记忆，让它记住用户的历史偏好和上下文？"

## Examples

输入：
我需要一个销售助理智能体，能查询 CRM 系统里的客户信息、生成跟进邮件，并自动记录到飞书文档。请设计架构和工具列表。

输出：

**智能体架构设计：销售助理 Agent**

**核心组件：**

```
用户输入（销售需求）
      │
      ▼
  Agent（LLM 推理层：Claude / GPT-4）
      │
  ┌───┼───────────┐
  │   │           │
  ▼   ▼           ▼
查询  生成      记录工具
工具  工具      （飞书API）
(CRM) (邮件模板)
```

**工具列表（Function Calling）：**

| 工具名 | 功能 | 输入参数 |
|--------|------|----------|
| `get_customer_info` | 查询 CRM 客户信息 | customer_id / name |
| `generate_followup_email` | 生成个性化跟进邮件 | customer_info, context |
| `save_to_feishu_doc` | 写入飞书文档 | doc_id, content |
| `search_deal_history` | 查询历史成交记录 | customer_id, date_range |

**多步推理流程：**

1. **理解意图**：解析销售人员输入，判断需要哪些工具
2. **查询客户**：调用 `get_customer_info` 获取基本信息 + `search_deal_history` 获取历史
3. **生成邮件**：基于客户画像调用 `generate_followup_email`，输出个性化内容
4. **记录存档**：调用 `save_to_feishu_doc` 将邮件草稿 + 操作记录写入飞书

**记忆管理建议：**
- **短期记忆**：对话上下文窗口（最近 10 轮）
- **长期记忆**：向量数据库存储客户偏好标签，每次对话前检索相关记忆注入 Prompt
- **工作记忆**：当前任务状态（已完成哪步、待执行哪步）存入 Redis

**关键代码片段（Python + OpenAI Function Calling）：**

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_info",
            "description": "从CRM系统查询客户基本信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "客户姓名或公司名"},
                },
                "required": ["customer_name"]
            }
        }
    },
    # 其他工具定义...
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": user_input}],
    tools=tools,
    tool_choice="auto"  # 让模型自动决定调用哪个工具
)
```

**部署建议：**
- 企业内部：通过企业微信 / 钉钉机器人接入，