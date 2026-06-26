#!/usr/bin/env node
/**
 * Automatic Skill — Stage 6: Self-Run (自跑)
 * 输出 Agent 执行 prompt，指导其执行新 skill 的每个脚本并验证输出无报错。
 *
 * 用法:
 *   node scripts/self-run.js <skill-dir>
 *   node scripts/self-run.js --from-pipeline
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
  console.error('Usage: node scripts/self-run.js <skill-dir>');
  console.error('       node scripts/self-run.js --from-pipeline');
  process.exit(1);
}

const skillName = path.basename(skillDir);

if (lang === 'en') {
  console.log(`
=== AUTOMATIC SKILL — Stage 6: Self-Run ===
Skill directory: ${skillDir}
Skill name: ${skillName}

Execute every script in the skill and verify the output. Follow these steps:

STEP A — Install dependencies
Run: cd ${skillDir} && npm install
If package.json has no dependencies, skip this step (no error).

STEP B — Enumerate scripts
List all .js files in: ${skillDir}/scripts/
Record their filenames.

STEP C — Run each script
For each script, run it with no arguments first:
  node ${skillDir}/scripts/<script-name>.js

Expected results:
- Scripts that require args: should print a usage message and exit with code 1 (PASS)
- Scripts that work without args: should print a non-empty prompt or result (PASS)
- Any script that crashes (throws uncaught exception, stack trace): FAIL

STEP D — Run scripts with --help or --dry-run if supported
Try: node ${skillDir}/scripts/<script-name>.js --help
     node ${skillDir}/scripts/<script-name>.js --dry-run
These should not crash.

STEP E — Run the main trigger script
Identify the primary script (the one most likely to be the first entry point — usually morning-push.js, daily-push.js, main.js, or the first script listed in package.json scripts).
Run it and confirm it produces readable, non-empty output.

EVALUATION CRITERIA:
✅ PASS: Script runs, exits with 0 or 1, produces meaningful output
⚠️ WARNING: Script exits with unexpected code or produces very short output
❌ FAIL: Script crashes with uncaught exception or stack trace

OUTPUT FORMAT (JSON):
{
  "stage": "self-run",
  "skillDir": "${skillDir}",
  "scriptsRun": [
    { "file": "scripts/xxx.js", "command": "node ...", "exitCode": 0, "outputPreview": "...", "result": "PASS" | "WARNING" | "FAIL", "notes": "..." }
  ],
  "verdict": "PASS" | "FAIL" | "PASS_WITH_WARNINGS",
  "completedAt": "<ISO timestamp>"
}

If verdict is FAIL: fix the crashing scripts, then re-run self-run.
If PASS or PASS_WITH_WARNINGS: proceed to Stage 7: node scripts/self-check.js ${skillDir}

Update data/current-pipeline.json: add "selfRun" key with the report above.
`);
} else {
  console.log(`
=== AUTOMATIC SKILL — 阶段 6：自跑 ===
Skill 目录：${skillDir}
Skill 名称：${skillName}

执行 skill 的每个脚本并验证输出无报错。按以下步骤操作：

步骤 A — 安装依赖
运行：cd ${skillDir} && npm install
如果 package.json 没有依赖，跳过此步骤（不报错）。

步骤 B — 枚举脚本
列出 ${skillDir}/scripts/ 中的所有 .js 文件，记录文件名。

步骤 C — 逐个运行脚本
对每个脚本，先不带参数运行：
  node ${skillDir}/scripts/<脚本名>.js

预期结果：
- 需要参数的脚本：打印用法信息并以 code 1 退出（通过）
- 无需参数即可运行的脚本：打印非空的 prompt 或结果（通过）
- 任何崩溃的脚本（未捕获异常、堆栈追踪）：失败

步骤 D — 带 --help 或 --dry-run 运行（如支持）
尝试：node ${skillDir}/scripts/<脚本名>.js --help
      node ${skillDir}/scripts/<脚本名>.js --dry-run
这些不应该崩溃。

步骤 E — 运行主触发脚本
确定主脚本（最可能是第一入口的脚本 — 通常是 morning-push.js、daily-push.js、main.js，或 package.json scripts 中列出的第一个脚本）。
运行它并确认产出可读的非空输出。

评估标准：
✅ 通过：脚本运行，以 0 或 1 退出，产出有意义的输出
⚠️ 警告：脚本以意外代码退出或产出极短输出
❌ 失败：脚本崩溃，有未捕获异常或堆栈追踪

输出格式（JSON）：
{
  "stage": "self-run",
  "skillDir": "${skillDir}",
  "scriptsRun": [
    { "file": "scripts/xxx.js", "command": "node ...", "exitCode": 0, "outputPreview": "...", "result": "PASS" | "WARNING" | "FAIL", "notes": "..." }
  ],
  "verdict": "PASS" | "FAIL" | "PASS_WITH_WARNINGS",
  "completedAt": "<ISO 时间戳>"
}

如果 verdict 为 FAIL：修复崩溃的脚本，然后重新自跑。
如果 PASS 或 PASS_WITH_WARNINGS：进入阶段 7：node scripts/self-check.js ${skillDir}

更新 data/current-pipeline.json：添加 "selfRun" 键，值为上述报告。
`);
}
