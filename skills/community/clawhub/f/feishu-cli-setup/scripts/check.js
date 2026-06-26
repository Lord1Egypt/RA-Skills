#!/usr/bin/env node
/**
 * feishu-cli-setup — check.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt to detect OS, Node.js version, and lark-cli install state.
 *
 * Usage:
 *   node scripts/check.js
 *   node scripts/check.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Step 0: Environment Check ===

Before installing lark-cli, check the user's environment and report findings.
Run each command and report the result clearly.

── DETECTION STEPS ──────────────────────────────────────────

CHECK 1 — Operating System
  uname -s 2>/dev/null || systeminfo | findstr "OS Name"
  → Report: macOS / Linux / Windows

CHECK 2 — Node.js & npm version
  node --version
  npm --version
  → Required: Node.js ≥ 18 and npm installed
  → If missing: tell user to install from https://nodejs.org

CHECK 3 — lark-cli install state
  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  → If shows a version (e.g., v1.0.4): already installed — skip to check.js step 3
  → If NOT_INSTALLED: proceed to install.js

CHECK 4 — lark-cli auth status (only if installed)
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"
  → If shows user info: already authenticated — skip to verify.js
  → If NOT_AUTHENTICATED: proceed to config.js then auth.js

── REPORT FORMAT ────────────────────────────────────────────

After running all checks, summarize:

Environment Report:
  OS:            <macOS 14.x / Ubuntu 22.04 / Windows 11>
  Node.js:       <v20.x.x> ✓ | ✗ (need ≥ v18)
  npm:           <10.x.x> ✓ | ✗
  lark-cli:      <v1.0.4 installed> | NOT INSTALLED
  auth status:   <logged in as user@example.com> | NOT AUTHENTICATED

Next step recommendation:
  → If Node.js missing: Install Node.js first from https://nodejs.org, then re-run.
  → If lark-cli missing: Proceed to install — run: node scripts/install.js
  → If lark-cli installed but not authenticated: run: node scripts/config.js
  → If fully authenticated: run: node scripts/verify.js
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 第 0 步：环境检测 ===

安装 lark-cli 之前，先检测用户的环境并报告结果。
逐一运行以下命令并清晰报告结果。

── 检测步骤 ──────────────────────────────────────────────────

检查 1 — 操作系统
  uname -s 2>/dev/null || systeminfo | findstr "OS Name"
  → 报告：macOS / Linux / Windows

检查 2 — Node.js 和 npm 版本
  node --version
  npm --version
  → 需要：Node.js ≥ 18，且已安装 npm
  → 如果缺失：告知用户前往 https://nodejs.org 安装

检查 3 — lark-cli 安装状态
  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  → 如显示版本（如 v1.0.4）：已安装 — 跳至检查 4
  → 如显示 NOT_INSTALLED：需要安装 — 继续运行 install.js

检查 4 — lark-cli 认证状态（仅在已安装时运行）
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"
  → 如显示用户信息：已认证 — 可直接运行 verify.js
  → 如显示 NOT_AUTHENTICATED：需要配置和登录 — 继续运行 config.js

── 报告格式 ──────────────────────────────────────────────────

完成所有检查后，输出汇总：

环境检测报告：
  操作系统：      <macOS 14.x / Ubuntu 22.04 / Windows 11>
  Node.js：       <v20.x.x> ✓ | ✗（需要 ≥ v18）
  npm：           <10.x.x> ✓ | ✗
  lark-cli：      <v1.0.4 已安装> | 未安装
  认证状态：      <已登录 user@example.com> | 未认证

下一步建议：
  → Node.js 缺失：先去 https://nodejs.org 安装 Node.js，完成后重新运行本检测
  → lark-cli 未安装：继续安装 — 运行：node scripts/install.js
  → 已安装但未认证：运行：node scripts/config.js
  → 已完整认证：运行：node scripts/verify.js
`);
}
