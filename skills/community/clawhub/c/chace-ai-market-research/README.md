# AI Market Research Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

> 整合 crawl4ai、trendradar、product-research 的全链路市场研究自动化技能

## ✨ 功能亮点

- 🔍 **深度抓取** - 利用 crawl4ai 从指定 URL 提取结构化内容
- 📈 **舆情监控** - 集成 trendradar 多平台热点追踪
- 🧠 **智能分析** - 基于 product-research 框架生成 SWOT/竞品矩阵
- 💾 **历史对比** - 自动与过往研究进行趋势对比（需 agentmemory）
- 📱 **即插即用** - 兼容 OpenClaw 技能系统，支持 CLI 与 API 调用

## 📦 安装

### 前置要求

- OpenClaw >= 2025.5.0
- Node.js 18+
- Python 3.10+ (crawl4ai 依赖)
- MCP 服务：
  - `crawl4ai` (localhost:11235)
  - `trendradar` (localhost:3333)

### 安装步骤

```bash
# 1. 克隆技能到本地
git clone https://github.com/yourusername/ai-market-research-skill.git \
  ~/.openclaw/workspace/.agents/skills/ai-market-research

# 2. 确保技能目录可执行
chmod +x ~/.openclaw/workspace/.agents/skills/ai-market-research/bin/run

# 3. 在 openclaw.json 中启用技能
# 编辑 ~/.openclaw/workspace/openclaw.json:
#   "skills": { "enabled": ["ai-market-research", ...] }

# 4. 重启 OpenClaw 网关
openclaw gateway restart
```

验证安装：
```bash
openclaw gateway status | grep ai-market-research
```

## 🚀 使用方法

### 命令行调用

```bash
cd ~/.openclaw/workspace
.agents/skills/ai-market-research/bin/run \
  --topic "宇树科技" \
  --depth standard \
  --sources "https://unitree.com","https://tesla.com/optimus" \
  --output_format markdown \
  --compare_previous true
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `--topic` | string | ✅ | - | 研究主题（产品/行业/赛道） |
| `--depth` | enum | ⭕ | `standard` | 研究深度：`quick`/`standard`/`deep` |
| `--sources` | CSV | ⭕ | 自动发现（待实现） | 数据源 URL 列表 |
| `--output_format` | enum | ⭕ | `markdown` | 输出格式：`markdown`/`html`/`json` |
| `--compare_previous` | bool | ⭕ | `true` | 是否对比历史研究 |

### 通过 OpenClaw 会话调用

在任意 OpenClaw 聊天中：
```
请用 ai-market-research 研究一下『人形机器人』赛道的主要玩家和技术路线。
```

系统会自动 spawn 子代理执行并返回报告。

### 定时任务集成

创建每日自动研究任务：
```bash
openclaw cron add \
  --name "每日市场简报" \
  --schedule "0 9 * * *" \
  --payload.agentTurn.message "用 ai-market-research 研究今日 AI 热点，深度 quick，输出到微信" \
  --delivery.announce.channel openclaw-weixin
```

## 📊 输出示例

报告默认保存在：
```
~/workspace/output/ai-market-research/
├── AI_聊天机器人_quick_20260526_1238.markdown
├── artifacts/
│   ├── crawl4ai_pages.json
│   ├── trendradar_news.json
│   └── analysis_result.json
```

Markdown 报告结构：
```markdown
# 主题 市场研究报告

**生成时间**: 2026-05-26 12:38
**研究深度**: quick

## 📰 热点追踪
- **AI 聊天机器人** 市场爆发式增长 (weibo 第1名)
...

## 🔍 深度分析
### 主要机会
- 领域热度上升
...

## 📈 历史对比
- 2026-05-20 AI 聊天机器人 研究
...
```

## ⚙️ 配置选项

### 默认配置（可在技能 config 中覆盖）

```json
{
  "default_depth": "standard",
  "max_sources_per_run": 30,
  "enable_historical_compare": true,
  "report_style": "wechat_friendly",
  "auto_push_to_channel": "openclaw-weixin"
}
```

在 `openclaw.json` 中添加：
```json
"plugins": {
  "entries": {
    "ai-market-research": {
      "enabled": true,
      "config": {
        "default_depth": "standard",
        "max_sources_per_run": 20
      }
    }
  }
}
```

## 🐛 故障排除

### 常见错误

**Error: No module named 'mcp'**
- 确保 `crawl4ai` MCP 服务已启动
- 检查 `openclaw.json` 中 `mcp.servers.crawl4ai` 配置

**Error: agentmemory 未安装**
- 已警告并跳过历史对比，不影响正常流程
- 如需对比功能，确认 `agentmemory` 插件已启用

**crawl4ai 抓取失败**
- 检查网络连通性
- 验证目标网站无反爬机制
- 调整 `request_interval`（crawl4ai 配置）

**报告生成失败 - 'list' object has no attribute 'get'**
- 这是历史对比数据类型不匹配的问题，已在 v0.1.0 修复
- 升级到最新版本

### 日志查看

```bash
# 查看 OpenClaw 主日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep ai-market-research

# 查看技能执行输出（如手动运行）
.agents/skills/ai-market-research/bin/run --topic "test" 2>&1 | tee /tmp/amr-test.log
```

## 🔧 开发与贡献

### 项目结构

```
ai-market-research/
├── SKILL.md           # 技能定义（必须）
├── README.md          # 本文档
├── LICENSE            # MIT 许可证
├── Requirements.md    # 依赖清单
├── bin/
│   └── run            # CLI 入口 (Node.js wrapper)
└── engine.py          # 核心编排引擎 (Python asyncio)
```

### 本地开发

```bash
# 直接运行引擎（无需 wrapper）
cd ~/.openclaw/workspace/.agents/skills/ai-market-research
echo '{"topic": "test", "depth": "quick"}' | python3 engine.py
```

### 测试

```bash
# 快速功能测试
bin/run --topic "OpenClaw" --depth quick --sources "https://openclaw.ai" --compare_previous false

# 验证输出
cat output/ai-market-research/*.markdown
```

## 📈 Roadmap

- [x] v0.1.0 - 基础编排框架（模拟数据）
- [ ] v0.2.0 - 真实 MCP 调用（crawl4ai + trendradar）
- [ ] v0.3.0 - product-research 深度集成
- [ ] v0.4.0 - 自动来源发现（Google 搜索）
- [ ] v0.5.0 - 向量历史对比（vector-memory）
- [ ] v1.0.0 - 生产就绪（完整测试 + CI/CD）

## 🤝 贡献

欢迎 PR 和 Issue！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)（待补充）。

## 📄 License

MIT © Chace

## 💬 支持

- 文档：https://github.com/yourusername/ai-market-research-skill/wiki
- 问题反馈：https://github.com/yourusername/ai-market-research-skill/issues
- OpenClaw 社区：https://openclaw.ai/community

---

**Made with ❤️ for OpenClaw Ecosystem**
