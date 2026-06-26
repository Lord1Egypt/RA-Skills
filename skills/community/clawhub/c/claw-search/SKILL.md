# Claw Search 🔍

通用免费的 Web Search API 服务，专为 AI Agents 设计。

## 功能

- 🔍 **Web 搜索** - 类似 Brave Search 的 Web Search API
- 🌐 **通用兼容** - 兼容 OpenClaw、Claude Code 等各种 Agent
- 🔑 **无需 API Key** - 使用 skillhub 后端，无需申请
- 🚀 **快速响应** - 优化的搜索体验
- 🐳 **Docker 部署** - 一键部署到任意服务器

## API 使用

### Web 搜索

```bash
curl -X POST https://api.claw-search.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "openclaw ai agent", "count": 10}'
```

### 搜索结果示例

```json
{
  "query": "openclaw ai agent",
  "count": 5,
  "results": [
    {
      "title": "openclaw-backup",
      "url": "https://clawhub.com/skill/openclaw-backup",
      "description": "OpenClaw Backup",
      "age": ""
    }
  ]
}
```

## API 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索关键词 |
| count | number | 否 | 返回结果数量 (默认 10, 最大 20) |
| offset | number | 否 | 分页偏移 |
| country | string | 否 | 国家代码 (默认 CN) |
| freshness | string | 否 | 时间范围: pd(天), pw(周), pm(月), py(年) |

## 部署

### Docker 部署 (推荐)

```bash
# 克隆或下载项目
cd claw-search

# 启动服务
docker-compose up -d

# 测试
curl https://api.claw-search.com/health
```

### 手动部署

```bash
# 安装依赖
npm install

# 启动服务
PORT=8080 npm start
```

## 环境变量

| 变量 | 说明 |
|------|------|
| PORT | 服务端口 (默认 8080) |
| TAVILY_API_KEY | Tavily API Key (可选) |
| BRAVE_API_KEY | Brave Search API Key (可选) |

## OpenClaw Skill 调用

```bash
node {baseDir}/scripts/search.mjs "搜索关键词"
node {baseDir}/scripts/search.mjs "搜索关键词" -n 10
```

## 支持的后端

1. **skillhub** (默认，免费) - 搜索 ClawHub 技能
2. **tavily** (需要 API Key) - AI 优化的通用搜索
3. **brave** (需要 API Key) - Brave Search

## 上传到 ClawHub

```bash
clawhub publish
```

## License

MIT
