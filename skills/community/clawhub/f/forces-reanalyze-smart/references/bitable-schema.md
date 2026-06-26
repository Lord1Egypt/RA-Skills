# 工单数据多维表格 Schema

## 字段定义（共 9 个字段）

| 字段名 | 类型 | 说明 |
|---|---|---|
| 文本 | 文本 (type=1) | 问题描述内容，来源自工单的 `content` 字段 |
| 问题链接 | 超链接 (type=15) | 工单详情页URL。导入格式：`{"link": "https://...", "text": "查看工单"}` |
| 工单状态\|修复情况 | 文本 (type=1) | 可选值：已关闭、处理中、已创建。竖线 `\|` 是字段名的一部分 |
| 问题原因 | 文本 (type=1) | 工单的问题原因及解决方式 |
| 责任人 | 文本 (type=1) | 处理人姓名（钉钉名称），如"李文茂"、"蒋达周"等 |
| 解决类别 | 文本 (type=1) | 可选值：无需优化-技术介入、内部原因-已解决、内部原因-延期处理、内部原因-无法重现 |
| 解决模块 | 文本 (type=1) | 解决模块名称，如"扫码点单"、"打印机"等 |
| 超时时间 | 文本 (type=1) | 超时状态文本，如"已过期10小时" |
| 超时备注 | 文本 (type=1) | 处理人流转记录，格式：`转交人->接收人: 时间；` |

## 字段名注意事项

- `工单状态|修复情况` —— 字段名含竖线 `|`，不要写错为 `工单状态/修复情况`（CSV列名是斜杠，Bitable字段名是竖线）
- `问题链接` 是超链接类型（type=15），导入时不要传 `property` 参数，否则报 `URLFieldPropertyError`
- 所有文本字段（type=1）无需传 `property` 参数

## 创建表格的 API 调用

```json
{
  "action": "create",
  "app_token": "APP_TOKEN",
  "table": {
    "name": "工单数据（2026年X月）",
    "default_view_name": "全部",
    "fields": [
      {"field_name": "文本", "type": 1},
      {"field_name": "问题链接", "type": 15},
      {"field_name": "工单状态|修复情况", "type": 1},
      {"field_name": "问题原因", "type": 1},
      {"field_name": "责任人", "type": 1},
      {"field_name": "解决类别", "type": 1},
      {"field_name": "解决模块", "type": 1},
      {"field_name": "超时时间", "type": 1},
      {"field_name": "超时备注", "type": 1}
    ]
  }
}
```

## 看板视图配置

创建看板视图后，需要通过 API 设置分组字段：

```
GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields
→ 找到 "责任人" 的 field_id

PATCH /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/views/{view_id}
Body: {"property": {"kanban_field_id": "责任人的field_id"}}
```

也可以在飞书 UI 中手动设置：视图 → 看板设置 → 分组依据 → 选择"责任人"。
