#!/usr/bin/env node
/**
 * Automatic Skill — Stage 4: Create (制作)
 * 输出 Agent 执行 prompt，指导其按设计（含 SEO 优化结果）逐文件生成完整的 Skill。
 *
 * 用法:
 *   node scripts/create.js --from-pipeline
 *   node scripts/create.js <design-json-path>
 *   node scripts/create.js --lang en --from-pipeline
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let design = null;
let seo = null;
let outputDir = process.env.SKILL_OUTPUT_DIR || path.join(process.env.HOME || '~', '.openclaw', 'workspace', 'skills');

if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (!fs.existsSync(pipelinePath)) {
    console.error('ERROR: data/current-pipeline.json not found. Run design.js first.');
    process.exit(1);
  }
  const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  if (!pipeline.design) {
    console.error('ERROR: No design found in current-pipeline.json. Complete Stage 2 first.');
    process.exit(1);
  }
  if (!pipeline.seo) {
    console.error('ERROR: No SEO data found in current-pipeline.json. Complete Stage 3 (SEO) first.');
    process.exit(1);
  }
  design = pipeline.design;
  seo = pipeline.seo;
} else {
  const designFilePath = args.filter(a => a !== '--lang' && a !== lang)[0];
  if (!designFilePath || !fs.existsSync(designFilePath)) {
    console.error('Usage: node scripts/create.js --from-pipeline');
    console.error('       node scripts/create.js <path-to-design.json>');
    process.exit(1);
  }
  design = JSON.parse(fs.readFileSync(designFilePath, 'utf8'));
}

const slug = (seo && seo.slug) || design.slug || 'unknown-skill';
// Read ownerId from env — never hardcode credentials in prompt instructions
const ownerId = process.env.CLAWHUB_OWNER_ID || '<your-clawhub-owner-id>';
const displayName = (seo && seo.displayName) || design.slug || slug;
const fullDescription = (seo && seo.fullDescription) || (design.skillMdOutline && design.skillMdOutline.frontmatter && design.skillMdOutline.frontmatter.description) || '';
const keywords = (seo && seo.keywords) || (design.skillMdOutline && design.skillMdOutline.frontmatter && design.skillMdOutline.frontmatter.keywords) || [];
const skillDir = path.join(outputDir, slug);

const seoNote = seo ? `
SEO OPTIMIZED VALUES (use these in SKILL.md and package.json — DO NOT use design defaults):
  Display name    : ${displayName}
  Tagline         : ${seo.tagline || ''}
  Short desc      : ${seo.shortDescription || ''}
  Full desc       : ${fullDescription}
  Keywords (${keywords.length}): ${keywords.slice(0, 10).join(', ')}${keywords.length > 10 ? ', ...' : ''}
  GitHub desc     : ${seo.githubDescription || ''}
  clawHub title   : ${seo.clawhubTitle || ''}
` : '';

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 4: Create ===
Skill: ${slug}
Output directory: ${skillDir}
${seoNote}
Design reference: ${JSON.stringify(design, null, 2).substring(0, 300)}...

Create every file listed in the design's fileTree. Follow these rules strictly:

CREATION RULES:
1. Create the skill directory at: ${skillDir}
2. For each file in the file tree, write the complete, working file content.
3. SKILL.md:
   - name: use SEO displayName above
   - description: use SEO fullDescription above (multi-line |)
   - keywords: use the full SEO keywords list above
   - metadata with openclaw runtime settings
   - All sections from the design outline
4. Scripts: each script must be a standalone Node.js file. It must print a prompt (console.log) that tells the agent exactly what to do. Include input validation and helpful error messages.
5. package.json: use SEO displayName, shortDescription, and keywords. Include name, version, description, keywords, scripts map.
6. _meta.json: ownerId "${ownerId}", slug, version "1.0.0", publishedAt null.
7. .clawhub/origin.json: same ownerId and slug.
8. data/ files: create with empty arrays or objects as in dataSchemas.

LANGUAGE STANDARDS:
- SKILL.md name, description, all section headings and body text: write in ENGLISH
- Keywords: include both English and Chinese terms (bilingual is fine here)
- Script header comments and usage strings: ENGLISH
- JSON data files: ENGLISH keys and values

QUALITY STANDARDS:
- Every script must have a header comment with filename, purpose, and usage.
- Every script must handle missing args gracefully (print usage + exit 1).
- SKILL.md must have a commands table and a ⚠️ Notes section.
- No placeholder text like "TODO" or "..." in final files.

AFTER CREATING ALL FILES:
- Run: ls -la ${skillDir} to confirm all files exist.
- Update data/current-pipeline.json: add key "create" with { "stage": "create", "skillDir": "${skillDir}", "filesCreated": [...], "completedAt": "<ISO timestamp>" }
- Then proceed to Stage 5: node scripts/review.js ${skillDir}
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 4：制作 ===
Skill：${slug}
输出目录：${skillDir}
${seoNote}
设计参考：${JSON.stringify(design, null, 2).substring(0, 300)}...

按照设计中的 fileTree，逐文件创建所有内容。严格遵守以下规则：

创建规则：
1. 在以下路径创建 skill 目录：${skillDir}
2. 对 fileTree 中的每个文件，写出完整、可运行的文件内容。
3. SKILL.md：
   - name：使用上方 SEO 展示名称
   - description：使用上方 SEO 完整描述（多行 | 格式）
   - keywords：使用上方完整的 SEO 关键词列表
   - metadata 含 openclaw runtime 配置
   - 包含设计大纲中的所有章节
4. 脚本：每个脚本必须是独立的 Node.js 文件，通过 console.log 打印 prompt，包含输入校验和友好错误提示。
5. package.json：使用 SEO 展示名称、简短描述和关键词，包含 name、version、description、keywords、scripts 映射。
6. _meta.json：ownerId "${ownerId}"，slug 来自设计，version "1.0.0"，publishedAt null。
7. .clawhub/origin.json：同样的 ownerId 和 slug。
8. data/ 文件：按 dataSchemas 规格创建空数组或空对象。

语言标准：
- SKILL.md 名称、描述、所有章节标题和正文：统一写英文
- keywords 关键词：中英双语均可
- 脚本头部注释和用法说明：英文
- JSON 数据文件：键和值统一英文

质量标准：
- 每个脚本必须有头部注释（文件名、用途、用法）。
- 每个脚本缺少参数时必须优雅处理（打印用法 + exit 1）。
- SKILL.md 必须包含命令表格和 ⚠️ 注意事项章节。
- 最终文件中不得出现"TODO"或"..."等占位符。

创建所有文件后：
- 运行：ls -la ${skillDir} 确认所有文件存在。
- 更新 data/current-pipeline.json：添加 "create" 键 { "stage": "create", "skillDir": "${skillDir}", "filesCreated": [...], "completedAt": "<ISO 时间戳>" }
- 然后进入阶段 5：node scripts/review.js ${skillDir}
`);
}
