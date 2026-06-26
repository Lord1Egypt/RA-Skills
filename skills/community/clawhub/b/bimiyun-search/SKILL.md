---
name: bimiyun-search
description: "比米云搜索（bimiyun search）：快速检索网络信息并返回LLM友好的数据，安全搜索默认启用。使用场景包括：当用户需要搜索网页信息、查找特定主题的资料、说出'比米云搜索'、'使用比米云'、'bimiyun搜索'、'搜索'、'查找'、'搜索一下'、'搜索网络'、'需要查找'、'帮我搜'、'查一下'、'搜索内容'、'搜索资料'、'搜索信息'、'搜索新闻'、'搜索知识'、'搜索答案'、'需要搜索'、'查找信息'、'查找资料'、'查找答案'等关键词时，以及需要快速从互联网获取答案的任何情况。支持 Markdown 格式（易读）和 JSON 格式（结构化数据）。"
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python"],"env":["BIMIYUN_API_KEY"]},"primaryEnv":"BIMIYUN_API_KEY"}}
---

# 比米云搜索

比米云搜索是一款快速、稳定的国内搜索 API，专为 LLM（大语言模型）和 AI 智能体设计，价格实惠且赠送额度可满足大多数需求。

## 准备工作

### 获取 API 密钥

1. 访问 [比米云官网](https://bimiyun.com)
2. 注册账号并登录
3. 进入控制台获取 API 密钥 (BIMIYUN_API_KEY)

### 配置方法

#### 方法 1 - 命令行参数
```bash
python scripts/bimiyun_search.py --query "如何学习Python" --api-key "your-key"
```

#### 方法 2 - 环境变量
```bash
# Windows
set BIMIYUN_API_KEY=your-key

# Linux/macOS
export BIMIYUN_API_KEY=your-key
```

#### 方法 3 - .env 文件
创建 .env 文件：
```
BIMIYUN_API_KEY=your-key
```

## 快速开始

```bash
# 默认：Markdown 格式（易读）
python scripts/bimiyun_search.py --query "如何学习Python"

# 指定语言和结果数量
python scripts/bimiyun_search.py --query "Python编程" --lang zh-CN --max-results 3

# 禁用安全搜索
python scripts/bimiyun_search.py --query "编程" --safe

# 原始 JSON 格式
python scripts/bimiyun_search.py --query "最新科技新闻" --format raw
```

## 选项说明

| 选项 | 说明 |
|------|------|
| --api-key | API 密钥（必填）|
| --query | 搜索查询（必填）|
| --max-results | 返回结果数（1-10，默认: 5）|
| --lang | 语言（默认: 自动检测）|
| --safe | 禁用安全搜索（默认: 启用）|
| --mode | 搜索模式：fulltext/详细（默认）, snippet/摘要 |
| --format | 输出格式：md/Markdown, raw/JSON |

## 输出格式

### Markdown（默认，推荐）
```markdown
1. Python入门教程 - 极客教程
   https://example.com/python-tutorial
   - 这是一篇关于Python入门的完整教程...
```

### JSON 格式
```json
{"query":"如何学习Python","results":[{"title":"教程","url":"https://...","content":"..."}]}
```

## 使用建议

- 对于大多数查询，使用 `--max-results 3-5` 即可
- 人类阅读推荐使用 Markdown 格式
- 程序处理推荐使用 raw 格式
- 安全搜索默认启用，适合家庭/办公环境
- 使用 `--lang zh-CN` 获取更好的中文搜索结果
