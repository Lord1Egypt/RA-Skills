---
name: ai-code-verification-guard
description: Deterministic code-verification guard for AI coding agents. Runs syntax, type, lint and test checks before and after code changes, and decides PASS / FAIL / REGRESSION / UNVERIFIED purely by script exit codes. The agent may only quote the verdict, never overrule it. Use when the user asks to modify code, implement features, fix bugs, or verify change reliability (trigger phrases - verify this, run the tests, regression check, confirm it works, 验证一下, 跑测试, 回归检查, 确认没问题). Not for general code review or security audits.
version: 1.0.1
license: MIT
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      env: []
      bins:
        - node
    primaryEnv: ""
    models: []
---

# AI Code Verification Guard (tool-decided verdict)

The arbiter is `scripts/verify.mjs`, shipped with this skill — `<skill-path>` below means this skill's install directory. The agent only invokes the script and quotes its verdict block verbatim; it has no authority to overrule the result.

Zero dependencies. Installs nothing. Reads the project, writes baselines only under `<project>/.verification/`.

## Hard rules

1. BEFORE changing code (any change touching logic, interfaces, or tests), run in the project root:

   ```
   node <skill-path>/scripts/verify.mjs snapshot
   ```

2. BEFORE reporting completion to the user, run in the project root:

   ```
   node <skill-path>/scripts/verify.mjs run
   ```

   and paste the emitted `VERIFY VERDICT` block verbatim in the reply.

## Disposal table (exit code decides; the agent has no discretion)

| RESULT | Exit code | Disposal |
|--------|-----------|----------|
| PASS | 0 | May report completion; must attach the VERDICT |
| PASS_WITH_UNVERIFIED | 0 | May report completion; must quote every unverified item |
| FAIL | 1 | Forbidden to report completion; fix and rerun until PASS |
| REGRESSION | 1 | A baseline-passing check broke; forbidden to report completion; fix and rerun |
| UNVERIFIED | 2 | Forbidden to report completion; quote the blocking reasons and let the user decide |

## What the script detects (content-first, not name-first)

- Node.js projects: `package.json` scripts classified by command content — lint, format-check, typecheck, composite check gates, tests. Build-ish scripts (`build`/`compile`/`generate`/`bench`) that emit files are never treated as type checks.
- Watch/modify traps neutralized: scripts containing `--watch`, `--fix`, `--write`, or bare `vitest` (which defaults to watch mode and hangs) are never executed as-is; bare-vitest test scripts are deterministically rewritten to a local `vitest.mjs run` invocation with the same semantics.
- Monorepo aware: declares guard scope (root-level checks only) for workspaces / pnpm-workspace / lerna.
- Go (`go build`/`go vet`/`go test`), Rust (`cargo check`/`cargo test`), Python (`compileall`/`pytest`) projects.
- Bare JS projects (no ecosystem markers): `node --check` syntax checks plus `node --test`.
- Regression detection: `run` compares every check against the `snapshot` baseline and flags any pass-to-fail flip as REGRESSION.
- Environment honesty: missing tools or unrecognizable project structure yield UNVERIFIED, never a fake pass.

## Boundaries

- If the script fails or the project structure is unrecognized, quote UNVERIFIED as-is; never pass off verbal inspection as verification.
- Baselines are written to `.verification/` in the project root; suggest the user add it to `.gitignore`.
- Docs-only, comment-only, or formatting-only changes may skip verification, but the skip reason must be stated to the user.
- Without a baseline, `run` still executes every check — just without regression comparison. Never retroactively fabricate a baseline.

---

# 代码验证守卫（工具裁决）

裁决者是随本 skill 分发的 `scripts/verify.mjs`——下文的 `<skill-path>` 指本 skill 的安装目录。模型只负责调用脚本并把 VERDICT 块原样转述给用户，无权改判。

零依赖，不安装任何包，仅在项目 `.verification/` 目录下写基线。

## 硬规则

1. 开始修改代码前（涉及逻辑、接口或测试的变更），在项目根目录执行：

   ```
   node <skill-path>/scripts/verify.mjs snapshot
   ```

2. 向用户报告完成之前，在项目根目录执行：

   ```
   node <skill-path>/scripts/verify.mjs run
   ```

   并把输出的 `VERIFY VERDICT` 块原样附在回复中。

## 结果处置（退出码决定，无裁量空间）

| RESULT | 退出码 | 处置 |
|--------|--------|------|
| PASS | 0 | 可报告完成，必须附 VERDICT |
| PASS_WITH_UNVERIFIED | 0 | 可报告完成，必须逐项转述 unverified 条目 |
| FAIL | 1 | 禁止报告完成，修复后重跑至 PASS |
| REGRESSION | 1 | 基线通过项被改坏，禁止报告完成，修复后重跑 |
| UNVERIFIED | 2 | 禁止报告完成，如实转述阻塞原因，交用户决策 |

## 脚本探测能力（以命令内容识别为主，不靠命名猜测）

- Node.js 项目：按命令内容分类 package.json 脚本——lint、format 检查、typecheck、复合 check 门禁、测试；build/compile/generate/bench 等会写盘的脚本绝不当作类型检查执行。
- watch/修改型陷阱防护：含 `--watch`、`--fix`、`--write` 的脚本绝不执行；裸 `vitest`（默认 watch 模式会挂死）被确定性改写为本地 `vitest.mjs run` 直调，语义不变仅关 watch。
- monorepo 感知：检测到 workspaces / pnpm-workspace / lerna 时声明守卫范围（仅根级检查）。
- Go（build/vet/test）、Rust（check/test）、Python（compileall/pytest）项目原生支持。
- 无生态标识的裸 JS 项目：`node --check` 语法检查 + `node --test`。
- 回归检测：`run` 将每项检查与 `snapshot` 基线对比，任何"基线通过 -> 现在失败"都判 REGRESSION。
- 环境诚实：工具缺失或项目结构不识别时输出 UNVERIFIED，绝不假装通过。

## 边界

- 脚本运行失败或项目结构不被识别时，转述 UNVERIFIED，禁止用口头检查冒充验证。
- 基线写入项目根目录 `.verification/`，建议用户将其加入 .gitignore。
- 纯文档、注释、格式化类变更可跳过验证，但需向用户说明跳过原因。
- 没有基线时 run 仍执行全部检查，只是没有回归对比；禁止为补基线而重跑历史。
