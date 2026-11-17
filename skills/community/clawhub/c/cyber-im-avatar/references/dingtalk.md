# 钉钉平台指南（dws / DingTalk Workspace CLI）

> DSH 插件壳从 0.9.0 起支持钉钉（dws）：默认不启用，在体检页点钉钉卡片的「启用」后
> 才轮询 / 唤醒。插件与 skill 共用同一套 CLI 与字段；下面的命令两边都适用。
>
> 出问题先看 [troubleshooting.md](troubleshooting.md)（§B 未登录最常见），
> 或 `dws doctor --json`（自带 `hint` 字段，按提示做即可）/ `python3 scripts/doctor.py dingtalk`。

## 实测基线

- CLI：`dws`（npm 包 `dingtalk-workspace-cli`，实测 v1.0.66）
- 安装：`npm install -g dingtalk-workspace-cli`
- 授权：`dws auth login`（OAuth 设备码；本人点头之后还要过**组织闸门**，见坑 5），状态 `dws auth status`
- 本人 ID：`dws profile list` → `profiles[].userId`（未登录时返回空数组，且 `authenticated: false`）

## 真实命令（已实测，未登录时行为已核对）

| 用途 | 命令 |
|---|---|
| 登录状态 | `dws auth status` |
| 本人账号 | `dws profile list` |
| 读群消息 | `dws chat +chat-messages --group <群名或openConversationId> --limit 20` |
| 读单聊 | `dws chat +chat-messages --user <userId> --limit 20` |
| 读单聊（用会话 ID） | `dws chat +chat-messages --group <conversationId> --limit 20`（`--group` 对单聊同样接受 `cidr…=` 形式的会话 ID，实测可读；有 `--conversation-id` 专名） |
| 最近会话 | `dws chat +recent-conversations`（结果在 `data.conversations[]`，字段 `conversationId` / `name` / `type`） |
| 搜群 | `dws chat +chat-search --query "关键词"` |
| 搜人 | `dws contact user search --query "关键词"` |
| 发单聊 | `dws chat +messages-send --as user --user <userId> --text "..."`；**默认带 AI 标识**（`--ai-tag` 默认 true，payload 里多一个 `clawType: "openClaw"`），要让对方看到普通消息须显式 `--ai-tag=false` |
| 发群聊 | `dws chat +messages-send --as user --chat-id <openConversationId> --text "..."` |
| 按姓名发 | `dws chat +dm --to 姓名 --content "..."`（内部解析唯一 userId） |

## 五个坑

1. **目标参数互斥**：`--group` 用于群聊，`--user` / `--open-dingtalk-id` 用于单聊，一次只能给一个。
   所以适配里群聊走 `cmd_list`、单聊走 `cmd_list_user` 两套模板。
2. **stdout 可能是多段 JSON**：先打结果 ledger，再打一个错误块。
   引擎用 `raw_decode` 只取第一个 JSON 文档，`json.loads` 会直接失败。
3. **默认 `order=desc`**（最新在前），与企微相反。适配里显式写 `"order": "desc"`。
4. **不能裸信 `messages[].sender` 展示名**：身份比较一律用 `senderId`；
   CLI 自己也标了 `identity_unverified` 语义，拿展示名做否定结论是错的。
5. **授权成功 ≠ 登录成功：组织闸门挡住时 token 不落盘**（2026-11 实测两次，两个不同组织）。
   设备码流程会一路走到「授权成功!」，Step 3 换 token 也过，到 Step 4 检查组织 CLI
   授权状态才被拒，退出码 2：

   ```
   ⚠️  您暂无 CLI 数据访问权限
      当前组织未授权您通过 CLI 访问个人数据。
      组织主管理员：<姓名>
      请联系组织主管理员开启后重新登录。
      管理员操作入口：https://open-dev.dingtalk.com/fe/old#/developerSettings
   ```

   现象：`dws auth status` 回到 `authenticated: false` / `message: 未登录`，
   `dws profile list` 空数组——**与「从没登录过」在状态里长得一模一样**，
   只能从登录输出本身认出这个形态。闸门按**组织**走，换号只有在目标号所在组织
   已开通（或本人就是该组织主管理员）时才有用，否则重试设备码也是同一个结果。
   `dws doctor --json` 的 `auth` 项只会说「未登录」，`hint` 仍是「运行 dws auth login」，
   照着做会死循环——先确认组织开关。

## 消息 ledger 的关键字段

`+chat-messages` 返回 `messages[]` / `count` / `hasMore` / `complete` /
`failures[]` / `stopReason` / `truncated`。

注意 `complete` 的口径：**`complete=false` 只表示「这一页没读到底」**——用 `--limit` 截断
或还有更早的消息时也是 false，此时 `messages[]` 完全可用。真正的失败看 `failures[]`
非空；两者都不能当成"没有新消息"。
单条消息的正文在 `text`（字符串），发送者是 `senderId`（可能是 `Dd…` 开头的
openDingTalkId，不等于 `userId`），时间 `createTime` 形如 `2026-11-03 08:56:34`。

## 校准流程

```bash
dws auth login                       # 先登录，否则 profile list / 读消息都会失败（rc=5）
python3 scripts/bootstrap.py --probe dingtalk --user-id <userId>
python3 scripts/bootstrap.py --selftest dingtalk <userId>
```

字段或命令变了，写 `~/.im-standin/env.json`：

```json
{ "overrides": { "dingtalk": { "cmd_list_user": ["chat","+chat-messages","--user","{user_id}","--limit","20"],
                               "f_items": [["messages"]] } } }
```

## 事件式监听的另一种可能

dws 自带 `dws event +listen-im --kind ...`（常驻事件流）。本 skill 不用它，
原因是：常驻进程不返回、无法"命中即退出 → agent 处理 → 重挂"，
与单发唤醒模型冲突。需要秒级实时性时再单独评估。
