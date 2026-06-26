
---
name: defuddle
description: 使用 Defuddle 库从任意网页提取主要内容并转换为 Markdown 格式。支持 CLI 和 Node.js 集成，用于内容爬虫、文本处理和自动化任务。
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "author": "Honcy Ye", "email": "honcy.ye@gmail.com"}}
---

# Defuddle 网页内容提取技能

使用 Defuddle 库从任意网页提取主要内容并转换为 Markdown 格式。

## 功能特性
- **内容提取**：自动检测并提取网页主要内容
- **Markdown 转换**：将 HTML 内容转换为 Markdown 格式
- **垃圾清理**：移除广告、侧边栏、评论等网页垃圾
- **CLI 支持**：提供命令行接口快速使用
- **Node.js 集成**：支持在 Node.js 环境中使用
- **自定义配置**：支持自定义内容选择器和选项

## 技术实现
- 使用 Defuddle 库进行网页内容提取
- 支持多种配置选项
- 提供简单易用的 API

## 使用方法

### 1. 命令行使用
```bash
# 解析 URL 并输出为 Markdown
npx defuddle parse https://example.com/article --markdown

# 解析本地 HTML 文件
npx defuddle parse page.html --markdown

# 输出为 JSON 格式（包含元数据）
npx defuddle parse page.html --json
```

### 2. 脚本使用
```bash
# 从 URL 提取内容并发送到微信文件传输助手
bash scripts/extract_and_send.sh "https://example.com/article" "文件传输助手"

# 从 URL 提取内容并发送到 Telegram
bash scripts/extract_and_send_telegram.sh "https://example.com/article" <chat_id>
```

### 3. Node.js API
```javascript
import { JSDOM } from 'jsdom';
import { Defuddle } from 'defuddle/node';

async function extractContent(url) {
  const response = await fetch(url);
  const html = await response.text();
  
  const dom = new JSDOM(html, { url });
  const result = await Defuddle(dom.window.document);
  
  return {
    title: result.title,
    content: result.content,
    markdown: result.contentMarkdown
  };
}
```

## 配置选项
- **markdown**: 转换为 Markdown 格式
- **debug**: 启用调试模式
- **contentSelector**: 自定义内容选择器
- **removeImages**: 移除图片
- **removeHiddenElements**: 移除隐藏元素

## 脚本说明
- `scripts/extract_content.sh`: 从 URL 提取内容并输出到控制台
- `scripts/extract_and_send.sh`: 提取内容并发送到微信
- `scripts/extract_and_send_telegram.sh`: 提取内容并发送到 Telegram

## 依赖
- Node.js 和 npm（用于 CLI）
- defuddle 库（已通过 npm 安装）

## 安装
```bash
npm install -g defuddle
```

## 注意事项
- Defuddle 需要 Node.js 环境（建议使用 Node.js 18 或更高版本）
- 某些网站可能有防爬虫机制，可能导致提取失败
- 大型网页内容提取可能需要较长时间
