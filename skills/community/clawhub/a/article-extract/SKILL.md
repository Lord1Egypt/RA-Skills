---
name: article-extract
description: 提取微信公众号、博客、新闻等网页的正文内容，绕过反爬机制，纯文本输出。
---

# Article Extract

网页文章内容提取工具。支持微信公众号、博客、新闻网站等，输出干净的纯文本内容。

## 特点

- ✅ 绕过微信公众号反爬机制
- ✅ 自动过滤脚本、样式、导航等无关内容
- ✅ 纯 Python 实现，无需额外依赖
- ✅ 支持任意网页 URL

## 安装

无需安装，直接使用 Python 3 运行。

## 使用

```bash
python3 skills/article-extract/scripts/extract.py <url>
```

### 示例

```bash
# 提取微信公众号文章
python3 skills/article-extract/scripts/extract.py "https://mp.weixin.qq.com/s/xxxxx"

# 提取博客文章
python3 skills/article-extract/scripts/extract.py "https://example.com/blog/post"

# 保存到文件
python3 skills/article-extract/scripts/extract.py "https://mp.weixin.qq.com/s/xxxxx" > article.txt
```

## 输出

工具会输出提取的纯文本内容到 stdout，可以通过重定向保存到文件：

```bash
python3 skills/article-extract/scripts/extract.py "https://..." > output.txt
```

## 原理

1. 使用标准浏览器 User-Agent 发送 HTTP 请求
2. 解析 HTML，过滤 `<script>`、`<style>`、`<nav>`、`<footer>` 等无关标签
3. 提取正文文本并清理多余空格

## 限制

- 需要目标网页允许标准浏览器访问
- 对于需要登录或特殊权限的页面可能无法提取
- 某些动态加载的内容（如无限滚动）可能无法完整提取

## 依赖

- Python 3.6+
- 无需第三方库（仅使用标准库）

## 作者

基于 OpenClaw 社区实践封装
