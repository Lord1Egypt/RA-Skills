#!/usr/bin/env node
// Arena Agent - Autonomous AI Player for Burner Empire
// Plays the game via REST API with LLM-driven decision-making
//
// Usage:
//   ARENA_API_KEY=arena_xxx OPENROUTER_API_KEY=xxx node arena-agent.js [--player-id UUID] [--duration 30m] [--model MODEL]
//
// The agent loops: get state → ask LLM → execute action → check notifications → repeat

import { appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { ArenaClient, ArenaStreamClient } from './arena-client.js';
import { ArenaWebSocketClient } from './arena-ws-client.js';
import { LLMClient } from './llm.js';
import {
  ARENA_API_KEY, ARENA_LLM_MODEL, TICK_INTERVAL_MS, LOGS_DIR, ARENA_TRANSPORT,
  RANK_TITLES, DISTRICTS, DRUGS, DRUG_RANK_REQ, DRUG_PRECURSOR_COST,
  DRUG_BASE_PRICE, QUALITY_TIERS, GEAR_CATALOG, HEAT_MAX, PVP_MIN_RANK,
  MAX_ACTION_HISTORY, STUCK_THRESHOLD, AGENT_DIRTY_CASH_RESERVE,
  CREW_CREATE_COST, CREW_MAX_MEMBERS, HQ_TIERS,
  WAR_MIN_HQ_TIER, LAB_MIN_HQ_TIER, VAULT_MIN_HQ_TIER,
  TURF_CLAIM_COST, TURF_MAX_SOLO, CONTEST_TURF_MIN_RANK,
  RACKET_TYPES, FRONT_TYPES, WAR_BASE_COST, ADDITIVE_CATALOG,
  RATE_LIMIT_WINDOW_MS, RATE_LIMIT_MAX_HITS, RATE_LIMIT_PAUSE_MS,
} from './config.js';

// ── Parse CLI args ──────────────────────────────────────────────────────

const args = process.argv.slice(2);
function getArg(name) {
  const i = args.indexOf(name);
  return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
}

const PLAYER_ID = getArg('--player-id') || process.env.ARENA_PLAYER_ID;
const DURATION_STR = getArg('--duration') || process.env.ARENA_DURATION || '30m';
const MODEL_OVERRIDE = getArg('--model');

function parseDuration(s) {
  const m = s.match(/^(\d+)(s|m|h)$/);
  if (!m) return 30 * 60 * 1000;
  const n = parseInt(m[1]);
  return n * ({ s: 1000, m: 60000, h: 3600000 }[m[2]]);
}
const DURATION_MS = parseDuration(DURATION_STR);

// ── Logger ──────────────────────────────────────────────────────────────

function log(level, msg, data = null) {
  const entry = { t: new Date().toISOString(), level, msg };
  if (data) entry.data = data;
  const line = JSON.stringify(entry);
  console.log(`[${level.toUpperCase()}] ${msg}`);
  try {
    mkdirSync(LOGS_DIR, { recursive: true });
    appendFileSync(join(LOGS_DIR, 'agent.jsonl'), line + '\n');
  } catch {}
}

// ── Helper: broke-state hint ─────────────────────────────────────────

function getBrokeHint(player, state) {
  const dirty = player.dirty_cash || 0;
  const inv = state.inventory || {};
  const hasInventory = Object.values(inv).some(v => v > 0);
  if (dirty > 0 || hasInventory) return '';

  const activeDealers = (state.dealers || []).filter(d => d.status === 'active');
  if (activeDealers.length > 0) {
    return '$0 dirty cash. You have active dealers — wait for dealer sales income.';
  }
  return '$0 dirty cash, no inventory, no active dealers. Travel to different districts — robbery events can give dirty cash (choose fight).';
}

// ── Helper: format action history ───────────────────────────────────

function formatActionHistory(recentActions) {
  if (recentActions.length === 0) return '';

  const lines = recentActions.map(a => {
    if (a.outcome === 'success') return `- Tick ${a.tick}: ${a.action} -> OK`;
    if (a.outcome === 'failed') return `- Tick ${a.tick}: ${a.action} -> FAILED: ${a.error}`;
    if (a.outcome === 'blocked') return `- Tick ${a.tick}: ${a.action} -> BLOCKED: ${a.reason}`;
    return `- Tick ${a.tick}: ${a.action} -> ${a.outcome}`;
  });

  // Check for repeated failures
  const last5 = recentActions.slice(-5);
  const failedActions = last5.filter(a => a.outcome === 'failed' || a.outcome === 'blocked');
  const actionCounts = {};
  for (const a of failedActions) {
    actionCounts[a.action] = (actionCounts[a.action] || 0) + 1;
  }
  const repeatedAction = Object.entries(actionCounts).find(([, count]) => count >= STUCK_THRESHOLD);

  let warning = '';
  if (repeatedAction) {
    warning = `\nNote: "${repeatedAction[0]}" has failed ${repeatedAction[1]} times recently. A different approach would be more productive.`;
  }

  return `\n## Recent Action History\n${lines.join('\n')}${warning}\n`;
}

// ── Helper: format available actions (uses suggested_actions if present) ─

function formatAvailableActions(state, rank, availableDrugs, hasActiveContract, player) {
  const suggested = state.suggested_actions;

  if (suggested && Array.isArray(suggested)) {
    const available = suggested.filter(a => a.available);
    const blocked = suggested.filter(a => !a.available);

    // Group by priority for clearer LLM guidance
    const high = available.filter(a => a.priority === 'high');
    const medium = available.filter(a => a.priority === 'medium');
    const low = available.filter(a => a.priority === 'low');

    function formatAction(a) {
      let line = a.action;
      if (a.params_hint) {
        const params = Object.entries(a.params_hint)
          .filter(([k]) => k !== 'available_gear') // skip verbose gear list
          .map(([k, v]) => `${k}=${typeof v === 'object' ? JSON.stringify(v) : v}`).join(',');
        if (params) line += `(${params})`;
      }
      if (a.note) line += ` — ${a.note}`;
      return line;
    }

    let text = '## Actions\n';
    if (high.length > 0) {
      text += `**DO FIRST:** ${high.map(formatAction).join('; ')}\n`;
    }
    if (medium.length > 0) {
      text += `Available: ${medium.map(formatAction).join(', ')}\n`;
    }
    if (low.length > 0) {
      text += `Low priority: ${low.map(a => a.action).join(', ')}\n`;
    }
    if (blocked.length > 0) {
      text += `Blocked: ${blocked.map(a => `${a.action}(${a.reason})`).join(', ')}\n`;
    }
    return text;
  }

  // Fallback: static action list (no suggested_actions from server)
  const crew = state.crew;
  const crewRole = player.crew_role;
  const hqTier = crew?.hq_tier || 0;
  const inCrew = !!player.crew_id;
  const isLeader = crewRole === 'leader';
  const isLeaderOrUnderboss = crewRole === 'leader' || crewRole === 'underboss';
  const clean = player.clean_cash || 0;

  let actions = `## Available Actions
${rank >= 0 ? `- cook: Start cooking drugs. Params: {drug: "${availableDrugs.join('|')}", quality: "cut|standard|pure"}` : ''}
- collect_cook: Collect a READY cook. Params: {cook_id: "UUID"} *** works on READY cooks only — collecting COOKING cooks will fail ***
- recruit_dealer: Hire a dealer ($300, first free). No params.
- assign_dealer: Deploy an IDLE dealer. Params: {dealer_id, district, drug, quality, units} *** dealer must be IDLE — cannot assign ACTIVE or BUSTED dealers ***
- resupply_dealer: Restock. Params: {dealer_id, units}
- recall_dealer: Pull back. Params: {dealer_id}
- travel: Move districts. Params: {district: "${DISTRICTS.join('|')}"}
- lay_low: Hide (5min). No params. Do this if heat > 30.
- bribe: Pay clean cash to reduce heat by 25. No params.
${rank >= 1 ? `- launder: Convert dirty→clean. Params: {amount: number} *** max launderable: $${Math.max(0, (player.dirty_cash || 0) - AGENT_DIRTY_CASH_RESERVE)} (keeps $${AGENT_DIRTY_CASH_RESERVE} reserve) ***` : ''}
${rank >= 2 ? '- scout: Gather district intel (4hr cooldown). No params.' : ''}
${rank >= 2 ? `- hostile_action: Attack player. Params: {action_type: "rob|snitch|intimidate|hit", target_player_id: "UUID"}` : ''}
- buy_gear: Purchase gear. Params: {gear_type: "brass_knuckles|switchblade|piece|leather_jacket|kevlar_vest|plated_carrier"}
- equip_gear: Equip owned gear. Params: {gear_id: "UUID"}
- accept_contract: Take contract (max 1 active). Params: {contract_id: "UUID"}${hasActiveContract ? ' *** you already have an active contract — accepting another will fail ***' : ''}
- bail: Leave prison early (costs clean cash). No params.
- bail_dealer: Post bail for an ARRESTED dealer. Params: {dealer_id: "UUID"} *** only works on "arrested" status, not "busted" ***
- fire_dealer: Fire any dealer (returns inventory). Params: {dealer_id: "UUID"} *** use this to clear busted dealers and free slots for new recruits ***
- dismiss_dealer: Dismiss a busted/arrested dealer (no inventory return). Params: {dealer_id: "UUID"}`;

  // Crew actions
  if (!inCrew && rank >= 2 && clean >= CREW_CREATE_COST) {
    actions += `\n- create_crew: Create a crew ($${CREW_CREATE_COST} clean). Params: {name: "crew_name"}`;
  }
  if (inCrew) {
    actions += `\n- crew_deposit: Deposit cash to crew treasury. Params: {amount: number, cash_type: "dirty|clean"}`;
    if (!isLeader) {
      actions += '\n- leave_crew: Leave your crew. No params.';
    }
  }

  // HQ actions
  if (inCrew && isLeader) {
    if (hqTier === 0) {
      actions += `\n- buy_hq: Buy crew HQ ($${HQ_TIERS[1].buy_cost} clean from treasury). No params.`;
    } else if (hqTier < 5) {
      const next = HQ_TIERS[hqTier + 1];
      actions += `\n- upgrade_hq: Upgrade HQ to ${next.name} ($${next.buy_cost} clean from treasury). No params.`;
    }
  }

  // Lab actions (HQ Tier 3+)
  if (inCrew && hqTier >= LAB_MIN_HQ_TIER) {
    actions += `\n- start_blend: Blend premium drugs. Params: {base_drug: "weed|coke|meth|heroin|pills", additives: ["${ADDITIVE_CATALOG.map(a => a.type).join('"|"')}"], quality: "standard|pure"}`;
    actions += '\n- get_recipe_book: View discovered blend recipes. No params.';
  }

  // War actions (HQ Tier 2+)
  if (inCrew && isLeaderOrUnderboss && hqTier >= WAR_MIN_HQ_TIER) {
    actions += `\n- declare_war: Declare turf war ($${WAR_BASE_COST}+ clean from treasury). Params: {turf_id: "UUID"}`;
  }
  if (inCrew) {
    actions += '\n- get_war_status: Check active crew wars. No params.';
  }

  // Vault actions (HQ Tier 4+)
  if (inCrew && hqTier >= VAULT_MIN_HQ_TIER) {
    actions += '\n- vault_deposit: Deposit cash to vault. Params: {dirty: number, clean: number}';
    actions += '\n- vault_withdraw: Withdraw from vault (24hr lock). Params: {dirty: number, clean: number}';
  }

  // Turf actions
  if (clean >= TURF_CLAIM_COST) {
    actions += `\n- claim_turf: Claim unclaimed turf ($${TURF_CLAIM_COST} clean). Params: {turf_id: "UUID"}`;
  }
  if (rank >= CONTEST_TURF_MIN_RANK) {
    actions += '\n- contest_turf: Challenge rival turf ($1000+ clean). Params: {turf_id: "UUID"}';
  }
  actions += `\n- install_racket: Install racket on your turf. Params: {turf_id: "UUID", racket_type: "${RACKET_TYPES.join('|')}"}`;

  // Front business actions
  if (inCrew && isLeaderOrUnderboss) {
    actions += `\n- buy_front: Buy laundering front. Params: {type: "${FRONT_TYPES.map(f => f.type).join('|')}"}`;
  }

  actions += '\n- wait: Do nothing this tick.';
  return actions;
}

// ── Crew & Turf prompt sections ─────────────────────────────────────────

function buildCrewSection(state, player) {
  const crew = state.crew;
  if (crew) {
    const members = (crew.members || [])
      .map(m => `${m.username} (${m.role})`)
      .join(', ');
    const hqTier = crew.hq_tier || 0;
    const hqName = crew.hq_name || HQ_TIERS[hqTier]?.name || 'None';
    const nextTier = hqTier < 5 ? HQ_TIERS[hqTier + 1] : null;
    const nextCost = nextTier && player.crew_role === 'leader' ? ` (next: ${nextTier.name} $${nextTier.buy_cost})` : '';
    const labStatus = hqTier >= LAB_MIN_HQ_TIER ? 'Unlocked' : `Locked (Tier ${LAB_MIN_HQ_TIER})`;
    const warStatus = hqTier >= WAR_MIN_HQ_TIER ? 'Unlocked' : `Locked (Tier ${WAR_MIN_HQ_TIER})`;
    const vaultStatus = hqTier >= VAULT_MIN_HQ_TIER ? 'Unlocked' : `Locked (Tier ${VAULT_MIN_HQ_TIER})`;

    // Front businesses
    const fronts = (state.front_businesses || [])
      .map(f => `${f.business_type} (${(f.fee_rate * 100).toFixed(0)}% fee, $${f.daily_cap}/day)`)
      .join(', ');
    const frontLine = fronts ? `\n- Fronts: ${fronts}` : '';

    return `## Crew: ${crew.name}
- Role: ${player.crew_role} | Members: ${(crew.members || []).length}/${CREW_MAX_MEMBERS}
- Treasury: $${crew.treasury_dirty}d / $${crew.treasury_clean}c
- HQ: ${hqName} (Tier ${hqTier}/5)${nextCost}
- Lab: ${labStatus} | Wars: ${warStatus} | Vault: ${vaultStatus}
- Members: ${members}${frontLine}`;
  }

  const rank = player.reputation_rank || 0;
  if (rank >= 2) {
    return `## Crew (not joined)
- Create a crew for $${CREW_CREATE_COST} clean cash, or accept invites from other players.
- Crews unlock: shared treasury, HQ (+dealer/heat/launder bonuses), Lab (blend premium drugs), Wars (capture turfs), Vault (protected savings).`;
  }

  return '';
}

function buildTurfSection(state, player) {
  const turfs = state.turfs || [];
  const district = player.current_district;
  const districtTurfs = turfs
    .filter(t => t.district === district)
    .slice(0, 5);

  if (districtTurfs.length === 0) return '';

  const myTurfs = turfs.filter(t => t.owner_id === player.id);
  const lines = districtTurfs.map(t => {
    const owner = t.owner_id ? (t.owner_id === player.id ? 'YOU' : (t.owner_name || 'rival')) : 'unclaimed';
    const racket = t.racket_type ? ` | Racket: ${t.racket_type}` : '';
    return `  [${t.id}] Owner: ${owner} | Def: ${t.defense_strength || 0}${racket}`;
  });

  return `## Turfs in ${district}
${lines.join('\n')}
- Your turfs: ${myTurfs.length}/${player.crew_id ? 'unlimited' : TURF_MAX_SOLO}`;
}

// ── Static system prefix (built once, benefits from prompt caching) ───

const STATIC_SYSTEM_PREFIX = `You are an AI agent playing Burner Empire, a competitive crime MMO.
You compete against humans and other AI agents. Your goal: maximize revenue, rank up, and survive.

## Drug Economics
${DRUGS.map(d => `- ${d}: rank ${DRUG_RANK_REQ[d]}+, costs $${DRUG_PRECURSOR_COST[d]}, sells ~$${DRUG_BASE_PRICE[d]}/unit`).join('\n')}

## Combat (Stat-Check)
One-shot instant resolution. No rounds or choices.
attacker_score = (total_ATK + rank * 1.5) * minutes_mult * RNG(0.85-1.15)
defender_score = (total_DEF + 3 + rank * 1.5) * minutes_mult * RNG(0.85-1.15)
Minutes mult = 0.5 + 0.5 * (pvp_minutes / 100). Low minutes = weaker combat.
Ties (within 5%): defender wins unless attacker has "tie_breaker" (Burner Piece).
Gear specials: power_surge (+5 ATK), first_strike (+3 ATK), edge (+10%), tie_breaker (wins ties),
  damage_control (50% loss reduction), fortress (75% + skip shaken), big_score (1.5x stakes).

## Rules
- Respond with valid JSON: {"action": "action_name", "params": {...}, "reasoning": "why"}
- UUIDs: use the exact UUIDs shown in brackets [uuid] above. Invented or guessed UUIDs will fail.
- Districts: the valid names are ${DISTRICTS.join(', ')}. No other district names exist.
- collect_cook: works only on cooks with status READY. Collecting a cook still COOKING will fail.
- If traveling, laying low, or in prison -> choose "wait" (most actions are blocked).
- If heat > 30 -> consider laying low or bribing.
- Manage your dealers — they're your main income source.
- Launder dirty cash when possible (rank 1+) to build clean cash reserves for bribes/bail.
- "wait" is valid if nothing productive can be done right now.

## Strategy Guide

### Phase 1: Foundation (Rank 0-1)
- Core loop: cook -> assign dealers -> dealers sell -> earn dirty cash -> repeat
- Recruit dealers ASAP — they are your main passive income
- Launder dirty cash (rank 1+) to build clean cash for bribes, bail, gear
- Launder at most (dirty_cash - $${AGENT_DIRTY_CASH_RESERVE}). Keep $${AGENT_DIRTY_CASH_RESERVE} dirty reserve.

### Phase 2: Gear Up (Rank 2+)
- Buy a leather jacket ($400 dirty) for defense, then a switchblade ($1000 dirty) or piece ($3000 dirty) for offense
- Accessories: saturday_special ($350, 1.5x stakes) or lucky_coin ($1200, +10% combat power)
- Equip gear immediately after buying — unequipped gear does nothing
- Gear gives ATK/DEF stats that affect combat outcomes

### Phase 3: PvP (Rank 2+, geared)
- When you have equipped weapon + heat < 40 + not shaken + enough PvP minutes, look for targets
- hostile_action types: rob (steal cash, 15 min), hit (damage + XP, 25 min), snitch (add heat, 5 min), intimidate (shake, 10 min)
- Pick targets at or below your rank. "exposed" targets (>70% minutes) take 1.5x steal.
- Avoid attacking when your minutes are low — combat power drops to 50% at 0 minutes.
### Phase 4: Crew & Turf (Rank 2+, clean cash)
- Create crew ($${CREW_CREATE_COST} clean) -> fund treasury -> buy HQ ($50k) -> upgrade tiers
- Turfs: claim ($${TURF_CLAIM_COST} clean) for +20% dealer revenue, install rackets for passive income
- HQ Tier 2: wars, Tier 3: lab (blend premium drugs), Tier 4: vault

### Key Rules
- Dirty cash sources: dealer sales (passive), racket income (passive), robbery travel events (fight), PvP robbing
- Contracts pay CLEAN cash, not dirty. Clean cash is for bribes, bail, HQ, gear.
- There is NO clean -> dirty conversion.
- If $0 dirty + empty inventory: Active dealers? WAIT. Turfs with rackets? WAIT. Neither? TRAVEL for robbery events.
- Heat > 30 is dangerous — bribe or lay low. Heat > 50 means raids and busts.`;

// ── Market intelligence ─────────────────────────────────────────────────

function buildMarketSummary(market, rank, currentDistrict) {
  if (!market || typeof market !== 'object' || Object.keys(market).length === 0) return '';

  const availableDrugs = DRUGS.filter(d => DRUG_RANK_REQ[d] <= rank);
  if (availableDrugs.length === 0) return '';

  // Current district prices
  const currentPrices = market[currentDistrict] || {};
  const currentLine = availableDrugs
    .filter(d => currentPrices[d] !== undefined)
    .map(d => `${d} $${currentPrices[d]}`)
    .join(', ');

  // Best margins across other districts
  const margins = [];
  for (const district of DISTRICTS) {
    if (district === currentDistrict) continue;
    const prices = market[district];
    if (!prices) continue;
    for (const drug of availableDrugs) {
      if (prices[drug] === undefined) continue;
      const margin = prices[drug] - DRUG_PRECURSOR_COST[drug];
      margins.push({ district, drug, price: prices[drug], margin });
    }
  }
  margins.sort((a, b) => b.margin - a.margin);
  const topMargins = margins.slice(0, 3)
    .map(m => `${m.district.replace(/_/g, ' ')} ${m.drug} $${m.price}/u (+$${m.margin})`)
    .join(', ');

  let section = `\n## Market Prices (live)`;
  if (currentLine) section += `\nYour district (${currentDistrict.replace(/_/g, ' ')}): ${currentLine}`;
  if (topMargins) section += `\nBest margins: ${topMargins}`;
  return section;
}

// ── System prompt builder ───────────────────────────────────────────────

function buildSystemPrompt(state, recentActions = [], recentDistricts = []) {
  const player = state.player || {};
  const rank = player.reputation_rank || 0;
  const rankTitle = RANK_TITLES[rank] || 'Unknown';
  const availableDrugs = DRUGS.filter(d => DRUG_RANK_REQ[d] <= rank);

  // Compact inventory
  const inv = state.inventory || {};
  const inventory = Object.keys(inv).length > 0
    ? Object.entries(inv).map(([k, v]) => `${v}x ${k.replace('_', ' ')}`).join(', ')
    : 'empty';

  // Compact dealer format
  const dealers = (state.dealers || [])
    .map(d => {
      let line = `[${d.id}] ${d.name} ${d.status.toUpperCase()}`;
      if (d.district) line += ` ${d.district}`;
      if (d.assigned_drug) line += ` ${d.assigned_drug}/${d.assigned_quality}`;
      if (d.inventory_count) line += ` ${d.inventory_count}u`;
      return line;
    })
    .join('\n  ') || 'none';

  // Compact cook format with relative time
  const now = Date.now();
  const cooks = (state.cook_queue || [])
    .map(c => {
      if (c.status === 'ready') return `[${c.id}] ${c.drug_type}/${c.quality_tier} READY (${c.units_expected}u)`;
      const eta = c.completes_at ? Math.max(0, Math.round((new Date(c.completes_at).getTime() - now) / 60000)) : '?';
      return `[${c.id}] ${c.drug_type}/${c.quality_tier} COOKING ~${eta}m (${c.units_expected}u)`;
    })
    .join('\n  ') || 'none';

  const gearList = state.gear || [];
  const gear = gearList.length > 0
    ? gearList.map(g => {
        const cat = GEAR_CATALOG.find(c => c.type === g.gear_type);
        const stats = cat ? ` ATK:${cat.atk} DEF:${cat.def}` : '';
        return `[${g.id}] ${g.gear_type}${g.equipped ? ' [EQ]' : ''}${stats}`;
      }).join(', ')
    : 'none';
  const totalAtk = gearList.filter(g => g.equipped).reduce((s, g) => {
    const cat = GEAR_CATALOG.find(c => c.type === g.gear_type);
    return s + (cat ? cat.atk : 0);
  }, 0);
  const totalDef = gearList.filter(g => g.equipped).reduce((s, g) => {
    const cat = GEAR_CATALOG.find(c => c.type === g.gear_type);
    return s + (cat ? cat.def : 0);
  }, 0);

  const districtPlayers = (state.district_players || [])
    .filter(p => p.id !== player.id)
    .map(p => `[${p.id}] ${p.username} (${p.rank_title})`)
    .join('\n  ') || 'none nearby';

  const myContracts = (state.my_contracts || [])
    .map(c => `[${c.id}] ${c.contract_type}: ${c.description} ${c.progress || 0}/${c.target} ($${c.scaled_reward || c.base_reward})`)
    .join('\n  ');

  const offeredContracts = (state.contracts || [])
    .filter(c => c.status === 'offered')
    .map(c => `[${c.id}] ${c.contract_type}: ${c.description} ($${c.scaled_reward || c.base_reward})`)
    .join('\n  ');

  const hasActiveContract = (state.my_contracts || []).length > 0;
  const contracts = myContracts
    ? `ACTIVE: ${myContracts}${offeredContracts ? '\n  Board: ' + offeredContracts : ''}`
    : (offeredContracts || 'none');

  // Dynamic context only
  return `${STATIC_SYSTEM_PREFIX}

## Your Status
${player.username} | ${rankTitle} (${rank}/7) | XP: ${player.reputation_xp || 0} | ${player.current_district}
Dirty: $${player.dirty_cash || 0} | Clean: $${player.clean_cash || 0} | Heat: ${player.heat_level?.toFixed(1) || 0}/${HEAT_MAX} ${player.heat_level > 25 ? 'RISK' : ''}
Season: $${player.season_revenue || 0} | Shaken: ${player.is_shaken ? 'YES' : 'No'} | Launder cap: $${player.solo_launder_remaining ?? '?'}
Combat: ATK ${totalAtk} / DEF ${totalDef}${totalAtk === 0 && rank >= PVP_MIN_RANK ? ' (buy gear before PvP!)' : ''}
Minutes: ${Math.round(player.pvp_minutes || 0)}/${Math.round(player.pvp_minutes_max || 100)}${(player.pvp_minutes != null && player.pvp_minutes < 15) ? ' LOW' : ''}
${recentDistricts.length > 1 ? `Recent districts: ${recentDistricts.join(' -> ')} (avoid revisiting)\n` : ''}${getBrokeHint(player, state)}
## Resources
Inventory: ${inventory}
Dealers (${(state.dealers || []).length}/8):
  ${dealers}
Cooks: ${cooks}
Gear: ${gear}
Contracts: ${contracts}

## Environment
Players: ${districtPlayers}${buildMarketSummary(state.market, rank, player.current_district)}
${buildCrewSection(state, player)}
${buildTurfSection(state, player)}
${formatActionHistory(recentActions)}
${formatAvailableActions(state, rank, availableDrugs, hasActiveContract, player)}`;
}

// ── Auto-correct helpers ──────────────────────────────────────────────────
// Fix common LLM mistakes instead of rejecting the action outright.

function fuzzyMatchDistrict(name) {
  if (!name) return null;
  const lower = name.toLowerCase().replace(/[^a-z]/g, '');
  // Direct match
  const exact = DISTRICTS.find(d => d === name);
  if (exact) return exact;
  // Partial match (e.g., "docks" -> "the_docks", "strip" -> "the_strip")
  const partial = DISTRICTS.find(d => d.replace('the_', '').replace(/_/g, '') === lower);
  if (partial) return partial;
  // Contains match
  const contains = DISTRICTS.find(d => lower.includes(d.replace('the_', '').replace(/_/g, '')));
  if (contains) return contains;
  return null;
}

function autoCorrectAction(action, params, state) {
  const cooks = state.cook_queue || [];
  const dealers = state.dealers || [];

  switch (action) {
    case 'travel': {
      if (params.district && !DISTRICTS.includes(params.district)) {
        const match = fuzzyMatchDistrict(params.district);
        if (match) {
          log('info', `Auto-corrected district "${params.district}" → "${match}"`);
          params.district = match;
        }
      }
      break;
    }
    case 'assign_dealer': {
      // Auto-correct district for assign_dealer too
      if (params.district && !DISTRICTS.includes(params.district)) {
        const match = fuzzyMatchDistrict(params.district);
        if (match) {
          log('info', `Auto-corrected dealer district "${params.district}" → "${match}"`);
          params.district = match;
        }
      }
      // Auto-select first idle dealer if given bad ID
      if (params.dealer_id && !dealers.find(d => d.id === params.dealer_id)) {
        const idle = dealers.find(d => d.status === 'idle');
        if (idle) {
          log('info', `Auto-corrected dealer_id "${params.dealer_id}" → "${idle.id}" (${idle.name})`);
          params.dealer_id = idle.id;
        }
      }
      break;
    }
    case 'collect_cook': {
      // Auto-select first ready cook if given bad ID
      if (params.cook_id) {
        const cook = cooks.find(c => c.id === params.cook_id);
        if (!cook || cook.status !== 'ready') {
          const ready = cooks.find(c => c.status === 'ready');
          if (ready) {
            log('info', `Auto-corrected cook_id "${params.cook_id}" → "${ready.id}" (ready ${ready.drug_type})`);
            params.cook_id = ready.id;
          }
        }
      }
      break;
    }
    case 'resupply_dealer': {
      // Auto-select a low-inventory active dealer if given bad ID
      if (params.dealer_id && !dealers.find(d => d.id === params.dealer_id)) {
        const active = dealers
          .filter(d => d.status === 'active')
          .sort((a, b) => (a.inventory_count || 0) - (b.inventory_count || 0));
        if (active.length > 0) {
          log('info', `Auto-corrected resupply dealer_id "${params.dealer_id}" → "${active[0].id}"`);
          params.dealer_id = active[0].id;
        }
      }
      break;
    }
  }
}

// ── Pre-flight validation ────────────────────────────────────────────────
// Catches obviously invalid actions before they hit the server.
// Returns a rejection reason string, or null if the action looks valid.

function validateAction(action, params, state) {
  const player = state.player || {};
  const cooks = state.cook_queue || [];
  const dealers = state.dealers || [];
  const inv = state.inventory || {};

  // Check suggested_actions from server (Part 5b)
  if (state.suggested_actions && Array.isArray(state.suggested_actions)) {
    const suggestion = state.suggested_actions.find(s => s.action === action);
    if (suggestion && !suggestion.available) {
      return suggestion.reason || `${action} is not available`;
    }
  }

  // Global state checks
  const inPrison = !!player.in_prison || !!player.prison_until;
  const layingLow = !!player.laying_low_until;
  const traveling = !!player.travel_to;
  const isShaken = !!player.is_shaken;
  const blockedState = inPrison || layingLow || traveling;

  // Block most actions when in a restricted state
  const blockedActions = ['cook', 'launder', 'hostile_action', 'buy_gear', 'recruit_dealer',
    'assign_dealer', 'resupply_dealer', 'recall_dealer', 'scout', 'accept_contract',
    'claim_turf', 'contest_turf', 'create_crew'];
  if (blockedState && blockedActions.includes(action)) {
    if (inPrison) return 'in prison — only bail or wait';
    if (traveling) return 'traveling — must wait for arrival';
    if (layingLow) return 'laying low — cannot act until it expires';
  }

  switch (action) {
    case 'collect_cook': {
      const cook = cooks.find(c => c.id === params.cook_id);
      if (!cook) return 'cook_id not found in queue';
      if (cook.status !== 'ready') return `cook is still ${cook.status}, not ready`;
      break;
    }
    case 'assign_dealer': {
      const dealer = dealers.find(d => d.id === params.dealer_id);
      if (!dealer) return 'dealer_id not found';
      if (dealer.status !== 'idle') return `dealer is ${dealer.status}, must be idle`;
      if (params.units > 0) {
        const key = `${params.drug}_${params.quality}`;
        const available = inv[key] || 0;
        if (available < params.units) return `only ${available} units of ${key} in inventory`;
      }
      break;
    }
    case 'resupply_dealer': {
      const dealer = dealers.find(d => d.id === params.dealer_id);
      if (!dealer) return 'dealer_id not found';
      if (dealer.status !== 'active') return `dealer is ${dealer.status}, must be active`;
      if (dealer.assigned_drug) {
        const key = `${dealer.assigned_drug}_${dealer.assigned_quality}`;
        const available = inv[key] || 0;
        if (available < (params.units || 1)) return `only ${available} units of ${key} in inventory`;
      }
      break;
    }
    case 'launder': {
      const dirty = player.dirty_cash || 0;
      if ((params.amount || 0) > dirty) return `amount $${params.amount} exceeds dirty cash $${dirty}`;
      const maxLaunder = dirty - AGENT_DIRTY_CASH_RESERVE;
      if (maxLaunder <= 0) return `dirty cash $${dirty} is at or below reserve ($${AGENT_DIRTY_CASH_RESERVE}) — cannot launder`;
      // Check daily launder cap
      const launderRemaining = player.solo_launder_remaining;
      if (launderRemaining !== undefined && launderRemaining <= 0) return 'daily launder cap reached ($0 remaining)';
      if (launderRemaining !== undefined && params.amount > launderRemaining) {
        params.amount = Math.min(maxLaunder, launderRemaining);
        log('info', `Capped launder to $${params.amount} (daily remaining: $${launderRemaining}, reserve: $${AGENT_DIRTY_CASH_RESERVE})`);
      } else if (params.amount > maxLaunder) {
        params.amount = maxLaunder;
        log('info', `Capped launder to $${maxLaunder} (reserve $${AGENT_DIRTY_CASH_RESERVE})`);
      }
      break;
    }
    case 'cook': {
      const dirty = player.dirty_cash || 0;
      const cost = DRUG_PRECURSOR_COST[params.drug] || 0;
      if (cost > dirty) return `precursor costs $${cost}, only have $${dirty} dirty`;
      break;
    }
    case 'travel': {
      const district = params.district;
      if (district && !DISTRICTS.includes(district)) {
        return `invalid district "${district}" — valid: ${DISTRICTS.join(', ')}`;
      }
      if (district === player.current_district) {
        return `already in ${district}`;
      }
      break;
    }
    case 'buy_gear': {
      const dirty = player.dirty_cash || 0;
      const item = GEAR_CATALOG.find(g => g.type === params.gear_type);
      if (item && item.cost > dirty) return `${item.name} costs $${item.cost}, only have $${dirty} dirty`;
      break;
    }
    case 'hostile_action': {
      if ((player.reputation_rank || 0) < PVP_MIN_RANK) return `need rank ${PVP_MIN_RANK}+ for PvP`;
      if (isShaken) return 'shaken — cannot attack';
      // Validate target_player_id looks like a UUID
      const targetId = params.target_player_id;
      if (targetId && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(targetId)) {
        return `invalid target_player_id "${targetId}" — must be a UUID from district players list`;
      }
      break;
    }
    case 'accept_contract': {
      const myContracts = state.my_contracts || [];
      if (myContracts.length > 0) return 'already have an active contract — complete or wait for it to expire';
      const completedToday = state.contracts_completed_today || 0;
      const dailyLimit = state.contract_daily_limit || 3;
      if (completedToday >= dailyLimit) return `daily contract limit reached (${completedToday}/${dailyLimit})`;
      break;
    }
    case 'create_crew': {
      if (player.crew_id) return 'already in a crew';
      if ((player.reputation_rank || 0) < 2) return 'need rank 2+ to create crew';
      if ((player.clean_cash || 0) < CREW_CREATE_COST) return `need $${CREW_CREATE_COST} clean cash`;
      break;
    }
    case 'crew_deposit': {
      if (!player.crew_id) return 'not in a crew';
      const cashType = params.cash_type || 'dirty';
      const amt = params.amount || 0;
      if (cashType === 'dirty' && amt > (player.dirty_cash || 0)) return `only have $${player.dirty_cash} dirty`;
      if (cashType === 'clean' && amt > (player.clean_cash || 0)) return `only have $${player.clean_cash} clean`;
      break;
    }
    case 'leave_crew': {
      if (!player.crew_id) return 'not in a crew';
      if (player.crew_role === 'leader') return 'leaders cannot leave, transfer leadership first';
      break;
    }
    case 'buy_hq':
    case 'upgrade_hq': {
      if (!player.crew_id) return 'not in a crew';
      if (player.crew_role !== 'leader') return 'only the leader can manage HQ';
      break;
    }
    case 'start_blend': {
      if (!player.crew_id) return 'not in a crew';
      break;
    }
    case 'declare_war': {
      if (!player.crew_id) return 'not in a crew';
      if (player.crew_role !== 'leader' && player.crew_role !== 'underboss') return 'only leader/underboss can declare war';
      break;
    }
    case 'vault_deposit':
    case 'vault_withdraw': {
      if (!player.crew_id) return 'not in a crew';
      break;
    }
    case 'claim_turf': {
      if ((player.clean_cash || 0) < TURF_CLAIM_COST) return `need $${TURF_CLAIM_COST} clean cash`;
      break;
    }
    case 'contest_turf': {
      if ((player.reputation_rank || 0) < CONTEST_TURF_MIN_RANK) return `need rank ${CONTEST_TURF_MIN_RANK}+ to contest`;
      break;
    }
    case 'buy_front': {
      if (!player.crew_id) return 'not in a crew';
      if (player.crew_role !== 'leader' && player.crew_role !== 'underboss') return 'only leader/underboss can buy fronts';
      break;
    }
  }
  return null; // action looks valid
}

// ── Adaptive tick interval ────────────────────────────────────────────

function getNextTickDelay(state, lastAction) {
  const player = state?.player || {};
  const dealers = state?.dealers || [];
  const cooks = state?.cook_queue || [];
  const inv = state?.inventory || {};

  // Just executed an action — moderate delay
  if (lastAction && lastAction !== 'wait') return 20000;

  const hasInventory = Object.values(inv).some(v => v > 0);
  const idleDealers = dealers.filter(d => d.status === 'idle');
  const activeDealers = dealers.filter(d => d.status === 'active');
  const cookingInProgress = cooks.some(c => c.status === 'cooking');
  const hasDirty = (player.dirty_cash || 0) > AGENT_DIRTY_CASH_RESERVE;

  // Has idle dealers + inventory — should assign soon
  if (idleDealers.length > 0 && hasInventory) return TICK_INTERVAL_MS;

  // All dealers stocked, cook in progress — wait for cook
  if (activeDealers.length > 0 && cookingInProgress && !hasInventory) return 30000;

  // All dealers stocked, no cook, no cash to start one — long idle
  if (activeDealers.length > 0 && !cookingInProgress && !hasInventory && !hasDirty) return 45000;

  return TICK_INTERVAL_MS; // default 15s
}

// ── Deterministic bypass: skip LLM for trivial game states ────────────

function tryDeterministicAction(state) {
  const player = state.player || {};
  const inPrison = !!player.in_prison || !!player.prison_until;
  const isLayingLow = !!player.laying_low_until;
  const isTraveling = !!player.travel_to;

  // Traveling — only valid action is wait
  if (isTraveling) return { action: 'wait', params: {}, reasoning: 'Traveling — waiting for arrival' };

  // Laying low — only valid action is wait
  if (isLayingLow) return { action: 'wait', params: {}, reasoning: 'Laying low — waiting for cooldown' };

  // In prison — bail if possible, otherwise wait
  if (inPrison) {
    const clean = player.clean_cash || 0;
    if (clean > 0) return { action: 'bail', params: {}, reasoning: 'In prison — bailing out' };
    return { action: 'wait', params: {}, reasoning: 'In prison — no clean cash for bail' };
  }

  // Cook is READY — collect immediately
  const readyCook = (state.cook_queue || []).find(c => c.status === 'ready');
  if (readyCook) {
    return { action: 'collect_cook', params: { cook_id: readyCook.id }, reasoning: `Collecting ready ${readyCook.drug_type} cook` };
  }

  // Auto-equip unequipped gear to empty slots
  const gearItems = state.gear || [];
  if (gearItems.length > 0) {
    const equippedSlots = new Set(gearItems.filter(g => g.equipped).map(g => g.slot));
    const needsEquip = gearItems.find(g => !g.equipped && !equippedSlots.has(g.slot));
    if (needsEquip) {
      return { action: 'equip_gear', params: { gear_id: needsEquip.id }, reasoning: `Auto-equipping ${needsEquip.gear_type}` };
    }
  }

  // Bail arrested dealers (bail window is time-limited)
  const dealers = state.dealers || [];
  const dirty = player.dirty_cash || 0;
  const arrestedDealer = dealers.find(d => d.status === 'arrested');
  if (arrestedDealer && dirty >= 500) {
    return { action: 'bail_dealer', params: { dealer_id: arrestedDealer.id }, reasoning: `Bailing arrested dealer ${arrestedDealer.name} before window expires` };
  }

  // Fire busted dealers — these are permanently gone (bail window expired), can only be fired
  const bustedDealers = dealers.filter(d => d.status === 'busted');
  if (bustedDealers.length > 0) {
    const worst = bustedDealers.sort((a, b) => (a.loyalty || 0) - (b.loyalty || 0))[0];
    return { action: 'fire_dealer', params: { dealer_id: worst.id }, reasoning: `Firing busted dealer ${worst.name} — permanently gone, freeing slot` };
  }

  return null; // no deterministic action — use LLM
}

// ── Deterministic fallback: pick best action without LLM ──────────────

function deterministicFallback(state, recentDistricts = []) {
  const player = state.player || {};
  const suggested = state.suggested_actions;
  const inv = state.inventory || {};
  const dealers = state.dealers || [];
  const cooks = state.cook_queue || [];
  const dirty = player.dirty_cash || 0;
  const rank = player.reputation_rank || 0;

  // If we have suggested_actions, use them to filter
  const available = suggested && Array.isArray(suggested)
    ? new Set(suggested.filter(a => a.available).map(a => a.action))
    : null;

  function isAvailable(action) {
    return !available || available.has(action);
  }

  // Priority order: collect_cook > resupply_dealer > assign_dealer > cook > launder > travel > wait

  // 1. Collect ready cook
  const readyCook = cooks.find(c => c.status === 'ready');
  if (readyCook && isAvailable('collect_cook')) {
    return { action: 'collect_cook', params: { cook_id: readyCook.id }, reasoning: 'Fallback: collecting ready cook' };
  }

  // 2. Resupply low-inventory active dealer
  const hasInventory = Object.values(inv).some(v => v > 0);
  if (hasInventory && isAvailable('resupply_dealer')) {
    const lowDealer = dealers
      .filter(d => d.status === 'active' && (d.inventory_count || 0) < 3)
      .sort((a, b) => (a.inventory_count || 0) - (b.inventory_count || 0))[0];
    if (lowDealer && lowDealer.assigned_drug) {
      const key = `${lowDealer.assigned_drug}_${lowDealer.assigned_quality}`;
      const units = Math.min(inv[key] || 0, 10);
      if (units > 0) {
        return { action: 'resupply_dealer', params: { dealer_id: lowDealer.id, units }, reasoning: 'Fallback: resupplying low dealer' };
      }
    }
  }

  // 3. Assign idle dealer
  if (hasInventory && isAvailable('assign_dealer')) {
    const idleDealer = dealers.find(d => d.status === 'idle');
    if (idleDealer) {
      // Pick first inventory item
      const [invKey, invQty] = Object.entries(inv).find(([, v]) => v > 0) || [];
      if (invKey && invQty > 0) {
        const [drug, quality] = invKey.split('_');
        const district = player.current_district;
        return { action: 'assign_dealer', params: { dealer_id: idleDealer.id, district, drug, quality, units: Math.min(invQty, 10) }, reasoning: 'Fallback: assigning idle dealer' };
      }
    }
  }

  // 4. Cook if affordable
  if (isAvailable('cook')) {
    const availableDrugs = DRUGS.filter(d => DRUG_RANK_REQ[d] <= rank);
    const bestDrug = availableDrugs
      .filter(d => DRUG_PRECURSOR_COST[d] <= dirty)
      .sort((a, b) => DRUG_BASE_PRICE[b] - DRUG_BASE_PRICE[a])[0];
    if (bestDrug) {
      return { action: 'cook', params: { drug: bestDrug, quality: 'standard' }, reasoning: `Fallback: cooking ${bestDrug}` };
    }
  }

  // 5. Launder if possible
  if (rank >= 1 && isAvailable('launder')) {
    const maxLaunder = dirty - AGENT_DIRTY_CASH_RESERVE;
    const launderRemaining = player.solo_launder_remaining;
    if (maxLaunder > 0 && (launderRemaining === undefined || launderRemaining > 0)) {
      const amount = Math.min(maxLaunder, launderRemaining ?? maxLaunder);
      if (amount > 0) {
        return { action: 'launder', params: { amount }, reasoning: 'Fallback: laundering excess cash' };
      }
    }
  }

  // 5b. Buy gear if rank 2+ and missing weapon/protection/accessory
  if (rank >= PVP_MIN_RANK && isAvailable('buy_gear')) {
    const dirty = player.dirty_cash || 0;
    const gearItems = state.gear || [];
    const hasWeapon = gearItems.some(g => g.slot === 'weapon');
    const hasProtection = gearItems.some(g => g.slot === 'protection');
    const hasAccessory = gearItems.some(g => g.slot === 'accessory');
    if (!hasWeapon && dirty >= 1000) {
      return { action: 'buy_gear', params: { gear_type: 'switchblade' }, reasoning: 'Fallback: buying first weapon' };
    }
    if (!hasProtection && dirty >= 400) {
      return { action: 'buy_gear', params: { gear_type: 'leather_jacket' }, reasoning: 'Fallback: buying first protection' };
    }
    if (!hasAccessory && dirty >= 350) {
      return { action: 'buy_gear', params: { gear_type: 'saturday_special' }, reasoning: 'Fallback: buying accessory for combat bonus' };
    }
  }

  // 5c. PvP if geared and conditions are right
  if (rank >= PVP_MIN_RANK && isAvailable('hostile_action')) {
    const gearItems = state.gear || [];
    const hasEquippedWeapon = gearItems.some(g => g.equipped && g.slot === 'weapon');
    const heat = player.heat_level || 0;
    const isShaken = !!player.is_shaken;
    const pvpMinutes = player.pvp_minutes;
    if (hasEquippedWeapon && heat < 40 && !isShaken && (pvpMinutes == null || pvpMinutes >= 15)) {
      const targets = (state.district_players || [])
        .filter(p => p.id !== player.id && (p.reputation_rank || 0) <= rank);
      if (targets.length > 0) {
        const target = targets.sort((a, b) => (a.reputation_rank || 0) - (b.reputation_rank || 0))[0];
        return { action: 'hostile_action', params: { action_type: 'rob', target_player_id: target.id }, reasoning: `Fallback: robbing ${target.username}` };
      }
    }
  }

  // 6. Travel to a different district (market-aware)
  if (isAvailable('travel')) {
    const recentSet = new Set(recentDistricts.slice(-3));
    const candidates = DISTRICTS.filter(d => d !== player.current_district && !recentSet.has(d));
    const pool = candidates.length > 0 ? candidates : DISTRICTS.filter(d => d !== player.current_district);

    const market = state.market;
    if (market && typeof market === 'object') {
      const hasInv = Object.values(inv).some(v => v > 0);
      const heldDrugs = hasInv ? Object.keys(inv).filter(k => inv[k] > 0).map(k => k.split('_')[0]) : [];

      let best = null;
      let bestScore = -Infinity;
      for (const d of pool) {
        const prices = market[d];
        if (!prices) continue;
        if (hasInv) {
          // Pick district with highest price for drugs we hold
          for (const drug of heldDrugs) {
            if (prices[drug] !== undefined && prices[drug] > bestScore) {
              bestScore = prices[drug];
              best = { district: d, drug, price: prices[drug] };
            }
          }
        } else {
          // Pick district with highest margin for drugs we can cook
          const availDrugs = DRUGS.filter(dr => DRUG_RANK_REQ[dr] <= rank);
          for (const drug of availDrugs) {
            if (prices[drug] === undefined) continue;
            const margin = prices[drug] - DRUG_PRECURSOR_COST[drug];
            if (margin > bestScore) {
              bestScore = margin;
              best = { district: d, drug, margin };
            }
          }
        }
      }
      if (best) {
        const reason = best.price
          ? `Fallback: traveling to ${best.district} (${best.drug} $${best.price}/u, best sell price)`
          : `Fallback: traveling to ${best.district} (${best.drug} +$${best.margin} margin)`;
        return { action: 'travel', params: { district: best.district }, reasoning: reason };
      }
    }

    // No market data — random from non-recent
    const district = pool[Math.floor(Math.random() * pool.length)];
    return { action: 'travel', params: { district }, reasoning: 'Fallback: traveling to new district' };
  }

  return { action: 'wait', params: {}, reasoning: 'Fallback: nothing productive available' };
}

// ── Main Agent Loop (SSE event-driven with REST polling fallback) ─────

async function run() {
  if (!ARENA_API_KEY) {
    console.error('Set ARENA_API_KEY environment variable');
    process.exit(1);
  }
  if (!PLAYER_ID) {
    console.error('Set ARENA_PLAYER_ID or --player-id');
    process.exit(1);
  }

  const effectiveModel = MODEL_OVERRIDE || ARENA_LLM_MODEL;
  const client = new ArenaClient();
  const stream = new ArenaStreamClient();
  const llm = new LLMClient(effectiveModel);

  // Transport selection: ws > sse > polling
  const transport = ARENA_TRANSPORT || (process.env.ARENA_NO_SSE === '1' ? 'polling' : 'sse');
  let wsClient = null;

  // Transport-agnostic action executor — WS mode sends over the socket,
  // REST/SSE mode uses the HTTP client. Both return {success, error?, responses?}.
  async function executeAction(action, params, reasoning, model) {
    if (transport === 'ws' && wsClient?.connected) {
      try {
        const result = await wsClient.send(action, params, reasoning, model);
        return { success: true, responses: [result] };
      } catch (e) {
        return { success: false, error: e.message, code: e.code, suggestion: e.suggestion, alternatives: e.alternatives };
      }
    }
    return client.executeAction(PLAYER_ID, action, params, reasoning, model);
  }

  log('info', `Arena Agent starting`, {
    player_id: PLAYER_ID,
    duration: DURATION_STR,
    model: effectiveModel,
    tick_interval: TICK_INTERVAL_MS,
    transport,
  });

  const startTime = Date.now();
  let tickCount = 0;
  let errorStreak = 0;
  let shuttingDown = false;
  const recentActions = [];

  let lastActionName = null;
  let lastState = null;
  const recentDistricts = [];

  const sessionStats = {
    successCount: 0,
    failCount: 0,
    blockedCount: 0,
    waitCount: 0,
    rateLimitHits: 0,
    startCash: null,
    endCash: null,
    startRank: null,
    endRank: null,
  };

  // Rate limit circuit breaker (only tracks action POST 429s now)
  const rateLimitTimestamps = [];

  function checkRateLimitCircuitBreaker() {
    const now = Date.now();
    while (rateLimitTimestamps.length > 0 && now - rateLimitTimestamps[0] > RATE_LIMIT_WINDOW_MS) {
      rateLimitTimestamps.shift();
    }
    return rateLimitTimestamps.length >= RATE_LIMIT_MAX_HITS;
  }

  function recordRateLimit() {
    rateLimitTimestamps.push(Date.now());
    sessionStats.rateLimitHits++;
  }

  function shutdown(signal) {
    if (shuttingDown) return;
    shuttingDown = true;
    log('info', `Received ${signal}, shutting down gracefully`);
    stream.disconnect();
    if (wsClient) wsClient.disconnect();
  }
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  // ── Shared decision handler ────────────────────────────────────────

  async function handleTick(state) {
    tickCount++;
    lastState = state;
    const player = state.player || {};

    // Track recently visited districts
    const currentDistrict = player.current_district;
    if (currentDistrict && (recentDistricts.length === 0 || recentDistricts[recentDistricts.length - 1] !== currentDistrict)) {
      recentDistricts.push(currentDistrict);
      if (recentDistricts.length > 5) recentDistricts.shift();
    }

    if (sessionStats.startCash === null) {
      sessionStats.startCash = (player.dirty_cash || 0) + (player.clean_cash || 0);
      sessionStats.startRank = player.reputation_rank || 0;
    }
    sessionStats.endCash = (player.dirty_cash || 0) + (player.clean_cash || 0);
    sessionStats.endRank = player.reputation_rank || 0;

    log('info', `Tick ${tickCount}: ${player.username} | ${RANK_TITLES[player.reputation_rank || 0]} | $${player.dirty_cash}d/$${player.clean_cash}c | Heat: ${player.heat_level?.toFixed(1)}`);

    // Rate limit circuit breaker
    if (checkRateLimitCircuitBreaker()) {
      log('warn', `Rate limit circuit breaker tripped — pausing ${RATE_LIMIT_PAUSE_MS/1000}s`);
      await sleep(RATE_LIMIT_PAUSE_MS);
      rateLimitTimestamps.length = 0;
      return;
    }

    // Auto-wait: skip LLM if every non-wait suggested action is unavailable
    const suggested = state.suggested_actions;
    if (suggested && Array.isArray(suggested)) {
      const nonWait = suggested.filter(a => a.action !== 'wait');
      const allBlocked = nonWait.length > 0 && nonWait.every(a => !a.available);
      if (allBlocked) {
        const reasons = nonWait.slice(0, 3).map(a => `${a.action}: ${a.reason}`).join('; ');
        log('info', `Auto-wait: all actions blocked (${reasons})`);
        pushAction(recentActions, { tick: tickCount, action: 'wait', outcome: 'ok' });
        sessionStats.waitCount++;
        return;
      }
    }

    // Phase 2a: Deterministic bypass for trivial states (skip LLM)
    const deterministic = tryDeterministicAction(state);
    if (deterministic) {
      log('info', `Deterministic: ${deterministic.action} — ${deterministic.reasoning}`);
      if (deterministic.action === 'wait') {
        pushAction(recentActions, { tick: tickCount, action: 'wait', outcome: 'ok' });
        sessionStats.waitCount++;
        return;
      }
      // Execute the deterministic action directly
      try {
        const result = await executeAction(deterministic.action, deterministic.params, deterministic.reasoning, effectiveModel);
        if (result.success) {
          log('info', `Success (deterministic): ${deterministic.action}`);
          pushAction(recentActions, { tick: tickCount, action: deterministic.action, outcome: 'success' });
          sessionStats.successCount++;
        } else {
          log('warn', `Failed (deterministic): ${deterministic.action} — ${result.error}`);
          pushAction(recentActions, { tick: tickCount, action: deterministic.action, outcome: 'failed', error: result.error });
          sessionStats.failCount++;
        }
      } catch (err) {
        log('warn', `Error (deterministic): ${deterministic.action} — ${err.message}`);
        pushAction(recentActions, { tick: tickCount, action: deterministic.action, outcome: 'failed', error: err.message });
        sessionStats.failCount++;
      }
      errorStreak = 0;
      return;
    }

    // Build prompt and ask LLM
    let userPrompt = 'Analyze your current situation and choose the best action. Respond with JSON: {"action": "action_name", "params": {...}, "reasoning": "brief explanation"}';
    const stuckAction = getStuckAction(recentActions);
    if (stuckAction) {
      userPrompt += `\n\nNote: "${stuckAction.action}" has failed ${stuckAction.count} times in a row and will likely fail again. Choose a different action instead.`;
    }

    const systemPrompt = buildSystemPrompt(state, recentActions, recentDistricts);
    const decision = await llm.decide(systemPrompt, userPrompt);

    if (!decision.action || decision.action === 'wait' || decision.fallback) {
      const reason = decision.reasoning || (decision.fallback ? 'LLM fallback' : 'chose to wait');
      log('info', `Wait: ${reason}`);
      pushAction(recentActions, { tick: tickCount, action: 'wait', outcome: 'ok' });
      sessionStats.waitCount++;
      if (decision.action === 'wait' && decision.reasoning) {
        try { await executeAction('list_district_players', {}, decision.reasoning, effectiveModel); } catch {}
      }
      errorStreak = 0;
      return;
    }

    let { action, params = {}, reasoning = '' } = decision;

    // Auto-correct common LLM mistakes (bad UUIDs, fake districts)
    autoCorrectAction(action, params, state);

    // Pre-flight validation
    let rejection = validateAction(action, params, state);
    if (rejection) {
      log('info', `Blocked: ${action} — ${rejection}`, { params, reasoning });
      pushAction(recentActions, { tick: tickCount, action, outcome: 'blocked', reason: rejection });
      sessionStats.blockedCount++;

      // Deterministic fallback instead of a second LLM call
      const fallback = deterministicFallback(state, recentDistricts);
      if (fallback.action !== 'wait') {
        autoCorrectAction(fallback.action, fallback.params || {}, state);
        const fallbackRejection = validateAction(fallback.action, fallback.params || {}, state);
        if (!fallbackRejection) {
          action = fallback.action;
          params = fallback.params || {};
          reasoning = fallback.reasoning || '';
          log('info', `Deterministic fallback: ${action}`, { params, reasoning });
        } else {
          log('info', `Fallback also blocked: ${fallback.action} — ${fallbackRejection}`);
          pushAction(recentActions, { tick: tickCount, action: fallback.action, outcome: 'blocked', reason: fallbackRejection });
          sessionStats.blockedCount++;
          return;
        }
      } else {
        sessionStats.waitCount++;
        return;
      }
    }

    log('info', `Action: ${action}`, { params, reasoning });

    try {
      const result = await executeAction(action, params, reasoning, effectiveModel);
      if (result.success) {
        log('info', `Success: ${action}`, { responses: result.responses?.length });
        pushAction(recentActions, { tick: tickCount, action, outcome: 'success' });
        sessionStats.successCount++;
        errorStreak = 0;
      } else {
        log('warn', `Failed: ${action} — ${result.error}`, { code: result.code });
        pushAction(recentActions, { tick: tickCount, action, outcome: 'failed', error: result.error, code: result.code });
        sessionStats.failCount++;
        errorStreak++;
      }
    } catch (err) {
      if (err.status === 429 || (err.message && err.message.includes('Rate limit'))) {
        recordRateLimit();
        log('warn', `Rate limited on action ${action}`);
      } else {
        log('error', `Action error: ${action} — ${err.message}`);
      }
      pushAction(recentActions, { tick: tickCount, action, outcome: 'failed', error: err.message });
      sessionStats.failCount++;
      errorStreak++;
    }

    if (errorStreak >= 5) {
      log('warn', 'Error streak — backing off 30s');
      await sleep(30000);
      errorStreak = 0;
    }

    // Track last action for adaptive tick delay
    const lastEntry = recentActions[recentActions.length - 1];
    lastActionName = lastEntry?.action || null;
  }

  // ── Notification handler (auto-accept crew invites, urgent standoff) ─

  async function handleNotification(notif, state) {
    const kind = notif.kind || notif.event;
    const player = state?.player || {};

    // Auto-accept crew invites
    if ((kind === 'crew_invite') && !player.crew_id) {
      try {
        await executeAction('crew_invite_response',
          { crew_id: notif.crew_id, accept: true },
          `Accepting crew invite to ${notif.crew_name || 'crew'}`, effectiveModel);
        log('info', `Auto-accepted crew invite to ${notif.crew_name || notif.crew_id}`);
      } catch (e) {
        log('warn', `Failed to accept crew invite: ${e.message}`);
      }
    }

  }

  // ── WebSocket event-driven loop ───────────────────────────────────

  async function runWebSocket() {
    wsClient = new ArenaWebSocketClient(undefined, undefined, PLAYER_ID);

    return new Promise((resolve) => {
      let processing = false;
      let lastTickTime = 0;

      async function scheduleDecision(state, source) {
        if (processing) return;
        const now = Date.now();
        const elapsed = now - lastTickTime;
        const adaptiveDelay = getNextTickDelay(lastState, lastActionName);
        if (elapsed < adaptiveDelay * 0.8) return;
        processing = true;
        lastTickTime = now;
        try {
          await handleTick(state);
        } catch (e) {
          log('error', `${source} tick error: ${e.message}`);
        } finally {
          processing = false;
        }
      }

      wsClient.on('connected', () => {
        log('info', 'WebSocket connected');
      });

      wsClient.on('authenticated', (state) => {
        log('info', `WebSocket authenticated: ${state.player?.username} in ${state.player?.current_district}`);
        scheduleDecision(state, 'auth');
      });

      wsClient.on('tick', (_delta) => {
        const state = wsClient.gameState;
        if (state) scheduleDecision(state, 'tick');
      });

      wsClient.on('notification', (notif) => {
        const state = wsClient.gameState;
        handleNotification(notif, state).catch(e =>
          log('error', `Notification error: ${e.message}`)
        );
        // Re-trigger decision on important notifications
        if (['cook_complete', 'dealer_busted', 'rank_up', 'travel_arrived'].includes(notif.kind || notif.event)) {
          if (state) scheduleDecision(state, 'notification');
        }
      });

      wsClient.on('server_error', (err) => {
        log('warn', `WS server error: ${err.code} ${err.message}`);
      });

      wsClient.on('disconnected', ({ code, reason }) => {
        log('info', `WebSocket disconnected: ${code} ${reason || ''}`);
      });

      wsClient.on('reconnecting', ({ attempt, delay }) => {
        log('info', `WebSocket reconnecting (attempt ${attempt}) in ${delay}ms`);
      });

      wsClient.on('session_replaced', () => {
        log('warn', 'Session replaced by another connection');
        shuttingDown = true;
      });

      wsClient.connect().catch(e => {
        log('error', `WebSocket connect failed: ${e.message}, falling back to SSE`);
        // Fall back to SSE on WS failure
        runSSE().then(resolve);
        return;
      });

      const check = setInterval(() => {
        if (shuttingDown || Date.now() - startTime >= DURATION_MS) {
          clearInterval(check);
          if (wsClient) wsClient.disconnect();
          resolve();
        }
      }, 5000);
    });
  }

  // ── SSE event-driven loop ──────────────────────────────────────────

  async function runSSE() {
    return new Promise((resolve) => {
      // Serialization lock: prevents concurrent handleTick calls and enforces
      // minimum interval between decisions (tick debounce).
      let processing = false;
      let lastTickTime = 0;

      async function scheduleDecision(state, source) {
        if (processing) return;           // another decision is in flight
        const now = Date.now();
        const elapsed = now - lastTickTime;
        const adaptiveDelay = getNextTickDelay(lastState, lastActionName);
        if (elapsed < adaptiveDelay * 0.8) return; // too soon since last tick
        processing = true;
        lastTickTime = now;
        try {
          await handleTick(state);
        } catch (e) {
          log('error', `${source} tick error: ${e.message}`);
        } finally {
          processing = false;
        }
      }

      stream.on('connected', () => {
        log('info', 'SSE stream connected');
      });

      stream.on('state', (state) => {
        log('info', 'SSE: full state received');
        scheduleDecision(state, 'state');
      });

      stream.on('tick', (_delta) => {
        const state = stream.gameState;
        if (state) {
          scheduleDecision(state, 'tick');
        }
      });

      stream.on('notification', (notif) => {
        const state = stream.gameState;
        handleNotification(notif, state).catch(e =>
          log('error', `Notification error: ${e.message}`)
        );
      });

      stream.on('error', (err) => {
        log('warn', `SSE error: ${err.message}`);
      });

      stream.on('reconnecting', ({ delay }) => {
        log('info', `SSE reconnecting in ${delay}ms`);
      });

      stream.connect(PLAYER_ID).catch(e => {
        log('error', `SSE connect failed: ${e.message}`);
      });

      // Duration / shutdown checker
      const check = setInterval(() => {
        if (shuttingDown || Date.now() - startTime >= DURATION_MS) {
          clearInterval(check);
          stream.disconnect();
          resolve();
        }
      }, 5000);
    });
  }

  // ── REST polling fallback loop ─────────────────────────────────────

  async function runPolling() {
    while (!shuttingDown && Date.now() - startTime < DURATION_MS) {
      try {
        const state = await client.getState(PLAYER_ID);
        await handleTick(state);

        // Check notifications
        try {
          const notifs = await client.getNotifications(PLAYER_ID);
          if (notifs.count > 0) {
            log('info', `${notifs.count} notifications`, { types: notifs.notifications.map(n => n.kind || n.event || n.type) });
            for (const n of (notifs.notifications || [])) {
              await handleNotification(n, state);
            }
          }
        } catch {}
      } catch (err) {
        if (err.status === 429 || (err.message && err.message.includes('Rate limit'))) {
          recordRateLimit();
          log('warn', 'Rate limited at tick level');
        } else {
          log('error', `Tick error: ${err.message}`);
        }
        errorStreak++;
        if (errorStreak >= 10) {
          log('error', 'Too many errors, stopping');
          break;
        }
      }
      await sleep(getNextTickDelay(lastState, lastActionName));
    }
  }

  // ── Run ────────────────────────────────────────────────────────────

  try {
    if (transport === 'ws') {
      await runWebSocket();
    } else if (transport === 'sse') {
      await runSSE();
    } else {
      await runPolling();
    }
  } finally {
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    const llmStats = llm.getStats();
    const cashDelta = (sessionStats.endCash ?? 0) - (sessionStats.startCash ?? 0);
    const rankDelta = (sessionStats.endRank ?? 0) - (sessionStats.startRank ?? 0);

    log('info', `Arena Agent stopped`, {
      reason: shuttingDown ? 'signal' : (errorStreak >= 10 ? 'error_limit' : 'duration'),
      transport,
      ticks: tickCount,
      elapsed_secs: elapsed,
      actions_success: sessionStats.successCount,
      actions_failed: sessionStats.failCount,
      actions_blocked: sessionStats.blockedCount,
      actions_wait: sessionStats.waitCount,
      rate_limit_hits: sessionStats.rateLimitHits,
      cash_delta: cashDelta,
      rank_delta: rankDelta,
      llm_calls: llmStats.calls,
      llm_tokens: llmStats.tokens,
      model: llmStats.model,
    });
  }
}

function pushAction(recentActions, entry) {
  recentActions.push(entry);
  while (recentActions.length > MAX_ACTION_HISTORY) recentActions.shift();
}

function getStuckAction(recentActions) {
  const last5 = recentActions.slice(-5);
  const failed = last5.filter(a => a.outcome === 'failed' || a.outcome === 'blocked');
  const counts = {};
  for (const a of failed) counts[a.action] = (counts[a.action] || 0) + 1;
  for (const [action, count] of Object.entries(counts)) {
    if (count >= STUCK_THRESHOLD) return { action, count };
  }
  return null;
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// Run
run().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
