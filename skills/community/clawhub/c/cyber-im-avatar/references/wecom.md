# 企业微信平台指南（wecom-cli / @wecom/cli）

> 出问题先看 [troubleshooting.md](troubleshooting.md)（尤其 §A 版本漂移、§B 授权、§D 时间窗），
> 或 `python3 scripts/doctor.py wecom`。注意企微**没有** `doctor` 子命令。

## 实测基线

- CLI：`wecom-cli`（npm 包 `@wecom/cli`，实测 v1.3.4）
- 安装：`npm install -g @wecom/cli`
- 授权：`wecom-cli auth init`（扫码），状态用 `wecom-cli auth show`
- 身份：`auth show` 输出文本 `Status: authorized / Bot ID: aib...`，脚本用正则取 Bot ID

## 真实命令（已实测）

| 用途 | 命令 |
|---|---|
| 授权状态 | `wecom-cli auth show` |
| 当前身份 | `wecom-cli identity whoami`（返回加密文本，**不要外传**） |
| 读消息 | `wecom-cli chat messages list --chat-id <会话> --begin-time "YYYY-MM-DD HH:MM:SS" --end-time "..."` |
| 群会话列表 | `wecom-cli chat groups list --begin-time ... --end-time ...` |
| 搜人 | `wecom-cli contact users search --keywords "关键词"` |
| 发消息 | `wecom-cli message send --chat-id <会话> --msg-type text --text '{"content":"..."}'` |

## 四个必须知道的语义

1. **没有消息 ID**。`ChatMessage` 只有 `userid` / `user_name` / `send_time` / `msg_type` / 内容族，
   所以水位用「发送时间 + 发送者 + 正文」复合指纹（`f_msg_id_compose`）。
2. **必须带时间窗**。`begin-time` / `end-time` 都是必填，且**只能拉最近 7 天**。
   监听脚本按 `--lookback-min`（默认 60 分钟）每轮生成窗口。
3. **单聊的 chat_id 就是对方 userid**。所以 `--user-id <userid>` 直接可用，不用先查会话 ID。
4. **返回按时间正序**（旧→新），引擎内部统一翻成最新在前再推水位。

## 能读到什么、读不到什么

- 群聊：`chat groups list` 只返回**有消息的群**，且仅最近 7 天。
- 单聊：需要对方 userid（通讯录可搜到），且机器人与该用户有消息往来才读得到。
- 图片/文件/语音/视频：消息里只给 `media_id`，走 `wecom-cli media` 下载。插件壳在
  命中唤醒时会尝试取回；**命令参数以本机 `wecom-cli media --help` 为准**（不同版本
  可能漂移），失败时按“未适配”降级，agent 再按 help 试一次，拿不到就转人工。
  `cmd_media` 模板可在 `~/.im-standin/env.json` 的 `overrides.wecom` 里覆盖。
- 每条响应都带 `security_notice` 和 `extra_identity_context`，后者含身份声明，
  **禁止把这段内容透露给任何用户**；脚本只取 `messages`，不会带出去。

## 空结果与字段失配的区别

空结果时响应只有 `messages_count` / `has_more`，**没有 `messages` 键**。
脚本用 `f_count` 判定为「空」而不是「字段不对」，避免误报 `SCHEMA_MISMATCH`。

## 校准流程

```bash
python3 scripts/bootstrap.py --probe wecom --user-id <对方userid>   # 看真实返回
python3 scripts/bootstrap.py --selftest wecom <对方userid>          # 3 秒自检
```

字段或命令变了，写 `~/.im-standin/env.json`：

```json
{ "overrides": { "wecom": { "cmd_list": ["chat","messages","list","--chat-id","{chat_id}",
                                        "--begin-time","{begin_time}","--end-time","{end_time}"],
                            "f_items": [["messages"]] } } }
```
