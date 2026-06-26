---
name: feishu-multi-agent
description: 飞书多端机器人群聊对话中继 (Multi-Agent Relay)。通过后台轮询飞书群消息历史，监听对方机器人发言并代表本机机器人自动回复，实现多机器人在群内围绕指定话题的持续对话。
version: 1.1.0
---

# Feishu Multi-Agent Relay

本技能用于让两个部署在不同机器上的飞书机器人，在同一个飞书群里围绕某个话题持续讨论。

`{baseDir}` = 本 `SKILL.md` 所在目录。

## 工作原理

- daemon 轮询目标群消息历史
- 当检测到对方机器人发言时，本机调用 OpenClaw brain 自动接话
- 可配置由本机或对方先抛出第一句观点
- 人类用户可以在群里动态更新话题、暂停、继续、设置轮数
- daemon 在群里空闲一段时间后自动退出

## 配置文件

所有业务配置统一集中在一个文件中：

- 运行时配置：`~/.openclaw/config/feishu-multi-agent.json`
- 模板参考：`{baseDir}/config/relay-config.json`

不要再依赖其他全局配置文件去决定本 skill 的业务行为。

## Trigger Hints

- `你们讨论一下`
- `讨论 XXX`
- `锁定话题 XXX`
- `STOP`
- `继续`
- `再对话 50 轮`

## Execution Template

```bash
python3 {baseDir}/scripts/feishu_multi_agent.py start-sync
python3 {baseDir}/scripts/feishu_multi_agent.py status
python3 {baseDir}/scripts/feishu_multi_agent.py stop-sync
python3 {baseDir}/scripts/feishu_multi_agent.py set-rounds 50
python3 {baseDir}/scripts/feishu_multi_agent.py send --to peer --msg "你好"
python3 {baseDir}/scripts/feishu_multi_agent.py daemon
```

## 群内控制规则

- `STOP`
  - 精确匹配，暂停自动对话
- `继续`
  - 包含匹配，恢复对话并沿用原话题
- `讨论 XXX` / `只聊 XXX` / `锁定话题 XXX`
  - 更新锁定话题并立即生效
- `解锁话题`
  - 清除锁定话题
- `再对话 XX 轮`
  - 设置本轮剩余轮数
