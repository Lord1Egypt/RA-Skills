---
name: bing-search-cn
description: 使用必应中文搜索引擎进行网络搜索和网页抓取
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "emoji": "🔍"}}
---

# bing-search-cn 技能

使用必应中文搜索引擎进行网络搜索和网页抓取。

## 工具

### 1. bing_search

必应搜索引擎搜索。

**参数：**
- `query` (必填): 搜索关键词
- `count` (可选): 返回结果数量，默认10条，最多50条
- `offset` (可选): 起始偏移，用于分页

**返回：**
- 搜索结果总数
- 每条结果的标题、链接、摘要、网站名称

### 2. bing_fetch

抓取网页内容（自动跳过黑名单网站）。

**参数：**
- `url` (必填): 要抓取的网页地址

**返回：**
- 网页标题
- 清理后的正文内容

### 黑名单

自动过滤的网站：
- 知乎 (zhihu.com)
- 小红书 (xiaohongshu.com)
- 微博 (weibo.com)
- 微信公众号 (weixin.qq.com)
- 抖音/TikTok (douyin.com, tiktok.com)
- B站 (bilibili.com)
- CSDN (csdn.net)

## 使用示例

```
"搜索人工智能最新进展"
"搜索Python教程，返回20条"
"抓取这个网页 https://example.com"
```

## 限制

- 需要能访问 cn.bing.com
- 建议每次搜索间隔1-2秒
- 搜索请求直接发送到必应，不存储日志
- 部分网站有反爬限制

## 技能路径

技能脚本位于: `{baseDir}/bing-search.js`

## 调用方式

通过 exec 工具调用:
```
node ~/.openclaw/skills/bing-search-cn/bing-search.js search "关键词" 数量 偏移
node ~/.openclaw/skills/bing-search-cn/bing-search.js fetch "网址"
```
