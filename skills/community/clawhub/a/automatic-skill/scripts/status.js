#!/usr/bin/env node
/**
 * Automatic Skill — Status (状态查询)
 * 查看当前流水线状态或历史记录。
 *
 * 用法:
 *   node scripts/status.js                  # 当前流水线状态
 *   node scripts/status.js --history        # 最近 10 次记录
 *   node scripts/status.js --history 20     # 最近 20 次
 *   node scripts/status.js --clear          # 清除当前流水线状态
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dataDir = path.join(__dirname, '..', 'data');
const pipelinePath = path.join(dataDir, 'current-pipeline.json');
const logPath = path.join(dataDir, 'pipeline-log.json');

const STAGE_NAMES = {
  research: '1. Research (调研)',
  design: '2. Design (设计)',
  create: '3. Create (制作)',
  review: '4. Review (审核)',
  selfRun: '5. Self-Run (自跑)',
  selfCheck: '6. Self-Check (自检)',
  upload: '7. Upload (上传)',
  verifyUpload: '8. Verify (验收)',
  finalReview: '9. Final Review (复查)',
};

// Handle --clear
if (args.includes('--clear')) {
  if (fs.existsSync(pipelinePath)) {
    fs.unlinkSync(pipelinePath);
    console.log('✅ Current pipeline state cleared.');
  } else {
    console.log('ℹ️  No current pipeline state to clear.');
  }
  const lockPath = path.join(dataDir, 'pipeline.lock');
  if (fs.existsSync(lockPath)) {
    fs.unlinkSync(lockPath);
    console.log('✅ Lock file cleared.');
  }
  process.exit(0);
}

// Handle --history
if (args.includes('--history')) {
  const nIdx = args.indexOf('--history');
  const n = parseInt(args[nIdx + 1], 10) || 10;

  if (!fs.existsSync(logPath)) {
    console.log('📋 No pipeline history found.');
    process.exit(0);
  }

  const log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
  const recent = log.slice(-n).reverse();

  console.log(`\n📋 Pipeline History (last ${recent.length} runs)\n`);
  console.log('Date         Skill                    Review  Check   GitHub     clawHub    Verdict');
  console.log('──────────── ──────────────────────── ─────── ─────── ────────── ────────── ────────────');

  for (const entry of recent) {
    const date = (entry.date || '').substring(0, 10).padEnd(12);
    const slug = (entry.slug || '').substring(0, 24).padEnd(24);
    const reviewScore = String(entry.reviewScore || '-').padEnd(7);
    const checkScore = String(entry.selfCheckScore || '-').padEnd(7);
    const github = (entry.githubStatus || '-').padEnd(10);
    const clawhub = (entry.clawhubStatus || '-').padEnd(10);
    const verdict = entry.verdict || '-';
    console.log(`${date} ${slug} ${reviewScore} ${checkScore} ${github} ${clawhub} ${verdict}`);
  }
  console.log('');
  process.exit(0);
}

// Default: show current pipeline status
if (!fs.existsSync(pipelinePath)) {
  console.log('\n📊 Automatic Skill — Pipeline Status');
  console.log('─────────────────────────────────────');
  console.log('Status: IDLE (no pipeline in progress)');
  console.log('');

  if (fs.existsSync(logPath)) {
    const log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    if (log.length > 0) {
      const last = log[log.length - 1];
      console.log(`Last run: ${last.date} — ${last.slug} — ${last.verdict}`);
    }
  }

  console.log('\nRun: node scripts/pipeline.js    to start a new pipeline');
  console.log('Run: node scripts/status.js --history    to view history\n');
  process.exit(0);
}

const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
const completedStages = Object.keys(STAGE_NAMES).filter(k => pipeline[k]);
const pendingStages = Object.keys(STAGE_NAMES).filter(k => !pipeline[k]);
const currentStage = pendingStages.length > 0 ? pendingStages[0] : 'complete';

console.log('\n📊 Automatic Skill — Pipeline Status');
console.log('─────────────────────────────────────');
console.log(`Date:    ${pipeline.research && pipeline.research.date || pipeline.design && pipeline.design.date || 'unknown'}`);
console.log(`Skill:   ${pipeline.design && pipeline.design.slug || '(not yet selected)'}`);
console.log(`Current: ${currentStage === 'complete' ? '✅ COMPLETE' : STAGE_NAMES[currentStage] || currentStage}`);
console.log('');

console.log('Stages:');
for (const [key, name] of Object.entries(STAGE_NAMES)) {
  const done = !!pipeline[key];
  const score = key === 'review' && pipeline[key] && pipeline[key].score !== undefined
    ? ` (score: ${pipeline[key].score})` : '';
  const verdict = pipeline[key] && pipeline[key].verdict ? ` — ${pipeline[key].verdict}` : '';
  console.log(`  ${done ? '✅' : '⏳'} ${name}${score}${verdict}`);
}

console.log('');
if (currentStage !== 'complete') {
  const nextScript = {
    research: 'research.js',
    design: 'design.js --from-pipeline',
    create: 'create.js --from-pipeline',
    review: 'review.js --from-pipeline',
    selfRun: 'self-run.js --from-pipeline',
    selfCheck: 'self-check.js --from-pipeline',
    upload: 'upload.js --from-pipeline',
    verifyUpload: 'verify-upload.js --from-pipeline',
    finalReview: 'final-review.js --from-pipeline',
  }[currentStage];
  console.log(`Next step: node scripts/${nextScript}`);
} else {
  console.log('Pipeline is complete. Run: node scripts/pipeline.js to start a new one.');
}
console.log('');
