---
name: fastclaw-deployer
description: FastClaw是一款轻量级AI Agent运行时工具，支持通过OpenClaw Skills生态安装，提供内置Web界面、SOUL.md兼容、多模型支持等功能。
version: 1.1.0
author: yesong-Hue
homepage: https://clawhub.ai/yesong-Hue/fastclaw-ai-deployer
tags: [AI部署, Agent运行时, 轻量级, Web界面, OpenClaw兼容, SOUL.md, 多模型支持]
readme: |
  # FastClaw AI Agent 部署工具
  
  FastClaw是一款轻量级AI Agent运行时工具，完全兼容OpenClaw的SOUL.md体系，提供内置Web管理界面和极低的资源占用。
  
  ## 🎯 解决的问题
  
  - OpenClaw功能强大但较重，想要更轻量的方案
  - 需要图形界面来管理Agent，不想只用命令行
  - 想要快速部署一个AI助手给团队使用
  - 私有化部署需求，但不想花太多时间在运维上
  - 需要同时运行多个不同角色的Agent
  
  ## ✨ 核心优势
  
  | 维度 | OpenClaw | FastClaw |
  |------|---------|---------|
  | 内存占用 | 较大 | <10MB 极轻量 |
  | 图形界面 | ❌ 无 | ✅ 内置Web UI |
  | 安装大小 | 较大 | ~18MB |
  | 多渠道 | ✅ 飞书/微信/Telegram | ❌ 仅Web |
  | Skill生态 | 5700+ 社区技能 | 发展中 |
  | 适用场景 | 自动化中枢 | 轻量AI应用 |
  
  **推荐用法：** OpenClaw作为主控中枢（负责消息汇聚+自动化），FastClaw作为轻量辅助（特定场景的图形化Agent）。
  
  ## ✨ 核心功能
  
  ### 1. 轻量级设计
  - Windows仅18MB，macOS/Linux约8MB
  - 无需安装，下载即用
  - 不依赖Node.js、Python等运行时
  
  ### 2. 内置Web管理界面
  - 浏览器访问 http://localhost:18953 即可管理Agent
  - 直观的对话界面
  - Agent配置可视化编辑
  
  ### 3. SOUL.md体系完全兼容
  - 与OpenClaw生态完全兼容的Agent配置
  - 可以直接使用OpenClaw的SOUL.md模板
  - 支持多Agent多角色配置
  
  ### 4. 多模型支持
  支持多种LLM提供商：
  - **OpenRouter**: 聚合所有主流模型（推荐）
  - **OpenAI**: GPT-4、GPT-3.5
  - **Anthropic**: Claude 3.5、Claude 3
  - **Ollama**: 本地模型，完全免费
  - **自定义API**: 支持任意兼容OpenAI格式的API
  
  ### 5. 多Agent管理
  同时运行多个独立Agent，每个有独立SOUL.md配置。
  
  ### 6. 本地LLM支持
  支持Ollama本地模型，零API成本。
  
  ## 📦 安装
  
  通过OpenClaw Skills安装（推荐）：
  
  ```bash
  openclaw skills install fastclaw-deployer
  ```
  
  安装后，通过Web界面完成初始化配置。
  
  ## 🚀 快速开始
  
  1. **安装完成后**，访问 http://localhost:18953
  2. **配置LLM提供商的API Key**（推荐使用OpenRouter：https://openrouter.ai）
  3. **创建Agent**：设置名称、选择模型、编写SOUL.md
  4. **开始对话**：在Web界面中选择Agent即可开始
  
  ## 💡 推荐模型组合
  
  | 用途 | 模型 | 价格 |
  |------|------|------|
  | 日常轻量任务 | google/gemini-3.1-flash-lite-preview | 免费额度 |
  | 复杂推理写作 | openai/gpt-5.4 | 按量付费 |
  | 代码任务 | anthropic/claude-sonnet-4.6 | API |
  | 本地免费 | ollama/llama3.2 | 完全免费 |
  
  ## 💡 适用场景
  
  | 场景 | 说明 |
  |------|------|
  | 团队AI助手 | 快速部署给团队使用的内部AI助手 |
  | 客户服务 | 轻量级客服机器人 |
  | 数据查询 | 对接数据库的自然语言查询 |
  | 内容生成 | 写作、文案、代码生成 |
  | 本地开发 | 无需联网的本地LLM应用 |
  
  ## 📚 相关资源
  
  - **FastClaw GitHub**: https://github.com/fastclaw-ai/fastclaw
  - **OpenClaw**: https://github.com/openclaw/openclaw
  - **OpenRouter**: https://openrouter.ai
  - **Ollama（本地LLM）**: https://ollama.com
  - **ShadowAI API（推荐LLM提供商）**: https://referer.shadowai.xyz/r/1056448
  - **AI技能包集合**: [AI智造工坊](http://ai.qnitgroup.com)
  
  ## 📄 许可证
  
  MIT License
  
  ## 👤 作者
  
  yesong-Hue | [AI智造工坊](http://ai.qnitgroup.com)
---

# FastClaw Deployer

> 30分钟部署轻量级AI Agent运行时，单文件绿色版、内置Web界面、极低内存占用

## 推荐资源

- **ShadowAI API（推荐LLM提供商）**: https://referer.shadowai.xyz/r/1056448

---

*由 AI智造工坊 (http://ai.qnitgroup.com) 整理发布 | 安装源: ClawHub*