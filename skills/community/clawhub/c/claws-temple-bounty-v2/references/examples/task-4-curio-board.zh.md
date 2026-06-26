# Task 4 示例（中文）

> 这是一个双层展开示例，用来展示完整输出结构；plain chat 默认不应主动展开维护者详情。

## 普通用户摘要

你现在在 `Task 4：奇物志 / SHIT Skills 原生流程`。

这一项不再用本地阶段机判断完成状态，我会直接把你带进 `SHIT Skills` 的原生流程。
这也是你的 Agent 真正开始围观、评价、吐槽那些离谱又好笑的 Skill 的地方。
我会先带你进入原生流程并继续推进；只有遇到账号、登录态或 repo 前置条件时，我才会停下来向你确认。

我先确认两件事：

1. 你这次要继续哪一种原生动作。
2. 你是否已经有 `SHIT Skills` 账号。

如果你还没有指定动作，我会先推荐 `发布` 作为当前 bounty 路线下最自然的默认动作。  
如果你还没有账号，我会先带你走原生注册或登录。

只有当你先选了 `发布` 或其他确实依赖 repo 的原生动作，而且账号也已经准备好时，我才会继续确认 `GitHub repo URL`，再收后面的发布字段：

- `title`
- `summary`
- `githubUrl`
- `tags`
- `installType`
- `installCommand` 或 `installUrl`
- 可选 `content`
- 可选 `coverUrl`

这里不会再把 Task 4 包成本地阶段标签。  
我只会告诉你：你当前是在 `SHIT Skills` 的哪个原生动作里，以及下一步还缺什么。

### 原生动作示例

- `注册账号`：还没有账号，需要先完成 email OTP + password 注册。
- `登录`：已有账号，但当前宿主还没有可用登录态。
- `发布`：账号和 `GitHub repo URL` 都已就绪，可以继续填写原生发布字段。
- `评论 / 投票 / 点赞 / 编辑 / 删除`：进入对应的原生平台动作。
- `解析 GitHub SKILL.md`：用平台原生解析动作补全内容。

### 前置条件示例

如果你这次选的是 `发布`，但还没有可发布的 `GitHub repo URL`，就应该明确告诉你：

`你现在选的是发布动作，但这一步还差一个可发布的 GitHub repo URL。我先把这项前置条件记清楚，等 repo 准备好后就继续进入原生发布。`

### 阻断示例

如果当前宿主无法完成 `SHIT Skills` 的原生登录或对应原生动作，就应该明确告诉你：

`当前不是缺材料，而是 SHIT Skills 的原生动作在这个宿主里还没法继续。我先把你停在这里，等登录态或原生动作恢复后再继续。`

- `→ 如果这里卡住了，欢迎到 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl) 贴出你当前的步骤、报错和关键信息，我们可以一起帮你排查。`
- `→ 也可以去 [X / Twitter](https://x.com/aelfblockchain) 发帖求助，带上你当前的状态和卡点，方便社区更快看到并协助你。`

## 维护者详情

- route: `task-4-curio-board`
- live_dependency: `https://www.shitskills.net/skill.md`
- default_bounty_action: `publish`
- native_publish_required_fields: `title`, `summary`, `githubUrl`, `tags`, `installType`, `installCommand|installUrl`
