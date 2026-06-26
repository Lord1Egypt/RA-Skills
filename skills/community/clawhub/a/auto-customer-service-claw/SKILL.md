---
name: auto-customer-service-claw
description: 自动客服应答虾 — 处理客户咨询的自动化回复系统。核心能力：意图识别与分类、知识库匹配、智能转人工判断、多轮对话管理。当以下情况时使用此 Skill：(1) 用户要求搭建或配置自动客服系统，(2) 需要处理客户咨询的自动化回复（售前、售后、账户问题等），(3) 需要配置 FAQ 知识库、意图识别规则或回复话术，(4) 需要启动/管理客服机器人服务，(5) 用户提到"客服"、"自动回复"、"智能客服"、"机器人客服"、"咨询"、"售前"、"售后"、"FAQ"、"问答"、"24小时客服"、"秒回"。
---

# 自动客服应答虾

## 概述

自动处理客户咨询，通过意图识别 + 知识库匹配实现秒级响应，复杂问题智能转人工。

## 工作流程

### 步骤 1：接收客户消息

监听客服渠道（飞书、微信、网站在线客服、APP 内客服等），实时接收客户消息。

### 步骤 2：意图识别与分类

读取 `references/intent-rules.md`，分析客户消息，识别咨询意图：
- 售前咨询（商品信息、价格、库存）
- 售后问题（退换货、物流、发票）
- 账户问题（登录、密码、会员）
- 投诉建议（产品问题、服务不满）
- 闲聊寒暄（打招呼、感谢）

### 步骤 3：知识库匹配

读取 `references/faq-database.md`，根据识别的意图搜索最匹配的答案：
- 精确匹配：关键词完全匹配
- 语义匹配：使用向量相似度计算
- 模糊匹配：处理拼写错误、同义词
- 上下文匹配：结合多轮对话历史

### 步骤 4：生成回复内容

读取 `references/response-templates.md`，根据匹配结果生成回复：
- 标准答案：直接返回知识库中的答案
- 动态答案：调用 API 获取实时数据（如库存、物流）
- 引导式回复：通过多轮对话收集信息
- 转人工提示：无法处理时引导转人工

### 步骤 5：智能转人工判断

识别需要转人工的场景：
- 连续 3 次未匹配到答案
- 客户明确要求人工客服
- 检测到负面情绪（愤怒、失望）
- 涉及退款、投诉等敏感问题

### 步骤 6：数据记录

记录每次对话（客户问题、匹配答案、客户反馈、是否转人工），用于持续优化知识库。

## 服务管理

使用 `scripts/chatbot-server.sh` 管理客服机器人服务：

```bash
# 启动服务
./scripts/chatbot-server.sh start

# 停止服务
./scripts/chatbot-server.sh stop

# 重新加载知识库
./scripts/chatbot-server.sh reload

# 测试问答效果
./scripts/chatbot-server.sh test "这个商品有货吗？"
```

## 知识库管理

使用 `scripts/knowledge-updater.sh` 更新知识库：

```bash
# 从 Excel 导入 FAQ
./scripts/knowledge-updater.sh import --file faq.xlsx

# 导出当前知识库
./scripts/knowledge-updater.sh export --output current_faq.xlsx
```

## 自定义配置

- **改 FAQ 知识库** → 编辑 `references/faq-database.md`
- **改意图识别规则** → 修改 `references/intent-rules.md`
- **改回复话术** → 修改 `references/response-templates.md`

## 环境依赖

- Python 3.8+
- `pip install flask transformers`
- 飞书插件（如接入飞书客服渠道）
