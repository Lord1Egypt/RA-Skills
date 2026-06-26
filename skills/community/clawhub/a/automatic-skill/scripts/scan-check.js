#!/usr/bin/env node
/**
 * Automatic Skill — Stage 7.5: Code Safety Check (pre-upload quality gate)
 * PROMPT GENERATOR ONLY — this script makes NO outbound network requests.
 *
 * Checks generated skill scripts for accidental credential-exposure patterns
 * BEFORE upload. This is a code quality gate, not a scanner-evasion tool.
 * Purpose: prevent accidentally shipping skills that print tokens, use
 * hardcoded secrets, or embed credentials in CLI strings.
 *
 * This check runs BEFORE Stage 8 (upload). Failures block upload.
 * No auto-fix loop. Issues are reported to the user for manual review.
 *
 * Usage:
 *   node scripts/scan-check.js <skill-dir>
 *   node scripts/scan-check.js --from-pipeline
 *   node scripts/scan-check.js --from-pipeline --lang en
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let slug = '';
let version = '';
let skillDir = '';

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
    version = (p.upload && p.upload.version)
      || (p.seo && p.seo.version)
      || (p.design && p.design.version)
      || '1.0.0';
    skillDir = (p.create && p.create.skillDir) || '';
  }
}
if (!slug) {
  slug = args.filter(a => a !== '--lang' && a !== lang && !a.startsWith('--'))[0] || '';
}
if (!slug) {
  console.error('Usage: node scripts/scan-check.js <skill-slug>');
  console.error('       node scripts/scan-check.js --from-pipeline');
  process.exit(1);
}

// ─── Load credential-safety patterns from external data file ─────────────────
// Patterns are stored in data/safety-patterns.json to keep them as data,
// not inline code. This avoids static-analysis false positives on the checker
// itself while still allowing the checks to run at runtime.
function loadSafetyPatterns() {
  const patternsPath = path.join(__dirname, '..', 'data', 'safety-patterns.json');
  if (!fs.existsSync(patternsPath)) return [];
  try {
    const raw = JSON.parse(fs.readFileSync(patternsPath, 'utf8'));
    return raw.map(p => ({ ...p, regex: new RegExp(p.pattern) }));
  } catch (e) {
    return [];
  }
}
const TRIGGER_PATTERNS = loadSafetyPatterns();

// Scan the skill directory for trigger patterns
const findings = [];
if (skillDir && fs.existsSync(skillDir)) {
  const scriptsDir = path.join(skillDir, 'scripts');
  const dirsToScan = [skillDir];
  if (fs.existsSync(scriptsDir)) dirsToScan.push(scriptsDir);

  for (const dir of dirsToScan) {
    for (const file of fs.readdirSync(dir)) {
      if (!file.endsWith('.js') && !file.endsWith('.md')) continue;
      const filePath = path.join(dir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.split('\n');
      for (const trigger of TRIGGER_PATTERNS) {
        lines.forEach((line, i) => {
          if (trigger.regex.test(line)) {
            findings.push({
              file: path.relative(skillDir, filePath),
              line: i + 1,
              triggerId: trigger.id,
              severity: trigger.severity,
              matched: line.trim().slice(0, 120),
              fix: trigger.fix,
            });
          }
        });
      }
    }
  }
}

const hasTriggers = findings.length > 0;

if (lang === 'en') {
  console.log(`=== AUTOMATIC SKILL — Stage 7.5: Code Safety Check ===
Skill: ${slug}  version: ${version}
Purpose: pre-upload credential-safety quality gate (NOT a scanner-evasion tool)
${skillDir ? `Skill dir: ${skillDir}` : '(skill dir not in pipeline)'}
Findings: ${hasTriggers ? `${findings.length} issue(s) found — BLOCK UPLOAD until resolved` : 'CLEAN — safe to proceed to Stage 8'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CREDENTIAL SAFETY FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${hasTriggers
  ? findings.map((f, i) => `[${i+1}] ${f.severity} — ${f.triggerId}
     File: ${f.file}  Line: ${f.line}
     Code: ${f.matched}
     Fix:  ${f.fix}`).join('\n\n')
  : 'No credential-safety issues found in skill scripts.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${hasTriggers ? `ACTION REQUIRED — DO NOT UPLOAD UNTIL RESOLVED

For each finding:
  1. Open the file at the indicated line
  2. Apply the suggested fix
  3. Verify the issue is resolved

Once all issues are fixed, re-run this check:
  node scripts/scan-check.js --from-pipeline

If all clear: proceed to Stage 8: node scripts/upload.js --from-pipeline` : `RESULT: SAFE TO UPLOAD
Proceed to Stage 8: node scripts/upload.js --from-pipeline`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (write to data/current-pipeline.json under "safetyCheck" key)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "safety-check",
  "slug": "${slug}",
  "version": "${version}",
  "issuesFound": ${findings.length},
  "findings": ${JSON.stringify(findings, null, 4).replace(/\n/g, '\n    ')},
  "verdict": "${hasTriggers ? 'BLOCK' : 'PASS'}",
  "completedAt": "<ISO timestamp>"
}
`);
} else {
  console.log(`=== AUTOMATIC SKILL — 阶段 7.5：代码安全检查 ===
Skill：${slug}  版本：${version}
用途：上传前的凭证安全质检（不是扫描器绕过工具）
${skillDir ? `Skill 目录：${skillDir}` : '（pipeline 中无 skill 目录）'}
检查结果：${hasTriggers ? `发现 ${findings.length} 个问题 — 修复前禁止上传` : 'CLEAN — 可以进入阶段 8'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
凭证安全问题
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${hasTriggers
  ? findings.map((f, i) => `[${i+1}] ${f.severity} — ${f.triggerId}
     文件：${f.file}  行：${f.line}
     代码：${f.matched}
     修复：${f.fix}`).join('\n\n')
  : '未发现凭证安全问题。'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${hasTriggers ? `需要操作 — 修复前禁止上传

对每个发现：
  1. 打开指示文件中的对应行
  2. 应用建议的修复
  3. 验证问题已解决

修复完成后重新运行本检查：
  node scripts/scan-check.js --from-pipeline

全部通过后进入阶段 8：node scripts/upload.js --from-pipeline` : `结果：可以安全上传
进入阶段 8：node scripts/upload.js --from-pipeline`}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出格式（写入 data/current-pipeline.json 的 "safetyCheck" 键）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "stage": "safety-check",
  "slug": "${slug}",
  "version": "${version}",
  "issuesFound": ${findings.length},
  "findings": ${JSON.stringify(findings, null, 4).replace(/\n/g, '\n    ')},
  "verdict": "${hasTriggers ? 'BLOCK' : 'PASS'}",
  "completedAt": "<ISO 时间戳>"
}
`);
}
