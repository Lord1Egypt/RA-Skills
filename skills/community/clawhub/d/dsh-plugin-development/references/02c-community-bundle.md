# 社区零代码组合包范本 · `dsh-ouroboros` 分册

> **文件来源**：本文件由 `02-templates.md` 拆分而来，正文为原文的**逐行搬迁**，未做改写。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。本技能面向任务的整理稿见 `02-templates.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

---

<!-- ↓ 源：H-community-bundle.md （全文） -->

# H. 社区零代码组合包范本 —— `dsh-ouroboros`（原始素材）

> 来源：`plugin-research/src/Q00_ouroboros/integrations/dsh-plugin/`（仓库 `Q00/ouroboros`，约 5,805★）。
> 官方精选清单里**唯一一个"纯配置、零代码"插件**。**整个插件只有 3 个文件，没有一行 TypeScript。**
> 全部内容逐字照抄。

## 0. 为什么它是"最有教学价值"的范本

| 事实 | 说明 |
|---|---|
| 文件数 | **3**（`README.md` + `cordis.patch.yml` + `package.json`） |
| 源码 | **0 行** |
| 作用 | 把 Ouroboros（一个 Python 的 spec-first 开发工作流引擎）作为 MCP 工具挂进 dsh，给模型新增 **35 个工具** |
| 安装 | `dsh plugin --profile web add dsh-ouroboros` |

> 💡 **它证明了一件事：插件 ≠ 必须写代码。** 很多时候你想要的"集成外部工具"，只需要一个正确的 `cordis.patch.yml`。

---

## 1. 完整目录树（逐字）

```
./README.md
./cordis.patch.yml
./package.json
```

---

## 2. `package.json`（全文逐字）

```json
{
  "name": "dsh-ouroboros",
  "version": "0.1.0",
  "description": "Mount Ouroboros (spec-first AI dev workflow engine) into DeepSeek Harness as native tools — type \"ooo interview\" or \"ooo auto\" in chat.",
  "type": "module",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/Q00/ouroboros.git",
    "directory": "integrations/dsh-plugin"
  },
  "homepage": "https://github.com/Q00/ouroboros/tree/main/integrations/dsh-plugin",
  "keywords": [
    "dsh-plugin",
    "deepseek-harness",
    "ouroboros",
    "mcp"
  ],
  "files": [
    "cordis.patch.yml",
    "README.md"
  ],
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

**四个必抄点**：
1. `"type": "module"` —— 必须。
2. `files` **只列了 `cordis.patch.yml` 和 `README.md`** —— 零代码包就这么短。**关键：patch 文件必须在 `files` 里，否则发布后它不会进 npm 包**。
3. `dsh.bundle.patch` —— 少了它，`dsh plugin add` 会打那条 `declares no dsh.bundle` 警告，装完不生效。
4. **没有 `main` / `exports` / `dependencies`** —— 因为没有任何 JS 入口。这是零代码包和普通包在 `package.json` 上的显著差异。

---

## 3. `cordis.patch.yml`（全文逐字，**最重要的模板**）

```yaml
# dsh-ouroboros — mounts Ouroboros as native MCP tools inside DeepSeek Harness.
#
# Ouroboros (https://github.com/Q00/ouroboros) is a spec-first AI dev workflow
# engine: Socratic interview -> Seed spec -> execute -> evaluate -> evolve.
# This bundle inserts one @deepseek-ai/dsh-mcp-client row that spawns
# `ouroboros mcp serve` over stdio, so every dsh agent gets tools named
# mcp__ouroboros__ouroboros_interview, mcp__ouroboros__ouroboros_auto, and 33
# others. Typing "ooo interview <goal>" or "ooo auto <goal>" in chat is enough
# for the model to find and call the matching tool on its own — no extra
# prompting needed (each tool carries its own description).
#
# Requirements: Python >= 3.12 and `uv` (https://astral.sh/uv) on PATH. No
# separate `pip install` step — uvx fetches and runs Ouroboros in an isolated
# environment on first launch.
#
# Configuration (env vars, read by the spawned `ouroboros mcp serve` process):
#   OUROBOROS_LLM_BACKEND   — LLM backend for interview/seed/QA. Unset uses
#                             your existing `ouroboros setup` default. `dsh`
#                             routes those calls back through DeepSeek Harness,
#                             but it is NOT a one-variable switch: Ouroboros
#                             spawns its own `dsh-acp-demo` child and fails
#                             closed (`invalid_config`) unless
#                             OUROBOROS_DSH_CONFIG_PATH names an absolute
#                             trusted Cordis composition. See the bundle README.
#   OUROBOROS_AGENT_RUNTIME — agent runtime backend for ooo run/ooo auto's
#                             execution step. Defaults to `host`: dsh has no
#                             installable execution CLI of its own, so by
#                             default the dsh model itself does the work —
#                             `execute_task` publishes a dispatch and dsh
#                             spawns its own subagent to service it
#                             (orchestrator/host_dispatch.py). Set this to an
#                             executable runtime (claude-cli, codex,
#                             opencode, ...) to have that CLI do the work
#                             instead.
#   OUROBOROS_DSH_CONFIG_PATH / OUROBOROS_DSH_CLI_PATH
#                           — the two prerequisites of the `dsh` LLM backend
#                             above: the absolute composition file, and the
#                             `dsh-acp-demo` bin when it is not on PATH.
#
# Override any field from your own profile's cordis.patch.yml by id (see the
# "Package and install a plugin" tutorial) — e.g. to pin a specific Ouroboros
# version, add local MCP servers back, or tighten toolCallTimeoutMs.
- insert:
    - id: mcp-ouroboros
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: ouroboros
        transport: stdio
        command: uvx
        args:
          # ⚠️ 主包必须写精确版本。uvx 会在启动时去索引取包并执行，写浮动规格
          #    （省略版本 / latest）等于「每次启动跑的都是当时的线上最新版」——
          #    这份配置被审阅之后，实际执行的代码仍然会变。
          #    另外注意：**上游原文只固定了辅助依赖（mcp==2.0.0），没有固定主包**。
          #    照抄上游写法时，「把版本固定住」是必须自行补上的那一步。
          #    下面的 1.4.0 是占位，请换成你核对过的精确版本。
          - --from
          - 'ouroboros-ai[mcp]==1.4.0'
          - --with
          - 'mcp==2.0.0'
          - ouroboros
          - mcp
          - serve
        # The child does NOT inherit the harness environment wholesale:
        # @deepseek-ai/dsh-subprocess hands mcp-client a scrubbed parent env
        # with every credential-shaped name (/KEY|PASSWORD|SECRET|TOKEN/i) and
        # every DSH_* name removed, precisely so harness credentials never leak
        # into a spawned process implicitly. This explicit layer merges *after*
        # that scrub, so any credential Ouroboros genuinely needs has to be
        # named here. It is deliberately a short allowlist covering the two
        # documented backends — not a wildcard passthrough. To forward another
        # (OPENAI_API_KEY, OPENROUTER_API_KEY, GOOGLE_API_KEY, ...), override
        # this row in your own profile's cordis.patch.yml with that one extra
        # name — restating the whole `config`, since a later layer replaces a
        # row's config rather than deep-merging it. Non-credential names
        # (PATH, HOME, the OUROBOROS_* selectors) survive the scrub on their
        # own; the OUROBOROS_* rows below are here to keep the contract
        # visible in one place.
        #
        # `?? ''` keeps every value a string (the row's schema is a string
        # dict). Ouroboros treats a blank credential as unset, so an unset host
        # variable stays effectively unset in the child. OUROBOROS_AGENT_RUNTIME
        # is the one exception: it falls back to the literal `'host'` rather
        # than `''`, because dsh has no installable execution CLI to fall back
        # to on its own — see the comment above.
        # ⚠️ 这里每一行都会被上面那个「运行时下载下来的子进程」读到，且它以 DSH
        #    同等权限运行。只列真正需要的那把，优先用低配额、可撤销的专用 key。
        env:
          OUROBOROS_LLM_BACKEND: !!js process.env.OUROBOROS_LLM_BACKEND ?? ''
          OUROBOROS_AGENT_RUNTIME: !!js process.env.OUROBOROS_AGENT_RUNTIME || 'host'
          OUROBOROS_DSH_CONFIG_PATH: !!js process.env.OUROBOROS_DSH_CONFIG_PATH ?? ''
          OUROBOROS_DSH_CLI_PATH: !!js process.env.OUROBOROS_DSH_CLI_PATH ?? ''
          ANTHROPIC_API_KEY: !!js process.env.ANTHROPIC_API_KEY ?? ''
          DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY ?? ''
        # ouroboros_auto runs a full interview -> Seed -> execute -> grade
        # pipeline synchronously when called without polling; give it real
        # headroom instead of dsh's 60s mcp-client default.
        toolCallTimeoutMs: 1800000
        # Soft-fail: a machine without `uv`/Ouroboros configured yet should
        # still boot dsh with every other plugin working, not crash outright.
        # Recovery is not guaranteed to be automatic — whether mcp-client
        # retries at all depends on the dsh build (the published rc has no
        # reconnect loop), and where it exists the attempt budget is bounded.
        # After fixing the cause, reload the plugin or restart dsh.
        failOnStartupError: false
```

---

## 4. 从这个文件里能学到的 8 条硬知识（逐条对应原文）

| # | 知识 | 原文依据 |
|---|---|---|
| 1 | 补丁文件**只写注释 + 一个 `- insert:` 列表**，注释可以写得很长（它就是这个插件的"文档"） | 整个文件 |
| 2 | 插一行就能给模型加 35 个工具（靠 `@deepseek-ai/dsh-mcp-client`） | 文件头注释：`so every dsh agent gets tools named mcp__ouroboros__ouroboros_interview, mcp__ouroboros__ouroboros_auto, and 33 others` |
| 3 | **`!!js` 可以写在 `config:` 内部**（`env:` 里就用了），与官方复盘 0002 一致 | `env:` 段落 |
| 4 | 🔥 **子进程环境会被"清洗"**：`@deepseek-ai/dsh-subprocess` 会把**凭据形状的名字**（正则 `/KEY\|PASSWORD\|SECRET\|TOKEN/i`）**和所有 `DSH_*`** 从父环境里删掉。**你要传的凭据必须显式列在 `env:` 里** | 注释原文：`hands mcp-client a scrubbed parent env with every credential-shaped name (/KEY\|PASSWORD\|SECRET\|TOKEN/i) and every DSH_* name removed` |
| 5 | 🔥 **后面的层"替换"整段 `config`，不做深合并** —— 所以覆盖时必须**把整个 config 重述一遍** | 注释原文：`restating the whole config, since a later layer replaces a row's config rather than deep-merging it` |
| 6 | 用 `?? ''` 保持"值的类型是字符串"（该行的 schema 是 string dict），用 `\|\|` 提供真值回退 | 注释原文：`` `?? ''` keeps every value a string (the row's schema is a string dict) `` |
| 7 | 长任务要**显式加大超时**（默认 mcp-client 60s → 这里 1800000ms = 30 分钟） | 注释原文：`give it real headroom instead of dsh's 60s mcp-client default` |
| 8 | **加 `failOnStartupError: false` 实现"软失败"** —— 没装 uv 的机器也能正常启动 dsh，其它插件照常工作 | 注释原文：`a machine without uv/Ouroboros configured yet should still boot dsh with every other plugin working, not crash outright` |

> ⚠️ 第 8 条后半句也很重要：**软失败不是自动恢复**。原文：`Recovery is not guaranteed to be automatic — whether mcp-client retries at all depends on the dsh build (the published rc has no reconnect loop)`。

---

## 5. 可直接套用的最小零代码插件模板

```json
// package.json
{
  "name": "dsh-<你的插件名>",
  "version": "0.1.0",
  "description": "<一句话说明它给 dsh 加了什么>",
  "type": "module",
  "license": "MIT",
  "keywords": ["dsh-plugin", "deepseek-harness"],
  "files": ["cordis.patch.yml", "README.md"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

```yaml
# cordis.patch.yml
# <这里写清楚：这个插件做了什么、有什么前置要求、怎么配置>
- insert:
    - id: <行 id，全局唯一>
      name: '<要挂载的包名>'
      config:
        <该包要求的配置>
```

**装法**：
```bash
dsh plugin --profile web add ./你的插件目录     # 本地目录
dsh plugin --profile web add dsh-<你的插件名>   # 已发布到 npm
```

---

## 6. 这个范本的边界（诚实标注）

- 它**不能**给你加"自定义工具"（要写 `defineTool`），只能**挂载已存在的插件能力**（如 MCP 客户端）。想把外部能力变成 dsh 工具，有两条路：
  - **零代码**：对方已经有 MCP server → 用 `@deepseek-ai/dsh-mcp-client` 挂（本范本的路子）。
  - **写代码**：自己写 `defineTool`（见官方 `tool-ask-user` 模板）。
- 它的 `env` 里只放**名字**，不放**值** —— 值是运行时从宿主环境读的。**别把密钥硬编码进 `cordis.patch.yml`**（补丁文件会进 npm 包）。

---

