#!/usr/bin/env node
/**
 * Automatic Skill — Stage 8: Upload
 * PROMPT GENERATOR ONLY — this script makes NO outbound network requests.
 * Outputs an agent prompt that uses the gh CLI (github skill pattern) for all
 * GitHub operations: auth check, repo access, commit verification, and PR workflow.
 *
 * Usage:
 *   node scripts/upload.js <skill-dir>
 *   node scripts/upload.js --from-pipeline
 *   node scripts/upload.js --dry-run --from-pipeline
 *   node scripts/upload.js --pr           # use PR workflow instead of direct push
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const dryRun = args.includes('--dry-run');
const usePR = args.includes('--pr');

let skillDir = '';
let slug = '';
let version = '';

if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (fs.existsSync(pipelinePath)) {
    const p = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
    skillDir = (p.create && p.create.skillDir) || '';
    slug = (p.design && p.design.slug)
      || (p.research && p.research.selected && p.research.selected.slug)
      || path.basename(skillDir);
    version = (p.seo && p.seo.version)
      || (p.design && p.design.version)
      || '1.0.0';
  }
}
if (!skillDir) {
  skillDir = args.filter(a => a !== '--lang' && a !== lang && !a.startsWith('--'))[0] || '';
  slug = path.basename(skillDir);
}
if (!skillDir) {
  console.error('Usage: node scripts/upload.js <skill-dir>');
  console.error('       node scripts/upload.js --from-pipeline');
  console.error('       node scripts/upload.js --pr    # use PR workflow');
  process.exit(1);
}

// Read for display in prompt text only — never sent over network by this script
const githubRepo = process.env.GITHUB_REPO || '<GITHUB_REPO not set>';
const dryRunNote = dryRun ? '\n⚠️  DRY-RUN MODE: print all commands but DO NOT execute git push, gh pr, or clawhub publish.' : '';
const prNote = usePR ? '\n📋  PR WORKFLOW: create a pull request instead of pushing directly to main.' : '';
const branchName = `auto-skill/${slug}`;

// Extract owner from GITHUB_REPO (format: owner/repo)
const githubOwner = githubRepo.includes('/') ? githubRepo.split('/')[0] : '<owner>';

if (lang === 'en') {
  console.log(`=== AUTOMATIC SKILL — Stage 8: Upload ===
Skill: ${slug}  version: ${version}
Skill directory: ${skillDir}
GitHub repo (monorepo): ${githubRepo}
Standalone repo: ${githubOwner}/${slug}
Workflow: ${usePR ? 'PR (branch → merge)' : 'Direct push to main'}${dryRunNote}${prNote}

Upload the skill to GitHub and clawHub using the gh CLI.
Prerequisites: gh CLI installed and authenticated (gh auth status should show ✓ Logged in).

PUBLISHING CONVENTION: Every skill must have BOTH:
  1. A standalone GitHub repo (${githubOwner}/${slug}) — allows users to search and find the skill directly
  2. A directory in the monorepo (${githubRepo}/openclaw/agents/skills/${slug}/) — for the registry index

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 1 — PRE-FLIGHT CHECKS (gh CLI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHECK 1 — Verify gh authentication
Run: gh auth status
→ Must show: ✓ Logged in to github.com
→ If not logged in: gh auth login
→ Verify token scopes include "repo" (needed for push/PR)

CHECK 2 — Verify monorepo access
Run: gh repo view ${githubRepo} --json name,defaultBranchRef,url
→ Must return JSON with name and defaultBranchRef.name = "main"
→ If 404: verify GITHUB_REPO is correct (format: owner/repo)
→ If permission denied: check token scopes with: gh auth status (look for the scopes list)

CHECK 3 — Confirm skill directory exists locally
Run: ls -la ${skillDir}/SKILL.md ${skillDir}/package.json ${skillDir}/_meta.json
→ All three files must exist. If missing, re-run Stage 4 (create.js).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 2 — STANDALONE SKILL REPO (required for discoverability)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — Check if standalone repo exists${dryRun ? ' (CHECK ONLY — dry-run)' : ''}
  gh repo view ${githubOwner}/${slug} --json name 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"

STEP 2 — Create standalone repo if not exists${dryRun ? ' (SKIPPED — dry-run)' : ''}
${dryRun
  ? `DRY-RUN: would run:
  gh repo create ${githubOwner}/${slug} --public --description "<tagline from SKILL.md>"`
  : `If NOT_FOUND:
  # Read the tagline from SKILL.md description field (first line after "description: |")
  gh repo create ${githubOwner}/${slug} --public --description "<tagline from SKILL.md frontmatter>"

  If EXISTS: skip creation, proceed to STEP 3.`}

STEP 3 — Push skill files to standalone repo${dryRun ? ' (SKIPPED — dry-run)' : ''}
${dryRun
  ? 'DRY-RUN: would initialize standalone repo and push skill files'
  : `Create a clean local git repo from the skill directory and push:
  cd /tmp
  rm -rf ${slug}-standalone
  cp -r ${skillDir} ${slug}-standalone
  cd ${slug}-standalone
  git init
  git add .
  git commit -m "feat: ${slug}@${version} — auto-generated by automatic-skill"
  git remote add origin https://github.com/${githubOwner}/${slug}.git
  git push -u origin main

  Verify standalone push:
  gh api repos/${githubOwner}/${slug}/commits/main --jq '.sha + " | " + .commit.message'
  → Should show the new commit`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 3 — MONOREPO GITHUB UPLOAD (git + gh CLI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4 — Navigate to monorepo root
Find the repo root and cd into it. The skill must be inside this repo:
  gh repo view ${githubRepo} --json url --jq '.url'
  cd <repo-root>

STEP 5 — Ensure skill directory is in the monorepo
  ls openclaw/agents/skills/${slug}/
  If missing: cp -r ${skillDir} openclaw/agents/skills/${slug}/

${usePR ? `STEP 6 — Create branch for PR workflow
  git checkout -b ${branchName}
  → If branch exists: git checkout ${branchName} && git reset --hard origin/main` : `STEP 6 — Confirm on main branch
  git branch --show-current
  → Must be "main". If not: git checkout main`}

STEP 7 — Stage skill files
  git add openclaw/agents/skills/${slug}/
  git status
  → Confirm only ${slug} files are staged. Check for unexpected changes.

STEP 8 — Commit
  git commit -m "feat: add ${slug}@${version} — auto-generated by automatic-skill"
  → Record the commit hash: git rev-parse HEAD

STEP 9 — ${usePR ? 'Push branch and open PR' : 'Push to main'}${dryRun ? ' (SKIPPED — dry-run)' : ''}
${dryRun ? `DRY-RUN: would run:
  ${usePR
    ? `git push -u origin ${branchName}
  gh pr create --title "feat: add ${slug}@${version} skill" \\
    --body "Auto-generated by automatic-skill pipeline. Skill: ${slug} v${version}" \\
    --base main --head ${branchName}`
    : 'git push origin main'}` : usePR
    ? `git push -u origin ${branchName}

  Then open a PR with gh:
  gh pr create \\
    --title "feat: add ${slug}@${version} skill" \\
    --body "Auto-generated by automatic-skill pipeline.\\n\\nSkill: ${slug}\\nVersion: ${version}\\nDirectory: openclaw/agents/skills/${slug}/" \\
    --base main \\
    --head ${branchName}

  → Record PR number: gh pr view --json number --jq '.number'

  Auto-merge (if branch protection allows):
  gh pr merge --squash --auto`
    : `git push origin main

  Verify push succeeded:
  gh api repos/${githubRepo}/commits/main --jq '.sha + " | " + .commit.message'
  → Should show your new commit at the top`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 3 — CLAWHUB PUBLISH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 7 — Verify clawHub authentication
  clawhub whoami
  → Must return your clawHub username (exit code 0)
  → If error: set CLAWHUB_TOKEN in your shell environment and retry

STEP 8 — Publish to clawHub${dryRun ? ' (SKIPPED — dry-run)' : ''}
${dryRun
  ? 'DRY-RUN: would run clawhub publish command'
  : `  clawhub publish ${skillDir} --version ${version}`}

  → On success: record the skill ID returned by clawhub publish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (write to data/current-pipeline.json under "upload" key)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "upload",
  "skillDir": "${skillDir}",
  "slug": "${slug}",
  "version": "${version}",
  "dryRun": ${dryRun},
  "workflow": "${usePR ? 'pr' : 'direct-push'}",
  "github": {
    "standaloneRepo": "${githubOwner}/${slug}",
    "standaloneCommitHash": "<standalone repo commit hash>",
    "monorepo": "${githubRepo}",
    "monorepoPath": "openclaw/agents/skills/${slug}/",
    "branch": "${usePR ? branchName : 'main'}",
    "commitHash": "<git rev-parse HEAD output>",
    "prNumber": ${usePR ? '"<PR number or null>"' : 'null'},
    "status": "SUCCESS | FAILED | SKIPPED",
    "error": null
  },
  "clawhub": {
    "publishedVersion": "${version}",
    "skillId": "<clawhub skill ID>",
    "status": "SUCCESS | FAILED | SKIPPED",
    "error": null
  },
  "completedAt": "<ISO timestamp>"
}

If any part FAILED: record the error, stop. Do not proceed to Stage 9.
If SUCCESS or SKIPPED (dry-run): proceed to Stage 9: node scripts/verify-upload.js --from-pipeline
`);
} else {
  console.log(`=== AUTOMATIC SKILL — 阶段 8：上传 ===
Skill：${slug}  版本：${version}
Skill 目录：${skillDir}
GitHub 主仓库（monorepo）：${githubRepo}
独立仓库：${githubOwner}/${slug}
工作流：${usePR ? 'PR（分支 → 合并）' : '直接推送到 main'}${dryRunNote}${prNote}

使用 gh CLI 将 skill 上传到 GitHub 和 clawHub。
前提条件：已安装 gh CLI 且已认证（gh auth status 应显示 ✓ Logged in）。

发布规则：每个 skill 必须同时拥有：
  1. 独立 GitHub 仓库（${githubOwner}/${slug}）— 让用户可以直接搜索到该 skill
  2. monorepo 子目录（${githubRepo}/openclaw/agents/skills/${slug}/）— 作为注册表索引

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一部分 — 预检（gh CLI）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检查 1 — 验证 gh 认证
运行：gh auth status
→ 必须显示：✓ Logged in to github.com
→ 如未登录：gh auth login
→ 验证 token scopes 包含 "repo"（推送/PR 所需）

检查 2 — 验证 monorepo 访问权限
运行：gh repo view ${githubRepo} --json name,defaultBranchRef,url
→ 必须返回 JSON，其中 defaultBranchRef.name = "main"
→ 如 404：检查 GITHUB_REPO 格式是否为 "owner/repo"
→ 如权限拒绝：gh auth status 检查 token scopes（查看输出中的 scopes 列表）

检查 3 — 确认 skill 目录在本地存在
运行：ls -la ${skillDir}/SKILL.md ${skillDir}/package.json ${skillDir}/_meta.json
→ 三个文件必须都存在，缺失则重跑阶段 4（create.js）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二部分 — 独立 skill 仓库（可发现性必需）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤 1 — 检查独立仓库是否已存在${dryRun ? '（仅检查 — dry-run）' : ''}
  gh repo view ${githubOwner}/${slug} --json name 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"

步骤 2 — 如不存在则创建独立仓库${dryRun ? '（已跳过 — dry-run）' : ''}
${dryRun
  ? `DRY-RUN：将运行：
  gh repo create ${githubOwner}/${slug} --public --description "<来自 SKILL.md 的 tagline>"`
  : `如结果为 NOT_FOUND：
  # 从 SKILL.md description 字段读取第一行作为 tagline
  gh repo create ${githubOwner}/${slug} --public --description "<SKILL.md frontmatter 中的 tagline>"

  如结果为 EXISTS：跳过创建，直接执行步骤 3。`}

步骤 3 — 将 skill 文件推送到独立仓库${dryRun ? '（已跳过 — dry-run）' : ''}
${dryRun
  ? 'DRY-RUN：将初始化独立仓库并推送 skill 文件'
  : `从 skill 目录创建干净的本地 git 仓库并推送：
  cd /tmp
  rm -rf ${slug}-standalone
  cp -r ${skillDir} ${slug}-standalone
  cd ${slug}-standalone
  git init
  git add .
  git commit -m "feat: ${slug}@${version} — auto-generated by automatic-skill"
  git remote add origin https://github.com/${githubOwner}/${slug}.git
  git push -u origin main

  验证推送成功：
  gh api repos/${githubOwner}/${slug}/commits/main --jq '.sha + " | " + .commit.message'`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三部分 — monorepo GitHub 上传（git + gh CLI）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤 4 — 进入 monorepo 根目录
  gh repo view ${githubRepo} --json url --jq '.url'
  cd <仓库根目录>

步骤 5 — 确认 skill 目录在仓库内
  ls openclaw/agents/skills/${slug}/
  如不存在：cp -r ${skillDir} openclaw/agents/skills/${slug}/

${usePR ? `步骤 6 — 创建 PR 分支
  git checkout -b ${branchName}
  → 如分支已存在：git checkout ${branchName} && git reset --hard origin/main` : `步骤 6 — 确认在 main 分支
  git branch --show-current
  → 必须为 "main"。如不是：git checkout main`}

步骤 7 — 暂存 skill 文件
  git add openclaw/agents/skills/${slug}/
  git status
  → 确认只有 ${slug} 的文件被暂存，注意检查意外改动

步骤 8 — 提交
  git commit -m "feat: add ${slug}@${version} — auto-generated by automatic-skill"
  → 记录 commit hash：git rev-parse HEAD

步骤 9 — ${usePR ? '推送分支并创建 PR' : '推送到 main'}${dryRun ? '（已跳过 — dry-run）' : ''}
${dryRun ? `DRY-RUN：将运行：
  ${usePR
    ? `git push -u origin ${branchName}
  gh pr create --title "feat: add ${slug}@${version} skill" \\
    --body "auto-generated by automatic-skill pipeline" \\
    --base main --head ${branchName}`
    : 'git push origin main'}` : usePR
    ? `git push -u origin ${branchName}

  用 gh 创建 PR：
  gh pr create \\
    --title "feat: add ${slug}@${version} skill" \\
    --body "由 automatic-skill 流水线自动生成。\\n\\nSkill：${slug}\\n版本：${version}\\n目录：openclaw/agents/skills/${slug}/" \\
    --base main \\
    --head ${branchName}

  → 记录 PR 号：gh pr view --json number --jq '.number'

  自动合并（如分支保护允许）：
  gh pr merge --squash --auto`
    : `git push origin main

  验证推送成功：
  gh api repos/${githubRepo}/commits/main --jq '.sha + " | " + .commit.message'
  → 应在最顶部看到新 commit`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三部分 — clawHub 发布
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤 7 — 验证 clawHub 认证
  clawhub whoami
  → 必须返回你的 clawHub 用户名（退出码 0）
  → 如报错：在 shell 环境中设置 CLAWHUB_TOKEN 后重试

步骤 8 — 发布到 clawHub${dryRun ? '（已跳过 — dry-run）' : ''}
${dryRun
  ? 'DRY-RUN：将运行 clawhub publish 命令'
  : `  clawhub publish ${skillDir} --version ${version}`}

  → 成功后：记录 clawhub publish 返回的 skill ID

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出格式（写入 data/current-pipeline.json 的 "upload" 键）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "upload",
  "skillDir": "${skillDir}",
  "slug": "${slug}",
  "version": "${version}",
  "dryRun": ${dryRun},
  "workflow": "${usePR ? 'pr' : 'direct-push'}",
  "github": {
    "repo": "${githubRepo}",
    "branch": "${usePR ? branchName : 'main'}",
    "commitHash": "<git rev-parse HEAD 输出>",
    "prNumber": ${usePR ? '"<PR 号或 null>"' : 'null'},
    "status": "SUCCESS | FAILED | SKIPPED",
    "error": null
  },
  "clawhub": {
    "publishedVersion": "${version}",
    "skillId": "<clawhub skill ID>",
    "status": "SUCCESS | FAILED | SKIPPED",
    "error": null
  },
  "completedAt": "<ISO 时间戳>"
}

如果任何部分 FAILED：记录错误并停止，不进入阶段 9。
如果 SUCCESS 或 SKIPPED（dry-run）：进入阶段 9：node scripts/verify-upload.js --from-pipeline
`);
}
