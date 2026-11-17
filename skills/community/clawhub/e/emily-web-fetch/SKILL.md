# Web Fetch Skill

## Description
抓取指定URL的网页内容，返回文本摘要或原始HTML。用于获取新闻、公告、数据页面等。

## Tools Provided
- `fetch(url)` - 抓取网页，返回文本内容（最多5000字符）

## Usage
助手调用此工具获取网页内容，然后进行分析、摘要或提取信息。

## Examples
用户：抓取 https://www.cls.cn/telegraph
助手：调用 web-fetch:fetch(url)，获取后返回内容并解读。

## Limitations
- 仅支持HTTP/HTTPS GET- 不处理JavaScript渲染的页面（静态HTML）
- 内容长度限制为5000字符，避免过大响应
- 需要目标网站允许爬取（遵守robots.txt）