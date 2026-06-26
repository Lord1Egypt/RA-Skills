const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const {
  AbiCoder,
  Interface,
  JsonRpcProvider,
  Wallet,
  encodeBytes32String,
  getCreateAddress,
  keccak256,
} = require('ethers');
const { Api3ReaderProxyV1Factory__factory } = require('@api3/contracts');
const {
  browserPlan,
  executeBuySubscription,
  parseArgs,
  purchaseInputs,
} = require('./api3-feed-manager');
const {
  buildRequiredFeeds,
  discoverMarkets,
  ensureFeeds,
  normalizeIntent,
  validatePlanMarketRequest,
} = require('./part2-planner');

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const CONTRACT_ARTIFACT_DIR = path.join(ROOT_DIR, 'data', 'part2', 'contract-artifacts');
const MORPHO_CONTRACT_ARTIFACT_PATHS = Object.freeze({
  MorphoApi3DirectOracle: path.join(CONTRACT_ARTIFACT_DIR, 'MorphoApi3DirectOracle.json'),
  MorphoApi3CompositeOracle: path.join(CONTRACT_ARTIFACT_DIR, 'MorphoApi3CompositeOracle.json'),
});
const DEFAULT_ACTIVATION_MODE = 'check-only';
const DEFAULT_EXECUTION_MODE = 'planning-only';
const DEFAULT_MARKET_SHAPE_INTENT = 'single-market';
const DEFAULT_MARKET_SET_STRATEGY = 'one-market-per-asset-pair';
const SHARED_EVK_ONLY_WARNING = 'Planner execution is EVK-first in this phase. Morpho is reserved for a later protocol track.';
const ABI_CODER = AbiCoder.defaultAbiCoder();
const contractArtifactCache = new Map();
const MORPHO_INTERFACE = new Interface([
  'function createMarket((address loanToken,address collateralToken,address oracle,address irm,uint256 lltv) marketParams)',
  'function idToMarketParams(bytes32 id) view returns (address loanToken,address collateralToken,address oracle,address irm,uint256 lltv)',
  'function market(bytes32 id) view returns (uint128 totalSupplyAssets,uint128 totalSupplyShares,uint128 totalBorrowAssets,uint128 totalBorrowShares,uint128 lastUpdate,uint128 fee)',
  'function isIrmEnabled(address irm) view returns (bool)',
  'function isLltvEnabled(uint256 lltv) view returns (bool)',
]);
const MORPHO_ORACLE_INTERFACE = new Interface([
  'function price() view returns (uint256)',
]);
const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';
const SEND_ACKNOWLEDGEMENT = 'I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS';
const DEFAULT_DRY_RUN_SIMULATION_FROM_ADDRESS = '0x000000000000000000000000000000000000dEaD';
const AGENT_DECISION_FILE_NAME = 'agent-decision.json';
const UNSAFE_PLACEHOLDER_RE = /replace-with|example\.com|\.example\b|dummy|placeholder/i;
const UNSAFE_REPEATED_HEX_RE = /^0x([012aAbB])\1+$/;
const PRIVATE_KEY_ENV_NAME_RE = /^[A-Z][A-Z0-9_]*$/;
const PRIVATE_KEY_HEX_RE = /^(?:0x)?[a-fA-F0-9]{64}$/;
const FEED_FUNDING_MODE_VALUES = Object.freeze(['classify-only', 'dry-run', 'real-send']);
const FEED_FUNDING_MODE_ALIASES = Object.freeze({
  'check-only': 'classify-only',
  simulate: 'dry-run',
});
const RISK_PRESET_LLTV_DEFAULTS = Object.freeze({
  core: '860000000000000000',
  isolated: '860000000000000000',
  'btc-major': '860000000000000000',
  'eth-major': '860000000000000000',
  'stable-major': '915000000000000000',
});

const MORPHO_DAPI_SYMBOL_ALIASES = Object.freeze({
  WETH: 'ETH',
  WBTC: 'BTC',
  CBBTC: 'BTC',
  TBTC: 'BTC',
});

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function canonicalizeMorphoFeedName(feedName) {
  const normalized = String(feedName || '').trim().toUpperCase();
  if (!normalized) {
    return normalized;
  }

  if (!normalized.includes('/')) {
    return MORPHO_DAPI_SYMBOL_ALIASES[normalized] || normalized;
  }

  return normalized
    .split('/')
    .map((segment) => MORPHO_DAPI_SYMBOL_ALIASES[segment] || segment)
    .join('/');
}

function assertPlainObject(value, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object`);
}

function assertAllowedKeys(value, allowedKeys, label) {
  const extras = Object.keys(value).filter((key) => !allowedKeys.includes(key));
  assert(extras.length === 0, `${label} has unsupported properties: ${extras.join(', ')}`);
}

function assertBooleanIfPresent(value, label) {
  if (value !== undefined) {
    assert(typeof value === 'boolean', `${label} must be a boolean`);
  }
}

function assertStringIfPresent(value, label) {
  if (value !== undefined) {
    assert(typeof value === 'string' && value.trim() !== '', `${label} must be a non-empty string`);
  }
}

function assertEnvVarNameIfPresent(value, label) {
  if (value !== undefined) {
    assert(typeof value === 'string' && PRIVATE_KEY_ENV_NAME_RE.test(value.trim()), `${label} must be an uppercase environment variable name`);
  }
}

function assertEnum(value, allowed, label) {
  assert(allowed.includes(value), `${label} must be one of: ${allowed.join(', ')}`);
}

function assertHexAddressIfPresent(value, label) {
  if (value !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value), `${label} must be a 20-byte hex address`);
  }
}

function assertLltvIfPresent(value, label) {
  if (value === undefined) {
    return;
  }

  const asString = String(value).trim();
  assert(/^\d+$/.test(asString), `${label} must be an integer string`);
}

function isUnsafePlaceholderString(value) {
  return typeof value === 'string' && UNSAFE_PLACEHOLDER_RE.test(value);
}

function isUnsafePlaceholderHex(value) {
  return typeof value === 'string' && /^0x[0-9a-fA-F]+$/.test(value) && UNSAFE_REPEATED_HEX_RE.test(value);
}

function collectUnsafePlaceholders(value, label = 'request', findings = []) {
  if (value === null || value === undefined) {
    return findings;
  }

  if (typeof value === 'string') {
    if (isUnsafePlaceholderString(value) || isUnsafePlaceholderHex(value)) {
      findings.push(`${label} contains unsafe placeholder value`);
    }
    return findings;
  }

  if (Array.isArray(value)) {
    value.forEach((entry, index) => collectUnsafePlaceholders(entry, `${label}[${index}]`, findings));
    return findings;
  }

  if (typeof value === 'object') {
    for (const [key, entry] of Object.entries(value)) {
      collectUnsafePlaceholders(entry, `${label}.${key}`, findings);
    }
  }

  return findings;
}

function collectInlineSecretFindings(request) {
  const findings = [];

  if (request?.feedFunding?.privateKey) {
    findings.push('request.feedFunding.privateKey contains a raw private key. Use request.feedFunding.privateKeyEnv instead.');
  }
  if (request?.send?.privateKey) {
    findings.push('request.send.privateKey contains a raw private key. Use request.send.privateKeyEnv instead.');
  }

  return findings;
}

function normalizePrivateKeyHex(value, label) {
  const trimmed = String(value || '').trim();
  assert(PRIVATE_KEY_HEX_RE.test(trimmed), `${label} must be a 32-byte hex private key with or without a 0x prefix`);
  return trimmed.startsWith('0x') ? trimmed : `0x${trimmed}`;
}

function assertPrivateKeyHexIfPresent(value, label) {
  if (value !== undefined) {
    normalizePrivateKeyHex(value, label);
  }
}

function normalizeFeedFundingMode(value, label = 'request.feedFunding.mode') {
  const raw = String(value || '').trim().toLowerCase();
  const canonical = FEED_FUNDING_MODE_ALIASES[raw] || raw;
  assert(FEED_FUNDING_MODE_VALUES.includes(canonical), `${label} must be one of: ${FEED_FUNDING_MODE_VALUES.join(', ')}`);
  return canonical;
}

function getFeedFundingMode(request) {
  if (!request?.feedFunding?.mode) {
    return 'classify-only';
  }

  return normalizeFeedFundingMode(request.feedFunding.mode);
}

function resolvePrivateKeyInput(value, label) {
  if (value?.privateKey !== undefined && value?.privateKey !== null && String(value.privateKey).trim() !== '') {
    return normalizePrivateKeyHex(value.privateKey, `${label}.privateKey`);
  }

  if (value?.privateKeyEnv === undefined || value?.privateKeyEnv === null || String(value.privateKeyEnv).trim() === '') {
    return null;
  }

  const envName = String(value.privateKeyEnv).trim();
  assert(PRIVATE_KEY_ENV_NAME_RE.test(envName), `${label}.privateKeyEnv must be an uppercase environment variable name`);
  const resolved = process.env[envName];
  assert(resolved && PRIVATE_KEY_HEX_RE.test(String(resolved).trim()), `${label}.privateKeyEnv did not resolve to a valid 32-byte hex private key with or without a 0x prefix`);
  return normalizePrivateKeyHex(resolved, `${label}.privateKeyEnv`);
}

function requestMayExecuteLiveTransactions(request) {
  const sendIsDryRun = request?.send?.dryRun === true || String(request?.send?.dryRun).toLowerCase() === 'true';
  return getFeedFundingMode(request) === 'real-send'
    || (request?.send?.enabled === true && !sendIsDryRun)
    || (request?.broadcast?.enabled === true && !sendIsDryRun);
}

function buildMorphoApprovalSummary({ request, workflow = null, phase = 'preflight', blockers = [], artifactPaths = {} }) {
  const collateralAssets = Array.isArray(request?.collateralAssets) ? request.collateralAssets : [];
  const borrowAssets = Array.isArray(request?.borrowAssets) ? request.borrowAssets : [];
  const fundingMode = request?.feedFunding?.mode || 'classify-only';
  const sendRequested = request?.send?.enabled === true;
  const sendIsDryRun = request?.send ? request.send.dryRun !== false : true;
  const liveTxRequested = requestMayExecuteLiveTransactions(request);
  const fundingPhase = workflow ? buildFeedFundingPhaseResult(workflow) : null;
  const browserHandoffLikely = Boolean(fundingPhase && fundingPhase.browserPlanEntries.length > 0);
  const marketCountEstimate = workflow?.prepareMorphoMarket?.marketCount || (collateralAssets.length > 0 && borrowAssets.length > 0
    ? collateralAssets.length * borrowAssets.length
    : 0);
  const phases = ['preflight', 'feed-classification'];

  if (browserHandoffLikely) {
    phases.push('funding-handoff');
  } else if (fundingMode !== 'classify-only') {
    phases.push('funding-execution');
    if (fundingMode === 'real-send') {
      phases.push('propagation-wait');
    }
  }

  if (sendRequested) {
    phases.push('adapter-deployment', 'market-deployment');
  }

  if (sendRequested || liveTxRequested) {
    phases.push('verification');
  }

  const uniquePhases = uniqueStrings(phases);
  const whatWillRun = [
    'Validate request shape, RPC inputs, and Morpho policy requirements.',
    `Classify Api3 feed readiness for ${marketCountEstimate || 'the requested'} Morpho market${marketCountEstimate === 1 ? '' : 's'}.`,
  ];

  if (browserHandoffLikely) {
    whatWillRun.push('Stop and hand off to a browser-assisted feed funding step if autonomous execution is not supported.');
  } else if (fundingMode === 'real-send') {
    whatWillRun.push('Attempt executable feed funding before deployment, then wait for propagation/readability before continuing.');
  } else if (fundingMode === 'dry-run') {
    whatWillRun.push('Simulate feed funding if required without broadcasting transactions.');
  } else if (fundingMode !== 'classify-only') {
    whatWillRun.push(`Run the requested feed funding mode (${fundingMode}) before deployment when needed.`);
  }

  if (sendRequested) {
    whatWillRun.push(sendIsDryRun
      ? 'Prepare deployment transactions in dry-run mode and persist the resulting artifacts.'
      : 'Deploy Morpho oracle adapter plus market creation transactions onchain when blockers stay clear.');
  }

  if (sendRequested || liveTxRequested) {
    whatWillRun.push('Verify the final Morpho market parameters and oracle.price() after a live send or when verification is forced.');
  }

  let expectedDuration;
  if (fundingMode === 'real-send' && liveTxRequested) {
    expectedDuration = {
      label: 'long',
      estimate: '2-10+ minutes',
      rationale: 'Live feed funding may be followed by propagation waits before adapter deployment, market creation, and verification can finish.',
    };
  } else if (liveTxRequested) {
    expectedDuration = {
      label: 'medium',
      estimate: '1-5 minutes',
      rationale: 'This path can broadcast transactions and then wait for confirmations and verification.',
    };
  } else if (sendRequested || fundingMode !== 'classify-only') {
    expectedDuration = {
      label: 'short',
      estimate: 'under 1 minute to a few minutes',
      rationale: 'This path still performs planning, artifact generation, and possibly dry-run transaction preparation.',
    };
  } else {
    expectedDuration = {
      label: 'short',
      estimate: 'seconds to under 1 minute',
      rationale: 'This path is planning-only unless later upgraded to a live or dry-run execution mode.',
    };
  }

  let resourceImpact;
  if (fundingMode === 'real-send' || liveTxRequested) {
    resourceImpact = {
      level: 'moderate',
      summary: 'RPC-heavy path with resumable artifacts, possible propagation polling, and possible transaction submission.',
      cpu: 'low-to-moderate',
      disk: 'moderate',
      network: 'high',
    };
  } else if (sendRequested || fundingMode !== 'classify-only') {
    resourceImpact = {
      level: 'moderate',
      summary: 'Artifact-heavy planning path with dry-run execution support and repeated local workflow recomputation.',
      cpu: 'low-to-moderate',
      disk: 'moderate',
      network: 'medium',
    };
  } else {
    resourceImpact = {
      level: 'low',
      summary: 'Planning/classification path with small artifact writes and no transaction submission.',
      cpu: 'low',
      disk: 'low',
      network: 'low-to-medium',
    };
  }

  const transactionCountEstimate = marketCountEstimate > 0 && sendRequested
    ? {
        min: marketCountEstimate,
        max: marketCountEstimate * 2,
        rationale: 'Each market always needs creation, and adapter deployment is often needed too.',
      }
    : null;

  return {
    phase,
    approvalMode: liveTxRequested ? 'live-send' : sendRequested ? 'dry-run' : 'planning-only',
    requiresUserApproval: liveTxRequested || browserHandoffLikely,
    maySendTransactions: liveTxRequested,
    browserHandoffLikely,
    fundingMode,
    marketCountEstimate,
    transactionCountEstimate,
    selectedAssets: {
      collateralSymbols: collateralAssets.map((asset) => asset.symbol),
      borrowSymbols: borrowAssets.map((asset) => asset.symbol),
    },
    phases: uniquePhases,
    whatWillRun,
    expectedDuration,
    resourceImpact,
    acknowledgement: {
      required: liveTxRequested,
      token: liveTxRequested ? SEND_ACKNOWLEDGEMENT : null,
    },
    blockers: uniqueStrings(blockers),
    artifactPaths,
  };
}

function assertNoUnsafeLivePlaceholders(request) {
  if (!requestMayExecuteLiveTransactions(request)) {
    return;
  }

  const findings = collectUnsafePlaceholders(request);
  assert(findings.length === 0, `Unsafe placeholder values are forbidden for live-capable Morpho execution: ${uniqueStrings(findings).join('; ')}`);
}

function readJsonFile(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function resolveUserPath(filePath) {
  const rawPath = String(filePath);
  if (path.isAbsolute(rawPath)) {
    return rawPath;
  }

  return path.resolve(process.cwd(), rawPath);
}

function resolveExistingUserPath(filePath) {
  const cwdResolvedPath = resolveUserPath(filePath);
  if (fs.existsSync(cwdResolvedPath)) {
    return cwdResolvedPath;
  }

  return path.resolve(ROOT_DIR, String(filePath));
}

function writeJsonFile(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function readJsonFileIfExists(filePath) {
  return fs.existsSync(filePath) ? readJsonFile(filePath) : null;
}

function getRunDirFromOptions(options = {}) {
  const runDir = options.runDir || options.resumeFromRunDir;
  assert(runDir, '--run-dir or --resume-from-run-dir is required');
  return resolveExistingUserPath(runDir);
}

function isCliFlagEnabled(value) {
  return value === true || String(value).toLowerCase() === 'true';
}

function makeArtifactRunDir(label) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  return path.join(ROOT_DIR, 'artifacts', label, timestamp);
}

function resolveMorphoWrapperPaths(options = {}) {
  const runDir = options.runDir
    ? resolveUserPath(options.runDir)
    : makeArtifactRunDir('morpho-wrapper');

  return {
    runDir,
    transactionPayloadsDir: path.join(runDir, 'transaction-payloads'),
    deployOutputPath: options.deployOutputFile
      ? resolveUserPath(options.deployOutputFile)
      : path.join(runDir, 'deploy-output.json'),
    verifyOutputPath: options.verifyOutputFile
      ? resolveUserPath(options.verifyOutputFile)
      : path.join(runDir, 'verify-output.json'),
  };
}

function resolveMorphoEnsureDeployPaths(options = {}) {
  const runDir = options.resumeFromRunDir
    ? resolveExistingUserPath(options.resumeFromRunDir)
    : options.runDir
    ? resolveUserPath(options.runDir)
    : makeArtifactRunDir(String(options.artifactLabel || 'morpho-ensure-deploy'));

  return {
    runDir,
    transactionPayloadsDir: path.join(runDir, 'transaction-payloads'),
    requestPath: path.join(runDir, 'request.json'),
    initialWorkflowPath: path.join(runDir, 'workflow.initial.json'),
    fundingPath: path.join(runDir, 'funding.json'),
    fundedFeedCachePath: path.join(runDir, 'funded-feed-cache.json'),
    propagationPath: path.join(runDir, 'propagation.json'),
    progressPath: path.join(runDir, 'progress-events.jsonl'),
    approvalSummaryPath: path.join(runDir, 'approval-summary.json'),
    perfSummaryPath: path.join(runDir, 'perf-summary.json'),
    rollbackPlanPath: path.join(runDir, 'rollback-plan.json'),
    agentDecisionPath: path.join(runDir, AGENT_DECISION_FILE_NAME),
    summaryPath: path.join(runDir, 'summary.json'),
    deployOutputPath: options.deployOutputFile
      ? resolveUserPath(options.deployOutputFile)
      : path.join(runDir, 'deploy-output.json'),
    verifyOutputPath: options.verifyOutputFile
      ? resolveUserPath(options.verifyOutputFile)
      : path.join(runDir, 'verify-output.json'),
  };
}

function writeMorphoRunArtifact(filePath, value) {
  writeJsonFile(filePath, value);
}

function sanitizeArtifactSlug(value, fallback = 'payload') {
  const normalized = String(value || '').trim().toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
  return normalized || fallback;
}

function externalizeMorphoTransactionPayloads(transactionPlan = [], transactionPayloadsDir) {
  if (!transactionPayloadsDir) {
    return Array.isArray(transactionPlan) ? transactionPlan : [];
  }

  return (Array.isArray(transactionPlan) ? transactionPlan : []).map((entry, index) => {
    if (!entry || typeof entry !== 'object' || typeof entry.data !== 'string' || !entry.data.startsWith('0x')) {
      return entry;
    }

    const payloadFileName = `${String(index + 1).padStart(3, '0')}-${sanitizeArtifactSlug(entry.transactionId, 'transaction')}.json`;
    const payloadPath = path.join(transactionPayloadsDir, payloadFileName);
    writeJsonFile(payloadPath, {
      transactionId: entry.transactionId,
      kind: entry.kind,
      marketKey: entry.marketKey,
      payloadKind: entry.payloadKind,
      data: entry.data,
    });

    const { data, ...rest } = entry;
    return {
      ...rest,
      payloadRef: payloadPath,
      dataBytes: Math.max(0, (data.length - 2) / 2),
      payloadOmitted: true,
    };
  });
}

function maybeExternalizeMorphoDeploymentPayloads(result, options = {}) {
  if (!result || !Array.isArray(result.transactionPlan)) {
    return result;
  }

  const runDir = options.runDir || options.resumeFromRunDir;
  if (!runDir) {
    return result;
  }

  const transactionPayloadsDir = path.join(resolveUserPath(runDir), 'transaction-payloads');
  const transactionPlanWithRefs = externalizeMorphoTransactionPayloads(result.transactionPlan, transactionPayloadsDir).map((entry, index) => ({
    ...result.transactionPlan[index],
    ...(entry && entry.payloadRef ? {
      payloadRef: entry.payloadRef,
      dataBytes: entry.dataBytes,
      payloadOmitted: entry.payloadOmitted,
    } : {}),
  }));

  return {
    ...result,
    transactionPlan: transactionPlanWithRefs,
  };
}

function getMorphoPerfState(options = {}) {
  if (!options.perfState) {
    options.perfState = {
      startedAt: new Date().toISOString(),
      startedAtMs: Date.now(),
      operations: [],
      aggregates: {},
    };
  }

  return options.perfState;
}

function recordMorphoPerf(options = {}, event = {}) {
  const perfState = getMorphoPerfState(options);
  const name = event.name || 'unknown';
  const elapsedMs = Number.isFinite(event.elapsedMs) ? event.elapsedMs : 0;
  const normalizedEvent = {
    at: new Date().toISOString(),
    name,
    elapsedMs,
    ...(event.details ? { details: event.details } : {}),
  };

  perfState.operations.push(normalizedEvent);
  if (!perfState.aggregates[name]) {
    perfState.aggregates[name] = {
      count: 0,
      totalElapsedMs: 0,
      maxElapsedMs: 0,
      minElapsedMs: null,
    };
  }

  const aggregate = perfState.aggregates[name];
  aggregate.count += 1;
  aggregate.totalElapsedMs += elapsedMs;
  aggregate.maxElapsedMs = Math.max(aggregate.maxElapsedMs, elapsedMs);
  aggregate.minElapsedMs = aggregate.minElapsedMs === null ? elapsedMs : Math.min(aggregate.minElapsedMs, elapsedMs);
}

async function measureMorphoPerf(options = {}, name, details, fn) {
  const startedAtMs = Date.now();
  try {
    return await fn();
  } finally {
    recordMorphoPerf(options, {
      name,
      elapsedMs: Date.now() - startedAtMs,
      details,
    });
  }
}

function buildMorphoPerfSummary(options = {}) {
  const perfState = options.perfState;
  if (!perfState) {
    return null;
  }

  return {
    startedAt: perfState.startedAt,
    finishedAt: new Date().toISOString(),
    totalElapsedMs: Date.now() - perfState.startedAtMs,
    operations: perfState.operations,
    aggregates: Object.fromEntries(Object.entries(perfState.aggregates).map(([name, aggregate]) => [
      name,
      {
        ...aggregate,
        averageElapsedMs: aggregate.count > 0 ? aggregate.totalElapsedMs / aggregate.count : 0,
      },
    ])),
  };
}

function withMorphoPerf(options = {}, perfSummaryPath) {
  const nextOptions = {
    ...options,
    ...(perfSummaryPath ? { perfSummaryPath } : {}),
  };
  getMorphoPerfState(nextOptions);
  return nextOptions;
}

function shouldEmitMorphoProgress(options = {}) {
  return options.progress !== false && String(options.progress || 'human').trim().toLowerCase() !== 'silent';
}

function getMorphoProgressFormat(options = {}) {
  const raw = String(options.progress || 'human').trim().toLowerCase();
  return raw === 'jsonl' ? 'jsonl' : 'human';
}

function formatMorphoProgressLine(event) {
  const prefix = `[morpho][${event.phase}][${event.status}]`;
  const extras = [];

  if (Number.isInteger(event.attempt)) {
    extras.push(`attempt ${event.attempt}`);
  }
  if (Number.isFinite(event.elapsedMs)) {
    extras.push(`elapsed ${event.elapsedMs}ms`);
  }
  if (Number.isFinite(event.waitMs)) {
    extras.push(`wait ${event.waitMs}ms`);
  }

  return extras.length > 0
    ? `${prefix} ${event.message} (${extras.join(', ')})`
    : `${prefix} ${event.message}`;
}

function emitMorphoProgress(options = {}, event = {}) {
  const normalizedEvent = {
    at: new Date().toISOString(),
    phase: event.phase || 'unknown',
    status: event.status || 'info',
    message: event.message || '',
    ...(event.details ? { details: event.details } : {}),
    ...(event.attempt !== undefined ? { attempt: event.attempt } : {}),
    ...(event.elapsedMs !== undefined ? { elapsedMs: event.elapsedMs } : {}),
    ...(event.waitMs !== undefined ? { waitMs: event.waitMs } : {}),
  };

  if (typeof options.onProgress === 'function') {
    options.onProgress(normalizedEvent);
  }
  if (Array.isArray(options.progressEvents)) {
    options.progressEvents.push(normalizedEvent);
  }
  if (options.progressPath) {
    fs.mkdirSync(path.dirname(options.progressPath), { recursive: true });
    fs.appendFileSync(options.progressPath, `${JSON.stringify(normalizedEvent)}\n`);
  }

  if (!shouldEmitMorphoProgress(options)) {
    return normalizedEvent;
  }

  if (getMorphoProgressFormat(options) === 'jsonl') {
    console.error(JSON.stringify(normalizedEvent));
  } else {
    console.error(formatMorphoProgressLine(normalizedEvent));
  }

  return normalizedEvent;
}

function withMorphoProgress(options = {}, progressPath) {
  return {
    ...options,
    ...(progressPath ? { progressPath } : {}),
  };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parsePositiveIntegerOption(value, fallback) {
  if (value === undefined || value === null || value === '') {
    return fallback;
  }

  const parsed = Number.parseInt(String(value), 10);
  return Number.isInteger(parsed) && parsed >= 0 ? parsed : fallback;
}

function loadContractArtifactBytecode(artifactPath) {
  const sidecarPath = artifactPath.replace(/\.json$/i, '.bytecode.txt');
  const rawBytecode = fs.readFileSync(sidecarPath, 'utf8').replace(/\s+/g, '');
  return rawBytecode.startsWith('0x') ? rawBytecode : `0x${rawBytecode}`;
}

function loadContractArtifact(contractName) {
  if (contractArtifactCache.has(contractName)) {
    return contractArtifactCache.get(contractName);
  }

  const artifactPath = MORPHO_CONTRACT_ARTIFACT_PATHS[contractName];
  assert(artifactPath, `Unsupported Morpho contract artifact: ${contractName}`);

  const artifact = readJsonFile(artifactPath);
  const bytecode = typeof artifact?.bytecode === 'string' && artifact.bytecode.startsWith('0x')
    ? artifact.bytecode
    : loadContractArtifactBytecode(artifactPath);
  const normalizedArtifact = { ...artifact, bytecode };
  contractArtifactCache.set(contractName, normalizedArtifact);
  return normalizedArtifact;
}

function loadInput(options) {
  let request;

  if (options.input !== undefined) {
    request = JSON.parse(String(options.input));
  } else if (options.inputFile) {
    request = readJsonFile(resolveExistingUserPath(options.inputFile));
  } else if (!process.stdin.isTTY) {
    try {
      const stdin = fs.readFileSync(0, 'utf8').trim();
      if (stdin) {
        request = JSON.parse(stdin);
      }
    } catch (error) {
      if (error.code !== 'EAGAIN') {
        throw error;
      }
    }
  }

  if (!request) {
    if (options.resumeFromRunDir) {
      const resumeRequestPath = path.join(resolveExistingUserPath(options.resumeFromRunDir), 'request.json');
      if (fs.existsSync(resumeRequestPath)) {
        request = readJsonFile(resumeRequestPath);
      }
    }
  }

  if (!request) {
    throw new Error('Missing request JSON. Pass --input, --input-file, pipe JSON on stdin, or use --resume-from-run-dir with an existing request.json.');
  }

  if (options.deploymentResultFile && request.deploymentResult === undefined) {
    request = {
      ...request,
      deploymentResult: readJsonFile(resolveExistingUserPath(options.deploymentResultFile)),
    };
  }

  return request;
}

function summarizeTransactionPlanForCompactOutput(transactionPlan = []) {
  return (Array.isArray(transactionPlan) ? transactionPlan : []).map((entry) => {
    const compactEntry = {
      transactionId: entry.transactionId,
      kind: entry.kind,
      payloadKind: entry.payloadKind,
      targetContract: entry.targetContract,
      contractFunction: entry.contractFunction,
      contractName: entry.contractName,
      marketKey: entry.marketKey,
      to: entry.to,
      value: entry.value,
      expectedMarketId: entry.expectedMarketId,
      deploymentRef: entry.deploymentRef,
      payloadRef: entry.payloadRef,
      notes: entry.notes,
      sendStatus: entry.sendStatus,
      txHash: entry.txHash,
      blockNumber: entry.blockNumber,
      deployedAddress: entry.deployedAddress,
      error: entry.error,
    };

    if (typeof entry.data === 'string') {
      compactEntry.dataBytes = Math.max(0, (entry.data.length - 2) / 2);
      compactEntry.payloadOmitted = true;
    }

    if (entry.payloadRef) {
      compactEntry.payloadRef = entry.payloadRef;
    }

    if (entry.dataBytes !== undefined) {
      compactEntry.dataBytes = entry.dataBytes;
    }

    if (entry.payloadOmitted !== undefined) {
      compactEntry.payloadOmitted = entry.payloadOmitted;
    }

    return compactEntry;
  });
}

function summarizeAutoOracleResolutionForCompactOutput(autoOracleResolution) {
  if (!autoOracleResolution) {
    return autoOracleResolution;
  }

  return {
    mode: autoOracleResolution.mode,
    signerAddress: autoOracleResolution.signerAddress,
    startingNonce: autoOracleResolution.startingNonce,
    marketKeys: autoOracleResolution.marketKeys,
  };
}

function summarizeMarketsForCompactOutput(markets = []) {
  return (Array.isArray(markets) ? markets : []).map((market) => ({
    marketKey: market.marketKey,
    displayName: market.displayName,
    marketId: market.marketId,
    ready: market.ready,
    oracle: market.oracle,
  }));
}

function summarizeAdaptersForCompactOutput(adapters = []) {
  return (Array.isArray(adapters) ? adapters : []).map((adapter) => ({
    marketKey: adapter.marketKey,
    displayName: adapter.displayName,
    ready: adapter.ready,
    adapterType: adapter.adapterType,
    routeType: adapter.routeType,
    deploymentRef: adapter.deploymentRef,
    contractName: adapter.contractName,
    deployedAddress: adapter.deployedAddress,
  }));
}

function summarizePerfSummaryForCompactOutput(perfSummary) {
  if (!perfSummary) {
    return perfSummary;
  }

  return {
    startedAt: perfSummary.startedAt,
    finishedAt: perfSummary.finishedAt,
    totalElapsedMs: perfSummary.totalElapsedMs,
    aggregates: perfSummary.aggregates,
  };
}

function buildCompactMorphoResult(result) {
  if (!result || typeof result !== 'object') {
    return result;
  }

  if (result.artifactPaths && result.status && result.approvalSummary) {
    return {
      phase: result.phase,
      resumedFromRunDir: result.resumedFromRunDir === true ? true : undefined,
      status: result.status,
      approvalSummary: result.approvalSummary,
      perfSummary: summarizePerfSummaryForCompactOutput(result.perfSummary),
      verifySkippedReason: result.verifySkippedReason,
      blockers: result.blockers,
      warnings: result.warnings,
      nextSteps: result.nextSteps,
      artifactPaths: result.artifactPaths,
      agentDecision: result.agentDecision,
      runDir: result.artifactPaths.runDir,
    };
  }

  if (Array.isArray(result.transactionPlan) && result.sendSummary) {
    return {
      status: result.status,
      ready: result.ready,
      mode: result.mode,
      strategy: result.strategy,
      chain: result.chain,
      morphoCoreAddress: result.morphoCoreAddress,
      marketCount: result.marketCount,
      autoOracleResolution: summarizeAutoOracleResolutionForCompactOutput(result.autoOracleResolution),
      markets: summarizeMarketsForCompactOutput(result.markets),
      adapters: summarizeAdaptersForCompactOutput(result.adapters),
      transactionPlan: summarizeTransactionPlanForCompactOutput(result.transactionPlan),
      sendSummary: result.sendSummary,
      blockers: result.blockers,
      warnings: result.warnings,
      nextSteps: result.nextSteps,
    };
  }

  return result;
}

function outputResult(result, options) {
  const format = String(options.format || 'json').trim().toLowerCase();
  if (format !== 'json') {
    throw new Error(`Unsupported format: ${format}`);
  }

  const outputMode = String(options.outputMode || 'compact').trim().toLowerCase();
  if (!['compact', 'full'].includes(outputMode)) {
    throw new Error(`Unsupported output mode: ${outputMode}`);
  }

  const rendered = outputMode === 'full' ? result : buildCompactMorphoResult(result);
  console.log(JSON.stringify(rendered, null, 2));
}

function printUsage() {
  console.error(`Usage:
  part2-morpho-planner run-workflow --input-file ./request.json
  part2-morpho-planner prepare-morpho-market --input-file ./request.json
  part2-morpho-planner deploy-morpho-oracle-adapter --input-file ./request.json
  part2-morpho-planner deploy-morpho-market --input-file ./request.json --deployment-result-file ./adapter-output.json
  part2-morpho-planner verify-morpho-market --input-file ./verify-request.json --deployment-result-file ./deploy-output.json
  part2-morpho-planner deploy-and-verify-morpho-market --input-file ./request.json --verify-anyway
  part2-morpho-planner ensure-feeds-and-deploy-morpho-market --input-file ./request.json --propagation-wait-ms 30000
  part2-morpho-planner ensure-feeds-and-deploy-morpho-market --resume-from-run-dir ./artifacts/morpho-ensure-deploy/<run>
  part2-morpho-planner preflight-morpho-market --input-file ./request.json
  part2-morpho-planner explain-next --run-dir ./artifacts/morpho-ensure-deploy/<run>
  part2-morpho-planner verify-feed-to-market-handoff --run-dir ./artifacts/morpho-ensure-deploy/<run>

Options:
  --input <json>
  --input-file <path>
  --deployment-result-file <path>
  --run-dir <path>
  --deploy-output-file <path>
  --verify-output-file <path>
  --verify-anyway
  --artifact-label <label>
  --propagation-wait-ms <ms>
  --propagation-poll-ms <ms>
  --progress <human|jsonl|silent>
  --resume-from-run-dir <path>
  --funded-feed-cache-file <path>
  --skip-rpc-check
  --format json
  --output-mode compact|full
  --registry-file <path>
  --feed-status-file <path>`);
}

function validateRpcPreference(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['rpcUrl', 'rpcUrls', 'allowPublicFallback'], label);
  assertStringIfPresent(value.rpcUrl, `${label}.rpcUrl`);
  if (value.rpcUrls !== undefined) {
    assert(Array.isArray(value.rpcUrls), `${label}.rpcUrls must be an array`);
    value.rpcUrls.forEach((entry, index) => assertStringIfPresent(entry, `${label}.rpcUrls[${index}]`));
  }
  assertBooleanIfPresent(value.allowPublicFallback, `${label}.allowPublicFallback`);
}

function validateMorphoPolicy(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['defaultIrmAddress', 'defaultLltv', 'byMarketKey'], label);
  assertHexAddressIfPresent(value.defaultIrmAddress, `${label}.defaultIrmAddress`);
  assertLltvIfPresent(value.defaultLltv, `${label}.defaultLltv`);

  if (value.byMarketKey !== undefined) {
    assertPlainObject(value.byMarketKey, `${label}.byMarketKey`);
    for (const [marketKey, entry] of Object.entries(value.byMarketKey)) {
      assertPlainObject(entry, `${label}.byMarketKey.${marketKey}`);
      assertAllowedKeys(entry, ['irmAddress', 'lltv'], `${label}.byMarketKey.${marketKey}`);
      assertHexAddressIfPresent(entry.irmAddress, `${label}.byMarketKey.${marketKey}.irmAddress`);
      assertLltvIfPresent(entry.lltv, `${label}.byMarketKey.${marketKey}.lltv`);
    }
  }
}

function validateOracleResolution(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['defaultOracleAddress', 'byMarketKey'], label);
  assertHexAddressIfPresent(value.defaultOracleAddress, `${label}.defaultOracleAddress`);

  if (value.byMarketKey !== undefined) {
    assertPlainObject(value.byMarketKey, `${label}.byMarketKey`);
    for (const [marketKey, address] of Object.entries(value.byMarketKey)) {
      assertHexAddressIfPresent(address, `${label}.byMarketKey.${marketKey}`);
    }
  }
}

function validateBroadcastIntent(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'acknowledgement', 'signerAddress'], label);
  assertBooleanIfPresent(value.enabled, `${label}.enabled`);
  assertStringIfPresent(value.acknowledgement, `${label}.acknowledgement`);
  assertHexAddressIfPresent(value.signerAddress, `${label}.signerAddress`);
}

function validateFeedFundingRequest(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['mode', 'executionMode', 'acknowledgement', 'rpcUrl', 'privateKey', 'privateKeyEnv', 'simulationFromAddress', 'deployCommunalProxy'], label);
  if (value.mode !== undefined) {
    normalizeFeedFundingMode(value.mode, `${label}.mode`);
  }
  if (value.executionMode !== undefined) {
    assertEnum(value.executionMode, ['auto', 'direct', 'wrapper'], `${label}.executionMode`);
  }
  assertStringIfPresent(value.acknowledgement, `${label}.acknowledgement`);
  if (value.rpcUrl !== undefined) {
    assert(typeof value.rpcUrl === 'string' && value.rpcUrl.trim(), `${label}.rpcUrl must be a non-empty string`);
  }
  assertPrivateKeyHexIfPresent(value.privateKey, `${label}.privateKey`);
  assertEnvVarNameIfPresent(value.privateKeyEnv, `${label}.privateKeyEnv`);
  assertHexAddressIfPresent(value.simulationFromAddress, `${label}.simulationFromAddress`);
  assertBooleanIfPresent(value.deployCommunalProxy, `${label}.deployCommunalProxy`);
}

function validateSendIntent(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'dryRun', 'rpcUrl', 'privateKey', 'privateKeyEnv'], label);
  assertBooleanIfPresent(value.enabled, `${label}.enabled`);
  assertBooleanIfPresent(value.dryRun, `${label}.dryRun`);
  assertStringIfPresent(value.rpcUrl, `${label}.rpcUrl`);
  assertPrivateKeyHexIfPresent(value.privateKey, `${label}.privateKey`);
  assertEnvVarNameIfPresent(value.privateKeyEnv, `${label}.privateKeyEnv`);
}

function validateDeploymentResult(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(
    value,
    ['status', 'ready', 'mode', 'strategy', 'chain', 'morphoCoreAddress', 'autoOracleResolution', 'marketCount', 'markets', 'adapters', 'transactionPlan', 'sendSummary', 'blockers', 'warnings', 'nextSteps'],
    label,
  );

  if (value.chain !== undefined) {
    assertPlainObject(value.chain, `${label}.chain`);
    assertAllowedKeys(value.chain, ['name', 'chainId'], `${label}.chain`);
    assertStringIfPresent(value.chain.name, `${label}.chain.name`);
    if (value.chain.chainId !== undefined) {
      assert(Number.isInteger(value.chain.chainId) && value.chain.chainId > 0, `${label}.chain.chainId must be a positive integer`);
    }
  }

  if (value.autoOracleResolution !== undefined && value.autoOracleResolution !== null) {
    assertPlainObject(value.autoOracleResolution, `${label}.autoOracleResolution`);
    assertAllowedKeys(
      value.autoOracleResolution,
      ['mode', 'signerAddress', 'startingNonce', 'byMarketKey', 'marketKeys'],
      `${label}.autoOracleResolution`,
    );
    assertStringIfPresent(value.autoOracleResolution.mode, `${label}.autoOracleResolution.mode`);
    assertHexAddressIfPresent(value.autoOracleResolution.signerAddress, `${label}.autoOracleResolution.signerAddress`);
    if (value.autoOracleResolution.startingNonce !== undefined) {
      assert(Number.isInteger(value.autoOracleResolution.startingNonce) && value.autoOracleResolution.startingNonce >= 0, `${label}.autoOracleResolution.startingNonce must be a non-negative integer`);
    }
    if (value.autoOracleResolution.byMarketKey !== undefined) {
      assertPlainObject(value.autoOracleResolution.byMarketKey, `${label}.autoOracleResolution.byMarketKey`);
      for (const [marketKey, address] of Object.entries(value.autoOracleResolution.byMarketKey)) {
        assertHexAddressIfPresent(address, `${label}.autoOracleResolution.byMarketKey.${marketKey}`);
      }
    }
    if (value.autoOracleResolution.marketKeys !== undefined) {
      assert(Array.isArray(value.autoOracleResolution.marketKeys), `${label}.autoOracleResolution.marketKeys must be an array`);
      value.autoOracleResolution.marketKeys.forEach((entry, index) => assertStringIfPresent(entry, `${label}.autoOracleResolution.marketKeys[${index}]`));
    }
  }

  if (value.transactionPlan !== undefined) {
    assert(Array.isArray(value.transactionPlan), `${label}.transactionPlan must be an array`);
    value.transactionPlan.forEach((entry, index) => {
      assertPlainObject(entry, `${label}.transactionPlan[${index}]`);
      assertAllowedKeys(
        entry,
        ['transactionId', 'kind', 'payloadKind', 'targetContract', 'contractFunction', 'contractName', 'marketKey', 'to', 'value', 'data', 'dataBytes', 'payloadOmitted', 'payloadRef', 'expectedMarketId', 'deploymentRef', 'notes', 'sendStatus', 'txHash', 'blockNumber', 'deployedAddress', 'error'],
        `${label}.transactionPlan[${index}]`,
      );
      assertStringIfPresent(entry.transactionId, `${label}.transactionPlan[${index}].transactionId`);
      assertStringIfPresent(entry.kind, `${label}.transactionPlan[${index}].kind`);
      assertStringIfPresent(entry.marketKey, `${label}.transactionPlan[${index}].marketKey`);
      assertHexAddressIfPresent(entry.deployedAddress, `${label}.transactionPlan[${index}].deployedAddress`);
    });
  }

  if (value.adapters !== undefined) {
    assert(Array.isArray(value.adapters), `${label}.adapters must be an array`);
  }
}

function buildPlanMarketValidationRequest(request) {
  return {
    protocol: 'morpho',
    chain: request.chain,
    collateralAssets: request.collateralAssets,
    borrowAssets: request.borrowAssets,
    unitOfAccount: request.unitOfAccount,
    riskPreset: request.riskPreset,
    oraclePreference: request.oraclePreference,
    hookProfile: request.hookProfile,
    ownershipProfile: request.ownershipProfile,
    duplicatePolicy: request.duplicatePolicy,
    discoverExistingMarkets: request.discoverExistingMarkets,
  };
}

function validateRunMorphoWorkflowRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(
    request,
    [
      'protocol',
      'chain',
      'collateralAssets',
      'borrowAssets',
      'unitOfAccount',
      'riskPreset',
      'oraclePreference',
      'hookProfile',
      'ownershipProfile',
      'duplicatePolicy',
      'discoverExistingMarkets',
      'activationMode',
      'executionMode',
      'rpcPreference',
      'marketShapeIntent',
      'morphoPolicy',
      'oracleResolution',
      'morphoCoreAddress',
      'feedFunding',
      'broadcast',
      'send',
      'deploymentResult',
    ],
    'request'
  );

  if (request.protocol !== undefined) {
    assert(request.protocol === 'morpho', 'request.protocol must be morpho when using the Morpho planner');
  }

  validatePlanMarketRequest(buildPlanMarketValidationRequest(request));

  if (request.activationMode !== undefined) {
    assertEnum(request.activationMode, ['check-only', 'prepare-only', 'allow-activation'], 'request.activationMode');
  }
  if (request.executionMode !== undefined) {
    assertEnum(request.executionMode, ['planning-only', 'dry-run', 'live'], 'request.executionMode');
  }
  if (request.marketShapeIntent !== undefined) {
    assertEnum(request.marketShapeIntent, ['single-market', 'market-set'], 'request.marketShapeIntent');
  }

  validateRpcPreference(request.rpcPreference, 'request.rpcPreference');
  validateMorphoPolicy(request.morphoPolicy, 'request.morphoPolicy');
  validateOracleResolution(request.oracleResolution, 'request.oracleResolution');
  assertHexAddressIfPresent(request.morphoCoreAddress, 'request.morphoCoreAddress');
  validateFeedFundingRequest(request.feedFunding, 'request.feedFunding');
  validateBroadcastIntent(request.broadcast, 'request.broadcast');
  validateSendIntent(request.send, 'request.send');
  validateDeploymentResult(request.deploymentResult, 'request.deploymentResult');
}

function validatePrepareMorphoMarketRequest(request) {
  validateRunMorphoWorkflowRequest(request);
}

function validateDeployMorphoMarketRequest(request) {
  validateRunMorphoWorkflowRequest(request);
}

function validateVerifyMorphoMarketRequest(request) {
  validateRunMorphoWorkflowRequest(request);
}

function makeCanonicalHash(payload) {
  return `sha256:${crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex')}`;
}

function uniqueStrings(values) {
  return values.filter((value, index, array) => value && array.indexOf(value) === index);
}

function sanitizeMarketKeySegment(value) {
  return String(value || '')
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
}

function makeFeedRequirement(baseAsset, quoteAsset, routeRole) {
  return {
    feedName: `${baseAsset.symbol}/${quoteAsset.symbol}`,
    base: {
      symbol: baseAsset.symbol,
      ...(baseAsset.address ? { address: baseAsset.address } : {}),
      role: routeRole === 'borrow-leg' ? 'borrow' : 'collateral',
    },
    quote: {
      symbol: quoteAsset.symbol,
      ...(quoteAsset.address ? { address: quoteAsset.address } : {}),
      role: 'unit-of-account',
    },
    maxStalenessSeconds: 86400,
    compatibilityPreference: 'native-api3-ok',
    routeRole,
  };
}

function buildCompositeRequiredFeeds(normalizedIntent) {
  const quoteAsset = { symbol: normalizedIntent.unitOfAccount, role: 'unit-of-account' };
  const collateralLegs = normalizedIntent.collateralAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'collateral-leg'));
  const borrowLegs = normalizedIntent.borrowAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'borrow-leg'));
  return [...collateralLegs, ...borrowLegs].sort((left, right) => left.feedName.localeCompare(right.feedName));
}

function normalizeMorphoWorkflowRequest(request) {
  const normalizedIntent = normalizeIntent(buildPlanMarketValidationRequest(request));

  return {
    ...normalizedIntent,
    executionMode: request.executionMode || DEFAULT_EXECUTION_MODE,
    marketShapeIntent: request.marketShapeIntent || DEFAULT_MARKET_SHAPE_INTENT,
    canonicalHash: makeCanonicalHash({
      protocol: normalizedIntent.protocol,
      chainId: normalizedIntent.chain.chainId,
      collateralAssets: normalizedIntent.collateralAssets,
      borrowAssets: normalizedIntent.borrowAssets,
      unitOfAccount: normalizedIntent.unitOfAccount,
      riskPreset: normalizedIntent.riskPreset,
      executionMode: request.executionMode || DEFAULT_EXECUTION_MODE,
      marketShapeIntent: request.marketShapeIntent || DEFAULT_MARKET_SHAPE_INTENT,
    }),
  };
}

function sanitizeDiscoveryResult(discovery) {
  const reasoning = Array.isArray(discovery.reasoning)
    ? discovery.reasoning.filter((entry) => entry !== SHARED_EVK_ONLY_WARNING)
    : [];

  let recommendedAction = discovery.recommendedAction;
  const hasMatches = (Array.isArray(discovery.exactMatches) && discovery.exactMatches.length > 0)
    || (Array.isArray(discovery.nearEquivalentMatches) && discovery.nearEquivalentMatches.length > 0);

  if (!hasMatches && recommendedAction === 'manual-review') {
    recommendedAction = 'deploy-new-market';
  }

  return {
    exactMatches: Array.isArray(discovery.exactMatches) ? discovery.exactMatches : [],
    nearEquivalentMatches: Array.isArray(discovery.nearEquivalentMatches) ? discovery.nearEquivalentMatches : [],
    recommendedAction,
    reasoning,
  };
}

function assessMorphoMarketShape(normalizedIntent) {
  const marketCount = normalizedIntent.collateralAssets.length * normalizedIntent.borrowAssets.length;
  const mode = marketCount === 1 ? 'single-market' : 'market-set';
  const warnings = mode === 'market-set'
    ? [`Morpho supports one collateral asset and one loan asset per market, so this request expands into ${marketCount} separate Morpho markets.`]
    : [];

  return {
    supported: normalizedIntent.collateralAssets.length >= 1 && normalizedIntent.borrowAssets.length >= 1,
    mode,
    strategy: DEFAULT_MARKET_SET_STRATEGY,
    collateralAssetCount: normalizedIntent.collateralAssets.length,
    borrowAssetCount: normalizedIntent.borrowAssets.length,
    marketCount,
    blockers: [],
    warnings,
  };
}

function buildMorphoMarketEntries(normalizedIntent) {
  const entries = [];

  for (const collateralAsset of normalizedIntent.collateralAssets) {
    for (const borrowAsset of normalizedIntent.borrowAssets) {
      const marketKey = `${sanitizeMarketKeySegment(collateralAsset.symbol)}__${sanitizeMarketKeySegment(borrowAsset.symbol)}`;
      const entryIntent = {
        ...normalizedIntent,
        collateralAssets: [collateralAsset],
        borrowAssets: [borrowAsset],
        marketKey,
        canonicalHash: makeCanonicalHash({
          protocol: normalizedIntent.protocol,
          chainId: normalizedIntent.chain.chainId,
          collateralAsset,
          borrowAsset,
          unitOfAccount: normalizedIntent.unitOfAccount,
          riskPreset: normalizedIntent.riskPreset,
        }),
      };

      entries.push({
        marketKey,
        displayName: `${normalizedIntent.chain.name} ${collateralAsset.symbol}/${borrowAsset.symbol} Morpho market`,
        normalizedIntent: entryIntent,
        collateralAsset,
        borrowAsset,
      });
    }
  }

  return entries;
}

function shouldEvaluateCompositePath(entry) {
  return entry.normalizedIntent.borrowAssets[0].symbol !== entry.normalizedIntent.unitOfAccount;
}

function deriveFeedReadinessState(ensureResult) {
  const feeds = Array.isArray(ensureResult?.feeds) ? ensureResult.feeds : [];
  if (feeds.length > 0 && feeds.every((feed) => feed.status === 'ready')) {
    return 'ready';
  }
  if (feeds.some((feed) => feed.status === 'activatable')) {
    return 'activation-needed';
  }
  if (feeds.some((feed) => feed.status === 'ready')) {
    return 'partially-ready';
  }
  if (feeds.some((feed) => feed.status === 'blocked')) {
    return 'blocked';
  }
  return 'unknown';
}

function summarizeFeedStatuses(feeds) {
  return feeds.reduce((summary, feed) => {
    const key = String(feed.status || 'unknown');
    summary[key] = (summary[key] || 0) + 1;
    return summary;
  }, {});
}

function makeCandidatePath({ pathId, label, routeType, requiredFeeds, ensureResult }) {
  const feeds = Array.isArray(ensureResult?.feeds) ? ensureResult.feeds : [];
  const blockers = uniqueStrings([...(ensureResult?.blockers || [])]);
  const warnings = uniqueStrings([...(ensureResult?.warnings || [])]);

  return {
    pathId,
    label,
    routeType,
    ready: feeds.length > 0 && feeds.every((feed) => feed.status === 'ready'),
    feedReadinessState: deriveFeedReadinessState(ensureResult),
    requiredFeeds,
    ensureFeeds: ensureResult,
    readyFeedCount: feeds.filter((feed) => feed.status === 'ready').length,
    activatableFeedCount: feeds.filter((feed) => feed.status === 'activatable').length,
    blockedFeedCount: feeds.filter((feed) => feed.status === 'blocked').length,
    statusSummary: summarizeFeedStatuses(feeds),
    blockers,
    warnings,
  };
}

function rankCandidatePath(candidate) {
  const readinessScoreByState = {
    ready: 4,
    'partially-ready': 3,
    'activation-needed': 2,
    blocked: 1,
    unknown: 0,
  };

  return {
    readinessScore: readinessScoreByState[candidate.feedReadinessState] || 0,
    readyFeedCount: candidate.readyFeedCount,
    blockedFeedPenalty: candidate.blockedFeedCount,
    feedCountPenalty: candidate.requiredFeeds.length,
    directBias: candidate.routeType === 'direct' ? 1 : 0,
  };
}

function compareCandidatePaths(left, right) {
  const leftRank = rankCandidatePath(left);
  const rightRank = rankCandidatePath(right);

  return rightRank.readinessScore - leftRank.readinessScore
    || rightRank.directBias - leftRank.directBias
    || rightRank.readyFeedCount - leftRank.readyFeedCount
    || leftRank.blockedFeedPenalty - rightRank.blockedFeedPenalty
    || leftRank.feedCountPenalty - rightRank.feedCountPenalty;
}

function chooseRecommendedPath(candidates) {
  if (candidates.length === 0) {
    return null;
  }

  return [...candidates].sort(compareCandidatePaths)[0];
}

function buildFeedFundingOptions(request, feedName) {
  const feedFunding = request.feedFunding || {};
  const rpcUrl = feedFunding.rpcUrl
    || (request.rpcPreference && request.rpcPreference.rpcUrl)
    || (request.rpcPreference && Array.isArray(request.rpcPreference.rpcUrls)
      ? request.rpcPreference.rpcUrls.find((entry) => typeof entry === 'string' && entry.trim())
      : undefined);
  const mode = getFeedFundingMode(request);
  const simulationFromAddress = feedFunding.simulationFromAddress
    || (mode === 'dry-run' ? DEFAULT_DRY_RUN_SIMULATION_FROM_ADDRESS : undefined);
  const deployCommunalProxy = feedFunding.deployCommunalProxy !== false;

  return {
    chain: request.chain.name || String(request.chain.chainId),
    dapiName: feedName,
    ...(rpcUrl ? { rpcUrl } : {}),
    ...(feedFunding.privateKey ? { privateKey: normalizePrivateKeyHex(feedFunding.privateKey, 'request.feedFunding.privateKey') } : {}),
    ...(feedFunding.privateKeyEnv ? { privateKeyEnv: feedFunding.privateKeyEnv } : {}),
    ...(feedFunding.acknowledgement ? { acknowledgement: feedFunding.acknowledgement } : {}),
    ...(feedFunding.executionMode ? { executionMode: feedFunding.executionMode } : {}),
    ...(simulationFromAddress ? { simulationFromAddress } : {}),
    deployCommunalProxy,
  };
}

function summarizeFundingState(entries) {
  const states = uniqueStrings(entries.map((entry) => entry.fundingExecutionState).filter(Boolean));
  if (states.length === 0) {
    return null;
  }
  if (states.length === 1) {
    return states[0];
  }
  if (states.every((state) => state === 'not-needed' || state === 'executable')) {
    return 'executable';
  }
  return 'mixed';
}

function promoteCandidatePathFromFunding(candidate, feedFundingResult, reason) {
  if (!candidate || !feedFundingResult || !Array.isArray(feedFundingResult.entries)) {
    return candidate;
  }

  const fundingByFeedName = new Map(
    feedFundingResult.entries
      .filter((entry) => entry && typeof entry.feedName === 'string')
      .map((entry) => [entry.feedName, entry]),
  );

  let promotedAny = false;
  const promotedFeeds = candidate.ensureFeeds.feeds.map((feed) => {
    if (!feed || feed.status === 'ready') {
      return feed;
    }

    const fundingEntry = fundingByFeedName.get(feed.feedName);
    if (!fundingEntry) {
      return feed;
    }

    const executionCompleted = fundingEntry.execution && fundingEntry.execution.executionSummary
      ? fundingEntry.execution.executionSummary.completed === true
      : false;
    if (fundingEntry.fundingExecutionState !== 'not-needed' && !executionCompleted) {
      return feed;
    }

    promotedAny = true;
    return {
      ...feed,
      status: 'ready',
      blockers: [],
    };
  });

  if (!promotedAny || promotedFeeds.some((feed) => !feed || feed.status !== 'ready')) {
    return candidate;
  }

  const promotedEnsure = {
    ...candidate.ensureFeeds,
    ready: true,
    blockers: [],
    warnings: uniqueStrings([
      ...(candidate.ensureFeeds.warnings || []),
      reason,
    ]),
    feeds: promotedFeeds,
  };

  return makeCandidatePath({
    pathId: candidate.pathId,
    label: candidate.label,
    routeType: candidate.routeType,
    requiredFeeds: candidate.requiredFeeds,
    ensureResult: promotedEnsure,
  });
}

function resolveFundedFeedCacheFilePath(options = {}) {
  return options.fundedFeedCacheFile
    ? path.resolve(ROOT_DIR, String(options.fundedFeedCacheFile))
    : null;
}

function isFundedFeedCacheChainCompatible(request, cache) {
  if (!cache || !cache.chain || !request?.chain) {
    return true;
  }

  if (cache.chain.chainId !== undefined && request.chain.chainId !== undefined) {
    return String(cache.chain.chainId) === String(request.chain.chainId);
  }

  if (cache.chain.name !== undefined && request.chain.name !== undefined) {
    return String(cache.chain.name).trim().toLowerCase() === String(request.chain.name).trim().toLowerCase();
  }

  return true;
}

function loadReusableFundedFeedCache(request, options = {}) {
  if (options.ignoreFundedFeedCache) {
    return null;
  }

  const cachePath = resolveFundedFeedCacheFilePath(options);
  if (!cachePath) {
    return null;
  }

  const cache = readJsonFile(cachePath);
  if (!cache || cache.version !== 1 || !cache.entriesByKey || typeof cache.entriesByKey !== 'object' || Array.isArray(cache.entriesByKey)) {
    return null;
  }

  if (!isFundedFeedCacheChainCompatible(request, cache)) {
    return null;
  }

  return {
    path: cachePath,
    generatedAt: cache.generatedAt || null,
    entriesByKey: cache.entriesByKey,
  };
}

function getCachedFundedFeedEntry(request, feedName, fundedFeedCache) {
  if (!fundedFeedCache) {
    return null;
  }

  const entry = fundedFeedCache.entriesByKey[makeFundedFeedCacheKey(request, feedName)];
  return entry && typeof entry === 'object' ? entry : null;
}

async function analyzeFundingForCandidate(candidate, request, options = {}) {
  const modeRequested = getFeedFundingMode(request);
  const feedFunding = {
    modeRequested,
    attemptedExecution: false,
    overallState: candidate && candidate.ready ? 'not-needed' : null,
    entries: [],
  };

  if (!candidate || candidate.ready) {
    return {
      candidate,
      feedFunding,
    };
  }

  const fundedFeedCache = loadReusableFundedFeedCache(request, options);
  const feedsNeedingFunding = candidate.ensureFeeds.feeds.filter((feed) => feed.status !== 'ready');
  for (const feed of feedsNeedingFunding) {
    const fundingOptions = buildFeedFundingOptions(request, feed.feedName);
    const entry = {
      feedName: feed.feedName,
      statusBefore: feed.status,
      fundingExecutionState: null,
      availableExecutionModes: [],
      selectedExecutionMode: null,
      purchaseInputs: null,
      browserPlan: null,
      execution: null,
      blockers: [],
      warnings: [],
    };

    const cachedFeed = getCachedFundedFeedEntry(request, feed.feedName, fundedFeedCache);
    if (cachedFeed) {
      entry.fundingExecutionState = 'executable';
      entry.selectedExecutionMode = cachedFeed.selectedExecutionMode || null;
      entry.cacheHit = true;
      entry.sourceCache = {
        path: fundedFeedCache.path,
        generatedAt: fundedFeedCache.generatedAt,
      };
      entry.execution = {
        fundingExecutionClassification: {
          state: 'executable',
          reason: 'Feed was found in the reusable funded-feed cache; skipping funding classification/execution and rechecking live propagation.',
        },
        selectedExecutionMode: entry.selectedExecutionMode,
        executionSummary: {
          completed: true,
          reusedFromFundedFeedCache: true,
        },
      };
      entry.warnings.push(`Reused funded-feed cache entry for ${feed.feedName}; skipping funding execution and waiting for live propagation.`);
      feedFunding.entries.push(entry);
      continue;
    }

    try {
      const purchasePlan = await purchaseInputs(fundingOptions);
      entry.purchaseInputs = purchasePlan;
      entry.fundingExecutionState = purchasePlan.fundingExecutionClassification
        ? purchasePlan.fundingExecutionClassification.state || null
        : null;
      entry.availableExecutionModes = Array.isArray(purchasePlan.fundingExecutionClassification?.availableExecutionModes)
        ? [...purchasePlan.fundingExecutionClassification.availableExecutionModes]
        : [];

      if (entry.fundingExecutionState === 'browser-assisted') {
        try {
          entry.browserPlan = await browserPlan(fundingOptions);
        } catch (error) {
          entry.blockers.push(`browser-plan failed for ${feed.feedName}: ${error.message}`);
        }
      }

      if (entry.fundingExecutionState === 'executable' && modeRequested !== 'classify-only') {
        feedFunding.attemptedExecution = true;
        entry.execution = await executeBuySubscription({
          ...fundingOptions,
          submit: modeRequested === 'real-send',
        });
        entry.fundingExecutionState = entry.execution.fundingExecutionClassification
          ? entry.execution.fundingExecutionClassification.state || entry.fundingExecutionState
          : entry.fundingExecutionState;
        entry.availableExecutionModes = Array.isArray(entry.execution.availableExecutionModes)
          ? [...entry.execution.availableExecutionModes]
          : entry.availableExecutionModes;
        entry.selectedExecutionMode = entry.execution.selectedExecutionMode || null;

        if (entry.execution.executionSummary && entry.execution.executionSummary.failureReason) {
          entry.blockers.push(entry.execution.executionSummary.failureReason);
        }
        if (entry.execution.communalProxyDeployment?.executionSummary?.failureReason) {
          entry.blockers.push(`communal proxy deployment failed for ${feed.feedName}: ${entry.execution.communalProxyDeployment.executionSummary.failureReason}`);
        }
      }
    } catch (error) {
      entry.blockers.push(`purchase-inputs failed for ${feed.feedName}: ${error.message}`);
    }

    feedFunding.entries.push(entry);
  }

  feedFunding.overallState = summarizeFundingState(feedFunding.entries);

  let finalCandidate = candidate;
  const completedFunding = feedFunding.entries.some((entry) => entry.execution && entry.execution.executionSummary?.completed === true);
  if (completedFunding) {
    finalCandidate = promoteCandidatePathFromFunding(
      candidate,
      feedFunding,
      'Promoted feeds to ready for Morpho planning after completed funding execution; rerun live verification if propagation lags.',
    );
  }

  return {
    candidate: finalCandidate,
    feedFunding,
  };
}

function buildDirectAdapterPlan(candidate, marketKey) {
  const feedArtifact = candidate.ensureFeeds.feeds[0] || null;
  const feedRequirement = candidate.requiredFeeds[0] || null;
  const blockers = [];

  if (!candidate.ready) {
    blockers.push('Direct Morpho adapter planning is blocked until the exact collateral/loan Api3 feed is ready.');
  }
  if (!feedArtifact) {
    blockers.push('Direct Morpho adapter planning could not resolve the required feed artifact.');
  }

  return {
    ready: blockers.length === 0,
    adapterType: 'MorphoApi3DirectOracle',
    routeType: 'direct',
    deploymentRef: `morpho-oracle:${marketKey}:direct`,
    feedBindings: feedArtifact
      ? [
          {
            role: 'direct',
            feedName: feedArtifact.feedName,
            proxyAddress: feedArtifact.proxyAddress,
            latestRead: feedArtifact.latestRead,
            proxyHasCode: feedArtifact.proxyHasCode,
            proxyDeploymentPlan: feedArtifact.proxyDeploymentPlan,
          },
        ]
      : [],
    constructorArgs: blockers.length === 0
      ? {
          api3Proxy: feedArtifact.proxyAddress,
          maxStaleness: feedRequirement.maxStalenessSeconds || 86400,
          invert: false,
        }
      : null,
    priceModel: {
      orientation: 'collateral-priced-in-loan-asset',
      morphoScale: '1e36',
      formula: 'api3Price * 1e18',
      expectedPair: feedRequirement ? feedRequirement.feedName : null,
    },
    blockers,
    warnings: candidate.warnings,
  };
}

function buildCompositeAdapterPlan(candidate, marketKey) {
  const collateralRequirement = candidate.requiredFeeds.find((feed) => feed.routeRole === 'collateral-leg') || null;
  const borrowRequirement = candidate.requiredFeeds.find((feed) => feed.routeRole === 'borrow-leg') || null;
  const collateralFeed = candidate.ensureFeeds.feeds.find(
    (feed) => canonicalizeMorphoFeedName(feed.feedName) === canonicalizeMorphoFeedName(collateralRequirement?.feedName),
  ) || null;
  const borrowFeed = candidate.ensureFeeds.feeds.find(
    (feed) => canonicalizeMorphoFeedName(feed.feedName) === canonicalizeMorphoFeedName(borrowRequirement?.feedName),
  ) || null;
  const blockers = [];

  if (!candidate.ready) {
    blockers.push('Composite Morpho adapter planning is blocked until both collateral/USD and loan/USD Api3 feeds are ready.');
  }
  if (!collateralFeed || !borrowFeed) {
    blockers.push('Composite Morpho adapter planning could not resolve both required feed artifacts.');
  }

  return {
    ready: blockers.length === 0,
    adapterType: 'MorphoApi3CompositeOracle',
    routeType: 'composite',
    deploymentRef: `morpho-oracle:${marketKey}:composite`,
    feedBindings: [collateralFeed, borrowFeed]
      .filter(Boolean)
      .map((feed) => ({
        role: canonicalizeMorphoFeedName(feed.feedName) === canonicalizeMorphoFeedName(collateralRequirement?.feedName) ? 'collateral-usd' : 'loan-usd',
        feedName: feed.feedName,
        proxyAddress: feed.proxyAddress,
        latestRead: feed.latestRead,
        proxyHasCode: feed.proxyHasCode,
        proxyDeploymentPlan: feed.proxyDeploymentPlan,
      })),
    constructorArgs: blockers.length === 0
      ? {
          collateralUsdProxy: collateralFeed.proxyAddress,
          loanUsdProxy: borrowFeed.proxyAddress,
          maxStaleness: Math.max(
            collateralRequirement?.maxStalenessSeconds || 86400,
            borrowRequirement?.maxStalenessSeconds || 86400,
          ),
          collateralUsdNeedsInversion: false,
          loanUsdNeedsInversion: false,
        }
      : null,
    priceModel: {
      orientation: 'collateral-priced-in-loan-asset',
      morphoScale: '1e36',
      formula: 'collateralUsdPrice * 1e36 / loanUsdPrice',
      expectedPairs: [collateralRequirement?.feedName || null, borrowRequirement?.feedName || null].filter(Boolean),
    },
    blockers,
    warnings: candidate.warnings,
  };
}

function buildMorphoOracleAdapterPlan(candidate, marketKey) {
  if (!candidate) {
    return {
      ready: false,
      adapterType: null,
      routeType: null,
      deploymentRef: `morpho-oracle:${marketKey}:unresolved`,
      feedBindings: [],
      constructorArgs: null,
      priceModel: null,
      blockers: ['No Morpho oracle route candidate was available.'],
      warnings: [],
    };
  }

  if (candidate.routeType === 'direct') {
    return buildDirectAdapterPlan(candidate, marketKey);
  }

  return buildCompositeAdapterPlan(candidate, marketKey);
}

function getMorphoAdapterConstructorArgs(oracleAdapterPlan) {
  assert(oracleAdapterPlan && oracleAdapterPlan.adapterType, 'oracleAdapterPlan.adapterType is required');

  if (oracleAdapterPlan.adapterType === 'MorphoApi3DirectOracle') {
    return [
      oracleAdapterPlan.constructorArgs.api3Proxy,
      oracleAdapterPlan.constructorArgs.maxStaleness,
      oracleAdapterPlan.constructorArgs.invert,
    ];
  }

  if (oracleAdapterPlan.adapterType === 'MorphoApi3CompositeOracle') {
    return [
      oracleAdapterPlan.constructorArgs.collateralUsdProxy,
      oracleAdapterPlan.constructorArgs.loanUsdProxy,
      oracleAdapterPlan.constructorArgs.maxStaleness,
      oracleAdapterPlan.constructorArgs.collateralUsdNeedsInversion,
      oracleAdapterPlan.constructorArgs.loanUsdNeedsInversion,
    ];
  }

  throw new Error(`Unsupported Morpho adapter type: ${oracleAdapterPlan.adapterType}`);
}

function buildMorphoAdapterDeploymentData(oracleAdapterPlan) {
  const artifact = loadContractArtifact(oracleAdapterPlan.adapterType);
  const contractInterface = new Interface(artifact.abi);
  const constructorArgs = getMorphoAdapterConstructorArgs(oracleAdapterPlan);
  const deployData = contractInterface.encodeDeploy(constructorArgs);

  return {
    contractName: artifact.contractName,
    constructorArgs,
    bytecode: artifact.bytecode,
    abi: artifact.abi,
    data: `${artifact.bytecode}${deployData.slice(2)}`,
  };
}

function resolveMorphoPolicy(request, marketKey, riskPreset) {
  const policy = request.morphoPolicy || {};
  const byMarketKey = policy.byMarketKey || {};
  const specific = byMarketKey[marketKey] || {};
  const defaultLltv = policy.defaultLltv || RISK_PRESET_LLTV_DEFAULTS[riskPreset] || null;
  const resolved = {
    irmAddress: specific.irmAddress || policy.defaultIrmAddress || null,
    lltv: specific.lltv || defaultLltv || null,
  };

  const blockers = [];
  const warnings = [];

  if (!resolved.irmAddress) {
    blockers.push(`No approved Morpho IRM is configured for ${marketKey}. Supply request.morphoPolicy.defaultIrmAddress or request.morphoPolicy.byMarketKey.${marketKey}.irmAddress.`);
  }
  if (!resolved.lltv) {
    blockers.push(`No approved Morpho LLTV is configured for ${marketKey}. Supply request.morphoPolicy.defaultLltv or request.morphoPolicy.byMarketKey.${marketKey}.lltv.`);
  }
  if (!policy.defaultLltv && !specific.lltv && RISK_PRESET_LLTV_DEFAULTS[riskPreset]) {
    warnings.push(`Using built-in LLTV default ${RISK_PRESET_LLTV_DEFAULTS[riskPreset]} for riskPreset=${riskPreset}. Confirm this matches the intended Morpho policy before deployment.`);
  }

  return {
    ready: blockers.length === 0,
    resolved,
    blockers,
    warnings,
  };
}

function resolveOracleTarget(request, marketKey, oracleAdapterPlan) {
  const oracleResolution = request.oracleResolution || {};
  const concreteAddress = (oracleResolution.byMarketKey && oracleResolution.byMarketKey[marketKey])
    || oracleResolution.defaultOracleAddress
    || null;

  if (concreteAddress) {
    return {
      ready: true,
      address: concreteAddress,
      source: 'request',
      deploymentRef: oracleAdapterPlan.deploymentRef,
      blockers: [],
      warnings: [],
    };
  }

  const blockers = [];
  if (!oracleAdapterPlan.ready) {
    blockers.push(`Oracle adapter planning is not ready for ${marketKey}.`);
  } else {
    blockers.push(`No concrete oracle address is configured for ${marketKey}. Deploy the planned adapter first or supply request.oracleResolution.byMarketKey.${marketKey}.`);
  }

  return {
    ready: false,
    address: null,
    source: 'deployment-ref',
    deploymentRef: oracleAdapterPlan.deploymentRef,
    blockers,
    warnings: [],
  };
}

function computeMorphoMarketId(marketParams) {
  const encoded = ABI_CODER.encode(
    ['address', 'address', 'address', 'address', 'uint256'],
    [
      marketParams.loanToken,
      marketParams.collateralToken,
      marketParams.oracle,
      marketParams.irm,
      BigInt(marketParams.lltv),
    ],
  );

  return keccak256(encoded);
}

function prepareMorphoMarketFromEntry(entry, request, oracleAdapterPlan) {
  const marketKey = entry.marketKey;
  const policy = resolveMorphoPolicy(request, marketKey, entry.normalizedIntent.riskPreset);
  const oracleTarget = resolveOracleTarget(request, marketKey, oracleAdapterPlan);
  const blockers = [];
  const warnings = [];

  const collateralToken = entry.collateralAsset.address || null;
  const loanToken = entry.borrowAsset.address || null;

  if (!collateralToken) {
    blockers.push(`Collateral token address is missing for ${marketKey}.`);
  }
  if (!loanToken) {
    blockers.push(`Loan token address is missing for ${marketKey}.`);
  }

  blockers.push(...policy.blockers, ...oracleTarget.blockers);
  warnings.push(...policy.warnings, ...oracleTarget.warnings);

  const marketParams = {
    loanToken: loanToken || ZERO_ADDRESS,
    collateralToken: collateralToken || ZERO_ADDRESS,
    oracle: oracleTarget.address || ZERO_ADDRESS,
    irm: policy.resolved.irmAddress || ZERO_ADDRESS,
    lltv: policy.resolved.lltv || '0',
  };

  const ready = blockers.length === 0;
  const marketId = ready ? computeMorphoMarketId(marketParams) : null;

  return {
    marketKey,
    displayName: entry.displayName,
    ready,
    policy: {
      riskPreset: entry.normalizedIntent.riskPreset,
      irmAddress: policy.resolved.irmAddress,
      lltv: policy.resolved.lltv,
    },
    oracle: {
      address: oracleTarget.address,
      deploymentRef: oracleTarget.deploymentRef,
      routeType: oracleAdapterPlan.routeType,
      adapterType: oracleAdapterPlan.adapterType,
    },
    marketParams,
    marketId,
    blockers: uniqueStrings(blockers),
    warnings: uniqueStrings(warnings),
  };
}

async function analyzeMorphoMarketEntry(entry, request, options) {
  const discovery = sanitizeDiscoveryResult(discoverMarkets({
    protocol: 'morpho',
    chain: request.chain,
    collateralAssets: [entry.collateralAsset],
    borrowAssets: [entry.borrowAsset],
    riskPreset: request.riskPreset,
    includeNearEquivalent: true,
  }, options));

  const directRequiredFeeds = buildRequiredFeeds({
    collateralAssets: [entry.collateralAsset],
    borrowAssets: [entry.borrowAsset],
    unitOfAccount: entry.normalizedIntent.unitOfAccount,
  });
  const directEnsure = await measureMorphoPerf(options, 'ensureFeeds', {
    routeType: 'direct',
    marketKey: entry.marketKey,
    feedCount: directRequiredFeeds.length,
  }, () => ensureFeeds({
    chain: request.chain,
    requiredFeeds: directRequiredFeeds,
    activationMode: request.activationMode || DEFAULT_ACTIVATION_MODE,
    requireChainlinkCompatibility: false,
    rpcPreference: request.rpcPreference,
  }, options));

  const candidatePaths = [
    makeCandidatePath({
      pathId: 'direct-exact-pair',
      label: 'Direct collateral/loan Api3 pair',
      routeType: 'direct',
      requiredFeeds: directRequiredFeeds,
      ensureResult: directEnsure,
    }),
  ];

  if (shouldEvaluateCompositePath(entry)) {
    const compositeRequiredFeeds = buildCompositeRequiredFeeds(entry.normalizedIntent);
    const compositeEnsure = await measureMorphoPerf(options, 'ensureFeeds', {
      routeType: 'composite',
      marketKey: entry.marketKey,
      feedCount: compositeRequiredFeeds.length,
    }, () => ensureFeeds({
      chain: request.chain,
      requiredFeeds: compositeRequiredFeeds,
      activationMode: request.activationMode || DEFAULT_ACTIVATION_MODE,
      requireChainlinkCompatibility: false,
      rpcPreference: request.rpcPreference,
    }, options));

    candidatePaths.push(makeCandidatePath({
      pathId: 'composite-usd-route',
      label: `Composite ${entry.normalizedIntent.unitOfAccount} route`,
      routeType: 'composite',
      requiredFeeds: compositeRequiredFeeds,
      ensureResult: compositeEnsure,
    }));
  }

  const initialRecommendedPath = chooseRecommendedPath(candidatePaths);
  const fundingResult = await analyzeFundingForCandidate(initialRecommendedPath, request, options);
  const recommendedPath = fundingResult.candidate;
  const oracleAdapterPlan = buildMorphoOracleAdapterPlan(recommendedPath, entry.marketKey);
  const preparation = prepareMorphoMarketFromEntry(entry, request, oracleAdapterPlan);

  return {
    marketKey: entry.marketKey,
    displayName: entry.displayName,
    normalizedIntent: entry.normalizedIntent,
    existingMarkets: discovery,
    feedReadiness: {
      recommendedPathId: recommendedPath ? recommendedPath.pathId : null,
      candidatePaths,
    },
    feedFunding: fundingResult.feedFunding,
    oracleAdapterPlan,
    prepareMorphoMarket: preparation,
    blockers: uniqueStrings([
      ...(recommendedPath ? recommendedPath.blockers : []),
      ...fundingResult.feedFunding.entries.flatMap((fundingEntry) => fundingEntry.blockers || []),
      ...oracleAdapterPlan.blockers,
      ...preparation.blockers,
    ]),
    warnings: uniqueStrings([
      ...candidatePaths.flatMap((candidate) => candidate.warnings || []),
      ...fundingResult.feedFunding.entries.flatMap((fundingEntry) => fundingEntry.warnings || []),
      ...oracleAdapterPlan.warnings,
      ...preparation.warnings,
    ]),
  };
}

function buildPrepareMorphoMarketSummary(markets, marketShape) {
  const preparedMarkets = markets.map((market) => market.prepareMorphoMarket);
  const readyCount = preparedMarkets.filter((market) => market.ready).length;

  return {
    ready: preparedMarkets.length > 0 && preparedMarkets.every((market) => market.ready),
    mode: marketShape.mode,
    strategy: marketShape.strategy,
    marketCount: preparedMarkets.length,
    readyMarketCount: readyCount,
    blockedMarketCount: preparedMarkets.length - readyCount,
    markets: preparedMarkets,
    blockers: uniqueStrings(preparedMarkets.flatMap((market) => market.blockers || [])),
    warnings: uniqueStrings(preparedMarkets.flatMap((market) => market.warnings || [])),
  };
}

function buildPrepareMorphoOracleAdapterSummary(markets, marketShape) {
  const adapters = markets.map((market) => {
    const deployment = market.oracleAdapterPlan.ready
      ? buildMorphoAdapterDeploymentData(market.oracleAdapterPlan)
      : null;

    return {
      marketKey: market.marketKey,
      displayName: market.displayName,
      ready: market.oracleAdapterPlan.ready,
      adapterType: market.oracleAdapterPlan.adapterType,
      routeType: market.oracleAdapterPlan.routeType,
      deploymentRef: market.oracleAdapterPlan.deploymentRef,
      feedBindings: market.oracleAdapterPlan.feedBindings,
      constructorArgs: market.oracleAdapterPlan.constructorArgs,
      deployment,
      blockers: [...(market.oracleAdapterPlan.blockers || [])],
      warnings: [...(market.oracleAdapterPlan.warnings || [])],
    };
  });

  const readyCount = adapters.filter((adapter) => adapter.ready).length;
  return {
    ready: adapters.length > 0 && adapters.every((adapter) => adapter.ready),
    mode: marketShape.mode,
    strategy: marketShape.strategy,
    marketCount: adapters.length,
    readyMarketCount: readyCount,
    blockedMarketCount: adapters.length - readyCount,
    adapters,
    blockers: uniqueStrings(adapters.flatMap((adapter) => adapter.blockers || [])),
    warnings: uniqueStrings(adapters.flatMap((adapter) => adapter.warnings || [])),
  };
}

function summarizeExecutionBoundary(markets, prepareSummary) {
  return {
    deployCommandImplemented: true,
    verifyCommandImplemented: true,
    executableToday: prepareSummary.ready,
    status: prepareSummary.ready
      ? 'deploy-morpho-market and verify-morpho-market are available'
      : 'market preparation incomplete',
    blockers: prepareSummary.ready
      ? []
      : ['At least one Morpho market is not fully prepared yet, so deploy-morpho-market should not be attempted.'],
    missingCommands: [],
    marketCount: markets.length,
  };
}

function buildHonestStatus(markets, prepareSummary) {
  if (markets.some((market) => ['browser-assisted', 'executable', 'mixed'].includes(market.feedFunding?.overallState || ''))) {
    return 'funding handoff required';
  }
  if (markets.some((market) => market.feedReadiness.candidatePaths.some((candidate) => candidate.feedReadinessState === 'activation-needed'))) {
    return 'funding handoff required';
  }
  if (prepareSummary.ready) {
    return 'market preparation ready';
  }
  if (markets.every((market) => market.oracleAdapterPlan.ready)) {
    return 'oracle-adapter design ready';
  }
  return 'plan-only';
}

function buildNextSteps(markets, prepareSummary, executionBoundary) {
  if (!prepareSummary.ready) {
    const browserPlans = markets
      .flatMap((market) => market.feedFunding && Array.isArray(market.feedFunding.entries) ? market.feedFunding.entries : [])
      .filter((entry) => entry.browserPlan)
      .map((entry) => ({
        type: 'browser-assisted',
        message: `Browser-assisted feed funding is required for ${entry.feedName}.`,
        browserPlan: entry.browserPlan,
      }));

    if (browserPlans.length > 0) {
      return browserPlans;
    }

    const activationSteps = markets
      .flatMap((market) => market.feedReadiness.candidatePaths)
      .flatMap((candidate) => candidate.ensureFeeds?.activationPlan?.actions || [])
      .map((action) => ({
        type: 'command',
        message: `Prepare activation for ${action.feedName}.`,
        command: action.command,
      }));

    if (activationSteps.length > 0) {
      return activationSteps;
    }

    return uniqueStrings(prepareSummary.blockers).map((blocker) => ({
      type: 'blocker',
      message: blocker,
    }));
  }

  return [
    {
      type: 'command',
      message: 'Run deploy-morpho-market with a Morpho core address to build or submit market creation transactions.',
      command: 'deploy-morpho-market',
    },
    ...executionBoundary.missingCommands.map((commandName) => ({
      type: 'implementation-gap',
      message: `Implement ${commandName} for post-deploy verification parity.`,
      command: commandName,
    })),
  ];
}

function buildDeployTransaction(preparedMarket, morphoCoreAddress) {
  return {
    transactionId: `morpho-create-market:${preparedMarket.marketKey}`,
    kind: 'contract-call',
    payloadKind: 'executable',
    targetContract: 'MorphoCore',
    contractFunction: 'createMarket',
    to: morphoCoreAddress,
    value: '0',
    data: MORPHO_INTERFACE.encodeFunctionData('createMarket', [preparedMarket.marketParams]),
    expectedMarketId: preparedMarket.marketId,
    marketKey: preparedMarket.marketKey,
    notes: `Create Morpho market ${preparedMarket.displayName}`,
    sendStatus: 'not-requested',
  };
}

function buildAdapterDeploymentTransaction(adapter) {
  return {
    transactionId: `morpho-deploy-adapter:${adapter.marketKey}`,
    kind: 'contract-deployment',
    payloadKind: 'executable',
    contractName: adapter.deployment.contractName,
    marketKey: adapter.marketKey,
    value: '0',
    data: adapter.deployment.data,
    deploymentRef: adapter.deploymentRef,
    notes: `Deploy ${adapter.deployment.contractName} for ${adapter.displayName}`,
    sendStatus: 'not-requested',
  };
}

function buildApi3ReaderProxyDeploymentTransaction(proxyDeployment, marketKeys = []) {
  const proxyFactoryInterface = Api3ReaderProxyV1Factory__factory.createInterface();

  return {
    transactionId: `api3-deploy-reader-proxy:${proxyDeployment.dapiName}:${proxyDeployment.proxyAddress}`,
    kind: 'contract-call',
    payloadKind: 'executable',
    targetContract: 'Api3ReaderProxyV1Factory',
    contractFunction: 'deployApi3ReaderProxyV1',
    to: proxyDeployment.factoryAddress,
    value: '0',
    data: proxyFactoryInterface.encodeFunctionData('deployApi3ReaderProxyV1', [
      proxyDeployment.dapiNameBytes32 || encodeBytes32String(proxyDeployment.dapiName),
      proxyDeployment.dappId,
      proxyDeployment.metadata || '0x',
    ]),
    notes: `Deploy communal Api3ReaderProxyV1 for ${proxyDeployment.dapiName}${marketKeys.length > 0 ? ` before ${marketKeys.join(', ')}` : ''}`,
    sendStatus: 'not-requested',
  };
}

function collectRequiredProxyDeploymentTransactions(markets, warnings = []) {
  const deploymentsByProxyAddress = new Map();

  for (const market of Array.isArray(markets) ? markets : []) {
    for (const binding of Array.isArray(market?.oracleAdapterPlan?.feedBindings) ? market.oracleAdapterPlan.feedBindings : []) {
      const proxyDeployment = binding?.proxyDeploymentPlan;
      if (!proxyDeployment || !proxyDeployment.proxyAddress) {
        continue;
      }

      const existing = deploymentsByProxyAddress.get(proxyDeployment.proxyAddress);
      if (existing) {
        existing.marketKeys.add(market.marketKey);
        continue;
      }

      deploymentsByProxyAddress.set(proxyDeployment.proxyAddress, {
        proxyDeployment,
        marketKeys: new Set([market.marketKey]),
      });
    }
  }

  return [...deploymentsByProxyAddress.values()].map(({ proxyDeployment, marketKeys }) => {
    warnings.push(`Will deploy communal Api3 reader proxy ${proxyDeployment.proxyAddress} for ${proxyDeployment.dapiName} before adapter deployment because the deterministic address has no code yet.`);
    return buildApi3ReaderProxyDeploymentTransaction(proxyDeployment, [...marketKeys].sort());
  });
}

function assessLiveFeedBindingSafety(markets, request) {
  const send = request && request.send ? request.send : {};
  const isLiveSend = Boolean(send.enabled) && send.dryRun === false;

  if (!isLiveSend) {
    return { blockers: [], warnings: [] };
  }

  const missingLiveProxyBindings = [];
  for (const market of Array.isArray(markets) ? markets : []) {
    for (const binding of Array.isArray(market?.oracleAdapterPlan?.feedBindings) ? market.oracleAdapterPlan.feedBindings : []) {
      if (binding?.proxyHasCode === false && !binding?.proxyDeploymentPlan) {
        missingLiveProxyBindings.push(`${market.marketKey}:${binding.feedName}`);
      }
    }
  }

  if (missingLiveProxyBindings.length === 0) {
    return { blockers: [], warnings: [] };
  }

  return {
    blockers: [
      `Refusing live Morpho send because these feed bindings resolve to proxy addresses with no code and no proxyDeploymentPlan: ${missingLiveProxyBindings.join(', ')}`,
    ],
    warnings: [],
  };
}

function mergeOracleResolution(request, byMarketKey) {
  const current = request.oracleResolution || {};
  return {
    ...current,
    byMarketKey: {
      ...(current.byMarketKey || {}),
      ...byMarketKey,
    },
  };
}

function buildPreparedMarketOracleResolutionArtifact(request, prepareSummary, fallbackAutoOracleResolution = null) {
  const byMarketKey = Object.fromEntries(
    (Array.isArray(prepareSummary?.markets) ? prepareSummary.markets : [])
      .filter((preparedMarket) => preparedMarket && preparedMarket.marketKey && /^0x[a-fA-F0-9]{40}$/.test(String(preparedMarket.oracle?.address || '')))
      .map((preparedMarket) => [preparedMarket.marketKey, preparedMarket.oracle.address]),
  );

  if (Object.keys(byMarketKey).length === 0) {
    return fallbackAutoOracleResolution;
  }

  let mode = 'resolved-oracle-resolution';
  if (fallbackAutoOracleResolution && fallbackAutoOracleResolution.mode) {
    mode = fallbackAutoOracleResolution.mode;
  } else if (request.deploymentResult) {
    mode = 'deployment-result-handoff';
  } else if (request.oracleResolution) {
    mode = 'explicit-oracle-resolution';
  }

  return {
    mode,
    ...(fallbackAutoOracleResolution && fallbackAutoOracleResolution.signerAddress
      ? { signerAddress: fallbackAutoOracleResolution.signerAddress }
      : {}),
    ...(fallbackAutoOracleResolution && Number.isInteger(fallbackAutoOracleResolution.startingNonce)
      ? { startingNonce: fallbackAutoOracleResolution.startingNonce }
      : {}),
    byMarketKey,
    marketKeys: Object.keys(byMarketKey),
  };
}

function listRequestMarketKeys(request) {
  return buildMorphoMarketEntries(normalizeMorphoWorkflowRequest(request)).map((entry) => entry.marketKey).sort();
}

function listDeploymentResultMarketKeys(deploymentResult) {
  return uniqueStrings([
    ...(Array.isArray(deploymentResult?.markets)
      ? deploymentResult.markets.map((entry) => entry && entry.marketKey).filter(Boolean)
      : []),
    ...(Array.isArray(deploymentResult?.transactionPlan)
      ? deploymentResult.transactionPlan.map((entry) => entry && entry.marketKey).filter(Boolean)
      : []),
    ...(Array.isArray(deploymentResult?.autoOracleResolution?.marketKeys)
      ? deploymentResult.autoOracleResolution.marketKeys.filter(Boolean)
      : []),
  ]).sort();
}

function assessDeploymentResultCompatibility(request) {
  const deploymentResult = request.deploymentResult;
  if (!deploymentResult) {
    return {
      compatible: true,
      blockers: [],
      warnings: [],
    };
  }

  const blockers = [];

  if (
    deploymentResult.chain
    && Number.isInteger(deploymentResult.chain.chainId)
    && Number.isInteger(request.chain?.chainId)
    && deploymentResult.chain.chainId !== request.chain.chainId
  ) {
    blockers.push(`deploymentResult chainId ${deploymentResult.chain.chainId} does not match request.chain.chainId ${request.chain.chainId}.`);
  }

  if (
    deploymentResult.morphoCoreAddress
    && request.morphoCoreAddress
    && normalizeLowerAddress(deploymentResult.morphoCoreAddress) !== normalizeLowerAddress(request.morphoCoreAddress)
  ) {
    blockers.push(`deploymentResult morphoCoreAddress ${deploymentResult.morphoCoreAddress} does not match request.morphoCoreAddress ${request.morphoCoreAddress}.`);
  }

  const deploymentMarketKeys = listDeploymentResultMarketKeys(deploymentResult);
  const requestMarketKeys = listRequestMarketKeys(request);
  if (deploymentMarketKeys.length > 0) {
    const deploymentKeyString = deploymentMarketKeys.join(',');
    const requestKeyString = requestMarketKeys.join(',');
    if (deploymentKeyString !== requestKeyString) {
      blockers.push(`deploymentResult market keys [${deploymentMarketKeys.join(', ')}] do not match request market keys [${requestMarketKeys.join(', ')}].`);
    }
  }

  return {
    compatible: blockers.length === 0,
    blockers,
    warnings: [],
  };
}

function assessLiveDeploymentResultSafety(request) {
  const deploymentResult = request.deploymentResult;
  const liveSendRequested = Boolean(request.send && request.send.enabled && request.send.dryRun === false);

  if (!deploymentResult || !liveSendRequested) {
    return {
      blockers: [],
      warnings: [],
    };
  }

  const deploymentTransactions = Array.isArray(deploymentResult.transactionPlan)
    ? deploymentResult.transactionPlan.filter((entry) => entry && entry.kind === 'contract-deployment')
    : [];

  if (deploymentTransactions.length === 0) {
    return {
      blockers: [],
      warnings: [],
    };
  }

  const blockers = [];
  const sendSummary = deploymentResult.sendSummary || {};
  if (sendSummary.completed !== true) {
    blockers.push('Refusing live Morpho market creation from deploymentResult because the upstream adapter deployment did not complete successfully.');
  }

  deploymentTransactions.forEach((entry) => {
    if (entry.sendStatus && !['submitted', 'confirmed'].includes(entry.sendStatus)) {
      blockers.push(`Refusing live Morpho market creation because upstream adapter deployment ${entry.transactionId} ended with sendStatus=${entry.sendStatus}.`);
    }
  });

  return {
    blockers: uniqueStrings(blockers),
    warnings: [],
  };
}

function deriveOracleResolutionFromDeploymentResult(deploymentResult) {
  if (!deploymentResult || typeof deploymentResult !== 'object') {
    return null;
  }

  const predictedByMarketKey = deploymentResult.autoOracleResolution && deploymentResult.autoOracleResolution.byMarketKey
    ? deploymentResult.autoOracleResolution.byMarketKey
    : {};

  const deployedByMarketKey = Array.isArray(deploymentResult.transactionPlan)
    ? deploymentResult.transactionPlan.reduce((accumulator, entry) => {
        if (
          entry
          && entry.kind === 'contract-deployment'
          && typeof entry.marketKey === 'string'
          && /^0x[a-fA-F0-9]{40}$/.test(String(entry.deployedAddress || ''))
        ) {
          accumulator[entry.marketKey] = entry.deployedAddress;
        }
        return accumulator;
      }, {})
    : {};

  const byMarketKey = {
    ...predictedByMarketKey,
    ...deployedByMarketKey,
  };

  if (Object.keys(byMarketKey).length === 0) {
    return null;
  }

  return { byMarketKey };
}

async function maybeBuildStandaloneAdapterOracleResolution(request, transactionPlan, warnings) {
  if (!Array.isArray(transactionPlan) || transactionPlan.length === 0) {
    return null;
  }

  const send = request.send || {};
  let resolvedPrivateKey = null;
  try {
    resolvedPrivateKey = resolvePrivateKeyInput(send, 'request.send');
  } catch (error) {
    warnings.push(error.message);
    return null;
  }

  if (!send.rpcUrl || !resolvedPrivateKey) {
    return null;
  }

  const networkResolution = await maybeResolveNetwork(warnings, send.rpcUrl);
  if (!networkResolution) {
    return null;
  }

  if (networkResolution.chainId !== request.chain.chainId) {
    warnings.push(`Resolved RPC chain id ${networkResolution.chainId} does not match requested chain id ${request.chain.chainId} for Morpho adapter deployment threading.`);
    return null;
  }

  const wallet = new Wallet(resolvedPrivateKey, networkResolution.provider);
  const signerAddress = await wallet.getAddress();
  const startingNonce = await networkResolution.provider.getTransactionCount(signerAddress, 'pending');
  const byMarketKey = {};

  transactionPlan.forEach((transaction, index) => {
    if (transaction.kind === 'contract-deployment' && typeof transaction.marketKey === 'string' && transaction.marketKey) {
      byMarketKey[transaction.marketKey] = getCreateAddress({ from: signerAddress, nonce: startingNonce + index });
    }
  });

  warnings.push(
    `Morpho adapter deploy output includes predicted oracle addresses from signer ${signerAddress} starting at pending nonce ${startingNonce}.`,
  );
  if (!send.enabled || send.dryRun !== false) {
    warnings.push('Predicted Morpho adapter addresses are planning-only until that same signer executes the deployment sequence.');
  }

  return {
    mode: 'predicted-adapter-deployments',
    signerAddress,
    startingNonce,
    byMarketKey,
    marketKeys: Object.keys(byMarketKey),
  };
}

function resolveAdapterDeploymentOracleResolution(predictedResolution, transactionPlan) {
  const deployedByMarketKey = Array.isArray(transactionPlan)
    ? transactionPlan.reduce((accumulator, entry) => {
        if (
          entry
          && entry.kind === 'contract-deployment'
          && typeof entry.marketKey === 'string'
          && /^0x[a-fA-F0-9]{40}$/.test(String(entry.deployedAddress || ''))
        ) {
          accumulator[entry.marketKey] = entry.deployedAddress;
        }
        return accumulator;
      }, {})
    : {};

  const byMarketKey = {
    ...((predictedResolution && predictedResolution.byMarketKey) || {}),
    ...deployedByMarketKey,
  };

  if (Object.keys(byMarketKey).length === 0) {
    return null;
  }

  return {
    mode: Object.keys(deployedByMarketKey).length > 0 ? 'adapter-deployment-results' : predictedResolution.mode,
    signerAddress: predictedResolution ? predictedResolution.signerAddress : undefined,
    startingNonce: predictedResolution ? predictedResolution.startingNonce : undefined,
    byMarketKey,
    marketKeys: Object.keys(byMarketKey),
  };
}

function applyDeploymentResultOracleResolution(request) {
  const derivedOracleResolution = deriveOracleResolutionFromDeploymentResult(request.deploymentResult);
  if (!derivedOracleResolution) {
    return request;
  }

  return {
    ...request,
    oracleResolution: {
      ...derivedOracleResolution,
      ...(request.oracleResolution || {}),
      byMarketKey: {
        ...(derivedOracleResolution.byMarketKey || {}),
        ...((request.oracleResolution && request.oracleResolution.byMarketKey) || {}),
      },
    },
  };
}

async function maybeBuildChainedMorphoDeployment(request, workflow, options = {}) {
  return measureMorphoPerf(options, 'maybeBuildChainedMorphoDeployment', {
    marketCount: Array.isArray(workflow?.markets) ? workflow.markets.length : 0,
  }, async () => {
  const marketsNeedingAdapterAddress = workflow.markets.filter((market) => (
    !market.prepareMorphoMarket.oracle.address
    && market.oracleAdapterPlan
    && market.oracleAdapterPlan.ready
  ));

  if (marketsNeedingAdapterAddress.length === 0) {
    return {
      request,
      workflow,
      adapterTransactionPlan: [],
      autoOracleResolution: null,
      blockers: [],
      warnings: [],
      startingNonce: undefined,
    };
  }

  const send = request.send || {};
  let resolvedPrivateKey = null;
  try {
    resolvedPrivateKey = resolvePrivateKeyInput(send, 'request.send');
  } catch (error) {
    return {
      request,
      workflow,
      adapterTransactionPlan: [],
      autoOracleResolution: null,
      blockers: [error.message],
      warnings: [],
      startingNonce: undefined,
    };
  }

  if (!send.rpcUrl || !resolvedPrivateKey) {
    return {
      request,
      workflow,
      adapterTransactionPlan: [],
      autoOracleResolution: null,
      blockers: [
        `Automatic Morpho adapter-to-market threading requires send.rpcUrl and send.privateKey or send.privateKeyEnv when oracleResolution is omitted for ${marketsNeedingAdapterAddress.map((market) => market.marketKey).join(', ')}.`,
      ],
      warnings: [],
      startingNonce: undefined,
    };
  }

  const warnings = [];
  const networkResolution = await maybeResolveNetwork(warnings, send.rpcUrl);
  if (!networkResolution) {
    return {
      request,
      workflow,
      adapterTransactionPlan: [],
      autoOracleResolution: null,
      blockers: ['Automatic Morpho adapter-to-market threading could not resolve the send RPC network.'],
      warnings,
      startingNonce: undefined,
    };
  }

  if (networkResolution.chainId !== request.chain.chainId) {
    return {
      request,
      workflow,
      adapterTransactionPlan: [],
      autoOracleResolution: null,
      blockers: [`Resolved RPC chain id ${networkResolution.chainId} does not match requested chain id ${request.chain.chainId} for automatic Morpho adapter threading.`],
      warnings,
      startingNonce: undefined,
    };
  }

  const wallet = new Wallet(resolvedPrivateKey, networkResolution.provider);
  const signerAddress = await wallet.getAddress();
  const startingNonce = await networkResolution.provider.getTransactionCount(signerAddress, 'pending');
  const predictedByMarketKey = {};
  const proxyTransactionPlan = collectRequiredProxyDeploymentTransactions(workflow.markets, warnings);
  /** @type {any[]} */
  const adapterTransactionPlan = [...proxyTransactionPlan];
  const missingMarketKeys = new Set(marketsNeedingAdapterAddress.map((market) => market.marketKey));
  let nextNonce = startingNonce + proxyTransactionPlan.length;

  for (const market of workflow.markets) {
    if (!missingMarketKeys.has(market.marketKey)) {
      continue;
    }

    const deployment = buildMorphoAdapterDeploymentData(market.oracleAdapterPlan);
    predictedByMarketKey[market.marketKey] = getCreateAddress({ from: signerAddress, nonce: nextNonce });
    nextNonce += 1;
    adapterTransactionPlan.push(buildAdapterDeploymentTransaction({
      marketKey: market.marketKey,
      displayName: market.displayName,
      deploymentRef: market.oracleAdapterPlan.deploymentRef,
      deployment,
    }));
  }

  warnings.push(
    `Auto-threaded Morpho oracle addresses were predicted from signer ${signerAddress} starting at pending nonce ${startingNonce}.`,
  );
  warnings.push(
    'The chained Morpho plan assumes no unrelated transactions consume signer nonces before these adapter deployments and market creations are sent.',
  );
  if (!send.enabled || send.dryRun !== false) {
    warnings.push('This chained Morpho result is planning-only until the same signer executes it. Recompute immediately before live send if the nonce may have changed.');
  }

  const requestWithOracleResolution = {
    ...request,
    oracleResolution: mergeOracleResolution(request, predictedByMarketKey),
  };
  const workflowWithOracleAddresses = await buildMorphoWorkflow(requestWithOracleResolution, options);

  return {
    request: requestWithOracleResolution,
    workflow: workflowWithOracleAddresses,
    adapterTransactionPlan,
    autoOracleResolution: {
      mode: 'predicted-adapter-deployments',
      signerAddress,
      startingNonce,
      byMarketKey: predictedByMarketKey,
      marketKeys: Object.keys(predictedByMarketKey),
    },
    blockers: [],
    warnings,
    startingNonce,
  };
  });
}

async function maybeResolveNetwork(warnings, rpcUrl) {
  if (!rpcUrl) {
    return null;
  }

  try {
    const provider = new JsonRpcProvider(rpcUrl);
    const network = await provider.getNetwork();
    return {
      provider,
      chainId: Number(network.chainId),
    };
  } catch (error) {
    warnings.push(`Failed to resolve RPC network: ${error.message}`);
    return null;
  }
}

function resolveVerificationRpcUrl(request) {
  if (request.send && typeof request.send.rpcUrl === 'string' && request.send.rpcUrl.trim()) {
    return request.send.rpcUrl.trim();
  }

  if (request.rpcPreference && typeof request.rpcPreference.rpcUrl === 'string' && request.rpcPreference.rpcUrl.trim()) {
    return request.rpcPreference.rpcUrl.trim();
  }

  if (request.rpcPreference && Array.isArray(request.rpcPreference.rpcUrls)) {
    const first = request.rpcPreference.rpcUrls.find((entry) => typeof entry === 'string' && entry.trim());
    if (first) {
      return first.trim();
    }
  }

  return null;
}

function getMorphoTransactionProgressPhase(transaction) {
  if (transaction.kind === 'contract-deployment') {
    return 'adapter-deployment';
  }
  if (transaction.targetContract === 'MorphoCore' || transaction.contractFunction === 'createMarket') {
    return 'market-deployment';
  }
  return 'deployment';
}

async function maybeSendMorphoTransactions({ transactionPlan, send, broadcast, executorWarnings, requestedChainId, startingNonce, progressOptions = {} }) {
  const sendSummary = {
    requested: Boolean(send && send.enabled),
    attempted: false,
    dryRun: send ? send.dryRun !== false : true,
    submittedTransactions: 0,
    failedTransactions: 0,
    skippedTransactions: 0,
    signerAddress: undefined,
    rpcUrlConfigured: Boolean(send && send.rpcUrl),
    failureReason: undefined,
    completed: false,
  };

  if (!sendSummary.requested) {
    return { transactionPlan, sendSummary };
  }

  if (!broadcast || broadcast.enabled !== true) {
    const failureReason = 'Send path requires broadcast.enabled=true.';
    executorWarnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, sendSummary };
  }

  if (broadcast.acknowledgement !== SEND_ACKNOWLEDGEMENT) {
    const failureReason = 'Send path requires the explicit broadcast acknowledgement token.';
    executorWarnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, sendSummary };
  }

  let resolvedPrivateKey = null;
  try {
    resolvedPrivateKey = resolvePrivateKeyInput(send, 'request.send');
  } catch (error) {
    sendSummary.failureReason = error.message;
    return { transactionPlan, sendSummary };
  }

  if (!send.rpcUrl || !resolvedPrivateKey) {
    const failureReason = 'Send path requires send.rpcUrl and send.privateKey or send.privateKeyEnv.';
    executorWarnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, sendSummary };
  }

  const networkResolution = await maybeResolveNetwork(executorWarnings, send.rpcUrl);
  if (!networkResolution) {
    sendSummary.failureReason = 'RPC network resolution failed.';
    return { transactionPlan, sendSummary };
  }

  if (networkResolution.chainId !== requestedChainId) {
    const failureReason = `Resolved RPC chain id ${networkResolution.chainId} does not match requested chain id ${requestedChainId}.`;
    executorWarnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, sendSummary };
  }

  const wallet = new Wallet(resolvedPrivateKey, networkResolution.provider);
  const signerAddress = await wallet.getAddress();
  sendSummary.signerAddress = signerAddress;

  if (broadcast.signerAddress && signerAddress.toLowerCase() !== broadcast.signerAddress.toLowerCase()) {
    const failureReason = 'Resolved signer address does not match broadcast.signerAddress.';
    executorWarnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, sendSummary };
  }

  sendSummary.attempted = true;

  for (let index = 0; index < transactionPlan.length; index += 1) {
    const transaction = transactionPlan[index];
    const progressPhase = getMorphoTransactionProgressPhase(transaction);

    emitMorphoProgress(progressOptions, {
      phase: progressPhase,
      status: 'started',
      message: transaction.notes || `Starting ${transaction.transactionId}`,
      attempt: index + 1,
      details: {
        transactionId: transaction.transactionId,
        marketKey: transaction.marketKey,
        kind: transaction.kind,
      },
    });

    if (sendSummary.dryRun) {
      transaction.sendStatus = 'dry-run';
      emitMorphoProgress(progressOptions, {
        phase: progressPhase,
        status: 'completed',
        message: `Dry-run prepared: ${transaction.notes || transaction.transactionId}`,
        attempt: index + 1,
        details: {
          transactionId: transaction.transactionId,
          mode: 'dry-run',
        },
      });
      continue;
    }

    try {
      const submitted = await wallet.sendTransaction({
        to: transaction.to,
        data: transaction.data,
        value: 0,
        ...(Number.isInteger(startingNonce) ? { nonce: startingNonce + index } : {}),
      });
      const receipt = await submitted.wait();
      transaction.sendStatus = 'submitted';
      transaction.txHash = submitted.hash;
      transaction.blockNumber = receipt ? receipt.blockNumber : undefined;
      transaction.deployedAddress = receipt && receipt.contractAddress ? receipt.contractAddress : undefined;
      sendSummary.submittedTransactions += 1;
      emitMorphoProgress(progressOptions, {
        phase: progressPhase,
        status: 'completed',
        message: `Completed: ${transaction.notes || transaction.transactionId}`,
        attempt: index + 1,
        details: {
          transactionId: transaction.transactionId,
          txHash: submitted.hash,
          blockNumber: receipt ? receipt.blockNumber : undefined,
        },
      });
    } catch (error) {
      transaction.sendStatus = 'failed';
      transaction.error = error.message;
      sendSummary.failedTransactions += 1;
      sendSummary.failureReason = error.message;

      emitMorphoProgress(progressOptions, {
        phase: progressPhase,
        status: 'blocked',
        message: `Failed: ${transaction.notes || transaction.transactionId}`,
        attempt: index + 1,
        details: {
          transactionId: transaction.transactionId,
          error: error.message,
        },
      });

      for (let restIndex = index + 1; restIndex < transactionPlan.length; restIndex += 1) {
        transactionPlan[restIndex].sendStatus = 'skipped';
        transactionPlan[restIndex].error = 'Skipped because a prior transaction in the chained Morpho plan failed.';
        sendSummary.skippedTransactions += 1;
      }
      return { transactionPlan, sendSummary };
    }
  }

  sendSummary.completed = !sendSummary.dryRun && sendSummary.failedTransactions === 0;
  return { transactionPlan, sendSummary };
}

function buildDeployMorphoMarketStatus({ prepareSummary, morphoCoreAddress, transactionPlan, sendSummary, adapterDeploymentCount, autoOracleResolution }) {
  return {
    ready: prepareSummary.ready,
    morphoCoreAddressConfigured: Boolean(morphoCoreAddress),
    adapterDeploymentCount,
    transactionCount: transactionPlan.length,
    created: sendSummary.completed,
    sendRequested: sendSummary.requested,
    sendCompleted: sendSummary.completed,
    sendDryRun: sendSummary.dryRun,
    autoOracleResolutionMode: autoOracleResolution ? autoOracleResolution.mode : 'explicit-or-requested',
  };
}

function combineMorphoSendSummaries(...summaries) {
  const present = summaries.filter(Boolean);
  return {
    requested: present.some((summary) => summary.requested),
    attempted: present.some((summary) => summary.attempted),
    dryRun: present.every((summary) => summary.dryRun !== false),
    submittedTransactions: present.reduce((total, summary) => total + (summary.submittedTransactions || 0), 0),
    failedTransactions: present.reduce((total, summary) => total + (summary.failedTransactions || 0), 0),
    skippedTransactions: present.reduce((total, summary) => total + (summary.skippedTransactions || 0), 0),
    signerAddress: present.find((summary) => summary.signerAddress)?.signerAddress,
    rpcUrlConfigured: present.some((summary) => summary.rpcUrlConfigured),
    failureReason: present.find((summary) => summary.failureReason)?.failureReason,
    completed: present.length > 0 && present.every((summary) => summary.completed === true),
  };
}

function normalizeLowerAddress(value) {
  return String(value || '').toLowerCase();
}

function marketParamsMatch(expected, actual) {
  return normalizeLowerAddress(expected.loanToken) === normalizeLowerAddress(actual.loanToken)
    && normalizeLowerAddress(expected.collateralToken) === normalizeLowerAddress(actual.collateralToken)
    && normalizeLowerAddress(expected.oracle) === normalizeLowerAddress(actual.oracle)
    && normalizeLowerAddress(expected.irm) === normalizeLowerAddress(actual.irm)
    && String(expected.lltv) === String(actual.lltv);
}

async function callMorphoView(provider, to, fragment, args) {
  const data = MORPHO_INTERFACE.encodeFunctionData(fragment, args);
  const raw = await provider.call({ to, data });
  return MORPHO_INTERFACE.decodeFunctionResult(fragment, raw);
}

async function callOraclePrice(provider, oracleAddress) {
  const data = MORPHO_ORACLE_INTERFACE.encodeFunctionData('price', []);
  const raw = await provider.call({ to: oracleAddress, data });
  const [price] = MORPHO_ORACLE_INTERFACE.decodeFunctionResult('price', raw);
  return price;
}

function buildVerifyMorphoMarketStatus({ verifiedMarkets, marketCount, rpcConfigured }) {
  return {
    verified: marketCount > 0 && verifiedMarkets === marketCount,
    marketCount,
    verifiedMarketCount: verifiedMarkets,
    rpcConfigured,
  };
}

async function buildMorphoWorkflow(request, options = {}) {
  return measureMorphoPerf(options, 'buildMorphoWorkflow', {
    collateralAssetCount: Array.isArray(request?.collateralAssets) ? request.collateralAssets.length : 0,
    borrowAssetCount: Array.isArray(request?.borrowAssets) ? request.borrowAssets.length : 0,
    feedFundingMode: getFeedFundingMode(request),
  }, async () => {
    validateRunMorphoWorkflowRequest(request);

  const deploymentResultCompatibility = assessDeploymentResultCompatibility(request);
  const resolvedRequest = deploymentResultCompatibility.compatible
    ? applyDeploymentResultOracleResolution(request)
    : request;

  const normalizedIntent = normalizeMorphoWorkflowRequest(resolvedRequest);
  const marketShape = assessMorphoMarketShape(normalizedIntent);
  const marketEntries = buildMorphoMarketEntries(normalizedIntent);
  const markets = [];

  for (const entry of marketEntries) {
    markets.push(await analyzeMorphoMarketEntry(entry, resolvedRequest, options));
  }

  const basePrepareSummary = buildPrepareMorphoMarketSummary(markets, marketShape);
  const prepareSummary = {
    ...basePrepareSummary,
    ready: deploymentResultCompatibility.blockers.length === 0 && basePrepareSummary.ready,
    blockedMarketCount: deploymentResultCompatibility.blockers.length === 0
      ? basePrepareSummary.blockedMarketCount
      : basePrepareSummary.blockedMarketCount + 1,
    blockers: uniqueStrings([
      ...deploymentResultCompatibility.blockers,
      ...(basePrepareSummary.blockers || []),
    ]),
    warnings: uniqueStrings([
      ...deploymentResultCompatibility.warnings,
      ...(basePrepareSummary.warnings || []),
    ]),
  };
  const executionBoundary = summarizeExecutionBoundary(markets, prepareSummary);
  const honestStatus = buildHonestStatus(markets, prepareSummary);
  const blockers = uniqueStrings([
    ...deploymentResultCompatibility.blockers,
    ...marketShape.blockers,
    ...markets.flatMap((market) => market.blockers || []),
    ...executionBoundary.blockers,
  ]);
  const warnings = uniqueStrings([
    ...deploymentResultCompatibility.warnings,
    ...marketShape.warnings,
    ...markets.flatMap((market) => market.warnings || []),
  ]);

  const firstMarket = markets[0] || null;

    return {
      honestStatus,
      normalizedIntent,
      marketShape,
      markets,
      feedFunding: {
        modeRequested: getFeedFundingMode(request),
        overallState: summarizeFundingState(markets.flatMap((market) => market.feedFunding?.entries || [])),
        entries: markets.flatMap((market) => market.feedFunding?.entries || []),
      },
      feedReadiness: firstMarket
        ? firstMarket.feedReadiness
        : { recommendedPathId: null, candidatePaths: [] },
      oracleAdapterPlan: firstMarket ? firstMarket.oracleAdapterPlan : null,
      prepareMorphoMarket: prepareSummary,
      deploymentResultCompatibility,
      executionBoundary,
      blockers,
      warnings,
      nextSteps: buildNextSteps(markets, prepareSummary, executionBoundary),
    };
  });
}

async function runMorphoWorkflow(request, options = {}) {
  return buildMorphoWorkflow(request, options);
}

async function prepareMorphoMarket(request, options = {}) {
  validatePrepareMorphoMarketRequest(request);
  const workflow = await buildMorphoWorkflow(request, options);
  return workflow.prepareMorphoMarket;
}

async function deployMorphoMarket(request, options = {}) {
  validateDeployMorphoMarketRequest(request);
  assertNoUnsafeLivePlaceholders(request);

  const initialWorkflow = options.precomputedWorkflow || await buildMorphoWorkflow(request, options);
  const chainedDeployment = await maybeBuildChainedMorphoDeployment(request, initialWorkflow, options);
  const liveDeploymentSafety = assessLiveDeploymentResultSafety(request);
  let resolvedRequest = chainedDeployment.request;
  let workflow = chainedDeployment.workflow;
  let prepareSummary = workflow.prepareMorphoMarket;
  let liveFeedBindingSafety = assessLiveFeedBindingSafety(workflow.markets, resolvedRequest);
  const blockers = [...(prepareSummary.blockers || [])];
  const warnings = [...(prepareSummary.warnings || []), ...(chainedDeployment.warnings || []), ...(liveDeploymentSafety.warnings || []), ...(liveFeedBindingSafety.warnings || [])];

  blockers.push(...(chainedDeployment.blockers || []));
  blockers.push(...(liveDeploymentSafety.blockers || []));
  blockers.push(...(liveFeedBindingSafety.blockers || []));

  if (!resolvedRequest.morphoCoreAddress) {
    blockers.push('request.morphoCoreAddress is required to build Morpho market creation calldata.');
  }

  for (const market of workflow.markets) {
    if (market.existingMarkets.exactMatches.length > 0) {
      blockers.push(`Exact Morpho market already appears in the local registry for ${market.marketKey}. Refusing duplicate market creation planning.`);
    }
  }

  const dryRunRequested = resolvedRequest.send ? resolvedRequest.send.dryRun !== false : true;
  const shouldThreadFromReceipts = blockers.length === 0
    && resolvedRequest.send?.enabled === true
    && dryRunRequested === false
    && Array.isArray(chainedDeployment.adapterTransactionPlan)
    && chainedDeployment.adapterTransactionPlan.length > 0
    && chainedDeployment.autoOracleResolution;

  let transactionPlan = [];

  let sendSummary = {
    requested: Boolean(request.send && request.send.enabled),
    attempted: false,
    dryRun: request.send ? request.send.dryRun !== false : true,
    submittedTransactions: 0,
    failedTransactions: 0,
    skippedTransactions: 0,
    signerAddress: undefined,
    rpcUrlConfigured: Boolean(request.send && request.send.rpcUrl),
    failureReason: undefined,
    completed: false,
  };

  if (blockers.length === 0) {
    if (shouldThreadFromReceipts) {
      const adapterSendResult = await maybeSendMorphoTransactions({
        transactionPlan: [...(chainedDeployment.adapterTransactionPlan || [])],
        send: resolvedRequest.send,
        broadcast: resolvedRequest.broadcast,
        executorWarnings: warnings,
        requestedChainId: resolvedRequest.chain.chainId,
        startingNonce: chainedDeployment.startingNonce,
        progressOptions: options,
      });

      transactionPlan = [...adapterSendResult.transactionPlan];
      sendSummary = adapterSendResult.sendSummary;

      if (adapterSendResult.sendSummary.completed) {
        const actualOracleResolution = resolveAdapterDeploymentOracleResolution(
          chainedDeployment.autoOracleResolution,
          adapterSendResult.transactionPlan,
        );
        resolvedRequest = {
          ...resolvedRequest,
          oracleResolution: mergeOracleResolution(resolvedRequest, actualOracleResolution.byMarketKey),
        };
        workflow = await buildMorphoWorkflow(resolvedRequest, options);
        prepareSummary = workflow.prepareMorphoMarket;
        liveFeedBindingSafety = assessLiveFeedBindingSafety(workflow.markets, resolvedRequest);
        warnings.push(...(prepareSummary.warnings || []), ...(liveFeedBindingSafety.warnings || []));
        blockers.push(...(prepareSummary.blockers || []), ...(liveFeedBindingSafety.blockers || []));

        if (blockers.length === 0) {
          const marketTransactionPlan = prepareSummary.markets.map((preparedMarket) => buildDeployTransaction(preparedMarket, resolvedRequest.morphoCoreAddress));
          const marketSendResult = await maybeSendMorphoTransactions({
            transactionPlan: marketTransactionPlan,
            send: resolvedRequest.send,
            broadcast: resolvedRequest.broadcast,
            executorWarnings: warnings,
            requestedChainId: resolvedRequest.chain.chainId,
            startingNonce: (chainedDeployment.startingNonce || 0) + adapterSendResult.transactionPlan.length,
            progressOptions: options,
          });
          transactionPlan = [...adapterSendResult.transactionPlan, ...marketSendResult.transactionPlan];
          sendSummary = combineMorphoSendSummaries(adapterSendResult.sendSummary, marketSendResult.sendSummary);
        }
      }
    } else {
      const marketTransactionPlan = prepareSummary.markets.map((preparedMarket) => buildDeployTransaction(preparedMarket, resolvedRequest.morphoCoreAddress));
      transactionPlan = [...(chainedDeployment.adapterTransactionPlan || []), ...marketTransactionPlan];
      const sendResult = await maybeSendMorphoTransactions({
        transactionPlan,
        send: resolvedRequest.send,
        broadcast: resolvedRequest.broadcast,
        executorWarnings: warnings,
        requestedChainId: resolvedRequest.chain.chainId,
        startingNonce: chainedDeployment.startingNonce,
        progressOptions: options,
      });
      sendSummary = sendResult.sendSummary;
    }
  }

  const status = buildDeployMorphoMarketStatus({
    prepareSummary,
    morphoCoreAddress: resolvedRequest.morphoCoreAddress,
    transactionPlan,
    sendSummary,
    adapterDeploymentCount: prepareSummary.marketCount,
    autoOracleResolution: buildPreparedMarketOracleResolutionArtifact(resolvedRequest, prepareSummary, chainedDeployment.autoOracleResolution),
  });

  const autoOracleResolution = buildPreparedMarketOracleResolutionArtifact(
    resolvedRequest,
    prepareSummary,
    chainedDeployment.autoOracleResolution,
  );

  const result = {
    status,
    ready: prepareSummary.ready && blockers.length === 0,
    mode: prepareSummary.mode,
    strategy: prepareSummary.strategy,
    chain: {
      name: resolvedRequest.chain.name,
      chainId: resolvedRequest.chain.chainId,
    },
    morphoCoreAddress: resolvedRequest.morphoCoreAddress || null,
    autoOracleResolution,
    marketCount: prepareSummary.marketCount,
    markets: prepareSummary.markets.map((preparedMarket) => ({
      marketKey: preparedMarket.marketKey,
      displayName: preparedMarket.displayName,
      marketId: preparedMarket.marketId,
      marketParams: preparedMarket.marketParams,
      ready: preparedMarket.ready,
      oracle: preparedMarket.oracle,
    })),
    transactionPlan,
    sendSummary,
    blockers: uniqueStrings(blockers),
    warnings: uniqueStrings(warnings),
    nextSteps: blockers.length > 0
      ? blockers.map((blocker) => ({ type: 'blocker', message: blocker }))
      : [
          {
            type: 'command',
            message: sendSummary.completed
              ? 'Run verify-morpho-market against the target RPC after creation to confirm params and oracle reads.'
              : 'Run this same deploy-morpho-market request with live send enabled to execute the chained adapter deployment plus market creation, then verify on-chain.',
            command: sendSummary.completed ? 'verify-morpho-market' : 'deploy-morpho-market',
          },
        ],
  };

  return maybeExternalizeMorphoDeploymentPayloads(result, options);
}

async function deployMorphoOracleAdapter(request, options = {}) {
  validateDeployMorphoMarketRequest(request);
  assertNoUnsafeLivePlaceholders(request);

  const workflow = await buildMorphoWorkflow(request, options);
  const prepareSummary = buildPrepareMorphoOracleAdapterSummary(workflow.markets, workflow.marketShape);
  const blockers = [...(prepareSummary.blockers || [])];
  const liveFeedBindingSafety = assessLiveFeedBindingSafety(workflow.markets, request);
  const warnings = [...(prepareSummary.warnings || []), ...(liveFeedBindingSafety.warnings || [])];
  blockers.push(...(liveFeedBindingSafety.blockers || []));

  const transactionPlan = blockers.length === 0
    ? [
        ...collectRequiredProxyDeploymentTransactions(workflow.markets, warnings),
        ...prepareSummary.adapters.map((adapter) => buildAdapterDeploymentTransaction(adapter)),
      ]
    : [];

  let sendSummary = {
    requested: Boolean(request.send && request.send.enabled),
    attempted: false,
    dryRun: request.send ? request.send.dryRun !== false : true,
    submittedTransactions: 0,
    failedTransactions: 0,
    skippedTransactions: 0,
    signerAddress: undefined,
    rpcUrlConfigured: Boolean(request.send && request.send.rpcUrl),
    failureReason: undefined,
    completed: false,
  };

  const predictedOracleResolution = blockers.length === 0
    ? await maybeBuildStandaloneAdapterOracleResolution(request, transactionPlan, warnings)
    : null;

  if (blockers.length === 0) {
    const sendResult = await maybeSendMorphoTransactions({
      transactionPlan,
      send: request.send,
      broadcast: request.broadcast,
      executorWarnings: warnings,
      requestedChainId: request.chain.chainId,
      startingNonce: undefined,
      progressOptions: options,
    });
    sendSummary = sendResult.sendSummary;
  }

  const autoOracleResolution = resolveAdapterDeploymentOracleResolution(predictedOracleResolution, transactionPlan);

  const result = {
    status: {
      ready: prepareSummary.ready,
      transactionCount: transactionPlan.length,
      sendRequested: sendSummary.requested,
      sendCompleted: sendSummary.completed,
      sendDryRun: sendSummary.dryRun,
      autoOracleResolutionMode: autoOracleResolution ? autoOracleResolution.mode : 'not-available',
    },
    ready: prepareSummary.ready && blockers.length === 0,
    mode: prepareSummary.mode,
    strategy: prepareSummary.strategy,
    chain: {
      name: request.chain.name,
      chainId: request.chain.chainId,
    },
    marketCount: prepareSummary.marketCount,
    autoOracleResolution,
    adapters: prepareSummary.adapters.map((adapter) => {
      const adapterTransaction = transactionPlan.find(
        (entry) => entry.kind === 'contract-deployment' && entry.deploymentRef === adapter.deploymentRef,
      );

      return {
        marketKey: adapter.marketKey,
        displayName: adapter.displayName,
        ready: adapter.ready,
        adapterType: adapter.adapterType,
        routeType: adapter.routeType,
        deploymentRef: adapter.deploymentRef,
        contractName: adapter.deployment ? adapter.deployment.contractName : null,
        constructorArgs: adapter.constructorArgs,
        deployedAddress: adapterTransaction
          ? adapterTransaction.deployedAddress || (autoOracleResolution && autoOracleResolution.byMarketKey
            ? autoOracleResolution.byMarketKey[adapter.marketKey] || null
            : null)
          : null,
      };
    }),
    transactionPlan,
    sendSummary,
    blockers: uniqueStrings(blockers),
    warnings: uniqueStrings(warnings),
    nextSteps: blockers.length > 0
      ? blockers.map((blocker) => ({ type: 'blocker', message: blocker }))
      : [
          {
            type: 'command',
            message: 'Pass this adapter deployment result into deploy-morpho-market with request.deploymentResult or --deployment-result-file so oracle addresses thread forward automatically.',
            command: 'deploy-morpho-market',
          },
        ],
  };

  return maybeExternalizeMorphoDeploymentPayloads(result, options);
}

async function verifyMorphoMarket(request, options = {}) {
  validateVerifyMorphoMarketRequest(request);

  const workflow = await buildMorphoWorkflow(request, options);
  const prepareSummary = workflow.prepareMorphoMarket;
  const blockers = [...(prepareSummary.blockers || [])];
  const warnings = [...(prepareSummary.warnings || [])];

  if (!request.morphoCoreAddress) {
    blockers.push('request.morphoCoreAddress is required to verify Morpho markets on-chain.');
  }

  const rpcUrl = resolveVerificationRpcUrl(request);
  if (!rpcUrl) {
    blockers.push('A verification RPC URL is required. Supply request.rpcPreference.rpcUrl or request.send.rpcUrl.');
  }

  let provider = null;
  if (blockers.length === 0) {
    const networkResolution = await maybeResolveNetwork(warnings, rpcUrl);
    if (!networkResolution) {
      blockers.push('Could not resolve the verification RPC network.');
    } else if (networkResolution.chainId !== request.chain.chainId) {
      blockers.push(`Resolved RPC chain id ${networkResolution.chainId} does not match requested chain id ${request.chain.chainId}.`);
    } else {
      provider = networkResolution.provider;
    }
  }

  const markets = [];
  let verifiedMarkets = 0;

  for (const preparedMarket of prepareSummary.markets) {
    const marketResult = {
      marketKey: preparedMarket.marketKey,
      displayName: preparedMarket.displayName,
      marketId: preparedMarket.marketId,
      expectedMarketParams: preparedMarket.marketParams,
      verified: false,
      existsOnChain: false,
      paramsMatch: false,
      irmEnabled: false,
      lltvEnabled: false,
      oraclePrice: null,
      oraclePricePositive: false,
      blockers: [...(preparedMarket.blockers || [])],
      warnings: [...(preparedMarket.warnings || [])],
    };

    if (!preparedMarket.ready) {
      marketResult.blockers.push('Prepared market is not ready, so on-chain verification cannot proceed.');
      markets.push(marketResult);
      continue;
    }

    if (!provider) {
      markets.push(marketResult);
      continue;
    }

    try {
      const [loanToken, collateralToken, oracle, irm, lltv] = await callMorphoView(provider, request.morphoCoreAddress, 'idToMarketParams', [preparedMarket.marketId]);
      marketResult.onchainMarketParams = {
        loanToken,
        collateralToken,
        oracle,
        irm,
        lltv: String(lltv),
      };
      marketResult.paramsMatch = marketParamsMatch(preparedMarket.marketParams, marketResult.onchainMarketParams);
      if (!marketResult.paramsMatch) {
        marketResult.blockers.push('On-chain market params do not match the expected prepared params.');
      }
    } catch (error) {
      marketResult.blockers.push(`Failed to read idToMarketParams: ${error.message}`);
    }

    try {
      const marketState = await callMorphoView(provider, request.morphoCoreAddress, 'market', [preparedMarket.marketId]);
      const lastUpdate = Number(marketState[4] || 0);
      marketResult.marketState = {
        totalSupplyAssets: String(marketState[0]),
        totalSupplyShares: String(marketState[1]),
        totalBorrowAssets: String(marketState[2]),
        totalBorrowShares: String(marketState[3]),
        lastUpdate,
        fee: String(marketState[5]),
      };
      marketResult.existsOnChain = lastUpdate > 0;
      if (!marketResult.existsOnChain) {
        marketResult.blockers.push('Market state was readable but appears uninitialized on-chain.');
      }
    } catch (error) {
      marketResult.blockers.push(`Failed to read market state: ${error.message}`);
    }

    try {
      const [irmEnabled] = await callMorphoView(provider, request.morphoCoreAddress, 'isIrmEnabled', [preparedMarket.marketParams.irm]);
      marketResult.irmEnabled = Boolean(irmEnabled);
      if (!marketResult.irmEnabled) {
        marketResult.blockers.push('Configured IRM is not enabled on Morpho core.');
      }
    } catch (error) {
      marketResult.warnings.push(`Failed to read IRM enabled state: ${error.message}`);
    }

    try {
      const [lltvEnabled] = await callMorphoView(provider, request.morphoCoreAddress, 'isLltvEnabled', [preparedMarket.marketParams.lltv]);
      marketResult.lltvEnabled = Boolean(lltvEnabled);
      if (!marketResult.lltvEnabled) {
        marketResult.blockers.push('Configured LLTV is not enabled on Morpho core.');
      }
    } catch (error) {
      marketResult.warnings.push(`Failed to read LLTV enabled state: ${error.message}`);
    }

    try {
      const oraclePrice = await callOraclePrice(provider, preparedMarket.marketParams.oracle);
      marketResult.oraclePrice = String(oraclePrice);
      marketResult.oraclePricePositive = BigInt(oraclePrice) > 0n;
      if (!marketResult.oraclePricePositive) {
        marketResult.blockers.push('Oracle price read succeeded but returned a non-positive value.');
      }
    } catch (error) {
      marketResult.blockers.push(`Failed to read oracle price(): ${error.message}`);
    }

    marketResult.verified = marketResult.blockers.length === 0;
    if (marketResult.verified) {
      verifiedMarkets += 1;
    }

    marketResult.blockers = uniqueStrings(marketResult.blockers);
    marketResult.warnings = uniqueStrings(marketResult.warnings);
    markets.push(marketResult);
  }

  const status = buildVerifyMorphoMarketStatus({
    verifiedMarkets,
    marketCount: prepareSummary.marketCount,
    rpcConfigured: Boolean(rpcUrl),
  });

  return {
    status,
    verified: blockers.length === 0 && status.verified,
    mode: prepareSummary.mode,
    strategy: prepareSummary.strategy,
    morphoCoreAddress: request.morphoCoreAddress || null,
    rpcUrlConfigured: Boolean(rpcUrl),
    marketCount: prepareSummary.marketCount,
    markets,
    blockers: uniqueStrings([...blockers, ...markets.flatMap((market) => market.blockers || [])]),
    warnings: uniqueStrings([...warnings, ...markets.flatMap((market) => market.warnings || [])]),
    nextSteps: status.verified
      ? []
      : uniqueStrings([...blockers, ...markets.flatMap((market) => market.blockers || [])]).map((blocker) => ({ type: 'blocker', message: blocker })),
  };
}

async function preflightMorphoMarketRequest(request, options = {}) {
  const blockers = [];
  const warnings = [];

  try {
    validateRunMorphoWorkflowRequest(request);
  } catch (error) {
    blockers.push(error.message);
  }

  const placeholderFindings = collectUnsafePlaceholders(request);
  blockers.push(...placeholderFindings);
  warnings.push(...collectInlineSecretFindings(request));

  if (request?.feedFunding?.mode) {
    const normalizedFundingMode = normalizeFeedFundingMode(request.feedFunding.mode);
    if (String(request.feedFunding.mode).trim().toLowerCase() !== normalizedFundingMode) {
      warnings.push(`request.feedFunding.mode=${request.feedFunding.mode} was normalized to ${normalizedFundingMode}.`);
    }
  }

  if (request.chain?.chainId !== undefined && (!Number.isInteger(request.chain.chainId) || request.chain.chainId <= 0)) {
    blockers.push('request.chain.chainId must be a positive integer.');
  }

  if (requestMayExecuteLiveTransactions(request)) {
    if (!request.rpcPreference?.rpcUrl && !request.send?.rpcUrl && !request.feedFunding?.rpcUrl) {
      blockers.push('Live-capable execution requires an explicit RPC URL.');
    }
    if (!request.morphoCoreAddress) {
      blockers.push('Live-capable execution requires request.morphoCoreAddress.');
    }
    if (!request.morphoPolicy?.defaultIrmAddress && !request.morphoPolicy?.byMarketKey) {
      blockers.push('Live-capable execution requires Morpho IRM policy input.');
    }
    if (!request.morphoPolicy?.defaultLltv && !request.morphoPolicy?.byMarketKey) {
      blockers.push('Live-capable execution requires Morpho LLTV policy input.');
    }
  }

  const rpcUrl = request.rpcPreference?.rpcUrl || request.send?.rpcUrl || request.feedFunding?.rpcUrl || null;
  if (rpcUrl && !isUnsafePlaceholderString(rpcUrl) && !isCliFlagEnabled(options.skipRpcCheck)) {
    const networkResolution = await maybeResolveNetwork(warnings, rpcUrl);
    if (!networkResolution) {
      blockers.push('Preflight could not resolve the configured RPC network.');
    } else if (request.chain?.chainId && networkResolution.chainId !== request.chain.chainId) {
      blockers.push(`Configured RPC chain id ${networkResolution.chainId} does not match request.chain.chainId ${request.chain.chainId}.`);
    }
  }

  const safeToRun = blockers.length === 0;
  const approvalSummary = buildMorphoApprovalSummary({
    request,
    phase: 'preflight',
    blockers,
  });
  return {
    command: 'preflight-morpho-market',
    safeToRun,
    liveTxAllowed: safeToRun && requestMayExecuteLiveTransactions(request),
    placeholderSafe: placeholderFindings.length === 0,
    requestMayExecuteLiveTransactions: requestMayExecuteLiveTransactions(request),
    approvalSummary,
    blockers: uniqueStrings(blockers),
    warnings: uniqueStrings(warnings),
    nextSteps: safeToRun
      ? [{ type: 'command', command: 'ensure-feeds-and-deploy-morpho-market', message: 'Preflight passed. Run the wrapper with this request when user approval is present.' }]
      : uniqueStrings(blockers).map((blocker) => ({ type: 'blocker', message: blocker })),
  };
}

function explainNextMorphoRun(options = {}) {
  const runDir = getRunDirFromOptions(options);
  const paths = resolveMorphoEnsureDeployPaths({ resumeFromRunDir: runDir });
  const artifacts = loadMorphoRunArtifacts(paths);
  const phase = artifacts.summary?.status?.phase
    || (artifacts.verifyResult ? (artifacts.verifyResult.verified ? 'completed' : 'verification-ready') : null)
    || (artifacts.deployResult ? 'market-deployment-ready' : null)
    || (artifacts.funding ? 'feeds-funded-waiting-propagation' : 'plan-only');
  const blockers = uniqueStrings([
    ...(artifacts.summary?.blockers || []),
    ...(artifacts.propagation?.blockers || []),
    ...(artifacts.deployResult?.blockers || []),
    ...(artifacts.verifyResult?.blockers || []),
  ]);
  const warnings = uniqueStrings([
    ...(artifacts.summary?.warnings || []),
    ...(artifacts.deployResult?.warnings || []),
    ...(artifacts.verifyResult?.warnings || []),
  ]);
  const nextSteps = artifacts.summary?.nextSteps || artifacts.verifyResult?.nextSteps || artifacts.deployResult?.nextSteps || [];
  const agentDecision = buildAgentDecision({
    phase,
    artifactPaths: { runDir, agentDecisionPath: paths.agentDecisionPath },
    blockers,
    warnings,
    nextSteps,
    propagationResult: artifacts.propagation,
    deployResult: artifacts.deployResult,
    verifyResult: artifacts.verifyResult,
    verifySkippedReason: artifacts.summary?.verifySkippedReason || null,
  });

  return {
    currentState: agentDecision.safeStatus,
    blocker: agentDecision.firstBlocker,
    nextCommand: agentDecision.nextCommand,
    liveTxAllowed: agentDecision.liveTxAllowed,
    userApprovalNeeded: agentDecision.requiresUserApproval,
    successClaimAllowed: agentDecision.successClaimAllowed,
    mustNotDo: agentDecision.mustNotDo,
    runDir,
  };
}

function verifyFeedToMarketHandoff(options = {}) {
  const runDir = getRunDirFromOptions(options);
  const paths = resolveMorphoEnsureDeployPaths({ resumeFromRunDir: runDir });
  const artifacts = loadMorphoRunArtifacts(paths);
  const blockers = [];
  const warnings = [];

  if (!artifacts.deployResult) {
    blockers.push('Missing deploy-output.json; cannot prove adapter-to-market handoff.');
  }
  if (!artifacts.verifyResult) {
    blockers.push('Missing verify-output.json; cannot prove market oracle price read.');
  }

  const adapters = artifacts.deployResult?.adapters || [];
  const adapterTransactions = Array.isArray(artifacts.deployResult?.transactionPlan)
    ? artifacts.deployResult.transactionPlan.filter((entry) => entry && entry.kind === 'contract-deployment')
    : [];
  const markets = artifacts.deployResult?.markets || [];
  const verifiedMarkets = artifacts.verifyResult?.markets || [];

  for (const market of markets) {
    const adapter = adapters.find((entry) => entry.marketKey === market.marketKey) || null;
    const adapterTransaction = adapterTransactions.find((entry) => entry.marketKey === market.marketKey)
      || adapterTransactions.find((entry) => entry.deploymentRef && entry.deploymentRef === market.oracle?.deploymentRef)
      || null;
    const adapterAddress = adapter?.deployedAddress
      || adapterTransaction?.deployedAddress
      || artifacts.deployResult?.autoOracleResolution?.byMarketKey?.[market.marketKey]
      || null;
    const marketOracle = market.marketParams?.oracle || market.oracle || null;
    const verified = verifiedMarkets.find((entry) => entry.marketKey === market.marketKey) || null;

    if (!adapter && !adapterTransaction) {
      blockers.push(`No adapter artifact or deployment transaction found for ${market.marketKey}.`);
      continue;
    }
    if (!adapterAddress) {
      blockers.push(`No deployed or predicted adapter address found for ${market.marketKey}.`);
    }
    if (!marketOracle) {
      blockers.push(`No market oracle address found for ${market.marketKey}.`);
    } else if (adapterAddress && marketOracle.toLowerCase() !== adapterAddress.toLowerCase()) {
      blockers.push(`Market oracle for ${market.marketKey} does not equal adapter address from this run.`);
    }
    if (!adapter?.constructorArgs && !adapterTransaction?.data && !adapterTransaction?.payloadRef) {
      blockers.push(`Adapter constructor/source args or deployment calldata are missing for ${market.marketKey}.`);
    }
    if (!verified?.oraclePricePositive) {
      blockers.push(`Verified oracle.price() is missing or non-positive for ${market.marketKey}.`);
    }
  }

  if (markets.length === 0) {
    blockers.push('No deployed market artifacts found.');
  }
  if (artifacts.propagation && artifacts.propagation.ready !== true) {
    blockers.push('Propagation artifact exists but does not prove feed readiness.');
  }
  if (!artifacts.verifyResult?.verified) {
    blockers.push('verifyResult.verified is not true.');
  }

  return {
    command: 'verify-feed-to-market-handoff',
    runDir,
    verified: blockers.length === 0,
    checks: {
      deployArtifactPresent: Boolean(artifacts.deployResult),
      verifyArtifactPresent: Boolean(artifacts.verifyResult),
      allMarketsUseRunAdapter: blockers.every((blocker) => !/does not equal adapter|No adapter artifact|No deployed or predicted adapter|No market oracle/.test(blocker)),
      oraclePriceVerified: Boolean(artifacts.verifyResult?.verified) && verifiedMarkets.every((market) => market.oraclePricePositive === true),
      propagationReadyWhenPresent: !artifacts.propagation || artifacts.propagation.ready === true,
    },
    blockers: uniqueStrings(blockers),
    warnings: uniqueStrings(warnings),
  };
}

function buildFeedFundingPhaseResult(workflow) {
  const entries = Array.isArray(workflow?.feedFunding?.entries) ? workflow.feedFunding.entries : [];
  const browserPlanEntries = entries.filter((entry) => entry && entry.browserPlan);
  const completedExecution = entries.some((entry) => entry && entry.execution && entry.execution.executionSummary?.completed === true);
  const attemptedExecution = entries.some((entry) => entry && entry.execution && !entry.cacheHit);
  const cachedFeedReuse = entries.some((entry) => entry && entry.cacheHit);

  return {
    state: workflow?.feedFunding?.overallState || 'not-needed',
    entryCount: entries.length,
    attemptedExecution,
    completedExecution,
    cachedFeedReuse,
    browserPlanEntries,
  };
}

function makeFundedFeedCacheKey(request, feedName) {
  const chain = request?.chain || {};
  const chainKey = chain.chainId !== undefined && chain.chainId !== null
    ? `chainId:${chain.chainId}`
    : `chain:${String(chain.name || '').trim().toLowerCase()}`;
  return `${chainKey}::${String(feedName || '').trim().toUpperCase()}`;
}

function isFundedFeedEntryReusable(entry) {
  if (!entry) {
    return false;
  }
  if (entry.fundingExecutionState === 'not-needed') {
    return true;
  }

  const summary = entry.execution && entry.execution.executionSummary
    ? entry.execution.executionSummary
    : null;
  if (!summary || summary.completed !== true) {
    return false;
  }

  return summary.reusedFromFundedFeedCache === true || summary.submitted === true;
}

function buildFundedFeedCache(request, feedFunding) {
  const entries = Array.isArray(feedFunding?.entries) ? feedFunding.entries : [];
  const reusableEntries = entries.filter(isFundedFeedEntryReusable);

  return {
    version: 1,
    generatedAt: new Date().toISOString(),
    chain: request?.chain || null,
    entryCount: reusableEntries.length,
    entriesByKey: Object.fromEntries(reusableEntries.map((entry) => [
      makeFundedFeedCacheKey(request, entry.feedName),
      {
        feedName: entry.feedName,
        fundingExecutionState: entry.fundingExecutionState,
        completedExecution: entry.execution && entry.execution.executionSummary
          ? entry.execution.executionSummary.completed === true
          : false,
        selectedExecutionMode: entry.selectedExecutionMode || entry.execution?.selectedExecutionMode || null,
      },
    ])),
  };
}

function writeFundedFeedCacheArtifact(paths, request, feedFunding) {
  const cache = buildFundedFeedCache(request, feedFunding);
  writeMorphoRunArtifact(paths.fundedFeedCachePath, cache);
  return cache;
}

function isWorkflowReadyForMorphoDeployment(workflow) {
  return Array.isArray(workflow?.markets)
    && workflow.markets.length > 0
    && workflow.markets.every((market) => market && market.oracleAdapterPlan && market.oracleAdapterPlan.ready);
}

function shouldAttemptFunding(workflow, request) {
  const requestedMode = request?.feedFunding?.mode || 'classify-only';
  return buildFeedFundingPhaseResult(workflow).state === 'executable' && requestedMode !== 'classify-only';
}

function buildMorphoPropagationTimeoutBlockers({ propagationWaitMs, attempts, lastWorkflow }) {
  const nextCommands = Array.isArray(lastWorkflow?.nextSteps)
    ? lastWorkflow.nextSteps.filter((step) => step && step.command).map((step) => step.command)
    : [];
  const nextCommandHint = nextCommands.length > 0
    ? ` Next likely command after propagation: ${nextCommands[0]}.`
    : '';

  return uniqueStrings([
    ...(lastWorkflow?.blockers || []),
    `Propagation wait stalled in phase propagation-wait after ${attempts} check${attempts === 1 ? '' : 's'} and ${propagationWaitMs}ms. The funded Morpho feeds still did not become readable for deployment.${nextCommandHint} Re-run ensure-feeds-and-deploy-morpho-market with --resume-from-run-dir once the feed is live, or increase --propagation-wait-ms if the network is just slow.`,
  ]);
}

async function waitForMorphoFeedPropagation(request, options = {}) {
  const propagationWaitMs = parsePositiveIntegerOption(options.propagationWaitMs, 30000);
  const propagationPollMs = Math.max(1, parsePositiveIntegerOption(options.propagationPollMs, 5000));
  const startedAt = Date.now();
  let attempts = 0;
  let lastWorkflow = null;

  emitMorphoProgress(options, {
    phase: 'propagation-wait',
    status: 'started',
    message: 'Waiting for funded Morpho feeds to become readable before deployment.',
    waitMs: propagationWaitMs,
  });

  do {
    const attemptStartedAtMs = Date.now();
    lastWorkflow = await buildMorphoWorkflow(request, {
      ...options,
      ignoreFundedFeedCache: true,
    });
    attempts += 1;
    recordMorphoPerf(options, {
      name: 'propagationPollAttempt',
      elapsedMs: Date.now() - attemptStartedAtMs,
      details: {
        attempt: attempts,
      },
    });

    emitMorphoProgress(options, {
      phase: 'propagation-wait',
      status: isWorkflowReadyForMorphoDeployment(lastWorkflow) ? 'completed' : 'heartbeat',
      message: isWorkflowReadyForMorphoDeployment(lastWorkflow)
        ? 'Funded Morpho feeds are now readable; continuing to deployment.'
        : 'Still working: funded Morpho feeds are not readable yet.',
      attempt: attempts,
      elapsedMs: Date.now() - startedAt,
      waitMs: propagationWaitMs,
    });

    if (isWorkflowReadyForMorphoDeployment(lastWorkflow)) {
      recordMorphoPerf(options, {
        name: 'waitForMorphoFeedPropagation',
        elapsedMs: Date.now() - startedAt,
        details: { attempts, state: 'funded-and-live' },
      });
      return {
        state: 'funded-and-live',
        ready: true,
        attempts,
        elapsedMs: Date.now() - startedAt,
        workflow: lastWorkflow,
        blockers: [],
        warnings: [...(lastWorkflow.warnings || [])],
      };
    }

    if (Date.now() - startedAt >= propagationWaitMs) {
      break;
    }

    await sleep(Math.min(propagationPollMs, Math.max(0, propagationWaitMs - (Date.now() - startedAt))));
  } while (Date.now() - startedAt <= propagationWaitMs);

  recordMorphoPerf(options, {
    name: 'waitForMorphoFeedPropagation',
    elapsedMs: Date.now() - startedAt,
    details: { attempts, state: 'timed-out' },
  });
  return {
    state: 'timed-out',
    ready: false,
    attempts,
    elapsedMs: Date.now() - startedAt,
    workflow: lastWorkflow,
    blockers: buildMorphoPropagationTimeoutBlockers({
      propagationWaitMs,
      attempts,
      lastWorkflow,
    }),
    warnings: [...(lastWorkflow?.warnings || [])],
  };
}

async function ensureMorphoFeedsThenRefreshWorkflow(request, options = {}) {
  const classifyOnlyRequest = request.feedFunding
    ? {
        ...request,
        feedFunding: {
          ...request.feedFunding,
          mode: 'classify-only',
        },
      }
    : request;

  emitMorphoProgress(options, {
    phase: 'feed-classification',
    status: 'started',
    message: 'Classifying required Api3 feeds for the requested Morpho route.',
  });

  const initialWorkflow = await buildMorphoWorkflow(classifyOnlyRequest, options);
  const initialFunding = buildFeedFundingPhaseResult(initialWorkflow);

  emitMorphoProgress(options, {
    phase: 'feed-classification',
    status: 'completed',
    message: initialWorkflow.feedReadiness?.ready
      ? 'Required Api3 feeds are already readable for deployment.'
      : 'Feed classification finished; checking whether funding or browser handoff is needed.',
    details: {
      recommendedPathId: initialWorkflow.feedReadiness?.recommendedPathId || null,
      honestStatus: initialWorkflow.honestStatus || null,
    },
  });

  if (isWorkflowReadyForMorphoDeployment(initialWorkflow)) {
    if (initialFunding.cachedFeedReuse) {
      const propagationResult = await waitForMorphoFeedPropagation(classifyOnlyRequest, options);
      return {
        phase: propagationResult.ready ? 'market-deployment-ready' : 'blocked',
        requestForDeployment: request,
        initialWorkflow,
        fundingWorkflow: { feedFunding: initialWorkflow.feedFunding },
        propagationResult,
        finalWorkflow: propagationResult.workflow,
        blockers: propagationResult.ready ? [] : propagationResult.blockers,
        warnings: uniqueStrings([
          ...(initialWorkflow.warnings || []),
          ...(propagationResult.warnings || []),
        ]),
        nextSteps: propagationResult.ready
          ? propagationResult.workflow.nextSteps
          : propagationResult.blockers.map((blocker) => ({ type: 'blocker', message: blocker })),
      };
    }

    return {
      phase: 'market-deployment-ready',
      requestForDeployment: request,
      initialWorkflow,
      fundingWorkflow: null,
      propagationResult: null,
      finalWorkflow: initialWorkflow,
      blockers: [],
      warnings: [...(initialWorkflow.warnings || [])],
      nextSteps: initialWorkflow.nextSteps,
    };
  }

  if (initialFunding.browserPlanEntries.length > 0) {
    emitMorphoProgress(options, {
      phase: 'funding-handoff',
      status: 'blocked',
      message: 'Feed funding requires browser-assisted handoff before Morpho deployment can continue.',
    });
    return {
      phase: 'blocked',
      requestForDeployment: request,
      initialWorkflow,
      fundingWorkflow: null,
      propagationResult: null,
      finalWorkflow: initialWorkflow,
      blockers: uniqueStrings(initialWorkflow.blockers || []),
      warnings: [...(initialWorkflow.warnings || [])],
      nextSteps: initialWorkflow.nextSteps,
    };
  }

  if (shouldAttemptFunding(initialWorkflow, request)) {
    emitMorphoProgress(options, {
      phase: 'funding-execution',
      status: 'started',
      message: 'Starting Morpho feed funding/classification execution.',
    });
    const fundingWorkflow = await buildMorphoWorkflow(request, options);
    const fundingResult = buildFeedFundingPhaseResult(fundingWorkflow);

    emitMorphoProgress(options, {
      phase: 'funding-execution',
      status: fundingResult.completedExecution || isWorkflowReadyForMorphoDeployment(fundingWorkflow) ? 'completed' : 'blocked',
      message: fundingResult.completedExecution
        ? 'Feed funding execution completed; checking propagation/readability next.'
        : isWorkflowReadyForMorphoDeployment(fundingWorkflow)
          ? 'Feed funding execution was unnecessary; deployment path is already ready.'
          : 'Feed funding execution did not complete cleanly.',
    });

    if (isWorkflowReadyForMorphoDeployment(fundingWorkflow) && !fundingResult.attemptedExecution) {
      return {
        phase: 'market-deployment-ready',
        requestForDeployment: request,
        initialWorkflow,
        fundingWorkflow,
        propagationResult: null,
        finalWorkflow: fundingWorkflow,
        blockers: [],
        warnings: uniqueStrings([
          ...(initialWorkflow.warnings || []),
          ...(fundingWorkflow.warnings || []),
        ]),
        nextSteps: fundingWorkflow.nextSteps,
      };
    }

    if (!fundingResult.completedExecution) {
      return {
        phase: 'blocked',
        requestForDeployment: request,
        initialWorkflow,
        fundingWorkflow,
        propagationResult: null,
        finalWorkflow: fundingWorkflow,
        blockers: uniqueStrings(fundingWorkflow.blockers || []),
        warnings: [...(fundingWorkflow.warnings || [])],
        nextSteps: fundingWorkflow.nextSteps,
      };
    }

    if ((request?.feedFunding?.mode || 'classify-only') === 'dry-run') {
      emitMorphoProgress(options, {
        phase: 'propagation-wait',
        status: 'completed',
        message: 'Skipping propagation wait because funding ran in dry-run mode and nothing was broadcast.',
      });
      return {
        phase: 'market-deployment-ready',
        requestForDeployment: request,
        initialWorkflow,
        fundingWorkflow,
        propagationResult: null,
        finalWorkflow: fundingWorkflow,
        blockers: [],
        warnings: uniqueStrings([
          ...(initialWorkflow.warnings || []),
          ...(fundingWorkflow.warnings || []),
          'Skipped live propagation wait because feed funding ran in dry-run mode and no transaction was broadcast.',
        ]),
        nextSteps: fundingWorkflow.nextSteps,
      };
    }

    const propagationResult = await waitForMorphoFeedPropagation(classifyOnlyRequest, options);
    return {
      phase: propagationResult.ready ? 'market-deployment-ready' : 'blocked',
      requestForDeployment: request,
      initialWorkflow,
      fundingWorkflow,
      propagationResult,
      finalWorkflow: propagationResult.workflow,
      blockers: propagationResult.ready ? [] : propagationResult.blockers,
      warnings: uniqueStrings([
        ...(initialWorkflow.warnings || []),
        ...(fundingWorkflow.warnings || []),
        ...(propagationResult.warnings || []),
      ]),
      nextSteps: propagationResult.ready
        ? propagationResult.workflow.nextSteps
        : propagationResult.blockers.map((blocker) => ({ type: 'blocker', message: blocker })),
    };
  }

  emitMorphoProgress(options, {
    phase: initialFunding.state === 'executable' ? 'funding-execution' : 'feed-classification',
    status: initialFunding.state === 'executable' ? 'blocked' : 'completed',
    message: initialFunding.state === 'executable'
      ? 'Feed funding is required before deployment, but execution mode is still classify-only.'
      : 'Feed classification ended in a blocked planning state.',
  });

  return {
    phase: initialFunding.state === 'executable' ? 'funding-required' : 'blocked',
    requestForDeployment: request,
    initialWorkflow,
    fundingWorkflow: null,
    propagationResult: null,
    finalWorkflow: initialWorkflow,
    blockers: uniqueStrings(initialWorkflow.blockers || []),
    warnings: [...(initialWorkflow.warnings || [])],
    nextSteps: initialWorkflow.nextSteps,
  };
}

function collectMorphoFundingRollbackItems(fundingWorkflow) {
  const entries = Array.isArray(fundingWorkflow?.feedFunding?.entries) ? fundingWorkflow.feedFunding.entries : [];

  return entries.flatMap((entry) => {
    const changes = [];
    const executionSummary = entry?.execution?.executionSummary || null;
    if (executionSummary?.txHash) {
      changes.push({
        phase: 'feed-funding',
        kind: 'buy-subscription',
        feedName: entry.feedName,
        txHash: executionSummary.txHash,
        executionMode: entry.execution?.selectedExecutionMode || entry.selectedExecutionMode || null,
        reversibility: 'irreversible-onchain',
        note: 'Api3 feed funding purchases cannot be undone in-place; use the saved run artifacts for audit/resume and treat this as a forward-only chain change.',
      });
    }

    const communalProxyDeployment = entry?.execution?.communalProxyDeployment || null;
    const proxyExecutionSummary = communalProxyDeployment?.executionSummary || null;
    if (proxyExecutionSummary?.txHash) {
      changes.push({
        phase: 'feed-funding',
        kind: 'deploy-communal-proxy',
        feedName: entry.feedName,
        txHash: proxyExecutionSummary.txHash,
        deployedAddress: communalProxyDeployment?.communalProxy || entry?.execution?.communalProxy || null,
        reversibility: 'irreversible-onchain',
        note: 'Deterministic communal proxy deployment is append-only onchain; rollback means stopping further dependent deployment, not deleting the contract.',
      });
    }

    return changes;
  });
}

function collectMorphoDeploymentRollbackItems(deployResult) {
  const transactionPlan = Array.isArray(deployResult?.transactionPlan) ? deployResult.transactionPlan : [];

  return transactionPlan
    .filter((entry) => entry && typeof entry.txHash === 'string' && entry.txHash)
    .map((entry) => ({
      phase: 'market-deployment',
      kind: entry.kind || 'transaction',
      marketKey: entry.marketKey || null,
      txHash: entry.txHash,
      deployedAddress: entry.deployedAddress || null,
      reversibility: 'irreversible-onchain',
      note: entry.kind === 'contract-deployment'
        ? 'Contract deployments and Morpho market creations are not truly rollbackable onchain; compensate by halting follow-on steps and using the recorded addresses/tx hashes for any unwind or replacement plan.'
        : 'This submitted deployment transaction is append-only onchain; treat rollback as a compensating-action exercise rather than a delete.',
    }));
}

function buildMorphoRollbackPlan({ phase, paths, orchestration, deployResult, verifyResult }) {
  const onchainChanges = [
    ...collectMorphoFundingRollbackItems(orchestration?.fundingWorkflow),
    ...collectMorphoDeploymentRollbackItems(deployResult),
  ];

  const localArtifactRollback = [
    {
      kind: 'preserve-run-artifacts',
      path: paths.runDir,
      note: 'Keep the full run directory intact first. It is the canonical audit/resume surface for this Morpho run.',
    },
    {
      kind: 'resume-or-stop',
      path: paths.requestPath,
      note: 'To stop safely, do not send any further dependent transactions. To continue later, resume from the saved run directory instead of reconstructing state manually.',
    },
  ];

  if (onchainChanges.length === 0) {
    localArtifactRollback.push({
      kind: 'discard-local-artifacts-only',
      path: paths.runDir,
      note: 'No submitted onchain transactions were detected in this run summary, so rollback is just local artifact cleanup or restoring a previous request/config state.',
    });
  }

  return {
    phase,
    generatedAt: new Date().toISOString(),
    localArtifactRollback,
    onchainRollbackReality: onchainChanges.length > 0
      ? 'Submitted Morpho/feed-funding transactions are forward-only. This plan records what changed so an operator can halt, audit, and design compensating actions without guessing.'
      : 'No submitted onchain changes were detected; rollback is local-only from this run directory.',
    onchainChanges,
    compensatingActionGuidance: onchainChanges.length > 0
      ? [
          'Stop before sending any further dependent transactions.',
          'Use the recorded tx hashes and deployed addresses to audit exactly what landed.',
          'If the deployment should not continue, treat any unwind as a fresh compensating plan, not a delete/undo operation.',
        ]
      : ['No compensating onchain action is needed unless you intentionally continue this workflow later.'],
    verificationState: verifyResult
      ? {
          attempted: true,
          verified: Boolean(verifyResult.verified),
        }
      : {
          attempted: false,
          verified: false,
        },
  };
}

function buildMorphoRunSummary({ phase, paths, orchestration, deployResult, verifyResult, verifySkippedReason, perfSummary = null }) {
  const finalWorkflow = orchestration?.finalWorkflow || orchestration?.initialWorkflow || null;
  const rollbackPlan = buildMorphoRollbackPlan({ phase, paths, orchestration, deployResult, verifyResult });
  const approvalSummary = buildMorphoApprovalSummary({
    request: orchestration?.requestForDeployment,
    workflow: finalWorkflow,
    phase,
    blockers: [
      ...(orchestration?.blockers || []),
      ...(deployResult?.blockers || []),
      ...(verifyResult?.blockers || []),
    ],
    artifactPaths: {
      runDir: paths.runDir,
      approvalSummaryPath: paths.approvalSummaryPath,
    },
  });

  return {
    status: {
      phase,
      completed: Boolean(verifyResult?.verified || deployResult?.sendSummary?.completed),
      blocked: phase === 'blocked' || phase === 'funding-required',
      deployAttempted: Boolean(deployResult),
      verifyAttempted: Boolean(verifyResult),
    },
    marketCount: finalWorkflow?.prepareMorphoMarket?.marketCount || 0,
    fundingState: finalWorkflow?.feedFunding?.overallState || orchestration?.initialWorkflow?.feedFunding?.overallState || null,
    propagationState: orchestration?.propagationResult?.state || null,
    approvalSummary,
    perfSummary,
    artifactPaths: {
      runDir: paths.runDir,
      requestPath: paths.requestPath,
      initialWorkflowPath: paths.initialWorkflowPath,
      fundingPath: orchestration?.fundingWorkflow ? paths.fundingPath : null,
      fundedFeedCachePath: orchestration?.fundingWorkflow ? paths.fundedFeedCachePath : null,
      propagationPath: orchestration?.propagationResult ? paths.propagationPath : null,
      progressPath: paths.progressPath,
      approvalSummaryPath: paths.approvalSummaryPath,
      perfSummaryPath: paths.perfSummaryPath,
      transactionPayloadsDir: deployResult ? paths.transactionPayloadsDir : null,
      deployOutputPath: deployResult ? paths.deployOutputPath : null,
      verifyOutputPath: verifyResult ? paths.verifyOutputPath : null,
      rollbackPlanPath: paths.rollbackPlanPath,
      agentDecisionPath: paths.agentDecisionPath,
      summaryPath: paths.summaryPath,
    },
    rollbackPlan,
    verifySkippedReason,
    blockers: uniqueStrings([
      ...(orchestration?.blockers || []),
      ...(deployResult?.blockers || []),
      ...(verifyResult?.blockers || []),
    ]),
    warnings: uniqueStrings([
      ...(orchestration?.warnings || []),
      ...(deployResult?.warnings || []),
      ...(verifyResult?.warnings || []),
    ]),
    nextSteps: verifyResult?.nextSteps || deployResult?.nextSteps || orchestration?.nextSteps || [],
  };
}

function deriveSafeStatus({ phase, blockers = [], verifyResult = null, propagationResult = null, deployResult = null }) {
  if (blockers.length > 0 || phase === 'blocked') {
    return 'blocked';
  }
  if (verifyResult?.verified) {
    return 'completed';
  }
  if (phase === 'verification-ready') {
    return 'verification-ready';
  }
  if (phase === 'market-deployment-ready') {
    return deployResult?.sendSummary?.completed ? 'market-created-awaiting-verification' : 'market-deployment-ready';
  }
  if (propagationResult && propagationResult.ready !== true) {
    return 'feeds-funded-waiting-propagation';
  }
  return phase || 'unknown';
}

function buildAgentDecision({ phase, artifactPaths = {}, blockers = [], warnings = [], nextSteps = [], propagationResult = null, deployResult = null, verifyResult = null, verifySkippedReason = null }) {
  const firstBlocker = blockers[0] || null;
  const nextCommand = nextSteps.find((step) => step && step.command)?.command || null;
  const successClaimAllowed = phase === 'completed' && verifyResult?.verified === true && blockers.length === 0;
  const canContinue = blockers.length === 0 && !successClaimAllowed && Boolean(nextCommand || phase === 'market-deployment-ready' || phase === 'verification-ready');
  const mustNotDo = [];

  if (propagationResult && propagationResult.ready !== true) {
    mustNotDo.push('do not deploy market until feed propagation/readability is proven');
  }
  if (verifySkippedReason || !verifyResult?.verified) {
    mustNotDo.push('do not claim Morpho market deployment success without verified oracle.price()');
  }
  if (!deployResult?.sendSummary?.completed && phase !== 'completed') {
    mustNotDo.push('do not claim a live market was created from planning or dry-run artifacts');
  }

  return {
    canContinue,
    safeStatus: deriveSafeStatus({ phase, blockers, verifyResult, propagationResult, deployResult }),
    phase,
    successClaimAllowed,
    nextCommand,
    firstBlocker,
    mustNotDo: uniqueStrings(mustNotDo),
    requiresUserApproval: Boolean(nextCommand && /deploy|send|fund|ensure/i.test(nextCommand)),
    liveTxAllowed: false,
    artifactPaths,
    warnings,
  };
}

function writeAgentDecisionArtifact(paths, result) {
  const agentDecision = buildAgentDecision(result);
  writeMorphoRunArtifact(paths.agentDecisionPath, agentDecision);
  return agentDecision;
}

function loadMorphoRunArtifacts(paths) {
  return {
    request: readJsonFileIfExists(paths.requestPath),
    initialWorkflow: readJsonFileIfExists(paths.initialWorkflowPath),
    funding: readJsonFileIfExists(paths.fundingPath),
    fundedFeedCache: readJsonFileIfExists(paths.fundedFeedCachePath),
    propagation: readJsonFileIfExists(paths.propagationPath),
    approvalSummary: readJsonFileIfExists(paths.approvalSummaryPath),
    perfSummary: readJsonFileIfExists(paths.perfSummaryPath),
    rollbackPlan: readJsonFileIfExists(paths.rollbackPlanPath),
    deployResult: readJsonFileIfExists(paths.deployOutputPath),
    verifyResult: readJsonFileIfExists(paths.verifyOutputPath),
    agentDecision: readJsonFileIfExists(paths.agentDecisionPath),
    summary: readJsonFileIfExists(paths.summaryPath),
  };
}

function requestsCompatibleForResume(activeRequest, resumedRequest) {
  if (!activeRequest || !resumedRequest) {
    return true;
  }

  return makeCanonicalHash(activeRequest) === makeCanonicalHash(resumedRequest);
}

function buildResumedMorphoResult({ phase, paths, initialWorkflow, fundingResult, propagationResult, deployResult, verifyResult, verifySkippedReason, approvalSummary = null, perfSummary = null, rollbackPlan = null, blockers = [], warnings = [], nextSteps = [] }) {
  const agentDecision = buildAgentDecision({
    phase,
    artifactPaths: { runDir: paths.runDir, progressPath: paths.progressPath, approvalSummaryPath: paths.approvalSummaryPath, agentDecisionPath: paths.agentDecisionPath },
    blockers,
    warnings,
    nextSteps,
    propagationResult,
    deployResult,
    verifyResult,
    verifySkippedReason,
  });
  writeMorphoRunArtifact(paths.agentDecisionPath, agentDecision);
  if (approvalSummary) {
    writeMorphoRunArtifact(paths.approvalSummaryPath, approvalSummary);
  }
  if (perfSummary) {
    writeMorphoRunArtifact(paths.perfSummaryPath, perfSummary);
  }

  return {
    phase,
    resumedFromRunDir: true,
    artifactPaths: {
      runDir: paths.runDir,
      requestPath: paths.requestPath,
      initialWorkflowPath: initialWorkflow ? paths.initialWorkflowPath : null,
      fundingPath: fundingResult ? paths.fundingPath : null,
      fundedFeedCachePath: fundingResult ? paths.fundedFeedCachePath : null,
      propagationPath: propagationResult ? paths.propagationPath : null,
      progressPath: paths.progressPath,
      approvalSummaryPath: paths.approvalSummaryPath,
      perfSummaryPath: paths.perfSummaryPath,
      transactionPayloadsDir: deployResult ? paths.transactionPayloadsDir : null,
      deployOutputPath: deployResult ? paths.deployOutputPath : null,
      verifyOutputPath: verifyResult ? paths.verifyOutputPath : null,
      rollbackPlanPath: paths.rollbackPlanPath,
      agentDecisionPath: paths.agentDecisionPath,
      summaryPath: paths.summaryPath,
    },
    approvalSummary,
    perfSummary,
    rollbackPlan,
    initialWorkflow,
    fundingResult,
    propagationResult,
    deployResult,
    verifyResult,
    verifySkippedReason,
    blockers,
    warnings,
    nextSteps,
    status: {
      phase,
      completed: Boolean(verifyResult?.verified || deployResult?.sendSummary?.completed),
      blocked: phase === 'blocked' || phase === 'funding-required',
      deployAttempted: Boolean(deployResult),
      verifyAttempted: Boolean(verifyResult),
    },
    agentDecision,
  };
}

async function ensureFeedsAndDeployMorphoMarket(request, options = {}) {
  validateDeployMorphoMarketRequest(request);
  assertNoUnsafeLivePlaceholders(request);

  const paths = resolveMorphoEnsureDeployPaths(options);
  const progressOptions = withMorphoProgress(options, paths.progressPath);
  const perfOptions = withMorphoPerf(progressOptions, paths.perfSummaryPath);
  const existingArtifacts = loadMorphoRunArtifacts(paths);
  const baseApprovalArtifactPaths = { runDir: paths.runDir, approvalSummaryPath: paths.approvalSummaryPath };

  emitMorphoProgress(perfOptions, {
    phase: 'preflight',
    status: 'started',
    message: options.resumeFromRunDir
      ? 'Validating Morpho request and loading resumable run artifacts.'
      : 'Validating Morpho request and preparing run artifacts.',
  });

  if (options.resumeFromRunDir && existingArtifacts.request && !requestsCompatibleForResume(request, existingArtifacts.request)) {
    emitMorphoProgress(perfOptions, {
      phase: 'preflight',
      status: 'blocked',
      message: 'Resume request does not match the request stored in the run directory.',
    });
    return buildResumedMorphoResult({
      phase: 'blocked',
      paths,
      initialWorkflow: existingArtifacts.initialWorkflow,
      fundingResult: existingArtifacts.funding,
      propagationResult: existingArtifacts.propagation,
      deployResult: existingArtifacts.deployResult,
      verifyResult: existingArtifacts.verifyResult,
      verifySkippedReason: null,
      approvalSummary: existingArtifacts.approvalSummary || buildMorphoApprovalSummary({ request, phase: 'blocked', blockers: ['The provided request does not match the request.json stored in the resume run directory.'], artifactPaths: baseApprovalArtifactPaths }),
      perfSummary: existingArtifacts.perfSummary,
      rollbackPlan: existingArtifacts.rollbackPlan || existingArtifacts.summary?.rollbackPlan || null,
      blockers: ['The provided request does not match the request.json stored in the resume run directory.'],
      warnings: [],
      nextSteps: [
        {
          type: 'blocker',
          message: 'Use the original request.json from the run directory, or start a fresh run without --resume-from-run-dir.',
        },
      ],
    });
  }

  emitMorphoProgress(perfOptions, {
    phase: 'preflight',
    status: 'completed',
    message: options.resumeFromRunDir
      ? 'Resume artifacts loaded; continuing from the stored Morpho run state.'
      : 'Preflight validation passed; continuing into feed classification.',
  });

  if (options.resumeFromRunDir && existingArtifacts.verifyResult) {
    return buildResumedMorphoResult({
      phase: existingArtifacts.verifyResult.verified ? 'completed' : 'verification-ready',
      paths,
      initialWorkflow: existingArtifacts.initialWorkflow,
      fundingResult: existingArtifacts.funding,
      propagationResult: existingArtifacts.propagation,
      deployResult: existingArtifacts.deployResult,
      verifyResult: existingArtifacts.verifyResult,
      verifySkippedReason: null,
      approvalSummary: existingArtifacts.approvalSummary || buildMorphoApprovalSummary({ request, workflow: existingArtifacts.initialWorkflow, phase: existingArtifacts.verifyResult.verified ? 'completed' : 'verification-ready', blockers: uniqueStrings(existingArtifacts.verifyResult.blockers || []), artifactPaths: baseApprovalArtifactPaths }),
      perfSummary: existingArtifacts.perfSummary,
      rollbackPlan: existingArtifacts.rollbackPlan || existingArtifacts.summary?.rollbackPlan || null,
      blockers: uniqueStrings(existingArtifacts.verifyResult.blockers || []),
      warnings: uniqueStrings(existingArtifacts.verifyResult.warnings || []),
      nextSteps: existingArtifacts.verifyResult.nextSteps || [],
    });
  }

  if (options.resumeFromRunDir && existingArtifacts.deployResult) {
    const shouldVerifyResumedDeploy = isCliFlagEnabled(options.verifyAnyway) || existingArtifacts.deployResult.sendSummary?.completed === true;
    if (shouldVerifyResumedDeploy) {
      const verifyRequest = {
        ...request,
        deploymentResult: existingArtifacts.deployResult,
      };
      const verifyResult = await verifyMorphoMarket(verifyRequest, options);
      writeMorphoRunArtifact(paths.verifyOutputPath, verifyResult);

      const resumedSummary = buildMorphoRunSummary({
        phase: verifyResult.verified ? 'completed' : 'verification-ready',
        paths,
        orchestration: {
          initialWorkflow: existingArtifacts.initialWorkflow,
          fundingWorkflow: existingArtifacts.funding ? { feedFunding: existingArtifacts.funding } : null,
          propagationResult: existingArtifacts.propagation,
          blockers: [],
          warnings: [],
          nextSteps: verifyResult.nextSteps || [],
        },
        deployResult: existingArtifacts.deployResult,
        verifyResult,
        verifySkippedReason: null,
        perfSummary: buildMorphoPerfSummary(perfOptions),
      });
      writeMorphoRunArtifact(paths.approvalSummaryPath, resumedSummary.approvalSummary);
      writeMorphoRunArtifact(paths.perfSummaryPath, resumedSummary.perfSummary);
      writeMorphoRunArtifact(paths.rollbackPlanPath, resumedSummary.rollbackPlan);
      writeMorphoRunArtifact(paths.summaryPath, resumedSummary);

      return buildResumedMorphoResult({
        phase: verifyResult.verified ? 'completed' : 'verification-ready',
        paths,
        initialWorkflow: existingArtifacts.initialWorkflow,
        fundingResult: existingArtifacts.funding,
        propagationResult: existingArtifacts.propagation,
        deployResult: existingArtifacts.deployResult,
        verifyResult,
        verifySkippedReason: null,
        approvalSummary: resumedSummary.approvalSummary,
        perfSummary: resumedSummary.perfSummary,
        rollbackPlan: resumedSummary.rollbackPlan,
        blockers: resumedSummary.blockers,
        warnings: resumedSummary.warnings,
        nextSteps: resumedSummary.nextSteps,
      });
    }

    return buildResumedMorphoResult({
      phase: 'market-deployment-ready',
      paths,
      initialWorkflow: existingArtifacts.initialWorkflow,
      fundingResult: existingArtifacts.funding,
      propagationResult: existingArtifacts.propagation,
      deployResult: existingArtifacts.deployResult,
      verifyResult: null,
      verifySkippedReason: 'Verification skipped while resuming because the stored deploy output did not complete a live send. Pass --verify-anyway to force verification from the stored artifact.',
      approvalSummary: existingArtifacts.approvalSummary || buildMorphoApprovalSummary({ request, workflow: existingArtifacts.initialWorkflow, phase: 'market-deployment-ready', blockers: uniqueStrings(existingArtifacts.deployResult.blockers || []), artifactPaths: baseApprovalArtifactPaths }),
      perfSummary: existingArtifacts.perfSummary,
      rollbackPlan: existingArtifacts.rollbackPlan || existingArtifacts.summary?.rollbackPlan || null,
      blockers: uniqueStrings(existingArtifacts.deployResult.blockers || []),
      warnings: uniqueStrings(existingArtifacts.deployResult.warnings || []),
      nextSteps: existingArtifacts.deployResult.nextSteps || [],
    });
  }
  if (options.resumeFromRunDir && existingArtifacts.funding && buildFeedFundingPhaseResult({ feedFunding: existingArtifacts.funding }).completedExecution) {
    const fundedFeedCache = existingArtifacts.fundedFeedCache || writeFundedFeedCacheArtifact(paths, request, existingArtifacts.funding);
    const propagationResult = await waitForMorphoFeedPropagation(request, perfOptions);
    const orchestration = {
      requestForDeployment: request,
      initialWorkflow: existingArtifacts.initialWorkflow || propagationResult.workflow,
      fundingWorkflow: { feedFunding: existingArtifacts.funding, fundedFeedCache },
      propagationResult,
      finalWorkflow: propagationResult.workflow,
      blockers: propagationResult.ready ? [] : propagationResult.blockers,
      warnings: propagationResult.warnings || [],
      nextSteps: propagationResult.ready
        ? propagationResult.workflow.nextSteps
        : propagationResult.blockers.map((blocker) => ({ type: 'blocker', message: blocker })),
    };

    let deployResult = null;
    let verifyResult = null;
    let verifySkippedReason = null;
    let phase = propagationResult.ready ? 'market-deployment-ready' : 'blocked';

    if (propagationResult.ready) {
      const wrapperResult = await deployAndVerifyMorphoMarket(request, {
        ...perfOptions,
        precomputedWorkflow: orchestration.finalWorkflow,
        runDir: paths.runDir,
        deployOutputFile: paths.deployOutputPath,
        verifyOutputFile: paths.verifyOutputPath,
      });
      deployResult = wrapperResult.deployResult;
      verifyResult = wrapperResult.verifyResult;
      verifySkippedReason = wrapperResult.verifySkippedReason;

      if (verifyResult?.verified) {
        phase = 'completed';
      } else if (deployResult?.ready) {
        phase = verifyResult ? 'verification-ready' : 'market-deployment-ready';
      } else {
        phase = 'blocked';
      }
    }

    const resumedSummary = buildMorphoRunSummary({
      phase,
      paths,
      orchestration,
      deployResult,
      verifyResult,
      verifySkippedReason,
      perfSummary: buildMorphoPerfSummary(perfOptions),
    });
    writeMorphoRunArtifact(paths.propagationPath, propagationResult);
    writeMorphoRunArtifact(paths.approvalSummaryPath, resumedSummary.approvalSummary);
    writeMorphoRunArtifact(paths.perfSummaryPath, resumedSummary.perfSummary);
    writeMorphoRunArtifact(paths.rollbackPlanPath, resumedSummary.rollbackPlan);
    writeMorphoRunArtifact(paths.summaryPath, resumedSummary);

    return buildResumedMorphoResult({
      phase,
      paths,
      initialWorkflow: orchestration.initialWorkflow,
      fundingResult: existingArtifacts.funding,
      propagationResult,
      deployResult,
      verifyResult,
      verifySkippedReason,
      approvalSummary: resumedSummary.approvalSummary,
      perfSummary: resumedSummary.perfSummary,
      rollbackPlan: resumedSummary.rollbackPlan,
      blockers: resumedSummary.blockers,
      warnings: resumedSummary.warnings,
      nextSteps: resumedSummary.nextSteps,
    });
  }


  writeMorphoRunArtifact(paths.requestPath, request);
  writeMorphoRunArtifact(paths.approvalSummaryPath, buildMorphoApprovalSummary({
    request,
    phase: 'preflight',
    artifactPaths: baseApprovalArtifactPaths,
  }));

  const orchestration = await ensureMorphoFeedsThenRefreshWorkflow(request, perfOptions);
  writeMorphoRunArtifact(paths.initialWorkflowPath, orchestration.initialWorkflow);
  if (orchestration.fundingWorkflow) {
    writeMorphoRunArtifact(paths.fundingPath, orchestration.fundingWorkflow.feedFunding);
    writeFundedFeedCacheArtifact(paths, request, orchestration.fundingWorkflow.feedFunding);
  }
  if (orchestration.propagationResult) {
    writeMorphoRunArtifact(paths.propagationPath, orchestration.propagationResult);
  }
  writeMorphoRunArtifact(paths.approvalSummaryPath, buildMorphoApprovalSummary({
    request,
    workflow: orchestration.finalWorkflow || orchestration.initialWorkflow,
    phase: orchestration.phase,
    blockers: orchestration.blockers,
    artifactPaths: baseApprovalArtifactPaths,
  }));

  let deployResult = null;
  let verifyResult = null;
  let verifySkippedReason = null;
  let phase = orchestration.phase;

  if (orchestration.phase === 'market-deployment-ready') {
    const wrapperResult = await deployAndVerifyMorphoMarket(orchestration.requestForDeployment, {
      ...perfOptions,
      precomputedWorkflow: orchestration.finalWorkflow,
      runDir: paths.runDir,
      deployOutputFile: paths.deployOutputPath,
      verifyOutputFile: paths.verifyOutputPath,
    });
    deployResult = wrapperResult.deployResult;
    verifyResult = wrapperResult.verifyResult;
    verifySkippedReason = wrapperResult.verifySkippedReason;

    if (verifyResult?.verified) {
      phase = 'completed';
    } else if (deployResult?.ready) {
      phase = verifyResult ? 'verification-ready' : 'market-deployment-ready';
    } else {
      phase = 'blocked';
    }
  }

  const summary = buildMorphoRunSummary({
    phase,
    paths,
    orchestration,
    deployResult,
    verifyResult,
    verifySkippedReason,
    perfSummary: buildMorphoPerfSummary(perfOptions),
  });
  writeMorphoRunArtifact(paths.approvalSummaryPath, summary.approvalSummary);
  writeMorphoRunArtifact(paths.perfSummaryPath, summary.perfSummary);
  writeMorphoRunArtifact(paths.rollbackPlanPath, summary.rollbackPlan);
  writeMorphoRunArtifact(paths.summaryPath, summary);
  const result = {
    phase,
    artifactPaths: summary.artifactPaths,
    rollbackPlan: summary.rollbackPlan,
    approvalSummary: summary.approvalSummary,
    perfSummary: summary.perfSummary,
    initialWorkflow: orchestration.initialWorkflow,
    fundingResult: orchestration.fundingWorkflow ? {
      ...orchestration.fundingWorkflow.feedFunding,
      ...buildFeedFundingPhaseResult(orchestration.fundingWorkflow),
    } : null,
    propagationResult: orchestration.propagationResult,
    deployResult,
    verifyResult,
    verifySkippedReason,
    blockers: summary.blockers,
    warnings: summary.warnings,
    nextSteps: summary.nextSteps,
    status: summary.status,
  };
  const agentDecision = writeAgentDecisionArtifact(paths, result);

  emitMorphoProgress(perfOptions, {
    phase: phase === 'completed' ? 'verification' : phase === 'blocked' ? 'preflight' : 'market-deployment',
    status: phase === 'blocked' ? 'blocked' : 'completed',
    message: phase === 'completed'
      ? 'Morpho wrapper finished with verified completion.'
      : phase === 'blocked'
        ? 'Morpho wrapper stopped with blockers. Check summary.json and agent-decision.json for the next action.'
        : `Morpho wrapper finished in phase ${phase}.`,
  });

  return {
    ...result,
    artifactPaths: {
      ...result.artifactPaths,
      agentDecisionPath: paths.agentDecisionPath,
    },
    agentDecision,
  };
}

async function deployAndVerifyMorphoMarket(request, options = {}) {
  validateDeployMorphoMarketRequest(request);
  assertNoUnsafeLivePlaceholders(request);

  const { deploymentResult: ignoredDeploymentResult, ...deployRequest } = request;
  const paths = resolveMorphoWrapperPaths(options);
  const wrapperWarnings = [];

  if (ignoredDeploymentResult !== undefined) {
    wrapperWarnings.push('Ignored request.deploymentResult because deploy-and-verify-morpho-market always uses the fresh deploy output it just wrote.');
  }

  emitMorphoProgress(options, {
    phase: 'adapter-deployment',
    status: 'started',
    message: 'Preparing Morpho adapter deployment transactions.',
  });

  const deployResult = await deployMorphoMarket(deployRequest, options);
  writeJsonFile(paths.deployOutputPath, {
    ...deployResult,
    transactionPlan: externalizeMorphoTransactionPayloads(deployResult.transactionPlan, paths.transactionPayloadsDir),
  });

  emitMorphoProgress(options, {
    phase: 'market-deployment',
    status: deployResult.ready ? 'completed' : 'blocked',
    message: deployResult.ready
      ? 'Morpho deployment planning/execution finished; deciding whether verification can run.'
      : 'Morpho deployment stopped before verification because deployment is not ready.',
  });

  const shouldVerify = isCliFlagEnabled(options.verifyAnyway) || deployResult.sendSummary?.completed === true;
  let verifyResult = null;
  let verifySkippedReason = null;

  if (shouldVerify) {
    emitMorphoProgress(options, {
      phase: 'verification',
      status: 'started',
      message: 'Starting on-chain Morpho verification.',
    });
    const verifyRequest = {
      ...deployRequest,
      deploymentResult: readJsonFile(paths.deployOutputPath),
    };
    verifyResult = await verifyMorphoMarket(verifyRequest, options);
    writeJsonFile(paths.verifyOutputPath, verifyResult);
    emitMorphoProgress(options, {
      phase: 'verification',
      status: verifyResult.verified ? 'completed' : 'blocked',
      message: verifyResult.verified
        ? 'Morpho verification succeeded.'
        : 'Morpho verification completed with blockers.',
    });
  } else {
    verifySkippedReason = 'Verification skipped because deploy-morpho-market did not complete a live send. Pass --verify-anyway to force verification using the written deployment result.';
    wrapperWarnings.push(verifySkippedReason);
    emitMorphoProgress(options, {
      phase: 'verification',
      status: 'blocked',
      message: verifySkippedReason,
    });
  }

  return {
    status: {
      deployReady: deployResult.ready,
      deployCompleted: deployResult.sendSummary?.completed === true,
      verifyAttempted: Boolean(verifyResult),
      verifySkipped: !verifyResult,
      verified: verifyResult ? verifyResult.verified === true : false,
    },
    artifactPaths: {
      runDir: paths.runDir,
      transactionPayloadsDir: paths.transactionPayloadsDir,
      deployOutputPath: paths.deployOutputPath,
      verifyOutputPath: verifyResult ? paths.verifyOutputPath : null,
    },
    verifySkippedReason,
    deployResult,
    verifyResult,
    warnings: uniqueStrings([
      ...wrapperWarnings,
      ...(deployResult.warnings || []),
      ...(verifyResult?.warnings || []),
    ]),
    blockers: uniqueStrings([
      ...(deployResult.blockers || []),
      ...(verifyResult?.blockers || []),
    ]),
  };
}

async function runCli(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  const command = args._[0];

  if (!command || command === 'help' || args.help) {
    printUsage();
    return;
  }

  if (!['run-workflow', 'prepare-morpho-market', 'deploy-morpho-oracle-adapter', 'deploy-morpho-market', 'verify-morpho-market', 'deploy-and-verify-morpho-market', 'ensure-feeds-and-deploy-morpho-market', 'preflight-morpho-market', 'explain-next', 'verify-feed-to-market-handoff'].includes(command)) {
    throw new Error(`Unsupported command: ${command}`);
  }

  const request = ['explain-next', 'verify-feed-to-market-handoff'].includes(command) ? null : loadInput(args);
  let result;

  if (command === 'preflight-morpho-market') {
    result = await preflightMorphoMarketRequest(request, args);
  } else if (command === 'explain-next') {
    result = explainNextMorphoRun(args);
  } else if (command === 'verify-feed-to-market-handoff') {
    result = verifyFeedToMarketHandoff(args);
  } else if (command === 'prepare-morpho-market') {
    result = await prepareMorphoMarket(request, args);
  } else if (command === 'deploy-morpho-oracle-adapter') {
    result = await deployMorphoOracleAdapter(request, args);
  } else if (command === 'deploy-morpho-market') {
    result = await deployMorphoMarket(request, args);
  } else if (command === 'verify-morpho-market') {
    result = await verifyMorphoMarket(request, args);
  } else if (command === 'deploy-and-verify-morpho-market') {
    result = await deployAndVerifyMorphoMarket(request, args);
  } else if (command === 'ensure-feeds-and-deploy-morpho-market') {
    result = await ensureFeedsAndDeployMorphoMarket(request, args);
  } else {
    result = await runMorphoWorkflow(request, args);
  }

  outputResult(result, args);
}

module.exports = {
  buildCompositeRequiredFeeds,
  buildMorphoOracleAdapterPlan,
  deployAndVerifyMorphoMarket,
  ensureFeedsAndDeployMorphoMarket,
  explainNextMorphoRun,
  deployMorphoOracleAdapter,
  deployMorphoMarket,
  prepareMorphoMarket,
  preflightMorphoMarketRequest,
  printUsage,
  runCli,
  runMorphoWorkflow,
  verifyFeedToMarketHandoff,
  verifyMorphoMarket,
  validateDeployMorphoMarketRequest,
  validatePrepareMorphoMarketRequest,
  validateRunMorphoWorkflowRequest,
  validateVerifyMorphoMarketRequest,
};
