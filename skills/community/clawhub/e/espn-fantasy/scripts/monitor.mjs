// ESPN Fantasy monitor — runs on a systemd timer. NO LLM. Only appends NEW events to
// state/espn-alerts.jsonl (diffed via state/espn-seen.json). Quiet = no output.
import fs from 'fs';
import path from 'path';

const WS = path.join(process.env.HOME, '.openclaw/workspace');
const ST = path.join(WS, 'state');
const COOKIES = path.join(WS, '.secrets/espn-cookies.txt');
const SEEN = path.join(ST, 'espn-seen.json');
const ALERTS = path.join(ST, 'espn-alerts.jsonl');
const LOG = path.join(ST, 'espn-monitor.log');
const LEAGUE = 1943401863, SEASON = 2026, TEAM = 3;
const log = m => fs.appendFileSync(LOG, `[${new Date().toISOString()}] ${m}\n`);

function headers() {
  const t = fs.readFileSync(COOKIES, 'utf8');
  const s2 = (t.match(/^espn_s2=(.+)$/m) || [])[1].trim();
  const swid = (t.match(/^SWID=(.+)$/m) || [])[1].trim();
  return { 'Cookie': `espn_s2=${s2}; SWID=${swid}`, 'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' };
}
const base = `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/${SEASON}/segments/0/leagues/${LEAGUE}`;
const get = async (q) => (await fetch(base + q, { headers: headers() })).json();
const load = (p, d) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return d; } };

async function main() {
  const seen = load(SEEN, { txnIds: [], inj: {}, pend: [] });
  const seenTxn = new Set(seen.txnIds), seenPend = new Set(seen.pend);
  const seenInj = seen.inj || {};
  const alerts = [];

  const status = await get('?view=mStatus');
  const wk = status?.status?.latestScoringPeriod || status?.scoringPeriodId || 4;

  const j = await get(`?view=mTransactions2&view=mRoster&view=mTeam&scoringPeriodId=${wk}`);
  const teams = Object.fromEntries((j.teams || []).map(t => [t.id, t.name]));
  const pos = { 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST' };

  // 1) pending trade proposals (any), especially involving me
  for (const x of (j.transactions || [])) {
    if (!/TRADE/.test(x.type)) continue;
    if (!x.isPending && x.status !== 'PENDING') continue;
    const k = String(x.id);
    if (seenPend.has(k)) continue;
    seenPend.add(k);
    const legs = (x.items || []).map(i => `${i.type}:${i.playerId}(${teams[i.fromTeamId] || i.fromTeamId}→${teams[i.toTeamId] || i.toTeamId})`).join(' ');
    const mine = x.teamId === TEAM || (x.items || []).some(i => i.fromTeamId === TEAM || i.toTeamId === TEAM);
    alerts.push({ kind: mine ? 'TRADE_TO_ME' : 'TRADE_PENDING', msg: `${mine ? '🚨 TRADE INVOLVING YOU' : 'League trade pending'}: ${teams[x.teamId] || x.teamId} :: ${legs} (exp ${x.expirationDate ? new Date(x.expirationDate).toISOString() : '?'})` });
  }

  // 2) new executed transactions (waivers, FA adds/drops, completed trades)
  for (const x of (j.transactions || [])) {
    const k = String(x.id);
    if (seenTxn.has(k)) continue;
    seenTxn.add(k);
    if (x.isPending || x.status === 'PENDING') continue;
    if (!['EXECUTED', 'TRADE_ACCEPT', 'WAIVER', 'FREEAGENT', 'ROSTER'].includes(x.type) && !/TRADE/.test(x.type)) continue;
    const legs = (x.items || []).map(i => {
      const pl = null;
      return `${i.type} ${i.playerId}`;
    }).join(' ');
    const notable = x.teamId === TEAM || /TRADE/.test(x.type) || /WAIVER/.test(x.type);
    if (notable) alerts.push({ kind: x.teamId === TEAM ? 'MY_ACTIVITY' : (x.type || 'TXN'), msg: `${x.type} (${teams[x.teamId] || x.teamId}): ${legs}` });
  }

  // 3) injury status changes on MY roster
  const my = (j.teams || []).find(t => t.id === TEAM);
  for (const e of (my?.roster?.entries || [])) {
    const p = e.playerPoolEntry?.player || {};
    const s = p.injuryStatus || 'ACTIVE';
    const prev = seenInj[p.id];
    if (prev !== undefined && prev !== s) alerts.push({ kind: 'MY_INJURY', msg: `⚠️ ${p.fullName}: ${prev} → ${s}` });
    seenInj[p.id] = s;
  }

  if (alerts.length) {
    const lines = alerts.map(a => JSON.stringify({ ts: Date.now(), ...a })).join('\n') + '\n';
    fs.appendFileSync(ALERTS, lines);
    log(`wrote ${alerts.length} alert(s)`);
  } else { log('no new events'); }

  fs.writeFileSync(SEEN, JSON.stringify({ txnIds: [...seenTxn].slice(-800), pend: [...seenPend].slice(-200), inj: seenInj, updated: Date.now() }));
}

main().catch(e => log('ERROR ' + e.message));
