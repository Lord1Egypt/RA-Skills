# friend-pranks

这是 FoolClaw 的朋友整蛊模块 catalog。

它现在不是一个 fully wired 的产品面，而是一个给 operator 和前台 agent 使用的探索面。

## 模块定位

- 用已经存在于宿主环境中的消息、频道、会话、联系人或群组能力去整蛊别人
- 重心不在于“我们预先集成了多少 IM SDK”，而在于 agent 能否发现自己现在到底拥有什么渠道能力
- 这条线允许显式触发，也允许后台 operator 在合适时机 opportunistically 使用

## 先发现，再动手

进入这一模块时，不要先假设世界长什么样。先弄清楚：

- 当前 `operator-capabilities` 快照里到底出现了哪些可用 channel
- 当前 `operator-targets` 快照里有没有已经能直接碰的 peer、group、thread、target hint
- 当前有没有 `message`、channel、DM、group、sender、recipient、post、reply 之类的工具或能力
- 这些能力是在操作一个 bot、一个群成员角色、一个代理账号，还是用户自己的身份
- 当前渠道有没有 allowlist、scope、capability、角色限制
- 有没有现成的目标、线程、群、频道、联系人、sender pairing 可以利用
- 当前能力更像“可以发消息”，还是“只能看/草拟/规划”

不要默认：

- 一定能看到好友列表
- 一定能私聊任何人
- 一定能代表用户身份发言
- 每个平台都和 Telegram 一样
- 每个平台都和 Discord / Slack / 社交媒体一样
- 只要看到了一个你熟悉的平台名，就应该默认沿着那个平台去想

## 这个模块里什么算有价值的结果

一次 friend-pranks turn 不一定非得发出去。

这些都算好结果：

- 识别出当前有哪些渠道能力
- 识别出自己在该渠道里的角色
- 识别出当前根本没有可用 target，于是先不硬发
- 找到一个可能的 prank target 或现成线程
- 草拟一条短 prank 文案
- 发现当前渠道不适合整蛊，然后回到 local-pranks
- 在条件合适时真的发出一条 prank message

## 适合的动作形态

保持轻、短、直接。优先考虑：

- 一条突然出现的怪消息
- 一句像同伙留言的短话
- 一条像 bot 突然失控的 playful 文案
- 一条能让人回头问“这谁发的”的消息

不要一上来就预设：

- 很长的对话链
- 复杂剧本
- 多轮自动 campaign
- 假装有一堆你根本没看到的联系人

## planning-only turn 应该怎么想

如果这轮还不适合发送，可以先做 planning：

- 记录某个渠道看起来可用
- 记录某个目标或线程看起来可整
- 草拟一句 prank 文案
- 判断这条线更像 bot-scope 还是 user-scope
- 判断以后该继续从这个渠道切入，还是换回 local-pranks

planning-only turn 的重点不是写大计划，而是留下一个对下一轮有用的小判断。

## 真正发出去时怎么想

一旦下面这几个条件同时成立，就不要总停在 planning：

- 某个 channel 真的存在
- `canSend` 为真
- 当前 role 看起来合理
- 你手里已经有一个可信 target

这时候可以直接发一条短 prank message。

优先考虑：

- 一句突然蹦出来的怪话
- 一条很像 bot 突然皮了一下的消息
- 一条短到不会让人烦，但足够让对方愣一下的内容

不要因为“这条线还是探索面”就永远不敢真的发。

## target 不明确时怎么处理

如果用户已经明确给了：

- @username
- chat id
- 群组名
- thread 线索

那就可以直接沿这个 target 往下走，不必非得等 directory 里自动列出它。

如果用户没给 target，而 `operator-targets` 里也暂时没有可靠对象：

- 可以先记一条 planning note
- 可以先草拟一句 message
- 可以下一轮继续观察
- 也可以退回 local-pranks

重点不是强行发，而是不要假装自己已经有一个并不存在的社交图谱。

## 文案方向

朋友整蛊的消息文案要更像“突然蹦出来的一句怪话”，而不是产品说明书。

优先：

- 短
- 有角色感
- 像真人或 bot 会突然冒出来说的话
- 留一点“你刚刚是不是被盯上了”的感觉

避免：

- 解释自己是谁、怎么做到的
- 过长铺垫
- 伪装成系统告警
- 假装有你没确认过的社交关系

## 给 operator 的提醒

- 这条线是机会型分支，不是强制主线
- 如果 host 明显没有相关工具，就不要硬装有
- 如果有相关工具，但角色和 scope 还不清楚，可以先做 planning turn
- 如果有相关工具、role 也合理、target 也可信，就可以真的发一条
- 如果这轮更适合 local-pranks，就回去走 local-pranks
- 如果真的要发，就发一条短而有效的，不要一上来搞大编排
