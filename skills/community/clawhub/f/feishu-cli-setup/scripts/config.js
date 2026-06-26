#!/usr/bin/env node
/**
 * feishu-cli-setup — config.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt to guide lark-cli app credential configuration.
 *
 * CRITICAL: lark-cli config init --new runs interactively and outputs a browser URL.
 * The agent must extract this URL and present it to the user.
 *
 * Usage:
 *   node scripts/config.js
 *   node scripts/config.js --lang en
 *   node scripts/config.js --existing   # user already has a Feishu app
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const existing = args.includes('--existing');

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Step 2: Configure App Credentials ===

This step creates a Feishu/Lark app and links its credentials to lark-cli.
${existing ? 'The user already has a Feishu app — skip app creation, enter credentials directly.' : 'This requires a browser step — extract the URL from CLI output and send it to the user.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT INSTRUCTIONS: Read carefully before running
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${existing ? `SCENARIO: User has an existing Feishu app

Run the standard config init (interactive mode):
  lark-cli config init

The CLI will prompt for:
  1. App ID     → user pastes their LARK_APP_ID
  2. App Secret → user pastes their LARK_APP_SECRET

Tell the user: "Please paste your Feishu App ID and App Secret.
You can find these at: https://open.feishu.cn/app → select your app → Credentials & Basic Info"

After entering credentials, the CLI saves them to the OS keychain.
` : `SCENARIO: New Feishu app creation (most users)

STEP 1 — Run config init in the background (non-blocking)
  Run this command and capture its output:
  lark-cli config init --new

  ⚠️ IMPORTANT: This command outputs a URL like:
    "Please open the following URL in your browser: https://open.feishu.cn/..."

  DO NOT wait for the command to complete before acting.
  Extract the URL immediately from the output.

STEP 2 — Send the URL to the user
  Tell the user:
  "Please open this URL in your browser to create a Feishu app:
   <extracted URL>

   The browser will guide you through creating an app on the Feishu Open Platform.
   This is a one-time setup. Come back and let me know when you've completed it."

STEP 3 — Wait for user confirmation
  Wait until the user says they've finished the browser setup.
  The CLI command will exit automatically once setup is complete.
  If it doesn't exit: run lark-cli config init (without --new) to enter credentials manually.
`}

STEP 4 — Verify configuration
  lark-cli config show 2>/dev/null || lark-cli auth status
  → Should show app ID (not empty)
  → If shows "no config": repeat Step 1-3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: No URL appears in output
  → Run without --new and enter App ID/Secret manually: lark-cli config init
  → Get credentials from: https://open.feishu.cn/app

Problem: URL expired (>10 minutes)
  → Re-run: lark-cli config init --new (generates a fresh URL)

Problem: "permission denied" or keychain error
  → macOS: grant terminal keychain access in System Preferences → Privacy & Security
  → Linux: install libsecret: apt install libsecret-1-0 or set LARK_CONFIG_FILE env var

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report:
  App configured: yes | no
  App ID visible: yes (first 8 chars: cli_xxxx...) | no
  Status: SUCCESS | FAILED | WAITING_FOR_USER

If SUCCESS: proceed to Step 3 — run: node scripts/auth.js
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 第 2 步：配置应用凭证 ===

本步骤创建飞书应用并将凭证与 lark-cli 关联。
${existing ? '用户已有飞书应用 — 跳过应用创建，直接输入凭证。' : '此步骤需要浏览器操作 — 从 CLI 输出中提取 URL 并发送给用户。'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent 操作说明：执行前请仔细阅读
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${existing ? `情景：用户已有飞书应用

运行标准配置初始化（交互模式）：
  lark-cli config init

CLI 会依次提示输入：
  1. App ID     → 用户粘贴 LARK_APP_ID
  2. App Secret → 用户粘贴 LARK_APP_SECRET

告知用户："请将您的飞书 App ID 和 App Secret 粘贴进来。
可在此处找到：https://open.feishu.cn/app → 选择您的应用 → 凭证与基础信息"

输入凭证后，CLI 将其保存到系统钥匙串。
` : `情景：新建飞书应用（大多数用户）

步骤 1 — 在后台运行 config init（非阻塞）
  运行此命令并捕获其输出：
  lark-cli config init --new

  ⚠️ 重要：此命令会输出类似以下内容的 URL：
    "Please open the following URL in your browser: https://open.feishu.cn/..."

  不要等命令执行完再操作。
  立即从输出中提取该 URL。

步骤 2 — 将 URL 发送给用户
  告知用户：
  "请在浏览器中打开这个链接来创建飞书应用：
   <提取的 URL>

   浏览器会引导您在飞书开放平台上创建应用。
   这是一次性设置。完成后告诉我，我们继续下一步。"

步骤 3 — 等待用户确认
  等待用户说已完成浏览器操作。
  用户完成后，CLI 命令会自动退出。
  如未自动退出：运行 lark-cli config init（不带 --new）手动输入凭证。
`}

步骤 4 — 验证配置
  lark-cli config show 2>/dev/null || lark-cli auth status
  → 应显示 App ID（非空）
  → 如显示 "no config"：重复步骤 1-3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
故障排查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

问题：输出中没有 URL
  → 不带 --new 运行，手动输入 App ID/Secret：lark-cli config init
  → 凭证获取地址：https://open.feishu.cn/app

问题：URL 已过期（>10 分钟）
  → 重新运行：lark-cli config init --new（生成新 URL）

问题："permission denied" 或钥匙串错误
  → macOS：在系统偏好设置 → 隐私与安全 中允许终端访问钥匙串
  → Linux：安装 libsecret：apt install libsecret-1-0，或设置 LARK_CONFIG_FILE 环境变量

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
结果报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

报告：
  应用已配置：是 | 否
  App ID 可见：是（前 8 位：cli_xxxx...）| 否
  状态：SUCCESS | FAILED | WAITING_FOR_USER

如果 SUCCESS：进入第 3 步 — 运行：node scripts/auth.js
`);
}
