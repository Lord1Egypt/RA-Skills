# 主流广告投放平台对比

## 腾讯广告 (Tencent Ads / 原广点通)

### 资源位
- 微信：朋友圈、公众号、视频号、小程序
- QQ：QQ空间、QQ浏览器
- 腾讯视频、腾讯新闻、腾讯看点
- 优量汇（联盟流量）

### 特点
- 社交数据强：微信生态闭环，社交关系链
- 人群定向：基础属性+兴趣行为+设备+自定义人群包
- 出价方式：oCPM、oCPA、CPC、CPM
- 适合：电商、游戏、教育、金融、本地生活

### 核心API
- Marketing API: `https://developers.e.qq.com/`
- 支持：广告管理、数据报表、素材管理、人群管理

## 巨量引擎 (Ocean Engine / 字节系)

### 资源位
- 抖音、今日头条、西瓜视频、火山小视频
- 穿山甲（联盟流量）

### 特点
- 算法驱动：推荐系统强大，冷启动快
- 内容生态：短视频+直播闭环转化
- 人群定向：兴趣标签+行为+人群包+智能放量
- 出价方式：oCPM、oCPC、CPM、CPC
- 适合：电商、游戏、网服、本地生活

### 核心API
- Marketing API: `https://open.oceanengine.com/`
- 支持：广告管理、数据报表、素材管理、DMP人群

## 百度推广 (Baidu Ads)

### 资源位
- 百度搜索、百度信息流、百度贴吧、百度地图

### 特点
- 搜索意图强：关键词触发，转化意图明确
- 搜索+信息流双引擎
- 适合：B2B、教育、医疗、本地服务

## Meta Ads (Facebook/Instagram)

### 资源位
- Facebook：信息流、视频、Marketplace、右边栏
- Instagram：信息流、Stories、Reels、Explore
- Messenger、Audience Network

### 特点
- 用户规模：全球30亿+月活
- Advantage+：AI智能投放产品
- 适合：跨境电商、App推广、品牌出海

### 核心API
- Marketing API (Graph API)
- 版本：v19.0+ (2025)

## Google Ads

### 资源位
- Google搜索、Google Display Network、YouTube
- Gmail、Google Maps、Google Play

### 特点
- Performance Max：AI全自动投放
- 搜索意图精准
- 适合：跨境电商、B2B、SaaS

### 核心API
- Google Ads API v17
- Developer Token 申请制

## 平台对比速览

| 维度 | 腾讯广告 | 巨量引擎 | Meta Ads | Google Ads |
|------|----------|----------|----------|------------|
| 核心优势 | 社交闭环 | 算法推荐 | 全球规模 | 搜索意图 |
| 适合行业 | 电商/游戏 | 电商/网服 | 跨境/App | 跨境/B2B |
| 学习成本 | 中 | 低 | 中 | 高 |
| 素材形态 | 图文/视频 | 短视频/直播 | 图文/视频 | 文字/图文/视频 |
| 冷启动 | 较慢 | 最快 | 中 | 中 |
| 数据回传 | API/代码 | API/像素 | Pixel/CAPI | Gtag/GTM |
| 最低日预算 | ¥50 | ¥300 | $1 | $1 |
