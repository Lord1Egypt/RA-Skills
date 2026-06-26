# 飞书配置模板（Feishu Config Example）

> 用途：family-cultivation-coach Skill 调用飞书 API 的配置模板
> 复制本文件为 `feishu_config.md` 后，填入自己的飞书域名、App Token 和 Table ID。
> `feishu_config.md` 是本地私有配置，不要提交到公开仓库。

---

## 应用信息

| 项目 | 值 |
|------|----|
| 多维表格名称 | 家庭养育系统 |
| App Token | `<YOUR_BITABLE_APP_TOKEN>` |
| 飞书域名 | `<YOUR_TENANT>.feishu.cn` |

---

## 表 ID

| 表名 | Table ID | 用途 |
|------|----------|------|
| 孩子画像 | `<TABLE_ID_CHILD_PROFILE>` | 基础信息，每次对话优先读取 |
| 课表版本 | `<TABLE_ID_SCHEDULES>` | 课表生成和更新时写入 |
| 每日记录 | `<TABLE_ID_DAILY_LOGS>` | 日常记录，只存当天已发生的事 |
| 每日日报 | `<TABLE_ID_DAILY_REPORTS>` | 每日生成并推送 |
| 每周复盘 | `<TABLE_ID_WEEKLY_REVIEWS>` | 每周汇总分析 |
| 累积洞察 | `<TABLE_ID_INSIGHTS>` | 长期趋势和规律 |
| 临时活动 | `<TABLE_ID_TEMP_EVENTS>` | 未来临时事件，日报/复盘/速记卡均来此查询 |

---

## API 调用基础路径

```text
# 读取表记录
GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records

# 写入新记录
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records

# 更新已有记录
PUT https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}

# 查询记录（带过滤条件）
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search
```

将上方路径中的变量替换为：

- `{app_token}` → `<YOUR_BITABLE_APP_TOKEN>`
- `{table_id}` → 对应表的 Table ID

---

## 常用查询示例

### 读取当前执行中的课表

```json
POST /apps/<YOUR_BITABLE_APP_TOKEN>/tables/<TABLE_ID_SCHEDULES>/records/search
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "状态",
        "operator": "is",
        "value": ["当前执行中"]
      }
    ]
  }
}
```

### 读取最近14天每日记录

```json
POST /apps/<YOUR_BITABLE_APP_TOKEN>/tables/<TABLE_ID_DAILY_LOGS>/records/search
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "日期",
        "operator": "isAfter",
        "value": ["14daysAgo"]
      }
    ]
  },
  "sort": [{ "field_name": "日期", "order": "DESC" }]
}
```

### 写入每日记录

```json
POST /apps/<YOUR_BITABLE_APP_TOKEN>/tables/<TABLE_ID_DAILY_LOGS>/records
{
  "fields": {
    "日期": "<TODAY_TIMESTAMP>",
    "孩子昵称": "<CHILD_NICKNAME>",
    "整体状态": "正常",
    "执行情况": ["英语输入", "睡前故事"],
    "亮点时刻": "<TODAY_HIGHLIGHT>",
    "困难点": "<TODAY_DIFFICULTY>",
    "孩子情绪": "稳定",
    "家长情绪": "稳定",
    "自由记录": "<FREE_NOTE>",
    "记录来源": "Skill写入"
  }
}
```

---

## 给 OpenClaw 的配置指令模板

```text
请保存以下飞书多维表格配置，后续所有养育系统相关的飞书操作都使用这份配置：

App Token：<YOUR_BITABLE_APP_TOKEN>
飞书域名：<YOUR_TENANT>.feishu.cn

表 ID 对应关系：
- 孩子画像：<TABLE_ID_CHILD_PROFILE>
- 课表版本：<TABLE_ID_SCHEDULES>
- 每日记录：<TABLE_ID_DAILY_LOGS>
- 每日日报：<TABLE_ID_DAILY_REPORTS>
- 每周复盘：<TABLE_ID_WEEKLY_REVIEWS>
- 累积洞察：<TABLE_ID_INSIGHTS>
- 临时活动：<TABLE_ID_TEMP_EVENTS>

配置保存后，请做以下验证：
1. 调用飞书 API 读取「孩子画像」表的所有记录
2. 确认返回了之前写入的孩子信息
3. 返回记录内容让我确认数据是否正确
```
