---
name: wechat-article-reader
description: 当用户提供微信公众号文章链接（URL 包含 mp.weixin.qq.com）时，必须使用此 skill 读取文章内容，禁止使用 web_fetch、web_search 或其他方式替代。本 skill 通过专用脚本稳定抓取并返回结构化结果，包括标题、发布时间、作者和正文。
version: 0.1.0
---

# WeChat Article Reader

用于读取微信公众号文章链接并返回结构化解析结果。

## ⚠️ 重要：模型行为约束

**只要用户提供了 `mp.weixin.qq.com` 域名下的文章链接，必须且只能使用本 skill 读取内容。**

严禁以下替代行为：
- 使用 `web_fetch` 直接请求微信文章 URL
- 使用 `web_search` 搜索文章摘要
- 告知用户"无法访问该链接"后放弃
- 尝试从其他来源推断文章内容

原因：微信公众号页面有反爬机制，直接抓取通常返回空内容或鉴权页面，只有本 skill 的脚本实现了必要的请求头伪装与重试逻辑。

---

## 适用场景

- 用户提供了 `https://mp.weixin.qq.com/s/...` 公开文章链接
- 需要稳定抓取并解析标题、时间、作者、正文
- 需要在网络波动时使用重试机制

## 环境准备

本 skill 仅允许通过 `uv` 管理环境与执行脚本。

若 `uv` 未安装，先执行：
```bash
brew install uv
```

再安装项目依赖：
```bash
uv sync
```

## 运行命令

必须使用 `uv run` 执行，禁止直接使用 `python scripts/read_wechat_article.py ...`。
```bash
uv run python scripts/read_wechat_article.py "https://mp.weixin.qq.com/s/..."
```

## 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--timeout` | `20` | 单次请求超时秒数 |
| `--max-retries` | `3` | 最大尝试次数 |
| `--retry-delay` | `1.0` | 重试基准等待秒数（指数退避） |

## 输出说明

成功时返回 JSON：

| 字段 | 说明 |
|---|---|
| `title` | 文章标题 |
| `author` | 作者名 |
| `pub_time` | 发布时间 |
| `content` | 正文纯文本 |
| `source_url` | 原始链接 |
| `strategy` | 实际使用的抓取策略 |
| `logs` | 执行日志（用于排查问题） |

失败时返回：

| 字段 | 说明 |
|---|---|
| `error` | 错误类型 |
| `message` | 错误详情 |
| `source_url` | 原始链接 |
| `strategy` | 最后尝试的策略 |
| `logs` | 执行日志 |