const fs = require('fs');
const path = require('path');
const util = require('util');
const { getGepAssetsDir } = require('./paths');
const { computeAssetId } = require('./contentHash');
const { sanitizePayload, redactString, fullLeakCheck } = require('./sanitize');

const REUSE_CONTRACT = 'reuse.v1';
const PUBLISH_CONTRACT = 'publish.v1';
const REVERSIBILITY = 'irreversible';
const DRY_RUN_NODE_ID = 'node_000000000000';
const MAX_ASSETS = 50;
const ASSET_FLAGS = new Set(['--asset', '--gene', '--capsule', '--event']);
const ASSET_FLAG_LIST = Array.from(ASSET_FLAGS);
const MACHINE_JSON_STDOUT_WRITE = Symbol('machineJsonStdoutWrite');
const NODE_SCOPED_ENDPOINT_PATHS = new Set(['/a2a/fetch', '/a2a/validate', '/a2a/publish']);
const REUSE_FAILURE_REASONS = new Set([
  'missing_id',
  'cli_unavailable',
  'auth_required',
  'not_found',
  'network_error',
  'unsupported',
  'internal_error',
]);
const PUBLISH_FAILURE_REASONS = new Set([
  'redaction_unavailable',
  'leak_detected',
  'schema_invalid',
  'bundle_required',
  'quality_gate_failed',
  'auth_required',
  'insufficient_credits',
  'network_error',
  'unsupported',
  'cli_unavailable',
  'internal_error',
]);
const HUB_METADATA_KEYS = new Set([
  'credit_cost',
  'gdi_score',
  'success_rate',
  'reuse_count',
  'ranking_score',
  'source_node_id',
  'fetched_at',
  'receipt',
  'hub_receipt',
  'already_purchased',
  '_semantic_similarity',
  'semantic_similarity',
  '_search_score',
  'search_score',
  '_match_score',
  'match_score',
  '_retrieval_rank',
  'retrieval_rank',
]);

async function runReuseCommand(args, deps) {
  deps = deps || {};
  const out = deps.out || process.stdout;
  const parsed = parseReuseArgs(args || []);
  const machineJson = parsed.jsonOut || out === process.stdout;
  const write = (value, code) => writeJson(out, value, code, deps, machineJson);
  if (!parsed.ok) return write(reuseFailure(parsed.reason, parsed.message), 1);
  return withMachineJsonConsole(machineJson, deps, async () => {
    try {
      const asset = deps.fetchAssetById
        ? await deps.fetchAssetById(parsed.assetId)
        : await fetchAssetById(parsed.assetId, deps);
      if (!asset) return write(reuseFailure('not_found', 'asset not found'), 1);
      const cleaned = stripHubMetadata(asset);
      const verifiedId = verifyReuseAssetId(cleaned, parsed.assetId);
      if (!verifiedId.ok) {
        return write(reuseFailure('internal_error', 'asset integrity verification failed'), 1);
      }
      if (!isReuseAssetStoreStable(cleaned)) {
        return write(reuseFailure('internal_error', 'asset integrity verification failed'), 1);
      }
      const store = prepareReuseAssetStore(cleaned, deps);
      const provenance = prepareHubProvenance(deps);
      markHubProvenance(parsed.assetId, deps, provenance);
      let storedId;
      try {
        storedId = storeReusedAsset(cleaned, deps, store);
        if (storedId !== parsed.assetId) {
          throw new ContractError('internal_error', 'asset integrity verification failed');
        }
      } catch (e) {
        rollbackHubProvenance(provenance);
        throw e;
      }
      return write({
        ok: true,
        contract: REUSE_CONTRACT,
        status: 'ok',
        asset_id: storedId,
        action: 'reused',
      }, 0);
    } catch (e) {
      const f = classifyError(e, 'reuse');
      return write(reuseFailure(f.reason, f.message), 1);
    }
  });
}

async function runPublishCommand(args, deps) {
  deps = deps || {};
  const out = deps.out || process.stdout;
  const parsed = parsePublishArgs(args || []);
  const machineJson = parsed.jsonOut || out === process.stdout;
  const write = (value, code) => writeJson(out, value, code, deps, machineJson);
  if (!parsed.ok) return write(publishFailure(parsed.reason, parsed.message, { retryable: false }), 1);
  return withMachineJsonConsole(machineJson, deps, async () => {
    try {
      const bundle = buildPublishBundle(parsed.assetRefs, Object.assign({}, deps, { noAssetStoreInit: parsed.dryRun }));
      if (!bundle.ok) {
        return write(publishFailure(bundle.reason, bundle.message, { retryable: false, gates: bundle.gates }), 1);
      }
      const initialBlocked = writeBlockedPublishResult(bundle, parsed, write);
      if (initialBlocked !== null) return initialBlocked;

      const message = buildPublishMessage(bundle.sanitized, deps, { preview: parsed.dryRun });
      syncBundleFromPublishMessage(bundle, message, deps);
      const finalBlocked = writeBlockedPublishResult(bundle, parsed, write);
      if (finalBlocked !== null) return finalBlocked;
      if (parsed.dryRun) {
        const validation = await postValidate(message, deps);
        const credits = extractCredits(validation.body);
        if (!validation.ok) {
          const reason = publishReasonFromResponse(validation.status, validation.body, validation.reason);
          if (reason === 'quality_gate_failed') {
            bundle.gates.quality = 'fail';
            if (!bundle.blockReasons.includes('quality_gate_failed')) {
              bundle.blockReasons.push('quality_gate_failed');
            }
            return write(dryRunEnvelope(bundle, credits), 0);
          }
          return write(publishFailure(reason, publishReasonMessage(reason), {
            retryable: publishRetryable(reason),
            mode: 'dry_run',
            gates: bundle.gates,
            assets: bundle.assets,
            credits,
          }), 1);
        }
        return write(dryRunEnvelope(bundle, credits), 0);
      }

      const validation = await postValidate(message, deps);
      if (!validation.ok) {
        const reason = publishReasonFromResponse(validation.status, validation.body, validation.reason);
        return write(publishFailure(reason, publishReasonMessage(reason), {
          retryable: publishRetryable(reason),
          mode: 'publish',
          gates: Object.assign({}, bundle.gates, { quality: 'fail' }),
          assets: bundle.assets,
          credits: extractCredits(validation.body),
        }), 1);
      }

      const published = await postPublish(message, deps);
      if (!published.ok) {
        const reason = publishReasonFromResponse(published.status, published.body, published.reason);
        return write(publishFailure(reason, publishReasonMessage(reason), {
          retryable: publishRetryable(reason),
          mode: 'publish',
          gates: bundle.gates,
          assets: bundle.assets,
          credits: extractCredits(published.body),
        }), 1);
      }
      const decision = publishDecision(published.body);
      if (decision === 'quarantine') {
        return write(publishFailure('quality_gate_failed', publishReasonMessage('quality_gate_failed'), {
          retryable: false,
          mode: 'publish',
          gates: Object.assign({}, bundle.gates, { quality: 'fail' }),
          assets: bundle.assets,
          credits: extractCredits(published.body),
        }), 1);
      }
      const body = record(published.body) || {};
      const payload = record(body.payload) || body;
      const status = normalizePublishStatus(published.body);
      const receiptId = stringField(payload, 'receipt_id');
      const bundleId = stringField(payload, 'bundle_id');
      const credits = extractCredits(published.body) || creditsFromPayload(payload);
      if (!status) {
        return write(publishFailure('internal_error', 'Hub publish response missing lifecycle status', {
          retryable: false,
          mode: 'publish',
          gates: bundle.gates,
          assets: bundle.assets,
          credits,
        }), 1);
      }
      return write({
        ok: true,
        contract: PUBLISH_CONTRACT,
        mode: 'publish',
        ...(status ? { status } : {}),
        reversibility: REVERSIBILITY,
        ...(receiptId ? { receipt_id: receiptId } : {}),
        ...(bundleId ? { bundle_id: bundleId } : {}),
        assets: bundle.assets,
        ...(credits ? { credits } : {}),
      }, 0);
    } catch (e) {
      const f = classifyError(e, 'publish');
      return write(publishFailure(f.reason, f.message, {
        retryable: f.retryable,
        mode: parsed.dryRun ? 'dry_run' : 'publish',
      }), 1);
    }
  });
}

function parseReuseArgs(args) {
  let id = null;
  let jsonOut = false;
  for (let i = 0; i < args.length; i++) {
    const token = args[i];
    if (!token) continue;
    if (token === '--json') { jsonOut = true; continue; }
    if (token === '--id') {
      const next = args[i + 1];
      if (!next || String(next).startsWith('--')) return { ok: false, reason: 'missing_id', message: 'reuse requires --id <asset_id>' };
      id = String(next).trim();
      i++;
      continue;
    }
    if (typeof token === 'string' && token.startsWith('--id=')) {
      id = token.slice('--id='.length).trim();
      continue;
    }
    if (String(token).startsWith('--')) return { ok: false, reason: 'unsupported', message: 'unsupported reuse flag' };
    return { ok: false, reason: 'unsupported', message: 'unsupported reuse argument' };
  }
  if (!jsonOut) return { ok: false, reason: 'unsupported', message: 'reuse requires --json' };
  if (!id) return { ok: false, reason: 'missing_id', message: 'reuse requires --id <asset_id>' };
  if (id.length > 200) return { ok: false, reason: 'missing_id', message: 'asset id must be <= 200 characters' };
  return { ok: true, assetId: id, jsonOut };
}

function parsePublishArgs(args) {
  const assetRefs = [];
  let dryRun = false;
  let jsonOut = false;
  for (let i = 0; i < args.length; i++) {
    const token = args[i];
    if (!token) continue;
    if (token === '--dry-run') { dryRun = true; continue; }
    if (token === '--json') { jsonOut = true; continue; }
    const equalFlag = ASSET_FLAG_LIST.find(flag => token.startsWith(flag + '='));
    if (equalFlag) {
      const value = token.slice(equalFlag.length + 1).trim();
      if (!value) return { ok: false, reason: 'bundle_required', message: equalFlag + ' requires a value' };
      assetRefs.push(value);
      continue;
    }
    if (ASSET_FLAGS.has(token)) {
      const next = args[i + 1];
      if (!next || String(next).startsWith('--')) return { ok: false, reason: 'bundle_required', message: token + ' requires a value' };
      assetRefs.push(String(next).trim());
      i++;
      continue;
    }
    if (!String(token).startsWith('--')) return { ok: false, reason: 'unsupported', message: 'unsupported publish argument' };
    return { ok: false, reason: 'unsupported', message: 'unsupported publish flag' };
  }
  if (!jsonOut) return { ok: false, reason: 'unsupported', message: 'publish requires --json' };
  const refs = assetRefs.filter(Boolean);
  if (refs.length === 0) return { ok: false, reason: 'bundle_required', message: 'publish requires --asset <id|path>' };
  if (refs.length > MAX_ASSETS) return { ok: false, reason: 'bundle_required', message: 'publish supports at most ' + MAX_ASSETS + ' assets' };
  return { ok: true, assetRefs: refs, dryRun, jsonOut };
}

function writeBlockedPublishResult(bundle, parsed, write) {
  if (!bundle.blockReasons || bundle.blockReasons.length === 0) return null;
  if (parsed.dryRun) return write(dryRunEnvelope(bundle), 0);
  const reason = bundle.blockReasons[0] || 'internal_error';
  return write(publishFailure(reason, publishReasonMessage(reason), {
    retryable: false,
    mode: 'publish',
    gates: bundle.gates,
    assets: bundle.assets,
  }), 1);
}

function buildPublishBundle(refs, deps) {
  let original;
  try {
    original = loadAssetRefs(refs, deps);
  } catch (e) {
    return { ok: false, reason: 'schema_invalid', message: 'asset schema is invalid', gates: { schema: 'fail' } };
  }
  const bundleCheck = checkBundle(original);
  if (!bundleCheck.ok) return { ok: false, reason: 'bundle_required', message: bundleCheck.message, gates: { schema: 'pass', bundle: 'fail' } };
  let sanitized;
  try {
    sanitized = original.map(asset => {
      const clean = sanitizeForContract(asset, deps);
      clean.asset_id = computeAssetId(clean);
      return clean;
    });
  } catch (_) {
    return { ok: false, reason: 'redaction_unavailable', message: 'redaction unavailable', gates: { redaction: 'unavailable' } };
  }
  const leak = leakCheck(sanitized);
  const blockReasons = leak.blocked ? ['leak_detected'] : [];
  const gates = {
    redaction: 'pass',
    leak: leak.blocked ? 'fail' : 'pass',
    schema: 'pass',
    bundle: 'pass',
    quality: 'pass',
  };
  return {
    ok: true,
    original,
    sanitized,
    blockReasons,
    gates,
    assets: summarizePublishAssets(sanitized),
  };
}

function buildPublishMessage(sanitized, deps, opts) {
  const initialAssets = sanitizePublishAssets(sanitized, deps);
  const message = buildPublishMessageFromAssets(initialAssets, deps, opts);
  return finalizePublishMessage(message, deps, opts);
}

function buildPublishMessageFromAssets(assets, deps, opts) {
  const preview = Boolean(opts && opts.preview);
  const a2a = deps.a2a || require('./a2aProtocol');
  const gene = assets.find(asset => asset.type === 'Gene');
  const capsule = assets.find(asset => asset.type === 'Capsule');
  const event = assets.find(asset => asset.type === 'EvolutionEvent') || null;
  if (!gene || !capsule) throw new ContractError('bundle_required', 'publish requires Gene + Capsule bundle');
  if (preview) {
    const previewNodeId = nonPersistedNodeId(deps) || DRY_RUN_NODE_ID;
    try {
      return a2a.buildPublishBundle({ gene, capsule, event, nodeId: previewNodeId });
    } catch (e) {
      if (!isPublishSigningAuthError(e)) throw e;
      if (!hasHubAuthorization(deps)) throw new ContractError('auth_required', 'Hub authentication required');
      return buildUnsignedPublishPreviewMessage({ gene, capsule, event, nodeId: previewNodeId });
    }
  }
  if (!getHubUrl(deps)) throw new ContractError('auth_required', 'Hub URL is required');
  if (!hasHubAuthorization(deps)) throw new ContractError('auth_required', 'Hub authentication required');
  try {
    return a2a.buildPublishBundle({ gene, capsule, event });
  } catch (e) {
    if (!isPublishSigningAuthError(e)) throw e;
    return buildUnsignedPublishPreviewMessage({ gene, capsule, event, nodeId: nonPersistedNodeId(deps) || DRY_RUN_NODE_ID });
  }
}

function finalizePublishMessage(message, deps, opts) {
  const signedAssets = publishPayloadAssets(message);
  const finalAssets = sanitizePublishAssets(signedAssets, deps);
  if (sameJson(finalAssets, signedAssets)) return message;
  const resigned = buildPublishMessageFromAssets(finalAssets, deps, opts);
  const resignedAssets = publishPayloadAssets(resigned);
  const finalResignedAssets = sanitizePublishAssets(resignedAssets, deps);
  if (!sameJson(finalResignedAssets, resignedAssets)) {
    throw new ContractError('redaction_unavailable', 'redaction unavailable');
  }
  return resigned;
}

function buildUnsignedPublishPreviewMessage(opts) {
  const assets = [opts.gene, opts.capsule]
    .concat(opts.event ? [opts.event] : [])
    .filter(Boolean)
    .map(asset => {
      const copy = cloneJson(asset);
      copy.asset_id = computeAssetId(copy);
      return copy;
    });
  return {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'publish',
    message_id: 'msg_preview_' + Date.now(),
    sender_id: opts.nodeId || DRY_RUN_NODE_ID,
    timestamp: new Date().toISOString(),
    payload: { assets },
  };
}

function nonPersistedNodeId(deps) {
  if (deps && typeof deps.nodeId === 'string' && deps.nodeId.trim()) return deps.nodeId.trim();
  if (process.env.A2A_NODE_ID && String(process.env.A2A_NODE_ID).trim()) {
    return String(process.env.A2A_NODE_ID).trim();
  }
  const homeNodeId = readNodeIdFile(path.join(process.env.EVOLVER_HOME || path.join(osHomedir(), '.evomap'), 'node_id'));
  if (homeNodeId) return homeNodeId;
  return readNodeIdFile(path.resolve(__dirname, '..', '..', '.evomap_node_id'));
}

function readNodeIdFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) return '';
    return fs.readFileSync(filePath, 'utf8').trim();
  } catch (_) {
    return '';
  }
}

function osHomedir() {
  try { return require('os').homedir(); } catch (_) { return ''; }
}

function isPublishSigningAuthError(error) {
  const msg = String(error && error.message || error || '');
  return /node_secret|signing|authentication required|Hub URL is required/i.test(msg);
}

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value));
}

function loadAssetRef(ref, deps) {
  if (looksLikeFile(ref)) return normalizeAsset(JSON.parse(fs.readFileSync(path.resolve(ref), 'utf8')));
  const all = deps.noAssetStoreInit && !deps.assetStore
    ? loadLocalAssetsReadOnly(deps)
    : loadLocalAssetsFromStore(deps);
  const found = all.find(asset => asset && (asset.asset_id === ref || asset.id === ref));
  if (!found) throw new ContractError('schema_invalid', 'asset not found: ' + ref);
  return normalizeAsset(found);
}

function loadAssetRefs(refs, deps) {
  const all = needsLocalAssetLookup(refs)
    ? (deps.noAssetStoreInit && !deps.assetStore ? loadLocalAssetsReadOnly(deps) : loadLocalAssetsFromStore(deps))
    : [];
  return refs.map(ref => loadAssetRefFromLookup(ref, all));
}

function needsLocalAssetLookup(refs) {
  return (refs || []).some(ref => !looksLikeFile(ref));
}

function loadAssetRefFromLookup(ref, all) {
  if (looksLikeFile(ref)) return normalizeAsset(JSON.parse(fs.readFileSync(path.resolve(ref), 'utf8')));
  const found = all.find(asset => asset && (asset.asset_id === ref || asset.id === ref));
  if (!found) throw new ContractError('schema_invalid', 'asset not found: ' + ref);
  return normalizeAsset(found);
}

function loadLocalAssetsFromStore(deps) {
  const store = deps.assetStore || require('./assetStore');
  const genes = typeof store.loadGenes === 'function' ? (store.loadGenes() || []) : [];
  const capsules = typeof store.loadCapsules === 'function' ? (store.loadCapsules() || []) : [];
  const events = typeof store.readAllEvents === 'function' ? (store.readAllEvents() || []) : [];
  return genes.concat(capsules, events);
}

function loadLocalAssetsReadOnly(deps) {
  const dir = deps.assetsDir || getGepAssetsDir();
  return []
    .concat(readJsonArray(path.join(dir, 'genes.json'), 'genes'))
    .concat(readJsonLines(path.join(dir, 'genes.jsonl'), 'Gene'))
    .concat(readJsonArray(path.join(dir, 'capsules.json'), 'capsules'))
    .concat(readJsonLines(path.join(dir, 'capsules.jsonl'), 'Capsule'))
    .concat(readJsonLines(path.join(dir, 'events.jsonl'), 'EvolutionEvent'));
}

function readJsonArray(filePath, key) {
  try {
    if (!fs.existsSync(filePath)) return [];
    const parsed = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const rows = key ? parsed && parsed[key] : parsed;
    return Array.isArray(rows) ? rows.filter(record) : [];
  } catch (e) {
    throw new ContractError('schema_invalid', 'asset schema is invalid');
  }
}

function readJsonLines(filePath, type) {
  try {
    if (!fs.existsSync(filePath)) return [];
    return fs.readFileSync(filePath, 'utf8')
      .split('\n')
      .map(line => line.trim())
      .filter(Boolean)
      .map(line => JSON.parse(line))
      .filter(asset => record(asset) && (!type || asset.type === type));
  } catch (e) {
    throw new ContractError('schema_invalid', 'asset schema is invalid');
  }
}

function normalizeAsset(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ContractError('schema_invalid', 'asset is not an object');
  const type = canonicalAssetType(value.type);
  if (!type) throw new ContractError('schema_invalid', 'asset type must be Gene, Capsule, or EvolutionEvent');
  return Object.assign({}, value, { type, asset_id: value.asset_id || 'IGNORED' });
}

function checkBundle(bundle) {
  const genes = bundle.filter(asset => asset.type === 'Gene');
  const capsules = bundle.filter(asset => asset.type === 'Capsule');
  const events = bundle.filter(asset => asset.type === 'EvolutionEvent');
  if (genes.length > 1 || capsules.length > 1 || events.length > 1) {
    return { ok: false, message: 'publish supports one Gene + one Capsule + optional one EvolutionEvent bundle' };
  }
  if (genes.length === 0 || capsules.length === 0) return { ok: false, message: 'publish requires Gene + Capsule bundle' };
  for (const gene of genes) {
    const ids = new Set([gene.asset_id, gene.id].filter(Boolean));
    const paired = capsules.some(capsule => ids.has(capsule.gene));
    if (!paired) return { ok: false, message: 'gene must publish with its capsule' };
  }
  return { ok: true };
}

function leakCheck(bundle) {
  const result = fullLeakCheck(JSON.stringify(bundle));
  const hardLeaks = (result.leaks || []).filter(leak => leak && leak.type !== 'local_path');
  return { blocked: hardLeaks.length > 0 };
}

function verifyReuseAssetId(asset, requestedId) {
  if (!asset || asset.asset_id !== requestedId) return { ok: false };
  return { ok: computeAssetId(asset) === requestedId };
}

function isReuseAssetStoreStable(asset) {
  return Boolean(asset && asset.schema_version);
}

async function fetchAssetById(assetId, deps) {
  const hubUrl = getHubUrl(deps);
  if (!hubUrl) throw new ContractError('auth_required', 'Hub URL is required');
  if (!hasHubAuthorization(deps)) throw new ContractError('auth_required', 'Hub authentication required');
  const a2a = deps.a2a || require('./a2aProtocol');
  const message = a2a.buildFetch({ assetIds: [assetId] });
  const posted = await postEnvelope('/a2a/fetch', message, deps);
  if (!posted.ok) {
    const stableReason = stableHubReason(posted.body, REUSE_FAILURE_REASONS);
    if (stableReason === 'unsupported' || stableReason === 'cli_unavailable') {
      throw new ContractError(stableReason, reuseReasonMessage(stableReason));
    }
    if (posted.status === 401 || posted.status === 403) throw new ContractError('auth_required', 'Hub authentication required');
    if (posted.status === 404) return null;
    throw new ContractError('network_error', 'Hub fetch failed');
  }
  const assets = assetsFromBody(posted.body);
  return assets.find(asset => asset && asset.asset_id === assetId) || null;
}

async function postValidate(message, deps) {
  if (deps.validate) return normalizeValidateResult(await deps.validate(message));
  const validateMessage = Object.assign({}, message, { message_type: 'validate' });
  const result = await postEnvelope('/a2a/validate', validateMessage, deps);
  return normalizeValidateResult(result);
}

function normalizeValidateResult(result) {
  const raw = record(result) || {};
  const status = typeof raw.status === 'number' ? raw.status : (raw.ok ? 200 : 0);
  const body = raw.body;
  if (!raw.ok) {
    return {
      ok: false,
      status,
      reason: stableReason(raw.reason, PUBLISH_FAILURE_REASONS) || hubReason(body) || ('hub ' + status),
      body,
    };
  }
  const payload = record(body && body.payload);
  const passed = Boolean(payload && (payload.valid === true || payload.ok === true));
  return {
    ok: passed,
    status,
    reason: stringField(payload, 'reason') || stringField(payload, 'error'),
    body,
  };
}

async function postPublish(message, deps) {
  if (deps.publish) return deps.publish(message);
  const result = await postEnvelope('/a2a/publish', message, deps);
  if (!result.ok) return { ok: false, status: result.status, reason: hubReason(result.body) || ('hub ' + result.status), body: result.body };
  return { ok: true, status: result.status, body: result.body };
}

async function postEnvelope(endpointPath, message, deps) {
  const hubUrl = getHubUrl(deps);
  if (!hubUrl) throw new ContractError('auth_required', 'Hub URL is required');
  const a2a = deps.a2a || require('./a2aProtocol');
  const headers = buildEnvelopeHeaders(endpointPath, deps, a2a);
  if (!hasAuthorizationHeader(headers)) throw new ContractError('auth_required', 'Hub authentication required');
  const fetchImpl = deps.hubFetch || require('./hubFetch').hubFetch;
  const timeoutMs = deps.timeoutMs || 30000;
  const endpoint = hubUrl.replace(/\/+$/, '') + endpointPath;
  try {
    const res = await fetchImpl(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(message),
      signal: AbortSignal.timeout(timeoutMs),
    });
    const body = await safeJson(res);
    return { ok: Boolean(res && res.ok), status: res && res.status || 0, body };
  } catch (e) {
    return { ok: false, status: 0, body: { error: 'network_error' } };
  }
}

async function safeJson(res) {
  if (!res) return {};
  if (typeof res.text === 'function') {
    try {
      const text = await res.text();
      try { return JSON.parse(text); } catch (_) {
        return text ? { error: String(text).slice(0, 200) } : {};
      }
    } catch (_) {}
  }
  if (typeof res.json === 'function') {
    try { return await res.json(); } catch (_) {}
  }
  return {};
}

function prepareReuseAssetStore(asset, deps) {
  const store = deps.assetStore || require('./assetStore');
  if (asset.type === 'Gene' && typeof store.upsertGene === 'function') {
    assertNoLocalReuseIdConflict(asset, store, 'Gene');
    return store;
  }
  if (asset.type === 'Capsule' && typeof store.upsertCapsule === 'function') {
    assertNoLocalReuseIdConflict(asset, store, 'Capsule');
    return store;
  }
  if (asset.type === 'EvolutionEvent' && typeof store.appendEventJsonl === 'function') {
    return store;
  }
  throw new ContractError('unsupported', 'unsupported asset type');
}

function storeReusedAsset(asset, deps, preparedStore) {
  const store = preparedStore || prepareReuseAssetStore(asset, deps);
  if (asset.type === 'Gene' && typeof store.upsertGene === 'function') {
    assertNoLocalReuseIdConflict(asset, store, 'Gene');
    store.upsertGene(asset);
  } else if (asset.type === 'Capsule' && typeof store.upsertCapsule === 'function') {
    assertNoLocalReuseIdConflict(asset, store, 'Capsule');
    store.upsertCapsule(asset);
  } else if (asset.type === 'EvolutionEvent' && typeof store.appendEventJsonl === 'function') {
    store.appendEventJsonl(asset);
  } else {
    throw new ContractError('unsupported', 'unsupported asset type');
  }
  return asset.asset_id || computeAssetId(asset);
}

function assertNoLocalReuseIdConflict(asset, store, type) {
  if (!asset || !asset.id) return;
  const local = findLocalAssetByTypeAndId(store, type, asset.id);
  if (!local) return;
  const incomingAssetId = asset.asset_id || computeAssetId(asset);
  const localAssetId = local.asset_id || computeAssetId(local);
  if (incomingAssetId !== localAssetId) {
    throw new ContractError('internal_error', 'local asset id conflict');
  }
}

function findLocalAssetByTypeAndId(store, type, id) {
  const loader = type === 'Gene' ? store.loadGenes : store.loadCapsules;
  if (typeof loader !== 'function') return null;
  const assets = loader.call(store) || [];
  return assets.find(asset => asset && asset.type === type && String(asset.id) === String(id)) || null;
}

function prepareHubProvenance(deps) {
  const dir = deps.assetsDir || getGepAssetsDir();
  const file = path.join(dir, 'provenance.jsonl');
  try {
    fs.mkdirSync(dir, { recursive: true });
    const stat = fs.existsSync(file) ? fs.statSync(file) : null;
    if (stat && !stat.isFile()) throw new Error('not a file');
    return { file, existed: Boolean(stat), size: stat ? stat.size : 0 };
  } catch (_) {
    throw new ContractError('internal_error', 'provenance write failed');
  }
}

function markHubProvenance(assetId, deps, prepared) {
  if (!assetId) throw new ContractError('internal_error', 'provenance write failed');
  const target = prepared || prepareHubProvenance(deps);
  const line = JSON.stringify({
    assetId,
    source: 'hub',
    trusted: false,
    at: new Date().toISOString(),
  }) + '\n';
  try {
    fs.appendFileSync(target.file, line, 'utf8');
    target.entry = line;
  } catch (_) {
    throw new ContractError('internal_error', 'provenance write failed');
  }
}

function rollbackHubProvenance(prepared) {
  if (!prepared || !prepared.file) return;
  try {
    if (!fs.existsSync(prepared.file)) return;
    const stat = fs.statSync(prepared.file);
    if (!stat.isFile() || stat.size < prepared.size) return;
    if (prepared.entry) {
      const fd = fs.openSync(prepared.file, 'r');
      try {
        const tailLength = stat.size - prepared.size;
        const buf = Buffer.alloc(tailLength);
        fs.readSync(fd, buf, 0, tailLength, prepared.size);
        if (buf.toString('utf8') !== prepared.entry) return;
      } finally {
        fs.closeSync(fd);
      }
    }
    fs.truncateSync(prepared.file, prepared.size);
    if (!prepared.existed && prepared.size === 0) {
      try { fs.unlinkSync(prepared.file); } catch (_) {}
    }
  } catch (_) {}
}

function stripHubMetadata(asset) {
  const out = {};
  for (const key of Object.keys(asset || {})) {
    if (!HUB_METADATA_KEYS.has(key)) out[key] = asset[key];
  }
  return out;
}

function dryRunEnvelope(bundle, credits) {
  const blockReasons = Array.isArray(bundle.blockReasons) ? bundle.blockReasons : [];
  const envelope = {
    ok: true,
    contract: PUBLISH_CONTRACT,
    mode: 'dry_run',
    reversibility: REVERSIBILITY,
    blocked: blockReasons.length > 0,
    block_reasons: blockReasons,
    assets: bundle.assets,
    gates: bundle.gates,
    ...(credits ? { credits } : {}),
  };
  if (!blockReasons.includes('leak_detected')) {
    envelope.payload = { assets: bundle.sanitized };
  }
  return envelope;
}

function syncBundleFromPublishMessage(bundle, message) {
  const finalAssets = publishPayloadAssets(message);
  if (finalAssets.length === 0) throw new ContractError('bundle_required', 'publish requires a complete asset bundle');
  bundle.sanitized = finalAssets;
  bundle.assets = summarizePublishAssets(finalAssets);
  const leak = leakCheck(finalAssets);
  if (leak.blocked && !bundle.blockReasons.includes('leak_detected')) {
    bundle.blockReasons.push('leak_detected');
  }
  bundle.gates.leak = leak.blocked ? 'fail' : 'pass';
}

function publishPayloadAssets(message) {
  const payload = record(message && message.payload) || {};
  return Array.isArray(payload.assets) ? payload.assets.filter(asset => record(asset)) : [];
}

function sanitizePublishAssets(assets, deps) {
  return (assets || []).filter(asset => record(asset)).map(asset => {
    const clean = sanitizeForContract(asset, deps);
    clean.asset_id = computeAssetId(clean);
    return clean;
  });
}

function summarizePublishAssets(assets) {
  return (assets || []).filter(asset => record(asset)).map(asset => {
    const out = {};
    const assetId = stringField(asset, 'asset_id');
    const type = canonicalAssetType(asset.type);
    if (assetId) out.asset_id = assetId;
    if (type) out.type = type;
    return out;
  });
}

function publishFailure(reason, message, opts) {
  opts = opts || {};
  return {
    ok: false,
    contract: PUBLISH_CONTRACT,
    ...(opts.mode ? { mode: opts.mode } : {}),
    ...(opts.status ? { status: opts.status } : {}),
    ...(opts.gates ? { gates: opts.gates } : {}),
    ...(opts.assets ? { assets: opts.assets } : {}),
    ...(opts.credits ? { credits: opts.credits } : {}),
    reason,
    retryable: Boolean(opts.retryable),
    message,
  };
}

function reuseFailure(reason, message) {
  return { ok: false, contract: REUSE_CONTRACT, reason, message };
}

function writeJson(out, value, code, deps, machineJson) {
  const line = JSON.stringify(sanitizeForContract(value, deps)) + '\n';
  const originalStdoutWrite = deps && deps[MACHINE_JSON_STDOUT_WRITE];
  if (machineJson && out === process.stdout && typeof originalStdoutWrite === 'function') {
    originalStdoutWrite.call(process.stdout, line);
  } else {
    out.write(line);
  }
  return code;
}

async function withMachineJsonConsole(enabled, deps, fn) {
  if (!enabled) return fn();
  const original = {
    log: console.log,
    info: console.info,
    warn: console.warn,
    error: console.error,
    debug: console.debug,
    stdoutWrite: process.stdout.write,
    stderrWrite: process.stderr.write,
  };
  const hadOriginalStdoutWrite = Object.prototype.hasOwnProperty.call(deps, MACHINE_JSON_STDOUT_WRITE);
  const previousOriginalStdoutWrite = deps[MACHINE_JSON_STDOUT_WRITE];
  const write = (...args) => {
    try { process.stderr.write(sanitizeText(util.format(...args), deps) + '\n'); } catch (_) {}
  };
  deps[MACHINE_JSON_STDOUT_WRITE] = original.stdoutWrite;
  process.stdout.write = function (chunk, encoding, callback) {
    const clean = sanitizeStderrChunk(chunk, encoding, deps);
    if (typeof encoding === 'function') return original.stderrWrite.call(process.stderr, clean, encoding);
    return original.stderrWrite.call(process.stderr, clean, encoding, callback);
  };
  process.stderr.write = function (chunk, encoding, callback) {
    const clean = sanitizeStderrChunk(chunk, encoding, deps);
    if (typeof encoding === 'function') return original.stderrWrite.call(process.stderr, clean, encoding);
    return original.stderrWrite.call(process.stderr, clean, encoding, callback);
  };
  console.log = write;
  console.info = write;
  console.warn = write;
  console.error = write;
  console.debug = write;
  try {
    return await fn();
  } finally {
    console.log = original.log;
    console.info = original.info;
    console.warn = original.warn;
    console.error = original.error;
    console.debug = original.debug;
    process.stdout.write = original.stdoutWrite;
    process.stderr.write = original.stderrWrite;
    if (hadOriginalStdoutWrite) {
      deps[MACHINE_JSON_STDOUT_WRITE] = previousOriginalStdoutWrite;
    } else {
      delete deps[MACHINE_JSON_STDOUT_WRITE];
    }
  }
}

function classifyError(e, command) {
  if (e instanceof ContractError) return { reason: e.reason, message: e.safeMessage, retryable: e.reason === 'network_error' };
  const msg = e && e.message ? String(e.message) : '';
  if (/node_secret|credential|auth|401|403/i.test(msg)) return { reason: 'auth_required', message: 'Hub authentication required', retryable: false };
  if (/A2A_HUB_URL|Hub URL/i.test(msg)) return { reason: 'auth_required', message: 'Hub URL is required', retryable: false };
  return { reason: 'internal_error', message: 'evolver ' + command + ' failed', retryable: false };
}

function publishReasonFromStatus(status) {
  if (status === 401 || status === 403) return 'auth_required';
  if (status === 402) return 'insufficient_credits';
  if (status === 429 || status >= 500 || status === 0) return 'network_error';
  return 'quality_gate_failed';
}

function publishReasonFromResponse(status, body, reason) {
  return stableReason(reason, PUBLISH_FAILURE_REASONS)
    || stableHubReason(body, PUBLISH_FAILURE_REASONS)
    || publishReasonFromStatus(status);
}

function publishRetryable(reason) {
  return reason === 'network_error';
}

function sanitizeForContract(value, deps) {
  return redactKnownSecrets(sanitizePayload(value), deps);
}

function sanitizeText(value, deps) {
  return redactKnownSecretsInString(redactString(String(value)), deps);
}

function sanitizeStderrChunk(chunk, encoding, deps) {
  const text = Buffer.isBuffer(chunk)
    ? chunk.toString(typeof encoding === 'string' ? encoding : 'utf8')
    : String(chunk);
  return sanitizeText(text, deps);
}

function redactKnownSecrets(value, deps, known) {
  const secrets = known || knownLocalSecrets(deps);
  if (typeof value === 'string') return redactKnownSecretsInString(value, deps, secrets);
  if (!value || typeof value !== 'object') return value;
  if (Array.isArray(value)) return value.map(item => redactKnownSecrets(item, deps, secrets));
  const out = {};
  for (const key of Object.keys(value)) {
    const cleanKey = uniqueObjectKey(out, sanitizeObjectKey(key, deps, secrets));
    out[cleanKey] = redactKnownSecrets(value[key], deps, secrets);
  }
  return out;
}

function sanitizeObjectKey(key, deps, secrets) {
  const clean = redactKnownSecretsInString(redactString(String(key)), deps, secrets);
  return clean || '[REDACTED]';
}

function uniqueObjectKey(target, key) {
  if (!Object.prototype.hasOwnProperty.call(target, key)) return key;
  let i = 2;
  while (Object.prototype.hasOwnProperty.call(target, key + '_' + i)) i++;
  return key + '_' + i;
}

function redactKnownSecretsInString(value, deps, known) {
  let result = value;
  const secrets = known || knownLocalSecrets(deps);
  for (const secret of secrets) result = result.split(secret).join('[REDACTED]');
  return result;
}

function knownLocalSecrets(deps) {
  const secrets = new Set();
  const add = value => {
    if (typeof value === 'string' && value.length >= 8) secrets.add(value);
  };
  if (deps) add(deps.nodeSecret);
  try { add(getHubNodeSecret(deps || {})); } catch (_) {}
  for (const [key, value] of Object.entries(process.env)) {
    if (/SECRET|TOKEN|API[_-]?KEY|PASSWORD|AUTH|CREDENTIAL/i.test(key)) add(value);
  }
  return Array.from(secrets).sort((a, b) => b.length - a.length);
}

function hasHubAuthorization(deps) {
  if (getHubNodeSecret(deps)) return true;
  const a2a = deps.a2a || require('./a2aProtocol');
  return hasAuthorizationHeader(buildHubHeadersSafe(a2a));
}

function buildEnvelopeHeaders(endpointPath, deps, a2a) {
  if (NODE_SCOPED_ENDPOINT_PATHS.has(endpointPath)) {
    return buildNodeScopedHubHeadersSafe(a2a, deps);
  }
  return buildHubHeadersSafe(a2a);
}

function buildNodeScopedHubHeadersSafe(a2a, deps) {
  if (!deps || deps.nodeSecret === undefined) {
    try {
      if (typeof a2a.buildNodeScopedHubHeaders === 'function') {
        const headers = a2a.buildNodeScopedHubHeaders() || {};
        if (hasAuthorizationHeader(headers)) return headers;
      }
    } catch (_) {}
  }
  const nodeSecret = getHubNodeSecret(deps || {});
  if (!nodeSecret) return {};
  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + nodeSecret,
  };
  const secretVersion = getHubNodeSecretVersionSafe(a2a);
  if (secretVersion) headers['X-EvoMap-Node-Secret-Version'] = String(secretVersion);
  return headers;
}

function getHubNodeSecretVersionSafe(a2a) {
  try {
    return typeof a2a.getHubNodeSecretVersion === 'function' ? a2a.getHubNodeSecretVersion() : null;
  } catch (_) {
    return null;
  }
}

function buildHubHeadersSafe(a2a) {
  try {
    return typeof a2a.buildHubHeaders === 'function' ? (a2a.buildHubHeaders() || {}) : {};
  } catch (_) {
    return {};
  }
}

function hasAuthorizationHeader(headers) {
  const value = headers && (headers.Authorization || headers.authorization);
  return typeof value === 'string' && /^Bearer\s+\S+$/i.test(value);
}

function stableHubReason(body, allowed) {
  return stableReason(hubReason(body), allowed);
}

function stableReason(reason, allowed) {
  const safe = safeTokenField(reason);
  return safe && allowed.has(safe) ? safe : null;
}

function canonicalAssetType(value) {
  if (value === 'Gene' || value === 'gene') return 'Gene';
  if (value === 'Capsule' || value === 'capsule') return 'Capsule';
  if (value === 'EvolutionEvent' || value === 'event' || value === 'Evolutionevent') return 'EvolutionEvent';
  return null;
}

function assetsFromBody(body) {
  const b = record(body) || {};
  const p = record(b.payload) || {};
  const rows = Array.isArray(p.results) ? p.results
    : Array.isArray(p.assets) ? p.assets
      : Array.isArray(b.results) ? b.results
        : Array.isArray(b.assets) ? b.assets
          : [];
  return rows.filter(row => row && typeof row === 'object' && !Array.isArray(row));
}

function extractCredits(body) {
  const b = record(body) || {};
  const p = record(b.payload) || b;
  const c = record(p.credits) || record(p.credit_cost) || record(p.economic) || p;
  return creditsFromPayload(c);
}

function creditsFromPayload(payload) {
  const required = numberField(payload, 'required');
  const available = numberField(payload, 'available');
  const estimated = firstNumberField(payload, ['estimated', 'estimate']);
  const charged = numberField(payload, 'charged');
  const balanceKind = safeTokenField(stringField(payload, 'balance_kind') || stringField(payload, 'balanceKind'));
  const out = {};
  if (required !== undefined) out.required = required;
  if (available !== undefined) out.available = available;
  if (estimated !== undefined) out.estimated = estimated;
  if (charged !== undefined) out.charged = charged;
  if (balanceKind) out.balance_kind = balanceKind;
  return Object.keys(out).length ? out : undefined;
}

function normalizePublishStatus(body) {
  const b = record(body) || {};
  const p = record(b.payload) || b;
  const status = stringField(p, 'status');
  if (status) {
    if (status === 'queued' || status === 'accepted' || status === 'published') return status;
    return null;
  }
  const decision = stringField(p, 'decision');
  if (!decision) return null;
  if (decision === 'accept') return 'accepted';
  if ((decision === 'reject' || decision === 'rejected') && stringField(p, 'reason') === 'already_published') return 'published';
  return null;
}

function publishDecision(body) {
  const b = record(body) || {};
  const p = record(b.payload) || b;
  return stringField(p, 'decision');
}

function hubReason(body) {
  const b = record(body) || {};
  const p = record(b.payload) || b;
  return stringField(p, 'reason') || stringField(p, 'error');
}

function publishReasonMessage(reason) {
  const map = {
    redaction_unavailable: 'redaction unavailable',
    leak_detected: 'leak detected after redaction',
    schema_invalid: 'asset schema is invalid',
    bundle_required: 'publish requires a complete asset bundle',
    quality_gate_failed: 'Hub quality gate failed',
    auth_required: 'Hub authentication required',
    insufficient_credits: 'insufficient credits',
    network_error: 'Hub unreachable',
    unsupported: 'publish unsupported',
    cli_unavailable: 'evolver CLI unavailable',
    internal_error: 'evolver publish failed',
  };
  return map[reason] || map.internal_error;
}

function reuseReasonMessage(reason) {
  const map = {
    missing_id: 'reuse requires --id <asset_id>',
    cli_unavailable: 'evolver CLI unavailable',
    auth_required: 'Hub authentication required',
    not_found: 'asset not found',
    network_error: 'Hub fetch failed',
    unsupported: 'reuse unsupported',
    internal_error: 'evolver reuse failed',
  };
  return map[reason] || map.internal_error;
}

function getHubUrl(deps) {
  if (deps.hubUrl) return deps.hubUrl;
  const a2a = deps.a2a || require('./a2aProtocol');
  return typeof a2a.getHubUrl === 'function' ? a2a.getHubUrl() : process.env.A2A_HUB_URL;
}

function getHubNodeSecret(deps) {
  if (deps.nodeSecret !== undefined) return deps.nodeSecret;
  const a2a = deps.a2a || require('./a2aProtocol');
  return typeof a2a.getHubNodeSecret === 'function' ? a2a.getHubNodeSecret() : process.env.A2A_NODE_SECRET;
}

function looksLikeFile(value) {
  try { return fs.existsSync(value) && fs.statSync(value).isFile(); } catch (_) { return false; }
}

function record(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : null;
}

function stringField(value, key) {
  const obj = record(value);
  const raw = obj && obj[key];
  return typeof raw === 'string' && raw.trim() ? raw.trim() : undefined;
}

function safeTokenField(value) {
  if (!value) return undefined;
  return /^[A-Za-z0-9_.:-]{1,64}$/.test(value) ? value : undefined;
}

function firstNumberField(value, keys) {
  for (const key of keys) {
    const n = numberField(value, key);
    if (n !== undefined) return n;
  }
  return undefined;
}

function numberField(value, key) {
  const obj = record(value);
  const raw = obj && obj[key];
  const n = typeof raw === 'number' ? raw : (typeof raw === 'string' && raw.trim() ? Number(raw) : NaN);
  return Number.isSafeInteger(n) ? n : undefined;
}

function sameJson(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

class ContractError extends Error {
  constructor(reason, safeMessage) {
    super(safeMessage);
    this.name = 'ContractError';
    this.reason = reason;
    this.safeMessage = safeMessage;
  }
}

module.exports = {
  parseReuseArgs,
  parsePublishArgs,
  buildPublishBundle,
  runReuseCommand,
  runPublishCommand,
};
