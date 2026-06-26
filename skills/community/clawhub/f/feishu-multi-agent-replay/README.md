# Feishu Multi-Agent Relay

让两个部署在不同机器上的飞书机器人，在同一个群内持续讨论指定话题。

## 核心行为

- 配置统一收敛到 `~/.openclaw/config/feishu-multi-agent.json`
- 支持由指定一方先在群里抛出第一句观点
- 支持动态锁定、更新、解锁话题，并立即生效
- `STOP` 采用精确匹配，只暂停群内对话
- `继续` 采用包含匹配，可沿用上一次锁定话题
- 支持 `再对话N轮` 等轮数指令
- 轮数耗尽后自动恢复到默认轮数
- daemon 常驻监听，群里在指定时间内无新消息时自动退出

## 快速开始

```bash
cd ~/.openclaw/skills/feishu-multi-agent
bash scripts/install.sh
nano ~/.openclaw/config/feishu-multi-agent.json
python3 scripts/feishu_multi_agent.py start-sync
python3 scripts/feishu_multi_agent.py status
```

## 使用前提

在分享给别人使用前，建议先确认这些前提已经满足：

- 这是双机部署方案：机器人A 和 机器人B 各自在自己的机器上安装一份 skill，并各自维护本机的 `~/.openclaw/config/feishu-multi-agent.json`
- 两边机器都需要能访问飞书 OpenAPI
- 两边机器都需要有可用的 OpenClaw API，默认地址是 `http://127.0.0.1:18789`
- 每台机器都需要准备自己的飞书应用身份：`self_app_id`、`self_app_secret`
- 每台机器都需要知道对方机器人的标识：`peer_name`、`peer_app_id`
- 两边配置里的 `chat_id` 必须指向同一个飞书群

如果对方是第一次部署，最容易卡住的是飞书应用权限、群 ID 获取和本机 OpenClaw API 可用性，这三项建议优先检查。

## 唯一配置文件

用户只需要维护一个文件：

```text
~/.openclaw/config/feishu-multi-agent.json
```

这个文件同时包含：

- 飞书身份
- 对方机器人身份
- 目标群 `chat_id`
- 开场角色 `starter_role`
- 话题控制关键词
- 轮数控制规则
- 空闲退出时间
- OpenClaw API 参数

脚本不会再去读取其他全局配置来决定 `require_mention` 等行为。

双机部署时，两台机器都要各自填写这份配置文件，不要共用同一份本地配置。

## 推荐配置

- 机器人A：`starter_role=self`
- 机器人B：`starter_role=peer`
- `default_rounds=50`
- `idle_timeout_minutes=30`
- `preserve_topic_on_stop=true`

## 首次配置建议

- 先在两台机器上分别运行 `bash scripts/install.sh`
- 先确认两边的 `self_name` / `peer_name`、`self_app_id` / `peer_app_id` 是互相对应的
- 两边使用同一个 `chat_id`
- 机器人A 所在机器设置 `starter_role=self`
- 机器人B 所在机器设置 `starter_role=peer`
- 如果只想被明确点名时才接话，可以把 `require_mention` 改成 `true`
- 如果只是小范围试跑，建议先把 `default_rounds` 设成较小值，例如 `10`

## 需要准备的信息

- 飞书机器人 App ID
- 飞书机器人 App Secret
- 目标群 `chat_id`
- 本机 OpenClaw API 地址
- 本机 OpenClaw API Token

其中 `chat_id` 必须是目标飞书群的实际群 ID，格式通常以 `oc_` 开头。

## 群内控制

- `讨论 XXX` / `只聊 XXX` / `锁定话题 XXX`
  - 锁定并更新当前讨论话题，若本机配置为开场方，会立即先说第一句
- `解锁话题`
  - 取消话题锁定
- `STOP`
  - 精确匹配，暂停自动对话，但不影响私聊
- `继续`
  - 继续当前对话；若未指定新话题，则沿用上次话题
- `再对话50轮`
  - 设置本轮剩余轮数为 50，并继续对话

## 命令

```bash
python3 scripts/feishu_multi_agent.py start-sync
python3 scripts/feishu_multi_agent.py stop-sync
python3 scripts/feishu_multi_agent.py status
python3 scripts/feishu_multi_agent.py set-rounds 50
python3 scripts/feishu_multi_agent.py send --to peer --msg "你好"
python3 scripts/feishu_multi_agent.py daemon
```
