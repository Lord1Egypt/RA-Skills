# DomainAgentHub - 领域专家枢纽

智能判断任务领域，优先推荐成熟方案，无成熟方案时扩展创建专业Agent。

## 功能特性

- **领域判断**: 根据任务关键词快速判断属于哪个大领域
- **成熟方案检测**: 先检查该领域是否有成熟方案，优先推荐
- **按需扩展**: 没有成熟方案时，引导用户创建自定义Agent

## 6大领域

| 领域 | 关键词 | 示例任务 |
|------|--------|----------|
| **办公** | PPT、Word、Excel、表格、文档、幻灯片 | 做PPT，写报告，做表格 |
| **开发** | 代码、编程、开发、调试、bug、项目 | 写代码、改bug、搭建项目 |
| **金融** | 股票、交易、基金、回测、量化、策略、持仓 | 分析股票，回测策略、选股 |
| **研究** | 搜索、调研、查找、查资料、最新 | 查资料、竞品调研、行业分析 |
| **创意** | 写作、写文章、内容、创意、脚本、博客 | 写文章、创作内容、视频脚本 |
| **思考** | 思考、哲学、反思、规划、人生 | 深度思考、人生规划、哲学讨论 |

## 成熟方案

领域Agent可以集成多种成熟方案：

- **开发领域**: Claude Code, OpenCode, Cline, Cursor, Trae
- **金融领域**: AkShare, Tushare, Wind, Bloomberg
- **搜索领域**: 秘塔AI搜索, Brave Search, Perplexity, Tavily
- **写作领域**: Claude Prose, 秘塔写作猫, WPS AI, Notion AI
- **图像领域**: Stable Diffusion, 通义万相, DALL-E, Midjourney
- **视频领域**: 可灵, Runway, Pika
- **语音领域**: OpenAI TTS, ElevenLabs, 讯飞语音
- **办公领域**: WPS AI, Notion, 飞书

## 安装

```bash
clawhub install domain-agent-hub
```

## 使用

安装后，DomainAgentHub会自动判断用户任务所属领域，并推荐合适的解决方案。

## 许可证

MIT License
