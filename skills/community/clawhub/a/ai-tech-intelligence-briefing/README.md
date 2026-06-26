# 🌅 Daily Intelligence Briefing / 每日情报简报

**双语版 / Bilingual Version**

A skill that generates daily AI/tech news briefings for global audiences.
自动生成每日 AI/科技新闻简报的技能，面向全球用户。

## Quick Start / 快速开始

```bash
# Generate today's briefing / 生成今日简报
python scripts/briefing.py generate

# Fetch a previous briefing / 获取历史简报
python scripts/briefing.py fetch 2026-03-10
```

## Features / 功能特性

- ✅ Auto-curates top AI/tech stories / 自动筛选顶级 AI/科技新闻
- ✅ Clean, shareable format / 简洁易分享的格式
- ✅ Saves to local folder / 自动保存到本地文件夹
- ✅ Configurable region/language / 可配置地区和语言
- ✅ Low token consumption / 低 token 消耗
- ✅ **Bilingual support (EN/ZH)** / **双语支持（中英文）**
- ✅ **Standalone - no workspace access** / **独立运行，不访问工作区**

## Configuration / 配置选项

Set these environment variables / 设置以下环境变量：

| Variable / 变量 | Default / 默认值 | Description / 描述 |
|----------------|-----------------|-------------------|
| BRIEFING_LANGUAGE | en | Language code: `en`, `zh` / 语言代码 |
| BRIEFING_REGION | global | Target region: `global`, `cn`, `us` / 目标地区 |
| BRIEFING_TOP_N | 10 | Number of stories: 1-20 / 新闻数量 |
| BRIEFING_OUTPUT_DIR | ./ | Output directory: path to save / 输出目录 |

## Output Format / 输出格式

The briefing is saved as:
简报保存为：
```
<BRIEFING_OUTPUT_DIR>/briefings/YYYY-MM-DD.md
```

## Security & Network / 安全与网络

### Network Behavior / 网络行为

This skill uses HTTP GET requests to fetch news from public RSS/API endpoints:
本技能使用 HTTP GET 请求从公开 RSS/API 端点获取新闻：

- ✅ **Read-only**: Only reads public news data / **只读**：只读取公开新闻数据
- ❌ **No Upload**: Does not send any user data / **不上传**：不发送任何用户数据
- ❌ **No Tracking**: Does not collect personal info / **不追踪**：不收集个人信息
- ❌ **No Workspace Access**: Does not access workspace files / **不访问工作区**：不访问工作区文件
- ❌ **No Subprocess Calls**: Pure Python implementation / **无子进程调用**：纯 Python 实现

### File System / 文件系统

- ✅ **Write-only**: Writes briefing files to configured output directory / **只写**：只将简报写入配置的输出目录
- ❌ **No Workspace Access**: Does not read from workspace / **不访问工作区**：不从工作区读取

## Monetization Ideas / 商业化想法

### Premium Version / 高级版
1. **More Sources** - Extended briefing with 50+ stories
   **更多源** - 扩展简报，包含 50+ 新闻
2. **Deeper Analysis** - AI-powered insights
   **深度分析** - AI 驱动的见解
3. **Custom Topics** - Focus on specific niches (crypto, startups, etc.)
   **自定义主题** - 聚焦特定领域（加密货币、创业等）

### Team Plans / 团队计划
- Shared team briefings with collaboration
   团队共享简报与协作
- Multi-user access with admin dashboard
   多用户访问与管理后台

### API Access / API 接入
- Embed briefings in other apps
   将简报嵌入其他应用
- Webhook notifications for daily updates
   通过 Webhook 通知每日更新

## Support the Author / 支持作者

If you find this skill useful, please support me:
如果您觉得这个技能有用，欢迎支持我：

**🇵🇪 PayPal: https://paypal.me/greatworks888**

## License / 许可证

MIT License - Free to use, modify, and distribute!
MIT 许可证 - 可自由使用、修改和分发！

---

Made with ❤️ by Sun Wukong (@greatworks)
Published on ClawHub 🚀
Repository: https://github.com/greatworks/ai-tech-intelligence-briefing