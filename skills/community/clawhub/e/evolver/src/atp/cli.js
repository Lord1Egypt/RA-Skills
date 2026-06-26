// ATP CLI: lightweight argument parsers and runners for the `buy`, `orders`,
// and `verify` subcommands. Separated from index.js so they can be unit-tested
// without booting the full evolver loop.
//
// Public API:
//   parseBuyArgs(args)   -> { ok, opts?, error? }
//   parseOrdersArgs(args)-> { ok, opts?, error? }
//   parseVerifyArgs(args)-> { ok, opts?, error? }
//   runBuy(opts, deps)
//   runOrders(opts, deps)
//   runVerify(opts, deps)
//
// `deps` is an object containing the ATP module (defaults to require('./index')),
// injectable for tests. Each runner returns a Promise that resolves to
// { exitCode: number, output?: string, data?: object }.

const {
  ATP_VERIFY_MODES,
  ATP_VERIFY_ACTIONS,
  ATP_ROUTING_MODES,
  ATP_PROOF_STATUSES,
  ATP_ROLES,
} = require('./protocol');

function _parseNamed(args, longFlag, shortFlag) {
  const long = args.findIndex(a => typeof a === 'string' && (a === longFlag || a.startsWith(longFlag + '=')));
  if (long !== -1) {
    const token = args[long];
    if (token.startsWith(longFlag + '=')) return token.slice(longFlag.length + 1);
    if (args[long + 1] && !String(args[long + 1]).startsWith('--')) return args[long + 1];
  }
  if (shortFlag) {
    const short = args.indexOf(shortFlag);
    if (short !== -1 && args[short + 1] && !String(args[short + 1]).startsWith('--')) return args[short + 1];
  }
  return null;
}

function _toBool(v) {
  if (typeof v !== 'string') return false;
  const s = v.toLowerCase();
  return s === '1' || s === 'true' || s === 'yes' || s === 'on';
}

function parseBuyArgs(args) {
  if (!Array.isArray(args) || args.length === 0) {
    return { ok: false, error: 'buy requires <capabilities>: comma-separated list (e.g. code_review,bug_fix)' };
  }

  // First positional (not starting with --) is the capability list.
  let capabilitiesRaw = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (typeof a === 'string' && !a.startsWith('--')) {
      capabilitiesRaw = a;
      break;
    }
  }
  if (!capabilitiesRaw) {
    return { ok: false, error: 'buy requires <capabilities>: comma-separated list' };
  }

  const capabilities = capabilitiesRaw.split(',').map(s => s.trim()).filter(Boolean);
  if (capabilities.length === 0) {
    return { ok: false, error: 'no valid capabilities parsed from: ' + capabilitiesRaw };
  }

  const budgetRaw = _parseNamed(args, '--budget', '-b');
  const budget = Math.max(1, Math.round(Number(budgetRaw) || 10));

  const question = _parseNamed(args, '--question', '-q') || '';
  const routingMode = _parseNamed(args, '--routing', null) || 'fastest';
  const verifyMode = _parseNamed(args, '--verify', null) || 'auto';
  const noWait = args.includes('--no-wait');
  const timeoutMsRaw = _parseNamed(args, '--timeout', null);
  const timeoutMs = timeoutMsRaw ? Math.max(1000, Math.round(Number(timeoutMsRaw) * 1000)) : 300000;

  return {
    ok: true,
    opts: {
      capabilities,
      budget,
      question,
      routingMode,
      verifyMode,
      noWait,
      timeoutMs,
    },
  };
}

function parseOrdersArgs(args) {
  const role = _parseNamed(args, '--role', null);
  if (role && !ATP_ROLES.includes(role)) {
    return { ok: false, error: 'invalid --role: ' + role + ' (expected ' + ATP_ROLES.join('|') + ')' };
  }
  const status = _parseNamed(args, '--status', null);
  if (status && !ATP_PROOF_STATUSES.includes(status)) {
    return { ok: false, error: 'invalid --status: ' + status };
  }
  const limitRaw = _parseNamed(args, '--limit', null);
  const limit = limitRaw ? Math.max(1, Math.min(100, Math.round(Number(limitRaw)))) : 20;
  const jsonOut = args.includes('--json');
  return {
    ok: true,
    opts: { role: role || 'consumer', status: status || null, limit, jsonOut },
  };
}

function parseVerifyArgs(args) {
  let orderId = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (typeof a === 'string' && !a.startsWith('--')) {
      orderId = a;
      break;
    }
  }
  if (!orderId) {
    return { ok: false, error: 'verify requires <orderId>' };
  }
  const action = _parseNamed(args, '--action', null) || 'confirm';
  if (!ATP_VERIFY_ACTIONS.includes(action)) {
    return { ok: false, error: 'invalid --action: ' + action + ' (expected ' + ATP_VERIFY_ACTIONS.join('|') + ')' };
  }
  return { ok: true, opts: { orderId, action } };
}

// `evolver atp <enable|disable|status>` — manage autoBuyer consent ack file.
// Non-TTY users (daemon, CI, hooks) opt in here instead of the interactive
// first-run prompt. Returns { ok, opts: { sub } } or { ok: false, error }.
function parseAtpArgs(args) {
  if (!Array.isArray(args) || args.length === 0) {
    return { ok: false, error: 'atp requires <enable|disable|status>' };
  }
  let sub = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (typeof a === 'string' && !a.startsWith('--')) {
      sub = a.toLowerCase();
      break;
    }
  }
  if (!sub || !['enable', 'disable', 'status'].includes(sub)) {
    return { ok: false, error: 'atp subcommand must be enable|disable|status (got: ' + sub + ')' };
  }
  return { ok: true, opts: { sub } };
}

async function runBuy(opts, deps) {
  const atp = (deps && deps.atp) || require('./index');
  const consumerAgent = atp.consumerAgent;
  const log = (deps && deps.log) || console.log;
  const err = (deps && deps.err) || console.error;

  log('[ATP] Placing order: capabilities=' + opts.capabilities.join(',') + ' budget=' + opts.budget + ' mode=' + opts.routingMode);

  try {
    if (opts.noWait) {
      const result = await consumerAgent.orderService({
        capabilities: opts.capabilities,
        budget: opts.budget,
        routingMode: opts.routingMode,
        verifyMode: opts.verifyMode,
        question: opts.question,
      });
      if (!result.ok) {
        err('[ATP] Order failed: ' + (result.error || 'unknown'));
        return { exitCode: 1, data: result };
      }
      log('[ATP] Order placed: ' + result.data.order_id);
      return { exitCode: 0, data: result.data };
    }

    const result = await consumerAgent.orderAndWait({
      capabilities: opts.capabilities,
      budget: opts.budget,
      routingMode: opts.routingMode,
      verifyMode: opts.verifyMode,
      question: opts.question,
      timeoutMs: opts.timeoutMs,
    });

    if (!result.ok) {
      err('[ATP] Order lifecycle failed: ' + (result.error || 'unknown'));
      return { exitCode: 1, data: result };
    }
    log('[ATP] Order settled: ' + (result.order && result.order.order_id));
    if (result.finalStatus) {
      log('[ATP] Final status: ' + JSON.stringify(result.finalStatus, null, 2));
    }
    return { exitCode: 0, data: result };
  } catch (e) {
    err('[ATP] buy error: ' + (e && e.message || e));
    return { exitCode: 1, error: String(e) };
  }
}

async function runOrders(opts, deps) {
  const atp = (deps && deps.atp) || require('./index');
  const hubClient = atp.hubClient;
  const log = (deps && deps.log) || console.log;
  const err = (deps && deps.err) || console.error;

  try {
    const result = await hubClient.listProofs({
      role: opts.role,
      status: opts.status || undefined,
      limit: opts.limit,
    });
    if (!result.ok) {
      err('[ATP] listProofs failed: ' + (result.error || 'unknown'));
      return { exitCode: 1, data: result };
    }

    const proofs = (result.data && result.data.proofs) || result.data || [];
    if (opts.jsonOut) {
      log(JSON.stringify(proofs, null, 2));
      return { exitCode: 0, data: proofs };
    }
    if (!Array.isArray(proofs) || proofs.length === 0) {
      log('[ATP] No orders found for role=' + opts.role + (opts.status ? ' status=' + opts.status : ''));
      return { exitCode: 0, data: [] };
    }
    log('[ATP] Showing ' + proofs.length + ' order(s):');
    for (const p of proofs) {
      const when = p.createdAt || p.created_at || 'unknown';
      log('  - ' + (p.taskId || p.order_id || p.id) + ' | status=' + p.status + ' | created=' + when);
    }
    return { exitCode: 0, data: proofs };
  } catch (e) {
    err('[ATP] orders error: ' + (e && e.message || e));
    return { exitCode: 1, error: String(e) };
  }
}

async function runVerify(opts, deps) {
  const atp = (deps && deps.atp) || require('./index');
  const consumerAgent = atp.consumerAgent;
  const log = (deps && deps.log) || console.log;
  const err = (deps && deps.err) || console.error;

  try {
    const fn = opts.action === 'ai_judge' ? consumerAgent.requestAiJudge : consumerAgent.confirmDelivery;
    const result = await fn(opts.orderId);
    if (!result.ok) {
      err('[ATP] verify failed: ' + (result.error || 'unknown'));
      return { exitCode: 1, data: result };
    }
    log('[ATP] verify ok (' + opts.action + '): ' + JSON.stringify(result.data));
    return { exitCode: 0, data: result.data };
  } catch (e) {
    err('[ATP] verify error: ' + (e && e.message || e));
    return { exitCode: 1, error: String(e) };
  }
}

// Subcommand runner for `evolver atp enable|disable|status`. Writes the ack
// file via autoBuyer.setConsent so subsequent daemon starts pick it up. Does
// NOT mutate process.env — env override wins over the ack file by design,
// and we don't want a transient CLI invocation to silently shadow operator
// shell config.
// Detect whether an EVOLVER_ATP_AUTOBUY env override is currently set AND
// would supersede the ack we are about to write. Returns the effective env
// boolean (true=on, false=off) or null if env is unset / whitespace-only.
// Mirrors the trim-before-length-check rule from autoBuyer.getConsent so
// the CLI and the runtime agree on what "set" means (Bugbot PR #141).
function _envOverride() {
  const raw = process.env.EVOLVER_ATP_AUTOBUY;
  if (typeof raw !== 'string') return null;
  const s = raw.trim().toLowerCase();
  if (s.length === 0) return null;
  return !(s === 'off' || s === '0' || s === 'false');
}

async function runAtp(opts, deps) {
  const autoBuyer = (deps && deps.autoBuyer) || require('./autoBuyer');
  const log = (deps && deps.log) || console.log;
  const err = (deps && deps.err) || console.error;

  try {
    if (opts.sub === 'enable') {
      const body = autoBuyer.setConsent(true);
      log('[ATP] auto-spend ENABLED (consent recorded ' + body.acknowledged_at + ').');
      log('      Caps: daily=' + (process.env.ATP_AUTOBUY_DAILY_CAP_CREDITS || '50') +
          ', per-order=' + (process.env.ATP_AUTOBUY_PER_ORDER_CAP_CREDITS || '10') + ' credits.');
      log('      Disable: evolver atp disable  (or  EVOLVER_ATP_AUTOBUY=off)');
      // Loud warning if an env override will silently undo the ack at
      // runtime. Bugbot PR #141 Medium: without this the user gets a
      // false confirmation and real credits keep flowing the wrong way.
      const envEnabled = _envOverride();
      if (envEnabled === false) {
        log('');
        log('[ATP] WARNING: EVOLVER_ATP_AUTOBUY=' + process.env.EVOLVER_ATP_AUTOBUY +
            ' is set in your environment and will OVERRIDE the ack file at runtime.');
        log('      Auto-spend will stay OFF until you unset it (env wins over the ack file).');
        return { exitCode: 0, data: body, envOverride: 'off' };
      }
      return { exitCode: 0, data: body };
    }
    if (opts.sub === 'disable') {
      const body = autoBuyer.setConsent(false);
      log('[ATP] auto-spend DISABLED (consent recorded ' + body.acknowledged_at + ').');
      log('      Re-enable: evolver atp enable');
      const envEnabled = _envOverride();
      if (envEnabled === true) {
        log('');
        log('[ATP] WARNING: EVOLVER_ATP_AUTOBUY=' + process.env.EVOLVER_ATP_AUTOBUY +
            ' is set in your environment and will OVERRIDE the ack file at runtime.');
        log('      Auto-spend will stay ON (and continue charging credits) until you unset it.');
        return { exitCode: 0, data: body, envOverride: 'on' };
      }
      return { exitCode: 0, data: body };
    }
    // status
    const consent = autoBuyer.getConsent();
    const ackPath = autoBuyer.getAckPath();
    log('[ATP] auto-spend: ' + (consent.enabled ? 'ENABLED' : 'DISABLED') +
        '  (source: ' + consent.source + ')');
    log('      ack file: ' + ackPath);
    if (consent.source === 'default') {
      log('      Default policy (no ack file, no env override). Run `evolver atp disable`');
      log('      to opt out, or `evolver atp enable` to record explicit opt-in.');
    }
    return { exitCode: 0, data: consent };
  } catch (e) {
    err('[ATP] atp command error: ' + (e && e.message || e));
    return { exitCode: 1, error: String(e) };
  }
}

function printUsage() {
  return [
    'ATP subcommands:',
    '  evolver buy <caps> [--budget=N] [--question "..."] [--routing=' + ATP_ROUTING_MODES.join('|') + ']',
    '              [--verify=' + ATP_VERIFY_MODES.join('|') + '] [--no-wait] [--timeout=<seconds>]',
    '  evolver orders [--role=' + ATP_ROLES.join('|') + '] [--status=' + ATP_PROOF_STATUSES.join('|') + ']',
    '                 [--limit=N] [--json]',
    '  evolver verify <orderId> [--action=' + ATP_VERIFY_ACTIONS.join('|') + ']',
    '  evolver atp <enable|disable|status>   -- manage auto-spend consent',
  ].join('\n');
}

module.exports = {
  parseBuyArgs,
  parseOrdersArgs,
  parseVerifyArgs,
  parseAtpArgs,
  runBuy,
  runOrders,
  runVerify,
  runAtp,
  printUsage,
};
