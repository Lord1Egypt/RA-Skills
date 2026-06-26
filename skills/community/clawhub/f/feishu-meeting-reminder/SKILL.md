---
name: feishu-meeting-reminder
description: |
  飞书会议自动提醒 - 会议前自动提醒参会人员，避免错过重要会议。
  
  **功能**：
  - 会议开始前 N 分钟自动提醒参会人
  - 支持设置重复提醒规则
  - 自动创建飞书日程并设置提醒
  - 支持查看即将到来的会议列表
  
  **触发条件**：
  - 用户提到"会议提醒"、"会议通知"、"开会提醒"、"提醒参会"
  - 用户要求创建会议或设置提醒
---

# 飞书会议自动提醒

## 🚨 执行前必读

- ✅ **时间格式**：ISO 8601 / RFC 3339（带时区），例如 `2026-02-28T14:00:00+08:00`
- ✅ **user_open_id 必填**：从消息上下文的 SenderId 获取（ou_...）
- ✅ **reminders 参数**：正数表示会前提醒，负数表示会后提醒（分钟）
- ✅ **首次添加参会人时自动创建飞书视频会议**

---

## 📋 快速索引

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 创建会议并提醒 | feishu_calendar_event | create | summary, start_time, end_time, user_open_id |
| 查看今日会议 | feishu_calendar_event | list | start_time, end_time |
| 查看会议详情 | feishu_calendar_event | get | event_id |
| 修改会议 | feishu_calendar_event | patch | event_id |
| 删除会议 | feishu_calendar_event | delete | event_id |
| 搜索会议 | feishu_calendar_event | search | query |

---

## 🛠️ 功能详解

### 1. 创建会议并设置提醒

创建会议并自动在会前提醒参会人：

```json
{
  "action": "create",
  "summary": "周例会",
  "description": "每周一上午10点例会",
  "start_time": "2026-03-31T10:00:00+08:00",
  "end_time": "2026-03-31T11:00:00+08:00",
  "user_open_id": "ou_xxx",
  "attendees": [
    {"type": "user", "id": "ou_xxx"},
    {"type": "user", "id": "ou_yyy"}
  ],
  "reminders": [
    {"minutes": 15},   // 会前15分钟提醒
    {"minutes": 5}     // 会前5分钟提醒
  ],
  "need_notification": true
}
```

**reminders 可选值**：
- 15：会前15分钟
- 10：会前10分钟
- 5：会前5分钟
- 0：会议开始时
- -30：会议结束后30分钟

### 2. 查看即将到来的会议

```json
{
  "action": "list",
  "start_time": "2026-03-31T00:00:00+08:00",
  "end_time": "2026-03-31T23:59:59+08:00",
  "user_open_id": "ou_xxx"
}
```

### 3. 会议冲突检测

在创建会议前检查时间冲突：

```json
{
  "action": "list",
  "start_time": "2026-03-31T09:00:00+08:00",
  "end_time": "2026-03-31T12:00:00+08:00",
  "user_open_id": "ou_xxx"
}
```

如果返回空结果则表示该时间段空闲。

### 4. 搜索会议

```json
{
  "action": "search",
  "query": "周例会"
}
```

---

## 💰 定价信息

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 基础会议创建、查看 |
| 专业版 | ¥12/月 | +自动提醒、重复提醒、冲突检测 |
| 企业版 | ¥39/月 | +批量创建、会议统计、API |

---

## 📝 使用示例

**用户说**："帮我创建一个明天上午10点的会议，主题是项目评审，参会人有张三和李四，会前15分钟提醒"

**执行步骤**：
1. 创建会议（带提醒）
2. 添加参会人
3. 确认创建成功

---

## 📚 附录：日历 API 限制

- 时间区间最长40天
- 返回实例数量上限1000
- 重复日程会自动展开为多个实例
