#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Paths
const WORKSPACE = path.resolve(__dirname, '..');
const ENV_PATH = path.join(WORKSPACE, '.env');
const SESSION_LOG_PATH = path.join(WORKSPACE, 'memory', 'session-posts.json');
const LEAGUE_STATE_PATH = path.join(WORKSPACE, 'memory', 'league-state.json');
const POSTS_LOG_PATH = path.join(WORKSPACE, 'memory', 'league-posts.json');

// Ensure directories exist
[path.dirname(LEAGUE_STATE_PATH), path.dirname(POSTS_LOG_PATH)].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Load environment
function loadEnv() {
  const content = fs.readFileSync(ENV_PATH, 'utf8');
  const env = {};
  content.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#')) return;
    const idx = line.indexOf('=');
    if (idx > 0) env[line.substring(0, idx).trim()] = line.substring(idx + 1).trim();
  });
  return env;
}
const env = loadEnv();
const MOLTBOOK_API_KEY = env.MOLTBOOK_API_KEY;
if (!MOLTBOOK_API_KEY) {
  console.error('MOLTBOOK_API_KEY not set in .env');
  process.exit(1);
}

// ----- League State -----
function loadLeagueState() {
  if (!fs.existsSync(LEAGUE_STATE_PATH)) {
    return { sessions: [], lastPostDate: null };
  }
  return JSON.parse(fs.readFileSync(LEAGUE_STATE_PATH, 'utf8'));
}

function saveLeagueState(state) {
  fs.writeFileSync(LEAGUE_STATE_PATH, JSON.stringify(state, null, 2));
}

// Parse session log to extract Saturday sessions
function getSaturdaySessions() {
  if (!fs.existsSync(SESSION_LOG_PATH)) return [];
  const log = JSON.parse(fs.readFileSync(SESSION_LOG_PATH, 'utf8'));
  // Filter to Saturday battles (type 'battle' or title pattern)
  return log.filter(entry => {
    const day = new Date(entry.timestamp).getDay();
    return day === 6; // Saturday
  });
}

// Metrics calculation
function calculateMetrics(sessions) {
  const metrics = sessions.map(s => {
    const content = s.content || '';
    const moves = content.split(/[,\n]/).filter(Boolean);
    const uniqueMoves = new Set(moves.map(m => m.replace(/\s*\(\d+(\.\d+)?\)/g, '').trim())).size;

    // Simple completeness score
    const hasKillOff = /kill\s*off/i.test(content);
    const conceptsCount = (content.match(/\b(Textures|Zones|In-Between|Focus Point|Storytelling|Musicality|Combo|Character)\b/gi) || []).length;
    const powerCount = (content.match(/\b(Smash|Snatch|Whip|Spazz|Wobble|Rumble|Get Off)\b/gi) || []).length;

    return {
      date: new Date(s.timestamp).toLocaleDateString('en-GB'),
      moveCount: moves.length,
      uniqueMoves,
      hasKillOff,
      conceptsCount,
      powerCount,
      completeness: (moves.length / 32) * 100 + uniqueMoves * 2 + (hasKillOff ? 10 : 0) + conceptsCount * 3 + powerCount * 2,
      rawContent: content
    };
  });

  return metrics;
}

// Generate weekly summary report
function generateWeeklyReport(allMetrics, weekStart) {
  const weekSessions = allMetrics.filter(m => {
    const d = new Date(m.date);
    const day = d.getDay();
    const diff = (d - weekStart) / (1000 * 60 * 60 * 24);
    return diff >= 0 && diff < 7;
  });

  if (weekSessions.length === 0) return null;

  const avgCompleteness = weekSessions.reduce((sum, m) => sum + m.completeness, 0) / weekSessions.length;
  const topSession = weekSessions.reduce((best, cur) => cur.completeness > best.completeness ? cur : best, weekSessions[0]);

  let report = '## Krump League Performance Summary\n\n';
  report += `**Week of ${weekStart.toLocaleDateString('en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}**\n\n`;
  report += `- Sessions this week: ${weekSessions.length}\n`;
  report += `- Avg. completeness score: ${avgCompleteness.toFixed(1)}\n`;
  report += `- Top session: ${topSession.date} (${topSession.moveCount} moves, ${topSession.uniqueMoves} unique, completeness ${topSession.completeness.toFixed(1)})\n\n`;

  report += '### Progress Tracker\n';
  report += '| Week | Sessions | Avg Completeness | Trend |\n';
  report += '|------|----------|------------------|-------|\n';

  // Group by week
  const weeks = {};
  allMetrics.forEach(m => {
    const d = new Date(m.date);
    // Sunday-based week start
    const weekStartDate = new Date(d);
    const day = d.getDay();
    weekStartDate.setDate(d.getDate() - day);
    const weekKey = weekStartDate.toISOString().split('T')[0];
    if (!weeks[weekKey]) weeks[weekKey] = [];
    weeks[weekKey].push(m);
  });

  const sortedWeeks = Object.keys(weeks).sort().slice(-6); // last 6 weeks
  sortedWeeks.forEach(weekKey => {
    const weekData = weeks[weekKey];
    const weekStart = new Date(weekKey);
    const avg = weekData.reduce((sum, m) => sum + m.completeness, 0) / weekData.length;
    // Simple trend: compare to previous week
    const prevIdx = sortedWeeks.indexOf(weekKey) - 1;
    let trend = '—';
    if (prevIdx >= 0) {
      const prevWeekKey = sortedWeeks[prevIdx];
      const prevAvg = weeks[prevWeekKey].reduce((sum, m) => sum + m.completeness, 0) / weeks[prevWeekKey].length;
      trend = avg > prevAvg ? '📈' : avg < prevAvg ? '📉' : '➡️';
    }
    report += `| ${weekStart.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' })} | ${weekData.length} | ${avg.toFixed(1)} | ${trend} |\n`;
  });

  report += `\n*Report generated: ${new Date().toLocaleString('en-GB', { timeZone: 'Europe/London' })}*`;
  return report;
}

// Post to Moltbook (krumpclaw submolt)
function postToMoltbook(title, content) {
  const payload = {
    subdomain: 'krumpclaw',
    title,
    content,
    verification_required: false
  };
  const cmd = `curl -s -X POST https://moltbook.com/api/posts/create \\\n    -H 'Authorization: Bearer ${MOLTBOOK_API_KEY}' \\\n    -H 'Content-Type: application/json' \\\n    -d '${JSON.stringify(payload)}'`;
  const response = execSync(cmd).toString();
  const parsed = JSON.parse(response);
  if (parsed.error) throw new Error(`Moltbook error: ${parsed.error}`);
  return parsed;
}

// Main: Run weekly on Sunday to post summary
async function main() {
  const state = loadLeagueState();
  const today = new Date();
  const todayStr = today.toISOString().split('T')[0];

  // Only post once per week (Sunday)
  if (state.lastPostDate && state.lastPostDate === todayStr) {
    console.log('Weekly league summary already posted today.');
    process.exit(0);
  }

  // Load all Saturday sessions from session log
  const saturdays = getSaturdaySessions();
  if (saturdays.length === 0) {
    console.log('No Saturday sessions recorded yet.');
    process.exit(0);
  }

  // Compute metrics
  const metrics = calculateMetrics(saturdays);

  // Determine week start (last Sunday)
  const day = today.getDay();
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - day);

  const report = generateWeeklyReport(metrics, weekStart);
  if (!report) {
    console.log('No data for this week.');
    process.exit(0);
  }

  const title = `[Krump League] Weekly Performance - Week of ${weekStart.toLocaleDateString('en-GB', { month: 'long', day: 'numeric', year: 'numeric' })}`;
  console.log('Posting weekly league summary to krumpclaw...');
  const postResponse = postToMoltbook(title, report);
  console.log('Posted successfully:', postResponse.post?.id || postResponse.content_id);

  // Update state
  state.lastPostDate = todayStr;
  saveLeagueState(state);

  // Log
  const log = fs.existsSync(POSTS_LOG_PATH) ? JSON.parse(fs.readFileSync(POSTS_LOG_PATH, 'utf8')) : [];
  log.push({
    timestamp: new Date().toISOString(),
    type: 'weekly-summary',
    postId: postResponse.post?.id || postResponse.content_id,
    title,
    sessionsCount: saturdays.length
  });
  fs.writeFileSync(POSTS_LOG_PATH, JSON.stringify(log, null, 2));

  console.log('Weekly league summary posted.');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});

