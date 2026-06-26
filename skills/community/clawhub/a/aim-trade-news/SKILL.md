---
name: aim-trade-news
description: "外贸资讯查询：查询最近1~3天的外贸相关资讯，返回AI生成的标题和摘要。Use when: 用户询问外贸资讯、外贸动态、外贸新闻、进出口政策、国际贸易资讯、trade news。NOT for: 国内新闻、娱乐资讯、实时行情（汇率/股价）。"
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins: [python3]
---

# 外贸资讯查询

查询最近 1~3 天的外贸相关资讯，返回 AI 生成的标题和摘要。数据源为 AEP Gateway 的 trending_hub 服务。

## 何时使用

当用户要求：
- 查看最近的外贸动态、外贸新闻
- 了解进出口政策变化
- 获取国际贸易相关资讯

## 用户交互流程

1. 用户询问外贸资讯（如"最近有什么外贸新闻"、"最近3天的外贸动态"）
2. Agent 先运行自检确认凭证可用
3. 调用脚本查询资讯
4. 按格式化模板展示结果

## 使用前自检

**每次使用前必须先跑自检**：

```bash
python3 scripts/search_news.py --check-config
```

- `configured: true` → 继续查询流程
- `configured: false` → 暂停，按下文"[密钥配置](#密钥配置)"章节的 4 步引导用户配置凭证（无需用户自己改文件，agent 代写 `.env`），配好后重跑自检

**注意**：通过 JSON 输出的 `configured` 字段判断状态，不看进程退出码。

## 技术流程

skill 不缓存数据、不写本地存储，只需要 `AEP_AUTHORIZATION` 一个凭证即可运行，每次查询都实时调用 AEP Gateway。

```
读取凭证 → AEP Gateway trending_hub API → 解析返回 → JSON 输出
```

1. 从环境变量或 `.env` 读取 `AEP_AUTHORIZATION` 凭证
2. 调用 `https://aep.vemic.com/trending_hub/ai_collection`，传 `category: "foreign_trade"` 和 `recentDays`
3. 解析返回数据，提取 `aiTitle`、`summary`、`publishDate`、`url` 等字段
4. 以 JSON 格式输出

## 命令

```bash
# 查询最近 3 天（默认）
python3 scripts/search_news.py

# 查询最近 1 天
python3 scripts/search_news.py --days 1

# 查询最近 2 天
python3 scripts/search_news.py --days 2
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--days` | 查询最近几天的资讯，仅支持 1、2、3 | `3` |
| `--check-config` | 检查 AEP 凭证配置状态 | — |

## 输出格式

脚本输出 JSON：

```json
{
  "success": true,
  "dataUpdateTime": "2026-04-15 10:30:00",
  "dataSize": 15,
  "items": [
    {
      "aiTitle": "AI改写后的标题",
      "title": "原始标题",
      "publishDate": "2026-04-15",
      "url": "https://example.com/article",
      "summary": "AI生成的摘要内容"
    }
  ]
}
```

如果返回 `"success": false`，展示 `message` 字段中的错误信息。

## 展示格式

按以下格式展示每条资讯：

```
### {序号}. {aiTitle 或 title}
- **发布日期**：{publishDate}
- **AI摘要**：{summary}
- **原文链接**：[查看原文]({url})
```

头部信息：

```
## 外贸资讯（最近 {days} 天）
数据更新时间：{dataUpdateTime} | 共 {dataSize} 条
```

如果返回 0 条资讯：`最近 {days} 天暂无外贸资讯更新。`

## 密钥配置

通过 AEP 网关调用 API，需要 `AEP_AUTHORIZATION` 凭证（Bearer token 格式）。凭证存储在 skill 目录下的 `.env` 文件中（已 gitignore，不提交），脚本会自动补全 `Bearer` 前缀，只需填写 token 值。

**配置流程（首次使用或自检 `configured: false` 时）**：

1. 提示用户去 `https://tools.mentarc.cn/aim-skills/` 注册获取 `AEP_AUTHORIZATION`（Bearer token）
2. 用户把 token 粘到对话框里发给 agent（**不让用户自己编辑文件或设置环境变量**）
3. **agent** 把 token 写入 skill 目录下的 `.env`，格式：

   ```
   AEP_AUTHORIZATION=<用户提供的token>
   ```

4. 重跑 `python3 scripts/search_news.py --check-config` 确认 `configured: true`，再继续用户原请求

脚本内置的 `load_dotenv()` 自动读取 `.env`，环境变量优先于文件。更多约束（如跨 agent 禁止共享凭证）见 [references/aep-setup.md](references/aep-setup.md)。

## 文件说明

| 文件 | 用途 |
|------|------|
| `scripts/search_news.py` | 主脚本：凭证检查 + 资讯查询 |
| `agents/openai.yaml` | Agent 接口定义（display_name、default_prompt） |
| `references/aep-setup.md` | AEP 凭证配置指引 |
| `requirements.txt` | Python 依赖声明 |
| `.env` | 凭证文件（已 gitignore，不提交） |

## 规则

- 展示时优先使用 `aiTitle`（AI 改写标题），回退到 `title`（原始标题）
- 如果 API 请求失败，直接展示错误信息，不重试
- API 请求超时 30 秒，超时后返回网络错误
- skill 不缓存资讯数据，每次调用实时查询 API
- 查询范围仅限 1~3 天，不支持自定义时间范围
- 不适用于国内新闻、娱乐资讯、实时行情查询（汇率/股价）
