# 常用搜索场景模板

## 1. 航班 / 出行 / 酒店

### 路由
优先 **domestic-first**。

### 主路径
1. 百度 / 必应中文做 broad lookup
2. 航旅/OTA/聚合页交叉验证
3. 若需要英文补源，再用 Google

### 关键词模板
- `{出发地} {目的地} 直飞 航班`
- `{出发地} {目的地} 航班 时刻表`
- `{城市} 酒店 推荐`
- `{景点} 攻略`

### 示例
```javascript
web_fetch({"url": "https://www.baidu.com/s?wd=上海+赤峰+直飞+航班"})
web_fetch({"url": "https://cn.bing.com/search?q=上海+赤峰+航班+时刻表&ensearch=0"})
```

## 2. GitHub / 技术文档 / API

### 路由
优先 **global-first**。

### 主路径
1. Google / DuckDuckGo HTML
2. 站内搜索 `site:github.com` / `site:docs.*`
3. 如果搜不到，再加 Brave 交叉验证

### 关键词模板
- `site:github.com {topic}`
- `site:docs.{vendor}.com {topic}`
- `{product} API docs`
- `{tool} changelog`

### 示例
```javascript
web_fetch({"url": "https://www.google.com/search?q=site:github.com+openclaw+memory+search"})
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+openclaw"})
```

## 3. 中文经验 / 口碑 / 对比

### 路由
优先 **domestic-first**。

### 主路径
1. 知乎
2. 小红书 fallback（Google/Baidu site）
3. Bilibili
4. 微博补热度

### 关键词模板
- `{产品} 好用吗`
- `{产品} 评测`
- `{产品A} {产品B} 对比`
- `{工具} 踩坑`

### 示例
```javascript
web_fetch({"url": "https://www.zhihu.com/search?type=content&q=OpenClaw+好用吗"})
web_fetch({"url": "https://www.google.com/search?q=site:xiaohongshu.com+OpenClaw"})
web_fetch({"url": "https://search.bilibili.com/all?keyword=OpenClaw+教程"})
```

## 4. 新闻 / 热点 / 最新动态

### 路由
按主题判断：
- 国内事件：**domestic-first**
- 国际事件：**global-first**
- 行业动态：可 mixed

### 主路径
1. 主搜索引擎 + 时间过滤
2. 第二来源交叉验证
3. 对高风险结论明确标注时间

### 示例
```javascript
web_fetch({"url": "https://www.google.com/search?q=AI+news&tbs=qdr:d&tbm=nws"})
web_fetch({"url": "https://search.brave.com/search?q=AI+news&tf=pw&source=news"})
```

## 5. PDF / 报告 / 白皮书

### 路由
大多数情况下 **global-first**；中文政策/行业材料可 domestic-first。

### 主路径
- `filetype:pdf`
- `site:` 限定机构域名
- 必要时加年份限制

### 示例
```javascript
web_fetch({"url": "https://www.google.com/search?q=AI+agent+filetype:pdf+2026"})
web_fetch({"url": "https://www.google.com/search?q=site:gov.cn+人工智能+filetype:pdf"})
```

## 6. 商品 / 参数 / 价格

### 路由
- 国内消费品：domestic-first
- 海外产品：global-first

### 主路径
1. 官方站
2. 电商/测评站
3. 社区口碑

### 示例
```javascript
web_fetch({"url": "https://www.baidu.com/s?wd=iPhone+16+参数"})
web_fetch({"url": "https://www.google.com/search?q=site:apple.com+iPhone+16+specs"})
```

## 7. 学术 / 研究 / 论文

### 路由
优先 **global-first**。

### 主路径
1. Google Scholar
2. arXiv / 官方实验室 / 论文主页
3. 普通 Google 补背景

### 示例
```javascript
web_fetch({"url": "https://scholar.google.com/scholar?q=agent+memory+retrieval"})
web_fetch({"url": "https://www.google.com/search?q=site:arxiv.org+agent+memory+retrieval"})
```
