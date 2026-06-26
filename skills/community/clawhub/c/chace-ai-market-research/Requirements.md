# Requirements - ai-market-research 组合技能

## 技能依赖

### 必备 MCP 服务器
- `crawl4ai` - 网页抓取与提取
- `trendradar` - 舆情监控与分析

### 必备 OpenClaw 技能
- `product-research` - 市场分析框架
- `agentmemory` (插件) - 持久化存储
- `vector-memory` (可选但推荐) - 历史对比

### 系统要求
- Python 3.10+ (crawl4ai 需求)
- Node.js 18+ (OpenClaw 网关)
- 至少 8GB RAM (深度模式建议 16GB+)

## 安装清单

```bash
# 1. 启动 TrendRadar MCP
cd ~/.openclaw/workspace/TrendRadar
uv sync
uv run python -m mcp_server.server --transport http --port 3333 &

# 2. 启动 crawl4ai (如未运行)
# 参考: ~/.openclaw/workspace/crawl4ai/README.md

# 3. 验证 OpenClaw 配置
openclaw gateway status
# 应显示 mcp.servers.crawl4ai 和 mcp.servers.trendradar 均为 connected

# 4. 启用技能
# 在 openclaw.json 的 skills.enabled 列表中添加 "ai-market-research"
```

## 权限要求

该技能需要以下工具权限：
- `web_fetch` / `crawl4ai` - 抓取外部网页
- `trendradar__*` - 调用 TrendRadar MCP 工具
- `memory_save` / `memory_search` - 读写持久记忆
- `ctx_execute` - 执行分析脚本
- `write` - 生成报告文件

## 配置项

在 `openclaw.json` 的 `plugins.entries.ai-market-research.config` 中可设置：

```json
{
  "default_depth": "standard",
  "max_sources_per_run": 30,
  "enable_historical_compare": true,
  "report_style": "wechat_friendly",
  "auto_push_to_channel": "openclaw-weixin"
}
```

## 成本预估

- **crawl4ai**: 按页面计费（如使用云服务），本地运行仅计算电费
- **trendradar AI**: 每次分析约 10-30k tokens（取决于数据量）
- **OpenClaw LLM**: 报告生成约 50-150k tokens

建议设置 `token_budget` 限制每日消耗。

---