# social-media-pranks

这是 FoolClaw 的社交媒体整蛊模块 catalog。

它目前仍然是一个开放探索面，不是 fully wired 的稳定产品路径。

## 模块定位

- 当 host 明确暴露出 posting、reply、thread、timeline、feed、draft、publish 之类的能力时，允许 agent 思考社交媒体 prank
- 重点不是“我们预设接好了哪些平台”，而是 agent 能否理解当前平台允许它做什么

## 不要预设统一平台模型

不同平台可能完全不同。

可能出现的情况包括：

- 只能操作一个 bot 或品牌号
- 只能在某个群、频道、社区里发言
- 只能草拟，不能直接发布
- 能回复，不能新建帖子
- 能代表一个机器人角色，但不能代表用户本人
- 能代表用户发，但 scope 很窄

所以进入这条线时，先搞清楚：

- `operator-capabilities` 快照里有没有真的出现相关渠道或 posting surface
- 我当前是在操作谁
- 我能发什么
- 我能看到什么
- 我能回帖、发帖、改帖、还是只能草拟

## 这条线里什么算好结果

和 friend-pranks 一样，不一定非得发出去。

这些都算好结果：

- 发现当前存在 posting capability
- 理清当前账号/角色/scope
- 发现当前只能 draft 不能 publish
- 草拟一条可能的 prank post
- 判断现在不适合发，转为 planning-only
- 在条件明确时真的发出一条轻量 prank 内容

## 更适合的形态

社交媒体 prank 第一代更适合：

- 一条短 post
- 一条短 reply
- 一个看起来像角色突然冒泡的短内容
- 一个语气很像 FoolClaw 的 draft

不适合一上来就默认：

- 长线程
- campaign
- 多平台联动
- 自动刷屏

## 给 operator 的提醒

- 这条线只在 host 清楚暴露相关能力时才值得探索
- 如果 role / scope 不清楚，可以先做 planning-only
- 如果这轮更适合 local-pranks 或 friend-pranks，就不要为了“社交媒体整蛊”这个标签硬上
- 先理解平台，再考虑节目效果
- 这条线现在更像一个机会型表演场，不是当前版本必须跑通的保底路径
