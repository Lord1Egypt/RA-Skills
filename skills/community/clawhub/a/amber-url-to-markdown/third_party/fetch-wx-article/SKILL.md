---
name: fetch-wx-article
description: 获取微信公众号文章内容。使用 scrapling 抓取微信公众号文章并转换为 Markdown 格式。当用户分享微信公众号链接（mp.weixin.qq.com/s/xxx）并希望提取内容时使用。
---

# Fetch WeChat Article - 获取微信公众号文章

从微信公众号文章链接提取内容的 skill。

## 快速开始

```bash
python3 scripts/fetch_wx_article.py https://mp.weixin.qq.com/s/xxx
```

## 安装依赖

使用前需要先安装依赖：

```bash
pip install "scrapling[ai]" html2text
```

## 使用说明

**当以下情况时使用此 Skill**：

1. 用户分享微信公众号文章链接（`mp.weixin.qq.com/s/xxx` 格式）
2. 需要提取文章纯文本内容
3. 需要获取标题、作者、正文等信息

## 输出格式

- 返回 Markdown 格式的纯文本内容
- 默认忽略链接和图片（可按需调整脚本）

## 脚本功能

`scripts/fetch_wx_article.py` 支持：

- 命令行参数传入文章 URL
- 错误处理和异常提示
- 函数封装方便调用
- 自动将 HTML 转换为 Markdown

## 技术说明

- 使用 `scrapling` 处理复杂的微信公众号页面
- 使用 `html2text` 转换 HTML 到 Markdown
- 支持微信公众号文章链接：`https://mp.weixin.qq.com/s/xxx`

## 注意事项

- 需要网络连接
- 微信公众号文章通常包含复杂的 CSS/JS，scrapling 专门用于处理此类场景

---

_从微信公众号提取内容，方便后续处理和归档。_
