---
name: url-auto-fetch
description: "自动检测用户发送的 URL 链接并调用 amber-url-to-markdown 技能抓取内容"
homepage: https://github.com/OrangeViolin/amber-url-to-markdown
metadata: { "openclaw": { "emoji": "🔗", "events": ["message:received"], "requires": { "bins": ["python3"] } } }
---

# URL Auto Fetch Hook

## 功能说明

当用户发送消息时，自动检测消息中是否包含 URL 链接。如果检测到 URL，自动调用 `amber-url-to-markdown` 技能抓取网页内容并转换为 Markdown 格式。

## 触发条件

1. **纯 URL 消息** - 消息只包含 URL 链接
   ```
   https://mp.weixin.qq.com/s/xxx
   ```

2. **URL + 意图关键词** - 消息包含 URL 且有以下关键词：
   - 解析、转换、转成、转为、生成、抓取、爬取、下载
   - markdown、md、文章、内容

## 支持的网站

- 微信公众号 (mp.weixin.qq.com)
- 知乎 (zhihu.com)
- 掘金 (juejin.cn)
- CSDN (blog.csdn.net)
- GitHub (github.com)
- Medium (medium.com)
- 通用网页

## 配置

无需额外配置，Hook 会自动查找 `amber-url-to-markdown` 技能的脚本路径。

## 输出

- MD 文件：`/root/openclaw/urltomarkdown/{文章标题}.md`
- 图片：`/root/openclaw/urltomarkdown/images/knowledge_YYYYMMDD_HHMMSS/`

## 注意事项

- 需要安装 Python 3 和必要的依赖库
- 首次使用需要运行 `playwright install chromium`
- 网络连接需要稳定
