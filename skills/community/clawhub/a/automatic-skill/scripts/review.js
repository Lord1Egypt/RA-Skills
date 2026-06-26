#!/usr/bin/env node
/**
 * Automatic Skill — Stage 5: Review (审核)
 * 输出 Agent 执行 prompt，指导其对照质量检查单验证生成的 Skill。
 *
 * 用法:
 *   node scripts/review.js <skill-dir>
 *   node scripts/review.js --from-pipeline
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let skillDir = '';
if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (fs.existsSync(pipelinePath)) {
    const p = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
    skillDir = p.create && p.create.skillDir ? p.create.skillDir : '';
  }
}
if (!skillDir) {
  skillDir = args.filter(a => a !== '--lang' && a !== lang && !a.startsWith('--'))[0] || '';
}
if (!skillDir) {
  console.error('Usage: node scripts/review.js <skill-dir>');
  console.error('       node scripts/review.js --from-pipeline');
  process.exit(1);
}

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 5: Review ===
Skill directory: ${skillDir}

Review the generated skill against this quality checklist. Mark each item PASS / FAIL / WARNING.

── STRUCTURE CHECKLIST ──────────────────────────────────────────
□ SKILL.md exists and is non-empty
□ SKILL.md frontmatter has: name, description, keywords, metadata.openclaw
□ description is ≥ 3 sentences and explains WHO it's for, WHAT it does, WHEN to use
□ keywords list has ≥ 15 entries, mix of Chinese and English
□ metadata.openclaw.runtime.node is set
□ package.json exists with name, version, description, scripts
□ _meta.json exists with ownerId, slug, version
□ .clawhub/origin.json exists with ownerId and slug
□ All scripts listed in package.json "scripts" actually exist as files

── SCRIPT QUALITY CHECKLIST ─────────────────────────────────────
□ Each script has a header comment (filename, purpose, usage)
□ Each script handles missing/invalid args (prints usage + exits with code 1)
□ Each script produces meaningful output (not empty, not placeholder "TODO")
□ Script output (prompt text) is specific enough for an agent to act on
□ No hardcoded user IDs, tokens, or secrets in scripts
□ No synchronous filesystem reads that could fail silently

── CONTENT QUALITY CHECKLIST ────────────────────────────────────
□ SKILL.md has a "何时使用" or "When to Use" section
□ SKILL.md has a scripts/commands reference section
□ SKILL.md has a ⚠️ notes / caveats section
□ No placeholder text ("...", "TODO", "FIXME", "Lorem ipsum") in any file
□ No broken internal references (mentioned scripts that don't exist)
□ Cron expressions (if any) are valid 5-field cron format

── SECURITY CHECKLIST ───────────────────────────────────────────
□ No hardcoded API keys or tokens
□ User input is validated before use (no injection risk)
□ No dynamic code execution using user-supplied input

OUTPUT INSTRUCTIONS:
For each failed item, describe what is wrong and the exact fix needed.
Produce a review report in this JSON format:

{
  "stage": "review",
  "skillDir": "${skillDir}",
  "score": <0-100>,
  "passed": [...list of PASS items...],
  "warnings": [...list of WARNING items with explanation...],
  "failures": [...list of FAIL items with required fix...],
  "verdict": "PASS" | "FAIL" | "PASS_WITH_WARNINGS",
  "completedAt": "<ISO timestamp>"
}

If verdict is FAIL: fix each failure in the files, then re-run review.
If verdict is PASS or PASS_WITH_WARNINGS: proceed to Stage 6: node scripts/self-run.js ${skillDir}

Update data/current-pipeline.json: add "review" key with the report above.
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 5：审核 ===
Skill 目录：${skillDir}

对照以下质量检查单审核生成的 skill。对每一项标注 通过 / 失败 / 警告。

── 结构检查 ──────────────────────────────────────────────────────
□ SKILL.md 存在且非空
□ SKILL.md frontmatter 包含：name, description, keywords, metadata.openclaw
□ description ≥ 3 句，说明了目标用户（WHO）、功能（WHAT）、触发场景（WHEN）
□ keywords 列表有 ≥ 15 项，中英混合
□ metadata.openclaw.runtime.node 已设置
□ package.json 存在，包含 name, version, description, scripts
□ _meta.json 存在，包含 ownerId, slug, version
□ .clawhub/origin.json 存在，包含 ownerId 和 slug
□ package.json scripts 中列出的所有脚本实际存在对应文件

── 脚本质量检查 ──────────────────────────────────────────────────
□ 每个脚本有头部注释（文件名、用途、用法）
□ 每个脚本处理缺失/无效参数（打印用法 + 以 code 1 退出）
□ 每个脚本产出有意义的输出（非空、非 "TODO" 占位符）
□ 脚本输出的 prompt 文本足够具体，Agent 可据此执行
□ 脚本中无硬编码的用户 ID、token 或密钥
□ 无可能静默失败的同步文件读取

── 内容质量检查 ──────────────────────────────────────────────────
□ SKILL.md 有"何时使用"章节
□ SKILL.md 有脚本/命令参考章节
□ SKILL.md 有 ⚠️ 注意事项章节
□ 任何文件中无占位符文本（"..."、"TODO"、"FIXME"、"Lorem ipsum"）
□ 无断裂的内部引用（提到了不存在的脚本）
□ Cron 表达式（如有）为有效的 5 字段 cron 格式

── 安全检查 ──────────────────────────────────────────────────────
□ 无硬编码的 API key 或 token
□ 用户输入在使用前经过校验（无注入风险）
□ 无使用用户输入作为代码执行的动态调用

输出说明：
对每项失败项，描述问题所在及需要的精确修复方案。
以如下 JSON 格式产出审核报告：

{
  "stage": "review",
  "skillDir": "${skillDir}",
  "score": <0-100>,
  "passed": [...通过项列表...],
  "warnings": [...警告项列表（含说明）...],
  "failures": [...失败项列表（含必要修复方案）...],
  "verdict": "PASS" | "FAIL" | "PASS_WITH_WARNINGS",
  "completedAt": "<ISO 时间戳>"
}

如果 verdict 为 FAIL：修复文件中的每个失败项，然后重新运行审核。
如果 verdict 为 PASS 或 PASS_WITH_WARNINGS：进入阶段 6：node scripts/self-run.js ${skillDir}

更新 data/current-pipeline.json：添加 "review" 键，值为上述报告。
`);
}
