# 60 秒上手 Audit Evolution

你不需要先理解 SACP，也不需要整理一堆日志。把下面一句话发给你的 Agent：

```text
进化
```

如果 Agent 不知道 Audit Evolution，再发这段：

```text
开始调用 Audit Evolution。

请先从当前上下文和允许访问的文件里自动寻找最近一次任务输出、用户反馈、失败/超时/重试记录、benchmark、worklog、handoff、receipt、最近修改过的 skill/config/gear。

先审计，不要直接修改系统。
```

它应该先输出：

```text
Evidence Pack
Snapshot
Evolution Card
Memory Ledger Entry
Minimal Skill Patch Proposal
Field Note
Next-Run Bootstrap
Short Command Menu
```

最后它应该问你是否批准下一步。你只需要回复：

```text
进化 / 保存 / 暂停 / 跑分 / 详情
```

安全边界：

- 没有证据就标记 `unknown`。
- 最多先读 5 个相关文件。
- 未经批准不发布、不上传、不安装、不评论、不投票、不跑官方 benchmark。
- 默认只提出最小补丁，不直接改系统。
