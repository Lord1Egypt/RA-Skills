# Pattern Memory

按软件名称 / 网页域名沉淀已验证的执行经验。

## 目标
- 对同一软件或同一域名，优先复用已验证成功的路径。
- 减少重复试错，缩短执行时间，降低对前台焦点的打扰。
- 只记录“已验证成功”或“已验证失败且可复现”的事实，不记录猜测。

## 记录粒度
- 本地应用：按 `app-name` 建文件，如 `site-patterns/wechat.md`、`site-patterns/microsoft-teams.md`
- 网页任务：按域名建文件，如 `site-patterns/x.com.md`、`site-patterns/feishu.cn.md`

## 建议结构
```markdown
---
kind: local-app | website
name: WeChat
app_id: com.tencent.xinWeChat
aliases: [微信, WeChat]
domain: x.com
updated: 2026-03-27
---

## 成功路径
- [2026-03-27] 前台执行：open -a WeChat → Command+F → 粘贴联系人 → Enter → 粘贴消息 → Enter

## 前提条件
- 输入焦点必须在聊天列表或主窗口
- 中文联系人搜索可用

## 不可行/不稳定路径
- [2026-03-27] 纯后台键盘注入：不稳定，无法可靠确认焦点归属

## 经验结论
- 发消息任务默认采用“后台准备 + 前台短执行 + 发送后校验”
```

## 使用规则
- 一旦目标对象已命中对应经验文件，先读经验，再决定是否走通用探索。
- 如果经验中的首选路径本次再次成功，继续沿用，无需重复探索次优路径。
- 如果首选路径失效，再回退到通用优先级策略，并在完成后更新经验。
- 经验优先级低于用户明确要求；若用户要求“静默模式”，可尝试静默路径，但必须说明成功率风险。
