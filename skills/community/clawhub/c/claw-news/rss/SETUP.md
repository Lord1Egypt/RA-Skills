# Newsman Kimi API 配置指南

## 概述

Newsman 现已支持使用 Kimi Coding API (Allegretto 订阅) 进行 AI 驱动的新闻摘要生成。

## 快速配置

### 1. 设置 API Key

**方式一：环境变量 (推荐)**

```powershell
# PowerShell
$env:KIMI_API_KEY="your-allegretto-api-key"

# 永久设置 (用户级别)
[Environment]::SetEnvironmentVariable("KIMI_API_KEY", "your-allegretto-api-key", "User")
```

**方式二：修改配置文件**

编辑 `config/config.toml`：

```toml
[kimi]
api_key = "your-allegretto-api-key"  # 直接填写 (不推荐用于共享环境)
```

### 2. 选择 API 端点

Allegretto 订阅支持以下端点：

| 平台 | Base URL | 说明 |
|------|----------|------|
| Moonshot AI (中国) | `https://api.moonshot.cn/v1` | 中国区 API |
| Kimi Code | `https://api.kimi.com/coding/v1` | Coding 专用 |

修改 `config/config.toml`：

```toml
[kimi]
base_url = "https://api.moonshot.cn/v1"  # 或 "https://api.kimi.com/coding/v1"
```

### 3. 选择模型

| 模型 | 上下文长度 | 适用场景 |
|------|-----------|----------|
| `moonshot-v1-8k` | 8K | 短新闻摘要 (推荐) |
| `moonshot-v1-32k` | 32K | 长文章摘要 |
| `moonshot-v1-128k` | 128K | 超长文档 |
| `kimi-k2` | 256K | 深度分析 |
| `kimi-for-coding` | 256K | 技术内容 |

### 4. 测试配置

```bash
# 测试 API 连接
cd scripts
python kimi_client.py

# 测试摘要功能
python summarize.py --method api --verbose
```

## 使用方法

### 命令行使用

```bash
# 使用 API 模式生成摘要
python scripts/summarize.py --input news.json --method api --output summaries.json

# 生成中文摘要 (默认)
python scripts/summarize.py --input news.json --method api -v

# 获取科技新闻摘要
python scripts/fetch_news.py --category tech --output tech_news.json
python scripts/summarize.py --input tech_news.json --method api --output tech_summary.json
```

### 完整工作流

```bash
# 1. 获取新闻
python scripts/fetch_news.py --hours 24 --output news.json

# 2. AI 摘要 (Kimi API)
python scripts/summarize.py --input news.json --method api --output news_summary.json

# 3. 生成 Markdown 简报
python scripts/digest.py --input news_summary.json --format markdown --output digest.md
```

## 配置选项

编辑 `config/config.toml`：

```toml
[api]
provider = "kimi"  # 使用 Kimi API

[kimi]
base_url = "https://api.moonshot.cn/v1"
api_key = "${KIMI_API_KEY}"  # 从环境变量读取
model = "moonshot-v1-8k"     # 模型选择
max_tokens = 500             # 最大生成 token 数
temperature = 0.3            # 创造性 (0-1)

[summarization]
default_method = "api"       # 默认使用 API
max_length = 150             # 摘要长度 (词数)
chinese_output = true        # 生成中文摘要
```

## 故障排除

### API Key 无效

```
❌ API test failed: Kimi API error: 401 - {"error":"Unauthorized"}
```

**解决**: 检查 `KIMI_API_KEY` 环境变量是否正确设置

### 模型不存在

```
❌ API test failed: Kimi API error: 404 - {"error":"Model not found"}
```

**解决**: 确认 Allegretto 订阅包含该模型访问权限

### 速率限制

```
❌ API test failed: Kimi API error: 429 - Rate limit exceeded
```

**解决**: Allegretto 订阅有较高的速率限制，如仍触发可添加延迟重试

## Allegretto 订阅权益

作为次顶配订阅，Allegretto 提供：

- ✅ 高速 API 访问
- ✅ 更高的请求频率限制
- ✅ 优先模型访问
- ✅ 专业技术支持

如需查看具体配额，请访问 [Moonshot AI 控制台](https://platform.moonshot.cn/)。

## 更多信息

- [Kimi CLI 文档](https://moonshotai.github.io/kimi-cli/)
- [Moonshot API 文档](https://platform.moonshot.cn/docs/)
