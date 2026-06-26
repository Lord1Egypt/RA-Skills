# 群聊机器人 — 卡片模板参考

## 日报卡片
```json
{
  "title": "📋 今日工作日报",
  "blocks": [
    {"type": "text", "text": "📅 2026-05-07 周三"},
    {"type": "divider"},
    {"type": "text", "text": "✅ 已完成\n• 完成API接口开发\n• 修复3个线上bug"},
    {"type": "text", "text": "🔄 进行中\n• 用户反馈系统重构"},
    {"type": "text", "text": "🚧 阻塞项\n• 等待设计稿"},
    {"type": "divider"},
    {"type": "text", "text": "⏰ 明日计划: 完成重构 & 启动测试"}
  ]
}
```

## 投票卡片
```json
{
  "title": "🗳️ 本周团建投票",
  "blocks": [
    {"type": "text", "text": "请选择你喜欢的团建方式"},
    {"type": "buttons", "buttons": [
      {"label": "🏔️ 爬山", "value": "hiking"},
      {"label": "🍲 聚餐", "value": "dinner"},
      {"label": "🎤 KTV", "value": "ktv"},
      {"label": "🎮 桌游", "value": "boardgame"}
    ]}
  ]
}
```

## 进度通知卡片
```json
{
  "title": "📊 项目 Sprint #3 进度",
  "tone": "info",
  "blocks": [
    {"type": "text", "text": "████████░░ 80% 完成"},
    {"type": "context", "text": "12/15 任务 · 2天剩余 · 0阻塞"},
    {"type": "buttons", "buttons": [
      {"label": "查看详情", "url": "https://xxx.feishu.cn/docs/xxx"},
      {"label": "催促任务", "value": "remind"}
    ]}
  ]
}
```

## 提醒消息模板
```
🔔 提醒: {事件名称}
⏰ 时间: {时间}（{倒计时}分钟后）
📍 地点: {地点}
👥 参与人: {名单}
📎 资料: {链接}
```

## 欢迎语模板
```
👋 欢迎 {新成员} 加入 {群名称}！

📌 请先阅读：
• 群公告（置顶消息）
• 新人指南：{文档链接}

💬 自我介绍：
方便大家认识你~可以说说你在做什么、对什么感兴趣
```
