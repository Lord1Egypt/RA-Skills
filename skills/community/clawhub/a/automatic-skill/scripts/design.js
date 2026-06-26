#!/usr/bin/env node
/**
 * Automatic Skill — Stage 2: Design (设计)
 * 输出 Agent 执行 prompt，指导其为选定创意产出完整的 Skill 架构设计。
 *
 * 用法:
 *   node scripts/design.js <skill-slug-or-idea>
 *   node scripts/design.js --from-pipeline   # 从 data/current-pipeline.json 读取 selected
 *   node scripts/design.js --lang en <skill-slug>
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

let idea = '';
if (args.includes('--from-pipeline')) {
  const pipelinePath = path.join(__dirname, '..', 'data', 'current-pipeline.json');
  if (!fs.existsSync(pipelinePath)) {
    console.error('ERROR: data/current-pipeline.json not found. Run research.js first.');
    process.exit(1);
  }
  const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  const selected = pipeline.selected || (pipeline.research && pipeline.research.selected);
  if (!selected) {
    console.error('ERROR: No selected idea found in current-pipeline.json. Complete Stage 1 first.');
    process.exit(1);
  }
  idea = `${selected.name} (${selected.slug}): ${selected.description}`;
} else {
  idea = args.filter(a => a !== '--lang' && a !== lang).join(' ');
  if (!idea) {
    console.error('Usage: node scripts/design.js <skill-idea-or-slug>');
    console.error('       node scripts/design.js --from-pipeline');
    process.exit(1);
  }
}

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 2: Design ===
Skill Idea: ${idea}
Date: ${dateISO}

Design a complete, production-ready openclaw skill for the idea above.

OUTPUT REQUIREMENTS — produce all of the following:

1. SKILL OVERVIEW
   - slug (lowercase, hyphenated)
   - Full name
   - One-paragraph description (for SKILL.md frontmatter)
   - Keywords list (20+ words, mix of Chinese and English)
   - Runtime requirements (Node version, npm packages needed)
   - Environment variables needed (name, required, description)

2. FILE TREE
   List every file the skill needs, e.g.:
   SKILL.md
   package.json
   _meta.json
   .clawhub/origin.json
   data/<filename>.json  (if any persistent data)
   scripts/
     <script-name>.js   (one line per script with its purpose)

3. SCRIPT SPECIFICATIONS
   For each script, provide:
   - Filename
   - Purpose (one sentence)
   - Input: CLI args or flags
   - Output: what console.log prints (prompt text or JSON)
   - Logic: 5-10 bullet points describing the algorithm

4. SKILL.md STRUCTURE
   - Frontmatter fields (name, description, keywords, metadata)
   - Example commands table
   - REQUIRED: the following five sections must appear in this exact order, with real content (not placeholders):

   ## Purpose & Capability
   What this skill is, what it can do, and what it cannot do.
   Must include:
   - One-paragraph explanation of the core concept
   - A table or bullet list of core capabilities
   - A "Does NOT" or "Boundary" section listing explicit non-capabilities

   ## Instruction Scope
   When to use this skill vs. when not to.
   Must include:
   - "In scope" list: example user requests this skill handles
   - "Out of scope" list: requests this skill will NOT handle
   - Behavior when called outside scope (e.g. politely refuse, redirect)

   ## Credentials
   Every credential, token, and env var this skill touches.
   Must include:
   - A table: Action | Credential | Scope (what gets written/read)
   - Explicit "Does NOT" row (no exfiltration, no other accounts)
   - Minimum token scope recommendations
   - If skill needs zero credentials: state "This skill requires no credentials."

   ## Persistence & Privilege
   Every file, cron job, or system-level change this skill makes.
   Must include:
   - Table of paths written to, with trigger condition
   - "Does NOT write" list
   - Privilege level (runs as current user, no sudo needed)
   - How to fully uninstall / revoke (delete files + revoke tokens)

   ## Install Mechanism
   How to install, configure, and verify the skill.
   Must include:
   - Standard install command (clawhub install <slug>)
   - Manual install fallback (cp -r)
   - Verification step (run a script, expect specific output)
   - Post-install env var configuration with example values
   - How to enable/disable any optional scheduled features

5. DATA SCHEMA
   For each data file, provide the JSON schema with example values.

6. CRON SCHEDULE
   If the skill needs scheduled pushes, list cron expressions and their triggers.

OUTPUT FORMAT (JSON, to be appended into data/current-pipeline.json under key "design"):
{
  "stage": "design",
  "idea": "${idea}",
  "slug": "...",
  "fileTree": ["SKILL.md", "package.json", ...],
  "scripts": [
    { "file": "scripts/xxx.js", "purpose": "...", "args": "...", "output": "...", "logic": [] }
  ],
  "skillMdOutline": { "frontmatter": {}, "sections": [] },
  "dataSchemas": {},
  "cronSchedules": [],
  "completedAt": "<ISO timestamp>"
}

Read the existing data/current-pipeline.json, add the "design" key, and save back.
Then proceed to Stage 3: node scripts/create.js --from-pipeline
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 2：设计 ===
Skill 创意：${idea}
日期：${dateISO}

为上述创意设计一个完整的、可投入生产的 openclaw skill。

输出要求 — 产出以下全部内容：

1. SKILL 概要
   - slug（小写，短横线分隔）
   - 全名
   - 一段描述（用于 SKILL.md frontmatter）
   - 关键词列表（20+ 词，中英混合）
   - 运行环境需求（Node 版本、所需 npm 包）
   - 所需环境变量（名称、是否必填、说明）

2. 文件树
   列出 skill 所需的每个文件，例如：
   SKILL.md
   package.json
   _meta.json
   .clawhub/origin.json
   data/<文件名>.json（如有持久化数据）
   scripts/
     <脚本名>.js（每行一个脚本及其用途）

3. 脚本规格
   对每个脚本，提供：
   - 文件名
   - 用途（一句话）
   - 输入：CLI 参数或 flag
   - 输出：console.log 打印的内容（prompt 文本或 JSON）
   - 逻辑：5-10 条描述算法的要点

4. SKILL.md 结构
   - frontmatter 字段（name, description, keywords, metadata）
   - 示例命令表格
   - 必须包含以下五个章节，按此顺序排列，必须填写真实内容（不得使用占位符）：

   ## Purpose & Capability
   这个 skill 是什么、能做什么、不能做什么。
   必须包含：
   - 一段核心概念说明
   - 核心能力表格或列表
   - "能力边界"/"Does NOT" 章节，明确列出不做的事

   ## Instruction Scope
   何时使用，何时不应使用。
   必须包含：
   - "在 scope 内" 列表：举例用户会说的请求
   - "不在 scope 内" 列表：明确拒绝的请求类型
   - 凭证缺失时的行为说明

   ## Credentials
   这个 skill 涉及的所有凭证、token、env var。
   必须包含：
   - 表格：操作 | 使用的凭证 | 写入/读取范围
   - "不做的事"行（不外传凭证、不访问其他账号）
   - 最小 token scope 建议
   - 若 skill 不需要任何凭证：明确写 "本 skill 无需任何凭证"

   ## Persistence & Privilege
   这个 skill 对文件系统、cron、系统的所有写入操作。
   必须包含：
   - 写入路径表格，含触发条件
   - "不写入"列表
   - 权限级别（以当前用户身份运行，无需 sudo）
   - 完整卸载/撤销方法

   ## Install Mechanism
   如何安装、配置、验证。
   必须包含：
   - 标准安装命令（clawhub install <slug>）
   - 手动安装备选方案（cp -r）
   - 验证步骤（运行某个脚本，预期输出）
   - 安装后的 env var 配置示例
   - 可选定时功能的启用/停用方法

5. 数据 Schema
   对每个数据文件，提供带示例值的 JSON schema。

6. Cron 计划
   如果 skill 需要定时推送，列出 cron 表达式及触发器。

输出格式（JSON，追加到 data/current-pipeline.json 的 "design" 键下）：
{
  "stage": "design",
  "idea": "${idea}",
  "slug": "...",
  "fileTree": ["SKILL.md", "package.json", ...],
  "scripts": [
    { "file": "scripts/xxx.js", "purpose": "...", "args": "...", "output": "...", "logic": [] }
  ],
  "skillMdOutline": { "frontmatter": {}, "sections": [] },
  "dataSchemas": {},
  "cronSchedules": [],
  "completedAt": "<ISO 时间戳>"
}

读取现有的 data/current-pipeline.json，添加 "design" 键后保存回去。
然后进入阶段 3：node scripts/create.js --from-pipeline
`);
}
