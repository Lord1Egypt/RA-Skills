# SkillHunt 发布文案

## 标题

Audit Evolution: 我们用它把 Longju 跑到 93.0、Jobs 跑到 88.8

## 一句话

一套可复现的 Agent 自进化飞行记录仪：每次运行后自动找证据、审计状态、沉淀记忆、提出最小补丁，让 Agent 越跑越强。

## 简介

Audit Evolution 把一次 Agent 运行记录转成下一轮进化输入。我们用这套闭环把 Longju 推到 `93.0/100`，把 Jobs 从 `76.4 -> 78.8 -> 88.8`，证明它不是概念 demo，而是一套可以复现的 Agent 自进化工作流。

用户不需要先整理材料，只要说一句“开始调用 Audit Evolution”，Agent 就会先从当前上下文和允许访问的文件里自动寻找最近任务记录、用户反馈、失败/超时/重试记录、benchmark、worklog、handoff、receipt、skill/config/gear 修改记录。

然后它会生成：

1. `Evidence Pack`: 找到了哪些证据、缺了哪些证据、可信度如何。
2. `Snapshot`: 当前可信状态、未知状态、停止条件。
3. `Evolution Card`: 本轮最该提升的能力维度和证据。
4. `Memory Ledger Entry`: 本轮值得沉淀的少量可检索记忆。
5. `Minimal Skill Patch Proposal`: 一个最小可执行 skill 补丁提案。
6. `Field Note`: 可发社区的测试记录。
7. `Next-Run Bootstrap`: 下一轮启动时必须优先读取或执行的短指令。

它不是只在 Agent 崩溃时救火，而是让 Agent 每一次完成任务后，都能沉淀一个可复用能力。

它也不是普通的 memory skill。普通 memory 往往什么都记，最后变成新的噪音。Audit Evolution 只沉淀 `verified_fact / user_feedback / decision / skill_patch / retrieval_key / next_run_bootstrap`，并且每条都带证据、可信度、过期条件和下一轮检索 key。

最后一步不是自动乱改系统，而是问人类：

```text
是否批准开始进化？
1. 只保存审计结果
2. 应用最小补丁并本地测试
3. 暂停，等待更多证据
```

为了让普通用户更容易用，每轮最后还会给一个短指令菜单：

```text
你可以直接回复：
进化 / 保存 / 暂停 / 跑分 / 继续 / 详情
```

Agent 会自己判断当前阶段：

- `进化`: 可能是先审计、应用本地补丁、请求一次 benchmark 证据，或提出下一轮。
- `保存`: 只保存审计结果。
- `暂停`: 写 handoff 并停止。
- `跑分`: 没有授权就先请求批准，已授权才跑 exactly one。
- `详情`: 展开证据和判断依据。

## 自动触发

装上以后，不应该每次都等用户手动说“Use Audit Evolution”。当出现以下任一事件时，Agent 应该主动调用：

- benchmark 完成。
- 用户指出错误、纠正事实、质疑结论。
- 任务失败、超时、重试、被阻塞。
- 上下文超过 60%。
- 本轮读取文件超过 5 个。
- 输出里出现“大概、可能、我理解为、不确定”等不可靠表达。
- 新增或修改 skill、config、gear、路由、答题范式后。

核心边界是：

```text
自动学习，半自动晋升，人工批准外部动作。
```

Agent 可以自动保存 run record、生成 evolution card、提出 minimal patch、跑本地检查、写 receipt。  
但 publish、upload、install、vote、comment、message、spend、official benchmark 等外部动作必须由人类批准。

## 适合谁

- 正在给 Agent 跑 BotLearn Benchmark 的开发者。
- 想让 Agent 越用越强的个人开发者。
- 做 Agent workflow / skill / prompt / automation 的团队。
- 需要可审计状态、交接和进化记录的人。

## 现场 30 秒体验

把这句话发给你的 Agent：

```text
开始调用 Audit Evolution。

目标：检查我最近一次任务后，是否应该继续自进化。
边界：先审计和提出建议，不要直接修改系统。
```

理想输出不是一段泛泛总结，而是：

```text
Evidence Pack -> Snapshot -> Evolution Card -> Memory Ledger Entry -> Minimal Skill Patch Proposal -> Field Note -> Next-Run Bootstrap -> 是否批准开始进化？
```

用户下一句不用写长 prompt，只要回：

```text
进化
```

## 下载后怎么用

这个 skill 支持三种使用方式：

1. 直接让 Agent 读取 `SKILL.md`，然后说“开始调用 Audit Evolution”。
2. 使用安装器写入 `AGENTS.md`，让 Codex / OpenClaw / 通用 Agent 自动识别触发条件。
3. 使用 `.audit-evolution/hooks/` 在任务失败、跑分完成、上下文超过 60% 时生成 run record。

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-audit-evolution.ps1 -TargetWorkspace "D:\YourAgentWorkspace" -Agent codex -Force
```

macOS / Linux:

```bash
bash ./scripts/install-audit-evolution.sh --target "$HOME/your-agent-workspace" --agent openclaw --force
```

## 现场 Demo

我们用 Longju 和 Jobs 两只 Agent 做了测试：

- Jobs: `76.4 -> 78.8 -> 88.8`
- Longju: 后期仍提升到 `93.0`

核心不是单次高分，而是把每轮反馈压成下一轮可执行 skill 修复。
