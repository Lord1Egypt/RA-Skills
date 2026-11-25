# AGENTS.md 片段 · 能力闭环接管（v2）

> 用途：把下面 12 行贴进工程根 `AGENTS.md`（或 `.agents/AGENTS.md`）。DSH 会在每个会话首个请求前自动注入这条链（`@deepseek-ai/dsh-agent-instructions`），所以它是**一定进上下文**的软接管。
> 硬接管（宿主插件注入契约、面板）见 `references/02-takeover.md` 的 P1/P2；本片段是 P0，不装插件今天就能用。
> 标记行 `<!-- dsh-capability-loop:on -->` 同时是**接管判定**的兜底：插件在 P1 会读它。

## 复制以下内容

```markdown
<!-- dsh-capability-loop:on -->
## 能力闭环（本工程）

动手或交付前先读 `.dsh/loop/state.json`：按 `stage` 与 `next` 执行；文件不存在就按普通流程，不要追问接入。
- **适用**：需求/方案、设计/改版、实现与交接、测试与验收、复盘。
- **豁免**：只读问答、单文件小改（≤30 分钟）、纯闲聊 —— 直接做，不套流程。
- **证据**：说“完成/已修复/已通过”必须给命令 + 退出码或截图；拿不到实测就写“未实测 + 原因 + 补测方式”。
- **门禁**：任务收口跑 `loop-gate.ps1`（脚本在 skill 的 `scripts/`，路径以 `state.json` 所在工程为 `-Workspace`）；FAIL 时只说“未通过 + 缺什么”。
- **自审不顶门**：PASS 不得由写的人自己给；交付前做 grill（`grill-*.md`）。
- **写回**：门禁/体检会自动写 `.dsh/loop/state.json`；改 skill 本体必须在同一提交 bump `version.json` + `CHANGELOG.md`。
```

## 为什么是这几行

| 行 | 作用 | 少了会怎样 |
|---|---|---|
| 标记行 | 接管判定 + 面板识别 | 面板显示「未接管」；P1 插件不注入 |
| 先读 state | 让模型知道阶段/下一步 | 每轮从零推测，等于没接管 |
| 适用/豁免 | 防止过度治理 | 闲聊也被追问六问，用户会关掉接管 |
| 证据 | 「证据先于结论」的下限 | 「已完成」不可证，返工 |
| 门禁 | 把脚本接进流程 | 门禁只在模型想起来时跑 |
| 自审不顶门 | 评审独立性的下限 | 自己给自己 PASS |
| 写回 | 状态源与面板同源 | 面板与真实进度脱节 |

## 注意

- **不要把整套 `SKILL.md` 或 `references/` 贴进来**：那是 24 KB+，每轮都付费；片段只放路由，细节按需 `read`。
- `state.json` 默认进 `.dsh/loop/.gitignore`（`loop-state.ps1 -Action init` 自动写）；`project.json` 随仓库提交。
- 想先试水：`loop-state.ps1 -Action init -Root <工程> -Mode shadow`，前 3 个会话只记录不阻断，再 `-Action set-mode -Mode on`。
- 移除接管：删标记行，或 `loop-state.ps1 -Action set-mode -Mode off`。
