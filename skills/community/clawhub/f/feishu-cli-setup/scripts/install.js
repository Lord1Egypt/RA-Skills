#!/usr/bin/env node
/**
 * feishu-cli-setup — install.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt to install lark-cli via npm and load Agent Skills.
 *
 * Usage:
 *   node scripts/install.js
 *   node scripts/install.js --lang en
 *   node scripts/install.js --source npm     # default
 *   node scripts/install.js --source source  # build from source (requires Go 1.23+)
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const srcIdx = args.indexOf('--source');
const source = srcIdx !== -1 ? args[srcIdx + 1] : 'npm';

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Step 1: Install ===
Install method: ${source === 'source' ? 'Build from source (requires Go 1.23+ and Python 3)' : 'npm (recommended)'}

Install lark-cli and load the 20 built-in Agent Skills.
Follow all steps in order. Report the output of each command.

── INSTALL STEPS ────────────────────────────────────────────
${source === 'source' ? `
METHOD: Build from Source
Requires: Go v1.23+, Python 3, git

STEP 1 — Clone and build
  git clone https://github.com/larksuite/cli.git
  cd cli
  make install
  → On success: lark-cli --version should print a version number
  → Common errors:
    - "go: command not found" → Install Go from https://go.dev/dl/ (v1.23+)
    - "make: command not found" → Install build tools (brew install make / apt install make)
` : `
METHOD: npm (Recommended)

STEP 1 — Install the CLI globally
  npm install -g @larksuite/cli
  → Installs lark-cli to your global npm prefix
  → Verify: lark-cli --version
  → Expected: v1.0.4 (or latest)
  → Common errors:
    - "EACCES: permission denied" → Run: sudo npm install -g @larksuite/cli
      Or fix npm permissions: https://docs.npmjs.com/resolving-eacces-permissions-errors
    - "npm: command not found" → Install Node.js first: https://nodejs.org
    - China mirror (slow npm): npm install -g @larksuite/cli --registry https://registry.npmmirror.com
`}
STEP 2 — Load Agent Skills (required — do not skip)
  npx skills add larksuite/cli -y -g
  → This installs 20 pre-built Agent Skills (lark-calendar, lark-im, lark-doc, etc.)
  → The -g flag installs globally so all agents can use them
  → Verify: npx skills list | grep lark
  → Expected: see lark-shared, lark-calendar, lark-im, lark-doc, and more

STEP 3 — Confirm installation
  lark-cli --version
  lark-cli --help | head -20
  → Both commands must succeed with exit code 0

── RESULT REPORT ────────────────────────────────────────────

Report back:
  lark-cli version:  <v1.0.4>
  Skills loaded:     <yes / no>
  Install method:    <npm / source>
  Status:            SUCCESS | FAILED

If FAILED: describe the exact error message and which step failed.
If SUCCESS: proceed to Step 2 — run: node scripts/config.js
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 第 1 步：安装 ===
安装方式：${source === 'source' ? '从源码构建（需要 Go 1.23+ 和 Python 3）' : 'npm 安装（推荐）'}

安装 lark-cli 并加载 20 个内置 Agent Skills。
按顺序执行所有步骤，并报告每个命令的输出结果。

── 安装步骤 ──────────────────────────────────────────────────
${source === 'source' ? `
方式：从源码构建
前提：Go v1.23+，Python 3，git

步骤 1 — 克隆并构建
  git clone https://github.com/larksuite/cli.git
  cd cli
  make install
  → 成功后：lark-cli --version 应打印版本号
  → 常见错误：
    - "go: command not found" → 从 https://go.dev/dl/ 安装 Go（v1.23+）
    - "make: command not found" → 安装构建工具（brew install make / apt install make）
` : `
方式：npm 安装（推荐）

步骤 1 — 全局安装 CLI
  npm install -g @larksuite/cli
  → 将 lark-cli 安装到全局 npm 前缀目录
  → 验证：lark-cli --version
  → 预期：v1.0.4（或最新版本）
  → 常见错误：
    - "EACCES: permission denied" → 运行：sudo npm install -g @larksuite/cli
    - "npm: command not found" → 先安装 Node.js：https://nodejs.org
    - 国内镜像加速：npm install -g @larksuite/cli --registry https://registry.npmmirror.com
`}
步骤 2 — 加载 Agent Skills（必须执行，不可跳过）
  npx skills add larksuite/cli -y -g
  → 安装 20 个预置 Agent Skills（lark-calendar、lark-im、lark-doc 等）
  → -g 标志全局安装，所有 agent 均可使用
  → 验证：npx skills list | grep lark
  → 预期：看到 lark-shared、lark-calendar、lark-im、lark-doc 等

步骤 3 — 确认安装成功
  lark-cli --version
  lark-cli --help | head -20
  → 两个命令均须以退出码 0 成功

── 结果报告 ──────────────────────────────────────────────────

报告以下内容：
  lark-cli 版本：  <v1.0.4>
  Skills 已加载：  <是 / 否>
  安装方式：       <npm / 源码>
  状态：           SUCCESS | FAILED

如果 FAILED：描述具体报错信息和失败的步骤。
如果 SUCCESS：进入第 2 步 — 运行：node scripts/config.js
`);
}
