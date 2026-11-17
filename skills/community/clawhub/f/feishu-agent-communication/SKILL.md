---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_082fd229731111f1986d525400d9a7a1
    ReservedCode1: ERYOqKJMdOzLT+yRrB+XvLH5+Qa4UdA5f+9Lzc18UOztcinIrfaTbgzPq4jPAu0agvfG7FaQ41aMCDxYaif44E3xxWKspMZMnIO5Mwvjxhj34q6Ctu8asBNBTiY0331VOQ6Thvh4DPBFFY6mvAM6apKEg1UAjyWee+Axl6faH9OAsaDyHMsnHE6nvEs=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_082fd229731111f1986d525400d9a7a1
    ReservedCode2: ERYOqKJMdOzLT+yRrB+XvLH5+Qa4UdA5f+9Lzc18UOztcinIrfaTbgzPq4jPAu0agvfG7FaQ41aMCDxYaif44E3xxWKspMZMnIO5Mwvjxhj34q6Ctu8asBNBTiY0331VOQ6Thvh4DPBFFY6mvAM6apKEg1UAjyWee+Axl6faH9OAsaDyHMsnHE6nvEs=
---

# 飞书多Agent群聊通信 v0.1.4

多个AI Agent各干各的，消息靠你手动搬？建一个飞书群把它们拉进来，自动认领、自动交接。直连互@与Gateway路由双路线，兼容OpenClaw/AutoClaw/CherryStudio等8个框架，含8条实测踩坑。

## 解决什么问题

当你同时使用多个 AI Agent（比如一个写代码、一个查资料、一个管项目），它们各自孤立运行，互不知道对方在干什么。每次想让一个 Agent 处理完通知另一个继续，只能手动搬运消息。

单 Agent 接入飞书的教程网上很多；多 Agent 场景下「消息谁先处理、处理完交给谁、卡住了怎么查」，才是这个 Skill 沉淀的价值——8 条实测踩坑方向都来自真实部署过程。

这个 Skill 让你：建一个飞书群，把多个 Agent 拉进去。群里发消息，对应 Agent 自动认领处理，处理完自动 @ 下一个继续。你从"搬运工"变回"老板"。

## 核心原理（双路线）

两条技术路线都可行，选择取决于你的框架形态：

**路线 A：直连互@（多 Agent 并行框架适用）**

```
Agent 1 处理完 → 调飞书 API 在群里 @ Agent 2
Agent 2 收到群消息 → 认领处理 → 再 @ 下一个
```

Bot 之间通过飞书 HTTP API 直接互发群消息，不需要部署 Gateway。适合多个 Agent 各自独立运行、没有统一调度中心的框架。

**路线 B：经 Gateway 路由（主 Agent 分派子 Agent 框架适用）**

```
飞书群发消息 → 飞书 WebSocket 推送 → Gateway 接收
→ 按路由规则（群 ID / 消息前缀）匹配 → 分发到对应 Agent
→ Agent 处理 → 回复到群
```

由 Gateway 统一收消息、按规则分发。适合有一个主 Agent 负责分派子 Agent 任务的框架。

> 两条路线均可行，选择取决于你的框架形态。

## 实测效果

- **3 Agent 协作**：任务拆解、执行、汇总全流程在群内完成，消息无丢失
- **API 成本**：飞书频控按 API 单独计算（分级 10次/分 ~ 100次/秒，每应用每租户），个人多 Agent 用量离上限很远，无需为额度担心

## 你需要准备

| 项目 | 说明 | 费用 |
|------|------|------|
| 飞书账号 | 个人免费注册 | 免费 |
| 飞书开放平台 | 创建机器人用 | 免费 |
| Agent 运行平台 | OpenClaw / AutoClaw / WorkBuddy 等，见下方兼容清单 | 免费开源 |

## 兼容性

OpenClaw / AutoClaw / WorkBuddy / CherryStudio / DeepSeek Harness / Pi / Claude Code / Codex

## 配置中常见问题（8 条实测踩坑方向）

以下是实测过程中踩过的坑。你的 Agent 可以基于这些方向自行排查：

### 1. 配置文件路径搞混
- 方向：OpenClaw 标准版和 AutoClaw 使用不同的配置文件路径，改了不对的位置重启不会生效。

### 2. 消息收不到
- 方向：飞书开放平台后台有一个「通过长连接接收事件」开关，默认关闭。

### 3. 群 ID 获取不到
- 方向：飞书网页版后台不显示群 ID，需在手机飞书 App → 群设置中查看（`oc_` 开头）。

### 4. 机器人读不到群消息
- 方向：缺少消息读取权限，需在飞书后台开通后重新发布应用。

### 5. Token 过期导致中断
- 方向：飞书接入 Token 有效期 2 小时，需确保 Gateway 支持自动刷新。

### 6. 多 Agent 按 @ 区分不生效
- 方向：路由是按群 ID 匹配而非 @ 语义，需通过消息前缀或关键词条件来区分。

### 7. Gateway 端口与实际监听不一致
- 方向：不同发行版可能覆写端口，Gateway 内部自动适配，一般不需手动处理。

### 8. 回复在群里显示为代码块
- 方向：消息格式选错会导致显示异常，用 `text` 类型而非 `post`。

## 完整部署文档

以上 8 个卡点的配置模板、分步操作（每步带期望日志）和一键验证方法，见部署文档（0.99 元，一次买断）：

> https://www.jinengpu.chat/feishu-multi-agent-detail.html

## 依赖与致谢

| 项目 | 用途 | 链接 |
|------|------|------|
| OpenClaw | Agent Gateway 核心 | github.com/openclaw/openclaw |
| AutoClaw | 社区发行版，方案验证 | 社区项目 |
| 飞书开放平台 | Bot API + WebSocket | open.feishu.cn |

## 关键词

中文：飞书多Agent / Agent群聊 / 多bot协作 / Agent互相@ / Agent交接 / 飞书机器人中转 / 多智能体通信 / Gateway路由 / 飞书 / 群聊通信 / WebSocket / 消息路由

English: feishu multi agent / agent to agent chat / bot relay / group chat agents / gateway routing / feishu / multi-agent / agent collaboration / websocket / message routing

*（内容由AI生成，仅供参考）*
