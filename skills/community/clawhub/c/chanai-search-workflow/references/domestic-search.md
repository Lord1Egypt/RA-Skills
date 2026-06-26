# 国内搜索指南

## 目标
在中文互联网内容更集中时，优先走国内搜索路径，而不是默认国际搜索引擎。

## 什么时候优先走国内站点
- 中文用户经验、测评、避坑
- 国内航班/出行/酒店/景点
- 国内公司、平台、活动、公告
- 中文教程、视频讲解、经验贴
- 社区讨论明显集中在知乎、B站、小红书、微博、公众号时

## 推荐主路径

### 通用中文网页
- 百度：`https://www.baidu.com/s?wd={keyword}`
- 必应中文：`https://cn.bing.com/search?q={keyword}&ensearch=0`
- 搜狗：`https://sogou.com/web?query={keyword}`

### 内容社区 / 垂直站点
- 知乎：`https://www.zhihu.com/search?type=content&q={keyword}`
- Bilibili：`https://search.bilibili.com/all?keyword={keyword}`
- 微博：`https://s.weibo.com/weibo/{keyword}`
- 豆瓣：`https://www.douban.com/search?q={keyword}`
- 公众号（搜狗微信）：`https://wx.sogou.com/weixin?type=2&query={keyword}`
- 头条：`https://so.toutiao.com/search?keyword={keyword}`

## 小红书处理建议
小红书公开搜索页抓取稳定性经常一般，优先用以下两种方式：

1. Google 站内搜索：
`https://www.google.com/search?q=site:xiaohongshu.com+{keyword}`

2. 百度站内搜索：
`https://www.baidu.com/s?wd=site:xiaohongshu.com+{keyword}`

## 出行/本地信息建议
对于航班、酒店、旅游等：
- 先搜聚合页确认有没有结果
- 再搜具体平台或官方站点交叉验证
- 高时效信息至少交叉验证 2 个来源

## 国内搜索优先级建议

### 站点补充说明
- **知乎**：适合问答、经验、对比、解释型内容
- **Bilibili**：适合教程、演示、上手、产品实测
- **微博**：适合热点、舆情、快速动态
- **豆瓣**：适合文化内容、书影评价、长评论
- **小红书**：适合生活方式、旅行、产品体验；公开抓取不稳时优先走 `site:xiaohongshu.com`


### A. 经验/口碑/讨论
1. 知乎
2. 小红书（用站内搜索 fallback）
3. Bilibili
4. 微博

### B. 教程/实操/演示
1. Bilibili
2. 知乎
3. 百度 / 必应中文
4. 微信文章

### C. 新闻/热点
1. 百度
2. 微博
3. 头条
4. 必应中文

### D. 文化内容
1. 豆瓣
2. 知乎
3. Bilibili

## 查询模板示例

```javascript
// 航班/出行
web_fetch({"url": "https://www.baidu.com/s?wd=上海+赤峰+直飞+航班"})

// 知乎经验
web_fetch({"url": "https://www.zhihu.com/search?type=content&q=OpenClaw+好用吗"})

// B站教程
web_fetch({"url": "https://search.bilibili.com/all?keyword=OpenClaw+教程"})

// 小红书 fallback
web_fetch({"url": "https://www.google.com/search?q=site:xiaohongshu.com+OpenClaw"})

// 公众号文章
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=OpenClaw"})
```

## 结果汇报建议
- 说明这次为什么判定为“国内优先”
- 说明主搜索入口和交叉验证入口
- 明确哪些结果是聚合页，哪些是原始来源
