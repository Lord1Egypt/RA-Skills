# awam-todo Agent 提示词（文件索引 + 简短分发提示词）

判定由 `todo.py` 的纯规则分诊完成，与模型/平台无关；Agent 只负责
「发现疑似待办 → 原样交给分诊 → 按结果执行或确认」，不自己猜测、不改写原句。

## 文件索引

| 文件 | 内容 | 用途 |
|------|------|------|
| `docs/prompt-doubao.md` | 豆包版完整提示词（分诊调用 + 执行映射 + 确认规则） | 豆包读取 |
| `docs/prompt-cursor.md` | Cursor 版完整提示词（同上，仓库相对路径） | Cursor 读取 |
| 本文档 | 简短分发提示词 + 命令速查 + JSON 契约 | 给用户粘配置用 |

## 简短提示词（分别粘到豆包 / Cursor 的提示词配置里）

### 豆包

```text
【待办自动分诊（awam-todo）】
对话中出现待办意图（记一下 / 加个待办 / 提醒 / 安排 / 完成 / 删除 / 改期 /
标记状态，拿不准也算）时，读取文件
<技能目录>\docs\prompt-doubao.md
（把 <技能目录> 换成本机 awam-todo 安装根）
并严格按其中流程执行；纯问答、闲聊不触发。
```

### Cursor

```text
# awam-todo 待办处理

以下编码周期阶段出现待办相关内容时，读取仓库内 docs/prompt-cursor.md 并按其流程执行：

1. 任务开始前：编码任务关联仓库内待办（T-ID 或内容匹配）时，标记进行中。
2. 任务进行中：对话出现待办意图（新增 / 完成 / 删除 / 改期 / 标记状态）时，走分诊执行。
3. 任务收尾 / 提交前：完成项标记 done、新事项 add、改期 postpone，并核对遗留进行中项。

纯技术问答、与待办无关的改动不触发。
```

---

## 附：命令速查（供参考，不必写入提示词）

| 意图 | 命令 |
|------|------|
| 分诊（只读） | `python scripts\todo.py triage --text "<原句>"` |
| 新增 | `add --text "<原句>" [--due 明天] [--importance 重要] [--urgent 紧急] [--tags 工作;紧急] [--note ...] [--workspace ...] [--force]` |
| 更新已有 | `add --update-id <T-ID> --text "<新内容>" [其他改动字段]` |
| 标记结束 | `done <T-ID> [--force]` |
| 标记进行中 | `start <T-ID> [--force]`（`work <T-ID>` 会顺带用配置的编辑器打开工作区） |
| 重新打开 | `reopen <T-ID>` |
| 改期/清期 | `postpone <T-ID> "下周一"` / `postpone <T-ID> --clear`（别名 reschedule/replan） |
| 删除 | `delete <T-ID>` |
| 列表/查看 | `list` / `list --state all` / `index` / `show <T-ID>` |
| 网页 API（服务在跑时） | `POST http://127.0.0.1:8796/api/capture/triage`，body `{"text":"<原句>"}`（UTF-8） |

triage JSON 契约字段：`action`(add/update/status/delete/unknown)、`confidence`(high/medium/low)、
`need_confirm`(bool)、`reasons`、`text`(用户原句原文)、`target`(T-ID 及相似度)、
`candidates`(候选任务)、`status`(目标状态)、`fields`(解析出的字段)、
`suggested_tags`(建议标签，只读)、`fallback_action`。
