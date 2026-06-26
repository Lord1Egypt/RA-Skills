# B站UP主成长助手 - SKILL.md

---
name: bilibili-up-master
description: "B站UP主成长运营助手 - 热门监控、数据分析、竞品研究、内容策划（已验证 macOS + OpenClaw）"
---

# B站UP主成长助手 v1.0

🐸 **B站UP主全能运营工具** - 已验证可用于 macOS + OpenClaw

## 功能概览

- 📊 **热门监控** - 实时追踪B站热门视频、热门话题，生成热门报告
- 🔍 **UP主分析** - 分析对标UP主数据、粉丝趋势、内容风格、涨粉速度
- 📈 **视频分析** - 单视频播放分析、互动数据、弹幕热词
- 💡 **内容策划** - 基于热门数据+竞品分析给出内容建议
- 📝 **报告生成** - 自动生成B站运营日报/周报

## 使用方法

### 监控热门
```
监控B站热门视频
查看今天B站热门
生成B站热门报告
```

### 分析UP主
```
分析B站UP主[UP主名称]
查一下[UP主]的粉丝数据
对比[UP主A]和[UP主B]
```

### 视频分析
```
分析视频[BV号]
看看这个视频为什么火
```

### 内容建议
```
给我一些B站内容建议
做什么类型视频容易火
最近热门趋势是什么
```

### 生成报告
```
生成B站运营日报
本周热门分析报告
```

## 技术细节

### 热门榜单URL（参考）
- 总榜: https://www.bilibili.com/ranking
- 动画: https://www.bilibili.com/ranking/bangumi/1/0/3/
- 音乐: https://www.bilibili.com/ranking/bangumi/3/0/3/
- 游戏: https://www.bilibili.com/ranking/bangumi/4/0/3/
- 科技: https://www.bilibili.com/ranking/bangumi/36/0/3/
- 生活: https://www.bilibili.com/ranking/bangumi/17/0/3/
- 美食: https://www.bilibili.com/ranking/bangumi/20/0/3/

### 关键页面
- UP主主页: `https://space.bilibili.com/{uid}`
- 视频页: `https://www.bilibili.com/video/{bvid}`
- 热门榜: `https://www.bilibili.com/ranking`

### API 接口（可选）
- 热门视频: `https://api.bilibili.com/x/web-interface/ranking/v2`
- UP主信息: `https://api.bilibili.com/x/web-interface/card`

## 运行规则

### 浏览器规则
- 默认使用内置浏览器：`profile="openclaw"`
- 每次动作前确认会话目标 tab
- 连续 2 次失败后改稳健路径
- 可选使用 `agent-reach` 读取B站内容

### 数据规则
- 热门数据每小时更新一次
- UP主数据每日更新
- 趋势分析需要至少 3 天数据积累
- 本地存储路径: `/tmp/bilibili-data/`

### 发布规则（可选扩展）
- 视频发布需要登录creator.bilibili.com
- 每次发布间隔建议 30 秒以上

## 核心能力

### 1. 热门监控
- 爬取各分区热门榜单
- 记录视频标题、播放量、点赞、投币、收藏
- 识别上升趋势视频
- 生成热门报告

### 2. UP主分析
- 基本信息（粉丝数、获赞数、简介）
- 最近视频数据
- 粉丝增长趋势
- 内容类型分析
- 更新频率

### 3. 视频分析
- 播放数据（播放、点赞、投币、收藏、分享）
- 弹幕热词
- 评论区热词
- 发布时间分析

### 4. 内容策划建议
- 基于热门分析推荐领域
- 推荐选题方向
- 最佳发布时间
- 标题/封面建议

## Persona（运营人设）

身份：蛙哥——B站十年老用户 🐸

语气：**接地气 + 数据控**
- 用数据说话
- 偶尔玩梗（"前方高能"、"2333"）
- 直接给结论，不绕弯子

示例回复：
- "这个UP主最近起号了，上周涨粉 2w+"
- "科技区现在是蓝海，做数码评测有搞头"
- "建议你周三晚上发，这个时段流量最好"

## 注意事项

1. B站反爬较严，避免频繁请求
2. 部分UP主数据需要登录才能查看
3. 热门数据有延迟，建议参考趋势而非实时
4. 遵守B站社区规范，不要过度爬取

## 常见问题

**Q: 数据获取失败？**
A: 检查网络环境，部分数据需要代理；可尝试使用 agent-reach 读取

**Q: UP主找不到？**
A: 尝试搜索全名、UID或直播间名称

**Q: 报告在哪里？**
A: 保存在 `/tmp/bilibili-data/reports/`

---

**版本**：1.0 (macOS 验证版)  
**验证日期**：2026-04-01  
**验证平台**：OpenClaw + macOS