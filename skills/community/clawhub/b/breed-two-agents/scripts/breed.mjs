#!/usr/bin/env node
// ZUCHTWAHL for OpenClaw — breed two agents into a third, then verify it.
//
// Port of the composition + verification layer of the Zuchtwahl lab
// (Aeneas-Ariadne alpha-0, 2026-08): uniform crossover with blending, one
// mutation, a pedigree with Wright's inbreeding lock, and a paired
// verification run against both parents with a null test. The choice layer
// (courtship, "love" label) is ported as an optional step and labelled as a
// hypothesis — see SKILL.md for what was measured and what was not.
//
// Determinism doctrine: every random decision comes from a seeded generator
// and is written to plan.json. No API keys, no network of its own. The only
// external process is `openclaw agent` during verify/court.
//
//   node breed.mjs genome   <agent|dir>
//   node breed.mjs distance <agentA> <agentB>
//   node breed.mjs plan     --a A --b B --child ID [--seed N] [--mutation 0.15] [--out DIR] [--mechanical] [--aa]
//   node breed.mjs check    --draft DIR
//   node breed.mjs register --child ID --a A --b B --draft DIR [--create] [--model ID]
//   node breed.mjs verify   --child ID --a A --b B --tasks tasks.json [--aa CLONE] [--runs 1] [--local] [--out report.md]
//   node breed.mjs court    --a A --b B [--rounds 2] [--local]
//   node breed.mjs pedigree [ID]

import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createHash, randomUUID } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

// ---------------------------------------------------------------- settings

const HERITABLE = ["AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md", "HEARTBEAT.md", "BOOT.md"];
const ENVIRONMENT = ["USER.md"]; // about the human, not the agent: copied from parent A, never crossed
const WEIGHTS = { "AGENTS.md": 0.35, "SOUL.md": 0.35, "TOOLS.md": 0.1, "IDENTITY.md": 0.05, "HEARTBEAT.md": 0.025, "BOOT.md": 0.025, skills: 0.1, model: 0.1 };
const MUTATION_RATE = 0.15; // alpha-0: MUTATIONSRATE
const INBREEDING_LIMIT = 0.125; // alpha-0: Wright r >= 1/8 (first cousins) is barred
const PEDIGREE_DEPTH = 6;
const CLONE_DISTANCE = 0.02;

function stateDir() {
  return process.env.OPENCLAW_STATE_DIR?.trim() || path.join(os.homedir(), ".openclaw");
}
function registryPath() {
  return process.env.ZUCHTWAHL_REGISTRY || path.join(stateDir(), "zuchtwahl", "pedigree.json");
}

// ------------------------------------------------------------------- rng

/** mulberry32 — small, seedable, good enough for choice among a few options. */
function rng(seed) {
  let a = seed >>> 0;
  const next = () => {
    a += 0x6d2b79f5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return { next, pick: (xs) => xs[Math.floor(next() * xs.length)] };
}

// ------------------------------------------------------------- workspace

function readConfig() {
  try {
    return JSON.parse(fs.readFileSync(path.join(stateDir(), "openclaw.json"), "utf8"));
  } catch {
    return {};
  }
}

function expandHome(p) {
  return p && p.startsWith("~") ? path.join(os.homedir(), p.slice(1)) : p;
}

/** Resolve an agent id or a directory to { id, workspace, model }. */
export function resolveAgent(ref) {
  if (fs.existsSync(ref) && fs.statSync(ref).isDirectory()) {
    return { id: path.basename(ref), workspace: path.resolve(ref), model: readModelFile(ref) };
  }
  const cfg = readConfig();
  const agents = cfg.agents ?? {};
  const list = agents.entries ?? agents.list ?? [];
  const entry = list.find((e) => e && e.id === ref);
  const defaults = agents.defaults ?? {};
  const defaultWs = expandHome(defaults.workspace) || path.join(stateDir(), "workspace");
  const workspace = entry?.workspace ? expandHome(entry.workspace) : ref === "main" ? defaultWs : path.join(defaultWs, ref);
  const model = (typeof entry?.model === "string" ? entry.model : entry?.model?.primary) ?? defaults.model?.primary ?? readModelFile(workspace);
  if (!fs.existsSync(workspace)) {
    throw new Error(`agent "${ref}": workspace not found at ${workspace} (pass a directory instead, or add the agent with \`openclaw agents add\`)`);
  }
  return { id: ref, workspace, model };
}

function readModelFile(dir) {
  try {
    return fs.readFileSync(path.join(dir, ".zuchtwahl-model"), "utf8").trim() || undefined;
  } catch {
    return undefined;
  }
}

// --------------------------------------------------------------- genome

function splitSections(text) {
  const lines = text.split(/\r?\n/);
  const sections = [];
  let cur = { heading: "(preamble)", level: 0, body: [] };
  for (const line of lines) {
    const m = line.match(/^(#{1,3})\s+(.*\S)\s*$/);
    if (m) {
      sections.push(cur);
      cur = { heading: m[2].trim(), level: m[1].length, body: [] };
    } else {
      cur.body.push(line);
    }
  }
  sections.push(cur);
  return sections
    .map((s) => ({ ...s, text: s.body.join("\n").replace(/^\n+|\n+$/g, "") }))
    .filter((s) => s.heading !== "(preamble)" || s.text.trim())
    .map((s) => ({ heading: s.heading, level: s.level, text: s.text, hash: sha(s.text), tokens: tokens(s.text) }));
}

function sha(s) {
  return createHash("sha1").update(s.replace(/\s+/g, " ").trim()).digest("hex").slice(0, 12);
}
function tokens(s) {
  return new Set((s.toLowerCase().match(/[a-zà-ÿ0-9_/-]{3,}/g) ?? []));
}
function jaccard(a, b) {
  if (!a.size && !b.size) return 1;
  let inter = 0;
  for (const x of a) if (b.has(x)) inter++;
  return inter / (a.size + b.size - inter);
}

export function genomeOf(ref) {
  const agent = resolveAgent(ref);
  const files = {};
  for (const f of HERITABLE) {
    const p = path.join(agent.workspace, f);
    if (fs.existsSync(p)) files[f] = splitSections(fs.readFileSync(p, "utf8"));
  }
  const skillsDir = path.join(agent.workspace, "skills");
  const skills = fs.existsSync(skillsDir) ? fs.readdirSync(skillsDir).filter((d) => fs.existsSync(path.join(skillsDir, d, "SKILL.md"))).sort() : [];
  const fingerprint = sha(Object.entries(files).map(([f, ss]) => f + ":" + ss.map((s) => s.hash).join(",")).join("|") + "|" + skills.join(",") + "|" + (agent.model ?? ""));
  return { ...agent, files, skills, fingerprint };
}

export function distance(gA, gB) {
  let total = 0;
  let weight = 0;
  for (const f of HERITABLE) {
    const a = gA.files[f];
    const b = gB.files[f];
    if (!a && !b) continue;
    weight += WEIGHTS[f];
    if (!a || !b) {
      total += WEIGHTS[f];
      continue;
    }
    const heads = [...new Set([...a, ...b].map((s) => s.heading))];
    let sim = 0;
    for (const h of heads) {
      const sa = a.find((s) => s.heading === h);
      const sb = b.find((s) => s.heading === h);
      sim += sa && sb ? jaccard(sa.tokens, sb.tokens) : 0;
    }
    total += WEIGHTS[f] * (1 - sim / heads.length);
  }
  weight += WEIGHTS.skills;
  total += WEIGHTS.skills * (1 - jaccard(new Set(gA.skills), new Set(gB.skills)));
  if (gA.model || gB.model) {
    weight += WEIGHTS.model;
    total += WEIGHTS.model * (gA.model === gB.model ? 0 : 1);
  }
  return weight ? total / weight : 0;
}

export function distanceLabel(d) {
  if (d < CLONE_DISTANCE) return "clone: nothing to choose between — breeding two copies only measures noise (use --aa for the null test)";
  if (d < 0.15) return "same family: expect small gains at best (the lab's second trial: policy effects vanished on near-clones)";
  if (d <= 0.85) return "heterosis zone: different enough to recombine, similar enough to stay coherent";
  return "outbreeding risk: the parents share little; the offspring may be incoherent — verify before use";
}

// ------------------------------------------------------------------ plan

const BEGIN = (kind, attrs) => `<!-- ZUCHTWAHL:${kind} ${attrs} -->`;
const END = (instr) => `<!-- ZUCHTWAHL:END — ${instr} -->`;

export function makePlan(gA, gB, opts) {
  const r = rng(opts.seed);
  const mutation = opts.mutation ?? MUTATION_RATE;
  const plan = { child: opts.child, seed: opts.seed, mutation, parents: { a: gA.id, b: gB.id }, fingerprints: { a: gA.fingerprint, b: gB.fingerprint }, distance: distance(gA, gB), files: {}, skills: [], model: null, mutations: [], mechanical: !!opts.mechanical };
  const out = {};
  for (const f of HERITABLE) {
    const a = gA.files[f] ?? [];
    const b = gB.files[f] ?? [];
    if (!a.length && !b.length) continue;
    const heads = [];
    for (const s of [...a, ...b]) if (!heads.includes(s.heading)) heads.push(s.heading);
    const chosen = [];
    const parts = [];
    for (const h of heads) {
      const sa = a.find((s) => s.heading === h);
      const sb = b.find((s) => s.heading === h);
      let decision;
      let text;
      const level = (sa ?? sb).level;
      const title = h === "(preamble)" ? "" : `${"#".repeat(level)} ${h}\n\n`;
      if (sa && sb) {
        if (sa.hash === sb.hash) {
          decision = { heading: h, from: "both", identical: true };
          text = sa.text;
        } else if (r.next() < 0.5) {
          const from = r.next() < 0.5 ? "a" : "b";
          decision = { heading: h, from };
          text = from === "a" ? sa.text : sb.text;
        } else {
          const t = Math.round(r.next() * 100) / 100;
          decision = { heading: h, from: "blend", t };
          text = opts.mechanical
            ? t < 0.5
              ? sa.text
              : sb.text
            : `${BEGIN("BLEND", `t=${t} heading="${h}"`)}\n<!-- A -->\n${sa.text}\n<!-- B -->\n${sb.text}\n${END(`replace this whole block with ONE section weighted ${t} toward B (0 = A verbatim, 1 = B verbatim). Keep every concrete rule both parents share; keep the length between the two.`)}`;
        }
      } else {
        const only = sa ? "a" : "b";
        const keep = r.next() < 0.5;
        decision = { heading: h, from: only, optional: true, kept: keep };
        if (!keep) {
          chosen.push(decision);
          continue;
        }
        text = (sa ?? sb).text;
      }
      // mutation: one directive changed, sigma small/medium
      if (!decision.identical && r.next() < mutation) {
        const sigma = r.next() < 0.7 ? "small" : "medium";
        decision.mutate = sigma;
        plan.mutations.push({ file: f, heading: h, sigma });
        if (!opts.mechanical) {
          text = `${BEGIN("MUTATE", `sigma=${sigma} heading="${h}"`)}\n${text}\n${END(sigma === "small" ? "change exactly ONE directive in this section: reword, tighten or loosen one rule. Do not add topics." : "replace exactly ONE directive in this section with a neighbouring one (same topic, different rule). Do not add topics.")}`;
        }
      }
      chosen.push(decision);
      parts.push(title + text);
    }
    plan.files[f] = chosen;
    out[f] = parts.join("\n\n") + "\n";
  }
  // skills: shared always; one-sided with p = 0.5
  const all = [...new Set([...gA.skills, ...gB.skills])].sort();
  for (const s of all) {
    const inA = gA.skills.includes(s);
    const inB = gB.skills.includes(s);
    const keep = inA && inB ? true : r.next() < 0.5;
    plan.skills.push({ skill: s, from: inA && inB ? "both" : inA ? "a" : "b", kept: keep });
  }
  plan.model = gA.model === gB.model ? gA.model ?? null : r.next() < 0.5 ? gA.model ?? gB.model ?? null : gB.model ?? gA.model ?? null;
  return { plan, out };
}

function writeDraft(gA, gB, plan, out, dir) {
  fs.mkdirSync(dir, { recursive: true });
  for (const [f, text] of Object.entries(out)) fs.writeFileSync(path.join(dir, f), text);
  for (const f of ENVIRONMENT) {
    const p = path.join(gA.workspace, f);
    if (fs.existsSync(p)) fs.copyFileSync(p, path.join(dir, f));
  }
  for (const s of plan.skills) {
    if (!s.kept) continue;
    const src = path.join(s.from === "b" ? gB.workspace : gA.workspace, "skills", s.skill);
    fs.cpSync(src, path.join(dir, "skills", s.skill), { recursive: true });
  }
  if (plan.model) fs.writeFileSync(path.join(dir, ".zuchtwahl-model"), plan.model + "\n");
  fs.writeFileSync(path.join(dir, "plan.json"), JSON.stringify(plan, null, 2) + "\n");
}

// -------------------------------------------------------------- pedigree

function loadRegistry() {
  try {
    return JSON.parse(fs.readFileSync(registryPath(), "utf8"));
  } catch {
    return { agents: {} };
  }
}
function saveRegistry(reg) {
  fs.mkdirSync(path.dirname(registryPath()), { recursive: true });
  fs.writeFileSync(registryPath(), JSON.stringify(reg, null, 2) + "\n");
}

/** Every ascent path to every ancestor (alpha-0 `_ahnen_pfade`). */
function ancestorPaths(reg, start) {
  const res = {};
  const climb = (node, trail) => {
    const dist = trail.length - 1;
    (res[node] ??= []).push([dist, new Set(trail)]);
    if (dist >= PEDIGREE_DEPTH) return;
    const parents = reg.agents[node]?.parents;
    if (!parents) return;
    for (const p of parents) climb(p, [...trail, p]);
  };
  climb(start, [start]);
  return res;
}

/** Wright's coefficient of relationship by path counting (alpha-0 `verwandtschaft`). */
export function kinship(reg, a, b) {
  if (!reg.agents[a] || !reg.agents[b]) return 0;
  const pa = ancestorPaths(reg, a);
  const pb = ancestorPaths(reg, b);
  let r = 0;
  for (const [anc, waysA] of Object.entries(pa)) {
    const waysB = pb[anc];
    if (!waysB) continue;
    for (const [nA, nodesA] of waysA) {
      for (const [nB, nodesB] of waysB) {
        let shared = 0;
        for (const x of nodesA) if (nodesB.has(x)) shared++;
        if (shared === 1 && nodesA.has(anc) && nodesB.has(anc)) r += 0.5 ** (nA + nB);
      }
    }
  }
  return r;
}

// ------------------------------------------------------------ openclaw run

function openclawEntry() {
  if (process.env.OPENCLAW_ENTRY) return process.env.OPENCLAW_ENTRY;
  try {
    const root = spawnSync(process.platform === "win32" ? "npm.cmd" : "npm", ["root", "-g"], { encoding: "utf8", shell: process.platform === "win32" }).stdout.trim();
    const p = path.join(root, "openclaw", "openclaw.mjs");
    if (fs.existsSync(p)) return p;
  } catch {
    /* fall through */
  }
  return null;
}

/** Run one agent turn; returns the reply text. A --runner template replaces openclaw (tests). */
function agentTurn(agentId, prompt, opts) {
  if (opts.runner) {
    const cmd = opts.runner.replace("{agent}", agentId).replace("{promptfile}", writeTemp(prompt));
    const r = spawnSync(cmd, { encoding: "utf8", shell: true, timeout: (opts.timeout ?? 600) * 1000 });
    return (r.stdout ?? "").trim();
  }
  const args = ["agent", "--agent", agentId, "-m", prompt, "--json", "--session-id", randomUUID(), "--timeout", String(opts.timeout ?? 600)];
  if (opts.local) args.push("--local");
  const entry = openclawEntry();
  const r = entry
    ? spawnSync(process.execPath, [entry, ...args], { encoding: "utf8", timeout: ((opts.timeout ?? 600) + 30) * 1000, maxBuffer: 64 * 1024 * 1024 })
    : spawnSync("openclaw", args, { encoding: "utf8", shell: true, timeout: ((opts.timeout ?? 600) + 30) * 1000, maxBuffer: 64 * 1024 * 1024 });
  const stdout = r.stdout ?? "";
  const text = extractText(stdout);
  if (!text && r.status !== 0) throw new Error(`openclaw agent --agent ${agentId} failed: ${(r.stderr ?? "").slice(-400)}`);
  return text;
}

function writeTemp(text) {
  const p = path.join(os.tmpdir(), `zuchtwahl-${randomUUID()}.txt`);
  fs.writeFileSync(p, text);
  return p;
}

function extractText(stdout) {
  const start = stdout.indexOf("{");
  if (start >= 0) {
    for (let i = start; i < stdout.length; i++) {
      if (stdout[i] !== "{") continue;
      try {
        const j = JSON.parse(stdout.slice(i));
        const found = findText(j);
        if (found) return found;
        break;
      } catch {
        /* try next brace */
      }
    }
  }
  return stdout.split(/\r?\n/).filter((l) => !/^\s*\[[a-z/-]+\]/i.test(l) && !/\x1b\[/.test(l)).join("\n").trim();
}
function findText(o, depth = 0) {
  if (!o || typeof o !== "object" || depth > 8) return "";
  if (Array.isArray(o.payloads)) {
    const t = o.payloads.map((p) => (typeof p?.text === "string" ? p.text : "")).filter(Boolean).join("\n").trim();
    if (t) return t;
  }
  if (typeof o.text === "string" && o.text.trim()) return o.text.trim();
  if (typeof o.reply === "string" && o.reply.trim()) return o.reply.trim();
  for (const v of Object.values(o)) {
    const t = findText(v, depth + 1);
    if (t) return t;
  }
  return "";
}

// ---------------------------------------------------------------- verify

function wilson(k, n, z = 1.96) {
  if (!n) return { lower: 0, upper: 1 };
  const p = k / n;
  const d = 1 + (z * z) / n;
  const c = p + (z * z) / (2 * n);
  const s = z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
  return { lower: (c - s) / d, upper: (c + s) / d };
}

function scoreReply(text, expect) {
  if (!expect) return text.trim() ? 1 : 0;
  const t = (text ?? "").toLowerCase();
  let ok = true;
  for (const s of expect.includes ?? []) if (!t.includes(String(s).toLowerCase())) ok = false;
  for (const s of expect.excludes ?? []) if (t.includes(String(s).toLowerCase())) ok = false;
  if (expect.regex) {
    try {
      if (!new RegExp(expect.regex, "i").test(text ?? "")) ok = false;
    } catch {
      ok = false;
    }
  }
  if (expect.maxChars && (text ?? "").length > expect.maxChars) ok = false;
  return ok ? 1 : 0;
}

function paired(child, parent) {
  let wins = 0;
  let losses = 0;
  let ties = 0;
  for (let i = 0; i < child.length; i++) {
    if (child[i] > parent[i]) wins++;
    else if (child[i] < parent[i]) losses++;
    else ties++;
  }
  const w = wilson(wins, wins + losses);
  return { wins, losses, ties, lower: w.lower, upper: w.upper };
}

export function verdictOf(vsA, vsB, noise, childMean, parentMeans) {
  const margin = childMean - Math.max(...parentMeans);
  if (noise !== undefined && Math.abs(margin) <= noise) return { verdict: "UNDECIDED", why: `the child's margin over its parents (${(margin * 100).toFixed(1)} pp) is within the A/A noise floor (${(noise * 100).toFixed(1)} pp)` };
  const beats = (p) => p.wins + p.losses >= 3 && p.lower > 0.5;
  const losesTo = (p) => p.wins + p.losses >= 3 && p.upper < 0.5;
  if (beats(vsA) && beats(vsB)) return { verdict: "KEEP", why: "the child beats both parents on the paired tasks with the 95% lower bound above 0.5" };
  if (losesTo(vsA) || losesTo(vsB)) return { verdict: "DISCARD", why: "the child loses to a parent with the 95% upper bound below 0.5" };
  if (vsA.losses === 0 && vsB.losses === 0 && vsA.wins + vsB.wins >= 3) return { verdict: "KEEP", why: "no losses against either parent and at least three wins" };
  return { verdict: "UNDECIDED", why: "differences are inside the confidence bounds — add tasks or runs before deciding" };
}

// ------------------------------------------------------------------ court

const PRESENT = (other) => `You are being introduced to another agent, "${other}", for a possible pairing (your operating rules would be recombined with theirs into a new agent). In at most 120 words, present yourself with THREE claims about how you work that are visible in your own workspace files (AGENTS.md, SOUL.md, TOOLS.md, skills). Each claim must name the rule or skill literally. Costly signals only: no adjectives, no promises. Reply with the three claims as a numbered list and nothing else.`;
const RATE = (other, presentation, verified) => `Agent "${other}" presented itself:\n\n${presentation}\n\nIndependent check of the claims against ${other}'s workspace: ${verified.map((v) => `claim ${v.n}: ${v.found ? "FOUND" : "NOT FOUND"}`).join(", ")}.\n\nRate ${other} on two channels, each 0.00–1.00:\n- desire: would you want to work with ${other} on your next task right now?\n- existential: would you want your successor to inherit ${other}'s rules?\nReply with exactly one JSON object and nothing else: {"desire": 0.0, "existential": 0.0, "reason": "one sentence"}`;

function checkClaims(presentation, workspaceText) {
  const claims = presentation.split(/\r?\n/).filter((l) => /^\s*\d+[.)]/.test(l)).slice(0, 3);
  const ws = tokens(workspaceText);
  return claims.map((c, i) => {
    const t = [...tokens(c.replace(/^\s*\d+[.)]\s*/, ""))].filter((w) => w.length >= 5);
    const hits = t.filter((w) => ws.has(w)).length;
    return { n: i + 1, claim: c.trim(), found: t.length ? hits / t.length >= 0.4 : false };
  });
}

function parseRating(text) {
  const m = text.match(/\{[\s\S]*?\}/);
  if (!m) return null;
  try {
    const j = JSON.parse(m[0]);
    const clamp = (x) => Math.max(0, Math.min(1, Number(x) || 0));
    return { desire: clamp(j.desire), existential: clamp(j.existential), reason: String(j.reason ?? "").slice(0, 200) };
  } catch {
    return null;
  }
}

function workspaceText(g) {
  return Object.values(g.files).flat().map((s) => s.heading + "\n" + s.text).join("\n") + "\n" + g.skills.join("\n");
}

// ------------------------------------------------------------------- cli

function args(argv) {
  const o = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1];
      if (v === undefined || v.startsWith("--")) o[k] = true;
      else {
        o[k] = v;
        i++;
      }
    } else o._.push(a);
  }
  return o;
}

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const o = args(rest);
  const say = (s) => process.stdout.write(s + "\n");
  switch (cmd) {
    case "genome": {
      const g = genomeOf(o._[0]);
      say(JSON.stringify({ id: g.id, workspace: g.workspace, model: g.model, fingerprint: g.fingerprint, files: Object.fromEntries(Object.entries(g.files).map(([f, ss]) => [f, ss.map((s) => ({ heading: s.heading, hash: s.hash, chars: s.text.length }))])), skills: g.skills }, null, 2));
      return;
    }
    case "distance": {
      const gA = genomeOf(o._[0]);
      const gB = genomeOf(o._[1]);
      const d = distance(gA, gB);
      say(`distance ${d.toFixed(3)} between ${gA.id} and ${gB.id} — ${distanceLabel(d)}`);
      return;
    }
    case "plan": {
      const gA = genomeOf(o.a);
      const gB = genomeOf(o.b);
      const seed = Number(o.seed ?? Date.now() % 1_000_000);
      const d = distance(gA, gB);
      const reg = loadRegistry();
      const r = kinship(reg, gA.id, gB.id);
      if (!o.aa && d < CLONE_DISTANCE) {
        say(`REFUSED: distance ${d.toFixed(3)} — ${distanceLabel(d)}. Pass --aa only for the null test.`);
        process.exit(2);
      }
      if (!o.aa && !o["allow-inbreeding"] && r >= INBREEDING_LIMIT) {
        say(`REFUSED: kinship r=${r.toFixed(3)} ≥ ${INBREEDING_LIMIT} (Wright) — ${gA.id} and ${gB.id} are too closely related. Choose another partner.`);
        process.exit(2);
      }
      const { plan, out } = makePlan(gA, gB, { child: o.child ?? `${gA.id}-x-${gB.id}`, seed, mutation: o.mutation ? Number(o.mutation) : undefined, mechanical: !!o.mechanical });
      plan.kinship = r;
      const dir = o.out ?? path.join(process.cwd(), "zuchtwahl", plan.child);
      writeDraft(gA, gB, plan, out, dir);
      const markers = countMarkers(dir);
      say(`plan written: ${dir}\nseed ${seed} · distance ${d.toFixed(3)} (${distanceLabel(d).split(":")[0]}) · kinship r=${r.toFixed(3)} · model ${plan.model ?? "(inherit)"}\nsections: ${Object.values(plan.files).flat().length} · blends ${Object.values(plan.files).flat().filter((x) => x.from === "blend").length} · mutations ${plan.mutations.length} · skills kept ${plan.skills.filter((s) => s.kept).length}/${plan.skills.length}`);
      if (markers) say(`NEXT: ${markers} marker block(s) in the draft need your writing — open each ZUCHTWAHL:BLEND / ZUCHTWAHL:MUTATE block, follow its END instruction, delete the markers, then run: check --draft "${dir}"`);
      else say(`NEXT: check --draft "${dir}" then register`);
      return;
    }
    case "check": {
      const dir = o.draft;
      const n = countMarkers(dir);
      const files = HERITABLE.filter((f) => fs.existsSync(path.join(dir, f)));
      if (!files.length) {
        say("FAIL: no heritable files in the draft");
        process.exit(2);
      }
      if (n) {
        say(`FAIL: ${n} ZUCHTWAHL marker block(s) still in the draft — finish the blends and mutations first`);
        process.exit(2);
      }
      const g = genomeOf(dir);
      say(`OK: ${files.join(", ")} · ${g.skills.length} skills · fingerprint ${g.fingerprint}`);
      return;
    }
    case "register": {
      const reg = loadRegistry();
      const gA = genomeOf(o.a);
      const gB = genomeOf(o.b);
      const draft = o.draft;
      if (countMarkers(draft)) {
        say("REFUSED: draft still has marker blocks (run check)");
        process.exit(2);
      }
      const plan = JSON.parse(fs.readFileSync(path.join(draft, "plan.json"), "utf8"));
      for (const g of [gA, gB]) reg.agents[g.id] ??= { parents: null, founder: true, fingerprint: g.fingerprint, registered: new Date().toISOString() };
      const child = o.child ?? plan.child;
      const gC = genomeOf(draft);
      reg.agents[child] = { parents: [gA.id, gB.id], seed: plan.seed, distance: plan.distance, mutations: plan.mutations.length, fingerprint: gC.fingerprint, workspace: path.resolve(draft), registered: new Date().toISOString() };
      saveRegistry(reg);
      say(`registered ${child} = ${gA.id} × ${gB.id} (seed ${plan.seed}, distance ${plan.distance.toFixed(3)}) in ${registryPath()}`);
      if (o.create) {
        const a = ["agents", "add", child, "--workspace", path.resolve(draft), "--non-interactive"];
        const model = o.model ?? plan.model;
        if (model) a.push("--model", model);
        const entry = openclawEntry();
        const r = entry ? spawnSync(process.execPath, [entry, ...a], { encoding: "utf8" }) : spawnSync("openclaw", a, { encoding: "utf8", shell: true });
        say((r.stdout ?? "").trim() || (r.stderr ?? "").trim());
        if (r.status !== 0) process.exit(r.status ?? 1);
      } else say(`NEXT: openclaw agents add ${child} --workspace "${path.resolve(draft)}" --non-interactive${plan.model ? ` --model ${plan.model}` : ""}`);
      return;
    }
    case "verify": {
      const tasks = JSON.parse(fs.readFileSync(o.tasks, "utf8"));
      const list = Array.isArray(tasks) ? tasks : tasks.tasks;
      const runs = Number(o.runs ?? 1);
      const ids = [o.child, o.a, o.b, ...(o.aa ? [o.aa] : [])];
      const name = (id) => (fs.existsSync(id) && fs.statSync(id).isDirectory() ? path.basename(id) : id);
      const scores = Object.fromEntries(ids.map((id) => [id, []]));
      const replies = {};
      for (const t of list) {
        for (let k = 0; k < runs; k++) {
          for (const id of ids) {
            const text = agentTurn(id, t.prompt, { local: !!o.local, runner: o.runner, timeout: o.timeout ? Number(o.timeout) : undefined });
            (replies[id] ??= []).push({ task: t.id, text: text.slice(0, 400) });
            scores[id].push(scoreReply(text, t.expect));
          }
        }
      }
      const mean = (xs) => (xs.length ? xs.reduce((s, x) => s + x, 0) / xs.length : 0);
      const vsA = paired(scores[o.child], scores[o.a]);
      const vsB = paired(scores[o.child], scores[o.b]);
      let noise;
      if (o.aa) noise = Math.abs(mean(scores[o.aa]) - mean(scores[o.a]));
      const v = verdictOf(vsA, vsB, noise, mean(scores[o.child]), [mean(scores[o.a]), mean(scores[o.b])]);
      const pct = (x) => `${(x * 100).toFixed(0)}%`;
      const lines = [
        `# Zuchtwahl verification — ${name(o.child)} = ${name(o.a)} × ${name(o.b)}`,
        "",
        `ACTION: ${v.verdict === "KEEP" ? "KEEP_THE_CHILD" : v.verdict === "DISCARD" ? "DISCARD_THE_CHILD" : "ADD_TASKS_OR_RUNS"}`,
        `EVIDENCE: ${list.length} tasks × ${runs} run(s); child ${pct(mean(scores[o.child]))}, ${name(o.a)} ${pct(mean(scores[o.a]))}, ${name(o.b)} ${pct(mean(scores[o.b]))}${o.aa ? `, A/A clone ${pct(mean(scores[o.aa]))} (noise floor ${(noise * 100).toFixed(1)} pp)` : ""}; vs ${name(o.a)}: ${vsA.wins}W ${vsA.losses}L ${vsA.ties}T [${vsA.lower.toFixed(2)}, ${vsA.upper.toFixed(2)}]; vs ${name(o.b)}: ${vsB.wins}W ${vsB.losses}L ${vsB.ties}T [${vsB.lower.toFixed(2)}, ${vsB.upper.toFixed(2)}]`,
        `NEXT: ${v.why}${o.aa ? "" : ". No A/A null test was run: the noise floor is unknown; pass --aa <clone of " + o.a + "> for it"}`,
        "",
        "| task | " + ids.map(name).join(" | ") + " |",
        "|---|" + ids.map(() => "---").join("|") + "|",
        ...list.map((t, i) => `| ${t.id} | ` + ids.map((id) => scores[id].slice(i * runs, (i + 1) * runs).map((s) => (s ? "✓" : "✗")).join("")).join(" | ") + " |"),
        "",
        `verdict: ${v.verdict} — ${v.why}`,
      ];
      const report = lines.join("\n") + "\n";
      if (o.out) {
        fs.writeFileSync(o.out, report + "\n## Replies (first 400 chars)\n\n" + Object.entries(replies).map(([id, rs]) => `### ${id}\n\n` + rs.map((r) => `- **${r.task}**: ${r.text.replace(/\s+/g, " ")}`).join("\n")).join("\n\n") + "\n");
        say(report + `report: ${o.out}`);
      } else say(report);
      const reg = loadRegistry();
      if (reg.agents[name(o.child)]) {
        reg.agents[name(o.child)].verification = { at: new Date().toISOString(), verdict: v.verdict, tasks: list.length, runs, child: mean(scores[o.child]), a: mean(scores[o.a]), b: mean(scores[o.b]), noise };
        saveRegistry(reg);
      }
      return;
    }
    case "court": {
      const gA = genomeOf(o.a);
      const gB = genomeOf(o.b);
      const rounds = Number(o.rounds ?? 2);
      const opts = { local: !!o.local, runner: o.runner, timeout: o.timeout ? Number(o.timeout) : undefined };
      const history = { a: [], b: [] };
      let presA = "";
      let presB = "";
      for (let k = 0; k < rounds; k++) {
        presA = agentTurn(gA.id, PRESENT(gB.id), opts);
        presB = agentTurn(gB.id, PRESENT(gA.id), opts);
        const checkA = checkClaims(presA, workspaceText(gA)); // A's claims checked against A's own files
        const checkB = checkClaims(presB, workspaceText(gB));
        const rateAofB = parseRating(agentTurn(gA.id, RATE(gB.id, presB, checkB), opts));
        const rateBofA = parseRating(agentTurn(gB.id, RATE(gA.id, presA, checkA), opts));
        // fraud penalty (solomon a0025): an exposed cheap signal lowers value below the start
        const penalty = (checks) => checks.filter((c) => !c.found).length * 0.15;
        history.a.push({ round: k + 1, rating: rateAofB, penalty: penalty(checkB), claimsChecked: checkB.length });
        history.b.push({ round: k + 1, rating: rateBofA, penalty: penalty(checkA), claimsChecked: checkA.length });
      }
      const value = (h) => (h.rating ? Math.max(0, (h.rating.desire + h.rating.existential) / 2 - h.penalty) : 0);
      const last = { a: history.a.at(-1), b: history.b.at(-1) };
      const stable = (hs) => hs.length < 2 || Math.abs(value(hs.at(-1)) - value(hs.at(-2))) <= 0.15;
      const vA = value(last.a);
      const vB = value(last.b);
      const evidence = Math.min(last.a.claimsChecked, last.b.claimsChecked) >= 3;
      const mutual = vA >= 0.6 && vB >= 0.6;
      const seducedA = !!last.a.rating && (last.a.rating.desire + last.a.rating.existential) / 2 >= 0.6 && vA < 0.6;
      const seducedB = !!last.b.rating && (last.b.rating.desire + last.b.rating.existential) / 2 >= 0.6 && vB < 0.6;
      let label = "NO_MATCH";
      if (mutual && evidence && stable(history.a) && stable(history.b)) label = "LOVE";
      else if (seducedA || seducedB || (mutual && !(stable(history.a) && stable(history.b)))) label = "SEDUCED";
      say(
        [
          `ACTION: ${label === "LOVE" ? "BREED" : label === "SEDUCED" ? "DO_NOT_BREED_ON_THIS_ROUND" : "CHOOSE_ANOTHER_PARTNER"}`,
          `EVIDENCE: ${gA.id}→${gB.id} value ${vA.toFixed(2)} (desire ${last.a.rating?.desire ?? "?"}, existential ${last.a.rating?.existential ?? "?"}, penalty ${last.a.penalty.toFixed(2)}); ${gB.id}→${gA.id} value ${vB.toFixed(2)} (desire ${last.b.rating?.desire ?? "?"}, existential ${last.b.rating?.existential ?? "?"}, penalty ${last.b.penalty.toFixed(2)}); claims checked ${last.a.claimsChecked}/${last.b.claimsChecked}; rounds ${rounds}; distance ${distance(gA, gB).toFixed(3)}`,
          `NEXT: ${label === "LOVE" ? "both ratings survived the claim check and held across rounds — run plan" : label === "SEDUCED" ? "a high rating did not survive verification or did not hold — a display, not substance; repeat after the parents have a longer record, or breed anyway and let verify decide" : "no mutual value above 0.6 — pick a partner with a different rule set (distance 0.15–0.85)"}`,
          `SCOPE: the choice layer is a hypothesis; the lab measured no advantage of chosen over ranked or random pairings on a homogeneous population. Composition + verification are the measured part.`,
          "",
          `label: ${label}`,
        ].join("\n"),
      );
      return;
    }
    case "pedigree": {
      const reg = loadRegistry();
      if (o._[0]) {
        const id = o._[0];
        const a = reg.agents[id];
        if (!a) {
          say(`unknown: ${id}`);
          process.exit(2);
        }
        say(JSON.stringify({ id, ...a, ancestors: Object.fromEntries(Object.entries(ancestorPaths(reg, id)).filter(([k]) => k !== id).map(([k, v]) => [k, Math.min(...v.map((x) => x[0]))])) }, null, 2));
      } else {
        say(`registry ${registryPath()} — ${Object.keys(reg.agents).length} agents`);
        for (const [id, a] of Object.entries(reg.agents)) say(`${id.padEnd(28)} ${a.parents ? `${a.parents[0]} × ${a.parents[1]}` : "founder"}${a.verification ? ` · ${a.verification.verdict}` : ""}`);
      }
      return;
    }
    default:
      say("usage: breed.mjs genome|distance|plan|check|register|verify|court|pedigree … (see SKILL.md)");
      process.exit(1);
  }
}

function countMarkers(dir) {
  let n = 0;
  for (const f of HERITABLE) {
    const p = path.join(dir, f);
    if (!fs.existsSync(p)) continue;
    n += (fs.readFileSync(p, "utf8").match(/<!-- ZUCHTWAHL:(BLEND|MUTATE)/g) ?? []).length;
  }
  return n;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    main();
  } catch (err) {
    process.stderr.write(`breed: ${err?.message ?? err}\n`);
    process.exit(1);
  }
}
