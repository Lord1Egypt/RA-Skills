#!/usr/bin/env node
/**
 * Automatic Skill — Daily Pipeline Entry Point (每日定时入口)
 * 由 openclaw cron 每日 02:00 触发，自动运行全流水线。
 * 包含防重复锁、失败日志、通知推送。
 *
 * 用法:
 *   node scripts/daily-pipeline.js              # 正常运行（由 cron 调用）
 *   node scripts/daily-pipeline.js --dry-run    # 只跑到 self-check，不上传
 *   node scripts/daily-pipeline.js --force      # 忽略锁文件强制运行
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const force = args.includes('--force');

const dataDir = path.join(__dirname, '..', 'data');
const lockPath = path.join(dataDir, 'pipeline.lock');
const pipelinePath = path.join(dataDir, 'current-pipeline.json');
const logPath = path.join(dataDir, 'pipeline-log.json');

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const scriptDir = path.join(__dirname);

// Check lock file to prevent duplicate runs
if (!force && fs.existsSync(lockPath)) {
  const lockData = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
  if (lockData.date === dateISO) {
    console.log(`⏭️  Pipeline already ran today (${dateISO}). Skipping. Use --force to override.`);
    console.log(`   Lock created at: ${lockData.createdAt}`);
    process.exit(0);
  }
}

// Check if a pipeline is already in progress
if (!force && fs.existsSync(pipelinePath)) {
  const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  if (pipeline.date === dateISO) {
    console.log(`⚠️  A pipeline for today is already in progress. Skipping duplicate run.`);
    console.log(`   Use --force to override, or delete data/current-pipeline.json.`);
    process.exit(0);
  }
}

// Write lock
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
fs.writeFileSync(lockPath, JSON.stringify({ date: dateISO, createdAt: now.toISOString() }));

console.log(`
=== AUTOMATIC SKILL — Daily Pipeline (${dateISO}) ===
Mode: ${dryRun ? 'DRY-RUN' : 'FULL'}
Lock created. Starting pipeline...

You are the openclaw daily skill generator. Today's task:
  1. Run the full 9-stage Automatic Skill pipeline (or 6 stages if dry-run)
  2. On success: clean up the lock file at ${lockPath}
  3. On failure: log the error and clean up the lock file

EXECUTION:
Run the pipeline orchestrator now:
  node ${scriptDir}/pipeline.js${dryRun ? ' --dry-run' : ''}

The pipeline will guide you through all stages automatically.

AFTER PIPELINE COMPLETES:
- If SUCCESS: delete the lock file ${lockPath}
- If FAILURE:
    1. Log the error to data/pipeline-log.json with verdict "FAILED"
    2. Delete the lock file ${lockPath}
    3. Send a failure notification (if OPENCLAW_NOTIFY_CHANNEL is set):
       "❌ Daily skill pipeline FAILED on ${dateISO}. Error: <error message>"

ENVIRONMENT CHECKS (run each command to verify before starting):
- GITHUB_TOKEN:      gh auth status   (must show: ✓ Logged in to github.com)
- GITHUB_REPO:       echo $GITHUB_REPO   (must print owner/repo, e.g. myorg/mycli)
- CLAWHUB_TOKEN:     clawhub whoami   (must return your clawHub username without error)
- SKILL_OUTPUT_DIR:  echo ${process.env.SKILL_OUTPUT_DIR || '~/.openclaw/workspace/skills (default)'}
${dryRun ? '\nDRY-RUN: upload stages will be skipped regardless of env vars.' : ''}

START THE PIPELINE: node ${scriptDir}/pipeline.js${dryRun ? ' --dry-run' : ''}
`);
