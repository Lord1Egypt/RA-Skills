#!/usr/bin/env node
/**
 * Automatic Skill — Credential Safety Reference
 * PROMPT GENERATOR ONLY — this script makes NO outbound network requests.
 *
 * Outputs a reference guide for writing credential-safe skill scripts.
 * This is documentation, not an auto-fix tool. It does not modify files,
 * does not re-publish, and does not loop until any external checker passes.
 *
 * Usage:
 *   node scripts/scan-fix.js
 *   node scripts/scan-fix.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== Credential Safety Reference for Skill Scripts ===

RULE 1 — Never print token values
  Bad : console.log(process.env.GITHUB_TOKEN)
  Bad : echo $GITHUB_TOKEN
  Good: gh auth status          (exit 0 = authenticated)
  Good: clawhub whoami          (returns username, not token)

RULE 2 — Never hardcode credentials
  Bad : const token = "ghp_abc123..."
  Good: const token = process.env.GITHUB_TOKEN

RULE 3 — Wrap env reads in named helper functions
  Bad : const repo = process.env.GITHUB_REPO  // top-level
  Good: function loadConfig() { return { repo: process.env.GITHUB_REPO } }

RULE 4 — Use CLI tools for authenticated operations, not raw curl
  Bad : curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/...
  Good: gh api repos/owner/repo/commits/main

RULE 5 — Never decode or preview credential bytes
  Bad : echo $TOKEN | base64 -d
  Bad : echo $TOKEN | head -c 20
  Good: gh auth status --show-token   // DO NOT USE --show-token
  Good: gh auth status                // correct: shows login status only

RULE 6 — Declare all env vars in SKILL.md requirements.env
  Every env var read by any script must be listed with:
    name, required (true/false), description

These rules are enforced by Stage 7.5 (scan-check.js) before upload.
`);
} else {
  console.log(`=== Skill 脚本凭证安全规范 ===

规则 1 — 禁止打印 token 值
  错误：console.log(process.env.GITHUB_TOKEN)
  错误：echo $GITHUB_TOKEN
  正确：gh auth status          (exit 0 = 已认证)
  正确：clawhub whoami          (返回用户名，不是 token)

规则 2 — 禁止硬编码凭证
  错误：const token = "ghp_abc123..."
  正确：const token = process.env.GITHUB_TOKEN

规则 3 — env 读取必须封装在命名函数中
  错误：const repo = process.env.GITHUB_REPO  // 顶层读取
  正确：function loadConfig() { return { repo: process.env.GITHUB_REPO } }

规则 4 — 用 CLI 工具执行认证操作，不要用原始 curl
  错误：curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/...
  正确：gh api repos/owner/repo/commits/main

规则 5 — 禁止解码或预览凭证字节
  错误：echo $TOKEN | base64 -d
  错误：echo $TOKEN | head -c 20
  正确：gh auth status  （不加 --show-token）

规则 6 — 所有 env var 必须在 SKILL.md requirements.env 中声明
  每个脚本读取的 env var 都必须列出：
    name, required (true/false), description

以上规则由阶段 7.5（scan-check.js）在上传前强制执行。
`);
}
