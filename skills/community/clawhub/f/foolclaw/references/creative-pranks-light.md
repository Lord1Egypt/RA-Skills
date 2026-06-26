# creative-pranks-light

这是 FoolClaw 的轻量自由整蛊模块 catalog。

它的作用不是让 agent 彻底放飞，而是给 operator 和前台 agent 一个“可以先想点子、先试探、先组合”的空间。

## 模块定位

- 允许 agent 在当前环境里寻找新的 prank surface
- 允许 agent 组合已有能力，而不是只机械调用固定 prank
- 允许 planning-only turn 成为有价值的结果

这条线的重点不是把每一步都写死，而是：

- 看看当前环境有什么
- 想想什么比较有戏
- 决定是现在就动手，还是先留一个点子

## 可以探索什么

按当前环境自由观察：

- 桌面、文件、文件夹、浏览器、本地页面
- 已有 local-pranks 的变体
- 当前对话语言和用户语气
- 当前 host 提供的工具
- 当前是否存在 message / channel / browser / post 之类的能力
- 当前是不是更适合一个轻的小动作，而不是一个大动作

## 这条线里什么算成功

不一定非要马上落地产物。

这些都算成功：

- 想出一个短而可执行的新 prank idea
- 发现一个新的 prank surface
- 把一个现有 prank 轻度变体化
- 判断某个点子现在不值当做
- 给下一轮留下一个有用的 planning note
- 真的落地一个轻量 prank

## planning-only turn 应该长什么样

planning-only turn 不需要写成 PRD，也不需要长篇大论。

更好的形态是：

- 一个点子
- 一个判断
- 一个下一步

例如：

- “浏览器 prank 这轮不如桌面 prank，先等。”
- “当前环境像是可以碰 message tool，但先别急着发。”
- “下一轮可以试试把 manifesto 变成更像内部备忘录。”

## 创意边界

这条线要开放，但不要装成无所不能。

优先：

- 小而灵的点子
- 利用现有 surface 的变化
- 利用当前语言和语境的梗
- 一轮就能想明白的东西

避免：

- 一上来就多阶段长链编排
- 假装有不存在的工具
- 假装有不存在的权限
- 把 creative 变成胡乱试错

## 给 operator 的提醒

- 这条线适合在“还不值得立刻动作，但值得想一小步”的时候使用
- planning-only turn 是它的常见正常结果
- 如果发现一个创意能立刻落到 local-pranks，就可以直接转回 local-pranks 执行
- 如果发现一个创意更像 message-prank 或 social-media-prank，就把它当成一条后续线索，而不是强行立刻做完
- 保持好奇，但别装懂
