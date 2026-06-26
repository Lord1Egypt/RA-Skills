#!/usr/bin/env node
/**
 * Automatic Skill — Stage 7: Self-Check (自检)
 * 输出 Agent 执行 prompt，指导其对新 skill 逐项核对必填字段、文件树、脚本签名。
 *
 * 用法:
 *   node scripts/self-check.js <skill-dir>
 *   node scripts/self-check.js --from-pipeline
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
  console.error('Usage: node scripts/self-check.js <skill-dir>');
  console.error('       node scripts/self-check.js --from-pipeline');
  process.exit(1);
}

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 7: Self-Check ===
Skill directory: ${skillDir}

Perform a rigorous self-check. This is the last gate before upload.

MANDATORY FILE CHECK — verify each file exists and is non-empty:
□ ${skillDir}/SKILL.md           → must exist, size > 500 bytes
□ ${skillDir}/package.json       → must be valid JSON, has "name", "version", "scripts"
□ ${skillDir}/_meta.json         → must have ownerId, slug, version
□ ${skillDir}/.clawhub/origin.json → must have ownerId and slug

FRONTMATTER CHECK — parse SKILL.md YAML frontmatter and verify:
□ name: non-empty string
□ description: ≥ 100 characters
□ keywords: array with ≥ 15 items
□ metadata.openclaw.runtime.node: present

SLUG CONSISTENCY CHECK:
□ slug in SKILL.md frontmatter name == slug in _meta.json == slug in .clawhub/origin.json == directory basename

SCRIPTS CHECK — for each script listed in package.json "scripts":
□ The file exists at the referenced path
□ File starts with "#!/usr/bin/env node" or similar shebang / header comment
□ File size > 100 bytes

VERSION CHECK:
□ package.json version matches _meta.json version

DATA FILES CHECK (if any data/ directory exists):
□ All .json files in data/ are valid JSON
□ No data file contains real user data (should be empty arrays/objects for a fresh skill)

REQUIRED SECTIONS CHECK — parse SKILL.md body and verify all five sections exist with real content:
□ "## Purpose & Capability" heading present
  → body must contain: core concept description + capability list/table + explicit "does not" boundary
□ "## Instruction Scope" heading present
  → body must contain: in-scope examples + out-of-scope list + behavior when missing credentials
□ "## Credentials" heading present
  → body must contain: Action/Credential/Scope table (or explicit "no credentials required" statement)
  → must NOT contain: hardcoded token values, personal account IDs, or real API keys
□ "## Persistence & Privilege" heading present
  → body must contain: paths-written table + "does not write" list + uninstall instructions
□ "## Install Mechanism" heading present
  → body must contain: clawhub install command + verification step + env var examples
Each section must be > 50 characters (non-empty). Missing or empty section = FAIL.

CROSS-REFERENCE CHECK:
□ All scripts mentioned in SKILL.md actually exist in the scripts/ directory
□ All cron commands in SKILL.md reference valid script files
□ package.json "scripts" entries match actual filenames

FINAL COMPLETENESS SCORE:
Count total checks. Calculate: passed / total * 100.

OUTPUT FORMAT (JSON):
{
  "stage": "self-check",
  "skillDir": "${skillDir}",
  "slug": "...",
  "totalChecks": <N>,
  "passedChecks": <N>,
  "score": <0-100>,
  "failures": [ { "check": "...", "detail": "...", "fix": "..." } ],
  "verdict": "READY_TO_UPLOAD" | "NEEDS_FIX",
  "completedAt": "<ISO timestamp>"
}

If verdict is NEEDS_FIX: apply all fixes and re-run self-check until READY_TO_UPLOAD.
If READY_TO_UPLOAD: proceed to Stage 8: node scripts/upload.js ${skillDir}

Update data/current-pipeline.json: add "selfCheck" key with the report above.
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 7：自检 ===
Skill 目录：${skillDir}

执行严格的自检。这是上传前的最后关卡。

必填文件检查 — 验证每个文件存在且非空：
□ ${skillDir}/SKILL.md           → 必须存在，大小 > 500 字节
□ ${skillDir}/package.json       → 必须是合法 JSON，有 "name"、"version"、"scripts"
□ ${skillDir}/_meta.json         → 必须有 ownerId, slug, version
□ ${skillDir}/.clawhub/origin.json → 必须有 ownerId 和 slug

Frontmatter 检查 — 解析 SKILL.md YAML frontmatter 并验证：
□ name：非空字符串
□ description：≥ 100 个字符
□ keywords：数组，≥ 15 项
□ metadata.openclaw.runtime.node：存在

Slug 一致性检查：
□ SKILL.md frontmatter name == _meta.json slug == .clawhub/origin.json slug == 目录 basename

脚本检查 — 对 package.json "scripts" 中列出的每个脚本：
□ 文件存在于引用路径
□ 文件以 "#!/usr/bin/env node" 或类似 shebang/头部注释开头
□ 文件大小 > 100 字节

版本检查：
□ package.json version == _meta.json version

数据文件检查（如存在 data/ 目录）：
□ data/ 中所有 .json 文件为合法 JSON
□ 数据文件不含真实用户数据（新 skill 应为空数组/空对象）

必要章节检查 — 解析 SKILL.md 正文，验证五个必要章节均存在且有真实内容：
□ "## Purpose & Capability" 标题存在
  → 正文必须包含：核心概念说明 + 能力列表/表格 + 明确的"不做"边界
□ "## Instruction Scope" 标题存在
  → 正文必须包含：在 scope 内示例 + 不在 scope 内列表 + 凭证缺失时的行为
□ "## Credentials" 标题存在
  → 正文必须包含：操作/凭证/范围表格（或明确的"无需凭证"声明）
  → 不得包含：硬编码的 token 值、个人账号 ID、真实 API 密钥
□ "## Persistence & Privilege" 标题存在
  → 正文必须包含：写入路径表格 + "不写入"列表 + 卸载方法
□ "## Install Mechanism" 标题存在
  → 正文必须包含：clawhub install 命令 + 验证步骤 + env var 配置示例
每个章节内容必须 > 50 个字符（非空）。章节缺失或为空 = FAIL。

交叉引用检查：
□ SKILL.md 中提及的所有脚本实际存在于 scripts/ 目录
□ SKILL.md 中所有 cron 命令引用的脚本文件均存在
□ package.json "scripts" 条目与实际文件名匹配

最终完整度评分：
计算总检查项数。计算：通过项 / 总项 * 100。

输出格式（JSON）：
{
  "stage": "self-check",
  "skillDir": "${skillDir}",
  "slug": "...",
  "totalChecks": <N>,
  "passedChecks": <N>,
  "score": <0-100>,
  "failures": [ { "check": "...", "detail": "...", "fix": "..." } ],
  "verdict": "READY_TO_UPLOAD" | "NEEDS_FIX",
  "completedAt": "<ISO 时间戳>"
}

如果 verdict 为 NEEDS_FIX：应用所有修复并重新自检，直到 READY_TO_UPLOAD。
如果 READY_TO_UPLOAD：进入阶段 8：node scripts/upload.js ${skillDir}

更新 data/current-pipeline.json：添加 "selfCheck" 键，值为上述报告。
`);
}
