# 生态适配器说明

## 核心原则

效能淘金者-SOP炼丹炉的核心不是某一个具体工具，而是统一分析框架：

```text
工作痕迹 -> 工作片段 -> 任务主题聚类 -> 重复摩擦识别 -> SOP/Skill 需求卡片 -> 待确认执行动作
```

不同生态只需要替换“工作痕迹来源”和“写入动作”。

## 统一工作片段

所有生态的数据都归一为：

```json
{
  "time": "<ISO或自然时间>",
  "source": "calendar|task|doc|sheet|approval|mail|message|crm|issue",
  "title": "<标题>",
  "summary": "<摘要>",
  "status": "<状态>",
  "related_project": "<项目/客户/流程主题>"
}
```

## 钉钉 / 悟空 dws 适配

| 数据源 | 能力 |
| --- | --- |
| 日程 | `dws calendar event list --format json` |
| 待办 | `dws todo task list --format json` |
| 文档 | `dws doc search/read/create/update --format json` |
| AI 表格 | `dws aitable record query/create/update --format json` |
| 审批 | `dws oa approval list-pending/list-initiated/detail --format json` |
| 消息 | `dws chat message list --format json` |

注意：

- 所有 dws 命令必须带 `--format json`。
- 写入文档、待办、AI 表格或发送催办前必须用户确认。
- 不能凭空编造 nodeId、taskId、baseId、tableId、instanceId、openconversation_id。

## Google Workspace 适配

| 工作痕迹 | Google 生态来源 | 可替代钉钉能力 |
| --- | --- | --- |
| 会议/日程 | Google Calendar | 日程 |
| 待办 | Google Tasks / Gmail action items | 待办 |
| 文档 | Google Docs / Drive files | 钉钉文档 |
| 表格 | Google Sheets | AI 表格 |
| 邮件沟通 | Gmail | 群消息/沟通摘要 |
| 文件产物 | Google Drive | 文档搜索与产物归档 |

执行原则：

- 优先使用当前平台已授权的 Google 连接器或 MCP。
- 不要求用户手动粘贴 OAuth token、cookie 或 API Key。
- 写入 Google Docs、Sheets、Tasks 或发送 Gmail 前必须用户确认。
- 如果没有对应连接器，只能基于用户提供的脱敏文本或演示数据生成分析结果，不声称已读取真实 Google 数据。

## 其他生态适配

| 生态 | 可映射工作痕迹 |
| --- | --- |
| Notion | 文档、数据库、项目进度 |
| Slack / Teams | 消息、线程、待确认口径 |
| Linear / Jira | 任务、工单、阻塞状态 |
| Salesforce / HubSpot | 客户跟进、商机、销售阶段 |
| GitHub / GitLab | Issue、PR、项目协作痕迹 |

要求：

- 只能使用当前平台实际提供的连接器、MCP、CLI 或用户授权数据。
- 缺少真实连接器时，输出“需要接入的数据源清单”，不要假装已经读取。
- 所有跨系统写入、发送、创建任务动作都必须先展示草稿并等待确认。

## 输出差异

无论生态如何变化，输出结构保持一致：

- 今日复盘
- 高频摩擦
- 自动化机会 Top 3
- 优先级评分
- Skill/SOP 需求卡片
- 日报草稿
- 明日待办
- 待确认执行动作
- 闭环状态
