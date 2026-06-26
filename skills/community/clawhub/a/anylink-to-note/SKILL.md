---
name: anylink-to-note
description: 将任意链接一键转化为结构化笔记。支持的链接类型：微信公众号文章、Get 笔记共享链接、RSS 播客订阅、任意公开网页。当用户分享或发送链接并希望"保存"、"解析"、"总结"、"收藏"时触发。输出包含标题、正文内容、摘要和标签。
---

# AnyLink to Note

**任意链接 → 结构化笔记，一键完成。**

## 支持的链接类型

| 链接类型 | 示例 | 提取方式 |
|---------|------|---------|
| 微信公众号 | `mp.weixin.qq.com/...` | Jina Reader |
| Get 笔记 | `d.biji.com/...` | Playwright 渲染 |
| RSS / 播客 | `xiaoyuzhoufm.com/...` | HTTP + XML 解析 |
| 公开网页 | 任意 URL | Jina Reader |

## 工作流程

### 1. 检测链接类型

```javascript
const host = new URL(url).host.replace(/^www\./, '');
// Get 笔记: /d\.biji\.com|biji\.com/.test(host)
// 微信公众号: /mp\.weixin\.qq|weixin\.qq/.test(host)
// RSS: url.includes('/feed') || url.includes('.xml')
```

### 2. 提取正文

**微信公众号 / 普通网页：**
```javascript
const res = await fetch(`https://r.jina.ai/${encodeURIComponent(url)}`, {
  headers: { Accept: 'application/json' }
});
const data = await res.json();
// → data.title, data.content
```

**Get 笔记：**
```bash
node skills/anylink-to-note/scripts/getnote.js <url>
```

**RSS 播客：**
```bash
curl -sL "<rss-url>" | python3 -c "import sys,xmltodict; d=xmltodict.parse(sys.stdin.read()); print(d['rss']['channel']['item'][0]['description'])"
```

### 3. 生成摘要 & 标签

用 LLM 根据正文内容生成：
- **摘要**：1-2 句话，概括核心内容或关键见解
- **标签**：3-5 个，以 `#` 开头，涵盖主题、人物、领域等维度

### 4. 返回结构化结果

```json
{
  "title": "文章标题",
  "content": "完整正文...",
  "summary": "1-2句摘要",
  "tags": ["#主题", "#领域", "#人物"],
  "sourceName": "WeChat" | "Get笔记" | "RSS" | "Web",
  "url": "<原始链接>"
}
```

## 注意事项

- **Playwright 环境**：Get 笔记提取依赖 Chromium，需确保已安装 `npx playwright install chromium`。
- **Jina Reader 限制**：部分网站（需登录、JS 渲染站）可能失败，此时可降级到 Playwright 方案。
