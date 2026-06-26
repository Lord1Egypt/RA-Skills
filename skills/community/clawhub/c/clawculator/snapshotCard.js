'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Generate a shareable cost snapshot card.
 * Square format — works on Twitter, Instagram, TikTok, Discord.
 * Shows grade, cost range, setup complexity — no exact dollars or session names.
 */
function generateSnapshotCard(analysis, outputDir) {
  const s = analysis.summary;

  // ── Compute grade ──────────────────────────────────────
  const criticals = s.critical || 0;
  const highs = s.high || 0;
  const mediums = s.medium || 0;
  const totalFindings = criticals + highs + mediums;

  // ── Filter findings by type ────────────────────────────
  // For the grade, only count CONFIG findings (things a new user would inherit)
  // Exclude: historical session costs, untracked sessions, cache totals, cost gaps
  // These are noise for "what does it cost to run this setup?"
  const configFindings = (analysis.findings || []).filter(f => {
    const t = (f.title || '').toLowerCase();
    const src = (f.source || '').toLowerCase();
    // Skip historical/session findings
    if (t.includes('orphaned session')) return false;
    if (t.includes('untracked session')) return false;
    if (t.includes('prompt caching added')) return false;
    if (t.includes('real cost') && t.includes('higher than')) return false;
    if (t.includes('>50k tokens')) return false;
    if (t.includes('pricing table')) return false;
    // Keep config findings (heartbeat, whatsapp, hooks, crons, models, vision, memory)
    return true;
  });

  const cfgCriticals = configFindings.filter(f => f.severity === 'critical').length;
  const cfgHighs = configFindings.filter(f => f.severity === 'high').length;
  const cfgMediums = configFindings.filter(f => f.severity === 'medium').length;

  // ── Cost range (bucketed, not exact) ───────────────────
  const todayCost = s.todayCost || 0;
  let costRange, costEmoji;
  if (todayCost === 0)       { costRange = 'Free tier';     costEmoji = '🆓'; }
  else if (todayCost < 0.50) { costRange = 'Under $0.50/day'; costEmoji = '💲'; }
  else if (todayCost < 1)    { costRange = 'Under $1/day';  costEmoji = '💲'; }
  else if (todayCost < 5)    { costRange = '$1–5/day';      costEmoji = '💵'; }
  else if (todayCost < 10)   { costRange = '$5–10/day';     costEmoji = '💰'; }
  else if (todayCost < 25)   { costRange = '$10–25/day';    costEmoji = '💰'; }
  else if (todayCost < 50)   { costRange = '$25–50/day';    costEmoji = '🔥'; }
  else                       { costRange = '$50+/day';      costEmoji = '🚨'; }

  // ── Compute grade ──────────────────────────────────────
  // Grade = "how well is this SETUP configured for cost efficiency?"
  // Only counts config findings, not historical session data
  let grade, gradeColor, gradeGlow, gradeEmoji;

  let score = (cfgCriticals * 5) + (cfgHighs * 2) + (cfgMediums * 0.5);

  // Cost bonus: low daily spend is the whole point
  if (todayCost < 1)       score -= 4;
  else if (todayCost < 5)  score -= 3;
  else if (todayCost < 10) score -= 1;
  else if (todayCost > 50) score += 3;

  // No criticals bonus
  if (cfgCriticals === 0) score -= 2;

  if (score < 0) score = 0;

  if (score === 0) {
    grade = 'A+'; gradeColor = '#22c55e'; gradeGlow = 'rgba(34,197,94,0.3)'; gradeEmoji = '🏆';
  } else if (score <= 2) {
    grade = 'A'; gradeColor = '#22c55e'; gradeGlow = 'rgba(34,197,94,0.2)'; gradeEmoji = '✅';
  } else if (score <= 5) {
    grade = 'B+'; gradeColor = '#84cc16'; gradeGlow = 'rgba(132,204,22,0.2)'; gradeEmoji = '👍';
  } else if (score <= 8) {
    grade = 'B'; gradeColor = '#f59e0b'; gradeGlow = 'rgba(245,158,11,0.2)'; gradeEmoji = '👍';
  } else if (score <= 12) {
    grade = 'C'; gradeColor = '#f97316'; gradeGlow = 'rgba(249,115,22,0.2)'; gradeEmoji = '⚠️';
  } else {
    grade = 'D'; gradeColor = '#ef4444'; gradeGlow = 'rgba(239,68,68,0.2)'; gradeEmoji = '🔥';
  }

  // ── Setup complexity from config ───────────────────────
  const config = analysis.config || {};

  const channels = [];
  if (config.channels?.whatsapp) channels.push('WhatsApp');
  if (config.channels?.telegram) channels.push('Telegram');
  if (config.channels?.discord)  channels.push('Discord');
  if (config.channels?.signal)   channels.push('Signal');
  if (config.channels?.slack)    channels.push('Slack');
  if (config.webchat || config.channels?.webchat) channels.push('Webchat');

  const skillCount = config.skills ? Object.keys(config.skills).length : 0;
  const cronCount = config.cron ? Object.keys(config.cron).length : 0;
  const hookCount = config.hooks ? Object.keys(config.hooks).length : 0;
  const agentCount = config.agents?.list ? Object.keys(config.agents.list).length : 1;
  const sessionCount = s.sessionsAnalyzed || 0;

  const modelSet = new Set();
  for (const sess of (analysis.sessions || [])) {
    if (sess.model || sess.modelLabel) modelSet.add(sess.modelLabel || sess.model);
  }
  const modelCount = modelSet.size || 1;

  const totalTokens = s.totalTokensFound || 1;
  const totalWithCache = totalTokens + (s.totalCacheRead || 0) + (s.totalCacheWrite || 0);
  const cacheEfficiency = Math.min(99, Math.round((s.totalCacheRead || 0) / totalWithCache * 100));

  // ── Build stat pills ──────────────────────────────────
  const pills = [];
  if (channels.length > 0)  pills.push({ icon: '📱', label: `${channels.length} channel${channels.length>1?'s':''}` });
  if (skillCount > 0)       pills.push({ icon: '🔧', label: `${skillCount} skill${skillCount>1?'s':''}` });
  if (cronCount > 0)        pills.push({ icon: '⏰', label: `${cronCount} cron${cronCount>1?'s':''}` });
  if (hookCount > 0)        pills.push({ icon: '🪝', label: `${hookCount} hook${hookCount>1?'s':''}` });
  if (agentCount > 1)       pills.push({ icon: '🤖', label: `${agentCount} agents` });
  if (sessionCount > 0)     pills.push({ icon: '💬', label: `${sessionCount} sessions` });
  pills.push({ icon: '🧠', label: `${modelCount} model${modelCount>1?'s':''}` });
  if (cacheEfficiency > 0)  pills.push({ icon: '⚡', label: `${cacheEfficiency}% cache` });

  // ── Findings summary (config only) ─────────────────────
  const findingSummary = [];
  if (cfgCriticals > 0) findingSummary.push(`🔴 ${cfgCriticals} critical`);
  if (cfgHighs > 0)     findingSummary.push(`🟠 ${cfgHighs} high`);
  if (cfgMediums > 0)   findingSummary.push(`🟡 ${cfgMediums} medium`);

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clawculator Snapshot</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  html, body {
    min-height: 100vh;
    font-family: 'Outfit', sans-serif;
    background: #020408;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card {
    width: 480px; max-width: 96vw;
    background: #05080f;
    border-radius: 24px;
    border: 1px solid #1a2744;
    padding: 32px 28px 24px;
    display: flex; flex-direction: column;
    align-items: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px rgba(34,211,238,0.04), 0 20px 60px rgba(0,0,0,0.5);
  }

  /* Grid bg */
  .card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background:
      linear-gradient(rgba(34,211,238,0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(34,211,238,0.02) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
  }

  .card > * { position: relative; z-index: 1; }

  /* Header */
  .header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px;
  }
  .logo-claw { font-size: 28px; }
  .logo-text {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800; font-size: 18px; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #22d3ee, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }

  /* Grade */
  .grade-container {
    display: flex; flex-direction: column; align-items: center;
    margin-bottom: 16px;
  }
  .grade-ring {
    width: 120px; height: 120px;
    border-radius: 50%;
    border: 3px solid ${gradeColor}44;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 40px ${gradeGlow}, inset 0 0 20px ${gradeGlow};
    position: relative;
  }
  .grade-ring::before {
    content: '';
    position: absolute; inset: -2px;
    border-radius: 50%;
    border: 2px solid ${gradeColor};
    opacity: 0.5;
  }
  .grade-letter {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 900; font-size: 52px;
    color: ${gradeColor};
    text-shadow: 0 0 20px ${gradeGlow};
    line-height: 1;
  }
  .grade-label {
    font-size: 11px; font-weight: 600; color: #64748b;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-top: 8px;
  }

  /* Cost */
  .cost-range {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700; font-size: 22px;
    color: #e2e8f0;
    margin-bottom: 14px;
    text-align: center;
  }

  /* Divider */
  .divider {
    width: 60px; height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, transparent);
    margin-bottom: 14px;
  }

  /* Pills */
  .pills {
    display: flex; flex-wrap: wrap; justify-content: center;
    gap: 6px;
    margin-bottom: 14px;
    max-width: 400px;
  }
  .pill {
    display: flex; align-items: center; gap: 4px;
    background: #0b1120;
    border: 1px solid #1a2744;
    border-radius: 14px;
    padding: 5px 12px;
    font-size: 12px; font-weight: 500;
    color: #94a3b8;
  }

  /* Findings */
  .findings {
    text-align: center;
    margin-bottom: 14px;
  }
  .findings-badges {
    display: flex; justify-content: center; gap: 8px;
    flex-wrap: wrap;
  }
  .findings-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; font-weight: 600;
    padding: 4px 10px; border-radius: 6px;
  }
  .findings-clean {
    font-size: 14px; color: #22c55e; font-weight: 600;
  }

  /* CTA */
  .cta {
    margin-top: auto;
    text-align: center;
    width: 100%;
  }
  .cta-divider {
    width: 100%; height: 1px;
    background: linear-gradient(90deg, transparent, #1a2744, transparent);
    margin-bottom: 14px;
  }
  .cta-prompt {
    font-size: 13px; color: #64748b;
    margin-bottom: 8px;
  }
  .cta-command {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; font-weight: 700;
    color: #22d3ee;
    background: #0b1120;
    border: 1px solid #1a2744;
    border-radius: 8px;
    padding: 10px 18px;
    display: inline-block;
    margin-bottom: 6px;
  }
  .cta-sub {
    font-size: 10px; color: #334155;
  }
</style>
</head>
<body>
<div class="card">

  <div class="header">
    <div class="logo-claw">🦞</div>
    <div class="logo-text">CLAWCULATOR</div>
  </div>

  <div class="grade-container">
    <div class="grade-ring">
      <div class="grade-letter">${grade}</div>
    </div>
    <div class="grade-label">${gradeEmoji} cost health</div>
  </div>

  <div class="cost-range">${costEmoji} ${costRange}</div>

  <div class="divider"></div>

  <div class="pills">
    ${pills.map(p => `<div class="pill"><span>${p.icon}</span>${p.label}</div>`).join('\n    ')}
  </div>

  <div class="findings">
    ${findingSummary.length > 0 ?
      `<div class="findings-badges">${findingSummary.map(f => {
        const c = f.startsWith('🔴') ? '#ef4444' : f.startsWith('🟠') ? '#f97316' : '#eab308';
        return `<div class="findings-badge" style="background:${c}18;color:${c}">${f}</div>`;
      }).join('')}</div>` :
      `<div class="findings-clean">✅ No issues found</div>`
    }
  </div>

  <div class="cta">
    <div class="cta-divider"></div>
    <div class="cta-prompt">Get your OpenClaw cost grade</div>
    <div class="cta-command">npx clawculator --snapshot</div>
    <div class="cta-sub">100% offline · your data never leaves your machine</div>
  </div>

</div>
</body>
</html>`;

  const htmlPath = path.join(outputDir, 'clawculator-snapshot.html');
  fs.writeFileSync(htmlPath, html, 'utf8');

  // ── Terminal card (screenshot-ready) ───────────────────
  const C = '\x1b[36m';   // cyan
  const G = gradeColor === '#22c55e' ? '\x1b[32m' : gradeColor === '#f59e0b' ? '\x1b[33m' : gradeColor === '#f97316' ? '\x1b[33m' : '\x1b[31m';
  const D = '\x1b[90m';   // dim
  const B = '\x1b[1m';    // bold
  const R = '\x1b[0m';    // reset
  const W = '\x1b[37m';   // white

  const pillStr = pills.map(p => `${p.icon} ${p.label}`).join('  ');
  const findStr = findingSummary.length > 0
    ? findingSummary.join('  ')
    : '✅ No issues found';

  const lines = [
    ``,
    `${D}  ╔══════════════════════════════════════════════╗${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}       ${C}🦞  C L A W C U L A T O R${R}            ${D}║${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}              ${G}${B}┌─────────┐${R}                  ${D}║${R}`,
    `${D}  ║${R}              ${G}${B}│  ${grade.padStart(3)}    │${R}                  ${D}║${R}`,
    `${D}  ║${R}              ${G}${B}└─────────┘${R}                  ${D}║${R}`,
    `${D}  ║${R}           ${D}cost health grade${R}                ${D}║${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}        ${W}${B}${costEmoji} ${costRange}${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}  ${D}──────────────────────────────────────────${R}  ${D}║${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}  ${pillStr}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}  ${findStr}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}  ${D}──────────────────────────────────────────${R}  ${D}║${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ║${R}     ${D}Get your OpenClaw cost grade${R}            ${D}║${R}`,
    `${D}  ║${R}     ${C}${B}npx clawculator --snapshot${R}             ${D}║${R}`,
    `${D}  ║${R}                                              ${D}║${R}`,
    `${D}  ╚══════════════════════════════════════════════╝${R}`,
    ``,
  ];

  console.log(lines.join('\n'));

  // Also mention the HTML file
  console.log(`  ${D}HTML card saved: ${htmlPath}${R}`);
  console.log(`  ${D}Screenshot this terminal or open the HTML — both work!${R}\n`);

  return { htmlPath, grade, costRange };
}

module.exports = { generateSnapshotCard };
