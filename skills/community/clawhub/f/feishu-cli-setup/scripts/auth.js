#!/usr/bin/env node
/**
 * feishu-cli-setup — auth.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt to guide OAuth login via lark-cli auth login.
 *
 * CRITICAL: lark-cli auth login outputs a browser URL that the agent must
 * extract and send to the user. The user completes OAuth in the browser.
 *
 * Usage:
 *   node scripts/auth.js
 *   node scripts/auth.js --lang en
 *   node scripts/auth.js --domain calendar,im,docs   # specific domains only
 *   node scripts/auth.js --mode full                 # all scopes (default: recommend)
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const domainIdx = args.indexOf('--domain');
const domain = domainIdx !== -1 ? args[domainIdx + 1] : null;
const modeIdx = args.indexOf('--mode');
const mode = modeIdx !== -1 ? args[modeIdx + 1] : 'recommend';

const loginCmd = domain
  ? `lark-cli auth login --domain ${domain} --no-wait`
  : mode === 'full'
    ? `lark-cli auth login --no-wait`
    : `lark-cli auth login --recommend --no-wait`;

const loginCmdNote = domain
  ? `Domain-specific login: ${domain}`
  : mode === 'full'
    ? 'Full scope login (all domains)'
    : 'Recommended scopes (most common domains — calendar, im, docs, tasks, mail)';

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Step 3: OAuth Login ===
Mode: ${loginCmdNote}

Log in to Feishu/Lark via OAuth. This step requires a browser action from the user.
The CLI outputs an authorization URL — extract it and send it to the user immediately.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT INSTRUCTIONS: Read carefully before running
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — Run auth login (non-blocking, with --no-wait)
  Run in the background:
  ${loginCmd}

  The command immediately outputs something like:
    "Please open the following URL to authorize:
     https://accounts.feishu.cn/suite/passport/oauth/authorize?..."

  ⚠️ The --no-wait flag makes the command return immediately with the URL.
  ⚠️ Extract the full URL from the output right away.

STEP 2 — Send the authorization URL to the user
  Tell the user:
  "Please open this link in your browser to authorize lark-cli:
   <extracted authorization URL>

   This will ask you to log in to Feishu and grant permissions to the app.
   Click 'Authorize' when prompted. Come back and tell me when you're done."

STEP 3 — Resume polling after user completes authorization
  Once the user says they've authorized in the browser, run:
  lark-cli auth login --device-code <DEVICE_CODE>
  (The device code appears in the original command output alongside the URL)

  OR: just run lark-cli auth status to check if login succeeded automatically.

STEP 4 — Verify login
  lark-cli auth status
  → Must show: logged in as <user email or name>
  → Must show: granted scopes list
  → If still "not authenticated": ask user to confirm they clicked Authorize in the browser

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCOPE MODES (for reference)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

--recommend     Grants commonly-used scopes: calendar, im, docs, tasks, contacts, mail
--domain X,Y    Only grants scopes for specific domains
(no flag)       Interactive TUI — user selects scopes manually
--scope "X"     Exact scope string

Tip for agents: Start with --recommend for most users. They can add more scopes later with:
  lark-cli auth login --domain <new-domain>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: Authorization URL expired
  → Re-run: ${loginCmd}

Problem: "app not configured" error
  → Run config step first: node scripts/config.js

Problem: Login shows success but auth status fails
  → Try: lark-cli auth logout && ${loginCmd}

Problem: Scope not granted after authorization
  → Check: lark-cli auth scopes (lists all available scopes for this app)
  → Re-login with specific scope: lark-cli auth login --scope "calendar:calendar"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report:
  Logged in as:   <user display name or email>
  Granted scopes: <count> (e.g., "12 scopes")
  Domains active: <calendar, im, docs, ...>
  Status:         SUCCESS | FAILED | WAITING_FOR_USER

If SUCCESS: proceed to Step 4 — run: node scripts/verify.js
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 第 3 步：OAuth 登录 ===
模式：${loginCmdNote}

通过 OAuth 登录飞书/Lark。本步骤需要用户在浏览器中操作。
CLI 会输出授权 URL — 立即提取并发送给用户。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent 操作说明：执行前请仔细阅读
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤 1 — 运行 auth login（非阻塞，使用 --no-wait）
  在后台运行：
  ${loginCmd}

  命令会立即输出类似以下内容：
    "Please open the following URL to authorize:
     https://accounts.feishu.cn/suite/passport/oauth/authorize?..."

  ⚠️ --no-wait 标志让命令立即返回 URL。
  ⚠️ 立即从输出中提取完整 URL。

步骤 2 — 将授权 URL 发送给用户
  告知用户：
  "请在浏览器中打开以下链接来授权 lark-cli：
   <提取的授权 URL>

   这将要求您登录飞书并授权应用权限。
   出现提示时点击"授权"。完成后告诉我。"

步骤 3 — 用户授权后恢复轮询
  用户表示已在浏览器中授权后，运行：
  lark-cli auth login --device-code <DEVICE_CODE>
  （device code 出现在原始命令输出中，与 URL 一起显示）

  或者：直接运行 lark-cli auth status 检查是否已自动登录成功。

步骤 4 — 验证登录
  lark-cli auth status
  → 必须显示：已登录为 <用户邮箱或姓名>
  → 必须显示：已授权的 scope 列表
  → 如仍显示"未认证"：询问用户是否确认在浏览器中点击了"授权"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scope 模式说明（参考）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

--recommend     授权常用 scope：日历、消息、文档、任务、通讯录、邮件
--domain X,Y    仅授权指定域的 scope
（无标志）      交互式 TUI — 用户手动选择 scope
--scope "X"     指定精确的 scope 字符串

Agent 提示：大多数用户建议使用 --recommend。之后可通过以下命令添加更多 scope：
  lark-cli auth login --domain <新域>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
故障排查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

问题：授权 URL 已过期
  → 重新运行：${loginCmd}

问题："app not configured" 错误
  → 先完成配置步骤：node scripts/config.js

问题：登录显示成功但 auth status 失败
  → 尝试：lark-cli auth logout && ${loginCmd}

问题：授权后 scope 未生效
  → 检查：lark-cli auth scopes（列出该应用所有可用 scope）
  → 用指定 scope 重新登录：lark-cli auth login --scope "calendar:calendar"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
结果报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

报告：
  已登录为：      <用户姓名或邮箱>
  已授权 scope：  <数量>（如"12 个 scope"）
  激活的域：      <calendar, im, docs, ...>
  状态：          SUCCESS | FAILED | WAITING_FOR_USER

如果 SUCCESS：进入第 4 步 — 运行：node scripts/verify.js
`);
}
