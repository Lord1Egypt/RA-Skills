// ESPN Fantasy WRITE helper — lineups, add/drop, quick lineup.
// Verified 2026-10-01. Key: bare transaction object (NO {transactions:[]} wrapper, NO memberId)
// + header x-fantasy-platform: espn-fantasy-web.
//
// Usage (as a module):
//   import { setLineup, addDrop, quickLineup } from './tx.mjs';
//   await addDrop({season, leagueId, teamId, addId, dropId, week});
//
// Cookies are read from .secrets/espn-cookies.txt (espn_s2 + SWID), root-only.
import fs from 'fs';
import path from 'path';

const COOKIES = process.env.ESPN_COOKIES || path.join(process.env.HOME, '.openclaw/workspace/.secrets/espn-cookies.txt');

function headers() {
  const t = fs.readFileSync(COOKIES, 'utf8');
  const s2 = (t.match(/^espn_s2=(.+)$/m) || [])[1].trim();
  const swid = (t.match(/^SWID=(.+)$/m) || [])[1].trim();
  return {
    'Cookie': `espn_s2=${s2}; SWID=${swid}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-fantasy-source': 'kona',
    'x-fantasy-platform': 'espn-fantasy-web',
    'Referer': 'https://fantasy.espn.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  };
}

const txUrl = (season, leagueId) =>
  `https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/${season}/segments/0/leagues/${leagueId}/transactions/`;

async function post(url, body, label) {
  const r = await fetch(url, { method: 'POST', headers: headers(), body: JSON.stringify(body) });
  const txt = await r.text();
  return { ok: r.status === 200, status: r.status, body: txt.slice(0, 400), label };
}

// Add a player, drop another (pair them — a bare ADD fails if the roster is full).
export async function addDrop({ season, leagueId, teamId, addId, dropId, week }) {
  const items = [{ playerId: addId, type: 'ADD', toTeamId: teamId }];
  if (dropId) items.push({ playerId: dropId, type: 'DROP', fromTeamId: teamId });
  return post(txUrl(season, leagueId), {
    isLeagueManager: false, teamId, type: 'FREEAGENT', scoringPeriodId: week, executionType: 'EXECUTE', items,
  }, 'addDrop');
}

// Move players between lineup slots. NOTE: transaction type is "ROSTER" (NOT "LINEUP");
// items are type "LINEUP". Send ONE move per call (multi-item ROSTER transactions can 400).
export async function setLineup({ season, leagueId, teamId, week, moves }) {
  const results = [];
  for (const m of moves) {
    const body = { isLeagueManager: false, teamId, type: 'ROSTER', scoringPeriodId: week, executionType: 'EXECUTE',
      items: [{ playerId: m.playerId, type: 'LINEUP', fromLineupSlotId: m.from, toLineupSlotId: m.to }] };
    results.push(await post(txUrl(season, leagueId), body, 'setLineup'));
  }
  return results;
}

// Ask ESPN to set the optimal lineup (Recommendations endpoint applies it server-side).
export async function quickLineup({ season, leagueId, teamId, week }) {
  const url = `https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/${season}/segments/0/leagues/${leagueId}` +
              `/teams/${teamId}/recommendations?lineupScoringPeriodId=${week}&recommendationTypeId=LINEUP&restOfWeek=true`;
  return post(url, {}, 'quickLineup');
}
