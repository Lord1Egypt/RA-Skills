#!/usr/bin/env node
/**
 * feishu-cli-setup — setup.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Full guided pipeline: outputs a complete agent prompt covering all 4 steps
 * of lark-cli installation (check → install → config → auth → verify).
 *
 * The agent reads this prompt and executes each step in sequence, handling
 * the browser OAuth flow by extracting URLs and sending them to the user.
 *
 * Usage:
 *   node scripts/setup.js
 *   node scripts/setup.js --lang en
 *   node scripts/setup.js --resume config   # start from a specific step
 *   node scripts/setup.js --existing-app    # user already has a Feishu app
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const resumeIdx = args.indexOf('--resume');
const resume = resumeIdx !== -1 ? args[resumeIdx + 1] : null;
const existingApp = args.includes('--existing-app');

const steps = ['check', 'install', 'config', 'auth', 'verify'];
const startStep = resume ? steps.indexOf(resume) : 0;
const activeSteps = steps.slice(Math.max(0, startStep));

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Full Guided Installation ===
Source: https://github.com/larksuite/cli
Version: lark-cli v1.0.4 (latest)
${resume ? `Resuming from: Step ${startStep + 1} (${resume})` : 'Starting from: Step 1 (environment check)'}
${existingApp ? 'App mode: existing Feishu app (skip new app creation)' : 'App mode: create new Feishu app'}

You are an AI agent (Claude / Manus / OpenClaw) helping a user install lark-cli.
Follow all steps in order. Do not skip steps. Pause at browser steps and wait for user confirmation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEFORE YOU START — AGENT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Run commands one at a time and report results before proceeding.
2. When a command outputs a URL (auth or config), extract it and send it to the user immediately.
3. Wait for user confirmation after any browser step before continuing.
4. Use --dry-run for any command that modifies data.
5. If a step fails, diagnose the error before retrying.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${activeSteps.includes('check') ? `STEP 1 — Environment Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run these checks and report results:

  node --version        # Must be ≥ v18
  npm --version         # Must be installed
  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

Decision tree:
  → Node.js missing: stop and tell user to install from https://nodejs.org
  → lark-cli missing: proceed to Step 2
  → lark-cli installed but not authenticated: skip to Step 3
  → lark-cli installed and authenticated: skip to Step 5

` : ''}${activeSteps.includes('install') ? `STEP 2 — Install lark-cli
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Install the CLI (try without sudo first)
  npm install -g @larksuite/cli

  # If permission error: sudo npm install -g @larksuite/cli
  # China mirror: npm install -g @larksuite/cli --registry https://registry.npmmirror.com

  # Verify installation
  lark-cli --version   # Expected: v1.0.4

  # Load 20 Agent Skills (required)
  npx skills add larksuite/cli -y -g

  # Verify skills loaded
  npx skills list | grep lark

Only proceed to Step 3 when lark-cli --version succeeds.

` : ''}${activeSteps.includes('config') ? `STEP 3 — Configure App Credentials  ⚠️ BROWSER STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${existingApp ? `User has an existing Feishu app.
Run: lark-cli config init
→ Enter App ID and App Secret when prompted.
→ Tell user: "Find your credentials at https://open.feishu.cn/app → your app → Credentials & Basic Info"
` : `Run in background and capture output:
  lark-cli config init --new

⚠️ EXTRACT THE URL from the output immediately. It looks like:
  "Please open the following URL in your browser: https://open.feishu.cn/..."

Send this message to the user:
  "Please open this URL in your browser to create your Feishu app:
   [paste URL here]
   Complete the guided setup in the browser, then let me know when done."

Wait for user confirmation before proceeding.
`}
Verify: lark-cli auth status (should show an app ID)

` : ''}${activeSteps.includes('auth') ? `STEP 4 — OAuth Login  ⚠️ BROWSER STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run in background and capture output:
  lark-cli auth login --recommend --no-wait

⚠️ EXTRACT THE AUTHORIZATION URL from the output immediately. It looks like:
  "Please open the following URL to authorize: https://accounts.feishu.cn/..."

Send this message to the user:
  "Please open this URL to authorize lark-cli:
   [paste URL here]
   Log in to Feishu and click Authorize. Come back and tell me when done."

After user confirms:
  lark-cli auth status   # Must show: logged in as <user>

If still not authenticated, run:
  lark-cli auth login --device-code <DEVICE_CODE from earlier output>

` : ''}${activeSteps.includes('verify') ? `STEP 5 — Verify & Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli --version
  lark-cli auth status
  lark-cli calendar +agenda   # Quick smoke test

If all succeed, congratulate the user and show this summary:

  ✅ lark-cli is ready!
  • Logged in as: <user>
  • 20 Agent Skills available: lark-calendar, lark-im, lark-doc, lark-base, lark-task, lark-mail, and more

  First commands to try:
    lark-cli calendar +agenda              # today's schedule
    lark-cli task +list                    # your tasks
    lark-cli im +messages-send --chat-id oc_xxx --text "Hello" --dry-run

  Run: node scripts/learn.js for a full first-steps guide.

` : ''}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK REFERENCE (save for later)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status          # check login status
  lark-cli auth login --domain calendar,im   # add more scopes
  lark-cli auth logout          # sign out
  lark-cli <service> --help     # discover commands for any service
  lark-cli schema               # browse all API schemas
  node scripts/learn.js         # first-steps guide
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 完整引导安装 ===
来源：https://github.com/larksuite/cli
版本：lark-cli v1.0.4（最新）
${resume ? `从第 ${startStep + 1} 步（${resume}）继续` : '从第 1 步（环境检测）开始'}
${existingApp ? '应用模式：已有飞书应用（跳过新建应用）' : '应用模式：新建飞书应用'}

你是一个 AI Agent（Claude / Manus / OpenClaw），正在帮助用户安装 lark-cli。
按顺序执行所有步骤，不要跳步。遇到浏览器步骤时暂停并等待用户确认。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
开始前 — Agent 行为规则
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 每次运行一条命令，报告结果后再继续。
2. 命令输出 URL（auth 或 config）时，立即提取并发送给用户。
3. 任何浏览器步骤后，等待用户确认后再继续。
4. 对修改数据的命令，使用 --dry-run 预览。
5. 步骤失败时，先诊断错误再重试。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${activeSteps.includes('check') ? `第 1 步 — 环境检测
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

运行以下检查并报告结果：

  node --version        # 必须 ≥ v18
  npm --version         # 必须已安装
  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

决策树：
  → Node.js 缺失：停止，告知用户去 https://nodejs.org 安装
  → lark-cli 未安装：进入第 2 步
  → 已安装但未认证：跳至第 3 步
  → 已安装且已认证：跳至第 5 步

` : ''}${activeSteps.includes('install') ? `第 2 步 — 安装 lark-cli
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 安装 CLI（先不用 sudo 尝试）
  npm install -g @larksuite/cli

  # 如遇权限错误：sudo npm install -g @larksuite/cli
  # 国内镜像加速：npm install -g @larksuite/cli --registry https://registry.npmmirror.com

  # 验证安装
  lark-cli --version   # 预期：v1.0.4

  # 加载 20 个 Agent Skills（必须执行）
  npx skills add larksuite/cli -y -g

  # 验证 Skills 已加载
  npx skills list | grep lark

lark-cli --version 成功后才进入第 3 步。

` : ''}${activeSteps.includes('config') ? `第 3 步 — 配置应用凭证  ⚠️ 浏览器步骤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${existingApp ? `用户已有飞书应用。
运行：lark-cli config init
→ 按提示输入 App ID 和 App Secret。
→ 告知用户："凭证获取地址：https://open.feishu.cn/app → 选择您的应用 → 凭证与基础信息"
` : `在后台运行并捕获输出：
  lark-cli config init --new

⚠️ 立即从输出中提取 URL，格式类似：
  "Please open the following URL in your browser: https://open.feishu.cn/..."

向用户发送此消息：
  "请在浏览器中打开这个链接，创建您的飞书应用：
   [粘贴 URL]
   在浏览器中完成引导设置后，回来告诉我。"

等待用户确认后再继续。
`}
验证：lark-cli auth status（应显示 App ID）

` : ''}${activeSteps.includes('auth') ? `第 4 步 — OAuth 登录  ⚠️ 浏览器步骤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

在后台运行并捕获输出：
  lark-cli auth login --recommend --no-wait

⚠️ 立即从输出中提取授权 URL，格式类似：
  "Please open the following URL to authorize: https://accounts.feishu.cn/..."

向用户发送此消息：
  "请在浏览器中打开这个链接来授权 lark-cli：
   [粘贴 URL]
   登录飞书后点击"授权"。完成后告诉我。"

用户确认后：
  lark-cli auth status   # 必须显示：已登录为 <用户>

如仍未认证，运行：
  lark-cli auth login --device-code <上面输出中的 DEVICE_CODE>

` : ''}${activeSteps.includes('verify') ? `第 5 步 — 验证与总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli --version
  lark-cli auth status
  lark-cli calendar +agenda   # 快速冒烟测试

全部成功后，向用户发送安装完成摘要：

  ✅ lark-cli 已准备就绪！
  • 已登录为：<用户>
  • 20 个 Agent Skills 可用：lark-calendar, lark-im, lark-doc, lark-base, lark-task, lark-mail 等

  推荐先试的命令：
    lark-cli calendar +agenda              # 今日日程
    lark-cli task +list                    # 我的任务
    lark-cli im +messages-send --chat-id oc_xxx --text "你好" --dry-run

  运行：node scripts/learn.js 查看完整上手指南。

` : ''}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
快速参考（保存备用）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status          # 检查登录状态
  lark-cli auth login --domain calendar,im   # 添加更多 scope
  lark-cli auth logout          # 退出登录
  lark-cli <service> --help     # 发现任意服务的命令
  lark-cli schema               # 浏览所有 API Schema
  node scripts/learn.js         # 上手第一步指南
`);
}
