---
name: auwomo-message
version: 1.0.0
description: >
  消息发送：通过飞书给组织成员发私信。
  Triggers: 消息, 通知, 提醒, 发消息, 发给, notify, message, send.
  NOT for: agent→agent inbox(暂不支持), 任务操作(use auwomo-task).
metadata:
  openclaw:
    requires:
      bins:
        - auwomo
        - lark-cli
---

# auwomo-message

安全地向组织成员发送飞书私信。所有操作通过 `auwomo` CLI 执行。

## 触发条件

当用户提到以下内容时激活本技能：

- "发给某某一条消息"
- "提醒某某今天提交日报"
- "通知某某"
- "给某某发消息说..."

## 排除场景

- agent→agent 文件 inbox → 暂不支持
- 任务创建/记录/汇报 → 转到 `auwomo-task`

## 前置依赖

1. 身份可用：`auwomo identity whoami` 正常返回
2. lark-cli 可用：`which lark-cli` 有输出
3. 收件人在 org.yaml 中且 enabled

## 安全规则

1. **仅允许精确匹配** — 收件人必须在 org.yaml 中精确命中
2. **必须有有效 open_id** — 匹配到的成员必须有非空 open_id
3. **使用 bot 身份发送** — 不以用户身份发送
4. **不模糊匹配** — 不猜测、不自动纠错、不用部分姓名匹配
5. **找不到人就不发** — 明确告知用户该成员不在系统中

## CLI 命令速查表

| 场景 | 命令 |
|------|------|
| 发送消息 | `auwomo message send --to "某某" --text "内容"` |
| 预览不发送 | `auwomo message send --to "某某" --text "内容" --dry-run` |
| 按 open_id 发送 | `auwomo message send --to ou_xxx --text "内容"` |

## 参考文档路由

| 场景 | 文档 |
|------|------|
| 需要发送消息 | [message-send.md](references/message-send.md) |
