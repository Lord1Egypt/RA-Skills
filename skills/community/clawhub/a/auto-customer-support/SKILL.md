---
name: auto-customer-support
description: 自动化客服（基于 FAQ 的轻量检索回复 + 简单转人工/工单接口；支持 Webhook 接入、邮件/企业微信/工单系统集成与可选升级到 LLM 混合模式）。
---

# 自动化客服 Skill

本 Skill 提供一个可运行的客服自动化 scaffold，适合快速搭建轻量客服机器人并接入外部渠道。默认实现是基于 FAQ 的检索+模板回复，并提供转人工/工单的接口。

适用触发语（示例）
- “帮我自动回复客服消息”
- “把这个接入到微信/邮箱，遇不到答案就转人工”
- “给我一份客服 FAQ 的示例和测试对话”

快速功能概览
- 加载 CSV 格式的 FAQ（intent, question_variants, answer）
- 基于简单关键词/模糊匹配选择最佳答案并渲染模板
- 可配置信心阈值，低信心时自动标记为需人工或创建工单
- 提供 /webhook 接口用于接收消息并返回回复（JSON），以及 /escalate 用于转人工

目录结构（已创建）
- scripts/server.py — Flask webhook 服务（主运行脚本）
- data/faq.csv — 示例问答对
- assets/templates/auto-reply.txt — 回复模板示例（变量支持）
- references/integration-guides.md — 渠道/集成与凭证说明
- examples/sample_conversation.md — 示例对话与测试用例

运行（快速上手）
1) 安装依赖：uv pip install flask
2) 启动服务（开发）：
   uv run python skills/auto-customer-support/scripts/server.py --port 5005
3) 测试请求：
   curl -X POST http://localhost:5005/webhook -H "Content-Type: application/json" -d '{"message":"如何退款","sender":"user-123"}'

输出（示例）
- 成功匹配时返回：{ "reply": "...", "confidence": 0.95, "escalate": false }
- 未匹配或低置信时返回：{ "reply": "抱歉，我不确定……我们将转人工处理。", "confidence": 0.35, "escalate": true }

扩展与升级点
- 将检索层替换成向量搜索（FAISS/Chroma）并接入 LLM 以生成更自然的回答
- 增加对话上下文管理与会话状态
- 集成渠道（企业微信/微信客服/邮箱/Zendesk）并实现双向消息同步

隐私与安全
- 不要把生产 API Key、密码粘贴到对话中；在部署时使用环境变量或受限凭证文件
- 自动回复前在测试环境做 100% 验证，避免误发敏感信息

下一步
- 我可以立刻在 workspace 中创建并启动服务供你本地测试；或根据你要接入的渠道（微信/邮箱/Zendesk）帮你生成对接示例。