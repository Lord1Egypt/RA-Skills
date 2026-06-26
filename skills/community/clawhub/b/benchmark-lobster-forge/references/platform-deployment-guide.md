# Platform Deployment Guide

## 目标

当目标 Agent workspace 已建立后，不要停在文档规划。
继续主动询问用户要部署的平台，并引导其完成接入前置准备。

---

## 标准动作

1. 确认目标 Agent workspace 已建立
2. 确认关键文档已写入目标 workspace
3. 主动询问：部署在哪个平台
4. 根据平台给出接入步骤
5. 说明第一次联调怎么测

---

## Telegram

常见准备：
- BotFather 创建 bot
- 获取 bot token
- 明确要接群聊还是私聊
- 后续绑定 agent / account / routing

---

## Feishu

常见准备：
- 创建应用
- 获取 app 凭据
- 明确收消息场景（群聊 / 单聊）
- 后续配置事件订阅与接入

---

## Discord

常见准备：
- 创建 bot application
- 获取 token
- 邀请进目标服务器 / 频道
- 后续做 routing / 绑定 / 联调

---

## 原则

- 主动问，不等用户自己想起来
- 平台问题要在 workspace 建好后尽快确认
- 引导目标是让用户知道“下一步该怎么接上去”
