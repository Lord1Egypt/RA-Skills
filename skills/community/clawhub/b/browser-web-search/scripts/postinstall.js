#!/usr/bin/env node

/**
 * browser-web-search-skill postinstall / help script
 * 显示安装后的使用说明
 */

const SKILL_VERSION = '0.4.10';
const REQUIRED_VERSION = '0.4.3';

console.log(`
╔══════════════════════════════════════════════════════════════════╗
║   Browser Web Search Skill v${SKILL_VERSION} 安装完成                     ║
║   (pinned npm pkg: browser-web-search@${REQUIRED_VERSION})                ║
╚══════════════════════════════════════════════════════════════════╝

把任何网站变成命令行 API，专为 OpenClaw 设计，复用浏览器登录态。

📦 内置平台 (55 平台，91+ 命令):
   知乎、小红书、B站、今日头条、36kr、澎湃、腾讯、网易、
   新浪、微博、微信公众号、百度、Bing、Google、CSDN、博客园、BOSS直聘 等

📥 安装 (必须精确版本 + 跳过包脚本):
   npm install -g browser-web-search@${REQUIRED_VERSION} --ignore-scripts

🚀 快速开始 (公共 adapter，无需任何 env):

   # 查看所有可用命令
   bws-skill list

   # 运行公共 adapter
   bws-skill run hn/search "llm" --count 5
   bws-skill run github/search "ai agent" --sort stars

   # JSON 输出 + jq 过滤
   bws-skill run hn/search "llm" --jq '.[].title'

🔐 敏感 adapter 四层闸门 (v0.4.10):

   Gate 1: BWS_PUBLIC_ONLY=1            → 硬隔离，拒绝所有 sensitive
   Gate 2: BWS_ENABLE_SENSITIVE_TIER=1  → v0.4.4+ 默认封印
   Gate 3: BWS_ALLOW_SENSITIVE=1        → 会话/调用级 opt-in
           (或 --i-understand-sensitive)
   Gate 4: --accept-platform-consent    → v0.4.10+ 首次访问该平台时
                                          记录到 ~/.bws/consents.json
                                          (绑定 pkgVersion + entrySha512)

   最小命令组合:
     export BWS_ENABLE_SENSITIVE_TIER=1
     export BWS_ALLOW_SENSITIVE=1
     bws-skill run weixin/search "ai" --accept-platform-consent

🧪 --dry-run (v0.4.10):
   跑完所有闸门、完整性校验和 audit/transparency 输出，但不 import 第三方包：
     BWS_ENABLE_SENSITIVE_TIER=1 BWS_ALLOW_SENSITIVE=1 \\
       bws-skill run weixin/search "ai" --accept-platform-consent --dry-run

⚠️  前提条件:
   - Node.js >= 18.0.0
   - OpenClaw 环境（openclaw 命令可用）
   - 如需登录态，请先在 OpenClaw 浏览器中登录目标网站

📖 详细文档:
   - SKILL.md      闸门、SOP、敏感 adapter 列表
   - SECURITY.md   v0.4.10 残留风险硬化与 ClawScan May 2026 verdict 映射

⚡ 安全提示:
   browser-web-search 会在浏览器页面上下文中执行 JavaScript，可访问站点认证数据。
   使用前请审计源码 (锁定到固定版本):
     https://github.com/sipingme/browser-web-search/blob/v${REQUIRED_VERSION}/src/index.ts

🔐 完整性校验 (无 env 旁路):
   Launcher 在 import 前会强制校验:
     - package.json.name == 'browser-web-search'
     - package.json.version == '${REQUIRED_VERSION}'
     - dist/index.js 大小 == 22871
     - dist/index.js SHA-512 == sha512-qoGLsU...3Q== (内置, timing-safe)

   本地复算:
     P=$(npm root -g)/browser-web-search/dist/index.js
     shasum -a 512 "$P" | awk '{print $1}' | xxd -r -p | base64

🪪 透明性 (v0.4.10):
   每次 sensitive 调用前，launcher 都会向 stderr 输出一行:
     [bws] transparency:{"adapter":"...","pkg":"browser-web-search@${REQUIRED_VERSION}","pkgEntrySha512":"...","gate":"...","auditLog":"~/.bws/audit.log",...}
   这行无法被被包装层抑制，便于审计/Agent 监控。

📝 升级到下一个 npm 包版本时:
   1) 在 sipingme/browser-web-search 仓库审计 diff
   2) 同步更新 scripts/run.js 中的 REQUIRED_VERSION / ENTRY_SHA512_BASE64 /
      ENTRY_EXPECTED_SIZE 三个常量
   3) 同步更新 config.json 中所有 0.4.3 / sha512 / size 字段
   4) bump SKILL_VERSION (本 launcher) 和文档；提交并 review
   5) 用户首次访问已同意过的 sensitive 站点时会自动失效 ~/.bws/consents.json
      中相关记录 (Gate 4 by-design)，需要重新加 --accept-platform-consent
`);
