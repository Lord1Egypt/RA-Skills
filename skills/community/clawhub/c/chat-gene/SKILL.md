---
name: chat-record-generator
description: 从零生成模拟微信群聊记录的 Excel (.xlsx) 文件，包含 group_info / active_members / message_stream 三个 sheet，格式与派平台的群聊训练数据完全兼容。使用场景：(1) 需要生成 AI 助手训练数据的模拟群聊对话；(2) 测试群聊 FAQ/知识库系统；(3) 展示多角色对话 multi-Agent 工作流；(4) 生成任意主题的群聊样本 xlsx 文件。触发词：生成群聊记录、模拟群聊数据、生成聊天记录表格、群聊 xlsx、派聊天记录。
---

# Chat Record Generator

生成符合派平台格式的模拟群聊 Excel 文件，支持多角色 multi-Agent 并行生成对话内容。

## 快速流程

1. **定义群组** → 2. **并行生成对话（multi-Agent）** → 3. **编排 + 写入 xlsx**

---

## 第一步：定义群组

需要确认以下信息（如用户未提供，按默认值生成）：

| 字段 | 说明 | 示例 |
|------|------|------|
| 群名 | 任意字符串 | AI资讯交流群 |
| 群ID | 数字字符串 | 123456789 |
| 成员数 | 建议 5–15 人 | 10 |
| AI助手昵称 | 群内机器人 | 元宝 |
| 话题列表 | 2–4 个话题 | 见下方 |
| 目标消息总数 | 建议 50–200 条 | 150 |

运行 `scripts/generate_group_def.js` 生成 group_definition.js，或参考 `references/group-schema.md` 手动编写。

---

## 第二步：并行生成对话（multi-Agent）

**最大并发限制：5 个 subagent**，超过时分批启动。

用 `sessions_spawn(runtime="subagent", mode="run")` 为每个角色启动一个子 Agent。

### Prompt 模板

```
你是「{群名}」中的角色【{昵称}】，{年龄}岁{职业}。

语言风格：{风格描述}

【群聊话题】
话题1（第1-N轮）：{话题1标题}
话题2（第N+1-M轮）：{话题2标题}
...

【你的任务】
以{昵称}身份生成{N}条消息，每个话题约{N/话题数}条。
- 话题1：{角色在该话题的具体行为}
- 话题2：...

直接输出JSON数组，不要有其他文字：
[{"话题": 1, "发言人": "{昵称}", "内容": "消息内容"}, ...]
共{N}条。
```

### 消息分配参考（总140条，10角色）

| 角色类型 | 条数 |
|---------|------|
| 活跃成员（核心讨论者）| 15 |
| 普通成员 | 12–14 |
| 工具人（发起话题/@AI）| 15 |

---

## 第三步：编排 + 写入 xlsx

收集所有子 Agent 结果后，运行 `scripts/write_xlsx.js` 写入文件。

### 关键规则

- **消息类型**：`text` → 内容非空、附件 null；`image/file` → 内容 null、附件为 `image_N`/`file_N`
- **时间分配**：每条消息间隔约 `0.002`（约3分钟），话题间隔 `0.05–0.1`（约1–2小时）
- **⚠️ numFmt Bug**：必须对每个时间单元格手动设置 `z` 属性，`aoa_to_sheet` 不会保留格式
- **Excel 时间 epoch**：`new Date(Date.UTC(1899, 11, 30))`

### 时间格式

```javascript
// 时间列
cell.z = 'yyyy/m/d h:mm;@'
// join_time 列（含秒）
cell.z = 'yyyy/m/d h:mm:ss;@'
```

---

## xlsx 格式规范

参见 `references/xlsx-format.md` 获取完整的三个 sheet 字段定义。

---

## 依赖

- Node.js + xlsx 库（`npm install xlsx`，通常缓存在 `/tmp/xlsxparse/node_modules/xlsx`）
- 若未安装：`mkdir -p /tmp/xlsxparse && cd /tmp/xlsxparse && npm install xlsx`

---

## 注意事项

- **昵称风格**：使用真实微信群昵称（陈默、林晓、周宇老师），避免社交媒体 ID 风格
- **@元宝**：AI助手被 @时应在同一话题内接近的轮次生成回复消息（可由主 Agent 补写）
- **task_list**：始终为 null，但列必须保留
- **bot_config**：group_info sheet 中为 null
