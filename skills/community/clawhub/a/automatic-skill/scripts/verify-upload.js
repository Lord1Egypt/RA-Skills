#!/usr/bin/env node
/**
 * Automatic Skill — Stage 9: Verify Upload
 *
 * PROMPT GENERATOR ONLY — this script makes NO outbound network requests.
 * Outputs an agent prompt that uses the gh CLI (github skill pattern) for all
 * GitHub verification: live commit check, directory existence, file count via gh api.
 *
 * Usage:
 *   node scripts/verify-upload.js <skill-slug>
 *   node scripts/verify-upload.js --from-pipeline
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let slug = '';
let commitHash = '';
let version = '';
let prNumber = null;
let workflow = 'direct-push';

function loadPipelineState() {
  try {
    const p = path.join(__dirname, '..', 'data', 'current-pipeline.json');
    if (!fs.existsSync(p)) return null;
    delete require.cache[require.resolve(p)];
    return require(p);
  } catch (e) {
    return null;
  }
}

if (args.includes('--from-pipeline')) {
  const p = loadPipelineState();
  if (p) {
    slug = (p.design && p.design.slug)
      || (p.research && p.research.selected && p.research.selected.slug)
      || '';
    commitHash = (p.upload && p.upload.github && p.upload.github.commitHash) || '';
    version = (p.upload && p.upload.version)
      || (p.seo && p.seo.version)
      || (p.design && p.design.version)
      || '1.0.0';
    prNumber = (p.upload && p.upload.github && p.upload.github.prNumber) || null;
    workflow = (p.upload && p.upload.workflow) || 'direct-push';
  }
}
if (!slug) {
  slug = args.filter(a => a !== '--lang' && a !== lang && !a.startsWith('--'))[0] || '';
}
if (!slug) {
  console.error('Usage: node scripts/verify-upload.js <skill-slug>');
  console.error('       node scripts/verify-upload.js --from-pipeline');
  process.exit(1);
}

const repo = '$GITHUB_REPO';
const skillPath = `openclaw/agents/skills/${slug}`;

if (lang === 'en') {
  console.log(`=== AUTOMATIC SKILL — Stage 9: Verify Upload ===
Skill: ${slug}  version: ${version}
Commit hash: ${commitHash || '(read from pipeline)'}
GitHub repo: ${repo}
Workflow used: ${workflow}${prNumber ? `  PR: #${prNumber}` : ''}

Verify that the skill is fully published on both GitHub and clawHub.
All checks use the gh CLI — no git fetch or local clone required.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 1 — GITHUB VERIFICATION (gh api)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHECK 1 — Verify authentication is still valid
  gh auth status
  → Must show ✓ Logged in. If expired: gh auth refresh

CHECK 2 — Verify commit landed on GitHub
  gh api repos/${repo}/commits/main \\
    --jq '[.sha, .commit.message, .commit.author.date] | @tsv'
  → The top commit SHA must match: ${commitHash || '<commitHash from pipeline>'}
  → The commit message must contain "${slug}"
${prNumber ? `
  (PR workflow) Confirm PR was merged:
  gh pr view ${prNumber} --json state,mergedAt,mergeCommit --jq '{state,mergedAt,sha:.mergeCommit.oid}'
  → state must be "MERGED"` : ''}

CHECK 3 — Verify skill directory exists on GitHub (live, no git fetch needed)
  gh api repos/${repo}/contents/${skillPath} \\
    --jq '[.[].name] | sort | .[]'
  → Must list at minimum: SKILL.md, package.json, _meta.json
  → If 404: the push did not include this path — re-run upload.js

CHECK 4 — Verify file count in skill directory
  gh api "repos/${repo}/git/trees/main?recursive=1" \\
    --jq '[.tree[] | select(.path | startswith("${skillPath}/")) | .path] | length'
  → Must be ≥ 4 (SKILL.md, package.json, _meta.json, ≥1 script)
  → If 0: skill directory was not committed — check git add path in upload step

CHECK 5 — Verify SKILL.md exists and has content on GitHub
  gh api repos/${repo}/contents/${skillPath}/SKILL.md \\
    --jq '{name, size, encoding}'
  → name must be "SKILL.md"
  → size must be > 0 (non-empty file)
  → Confirms the file was uploaded and is accessible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 2 — CLAWHUB VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHECK 6 — Query clawHub for the published skill
  clawhub get ${slug}
  → Must return: slug, version, ownerId
  → Exit code must be 0
  → If error: check CLAWHUB_TOKEN and re-run clawhub publish

CHECK 7 — Verify version matches _meta.json
  clawhub get ${slug} | grep '"version"'
  → Must show: "${version}"
  → If mismatch: a previous version may have been cached — run clawhub publish with --version ${version}

CHECK 8 — Verify skill is searchable (optional)
  clawhub search ${slug}
  → Should return this skill in results within 1–2 minutes of publish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (write to data/current-pipeline.json under "verifyUpload" key)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "verify-upload",
  "slug": "${slug}",
  "version": "${version}",
  "github": {
    "commitFound": true | false,
    "commitHashMatch": true | false,
    "directoryExists": true | false,
    "fileCount": <N>,
    "skillMdNonEmpty": true | false,
    "status": "VERIFIED | FAILED",
    "detail": "..."
  },
  "clawhub": {
    "skillFound": true | false,
    "publishedVersion": "...",
    "versionMatch": true | false,
    "status": "VERIFIED | FAILED",
    "detail": "..."
  },
  "overallVerdict": "FULLY_VERIFIED | PARTIAL | FAILED",
  "completedAt": "<ISO timestamp>"
}

If FAILED: identify which check failed, re-run Stage 8 (upload.js) for that part only.
If FULLY_VERIFIED or PARTIAL: proceed to Stage 9b: node scripts/scan-check.js --from-pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 3 — SECURITY SCAN (VirusTotal + OpenClaw)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After confirming clawHub publish succeeded, check security ratings:

  node scripts/scan-check.js --from-pipeline

This will:
  1. Wait for VirusTotal and OpenClaw scan results (polls up to 5 min)
  2. Run static analysis on the skill's scripts for known trigger patterns
  3. If Suspicious: output targeted fix instructions + re-publish guidance
  4. Repeat until PASS or max 3 attempts reached

→ PASS or TIMEOUT:   proceed to Stage 10: node scripts/final-review.js --from-pipeline
→ SUSPICIOUS (after fixes): proceed to Stage 10 with a scan warning in the final report
`);
} else {
  console.log(`=== AUTOMATIC SKILL — 阶段 9：验收 ===
Skill：${slug}  版本：${version}
Commit hash：${commitHash || '（从 pipeline 读取）'}
GitHub 仓库：${repo}
使用的工作流：${workflow}${prNumber ? `  PR：#${prNumber}` : ''}

验证 skill 已完整发布到 GitHub 和 clawHub。
所有检查使用 gh CLI — 无需 git fetch 或本地 clone。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一部分 — GitHub 验证（gh api）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检查 1 — 确认认证仍然有效
  gh auth status
  → 必须显示 ✓ Logged in。如已过期：gh auth refresh

检查 2 — 验证 commit 已到达 GitHub
  gh api repos/${repo}/commits/main \\
    --jq '[.sha, .commit.message, .commit.author.date] | @tsv'
  → 最顶部 commit SHA 必须匹配：${commitHash || '<pipeline 中的 commitHash>'}
  → commit message 必须包含 "${slug}"
${prNumber ? `
  （PR 工作流）确认 PR 已合并：
  gh pr view ${prNumber} --json state,mergedAt,mergeCommit --jq '{state,mergedAt,sha:.mergeCommit.oid}'
  → state 必须为 "MERGED"` : ''}

检查 3 — 验证 skill 目录在 GitHub 上存在（实时，无需 git fetch）
  gh api repos/${repo}/contents/${skillPath} \\
    --jq '[.[].name] | sort | .[]'
  → 必须至少列出：SKILL.md, package.json, _meta.json
  → 如 404：push 未包含此路径 — 重新运行 upload.js

检查 4 — 验证 skill 目录文件数量
  gh api "repos/${repo}/git/trees/main?recursive=1" \\
    --jq '[.tree[] | select(.path | startswith("${skillPath}/")) | .path] | length'
  → 必须 ≥ 4（SKILL.md, package.json, _meta.json, ≥1 脚本）
  → 如为 0：skill 目录未被提交 — 检查 upload 步骤中的 git add 路径

检查 5 — 验证 SKILL.md 在 GitHub 上存在且有内容
  gh api repos/${repo}/contents/${skillPath}/SKILL.md \\
    --jq '{name, size, encoding}'
  → name 必须为 "SKILL.md"
  → size 必须 > 0（非空文件）
  → 确认文件已上传且可访问

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二部分 — clawHub 验证
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检查 6 — 从 clawHub 查询已发布的 skill
  clawhub get ${slug}
  → 必须返回：slug, version, ownerId
  → 退出码必须为 0
  → 如报错：检查 CLAWHUB_TOKEN 并重新运行 clawhub publish

检查 7 — 验证版本与 _meta.json 匹配
  clawhub get ${slug} | grep '"version"'
  → 必须显示："${version}"
  → 如不匹配：可能是旧版本缓存 — 用 --version ${version} 重新 clawhub publish

检查 8 — 验证 skill 可被搜索（可选）
  clawhub search ${slug}
  → 发布后 1~2 分钟内应能在结果中找到该 skill

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出格式（写入 data/current-pipeline.json 的 "verifyUpload" 键）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "verify-upload",
  "slug": "${slug}",
  "version": "${version}",
  "github": {
    "commitFound": true | false,
    "commitHashMatch": true | false,
    "directoryExists": true | false,
    "fileCount": <N>,
    "skillMdNonEmpty": true | false,
    "status": "VERIFIED | FAILED",
    "detail": "..."
  },
  "clawhub": {
    "skillFound": true | false,
    "publishedVersion": "...",
    "versionMatch": true | false,
    "status": "VERIFIED | FAILED",
    "detail": "..."
  },
  "overallVerdict": "FULLY_VERIFIED | PARTIAL | FAILED",
  "completedAt": "<ISO 时间戳>"
}

如果 FAILED：确定哪项检查失败，仅针对该部分重新运行阶段 8（upload.js）。
如果 FULLY_VERIFIED 或 PARTIAL：进入阶段 9b：node scripts/scan-check.js --from-pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三部分 — 安全扫描（VirusTotal + OpenClaw）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

确认 clawHub 发布成功后，检查安全评级：

  node scripts/scan-check.js --from-pipeline

此命令将：
  1. 等待 VirusTotal 和 OpenClaw 扫描结果（最多轮询 5 分钟）
  2. 对 skill 脚本进行静态分析，查找已知触发模式
  3. 如为 Suspicious：输出针对性修复指令 + 重新发布指引
  4. 最多重复 3 次，直到 PASS 为止

→ PASS 或 TIMEOUT：进入阶段 10：node scripts/final-review.js --from-pipeline
→ SUSPICIOUS（修复后仍是）：带扫描警告进入阶段 10，在 final report 中标注
`);
}
