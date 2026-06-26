---
name: "diagnose-openclaw-model-routing-and-fallback-usage"
description: "用于分析 OpenClaw 中“某个 provider/模型为什么看起来没被用上”、主模型与 fallback 实际是否生效、以及 ClaudeCodeCLI 协作任务为何中断。遇到这些情况就应触发：用户提到“没请求打到 local-router”“明明注册了模型却没流量”“Agent 到底在用哪个模型”“fallback 有没有发生”“为什么日志里看不到候选切换”“code 143 / SIGTERM / Exec failed”“需要结合当前配置和日志做严谨归因”。也适用于区分“provider 被调用”与“provider 下某个特定模型被调用”这两类常见混淆。"
metadata: { "openclaw": { "emoji": "🧭" } }
---

# 诊断 OpenClaw 的模型路由、fallback 使用情况与 CLI 中断原因

这个技能帮助你把 OpenClaw 的 Agent 配置、provider 注册信息和运行日志串起来，判断“请求到底发到了哪里、为什么某个模型没有被实际使用、fallback 是否真的发生过”，并补充分析 ClaudeCodeCLI 协作执行中断的根因。

## When to use this skill
- 当用户怀疑“模型明明配置了，但实际没在跑”，需要区分“已注册可用”与“已绑定到执行链路”。
- 当用户要你结合 OpenClaw 当前配置和日志，判断主模型、fallback 链、provider 命中情况，而不是只做静态配置解读。
- 当用户问“是否所有请求都成功”“有没有进入 fallback”“为什么感觉都在走 GPT / 没走 Claude”。
- 当 OpenClaw 调起 ClaudeCodeCLI 失败，出现 `Exec failed`、`code 143`、中途被杀、无 stdout 等现象，需要给出可执行的规避方案。

## Steps

1. **先区分用户到底在问“provider 没被调用”，还是“provider 下某个模型没被调用”**
   - 要做什么：先把问题拆成两层再分析：
     - `local-router` 这个 provider 是否被请求命中
     - `local-router/claude-opus-4-6-thinking` 这个具体模型是否被 Agent 主链或 fallback 链使用
   - 为什么：这两件事最容易被混为一谈；provider 有流量，不代表 provider 里的每个模型都有流量。

2. **读取当前各 Agent 的主模型配置**
   - 要做什么：核对 `main`、`coder`、`writer` 当前绑定的模型。
   - 已验证结论：
     - `main` → `local-router/gpt-5.4`
     - `coder` → `local-router/gpt-5.4`
     - `writer` → `local-router/gpt-5.4`
   - 为什么：用户的体感常来自“回答风格不像预期模型”，而主模型配置是最直接的证据链起点。

3. **读取默认 fallback 链，而不是只看 provider 的 models 列表**
   - 要做什么：核对 `agents.defaults.model` 的 primary 和 fallbacks。
   - 已验证结论：
     - primary: `local-router/gpt-5.4`
     - fallbacks:
       1. `aigocode-gpt/gpt-5.4-codex`
       2. `openai-codex/gpt-5.4`
       3. `local-router/gpt-5.3-codex`
       4. `aigocode-gpt/gpt-5.3-codex`
   - 为什么：模型是否“会自然切到某个候选”，取决于 fallback 链有没有引用它，而不是 provider 是否声明过它可用。

4. **检查目标模型只是“已注册”，还是“已绑定”**
   - 要做什么：确认 `local-router/claude-opus-4-6-thinking` 所在位置。
   - 已验证结论：
     - 它存在于 `models.providers.local-router.models[]`
     - 但当前没有任何 Agent 主模型引用它
     - 默认 fallback 链也没有引用它
   - 为什么：`provider 中存在` 只表示“可选”，不表示“当前执行链会使用”。

5. **给出第一层诊断结论：为什么用户感觉没请求发到某个模型**
   - 要做什么：明确输出这类结论：
     - 如果用户特指 `local-router/claude-opus-4-6-thinking`，那“感觉没流量”是正确的
     - 因为它当前既不是主模型，也不在默认 fallback 链里
   - 为什么：这能把“错觉”变成“配置导致的必然结果”，降低误判。

6. **同时纠正另一种常见误解：不能把“没打到目标模型”误说成“没打到 provider”**
   - 要做什么：说明当前主模型本身就是 `local-router/gpt-5.4`，所以请求确实在打 `local-router` provider。
   - 已验证线索：
     - 日志中大量出现：`OpenClaw fallback model: gpt-5.4 via http://localhost:8317/v1`
   - 为什么：用户往往观察的是模型风格或某个具体模型名，而不是 provider 维度的流量。

7. **补充历史与当前状态的区别，避免把旧日志当成当前事实**
   - 要做什么：如果系统里有历史上目标模型被调用的痕迹，要明确说明“曾经用过”不等于“现在还在用”。
   - 已验证历史线索：
     - 曾出现过 `requested=local-router/claude-opus-4-6-thinking`
     - 曾出现 `candidate_failed... reason=rate_limit`
     - 然后 fallback 到 `aigocode-gpt/gpt-5.4-codex`
   - 为什么：日志回看很容易把旧配置时期的调用轨迹误判为当前链路。

8. **检查辅助链路，避免只盯主 Agent**
   - 要做什么：同时看 memory/plugin 等辅助组件的模型。
   - 已验证线索：
     - `memos-local-openclaw-plugin` 的 summarizer 使用 `claude-sonnet-4-6`
     - endpoint 为 `http://localhost:8317/v1`
   - 为什么：系统可能“用了 local-router”，但用在插件辅助链路，而不是主 Agent；这会影响用户体感。

9. **针对“是否所有请求到 local-router/gpt-5.4 都成功”做日志核验**
   - 要做什么：不要只依据配置；要找失败证据。
   - 已验证失败日志：
     - `2026-03-14T05:32:22.073+08:00`
     - `embedded run agent end`
     - `isError=true`
     - `model=gpt-5.4`
     - `provider=local-router`
     - `error=500 Post "https://chatgpt.com/backend-api/codex/responses": EOF`
   - 为什么：只要存在一条明确失败记录，就足以否定“全部成功”这个命题。

10. **区分“没有看到 fallback 证据”与“没有发生 fallback”**
    - 要做什么：检查是否存在标准化 fallback 决策日志。
    - 已验证精确结果：
      - `requested=local-router/gpt-5.4` → `0` 条
      - `candidate_failed requested=local-router/gpt-5.4` → `0` 条
      - `candidate_succeeded requested=local-router/gpt-5.4` → `0` 条
    - 为什么：日志中缺少标准字段，只能说明“证据不完整”，不能直接推出“绝对没有 fallback”。

11. **解释为什么 `OpenClaw fallback model: gpt-5.4 via http://localhost:8317/v1` 不能直接当作 fallback 发生证据**
    - 要做什么：把这类日志视为“配置/调试打印”的高可能信号，而不是逐请求 fallback 决策记录。
    - 为什么：否则会把“当前 fallback 配置值”误读成“本次请求确实从主模型掉进 fallback 候选”。

12. **给出严谨结论，而不是过度下判断**
    - 要做什么：按证据强度输出：
      - 可以确定：`local-router/gpt-5.4` 是当前主模型
      - 可以确定：并非所有请求都成功
      - 不能确定：所有失败后都没有进入 fallback
      - 只能说：当前看不到清晰完整的标准 fallback 决策链
    - 为什么：这种问题最怕把“没查到”说成“没有发生”。

13. **当用户追问 ClaudeCodeCLI 中断原因时，先解读退出码**
    - 要做什么：对 `Exec failed (..., code 143)` 进行归因。
    - 已验证解释：
      - `143 = 128 + 15`
      - 通常对应 `SIGTERM`
      - 表现为“被外部终止”
    - 为什么：退出码是判断“CLI 自己报错”还是“外层执行环境杀进程”的关键证据。

14. **结合执行现象判断是外层 exec/调度问题，而非 Claude 本身逻辑错误**
    - 要做什么：结合这些现象给结论：
      - 会话：`mild-breeze`
      - 状态：`failed`
      - 持续约 3 分钟 1 秒
      - 没留下有效 stdout
    - 结论：高概率不是 Claude 自己正常报错退出，而是外层执行容器/调度把进程终止了。
    - 为什么：如果是参数、权限、认证、网络等 CLI 级错误，通常更容易留下 stderr 或非 143 退出码。

15. **给出高概率原因排序**
    - 要做什么：按优先级解释中断来源：
      1. 外层 exec 会话超时或被回收
      2. `stdin` / heredoc / pipeline 方式不稳
      3. Claude CLI 等待某些外部资源，导致上层误判并终止
    - 已验证调用方式线索：
      - 先写 `/tmp/claude_review_prompt.txt`
      - 再 `claude -p < /tmp/claude_review_prompt.txt`
    - 为什么：用户不仅要知道“发生了什么”，还要知道后续流程该避免什么。

16. **在后续流程中改用结果落盘，而不是只依赖 stdout**
    - 要做什么：用输出文件保存结果与错误。
   - 已验证建议命令：
     ```bash
     claude -p... > /tmp/claude_review_output.txt 2>/tmp/claude_review_error.txt
     ```
   - 为什么：即使 session 输出流断掉，也更有机会保住最终产物，方便补救和审计。

17. **改用后台任务 + 轮询方式管理长任务**
    - 要做什么：后续流程改为：
      1. 后台启动 Claude Code review
      2. 记录 session id / pid
      3. 轮询进程状态
      4. 检查结果文件是否生成
      5. 超时则显式判定失败并回收
    - 为什么：这比“前台阻塞等待 stdout”更稳，更适合 OpenClaw 编排外部 CLI。

18. **在正式大任务前加最小健康探针**
    - 要做什么：先运行极小命令，例如：
      ```bash
      claude -p "reply with OK"
      ```
    - 验证点：
      - 命令是否可返回
      - 当前认证是否正常
      - print 模式是否正常
      - 当前工作目录是否会触发异常
    - 为什么：先发现环境问题，能避免把长任务直接送进不稳定链路。

19. **区分多层超时并单独处理**
    - 要做什么：将超时拆成：
      - CLI 内部超时
      - OpenClaw exec 外层超时
      - 结果文件未生成超时
    - 为什么：这样才能知道究竟是模型慢、CLI 卡住，还是 orchestrator 把子进程回收了。

20. **输出时直接闭环，不把“继续捞结果”再抛回给用户**
    - 要做什么：在这种协作流程里，直接输出：
      - 配置分析结果
      - 日志证据
      - 失败归因
      - 后续规避方案
    - 为什么：用户要求的是完成后的结果整理，而不是让用户再决定是否继续补救链路。

## Pitfalls and solutions

❌ **看到 provider 里注册了某模型，就认定它在被使用**  
→ 失败原因：`models.providers.local-router.models[]` 只能证明“可用”，不能证明“某个 Agent 正在引用它”  
✅ **先查 Agent 主模型和 fallback 链，再判断模型是否真在执行链路中**

❌ **把“没打到 local-router/claude-opus-4-6-thinking”理解成“没打到 local-router provider”**  
→ 失败原因：provider 命中和具体模型命中是两层概念  
✅ **分别判断 provider 流量和模型流量；当前确实在打 `local-router`，但主走的是 `local-router/gpt-5.4`**

❌ **只看当前 provider 声明，不看 fallback 链**  
→ 失败原因：某模型不在 fallback 链里，就算主模型失败也不会自然切过去  
✅ **核对 `agents.defaults.model` 的完整 fallback 列表**

❌ **看到 `OpenClaw fallback model: gpt-5.4 via http://localhost:8317/v1` 就断言“本次请求发生了 fallback”**  
→ 失败原因：这类日志更像配置/调试打印，不一定是逐请求决策日志  
✅ **以 `requested=...`、`candidate_failed`、`candidate_succeeded` 这类更强证据为准**

❌ **因为没查到标准 fallback 日志，就断言“完全没有 fallback”**  
→ 失败原因：日志打点可能不完整，错误也可能发生在 provider 适配器层  
✅ **表述为“当前没有看到清晰完整的 fallback 决策证据”，避免过度结论**

❌ **把一次 `500 EOF` 失败忽略掉，继续说“所有请求都成功”**  
→ 失败原因：只要存在一条明确失败日志，就足以推翻“全成功”  
✅ **先确认是否有任意失败样本，再谈成功率和 fallback 概率**

❌ **把 `code 143` 当作 ClaudeCodeCLI 自身功能错误**  
→ 失败原因：`143` 通常是 `SIGTERM`，更像外层调度/会话终止  
✅ **优先从 exec 包装层、会话回收、超时策略和 stdin 生命周期分析**

❌ **直接前台等待长任务 stdout 作为唯一结果来源**  
→ 失败原因：会话被回收时，stdout 常常拿不到，导致“任务做了但结果丢了”  
✅ **把 stdout/stderr 都落盘，并用后台轮询接回结果**

❌ **用 heredoc / stdin 重定向跑长时间 CLI，而不做探针**  
→ 失败原因：包装层对子进程树和输入流生命周期不稳定  
✅ **先跑 `claude -p "reply with OK"` 探针，再启动正式任务**

## Key code and configuration

### 当前 Agent 主模型与默认 fallback（已验证）
```yaml
agents:
  main:
    model: local-router/gpt-5.4
  coder:
    model: local-router/gpt-5.4
  writer:
    model: local-router/gpt-5.4

  defaults:
    model:
      primary: local-router/gpt-5.4
      fallbacks:
        - aigocode-gpt/gpt-5.4-codex
        - openai-codex/gpt-5.4
        - local-router/gpt-5.3-codex
        - aigocode-gpt/gpt-5.3-codex
```

### 目标模型当前所处位置（已验证语义）
```yaml
models:
  providers:
    local-router:
      models:
        - local-router/gpt-5.4
        - local-router/gpt-5.3-codex
        - local-router/claude-opus-4-6-thinking
        - claude-sonnet-4-6
```

### 关键失败日志样例：证明 `local-router/gpt-5.4` 并非全成功
```text
2026-03-14T05:32:22.073+08:00
embedded run agent end
isError=true
model=gpt-5.4
provider=local-router
error=500 Post "https://chatgpt.com/backend-api/codex/responses": EOF
```

### 历史上目标 Claude 模型曾被请求的证据样式
```text
requested=local-router/claude-opus-4-6-thinking
candidate_failed... reason=rate_limit
fallback -> aigocode-gpt/gpt-5.4-codex
```

### 当前缺失的标准 fallback 决策证据
```text
requested=local-router/gpt-5.4 -> 0
candidate_failed requested=local-router/gpt-5.4 -> 0
candidate_succeeded requested=local-router/gpt-5.4 -> 0
```

### 辅助链路使用的模型线索
```text
memos-local-openclaw-plugin summarizer:
model = claude-sonnet-4-6
endpoint = http://localhost:8317/v1
```

### ClaudeCodeCLI 中断的关键状态
```text
session = mild-breeze
status = failed
duration ≈ 3m1s
Exec failed (..., code 143)
```

### 不稳定的调用方式线索
```bash
claude -p < /tmp/claude_review_prompt.txt
```

### 更稳的结果落盘方式
```bash
claude -p... > /tmp/claude_review_output.txt 2>/tmp/claude_review_error.txt
```

### 最小健康探针
```bash
claude -p "reply with OK"
```

## Environment and prerequisites

- 需要有 OpenClaw 当前配置读取权限，至少能查看：
  - `agents.main`
  - `agents.coder`
  - `agents.writer`
  - `agents.defaults.model`
  - `models.providers.local-router.models[]`
- 需要能读取 OpenClaw 运行日志或聚合日志。
- 需要能看到与 provider、model、fallback、embedded run、plugin summarizer 相关的日志字段。
- 若要分析 CLI 中断，需要能读取 exec session 状态、退出码、持续时间，以及 stdout/stderr 是否落盘。
- 若要复现规避方案，需要本机可执行 `claude` CLI，并允许将输出重定向到临时文件。
- 对 `code 143` 的分析依赖类 Unix 退出码语义：`143 = 128 + 15 = SIGTERM`。

## Companion files

- `references/claudecodecli-exit-code-143-sigterm-reference.md` — reference documentation
- `references/openclaw-fallback-log-interpretation-reference.md` — reference documentation