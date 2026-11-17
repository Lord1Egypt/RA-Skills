// stats.mjs — `pe stats`: where the time goes, and what to change. Reads runs.jsonl (CLI phases) and
// agent.jsonl (hooks/marks). Advice is rule-based and conservative: it names the phase and the lever.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { RUNS, LOG_DIR } from './trace.mjs';
const AGENT = process.env.PE_AGENT_LOG || join(LOG_DIR, 'agent.jsonl');
const lines = f => { try { return readFileSync(f, 'utf8').trim().split('\n').filter(Boolean).map(l => JSON.parse(l)); } catch { return []; } };
const pct = (a, p) => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
const ms = v => (v >= 1000 ? `${(v / 1000).toFixed(1)} s` : `${Math.round(v)} ms`);

export function cliStats(runs) {
  const by = {};
  for (const r of runs) for (const [k, v] of Object.entries(r.phases || {})) {
    const key = k.replace(/^plugin:.*/, 'plugins');
    (by[key] ||= []).push(v);
  }
  const total = runs.map(r => r.total_ms);
  return { runs: runs.length, total_p50: pct(total, 0.5), total_p95: pct(total, 0.95),
    phases: Object.entries(by).map(([k, v]) => ({ phase: k, n: v.length, p50: pct(v, 0.5), p95: pct(v, 0.95), sum: v.reduce((a, b) => a + b, 0) })).sort((a, b) => b.sum - a.sum) };
}

// A turn = UserPromptSubmit … Stop (hooks), or the first Mark … `mark end` (manual). Tool time = Σ(Post − Pre).
export function agentStats(events) {
  const turns = []; let cur = null; const pending = new Map();
  for (const e of events) {
    if (e.ev === 'UserPromptSubmit' || (e.ev === 'Mark' && !cur)) { cur = { start: e.t, session: e.session, tools: [], marks: [] }; turns.push(cur); if (e.ev === 'Mark') cur.marks.push([e.step, e.t]); continue; }
    if (!cur) continue;
    if (e.ev === 'PreToolUse') pending.set(e.id || e.tool + e.cmd, e);
    else if (e.ev === 'PostToolUse') { const p = pending.get(e.id || e.tool + e.cmd); if (p) { cur.tools.push({ tool: p.tool, cmd: p.cmd, pe: p.pe, ms: e.t - p.t }); pending.delete(e.id || e.tool + e.cmd); } }
    else if (e.ev === 'Mark') { cur.marks.push([e.step, e.t]); if (e.step === 'end') { cur.end = e.t; cur = null; } }
    else if (e.ev === 'Stop') { cur.end = e.t; cur = null; }
  }
  return turns.filter(t => t.end).map(t => {
    const total = t.end - t.start, tool = t.tools.reduce((a, x) => a + x.ms, 0), pe = t.tools.filter(x => x.pe).reduce((a, x) => a + x.ms, 0);
    const steps = t.marks.map(([n, at], k) => ({ step: n, ms: (t.marks[k + 1]?.[1] ?? t.end) - at })).filter(s => s.step !== 'end');
    return { session: t.session, total, tool, pe, model: total - tool, calls: t.tools.length, steps, slowest: [...t.tools].sort((a, b) => b.ms - a.ms).slice(0, 3) };
  });
}

export function advise(cli, turns, runs) {
  const tips = [];
  const ph = Object.fromEntries(cli.phases.map(p => [p.phase, p]));
  const router = cli.phases.filter(p => p.phase.startsWith('router:'));
  for (const r of router) if (r.p50 > 1000) tips.push(`${r.phase} 中位 ${ms(r.p50)}：有 TypeSafe key 用 typesafe（约 0.2 s），或 local（离线 0 ms）`);
  if (ph['form:mermaid']?.p95 > 300) tips.push(`Mermaid 渲染 p95 ${ms(ph['form:mermaid'].p95)}：有超大图，拆图或减少节点`);
  const hit = runs.reduce((a, r) => a + (r.counts?.cache_hit || 0), 0), miss = runs.reduce((a, r) => a + (r.counts?.cache_miss || 0), 0);
  if (hit + miss) tips.push(`路由缓存命中 ${Math.round(100 * hit / (hit + miss))}%（${hit}/${hit + miss} 块）`);
  const todo = runs.filter(r => r.cmd === 'route').map(r => r.counts?.todo || 0);
  if (todo.length && todo.reduce((a, b) => a + b, 0) / todo.length > 1) tips.push(`route 平均留下 ${(todo.reduce((a, b) => a + b, 0) / todo.length).toFixed(1)} 个 TODO，模型要写第二遍：用 pe answer 一遍出页，或在回答里直接写表格/列表，让派生器接管`);
  const errs = runs.filter(r => (r.counts?.errors || 0) > 0).length;
  if (errs) tips.push(`${errs} 次渲染因稿件错误失败：看 lint 规则 id，把常见坑写进 SKILL.md`);
  if (turns.length) {
    const m = turns.map(t => t.model / t.total), share = m.reduce((a, b) => a + b, 0) / m.length;
    const peShare = turns.reduce((a, t) => a + t.pe, 0) / Math.max(1, turns.reduce((a, t) => a + t.total, 0));
    if (share > 0.6) tips.push(`模型生成占回合 ${(share * 100).toFixed(0)}%：减少重写——只写一遍回答，交给 pe answer；不要先写回答再整篇改写成稿件`);
    if (peShare < 0.05) tips.push(`pe 自身只占 ${(peShare * 100).toFixed(1)}%：瓶颈不在脚本`);
    const nonPe = turns.flatMap(t => t.tools.filter(x => !x.pe && /Bash|shell/i.test(x.tool || ''))).length / turns.length;
    if (nonPe > 3) tips.push(`每回合平均 ${nonPe.toFixed(1)} 次非 pe 的命令：多为额外验证或调试，交付前只跑 pe check`);
  }
  return tips;
}

export function stats(opts = {}) {
  const last = Number(opts.last) || 50;
  const runs = lines(RUNS).slice(-last), events = lines(AGENT);
  const cli = cliStats(runs), turns = agentStats(events).slice(-last);
  const tips = advise(cli, turns, runs);
  if (opts.json) { console.log(JSON.stringify({ cli, turns, tips }, null, 2)); return 0; }
  console.log(`pe 运行 ${cli.runs} 次 · 总耗时中位 ${ms(cli.total_p50)} · p95 ${ms(cli.total_p95)}  (${RUNS})`);
  for (const p of cli.phases.slice(0, 12)) console.log(`  ${p.phase.padEnd(22)} p50 ${ms(p.p50).padStart(8)}  p95 ${ms(p.p95).padStart(8)}  ×${p.n}`);
  if (turns.length) {
    console.log(`\nAgent 回合 ${turns.length} 个  (${AGENT})`);
    for (const t of turns.slice(-5)) {
      console.log(`  回合 ${ms(t.total)}：模型 ${ms(t.model)} · 工具 ${ms(t.tool)}（其中 pe ${ms(t.pe)}）· ${t.calls} 次调用`);
      for (const s of t.steps) console.log(`    ${s.step.padEnd(16)} ${ms(s.ms)}`);
      for (const x of t.slowest) console.log(`    慢：${x.tool} ${ms(x.ms)} ${x.cmd || ''}`);
    }
  } else console.log('\n还没有 Agent 回合记录：Claude Code 装插件后自动记录；其他 Agent 用 hooks/agent-hook.mjs mark <步骤>。');
  if (tips.length) { console.log('\n建议'); tips.forEach(t => console.log('  · ' + t)); }
  return 0;
}
