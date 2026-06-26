#!/usr/bin/env node

function parseArgv(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      flags[key] = next;
      i += 1;
    } else {
      flags[key] = true;
    }
  }
  return flags;
}

function toPositiveInt(value, fallback) {
  const numeric = Number(value);
  if (!Number.isInteger(numeric) || numeric <= 0) {
    return fallback;
  }
  return numeric;
}

function toNonNegativeInt(value, fallback) {
  const numeric = Number(value);
  if (!Number.isInteger(numeric) || numeric < 0) {
    return fallback;
  }
  return numeric;
}

function toOptionalPositiveInt(value) {
  if (value === undefined || value === null || value === '') {
    return null;
  }
  const numeric = Number(value);
  if (!Number.isInteger(numeric) || numeric <= 0) {
    throw new Error(`invalid positive integer: ${value}`);
  }
  return numeric;
}

function toBoolean(value, fallback = false) {
  if (value === undefined || value === null || value === '') {
    return fallback;
  }
  if (typeof value === 'boolean') {
    return value;
  }
  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'y', 'on'].includes(normalized)) {
    return true;
  }
  if (['false', '0', 'no', 'n', 'off'].includes(normalized)) {
    return false;
  }
  return fallback;
}

function normalizeRole(value) {
  const role = String(value ?? 'buyer').trim().toLowerCase();
  if (!['buyer', 'seller'].includes(role)) {
    throw new Error('role must be buyer or seller');
  }
  return role;
}

function toAmountText(amountMinorUnits, currency) {
  return `${(amountMinorUnits / 100).toFixed(2)} ${currency}`;
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function readStdinJson() {
  if (process.stdin.isTTY) {
    return {};
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) {
    return {};
  }
  return JSON.parse(raw);
}

function pickValue(...values) {
  for (const value of values) {
    if (value !== undefined && value !== null && value !== '') {
      return value;
    }
  }
  return undefined;
}

function tryParseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function extractJsonObject(text) {
  const source = String(text ?? '').trim();
  if (!source) {
    throw new Error('empty text');
  }

  const direct = tryParseJson(source);
  if (direct && typeof direct === 'object') {
    return direct;
  }

  const fenced = source.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenced) {
    const parsed = tryParseJson(fenced[1].trim());
    if (parsed && typeof parsed === 'object') {
      return parsed;
    }
  }

  const firstBrace = source.indexOf('{');
  const lastBrace = source.lastIndexOf('}');
  if (firstBrace >= 0 && lastBrace > firstBrace) {
    const fragment = source.slice(firstBrace, lastBrace + 1);
    const parsed = tryParseJson(fragment);
    if (parsed && typeof parsed === 'object') {
      return parsed;
    }
  }

  throw new Error('cannot parse JSON object');
}

function walkStrings(value, out) {
  if (typeof value === 'string') {
    out.push(value);
    return;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      walkStrings(item, out);
    }
    return;
  }
  if (value && typeof value === 'object') {
    for (const item of Object.values(value)) {
      walkStrings(item, out);
    }
  }
}

function extractTextCandidatesFromOpenClawOutput(rawStdout) {
  const source = String(rawStdout ?? '').trim();
  if (!source) {
    return [];
  }

  const lines = source.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const candidates = [];

  const parsedWhole = tryParseJson(source);
  if (parsedWhole) {
    const prioritized = [
      parsedWhole.answer,
      parsedWhole.output,
      parsedWhole.outputText,
      parsedWhole.result,
      parsedWhole.message,
      parsedWhole.content,
      parsedWhole.response
    ].filter((item) => typeof item === 'string' && item.trim().length > 0);
    candidates.push(...prioritized);

    const allStrings = [];
    walkStrings(parsedWhole, allStrings);
    candidates.push(...allStrings);
  }

  for (const line of lines) {
    const parsed = tryParseJson(line);
    if (!parsed) {
      candidates.push(line);
      continue;
    }

    const prioritized = [
      parsed.answer,
      parsed.output,
      parsed.outputText,
      parsed.result,
      parsed.message,
      parsed.content,
      parsed.response
    ].filter((item) => typeof item === 'string' && item.trim().length > 0);
    candidates.push(...prioritized);

    const allStrings = [];
    walkStrings(parsed, allStrings);
    candidates.push(...allStrings);
  }

  return candidates.filter((item, index, arr) => arr.indexOf(item) === index);
}

function normalizeDecision(decision) {
  if (!decision || typeof decision !== 'object' || Array.isArray(decision)) {
    throw new Error('contract mismatch: turn-decision-v1 requires a JSON object');
  }

  if ('result' in decision || 'status' in decision || 'traceUrl' in decision || 'dialogue' in decision || 'history' in decision) {
    throw new Error('contract mismatch: got session-level result fields; expected turn decision JSON');
  }

  const requiredFields = ['action', 'offerMinorUnits', 'utterance', 'reason'];
  for (const field of requiredFields) {
    if (!(field in decision)) {
      throw new Error(`contract mismatch: missing required field "${field}" in turn-decision-v1`);
    }
  }

  const action = String(decision?.action ?? '').trim().toLowerCase();
  if (!['offer', 'counter', 'accept', 'reject'].includes(action)) {
    throw new Error(`invalid action: ${decision?.action}`);
  }

  const rawOffer = decision?.offerMinorUnits;
  let offerMinorUnits = null;
  if (!(rawOffer === null || rawOffer === undefined || rawOffer === '')) {
    const numeric = Number(rawOffer);
    if (!Number.isInteger(numeric) || numeric <= 0) {
      throw new Error(`invalid offerMinorUnits: ${rawOffer}`);
    }
    offerMinorUnits = numeric;
  }

  const utterance = String(decision?.utterance ?? '').trim();
  if (!utterance) {
    throw new Error('contract mismatch: utterance is required and must be non-empty');
  }

  const reason = String(decision?.reason ?? '').trim();
  if (!reason) {
    throw new Error('contract mismatch: reason is required and must be non-empty');
  }

  return {
    action,
    offerMinorUnits,
    utterance,
    reason
  };
}

function extractDecisionFromAnyText(rawText) {
  const parsed = extractJsonObject(rawText);
  return normalizeDecision(parsed);
}

function hasAnyProviderKey(env) {
  const candidates = [
    'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY',
    'GOOGLE_API_KEY',
    'GEMINI_API_KEY',
    'GROQ_API_KEY',
    'DEEPSEEK_API_KEY',
    'MISTRAL_API_KEY',
    'TOGETHER_API_KEY',
    'OPENROUTER_API_KEY'
  ];
  return candidates.some((name) => String(env[name] ?? '').trim().length > 0);
}

function resolveTurnContext(input) {
  const session = (input.session && typeof input.session === 'object') ? input.session : {};
  const message = (input.message && typeof input.message === 'object') ? input.message : {};
  const payload = (message.payload && typeof message.payload === 'object') ? message.payload : {};
  const policy = (session.policy && typeof session.policy === 'object')
    ? session.policy
    : ((payload.policy && typeof payload.policy === 'object') ? payload.policy : {});

  const role = normalizeRole(pickValue(input.role, session.role, payload.role));
  const phase = String(pickValue(payload.phase, input.phase, 'counter')).trim();
  const round = toNonNegativeInt(pickValue(payload.round, input.round), 0);
  const currency = String(pickValue(session.currency, payload.currency, input.currency, 'USD')).trim() || 'USD';
  const listAmountMinorUnits = toPositiveInt(
    pickValue(session.listAmountMinorUnits, payload.listAmountMinorUnits, input.listAmountMinorUnits),
    9000
  );

  const buyerLabel = String(pickValue(session.buyerLabel, payload.buyerLabel, input.buyerLabel, session.buyerAgentId, 'buyer')).trim();
  const sellerLabel = String(pickValue(session.sellerLabel, payload.sellerLabel, input.sellerLabel, session.sellerAgentId, 'seller')).trim();
  const speaker = role === 'seller' ? sellerLabel : buyerLabel;

  const sellerOfferMinorUnits = toOptionalPositiveInt(pickValue(payload.sellerOfferMinorUnits, input.sellerOfferMinorUnits));
  const buyerOfferMinorUnits = toOptionalPositiveInt(pickValue(payload.buyerOfferMinorUnits, input.buyerOfferMinorUnits));
  const lastSellerOfferMinorUnits = toOptionalPositiveInt(pickValue(payload.lastSellerOfferMinorUnits, input.lastSellerOfferMinorUnits));

  const buyerTargetDiscountBps = toNonNegativeInt(
    pickValue(input.buyerTargetDiscountBps, policy.buyerTargetDiscountBps),
    700
  );
  const buyerConcessionBpsPerRound = toNonNegativeInt(
    pickValue(input.buyerConcessionBpsPerRound, policy.buyerConcessionBpsPerRound),
    200
  );
  const sellerMinDiscountBps = toNonNegativeInt(
    pickValue(input.sellerMinDiscountBps, policy.sellerMinDiscountBps),
    300
  );
  const floorMinorUnits = toOptionalPositiveInt(pickValue(input.floorMinorUnits, policy.floorMinorUnits));
  const ceilingMinorUnits = toOptionalPositiveInt(pickValue(input.ceilingMinorUnits, policy.ceilingMinorUnits));

  return {
    role,
    phase,
    round,
    currency,
    listAmountMinorUnits,
    buyerLabel,
    sellerLabel,
    speaker,
    sellerOfferMinorUnits,
    buyerOfferMinorUnits,
    lastSellerOfferMinorUnits,
    buyerTargetDiscountBps,
    buyerConcessionBpsPerRound,
    sellerMinDiscountBps,
    floorMinorUnits,
    ceilingMinorUnits
  };
}

function decideTurn(ctx) {
  const {
    role,
    phase,
    round,
    currency,
    listAmountMinorUnits,
    speaker,
    sellerOfferMinorUnits,
    buyerOfferMinorUnits,
    lastSellerOfferMinorUnits,
    buyerTargetDiscountBps,
    buyerConcessionBpsPerRound,
    sellerMinDiscountBps,
    floorMinorUnits,
    ceilingMinorUnits
  } = ctx;

  if (role === 'seller') {
    const computedFloor = Math.max(1, Math.round(listAmountMinorUnits * (1 - sellerMinDiscountBps / 10_000)));
    const sellerFloor = floorMinorUnits === null ? computedFloor : Math.max(1, floorMinorUnits);

    if (phase === 'opening') {
      const openingBase = Math.max(sellerFloor, listAmountMinorUnits);
      const opening = ceilingMinorUnits === null ? openingBase : Math.min(openingBase, ceilingMinorUnits);
      return {
        action: 'offer',
        offerMinorUnits: opening,
        utterance: `${speaker}: Opening offer is ${toAmountText(opening, currency)} with dependable delivery.`,
        reason: 'opening_offer'
      };
    }

    if (buyerOfferMinorUnits !== null && buyerOfferMinorUnits >= sellerFloor) {
      return {
        action: 'accept',
        offerMinorUnits: buyerOfferMinorUnits,
        utterance: `${speaker}: Accepted at ${toAmountText(buyerOfferMinorUnits, currency)} in round ${round}.`,
        reason: 'buyer_offer_meets_floor'
      };
    }

    const anchor = buyerOfferMinorUnits === null ? sellerFloor : buyerOfferMinorUnits;
    const previous = lastSellerOfferMinorUnits === null ? listAmountMinorUnits : lastSellerOfferMinorUnits;
    const nextBase = Math.max(sellerFloor, Math.round((previous + anchor) / 2));
    const next = ceilingMinorUnits === null ? nextBase : Math.min(nextBase, ceilingMinorUnits);

    return {
      action: 'counter',
      offerMinorUnits: next,
      utterance: `${speaker}: I can move to ${toAmountText(next, currency)} while keeping service quality.`,
      reason: 'seller_counter'
    };
  }

  if (sellerOfferMinorUnits === null) {
    throw new Error('sellerOfferMinorUnits is required for buyer turns');
  }

  const target = Math.max(1, Math.round(listAmountMinorUnits * (1 - buyerTargetDiscountBps / 10_000)));
  const concession = Math.max(1, Math.round(listAmountMinorUnits * (buyerConcessionBpsPerRound / 10_000)));
  const dynamicMaxAccept = target + concession * Math.max(0, round - 1);
  const buyerCeiling = ceilingMinorUnits === null ? dynamicMaxAccept : Math.min(dynamicMaxAccept, ceilingMinorUnits);

  if (sellerOfferMinorUnits <= buyerCeiling) {
    return {
      action: 'accept',
      offerMinorUnits: sellerOfferMinorUnits,
      utterance: `${speaker}: Accepted at ${toAmountText(sellerOfferMinorUnits, currency)} in round ${round}.`,
      reason: 'offer_within_threshold'
    };
  }

  const counterRaw = Math.max(target, sellerOfferMinorUnits - concession);
  const counter = ceilingMinorUnits === null ? counterRaw : Math.min(counterRaw, ceilingMinorUnits);
  if (counter >= sellerOfferMinorUnits) {
    return {
      action: 'reject',
      offerMinorUnits: null,
      utterance: `${speaker}: I cannot justify these terms in this round.`,
      reason: 'no_counter_space'
    };
  }

  return {
    action: 'counter',
    offerMinorUnits: counter,
    utterance: `${speaker}: I can proceed at ${toAmountText(counter, currency)} if we close now.`,
    reason: 'buyer_counter'
  };
}

function hasTurnContext(input) {
  const message = input?.message;
  if (message && typeof message === 'object') {
    return true;
  }
  if ('sellerOfferMinorUnits' in input || 'buyerOfferMinorUnits' in input || 'phase' in input || 'round' in input) {
    return true;
  }
  return false;
}

function resolveDecisionEngine(input) {
  const raw = String(
    input['decision-engine']
    ?? input.decisionEngine
    ?? input.engine
    ?? 'rule'
  ).trim().toLowerCase();

  if (['rule', 'rules', 'strategy'].includes(raw)) {
    return 'rule';
  }
  if (['openclaw', 'model', 'llm'].includes(raw)) {
    return 'openclaw';
  }
  throw new Error(`unsupported decision engine: ${raw}`);
}

function resolveOpenClawOptions(input) {
  return {
    providerEnvName: String(input['provider-env'] ?? input.providerEnv ?? 'OPENAI_API_KEY').trim(),
    directApiKey: String(input['api-key'] ?? input.apiKey ?? '').trim(),
    allowNoKey: toBoolean(input['allow-no-key'] ?? input.allowNoKey, false),
    thinking: String(input.thinking ?? input['openclaw-thinking'] ?? 'low').trim(),
    timeoutSeconds: toPositiveInt(input.timeout ?? input['openclaw-timeout-seconds'] ?? 60, 60),
    extraPrompt: String(input['openclaw-extra-prompt'] ?? input.openclawExtraPrompt ?? '').trim()
  };
}

function buildOpenClawTurnPrompt({ turnInput, role, extraPrompt }) {
  const compactPayload = JSON.stringify(turnInput);
  const roleText = role === 'seller' ? 'seller' : 'buyer';
  return [
    `You are the ${roleText} side in an A2A pricing negotiation turn.`,
    'Contract=turn-decision-v1.',
    'Return ONLY JSON with exactly these keys: action, offerMinorUnits, utterance, reason.',
    'action must be one of offer/counter/accept/reject.',
    'For offer/counter, offerMinorUnits must be a positive integer.',
    'For accept/reject, offerMinorUnits can be null.',
    'Do not output markdown or any extra text.',
    'Do not output session-level fields such as result/status/trace/dialogue/history.',
    extraPrompt || '',
    `Context: ${compactPayload}`
  ].filter(Boolean).join(' ');
}

function resolveOpenClawBin() {
  const configured = String(process.env.A2A_OPENCLAW_BIN ?? '').trim();
  if (configured) {
    return {
      command: configured,
      argsPrefix: []
    };
  }

  if (process.platform === 'win32') {
    const appData = String(process.env.APPDATA ?? '').trim();
    if (appData) {
      const pathModule = require('node:path');
      const fsModule = require('node:fs');
      const mjsPath = pathModule.join(appData, 'npm', 'node_modules', 'openclaw', 'openclaw.mjs');
      if (fsModule.existsSync(mjsPath)) {
        return {
          command: process.execPath,
          argsPrefix: [mjsPath]
        };
      }
    }
  }

  return {
    command: 'openclaw',
    argsPrefix: []
  };
}

async function runOpenClawTurnDecision({ turnInput, role, agentId, openclawOptions }) {
  const { spawn } = await import('node:child_process');
  const {
    providerEnvName,
    directApiKey,
    allowNoKey,
    thinking,
    timeoutSeconds,
    extraPrompt
  } = openclawOptions;

  const env = { ...process.env };
  if (directApiKey) {
    env[providerEnvName] = directApiKey;
  }

  if (!allowNoKey && !hasAnyProviderKey(env)) {
    throw new Error(
      'openclaw engine requires a model provider key. Set OPENAI_API_KEY (or another supported *_API_KEY), or pass --api-key with --provider-env.'
    );
  }

  const prompt = buildOpenClawTurnPrompt({ turnInput, role, extraPrompt });
  const sessionId = String(
    turnInput?.message?.sessionId
    ?? turnInput?.session?.sessionId
    ?? turnInput?.sessionId
    ?? ''
  ).trim();

  const runtime = resolveOpenClawBin();
  const args = [...runtime.argsPrefix, 'agent', '--local', '--json', '--message', prompt];

  if (sessionId) {
    args.push('--session-id', sessionId);
  } else if (agentId) {
    args.push('--agent', String(agentId));
  }
  if (thinking) {
    args.push('--thinking', thinking);
  }
  if (timeoutSeconds > 0) {
    args.push('--timeout', String(timeoutSeconds));
  }

  const rawOutput = await new Promise((resolve, reject) => {
    const child = spawn(runtime.command, args, {
      shell: false,
      windowsHide: true,
      stdio: ['ignore', 'pipe', 'pipe'],
      env
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    child.on('error', (err) => {
      reject(err);
    });

    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`openclaw exited ${code}; stderr=${stderr.trim()}`));
        return;
      }
      resolve(stdout);
    });
  });

  const candidates = extractTextCandidatesFromOpenClawOutput(rawOutput);
  let lastParseError = null;
  for (const candidate of candidates) {
    try {
      return extractDecisionFromAnyText(candidate);
    } catch (err) {
      lastParseError = err;
    }
  }

  const detail = lastParseError instanceof Error ? `; last_error=${lastParseError.message}` : '';
  throw new Error(`unable to extract turn decision JSON from OpenClaw output${detail}`);
}

async function decideTurnByEngine({ turnInput, decisionEngine, openclawOptions, agentId }) {
  if (decisionEngine === 'openclaw') {
    return runOpenClawTurnDecision({
      turnInput,
      role: normalizeRole(turnInput.role),
      agentId,
      openclawOptions
    });
  }

  const ctx = resolveTurnContext(turnInput);
  return decideTurn(ctx);
}

async function fetchJsonOrThrow(url, options = {}) {
  const response = await fetch(url, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.error ?? `HTTP ${response.status} ${url}`);
  }
  return body;
}

function makeAgentResponder({
  role,
  agentId,
  expectedAuthToken,
  sessionStore,
  decisionEngine,
  openclawOptions
}) {
  return async (envelope) => {
    const type = String(envelope?.type ?? '');
    switch (type) {
      case 'HELLO':
        return {
          ok: true,
          role,
          agentId,
          protocolVersion: 'a2a-negotiation/1.0',
          agentType: decisionEngine === 'openclaw' ? 'skill-gateway-loop-openclaw' : 'skill-gateway-loop'
        };
      case 'AUTH':
        return {
          ok: String(envelope?.payload?.token ?? '') === expectedAuthToken,
          role,
          agentId
        };
      case 'CAPABILITIES':
        return {
          ok: true,
          capabilities: [
            'natural_language_negotiation',
            'structured_offer_decision',
            decisionEngine === 'openclaw' ? 'openclaw_reasoning' : 'skill_gateway_loop'
          ]
        };
      case 'NEGOTIATION_OPEN': {
        sessionStore.set(String(envelope.sessionId ?? ''), {
          ...(envelope.payload ?? {}),
          openedAt: Date.now()
        });
        return { ok: true, sessionId: envelope.sessionId };
      }
      case 'NEGOTIATION_TURN': {
        const sessionId = String(envelope.sessionId ?? '');
        const session = sessionStore.get(sessionId) ?? {};
        const turnInput = {
          role,
          session,
          message: envelope
        };

        const decision = await decideTurnByEngine({
          turnInput,
          decisionEngine,
          openclawOptions,
          agentId
        });

        return {
          ok: true,
          ...decision,
          source: decisionEngine === 'openclaw' ? 'openclaw-local' : 'a2a-market-acp-lite-negotiation'
        };
      }
      case 'HEARTBEAT':
        return { ok: true, at: Date.now() };
      default:
        return { ok: false, error: `unsupported message type: ${type || 'unknown'}` };
    }
  };
}

async function waitForAgentOnline({ gateway, agentId, timeoutMs, retryDelayMs }) {
  const startedAt = Date.now();
  while (true) {
    const status = await fetchJsonOrThrow(`${gateway}/agents/status`);
    const exists = (status.agents ?? []).some((item) => item.agentId === agentId);
    if (exists) {
      return;
    }
    if (Date.now() - startedAt >= timeoutMs) {
      throw new Error(`counterparty agent not online within timeout: ${agentId}`);
    }
    await sleep(retryDelayMs);
  }
}

function resolveOptionalPositive(value, fieldName) {
  if (value === undefined || value === null || value === '') {
    return null;
  }
  const numeric = Number(value);
  if (!Number.isInteger(numeric) || numeric <= 0) {
    throw new Error(`${fieldName} must be a positive integer`);
  }
  return numeric;
}

async function runGatewayLoop(input) {
  const role = normalizeRole(input.role);
  const gateway = String(input.gateway ?? 'http://127.0.0.1:3085').trim().replace(/\/+$/, '');
  const agentId = String(input['agent-id'] ?? input.agentId ?? `${role}-skill-loop`).trim();
  const expectedAuthToken = String(input['auth-token'] ?? input.authToken ?? 'market-auth-token').trim();
  const pullTimeoutMs = toPositiveInt(input['pull-timeout-ms'] ?? input.pullTimeoutMs, 25_000);
  const retryDelayMs = toPositiveInt(input['retry-delay-ms'] ?? input.retryDelayMs, 1_000);
  const maxPolls = toNonNegativeInt(input['max-polls'] ?? input.maxPolls, 0);
  const verbose = toBoolean(input.verbose, true);
  const decisionEngine = resolveDecisionEngine(input);
  const openclawOptions = resolveOpenClawOptions(input);
  const autoStartSession = toBoolean(
    input['start-session']
    ?? input.startSession
    ?? input.negotiate,
    false
  );
  const stopOnSessionEnd = toBoolean(input['stop-on-session-end'] ?? input.stopOnSessionEnd, false);
  const waitCounterpartyMs = toNonNegativeInt(input['wait-counterparty-ms'] ?? input.waitCounterpartyMs, 15_000);

  if (!agentId) {
    throw new Error('agentId is required in gateway mode');
  }

  const registerPayload = {
    agentId,
    role
  };
  const fixedToken = String(input.token ?? '').trim();
  if (fixedToken) {
    registerPayload.token = fixedToken;
  }

  const registration = await fetchJsonOrThrow(`${gateway}/agents/register`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(registerPayload)
  });
  const token = String(registration.token ?? fixedToken).trim();
  if (!token) {
    throw new Error('gateway register succeeded but token is missing');
  }

  process.stdout.write(`${JSON.stringify({
    ok: true,
    mode: 'gateway-agent-loop',
    role,
    agentId,
    decisionEngine,
    gateway,
    pullUrl: registration.pullUrl ?? `${gateway}/agents/pull?agentId=${encodeURIComponent(agentId)}&token=${encodeURIComponent(token)}`
  })}\n`);

  const sessionStore = new Map();
  const respond = makeAgentResponder({
    role,
    agentId,
    expectedAuthToken,
    sessionStore,
    decisionEngine,
    openclawOptions
  });

  let running = true;
  let pollCount = 0;

  if (autoStartSession) {
    const counterpartyAgentId = String(
      input['counterparty-agent-id']
      ?? input.counterpartyAgentId
      ?? ''
    ).trim();
    if (!counterpartyAgentId) {
      throw new Error('start-session requires --counterparty-agent-id');
    }

    const listAmountMinorUnits = toPositiveInt(
      input['list-amount-minor-units']
      ?? input.listAmountMinorUnits
      ?? input['current-offer-minor-units']
      ?? 9_000,
      9_000
    );
    const maxRounds = toPositiveInt(input['max-rounds'] ?? input.maxRounds, 5);
    const currency = String(input.currency ?? 'USD').trim() || 'USD';
    const product = String(input.product ?? input.item ?? 'mechanical keyboard').trim();
    const goal = String(
      input.goal
      ?? (role === 'buyer' ? 'close deal with fair discount' : 'preserve margin and close deal')
    ).trim();
    const floorMinorUnits = resolveOptionalPositive(input['floor-minor-units'] ?? input.floorMinorUnits, 'floor-minor-units');
    const ceilingMinorUnits = resolveOptionalPositive(input['ceiling-minor-units'] ?? input.ceilingMinorUnits, 'ceiling-minor-units');
    const sessionId = String(input['session-id'] ?? input.sessionId ?? `nego_${Date.now()}`).trim();

    const buyerAgentId = role === 'buyer' ? agentId : counterpartyAgentId;
    const sellerAgentId = role === 'seller' ? agentId : counterpartyAgentId;
    const neededCounterparty = role === 'buyer' ? sellerAgentId : buyerAgentId;

    void (async () => {
      try {
        if (waitCounterpartyMs > 0) {
          await waitForAgentOnline({
            gateway,
            agentId: neededCounterparty,
            timeoutMs: waitCounterpartyMs,
            retryDelayMs
          });
        }

        process.stdout.write(`${JSON.stringify({
          ok: true,
          mode: 'gateway-agent-loop',
          event: 'session_starting',
          sessionId,
          buyerAgentId,
          sellerAgentId,
          listAmountMinorUnits,
          currency,
          maxRounds
        })}\n`);

        const negotiationPayload = await fetchJsonOrThrow(`${gateway}/sessions/negotiate`, {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({
            sessionId,
            buyerAgentId,
            sellerAgentId,
            buyerLabel: buyerAgentId,
            sellerLabel: sellerAgentId,
            listAmountMinorUnits,
            currency,
            maxRounds,
            policy: {
              product,
              goal,
              requestedByRole: role,
              floorMinorUnits,
              ceilingMinorUnits
            }
          })
        });

        process.stdout.write(`${JSON.stringify({
          ok: true,
          mode: 'gateway-agent-loop',
          event: 'session_finished',
          sessionId,
          traceUrl: negotiationPayload.traceUrl ?? null,
          result: negotiationPayload.result ?? null
        })}\n`);

        if (stopOnSessionEnd) {
          running = false;
        }
      } catch (err) {
        const error = err instanceof Error ? err.message : String(err);
        process.stderr.write(`${JSON.stringify({
          ok: false,
          mode: 'gateway-agent-loop',
          event: 'session_error',
          error
        })}\n`);
        if (stopOnSessionEnd) {
          running = false;
        }
      }
    })();
  }

  process.on('SIGINT', () => {
    running = false;
  });

  while (running) {
    if (maxPolls > 0 && pollCount >= maxPolls) {
      break;
    }

    try {
      const pullUrl = `${gateway}/agents/pull?agentId=${encodeURIComponent(agentId)}&token=${encodeURIComponent(token)}&timeoutMs=${pullTimeoutMs}`;
      const pull = await fetchJsonOrThrow(pullUrl);
      pollCount += 1;
      const message = pull.message ?? null;
      if (!message) {
        continue;
      }

      const response = await respond(message);
      await fetchJsonOrThrow(`${gateway}/agents/respond`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          agentId,
          token,
          inReplyTo: message.messageId,
          response
        })
      });

      if (verbose) {
        process.stdout.write(`${JSON.stringify({
          ok: true,
          mode: 'gateway-agent-loop',
          event: 'responded',
          type: message.type,
          sessionId: message.sessionId ?? null,
          inReplyTo: message.messageId,
          response
        })}\n`);
      }
    } catch (err) {
      const error = err instanceof Error ? err.message : String(err);
      process.stderr.write(`${JSON.stringify({
        ok: false,
        mode: 'gateway-agent-loop',
        event: 'poll_error',
        agentId,
        gateway,
        error
      })}\n`);
      if (!running) {
        break;
      }
      await sleep(retryDelayMs);
    }
  }

  process.stdout.write(`${JSON.stringify({
    ok: true,
    mode: 'gateway-agent-loop',
    event: 'stopped',
    agentId,
    polls: pollCount
  })}\n`);
}

async function main() {
  const flags = parseArgv(process.argv.slice(2));
  const stdinInput = await readStdinJson().catch(() => ({}));
  const input = { ...stdinInput, ...flags };

  if (hasTurnContext(input)) {
    throw new Error(
      'single-turn mode is disabled. Use gateway loop mode only: provide role/gateway/agent-id (and optional start-session + counterparty-agent-id).'
    );
  }

  await runGatewayLoop(input);
}

main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  process.stderr.write(message);
  process.exitCode = 1;
});
