---
name: feishu-calendar
description: 创建飞书日历事件和视频会议。通过日历 API 创建，自动关联飞书视频会议。
emoji: 📅
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires":
          {
            "bins": [],
            "env": [],
            "tokens": ["feishu_user_token"],
          },
      },
  }
---

# 飞书日历 & 视频会议

通过飞书日历 API 创建事件，可选择关联飞书视频会议。

## 准备工作

### 1. OAuth 授权（首次）

需要获取 user_access_token，流程：
1. 在飞书开放平台后台开通权限：
   - `calendar:calendar`
   - `calendar:calendar.event:create`
   - `vc:meeting`
2. 配置重定向 URL（如 `http://127.0.0.1:8080/callback`）
3. 生成授权链接并让用户授权

### 2. Token 管理

- access_token 有效期约 2 小时
- refresh_token 有效期约 30 天
- 过期后用 refresh_token 刷新

Token 保存在 `~/.openclaw/workspace/feishu_tokens.md`

## 使用方式

### 创建日历会议（带视频会议）

```bash
# 参数
USER_TOKEN="xxx"  # 从 feishu_tokens.md 读取
CALENDAR_ID="feishu.cn_xxx@group.calendar.feishu.cn"

# 时间戳计算（明天 10:00-11:00 北京时间）
START_TS="1772071200"  # 2026-02-26 10:00:00
END_TS="1772074800"    # 2026-02-26 11:00:00

# 创建日历事件（带视频会议）
# 根据用户输入选择添加字段，不要添加用户未指定的字段

# 必填字段
JSON='{
  "start_time": {"timestamp": "'"$START_TS"'", "timezone": "Asia/Shanghai"},
  "end_time": {"timestamp": "'"$END_TS"'", "timezone": "Asia/Shanghai"},
  "summary": "会议标题",
  "vchat": {"vc_type": "vc"}
}'

# 可选：用户指定描述时添加
# "description": "描述内容"

# 可选：用户指定地点时添加
# "location": "地点"

curl -s -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/${CALENDAR_ID}/events" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$JSON"
```

### 参数说明

根据用户输入决定是否包含以下字段：
- summary: 会议标题（必填）
- description: 会议描述（用户指定时）
- start_time: 开始时间（必填）
- end_time: 结束时间（必填）
- location: 会议地点（用户指定时）
- vchat.vc_type: 设为 "vc" 创建视频会议

### 时间戳计算

```python
import datetime
dt = datetime.datetime(2026, 2, 26, 10, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
timestamp = int(dt.timestamp())
```

### 获取用户日历 ID

```bash
curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
  -H "Authorization: Bearer $USER_TOKEN"
```

返回的 `calendar_id` 即为主日历 ID

## 返回结果示例

成功创建后，返回要点：
- 会议标题
- 日期和时间
- 会议链接

示例：
```
✅ 会议已创建！
📅 2026年2月27日 10:00-11:00
🎥 https://vc.feishu.cn/j/xxx
```

## 注意事项

- 如果用户没有指定描述（description），不要添加额外的描述
- 如果用户没有指定地点（location），不要添加
