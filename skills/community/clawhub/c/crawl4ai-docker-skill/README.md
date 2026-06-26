# 🐳 Crawl4AI Docker Skill

专为 Docker 部署的 Crawl4AI 服务设计的技能包，提供完整的 REST API 调用指南和实用工具。

## 📦 技能内容

- **SKILL.md** - 详细的技能说明和使用指南
- **scripts/crawl4ai-docker.sh** - 便捷的 API 调用脚本
- **scripts/test-crawl4ai.sh** - 功能测试脚本
- **references/example-config.json** - 配置示例

## 🚀 快速开始

### 1. 验证服务状态

```bash
# 运行测试脚本
./scripts/test-crawl4ai.sh

# 或手动检查
./scripts/crawl4ai-docker.sh health
```

### 2. 基础使用

```bash
# 基础网页抓取
./scripts/crawl4ai-docker.sh crawl https://example.com

# LLM 智能提取
./scripts/crawl4ai-docker.sh llm https://example.com "总结主要内容"

# 网页截图
./scripts/crawl4ai-docker.sh screenshot https://example.com
```

### 3. 监控功能

```bash
# 查看系统监控
./scripts/crawl4ai-docker.sh monitor

# 访问网页监控面板
open http://localhost:11235/dashboard
```

## 🔧 配置说明

### LLM 配置

创建 `.llm.env` 文件：

```bash
# OpenRouter 配置
OPENROUTER_API_KEY=your-api-key
LLM_PROVIDER=openrouter/free
LLM_MAX_TOKENS=2000

# 或使用自定义 OpenAI 兼容 API
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://your-custom-api.com/v1
LLM_PROVIDER=openai/gpt-4o-mini
```

### Docker Compose 配置

参考 `references/example-config.json` 中的完整配置示例。

## 📚 详细文档

查看 `SKILL.md` 文件获取完整的 API 参考和使用示例。

## 🛠️ 故障排除

- **服务未启动**: 运行 `docker compose ps` 检查状态
- **API 调用失败**: 检查端口 11235 是否被占用
- **LLM 提取失败**: 验证 `.llm.env` 配置

## 🔗 相关链接

- [Crawl4AI 官方文档](https://docs.crawl4ai.com/)
- [GitHub 仓库](https://github.com/unclecode/crawl4ai)
- [Docker Hub](https://hub.docker.com/r/unclecode/crawl4ai)