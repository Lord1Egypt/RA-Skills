#!/usr/bin/env node
// Launches ONE headless executor, reviewer or scout on a CLI harness (Claude Code, Codex, OpenCode)
// with a brief on stdin, and records what happened in a run directory the orchestrator reads.
//
// Usage:
//   node scripts/spawn.mjs --harness claude|codex|opencode --brief <file|-> --dir <workdir> --out <run-dir>
//        [--model M] [--effort E] [--mode write|read-only] [--resume <session-id>] [--timeout <sec>]
//        [--permission <claude permission mode>] [--ledger <file> --feature <id> --round <n> --role <r>]
//        [--bin <path>] [--no-lean] [--dry-run] [-- <extra CLI args>]
//
// Writes into <run-dir> (created; must be empty or absent):
//   command.txt   the exact argv (the brief is not repeated: it is stdin)
//   events.jsonl  the CLI's raw stdout (JSON / JSONL events)
//   stderr.log    the CLI's raw stderr
//   final.md      the agent's final message (its report)
//   result.json   { harness, model, effort, mode, sessionId, exitCode, status, seconds, tokensIn,
//                   tokensOut, costUsd, final, out }
// Exit code: the CLI's own exit code (1 if it exited 0 but its events report an error); 3 if it
// exited 0 without a final report; 124 on timeout; 127 if the CLI is not on PATH; 2 on usage errors
// (nothing is written). Judge the run by this code and result.json, never by the final text.
//
// Modes: write = may edit files and run commands inside --dir; read-only = review/scout, no edits.
//   claude:   write -> --permission-mode <--permission, default auto>; read-only -> plan. Lean by
//             default (no MCP servers, no skills, per-machine prompt sections moved out of the
//             system prompt for cache reuse); --no-lean keeps the user's full setup.
//   codex:    write -> --sandbox workspace-write; read-only -> --sandbox read-only
//   opencode: write -> --agent build --auto; read-only -> --agent plan (no --auto). OpenCode has no
//             OS sandbox: only point it at a disposable worktree. The major version is detected:
//             v2 runs `run --standalone` in --dir (cwd) with the effort as `-m provider/model#effort`;
//             v1 uses `--dir` and `--variant`. Lean by default: OPENCODE_DISABLE_CLAUDE_CODE=1 (no
//             ~/.claude prompt or skills); --no-lean keeps them.
// --bin picks the CLI binary (default: the harness name on PATH), e.g. when several are installed.
// Resume: --resume <id> continues that exact session (never "the last one"): use it for reviewer
// re-reviews and for answering an executor's blocked question; fix rounds use a FRESH session.
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, existsSync, readdirSync, readFileSync, writeFileSync, appendFileSync, openSync, closeSync } from 'node:fs';
import { resolve, join } from 'node:path';

const usage = (msg) => {
  if (msg) console.error(`spawn.mjs: ${msg}`);
  console.error('usage: node scripts/spawn.mjs --harness claude|codex|opencode --brief <file|-> --dir <workdir> --out <run-dir> [--model M] [--effort E] [--mode write|read-only] [--resume <id>] [--timeout <sec>] [--permission <mode>] [--ledger <file> --feature <id> --round <n> --role <r>] [--bin <path>] [--no-lean] [--dry-run] [-- extra args]');
  process.exit(2);
};

const opts = { mode: 'write', timeout: '3600', permission: 'auto' };
const extra = [];
const argv = process.argv.slice(2);
const VALUED = new Set(['harness', 'brief', 'dir', 'out', 'model', 'effort', 'mode', 'resume', 'timeout', 'permission', 'ledger', 'feature', 'round', 'role', 'bin']);
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--') { extra.push(...argv.slice(i + 1)); break; }
  if (a === '--dry-run') { opts.dryRun = true; continue; }
  if (a === '--no-lean') { opts.noLean = true; continue; }
  const key = a.startsWith('--') ? a.slice(2) : null;
  if (!key || !VALUED.has(key)) usage(`unknown argument '${a}'`);
  if (i + 1 >= argv.length) usage(`--${key} needs a value`);
  opts[key] = argv[++i];
}

const HARNESSES = ['claude', 'codex', 'opencode'];
if (!HARNESSES.includes(opts.harness)) usage(`--harness must be one of ${HARNESSES.join(', ')}`);
for (const k of ['brief', 'dir', 'out']) if (!opts[k]) usage(`--${k} is required`);
if (!['write', 'read-only'].includes(opts.mode)) usage("--mode must be 'write' or 'read-only'");
if (!/^[1-9][0-9]*$/.test(opts.timeout)) usage('--timeout must be a positive integer (seconds)');
if (opts.ledger && !(opts.feature && opts.round && opts.role)) usage('--ledger needs --feature, --round and --role');
if (opts.harness === 'opencode' && !opts.model && !opts.resume) usage('opencode needs --model provider/model on a fresh run');
const dir = resolve(opts.dir);
if (!existsSync(dir)) usage(`--dir does not exist: ${dir}`);
const out = resolve(opts.out);
if (existsSync(out) && readdirSync(out).length > 0) usage(`--out must be empty or absent (refusing to mix runs): ${out}`);

let brief;
try {
  brief = opts.brief === '-' ? readFileSync(0, 'utf8') : readFileSync(resolve(opts.brief), 'utf8');
} catch (e) {
  usage(`cannot read brief: ${e.message}`);
}
if (!brief.trim()) usage('the brief is empty');
if (/\{\{[A-Z0-9_]+\}\}/.test(brief)) usage('the brief still contains {{PLACEHOLDERS}}; fill them (scripts/brief.mjs refuses these too)');

const write = opts.mode === 'write';
const finalPath = join(out, 'final.md');
const cmd = opts.bin ?? opts.harness;
const present = spawnSync('sh', ['-c', 'command -v "$1"', 'sh', cmd]).status === 0;
// PWD must match cwd: OpenCode v2 takes its project directory from $PWD, so an inherited PWD would
// point the agent at the orchestrator's checkout instead of --dir (observed).
// The caller's environment is passed through unchanged so the agent CLI finds its PATH and login;
// this script reads no variables from it and makes no network calls of its own.
const env = { ...process.env, PWD: dir };
let args;
if (opts.harness === 'claude') {
  args = ['-p', '--output-format', 'json', '--permission-mode', write ? opts.permission : 'plan'];
  if (opts.model) args.push('--model', opts.model);
  if (opts.effort) args.push('--effort', opts.effort);
  if (opts.resume) args.push('--resume', opts.resume);
  // Lean by default: a headless run otherwise loads every user MCP server and skill (measured: 61K
  // input tokens for a one-line reply). Executors get their context from the brief, not from tools.
  if (!opts.noLean) args.push('--strict-mcp-config', '--disable-slash-commands', '--exclude-dynamic-system-prompt-sections');
} else if (opts.harness === 'codex') {
  const sandbox = write ? 'workspace-write' : 'read-only';
  // `codex exec resume` takes neither --cd nor --sandbox: it runs in cwd and takes the sandbox as config.
  args = opts.resume
    ? ['exec', 'resume', opts.resume, '--json', '-o', finalPath, '-c', `sandbox_mode="${sandbox}"`]
    : ['exec', '--json', '-C', dir, '--sandbox', sandbox, '-o', finalPath];
  if (opts.model) args.push('-m', opts.model);
  if (opts.effort) args.push('-c', `model_reasoning_effort="${opts.effort}"`);
} else {
  // v1 and v2 differ: v2 dropped --dir and --variant (effort goes in the model id) and runs through
  // a shared background service unless --standalone (a private server per run, rooted at its cwd).
  let major = 2;
  if (present) {
    const v = spawnSync(cmd, ['--version'], { encoding: 'utf8', timeout: 20_000 });
    const m = `${v.stdout ?? ''}${v.stderr ?? ''}`.match(/(\d+)\.\d+\.\d+/);
    if (!m) usage(`cannot read the version from '${cmd} --version'`);
    major = Number(m[1]);
  }
  if (major >= 2) {
    args = ['run', '--standalone', '--format', 'json', '--agent', write ? 'build' : 'plan'];
    if (write) args.push('--auto');
    if (opts.model) args.push('-m', opts.effort ? `${opts.model}#${opts.effort}` : opts.model);
    else if (opts.effort) usage('opencode v2 takes the effort inside the model id (provider/model#effort): pass --model too');
  } else {
    args = ['run', '--format', 'json', '--dir', dir, '--agent', write ? 'build' : 'plan'];
    if (write) args.push('--auto');
    if (opts.model) args.push('-m', opts.model);
    if (opts.effort) args.push('--variant', opts.effort);
  }
  if (opts.resume) args.push('--session', opts.resume);
  if (!opts.noLean) env.OPENCODE_DISABLE_CLAUDE_CODE = '1';
}
args.push(...extra);
if (opts.harness === 'codex') args.push('-'); // prompt from stdin, after any extra options

if (opts.dryRun) {
  console.log([cmd, ...args].map((a) => (/^[\w@%+=:,./-]+$/.test(a) ? a : `'${a.replace(/'/g, `'\\''`)}'`)).join(' '));
  process.exit(0);
}

if (!present) {
  mkdirSync(out, { recursive: true });
  const r = { harness: opts.harness, status: 'cli_missing', exitCode: 127, out };
  writeFileSync(join(out, 'result.json'), JSON.stringify(r, null, 2) + '\n');
  console.error(`spawn.mjs: '${cmd}' is not on PATH`);
  process.exit(127);
}

mkdirSync(out, { recursive: true });
writeFileSync(join(out, 'command.txt'), JSON.stringify({ cwd: dir, argv: [cmd, ...args] }, null, 2) + '\n');
const outFd = openSync(join(out, 'events.jsonl'), 'w');
const errFd = openSync(join(out, 'stderr.log'), 'w');
const started = Date.now();
const child = spawn(cmd, args, { cwd: dir, env, stdio: ['pipe', outFd, errFd], detached: true });
child.stdin.on('error', () => {}); // a CLI that exits early closes stdin; the exit code tells the story
child.stdin.end(brief);

let timedOut = false;
const killGroup = (sig) => {
  try {
    process.kill(-child.pid, sig);
  } catch {
    /* already gone */
  }
};
const timer = setTimeout(() => {
  timedOut = true;
  killGroup('SIGTERM');
  setTimeout(() => killGroup('SIGKILL'), 10_000).unref();
}, Number(opts.timeout) * 1000);
for (const sig of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(sig, () => killGroup(sig));

child.on('error', (e) => {
  console.error(`spawn.mjs: cannot start ${cmd}: ${e.message}`);
});

child.on('close', (code, signal) => {
  clearTimeout(timer);
  closeSync(outFd);
  closeSync(errFd);
  const seconds = Math.round((Date.now() - started) / 1000);
  let exitCode = code ?? (signal ? 128 + (({ SIGINT: 2, SIGKILL: 9, SIGTERM: 15, SIGHUP: 1 })[signal] ?? 0) : 1);
  if (timedOut) exitCode = 124;

  const raw = readFileSync(join(out, 'events.jsonl'), 'utf8');
  const events = [];
  for (const line of raw.split('\n')) {
    if (!line.trim()) continue;
    try {
      events.push(JSON.parse(line));
    } catch {
      /* non-JSON noise */
    }
  }
  if (events.length === 0 && raw.trim()) {
    try {
      events.push(JSON.parse(raw)); // claude --output-format json may pretty-print one object
    } catch {
      /* keep raw only */
    }
  }

  let sessionId = null;
  let final = '';
  let tokensIn = null;
  let tokensOut = null;
  let costUsd = null;
  let reportedError = false;
  const add = (cur, v) => (typeof v === 'number' ? (cur ?? 0) + v : cur);

  if (opts.harness === 'claude') {
    const r = events.find((e) => e && e.type === 'result') ?? events[events.length - 1] ?? {};
    sessionId = r.session_id ?? null;
    final = typeof r.result === 'string' ? r.result : '';
    reportedError = r.is_error === true;
    costUsd = typeof r.total_cost_usd === 'number' ? r.total_cost_usd : null;
    if (r.usage) {
      tokensIn = add(add(add(null, r.usage.input_tokens), r.usage.cache_read_input_tokens), r.usage.cache_creation_input_tokens);
      tokensOut = add(null, r.usage.output_tokens);
    }
  } else if (opts.harness === 'codex') {
    for (const e of events) {
      if (!sessionId && (e.thread_id || e.session_id)) sessionId = e.thread_id || e.session_id;
      if (e.type === 'turn.completed' && e.usage) {
        tokensIn = add(tokensIn, e.usage.input_tokens);
        tokensOut = add(tokensOut, e.usage.output_tokens);
      }
      if (e.type === 'turn.failed' || e.type === 'error') reportedError = true;
    }
    if (!sessionId && opts.resume) sessionId = opts.resume;
    final = existsSync(finalPath) ? readFileSync(finalPath, 'utf8') : '';
  } else {
    const texts = [];
    for (const e of events) {
      if (!sessionId) sessionId = e.sessionID ?? e.sessionId ?? e.part?.sessionID ?? null;
      if (e.type === 'text' && typeof e.part?.text === 'string') texts.push(e.part.text);
      const t = e.part?.tokens;
      if (e.type === 'step_finish' && t) {
        tokensIn = add(add(tokensIn, t.input), t.cache?.read);
        tokensOut = add(tokensOut, t.output);
      }
      if (e.type === 'step_finish' && typeof e.part?.cost === 'number') costUsd = add(costUsd, e.part.cost);
      if (e.type === 'error') reportedError = true;
    }
    if (!sessionId && opts.resume) sessionId = opts.resume;
    final = texts.join('\n');
  }
  if (opts.harness !== 'codex') writeFileSync(finalPath, final);
  if (exitCode === 0 && reportedError) exitCode = 1; // the CLI said success but the run reported an error

  const status = timedOut ? 'timeout' : exitCode === 0 ? (final.trim() ? 'ok' : 'no_report') : 'failed';
  if (status === 'no_report' && exitCode === 0) exitCode = 3;
  const result = {
    harness: opts.harness,
    model: opts.model ?? null,
    effort: opts.effort ?? null,
    mode: opts.mode,
    resumed: opts.resume ?? null,
    sessionId,
    exitCode,
    status,
    seconds,
    tokensIn,
    tokensOut,
    costUsd,
    final: finalPath,
    out,
  };
  writeFileSync(join(out, 'result.json'), JSON.stringify(result, null, 2) + '\n');

  if (opts.ledger) {
    const ledger = resolve(opts.ledger);
    const cols = ['utc', 'feature', 'round', 'role', 'harness', 'model', 'effort', 'mode', 'seconds', 'exit', 'status', 'session', 'tokens_in', 'tokens_out', 'cost_usd', 'findings', 'run_dir'];
    if (!existsSync(ledger)) appendFileSync(ledger, cols.join('\t') + '\n');
    const clean = (v) => String(v ?? '').replace(/[\t\n]/g, ' ');
    const row = [new Date().toISOString(), opts.feature, opts.round, opts.role, opts.harness, opts.model, opts.effort, opts.mode, seconds, exitCode, status, sessionId, tokensIn, tokensOut, costUsd, '', out];
    appendFileSync(ledger, row.map(clean).join('\t') + '\n');
  }

  console.log(`spawn.mjs: ${opts.harness} ${status} exit=${exitCode} ${seconds}s session=${sessionId ?? '-'} report=${finalPath}`);
  process.exit(exitCode);
});
