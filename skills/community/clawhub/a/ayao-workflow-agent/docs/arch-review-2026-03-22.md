# Architecture Review — 2026-03-22

> 审查范围：coding-swarm-agent 全系统（SKILL.md、playbook、18 个脚本共 3251 行、5 个 prompt 模板、task schema）
> 对比参考：gstack（garrytan/gstack）
> 审查者立场：不客气，直接说问题。

---

## 第一部分：核心假设评估

### 假设 1："Codex 后端 / Claude Code 前端"的分工仍然成立？

**Partial — 站不住脚的时间不会超过 6 个月。**

当前分工的真正驱动力不是能力差异，而是**成本和配额管理**。Claude Code Max 会员的 opus 额度有限但 sonnet 充足，Codex Pro 的 gpt-5.4 额度充足。所以"后端用 Codex 省 Claude 额度"本质上是一个**经济决策伪装成架构决策**。

问题在于：
1. 2026 年两家模型能力已经高度趋同，"Claude 适合前端、Codex 适合后端"没有技术依据
2. 一旦任何一家调整定价或额度（历史上每 3-6 个月就发生一次），整个分工逻辑要重写
3. 这个假设已经在系统中硬编码到了命名规范（`codex-1`, `cc-frontend`）、prompt 模板、dispatch 逻辑、agent-pool 结构中，切换成本很高

**建议：** 把模型选择从 agent 身份中解耦。agent 应该按**职责**命名（`backend-1`, `frontend-1`），底层用哪个模型应该是一个配置项，不是架构决策。

### 假设 2："Main branch only + 原子 commit"安全吗？

**Partial — 对个人开发安全，对任何需要协作的场景危险。**

代价清单（playbook 没有充分讨论的）：
1. **没有 feature-level review**：每个 commit 单独原子验证，但没有人从"这个功能整体对不对"的角度 review。20 个正确的 commit 可能组合出一个错误的功能。
2. **回滚是假安全网**：`git revert` 对单个 commit 有效，但如果一个 batch 的 18 个 commit 互相依赖（它们确实依赖），回滚第 3 个 commit 会破坏第 4-18 个。你需要回滚整个 batch，但系统没有 batch-level rollback 机制。
3. **没有 CI**：tsc + ESLint 是 commit-level 门禁，但没有集成测试、没有端到端测试。一个 commit 类型正确但运行时崩溃的代码会直接推到 main。
4. **多人协作时是灾难**：两个人同时跑 swarm，两组 agent 往同一个 main 推 commit，文件隔离靠人工保证。没有锁，没有合并冲突检测，没有 CI 卡点。

**事实上你已经遇到了症状**：playbook 18.2 节记录了 cc-frontend 超额完成（做了没派给它的任务）、agent 改了 scope 外的文件需要 revert。这些都是 main-branch-only 模式下缺乏隔离的直接后果。

**建议：** 不需要切到 full PR flow。但至少需要：(a) batch-level tag，支持 `git revert batch-N..HEAD` 式的回滚；(b) 在 batch 前后跑一次完整测试（如果项目有的话）；(c) 对多人场景明确说"不支持"或加互斥锁。

### 假设 3："AI orchestrator 自主分解任务"质量有保证？

**No — 这是整个系统最被低估的风险。**

系统的核心循环是：用户给需求 → orchestrator 分解任务 → dispatch 到 agent。但 orchestrator 本身也是 AI。如果分解质量差（粒度不对、依赖关系遗漏、scope 重叠），下游所有 agent 的工作都建立在错误基础上。

v2.6 的 Plan 三层规范试图解决这个问题，但仍然是 AI 读 AI 的设计文档再分解任务。没有人类在任务分解环节的 gate。playbook 说"人类只在升级时介入"，但任务分解质量差不会触发升级——agent 会按照错误的分解认真执行，产出一堆"正确但无用"的代码。

**对比 gstack：** gstack 的方式是人类保持在循环中（plan mode 需要人类 approve），agent 做的是 review 和 QA，不是自主分解。这是一个根本不同的信任模型。

**建议：** 任务分解后、dispatch 前，必须有一个人类确认步骤（至少 B 档和 C 档任务）。可以是 Telegram 确认，不需要坐在电脑前。

### 假设 4："Cross-review"用同一家的两个模型互审，盲区重叠？

**Partial — 比不 review 好很多，但有结构性盲区。**

Claude 和 GPT 确实是不同架构、不同训练数据，互审能发现一些对方的盲点。PolyGo 的 T006 nonce 问题被 cc-review 抓到就是一个成功案例。

但是：
1. 两家在安全漏洞检测上的能力都不如专用安全工具（semgrep、CodeQL）
2. 两家都倾向于认为"看起来合理"的代码是正确的，对业务逻辑的正确性缺乏判断力
3. review prompt 模板侧重代码质量（风格、命名、edge case），没有业务逻辑验证维度

**更大的问题：** review 只看 diff，不看代码在整个系统中的上下文。Agent 可能写了一个完美的函数，但它和已有代码的交互方式是错的。Diff-only review 抓不到这类问题。

---

## 第二部分：最严重的 3 个架构问题

### 问题 1：Shell 脚本 orchestration 是一条死路

**严重程度：致命（12 个月内必须解决）**

当前状况：
- 18 个 shell 脚本，3251 行 bash + 大量内联 python
- 脚本之间通过文件系统（JSON 文件 + flock）通信
- 错误处理依赖 exit code、trap、pid 文件
- 调试手段：`tail -5 /tmp/agent-swarm-signals.jsonl` + `tmux capture-pane`

这已经是一个中等复杂度的分布式系统，但用了最不适合写分布式系统的语言。

具体风险：
1. **不可测试**：没有单元测试，没有集成测试。`dispatch.sh` 342 行，任何改动都是盲改。playbook v1 到 v2.5 的每次升级都是"踩坑 → 打补丁"，没有"跑测试 → 确认不回归"
2. **竞态条件**：虽然用了 flock，但 flock 在 macOS 上的行为和 Linux 不同（macOS 的 flock 来自 util-linux homebrew，不是原生的）。agent-pool.json 和 active-tasks.json 的并发更新在高并行度下可能丢数据
3. **平台锁定到 macOS**：脚本中有 macOS 特定的假设（`/tmp` 行为、`mktemp` 格式、zsh 默认 shell），尽管做了一些兼容处理
4. **Anthropic 和 OpenAI 都在做 native multi-agent**：Claude Code 的 Agent tool 已经可以并行 dispatch 子 agent。Codex 的云端执行已经内置了隔离环境。6-12 个月内，tmux + shell 会变成完全不必要的基础设施

**对比 gstack：** gstack 完全没有 orchestration 层。每个 skill 是一个 Markdown 文件，由 Claude Code 原生执行。没有 tmux，没有 shell 脚本，没有外部进程。升级成本为零，因为没有基础设施要维护。

**建议：**
- 短期：把核心逻辑（task 状态机、agent 调度、token 追踪）重写为一个 TypeScript/Python 单文件程序，shell 脚本只做 thin wrapper
- 中期：评估 Claude Code 的 native Agent tool 能否替代 tmux dispatch。如果 `claude --model sonnet --print` 可以在子进程中运行并返回结果，就不需要 tmux
- 长期：整个 orchestration 层可能被平台 API 替代，保持架构足够薄以便迁移

### 问题 2：系统复杂度已经超过了单人可维护的阈值

**严重程度：高（现在就在造成问题）**

数据：
- SKILL.md：618 行
- Playbook：1140 行
- Shell 脚本：3251 行
- Prompt 模板：5 个文件
- 配置文件：active-tasks.json、agent-pool.json、config.json、notify-target、project-dir、hook-token
- 临时文件：signal file、log files、pid files、sent files、warned files、prompt tmpfiles
- 目录：scripts/、references/、projects/、docs/、swarm/

一个新手（或者 3 个月后的你自己）能在 10 分钟内定位一个 bug 吗？

具体案例：如果一个任务完成了但 Telegram 没收到通知，debug 路径是：
1. on-complete.sh 是否被调用？→ 检查 tmux 日志
2. update-task-status.sh 返回了什么？→ 检查 exit code 和 signal file
3. openclaw system event 是否发出？→ 检查 openclaw 日志
4. notify-target 配置对吗？→ 检查 swarm-config.sh resolve 结果
5. openclaw message send 成功了吗？→ 检查 Telegram API 响应
6. 是不是幂等去重挡掉了？→ 检查 /tmp/agent-swarm-complete/*.sent

6 步，涉及 4 个脚本、3 个配置源、2 个外部服务。这不是 10 分钟能搞定的。

**过度工程化的具体信号：**
- agent-manager.sh 的动态扩容逻辑（PolyGo 18 个任务最多用了 3 路并行，是否真的需要 auto-scale 到 codex-4 + cc-frontend-2 的能力？）
- 三层配置体系（Skill 层 / Workspace 层 / 项目层 / Gateway 层——实际上是四层）
- token 里程碑预警系统（用了多少次？值得 80 行 python 吗？）
- heartbeat 保活机制（每个 dispatch 启动一个后台进程每 5 分钟更新 last_seen——为了防止 health-check 误报，而 health-check 本身是否真的必要？）

**建议：** 做一次"哪些功能实际用过"的审计。没用过的删掉，不是注释掉，是删掉。复杂度不会自己消失，只会在下一次 debug 时咬你。

### 问题 3：编排层和执行层的边界在 v1.5.0 后已经模糊

**严重程度：中高（方向问题）**

v1.0 时系统定位清晰：orchestrate multi-agent **coding** workflows。
v1.5.0 加入了 writing、analysis、image generation。

现在 cc-plan 的职责是：
- 探索代码库，输出设计文档（原始职责）
- 写技术文章、产品需求文档、报告（prompt-cc-writing.md）
- 做竞品分析、技术评估、决策简报（prompt-cc-analysis.md）
- 生成图片（generate-image.sh）

这已经不是一个 "coding swarm agent"，这是一个 "general purpose AI workflow engine"。

问题：
1. 每种新能力都增加了 prompt 模板、可能的新脚本、新的 task domain 类型。系统的表面积在膨胀
2. writing 和 analysis 任务不需要 git commit、不需要 cross-review、不需要 scope 验证——但它们复用了相同的 dispatch + on-complete 流水线。这导致流水线中充斥着 `if domain == "writing" then skip review` 类型的条件分支
3. 名字叫 "coding-swarm-agent" 但做的事情远不止 coding。这造成认知负担——新用户看到名字以为只是代码工具，看到功能列表又会困惑

**建议：** 要么接受自己是一个通用 workflow engine 并重新命名和重构（剥离 coding-specific 逻辑为一个 workflow preset），要么把 writing/analysis 从 swarm 中移出来作为独立 skill（它们本来就不需要 multi-agent 协调）。

---

## 第三部分：系统边界建议

### 适合用在哪里

| 场景 | 适合度 | 理由 |
|------|--------|------|
| 单人开发、项目初期（<5 万行代码）| ✅ 很适合 | 原子 commit + main branch 模式在这个规模下风险可控 |
| 后端密集型项目（API、数据处理） | ✅ 很适合 | Codex 的 reasoning 能力配合精确 prompt 效果好 |
| 有明确规格的批量实现 | ✅ 最佳场景 | "18 个任务 2 小时"的 PolyGo 案例就是这个场景 |
| 需要大量 boilerplate 的项目 | ✅ 适合 | agent 擅长这个 |

### 不适合用在哪里

| 场景 | 适合度 | 理由 |
|------|--------|------|
| 多人团队同时开发 | ❌ 不适合 | main branch only 没有冲突解决机制 |
| 需要频繁 hotfix 的生产系统 | ⚠️ 勉强 | hotfix flow 存在但链路太长，紧急情况下手动更快 |
| 探索性开发（不确定要做什么）| ⚠️ 勉强 | 系统假设需求是清晰的，分解是可行的 |
| 大型 monorepo（>20 万行）| ⚠️ 未验证 | agent 的 context window 能否装下足够的代码理解？|
| 前端为主的项目 | ⚠️ 未验证 | UI 质量需要视觉验证，agent 做不到（除非接 screenshot） |
| 已有 CI/CD 和 PR 流程的团队 | ❌ 冲突 | 系统的设计哲学和 PR-based 工作流互斥 |

### PolyGo 当前规模是否合适？

合适。PolyGo 是一个中小型项目（单人、后端为主、有明确功能需求）。但随着项目增长到需要部署管道、多环境、集成测试的阶段，main-branch-only 的限制会越来越明显。

---

## 第四部分：最值得警惕的盲区

### 审计追踪缺失——出了事故你无法复盘

这是我认为**最容易被忽视但可能造成最大问题**的 1 个点。

当前的追踪能力：
- active-tasks.json 只保存**最终状态**，不保存历史状态变更
- signal file 是 append-only 的 JSONL，但只记录完成事件，不记录 dispatch、retry、review 的中间过程
- agent 的实际输出只保存在 `/tmp/agent-swarm-*.log`，临时文件重启后消失
- retro.jsonl 是事后总结，不是实时审计日志

想象这个场景：agent 在凌晨 3 点自动运行，产出的代码引入了一个安全漏洞，第二天上线后被利用。你需要回答：
1. 这个代码是哪个 agent 写的？→ 可以从 commit 追溯
2. 当时的 prompt 是什么？→ **丢失了**（tmpfile 已删）
3. 中间有没有 review？review 说了什么？→ **不确定**（review agent 的输出在 /tmp 里可能已经被覆盖）
4. orchestrator 当时为什么没有 catch 这个问题？→ **无法复盘**（AI 的"思考过程"没有持久化）

系统号称 "event-driven"，但事件日志不完整、不持久、不可查询。这在个人项目上问题不大，但如果用在任何需要问责的场景（金融、安全、合规），是一个致命缺陷。

**建议：**
1. prompt 文件保留 24 小时（或永久归档到 `projects/<slug>/prompts/`），不要 dispatch 完就删
2. 每个状态变更写一条审计日志（不是信号，是审计），包含 who、what、when、why
3. review 输出持久化到 task 记录中，不只是 pass/fail 结论

---

## 第五部分：整体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 架构合理性 | 6/10 | 核心循环（dispatch → complete → unblock → next）设计合理，但 shell 实现和文件系统通信是技术债 |
| 方向正确性 | 5/10 | "外部控制平面 orchestrate agents"这个方向在 2026 年 Q1 还可以，但 native multi-agent API 出来后会被替代。shell 脚本积累的复杂度很难迁移 |
| 复杂性控制 | 4/10 | 已经过了"一个人能完全掌握"的阈值。18 个脚本 3251 行 + 618 行 SKILL.md + 1140 行 playbook，没有测试，没有文档生成，debug 靠读代码。每次加功能都在增加复杂度但没有偿还技术债 |

### 一句话

**这套系统最大的风险是：你在用会被平台替代的基础设施（tmux + shell orchestration）积累越来越多的复杂度，而这些复杂度在迁移时几乎无法复用。**

---

## 附录：与 gstack 的方向对比

| 维度 | coding-swarm-agent | gstack |
|------|-------------------|--------|
| 哲学 | 外部控制平面，AI orchestrator 自主运行 | 给 agent 人格和流程，人类保持在循环中 |
| 实现 | tmux + 18 个 shell 脚本 + JSON 文件 | Markdown SKILL.md 文件，零外部基础设施 |
| 可移植性 | 绑定 macOS + tmux + OpenClaw | 任何支持 SKILL.md 的 agent（Claude Code、Codex、Gemini） |
| 升级成本 | 修改 shell 脚本，无测试，风险高 | 编辑 Markdown，git push |
| 并行模式 | 多 agent 在同一 repo 的同一 branch | 多 session 在不同 branch |
| 人类参与度 | 低（通知为主，升级才介入）| 中（plan mode 需 approve，review 需确认）|
| 适合场景 | 批量实现已知规格 | 迭代式开发，需求边开发边明确 |

**哪个方向更有生命力？**

坦率说，gstack 的方向更有生命力。原因不是 gstack 做得更好，而是它的赌注更安全：
- 如果 native multi-agent API 出来，gstack 几乎不需要改（它不依赖任何 orchestration 基础设施）
- 如果模型能力继续增强，gstack 的 role-based prompt 可以轻松升级
- 如果平台生态碎片化（Claude、Codex、Gemini 各自进化），gstack 已经跨平台了

coding-swarm-agent 如果要生存，需要在 shell orchestration 被替代之前完成两件事：
1. 把核心价值（任务分解规范、cross-review 流程、分级 review、prompt 模板）从 shell 基础设施中剥离出来
2. 找到一个平台无关的方式重新承载这些价值（可能是一个轻量级 TypeScript SDK，可能是纯 SKILL.md 模板）

这两件事不做，6-12 个月后 shell 脚本会变成纯负债。
