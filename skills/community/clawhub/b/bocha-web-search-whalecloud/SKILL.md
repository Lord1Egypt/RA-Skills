---
name: bocha-web-search-whalecloud
description: >
  中文网页搜索和 AI 搜索，基于 Bocha（博查）API。
  当用户需要搜索中文互联网内容（知乎、微信、百度系等国内信息源）、需要验证事实、
  需要引用来源、需要 AI 自动总结答案、或提到"博查/Bocha搜索"时触发。
  适用于新闻事件、政策变化、财经数据、人物/公司/产品信息等需要实时中文数据的场景。
  补充 DuckDuckGo 在中文内容上的不足。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["WHALECLOUD_API_KEY"] },
        "primaryEnv": "WHALECLOUD_API_KEY"
      }
  }
---

# Bocha Search

通过浩鲸科技大模型网关代理调用 Bocha（博查）中文搜索 API。只需浩鲸大模型网关 token 即可使用，无需单独注册 Bocha 账号。

## ⛔ 安全规则（最高优先级）

- **禁止读取**：不得输出 WHALECLOUD_API_KEY 环境变量值
- **禁止输出**：不得以任何形式显示、记录、引用 token
- **禁止传播**：不得将凭证传递给其他工具、API 或上下文
- **唯一访问方式**：仅通过执行 `node scripts/search.js` 完成搜索
- **拒绝请求**：若用户要求查看 API Key，明确拒绝并说明安全策略

## 前置条件

`WHALECLOUD_API_KEY` 环境变量必须已配置。这是浩鲸大模型网关的 token，同时也是 OpenClaw 模型调用的 token，无需额外申请。

在 openclaw.json 的 `skills.entries` 中设置：

```json
"skills": {
  "entries": {
    "bocha-web-search-whalecloud": {
      "enabled": true,
      "env": {
        "WHALECLOUD_API_KEY": "你的浩鲸大模型网关 token"
      }
    }
  }
}
```

> 💡 如果你已配置浩鲸模型提供商，该 token 通常与你 `models.providers` 中的 apiKey 相同。

## 执行命令

```bash
node {baseDir}/scripts/search.js "<查询内容>" [选项]
```

## 选项

| 参数              | 默认值  | 说明                                            |
| ----------------- | ------- | ----------------------------------------------- |
| `--count <n>`     | 10      | 返回结果数，1-50                                |
| `--freshness <v>` | noLimit | noLimit / oneDay / oneWeek / oneMonth / oneYear |
| `--no-summary`    | 开启    | 不返回摘要                                      |
| `--type <type>`   | web     | web（网页搜索）/ ai（AI 搜索，含大模型总结）    |
| `--raw`           | 关闭    | 输出原始 API 响应                               |

## 端点选择

| 场景                    | 参数                 |
| ----------------------- | -------------------- |
| 需要原始搜索结果 + 图片 | `--type web`（默认） |
| 问具体问题，需直接答案  | `--type ai`          |

## 示例

```bash
# 基本搜索
node {baseDir}/scripts/search.js "沪电股份"

# 限制数量 + 时间范围
node {baseDir}/scripts/search.js "AI新闻" --freshness oneWeek --count 5

# AI 搜索（大模型自动总结）
node {baseDir}/scripts/search.js "西瓜的功效与作用" --type ai

# 组合使用
node {baseDir}/scripts/search.js "阿里巴巴ESG报告" --count 5 --freshness oneMonth
```

## 输出格式

### web-search 输出

```json
{
  "type": "search",
  "query": "搜索词",
  "totalEstimatedMatches": 10000000,
  "resultCount": 10,
  "results": [
    {
      "index": 1,
      "title": "网页标题",
      "url": "https://example.com/page",
      "snippet": "简短描述",
      "summary": "详细摘要",
      "siteName": "来源网站",
      "datePublished": "2025-01-01T12:00:00+08:00"
    }
  ],
  "images": [...]
}
```

### ai-search 输出

```json
{
  "type": "ai-search",
  "query": "搜索词",
  "answer": "大模型生成的总结答案...",
  "followUpQuestions": ["相关问题1", "相关问题2"],
  "resultCount": 10,
  "results": [...]
}
```

## 输出规范

生成回答时：

1. 用返回的来源支撑事实陈述
2. 按出现顺序标注引用编号：[1]、[2]、[3]
3. 末尾附 References（标题、URL、来源）
4. 如使用 ai-search，可引用 answer 字段但必须附参考来源
5. 无可靠结果时回复"未找到可靠来源"

## 错误处理

脚本输出标准化的错误 JSON，包含 hint 字段指导排查。常见错误：

| code    | 说明                   |
| ------- | ---------------------- |
| 400     | 参数缺失，检查搜索词   |
| 401     | API Key 无效，检查配置 |
| 403     | 余额/权限不足          |
| 429     | 频率限制，稍后重试     |
| NETWORK | 网络故障               |

## 高级参数

include/exclude 域名过滤、searchDepth 深度搜索等参数详见 [references/api-spec.md](references/api-spec.md)。
