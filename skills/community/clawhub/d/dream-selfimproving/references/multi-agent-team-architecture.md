# 多 Agent 团队架构参考

> 来源：OpenClaw 搭建 6 人团队，它开始自己转起来了
> 作者：yabin
> 链接：https://mp.weixin.qq.com/s/D33ScqwgpjiwI4PDN3vUaA
> 抓取时间：2026-04-17

## 核心架构

```
同一飞书机器人（一个前台号码）
  ↓ 按群聊 ID 路由
开发群 → main agent
产品群 → product-claw
测试群 → qa-claw
调研群 → research-claw
数据分析群 → analytics-claw
运营群 → ops-claw
```

每个 agent 有独立 workspace，上下文件隔离，形成闭环飞轮：
```
research → product → dev → qa → analytics → ops → 下一轮
```

## 关键结论

### 1. 不拆 workspace，多 agent 很容易只是幻觉
- 不同角色的长期记忆不会混在一起
- 本地 skill、模板、文档可以按角色分别放
- 同一个飞书机器人进来的消息，最终会落进不同工作目录

### 2. 角色文件必须落到角色边界上
每个 agent 独立配置：
- AGENTS.md、IDENTITY.md、SOUL.md、USER.md、TOOLS.md、MEMORY.md

### 3. 产品 agent 特别值得挂方法库
开发 agent 靠代码库天然有上下文，产品 agent 没有方法库的话很容易退化成"会写点文档的通用聊天机器人"。

### 4. 路由方式选择
- 按群聊 peer-id 路由是最自然的形态
- 人在协作里本来就已按群在分场景

### 5. 专人助手式的 agent，交互摩擦一定要足够低
- 如果机器人是共享工具，那 @ 一下很合理
- 如果机器人是专属群的长期助手，每次都 @ 一下就很蠢

## OpenClaw 飞书插件 Bug（已发现）

1. **机器人名字**不是在 OpenClaw 里改，而是在飞书开放平台的 Bot 能力页改
   - appId/appSecret 解决"这个机器人是谁"
   - Bot 显示名解决"别人看到它叫什么"

2. **requireMention per-group 配置无效**
   - 文档支持 `groups.<id>.requireMention`
   - 配置 schema 也支持
   - 但运行时代码只读了全局 `channels.feishu-china.requireMention`
   - per-group 覆盖配置根本没被用上

## 方案边界

解决的是：
- 角色分工
- 上下文隔离
- 单机器人多场景协作

没有解决的是：
- 容器级强安全隔离
- 多套全局凭证隔离
- 多飞书机器人并行的插件级支持

本质：同一个 gateway 进程、同一个 OpenClaw 实例、同一套全局配置。
是「角色隔离 + 上下文隔离」，不是「基础设施级彻底隔离」。

## 实践要点

1. 默认开发 agent 尽量保留 main（兼容性现实）
2. 多 agent 的关键不是多写几个 id，而是拆 workspace
3. 人格文件必须和 AGENTS.md、TOOLS.md、MEMORY.md 一起工作
4. 产品 agent 特别值得挂方法库
5. 同一个飞书机器人按群路由是最顺手的形态
6. 如果配置明明对了但不工作，第一时间去看运行时日志，不要先怀疑自己
