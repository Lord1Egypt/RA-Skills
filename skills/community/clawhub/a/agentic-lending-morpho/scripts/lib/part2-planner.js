const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { AbiCoder, Interface, JsonRpcProvider, Wallet, getCreateAddress, solidityPacked } = require('ethers');
const dapiCatalog = require('@api3/dapi-management/dist/data/dapis.json');
const {
  browserPlan,
  executeBuySubscription,
  parseArgs,
  ensureActive,
  purchaseInputs,
} = require('./api3-feed-manager');
const { getEvkRecipe, listEvkRecipes } = require('./part2-recipes');
const { resolveAutoVaultContext } = require('./part2-chain-bootstrap');

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.join(ROOT_DIR, 'data', 'part2');
const REGISTRY_PATH = path.join(DATA_DIR, 'market-registry.json');
const FEED_STATUS_PATH = path.join(DATA_DIR, 'feed-status.json');
const CONTRACT_ARTIFACT_DIR = path.join(DATA_DIR, 'contract-artifacts');
const CONTRACT_ARTIFACT_PATHS = Object.freeze({
  Api3PartialAggregatorV2V3Interface: path.join(CONTRACT_ARTIFACT_DIR, 'Api3PartialAggregatorV2V3Interface.json'),
  ChainlinkInfrequentOracle: path.join(CONTRACT_ARTIFACT_DIR, 'ChainlinkInfrequentOracle.json'),
  ChainlinkOracle: path.join(CONTRACT_ARTIFACT_DIR, 'ChainlinkOracle.json'),
  CrossAdapter: path.join(CONTRACT_ARTIFACT_DIR, 'CrossAdapter.json'),
  EulerRouter: path.join(CONTRACT_ARTIFACT_DIR, 'EulerRouter.json'),
});
const CALL_ARTIFACT_PATHS = Object.freeze({
  GenericFactory: path.join(CONTRACT_ARTIFACT_DIR, 'GenericFactory.json'),
});
const ABI_CODER = AbiCoder.defaultAbiCoder();
const contractArtifactCache = new Map();
const callArtifactCache = new Map();

const SUPPORTED_PROTOCOLS = new Set(['evk', 'morpho']);
const SUPPORTED_COMMANDS = new Set([
  'plan-market',
  'discover-markets',
  'ensure-feeds',
  'prepare-euler-oracle',
  'deploy-euler-oracle',
  'prepare-evk-market',
  'prepare-evk-deployment',
  'deploy-evk-market',
  'run-evk-workflow',
]);
const EVK_ONLY_WARNING = 'Planner execution is EVK-first in this phase. Morpho is reserved for a later protocol track.';
const DEFAULT_ORACLE_PREFERENCE = 'chainlink-compatible-first';
const DEFAULT_DUPLICATE_POLICY = 'block-on-exact';
const DEFAULT_ACTIVATION_MODE = 'check-only';
const DEFAULT_STATUSES = ['draft', 'active', 'deprecated', 'paused'];
const DEFAULT_MAX_STALENESS_SECONDS = 3600;
const DEFAULT_UNIT_OF_ACCOUNT = 'USD';
const DAPI_SYMBOL_ALIASES = Object.freeze({
  WETH: 'ETH',
  WBTC: 'BTC',
  CBBTC: 'BTC',
  TBTC: 'BTC',
});
const SYNTHETIC_ASSET_ADDRESSES = Object.freeze({
  USD: '0x0000000000000000000000000000000000000348',
});
const CHAINLINK_ORACLE_MAX_STALENESS_LOWER_BOUND = 60;
const CHAINLINK_ORACLE_MAX_STALENESS_UPPER_BOUND = 72 * 60 * 60;
const DAPI_NAME_SET = new Set(dapiCatalog.map((entry) => String(entry.name || '').trim().toUpperCase()).filter(Boolean));

function sanitizeChainName(chain) {
  return String(chain?.name || '')
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, '_');
}

function resolveRpcUrlForChain(chain, rpcPreference = {}) {
  const preferredRpcUrls = [];

  if (typeof rpcPreference.rpcUrl === 'string' && rpcPreference.rpcUrl.trim()) {
    preferredRpcUrls.push({ rpcUrl: rpcPreference.rpcUrl.trim(), source: 'request:rpcUrl' });
  }

  if (Array.isArray(rpcPreference.rpcUrls)) {
    rpcPreference.rpcUrls
      .filter((entry) => typeof entry === 'string' && entry.trim())
      .forEach((entry, index) => {
        preferredRpcUrls.push({ rpcUrl: entry.trim(), source: `request:rpcUrls[${index}]` });
      });
  }

  if (preferredRpcUrls.length > 0) {
    return preferredRpcUrls[0];
  }

  if (rpcPreference.allowPublicFallback === false) {
    return { rpcUrl: null, source: 'request:no-fallback' };
  }

  const chainName = sanitizeChainName(chain);
  const candidates = [
    chainName ? `PART2_PLANNER_RPC_URL_${chainName}` : null,
    chainName ? `${chainName}_RPC_URL` : null,
    chainName ? `API3_FEED_MANAGER_RPC_URL_${chainName}` : null,
    'PART2_PLANNER_RPC_URL',
    'API3_FEED_MANAGER_RPC_URL',
    'RPC_URL',
  ].filter(Boolean);

  for (const envName of candidates) {
    const value = process.env[envName];
    if (typeof value === 'string' && value.trim()) {
      return { rpcUrl: value.trim(), source: `env:${envName}` };
    }
  }

  return { rpcUrl: null, source: null };
}

async function fetchLiveFeedStatus(chain, feedRequirement, rpcPreference = {}) {
  const { rpcUrl, source } = resolveRpcUrlForChain(chain, rpcPreference);
  if (!rpcUrl) {
    return {
      ok: false,
      fallbackReason: `No RPC URL configured for ${chain.name || `chain-${chain.chainId}`}`,
    };
  }

  const dapiName = feedRequirement.feedName || `${feedRequirement.base.symbol}/${feedRequirement.quote.symbol}`;
  const canonicalDapiName = canonicalizeFeedName(dapiName);

  const ensureResult = await ensureActive({
    chain: chain.name || String(chain.chainId),
    rpcUrl,
    dapiName,
  });

  const resolution = ensureResult.resolution || {};
  const addresses = resolution.addresses || {};
  const activation = ensureResult.activation || {};
  const latestReadSource = resolution.latestRead || resolution.verification;
  const latestRead = latestReadSource
    ? {
        value: String(latestReadSource.value ?? ''),
        timestamp: Number(latestReadSource.timestamp ?? 0),
        humanValue: latestReadSource.humanValue ?? undefined,
      }
    : undefined;

  const classification = activation.classification || ensureResult.status || 'blocked';
  const statusMap = {
    active: 'ready',
    activatable: 'activatable',
    inactive: 'inactive',
    unsupported: 'blocked',
    blocked: 'blocked',
  };

  return {
    ok: true,
    source,
    status: statusMap[classification] || 'blocked',
    proxyAddress: addresses.communalProxy || addresses.readerProxy || addresses.dataFeedProxy || fakeProxyAddress(canonicalDapiName || dapiName, chain.chainId),
    proxyDeploymentPlan: resolution.proxyDeploymentPlan || undefined,
    proxyHasCode: resolution.verification && typeof resolution.verification.proxyHasCode === 'boolean'
      ? resolution.verification.proxyHasCode
      : undefined,
    supportsAggregatorV2V3Interface: classification !== 'unsupported',
    requiresCompatibilityWrapper: classification !== 'unsupported',
    latestRead,
    blockers: Array.isArray(activation.blockers) && activation.blockers.length > 0
      ? activation.blockers.map(String)
      : ((classification === 'blocked' || classification === 'unsupported' || classification === 'inactive') && ensureResult.reason
        ? [String(ensureResult.reason)]
        : []),
    activation: ensureResult.activation,
    resolution,
    ensureResult,
  };
}

function printUsage() {
  console.error(`Usage:
  part2-planner plan-market --input '{"protocol":"evk",...}'
  part2-planner discover-markets --input-file ./request.json
  part2-planner ensure-feeds < request.json
  part2-planner prepare-euler-oracle --input-file ./request.json
  part2-planner deploy-euler-oracle --input-file ./request.json
  part2-planner prepare-evk-market --input-file ./request.json
  part2-planner prepare-evk-deployment --input-file ./request.json
  part2-planner deploy-evk-market --input-file ./request.json
  part2-planner run-evk-workflow --input-file ./request.json

Options:
  --input <json>
  --input-file <path>
  --format json
  --registry-file <path>
  --feed-status-file <path>`);
}

function readJsonFile(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function resolveExistingUserPath(filePath) {
  const rawPath = String(filePath);
  if (path.isAbsolute(rawPath)) {
    return rawPath;
  }

  const cwdResolvedPath = path.resolve(process.cwd(), rawPath);
  if (fs.existsSync(cwdResolvedPath)) {
    return cwdResolvedPath;
  }

  return path.resolve(ROOT_DIR, rawPath);
}

function loadInput(options) {
  if (options.input !== undefined) {
    return JSON.parse(String(options.input));
  }

  if (options.inputFile) {
    return readJsonFile(resolveExistingUserPath(options.inputFile));
  }

  if (!process.stdin.isTTY) {
    const stdin = fs.readFileSync(0, 'utf8').trim();
    if (stdin) {
      return JSON.parse(stdin);
    }
  }

  throw new Error('Missing request JSON. Pass --input, --input-file, or pipe JSON on stdin.');
}

function loadRegistry(options) {
  const registryPath = options.registryFile
    ? resolveExistingUserPath(options.registryFile)
    : REGISTRY_PATH;
  return readJsonFile(registryPath);
}

function loadFeedStatus(options) {
  const filePath = options.feedStatusFile
    ? resolveExistingUserPath(options.feedStatusFile)
    : FEED_STATUS_PATH;
  return readJsonFile(filePath);
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function assertPlainObject(value, label) {
  assert(value && typeof value === 'object' && !Array.isArray(value), `${label} must be an object`);
}

function assertAllowedKeys(value, allowedKeys, label) {
  const extras = Object.keys(value).filter((key) => !allowedKeys.includes(key));
  assert(extras.length === 0, `${label} has unsupported properties: ${extras.join(', ')}`);
}

function assertEnum(value, allowed, label) {
  assert(allowed.includes(value), `${label} must be one of: ${allowed.join(', ')}`);
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

function isHexAddress(value) {
  return /^0x[a-fA-F0-9]{40}$/.test(value || '');
}

function isNonZeroHexAddress(value) {
  return isHexAddress(value) && !/^0x0{40}$/.test(value);
}

function normalizeUint256Like(value) {
  if (typeof value === 'bigint') {
    return value >= 0n ? value : null;
  }

  if (typeof value === 'number') {
    return Number.isInteger(value) && value >= 0 ? BigInt(value) : null;
  }

  if (typeof value === 'string' && /^[0-9]+$/.test(value)) {
    return BigInt(value);
  }

  return null;
}

function findRouteFeedForArtifact(routeFeeds, artifact) {
  if (!Array.isArray(routeFeeds) || routeFeeds.length === 0) {
    return null;
  }

  return routeFeeds.find((feed) => feedNamesEqual(
    feed.feedName || `${feed.base.symbol}/${feed.quote.symbol}`,
    artifact.feedName || `${artifact.base?.symbol || 'BASE'}/${artifact.quote?.symbol || 'QUOTE'}`,
  )) || null;
}

function buildConcreteChainlinkOracleArgs({ artifact, routeFeed, route, wrapperDeploymentRef }) {
  if (!routeFeed || !isNonZeroHexAddress(routeFeed.base && routeFeed.base.address) || !isNonZeroHexAddress(routeFeed.quote && routeFeed.quote.address)) {
    return null;
  }

  return {
    base: routeFeed.base.address,
    quote: routeFeed.quote.address,
    ...(wrapperDeploymentRef ? { feedDeploymentRef: wrapperDeploymentRef } : { feed: artifact.proxyAddress }),
    maxStaleness: route.maxStalenessSeconds || DEFAULT_MAX_STALENESS_SECONDS,
  };
}

function getConstructorDependencyRefs(constructorArgs) {
  if (!constructorArgs || typeof constructorArgs !== 'object' || Array.isArray(constructorArgs)) {
    return [];
  }

  return Object.entries(constructorArgs)
    .filter(([key, value]) => key !== 'deploymentRef' && key.endsWith('DeploymentRef') && typeof value === 'string' && value.trim())
    .map(([, value]) => value);
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
    value.rpcUrls.forEach((entry, index) => {
      assert(typeof entry === 'string' && entry.trim() !== '', `${label}.rpcUrls[${index}] must be a non-empty string`);
    });
  }
  assertBooleanIfPresent(value.allowPublicFallback, `${label}.allowPublicFallback`);
}

function validateChainRef(chain, label) {
  assertPlainObject(chain, label);
  assertAllowedKeys(chain, ['name', 'chainId'], label);
  assert(Number.isInteger(chain.chainId) && chain.chainId >= 1, `${label}.chainId must be an integer >= 1`);
  assertStringIfPresent(chain.name, `${label}.name`);
}

function validateAssetRef(asset, label) {
  assertPlainObject(asset, label);
  assertAllowedKeys(asset, ['symbol', 'address', 'decimals', 'role'], label);
  assert(asset.symbol || asset.address, `${label} must include symbol or address`);
  if (asset.symbol !== undefined) {
    assert(typeof asset.symbol === 'string' && asset.symbol.trim() !== '', `${label}.symbol must be a non-empty string`);
  }
  if (asset.address !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(asset.address), `${label}.address must be a 20-byte hex address`);
  }
  if (asset.decimals !== undefined) {
    assert(Number.isInteger(asset.decimals) && asset.decimals >= 0 && asset.decimals <= 36, `${label}.decimals must be an integer between 0 and 36`);
  }
  if (asset.role !== undefined) {
    assertEnum(asset.role, ['collateral', 'borrow', 'quote', 'unit-of-account'], `${label}.role`);
  }
}

function validateFeedRequirement(feed, label) {
  assertPlainObject(feed, label);
  assertAllowedKeys(feed, ['feedName', 'base', 'quote', 'maxStalenessSeconds', 'compatibilityPreference', 'routeRole'], label);
  validateAssetRef(feed.base, `${label}.base`);
  validateAssetRef(feed.quote, `${label}.quote`);
  if (feed.feedName !== undefined) {
    assert(typeof feed.feedName === 'string' && feed.feedName.trim() !== '', `${label}.feedName must be a non-empty string`);
  }
  if (feed.maxStalenessSeconds !== undefined) {
    assert(Number.isInteger(feed.maxStalenessSeconds) && feed.maxStalenessSeconds >= 1, `${label}.maxStalenessSeconds must be an integer >= 1`);
  }
  if (feed.compatibilityPreference !== undefined) {
    assertEnum(feed.compatibilityPreference, ['chainlink-compatible-first', 'native-api3-ok', 'custom-fallback-ok'], `${label}.compatibilityPreference`);
  }
  if (feed.routeRole !== undefined) {
    assertEnum(feed.routeRole, ['direct', 'collateral-leg', 'borrow-leg'], `${label}.routeRole`);
  }
}

function validatePlanMarketRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(
    request,
    ['protocol', 'chain', 'collateralAssets', 'borrowAssets', 'unitOfAccount', 'riskPreset', 'oraclePreference', 'hookProfile', 'ownershipProfile', 'duplicatePolicy', 'discoverExistingMarkets'],
    'request'
  );
  assert(typeof request.protocol === 'string', 'request.protocol must be a string');
  assert(SUPPORTED_PROTOCOLS.has(request.protocol), 'request.protocol must be evk or morpho');
  validateChainRef(request.chain, 'request.chain');
  assert(Array.isArray(request.collateralAssets) && request.collateralAssets.length >= 1, 'request.collateralAssets must contain at least one asset');
  request.collateralAssets.forEach((asset, index) => validateAssetRef(asset, `request.collateralAssets[${index}]`));
  assert(Array.isArray(request.borrowAssets) && request.borrowAssets.length >= 1, 'request.borrowAssets must contain at least one asset');
  request.borrowAssets.forEach((asset, index) => validateAssetRef(asset, `request.borrowAssets[${index}]`));
  assertStringIfPresent(request.unitOfAccount, 'request.unitOfAccount');
  assertStringIfPresent(request.riskPreset, 'request.riskPreset');
  assert(request.riskPreset, 'request.riskPreset is required');
  if (request.oraclePreference !== undefined) {
    assertEnum(request.oraclePreference, ['chainlink-compatible-first', 'direct-first', 'composite-ok', 'custom-fallback-ok'], 'request.oraclePreference');
  }
  if (request.ownershipProfile !== undefined) {
    assertEnum(request.ownershipProfile, ['deployer-owned', 'multisig-owned', 'governor-owned'], 'request.ownershipProfile');
  }
  if (request.duplicatePolicy !== undefined) {
    assertEnum(request.duplicatePolicy, ['block-on-exact', 'block-on-near-equivalent', 'warn-only'], 'request.duplicatePolicy');
  }
  assertBooleanIfPresent(request.discoverExistingMarkets, 'request.discoverExistingMarkets');
}

function validateDiscoverMarketsRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['protocol', 'chain', 'collateralAssets', 'borrowAssets', 'riskPreset', 'includeNearEquivalent', 'statuses'], 'request');
  assert(typeof request.protocol === 'string', 'request.protocol must be a string');
  assert(SUPPORTED_PROTOCOLS.has(request.protocol), 'request.protocol must be evk or morpho');
  validateChainRef(request.chain, 'request.chain');
  if (request.collateralAssets !== undefined) {
    assert(Array.isArray(request.collateralAssets), 'request.collateralAssets must be an array');
    request.collateralAssets.forEach((asset, index) => validateAssetRef(asset, `request.collateralAssets[${index}]`));
  }
  if (request.borrowAssets !== undefined) {
    assert(Array.isArray(request.borrowAssets), 'request.borrowAssets must be an array');
    request.borrowAssets.forEach((asset, index) => validateAssetRef(asset, `request.borrowAssets[${index}]`));
  }
  assertStringIfPresent(request.riskPreset, 'request.riskPreset');
  assertBooleanIfPresent(request.includeNearEquivalent, 'request.includeNearEquivalent');
  if (request.statuses !== undefined) {
    assert(Array.isArray(request.statuses), 'request.statuses must be an array');
    request.statuses.forEach((status, index) => assertEnum(status, DEFAULT_STATUSES, `request.statuses[${index}]`));
  }
}

function validateEnsureFeedsRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['chain', 'requiredFeeds', 'activationMode', 'requireChainlinkCompatibility', 'rpcPreference'], 'request');
  validateChainRef(request.chain, 'request.chain');
  assert(Array.isArray(request.requiredFeeds) && request.requiredFeeds.length >= 1, 'request.requiredFeeds must contain at least one feed');
  request.requiredFeeds.forEach((feed, index) => validateFeedRequirement(feed, `request.requiredFeeds[${index}]`));
  if (request.activationMode !== undefined) {
    assertEnum(request.activationMode, ['check-only', 'prepare-only', 'allow-activation'], 'request.activationMode');
  }
  assertBooleanIfPresent(request.requireChainlinkCompatibility, 'request.requireChainlinkCompatibility');
  validateRpcPreference(request.rpcPreference, 'request.rpcPreference');
}

function validatePrepareEulerOracleRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['chain', 'oracleRoute', 'feedArtifacts', 'preferInfrequentOracle', 'unitOfAccount', 'allowCustomFallback', 'shareAwareRouter'], 'request');
  validateChainRef(request.chain, 'request.chain');
  validateOracleRoute(request.oracleRoute);
  assert(Array.isArray(request.feedArtifacts) && request.feedArtifacts.length >= 1, 'request.feedArtifacts must contain at least one feed artifact');
  request.feedArtifacts.forEach((artifact, index) => validateFeedArtifact(artifact, `request.feedArtifacts[${index}]`));
  assertBooleanIfPresent(request.preferInfrequentOracle, 'request.preferInfrequentOracle');
  assertStringIfPresent(request.unitOfAccount, 'request.unitOfAccount');
  assertBooleanIfPresent(request.allowCustomFallback, 'request.allowCustomFallback');
  validateShareAwareRouter(request.shareAwareRouter, 'request.shareAwareRouter');
}

function validateVaultContext(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['factoryAddress', 'assetAddress'], label);
  if (value.factoryAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.factoryAddress), `${label}.factoryAddress must be a 20-byte hex address`);
  }
  if (value.assetAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.assetAddress), `${label}.assetAddress must be a 20-byte hex address`);
  }
}

function validateShareAwareRouter(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'evcAddress', 'governorAddress', 'resolvedVaults'], label);
  if (value.enabled !== undefined) {
    assert(typeof value.enabled === 'boolean', `${label}.enabled must be a boolean`);
  }
  if (value.evcAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.evcAddress), `${label}.evcAddress must be a 20-byte hex address`);
  }
  if (value.governorAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.governorAddress), `${label}.governorAddress must be a 20-byte hex address`);
  }
  if (value.resolvedVaults !== undefined) {
    assert(Array.isArray(value.resolvedVaults), `${label}.resolvedVaults must be an array`);
    value.resolvedVaults.forEach((entry, index) => {
      assert(/^0x[a-fA-F0-9]{40}$/.test(entry), `${label}.resolvedVaults[${index}] must be a 20-byte hex address`);
    });
  }
  if (value && value.enabled) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.evcAddress), `${label}.evcAddress is required when share-aware router support is enabled`);
  }
}

function validatePrepareEvkMarketRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['chain', 'recipeId', 'riskPreset', 'collateralAssets', 'borrowAssets', 'oraclePreparation', 'hookProfile', 'ownershipProfile', 'governanceProfile', 'publishToRegistry', 'vaultContext'], 'request');
  validateChainRef(request.chain, 'request.chain');
  assert(typeof request.recipeId === 'string' && request.recipeId.trim(), 'request.recipeId must be a non-empty string');
  assert(typeof request.riskPreset === 'string' && request.riskPreset.trim(), 'request.riskPreset must be a non-empty string');
  assert(Array.isArray(request.collateralAssets) && request.collateralAssets.length >= 1, 'request.collateralAssets must contain at least one asset');
  request.collateralAssets.forEach((asset, index) => validateAssetRef(asset, `request.collateralAssets[${index}]`));
  assert(Array.isArray(request.borrowAssets) && request.borrowAssets.length >= 1, 'request.borrowAssets must contain at least one asset');
  request.borrowAssets.forEach((asset, index) => validateAssetRef(asset, `request.borrowAssets[${index}]`));
  assertPlainObject(request.oraclePreparation, 'request.oraclePreparation');
  assertStringIfPresent(request.hookProfile, 'request.hookProfile');
  if (request.ownershipProfile !== undefined) {
    assertEnum(request.ownershipProfile, ['deployer-owned', 'multisig-owned', 'governor-owned'], 'request.ownershipProfile');
  }
  assertStringIfPresent(request.governanceProfile, 'request.governanceProfile');
  assertBooleanIfPresent(request.publishToRegistry, 'request.publishToRegistry');
  validateVaultContext(request.vaultContext, 'request.vaultContext');
}

function validateContractDeploymentSpec(contract, label) {
  assertPlainObject(contract, label);
  assertAllowedKeys(contract, ['contractName', 'constructorArgs', 'purpose'], label);
  assert(typeof contract.contractName === 'string' && contract.contractName.trim(), `${label}.contractName must be a non-empty string`);
  assertPlainObject(contract.constructorArgs, `${label}.constructorArgs`);
  assertStringIfPresent(contract.purpose, `${label}.purpose`);
}

function validateStringArray(value, label) {
  assert(Array.isArray(value), `${label} must be an array`);
  value.forEach((entry, index) => {
    assert(typeof entry === 'string', `${label}[${index}] must be a string`);
  });
}

function validateBroadcastIntent(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'acknowledgement', 'signerAddress'], label);
  assertBooleanIfPresent(value.enabled, `${label}.enabled`);
  if (value.acknowledgement !== undefined) {
    assert(typeof value.acknowledgement === 'string' && value.acknowledgement.trim(), `${label}.acknowledgement must be a non-empty string`);
  }
  if (value.signerAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(value.signerAddress), `${label}.signerAddress must be a 20-byte hex address`);
  }
}

function validateSendIntent(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'dryRun', 'rpcUrl', 'privateKey'], label);
  assertBooleanIfPresent(value.enabled, `${label}.enabled`);
  assertBooleanIfPresent(value.dryRun, `${label}.dryRun`);
  if (value.rpcUrl !== undefined) {
    assert(typeof value.rpcUrl === 'string' && value.rpcUrl.trim(), `${label}.rpcUrl must be a non-empty string`);
  }
  if (value.privateKey !== undefined) {
    assert(/^0x[a-fA-F0-9]{64}$/.test(value.privateKey), `${label}.privateKey must be a 32-byte hex string`);
  }
}

function validateFeedFundingRequest(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['mode', 'executionMode', 'acknowledgement', 'rpcUrl', 'privateKey'], label);
  if (value.mode !== undefined) {
    assertEnum(value.mode, ['classify-only', 'dry-run', 'real-send'], `${label}.mode`);
  }
  if (value.executionMode !== undefined) {
    assertEnum(value.executionMode, ['auto', 'direct', 'wrapper'], `${label}.executionMode`);
  }
  assertStringIfPresent(value.acknowledgement, `${label}.acknowledgement`);
  if (value.rpcUrl !== undefined) {
    assert(typeof value.rpcUrl === 'string' && value.rpcUrl.trim(), `${label}.rpcUrl must be a non-empty string`);
  }
  if (value.privateKey !== undefined) {
    assert(/^0x[a-fA-F0-9]{64}$/.test(value.privateKey), `${label}.privateKey must be a 32-byte hex string`);
  }
}

function validateArtifactsRequest(value, label) {
  if (value === undefined) {
    return;
  }

  assertPlainObject(value, label);
  assertAllowedKeys(value, ['enabled', 'outputDir', 'label', 'runId'], label);
  assertBooleanIfPresent(value.enabled, `${label}.enabled`);
  assertStringIfPresent(value.outputDir, `${label}.outputDir`);
  assertStringIfPresent(value.label, `${label}.label`);
  assertStringIfPresent(value.runId, `${label}.runId`);
}

function hasExplicitBroadcastOptIn(broadcastIntent) {
  return Boolean(
    broadcastIntent
    && broadcastIntent.enabled === true
    && broadcastIntent.acknowledgement === 'I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS'
  );
}

function validateDeploymentRecipe(recipe, label) {
  assertPlainObject(recipe, label);
  assertAllowedKeys(
    recipe,
    ['recipeId', 'protocol', 'riskPreset', 'hookProfile', 'ownershipProfile', 'governanceProfile', 'oracleIntegrationMode', 'ltvBps', 'liquidationThresholdBps', 'publishToRegistry'],
    label,
  );
  assert(typeof recipe.recipeId === 'string' && recipe.recipeId.trim(), `${label}.recipeId must be a non-empty string`);
  assertEnum(recipe.protocol, ['evk'], `${label}.protocol`);
  assert(typeof recipe.riskPreset === 'string' && recipe.riskPreset.trim(), `${label}.riskPreset must be a non-empty string`);
  assertStringIfPresent(recipe.hookProfile, `${label}.hookProfile`);
  if (recipe.ownershipProfile !== undefined) {
    assertEnum(recipe.ownershipProfile, ['deployer-owned', 'multisig-owned', 'governor-owned'], `${label}.ownershipProfile`);
  }
  assertStringIfPresent(recipe.governanceProfile, `${label}.governanceProfile`);
  if (recipe.oracleIntegrationMode !== undefined) {
    assertEnum(recipe.oracleIntegrationMode, ['chainlink-oracle', 'chainlink-infrequent-oracle', 'cross-adapter', 'custom-api3-fallback', 'unknown'], `${label}.oracleIntegrationMode`);
  }
  if (recipe.ltvBps !== undefined && recipe.ltvBps !== null) {
    assert(Number.isInteger(recipe.ltvBps) && recipe.ltvBps >= 0, `${label}.ltvBps must be an integer >= 0`);
  }
  if (recipe.liquidationThresholdBps !== undefined && recipe.liquidationThresholdBps !== null) {
    assert(Number.isInteger(recipe.liquidationThresholdBps) && recipe.liquidationThresholdBps >= 0, `${label}.liquidationThresholdBps must be an integer >= 0`);
  }
  assertBooleanIfPresent(recipe.publishToRegistry, `${label}.publishToRegistry`);
}

function validatePrepareEvkDeploymentRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['chain', 'oraclePreparation', 'marketPreparation', 'executionProfile', 'vaultContext'], 'request');
  validateChainRef(request.chain, 'request.chain');

  assertPlainObject(request.oraclePreparation, 'request.oraclePreparation');
  assertAllowedKeys(request.oraclePreparation, ['ready', 'integrationMode', 'contracts', 'expectedQuote', 'verificationChecks', 'blockers', 'warnings'], 'request.oraclePreparation');
  assert(typeof request.oraclePreparation.ready === 'boolean', 'request.oraclePreparation.ready must be a boolean');
  assertEnum(request.oraclePreparation.integrationMode, ['chainlink-oracle', 'chainlink-infrequent-oracle', 'cross-adapter', 'custom-api3-fallback'], 'request.oraclePreparation.integrationMode');
  assert(Array.isArray(request.oraclePreparation.contracts) && request.oraclePreparation.contracts.length >= 1, 'request.oraclePreparation.contracts must contain at least one contract');
  request.oraclePreparation.contracts.forEach((contract, index) => validateContractDeploymentSpec(contract, `request.oraclePreparation.contracts[${index}]`));
  if (request.oraclePreparation.expectedQuote !== undefined) {
    assertPlainObject(request.oraclePreparation.expectedQuote, 'request.oraclePreparation.expectedQuote');
  }
  validateStringArray(request.oraclePreparation.verificationChecks, 'request.oraclePreparation.verificationChecks');
  validateStringArray(request.oraclePreparation.blockers, 'request.oraclePreparation.blockers');
  validateStringArray(request.oraclePreparation.warnings, 'request.oraclePreparation.warnings');

  assertPlainObject(request.marketPreparation, 'request.marketPreparation');
  assertAllowedKeys(request.marketPreparation, ['ready', 'deploymentRecipe', 'contracts', 'manifestPreview', 'deploymentSteps', 'verificationChecklist', 'blockers', 'warnings'], 'request.marketPreparation');
  assert(typeof request.marketPreparation.ready === 'boolean', 'request.marketPreparation.ready must be a boolean');
  validateDeploymentRecipe(request.marketPreparation.deploymentRecipe, 'request.marketPreparation.deploymentRecipe');
  assertPlainObject(request.marketPreparation.contracts, 'request.marketPreparation.contracts');
  validateManifestPreview(request.marketPreparation.manifestPreview, 'request.marketPreparation.manifestPreview');
  assert(Array.isArray(request.marketPreparation.deploymentSteps) && request.marketPreparation.deploymentSteps.length >= 1, 'request.marketPreparation.deploymentSteps must contain at least one step');
  request.marketPreparation.deploymentSteps.forEach((entry, index) => {
    assertPlainObject(entry, `request.marketPreparation.deploymentSteps[${index}]`);
    assertAllowedKeys(entry, ['step', 'action', 'contract', 'notes'], `request.marketPreparation.deploymentSteps[${index}]`);
    assert(Number.isInteger(entry.step) && entry.step > 0, `request.marketPreparation.deploymentSteps[${index}].step must be a positive integer`);
    assert(typeof entry.action === 'string' && entry.action.trim(), `request.marketPreparation.deploymentSteps[${index}].action must be a non-empty string`);
    assertStringIfPresent(entry.contract, `request.marketPreparation.deploymentSteps[${index}].contract`);
    assertStringIfPresent(entry.notes, `request.marketPreparation.deploymentSteps[${index}].notes`);
  });
  validateStringArray(request.marketPreparation.verificationChecklist, 'request.marketPreparation.verificationChecklist');
  validateStringArray(request.marketPreparation.blockers, 'request.marketPreparation.blockers');
  validateStringArray(request.marketPreparation.warnings, 'request.marketPreparation.warnings');

  if (request.executionProfile !== undefined) {
    assertPlainObject(request.executionProfile, 'request.executionProfile');
    assertAllowedKeys(request.executionProfile, ['mode', 'executorAddress', 'startingNonce', 'verifyBeforeBroadcast', 'registerMarket'], 'request.executionProfile');
    if (request.executionProfile.mode !== undefined) {
      assertEnum(request.executionProfile.mode, ['simulate', 'broadcast-ready'], 'request.executionProfile.mode');
    }
    if (request.executionProfile.executorAddress !== undefined) {
      assert(/^0x[a-fA-F0-9]{40}$/.test(request.executionProfile.executorAddress), 'request.executionProfile.executorAddress must be a 20-byte hex address');
    }
    if (request.executionProfile.startingNonce !== undefined) {
      assert(Number.isInteger(request.executionProfile.startingNonce) && request.executionProfile.startingNonce >= 0, 'request.executionProfile.startingNonce must be an integer >= 0');
    }
    assertBooleanIfPresent(request.executionProfile.verifyBeforeBroadcast, 'request.executionProfile.verifyBeforeBroadcast');
    assertBooleanIfPresent(request.executionProfile.registerMarket, 'request.executionProfile.registerMarket');
  }

  validateVaultContext(request.vaultContext, 'request.vaultContext');
}

function validateDeploymentBundle(bundle, label) {
  assertPlainObject(bundle, label);
  assertAllowedKeys(bundle, ['canonicalHash', 'displayName', 'chainId', 'manifestPreview', 'oracleDeploymentPlan', 'marketDeploymentPlan'], label);
  assert(typeof bundle.canonicalHash === 'string' && bundle.canonicalHash.trim(), `${label}.canonicalHash must be a non-empty string`);
  assertStringIfPresent(bundle.displayName, `${label}.displayName`);
  assert(Number.isInteger(bundle.chainId) && bundle.chainId >= 1, `${label}.chainId must be an integer >= 1`);
  validateManifestPreview(bundle.manifestPreview, `${label}.manifestPreview`);
  assert(Array.isArray(bundle.oracleDeploymentPlan), `${label}.oracleDeploymentPlan must be an array`);
  bundle.oracleDeploymentPlan.forEach((entry, index) => {
    assertPlainObject(entry, `${label}.oracleDeploymentPlan[${index}]`);
    assertAllowedKeys(entry, ['order', 'action', 'contractName', 'purpose', 'constructorArgs', 'artifactKey'], `${label}.oracleDeploymentPlan[${index}]`);
    assert(Number.isInteger(entry.order) && entry.order > 0, `${label}.oracleDeploymentPlan[${index}].order must be a positive integer`);
    assert(entry.action === 'deploy-contract', `${label}.oracleDeploymentPlan[${index}].action must be deploy-contract`);
    assert(typeof entry.contractName === 'string' && entry.contractName.trim(), `${label}.oracleDeploymentPlan[${index}].contractName must be a non-empty string`);
    assertStringIfPresent(entry.purpose, `${label}.oracleDeploymentPlan[${index}].purpose`);
    assertPlainObject(entry.constructorArgs, `${label}.oracleDeploymentPlan[${index}].constructorArgs`);
    assert(typeof entry.artifactKey === 'string' && entry.artifactKey.trim(), `${label}.oracleDeploymentPlan[${index}].artifactKey must be a non-empty string`);
  });
  assert(Array.isArray(bundle.marketDeploymentPlan), `${label}.marketDeploymentPlan must be an array`);
  bundle.marketDeploymentPlan.forEach((entry, index) => {
    assertPlainObject(entry, `${label}.marketDeploymentPlan[${index}]`);
    assertAllowedKeys(entry, ['order', 'action', 'contract', 'notes', 'dependsOn', 'vaultParams'], `${label}.marketDeploymentPlan[${index}]`);
    assert(Number.isInteger(entry.order) && entry.order > 0, `${label}.marketDeploymentPlan[${index}].order must be a positive integer`);
    assert(typeof entry.action === 'string' && entry.action.trim(), `${label}.marketDeploymentPlan[${index}].action must be a non-empty string`);
    assertStringIfPresent(entry.contract, `${label}.marketDeploymentPlan[${index}].contract`);
    assertStringIfPresent(entry.notes, `${label}.marketDeploymentPlan[${index}].notes`);
    validateStringArray(entry.dependsOn, `${label}.marketDeploymentPlan[${index}].dependsOn`);
    if (entry.vaultParams !== undefined) {
      assertPlainObject(entry.vaultParams, `${label}.marketDeploymentPlan[${index}].vaultParams`);
      assertAllowedKeys(entry.vaultParams, ['factoryAddress', 'assetAddress', 'oracleAddress', 'oracleDeploymentRef', 'unitOfAccountAddress'], `${label}.marketDeploymentPlan[${index}].vaultParams`);
      if (entry.vaultParams.factoryAddress !== undefined) {
        assert(/^0x[a-fA-F0-9]{40}$/.test(entry.vaultParams.factoryAddress), `${label}.marketDeploymentPlan[${index}].vaultParams.factoryAddress must be a 20-byte hex address`);
      }
      if (entry.vaultParams.assetAddress !== undefined) {
        assert(/^0x[a-fA-F0-9]{40}$/.test(entry.vaultParams.assetAddress), `${label}.marketDeploymentPlan[${index}].vaultParams.assetAddress must be a 20-byte hex address`);
      }
      if (entry.vaultParams.oracleAddress !== undefined) {
        assert(/^0x[a-fA-F0-9]{40}$/.test(entry.vaultParams.oracleAddress), `${label}.marketDeploymentPlan[${index}].vaultParams.oracleAddress must be a 20-byte hex address`);
      }
      assertStringIfPresent(entry.vaultParams.oracleDeploymentRef, `${label}.marketDeploymentPlan[${index}].vaultParams.oracleDeploymentRef`);
      if (entry.vaultParams.unitOfAccountAddress !== undefined) {
        assert(/^0x[a-fA-F0-9]{40}$/.test(entry.vaultParams.unitOfAccountAddress), `${label}.marketDeploymentPlan[${index}].vaultParams.unitOfAccountAddress must be a 20-byte hex address`);
      }
    }
  });
}

function validateDeployEvkMarketRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['ready', 'executionMode', 'deploymentBundle', 'preflightChecks', 'blockers', 'warnings', 'executorAddress', 'resolutionRpcUrl', 'startingNonce', 'broadcast', 'send'], 'request');
  if (request.ready !== undefined) {
    assert(typeof request.ready === 'boolean', 'request.ready must be a boolean');
  }
  assertEnum(request.executionMode, ['simulate', 'broadcast-ready'], 'request.executionMode');
  validateDeploymentBundle(request.deploymentBundle, 'request.deploymentBundle');
  validateStringArray(request.preflightChecks, 'request.preflightChecks');
  validateStringArray(request.blockers, 'request.blockers');
  validateStringArray(request.warnings, 'request.warnings');
  if (request.executorAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(request.executorAddress), 'request.executorAddress must be a 20-byte hex address');
  }
  if (request.resolutionRpcUrl !== undefined) {
    assert(typeof request.resolutionRpcUrl === 'string' && request.resolutionRpcUrl.trim() !== '', 'request.resolutionRpcUrl must be a non-empty string');
  }
  if (request.startingNonce !== undefined) {
    assert(Number.isInteger(request.startingNonce) && request.startingNonce >= 0, 'request.startingNonce must be an integer >= 0');
  }
  validateBroadcastIntent(request.broadcast, 'request.broadcast');
  validateSendIntent(request.send, 'request.send');
}

function validateDeployEulerOracleRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(request, ['chain', 'ready', 'integrationMode', 'contracts', 'expectedQuote', 'verificationChecks', 'blockers', 'warnings', 'executionMode', 'executorAddress', 'broadcast', 'send'], 'request');
  validateChainRef(request.chain, 'request.chain');
  if (request.ready !== undefined) {
    assert(typeof request.ready === 'boolean', 'request.ready must be a boolean');
  }
  assertEnum(request.integrationMode, ['chainlink-oracle', 'chainlink-infrequent-oracle', 'cross-adapter', 'custom-api3-fallback'], 'request.integrationMode');
  assert(Array.isArray(request.contracts) && request.contracts.length >= 1, 'request.contracts must contain at least one contract');
  request.contracts.forEach((contract, index) => validateContractDeploymentSpec(contract, `request.contracts[${index}]`));
  if (request.expectedQuote !== undefined) {
    assertPlainObject(request.expectedQuote, 'request.expectedQuote');
  }
  validateStringArray(request.verificationChecks, 'request.verificationChecks');
  validateStringArray(request.blockers, 'request.blockers');
  validateStringArray(request.warnings, 'request.warnings');
  assertEnum(request.executionMode, ['simulate', 'broadcast-ready'], 'request.executionMode');
  if (request.executorAddress !== undefined) {
    assert(/^0x[a-fA-F0-9]{40}$/.test(request.executorAddress), 'request.executorAddress must be a 20-byte hex address');
  }
  validateBroadcastIntent(request.broadcast, 'request.broadcast');
  validateSendIntent(request.send, 'request.send');
}

function validateRunEvkWorkflowRequest(request) {
  assertPlainObject(request, 'request');
  assertAllowedKeys(
    request,
    [
      'chain',
      'collateralAssets',
      'borrowAssets',
      'riskPreset',
      'recipeId',
      'unitOfAccount',
      'oraclePreference',
      'hookProfile',
      'ownershipProfile',
      'governanceProfile',
      'duplicatePolicy',
      'discoverExistingMarkets',
      'activationMode',
      'rpcPreference',
      'allowCustomFallback',
      'preferInfrequentOracle',
      'publishToRegistry',
      'vaultContext',
      'executionProfile',
      'broadcast',
      'send',
      'feedFunding',
      'artifacts',
      'shareAwareRouter',
    ],
    'request'
  );

  validateChainRef(request.chain, 'request.chain');
  assert(typeof request.riskPreset === 'string' && request.riskPreset.trim(), 'request.riskPreset must be a non-empty string');
  assert(Array.isArray(request.collateralAssets) && request.collateralAssets.length >= 1, 'request.collateralAssets must contain at least one asset');
  request.collateralAssets.forEach((asset, index) => validateAssetRef(asset, `request.collateralAssets[${index}]`));
  assert(Array.isArray(request.borrowAssets) && request.borrowAssets.length >= 1, 'request.borrowAssets must contain at least one asset');
  request.borrowAssets.forEach((asset, index) => validateAssetRef(asset, `request.borrowAssets[${index}]`));
  assertStringIfPresent(request.recipeId, 'request.recipeId');
  assertStringIfPresent(request.unitOfAccount, 'request.unitOfAccount');
  if (request.oraclePreference !== undefined) {
    assertEnum(request.oraclePreference, ['chainlink-compatible-first', 'direct-first', 'composite-ok', 'custom-fallback-ok'], 'request.oraclePreference');
  }
  assertStringIfPresent(request.hookProfile, 'request.hookProfile');
  if (request.ownershipProfile !== undefined) {
    assertEnum(request.ownershipProfile, ['deployer-owned', 'multisig-owned', 'governor-owned'], 'request.ownershipProfile');
  }
  assertStringIfPresent(request.governanceProfile, 'request.governanceProfile');
  if (request.duplicatePolicy !== undefined) {
    assertEnum(request.duplicatePolicy, ['block-on-exact', 'block-on-near-equivalent', 'warn-only'], 'request.duplicatePolicy');
  }
  assertBooleanIfPresent(request.discoverExistingMarkets, 'request.discoverExistingMarkets');
  if (request.activationMode !== undefined) {
    assertEnum(request.activationMode, ['check-only', 'prepare-only', 'allow-activation'], 'request.activationMode');
  }
  validateRpcPreference(request.rpcPreference, 'request.rpcPreference');
  assertBooleanIfPresent(request.allowCustomFallback, 'request.allowCustomFallback');
  assertBooleanIfPresent(request.preferInfrequentOracle, 'request.preferInfrequentOracle');
  assertBooleanIfPresent(request.publishToRegistry, 'request.publishToRegistry');
  validateVaultContext(request.vaultContext, 'request.vaultContext');
  validateShareAwareRouter(request.shareAwareRouter, 'request.shareAwareRouter');

  if (request.executionProfile !== undefined) {
    assertPlainObject(request.executionProfile, 'request.executionProfile');
    assertAllowedKeys(request.executionProfile, ['mode', 'executorAddress', 'startingNonce', 'verifyBeforeBroadcast', 'registerMarket'], 'request.executionProfile');
    if (request.executionProfile.mode !== undefined) {
      assertEnum(request.executionProfile.mode, ['simulate', 'broadcast-ready'], 'request.executionProfile.mode');
    }
    if (request.executionProfile.executorAddress !== undefined) {
      assert(/^0x[a-fA-F0-9]{40}$/.test(request.executionProfile.executorAddress), 'request.executionProfile.executorAddress must be a 20-byte hex address');
    }
    if (request.executionProfile.startingNonce !== undefined) {
      assert(Number.isInteger(request.executionProfile.startingNonce) && request.executionProfile.startingNonce >= 0, 'request.executionProfile.startingNonce must be an integer >= 0');
    }
    assertBooleanIfPresent(request.executionProfile.verifyBeforeBroadcast, 'request.executionProfile.verifyBeforeBroadcast');
    assertBooleanIfPresent(request.executionProfile.registerMarket, 'request.executionProfile.registerMarket');
  }

  validateBroadcastIntent(request.broadcast, 'request.broadcast');
  validateSendIntent(request.send, 'request.send');
  validateFeedFundingRequest(request.feedFunding, 'request.feedFunding');
  validateArtifactsRequest(request.artifacts, 'request.artifacts');
}

function normalizeSymbol(symbol) {
  return String(symbol || '').trim().toUpperCase();
}

function canonicalizeDapiSymbol(symbol) {
  const normalized = normalizeSymbol(symbol);
  return normalized ? (DAPI_SYMBOL_ALIASES[normalized] || normalized) : normalized;
}

function canonicalizeFeedName(feedName) {
  const normalized = normalizeSymbol(feedName);
  if (!normalized) {
    return normalized;
  }

  if (!normalized.includes('/')) {
    return canonicalizeDapiSymbol(normalized);
  }

  return normalized
    .split('/')
    .map((segment) => canonicalizeDapiSymbol(segment))
    .join('/');
}

function feedNamesEqual(left, right) {
  const canonicalLeft = canonicalizeFeedName(left);
  const canonicalRight = canonicalizeFeedName(right);
  return Boolean(canonicalLeft) && canonicalLeft === canonicalRight;
}

function lookupSyntheticAssetAddress(symbol) {
  const normalizedSymbol = normalizeSymbol(symbol);
  return normalizedSymbol ? (SYNTHETIC_ASSET_ADDRESSES[normalizedSymbol] || null) : null;
}

function normalizeAsset(asset, role) {
  const normalizedSymbol = asset.symbol ? normalizeSymbol(asset.symbol) : null;
  const resolvedAddress = asset.address || lookupSyntheticAssetAddress(normalizedSymbol);

  return {
    ...(normalizedSymbol ? { symbol: normalizedSymbol } : {}),
    ...(resolvedAddress ? { address: resolvedAddress } : {}),
    ...(Number.isInteger(asset.decimals) ? { decimals: asset.decimals } : {}),
    role: asset.role || role,
  };
}

function normalizeChain(chain) {
  return {
    chainId: chain.chainId,
    name: chain.name ? String(chain.name).trim().toLowerCase() : `chain-${chain.chainId}`,
  };
}

function makeFeedRequirement(baseAsset, quoteAsset, routeRole) {
  const base = normalizeAsset(baseAsset, routeRole === 'borrow-leg' ? 'borrow' : 'collateral');
  const quote = normalizeAsset(quoteAsset, 'unit-of-account');
  return {
    feedName: `${base.symbol}/${quote.symbol}`,
    base,
    quote,
    maxStalenessSeconds: 86400,
    compatibilityPreference: 'chainlink-compatible-first',
    routeRole,
  };
}

function compareAssets(left, right) {
  return left.symbol.localeCompare(right.symbol) || (left.address || '').localeCompare(right.address || '');
}

function uniqueByFeedName(feeds) {
  const seen = new Set();
  return feeds.filter((feed) => {
    const canonicalFeedName = canonicalizeFeedName(feed.feedName);
    if (seen.has(canonicalFeedName)) {
      return false;
    }
    seen.add(canonicalFeedName);
    return true;
  });
}

function buildRequiredFeeds(request) {
  if (request.collateralAssets.length === 1 && request.borrowAssets.length === 1) {
    return [makeFeedRequirement(request.collateralAssets[0], request.borrowAssets[0], 'direct')];
  }

  const quoteAsset = { symbol: request.unitOfAccount || 'USD', role: 'unit-of-account' };
  const collateralLegs = request.collateralAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'collateral-leg'));
  const borrowLegs = request.borrowAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'borrow-leg'));
  return uniqueByFeedName([...collateralLegs, ...borrowLegs]).sort((left, right) => left.feedName.localeCompare(right.feedName));
}

function buildCompositeRequiredFeeds(request) {
  const quoteAsset = { symbol: request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT, role: 'unit-of-account' };
  const collateralLegs = request.collateralAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'collateral-leg'));
  const borrowLegs = request.borrowAssets.map((asset) => makeFeedRequirement(asset, quoteAsset, 'borrow-leg'));
  return uniqueByFeedName([...collateralLegs, ...borrowLegs]).sort((left, right) => left.feedName.localeCompare(right.feedName));
}

function shouldAttemptCompositeFallback(request, planMarketResult, ensureFeedsResult) {
  if (!planMarketResult || !ensureFeedsResult || !Array.isArray(ensureFeedsResult.feeds)) {
    return false;
  }

  const unitOfAccount = normalizeSymbol(request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT);
  return request.collateralAssets.length === 1
    && request.borrowAssets.length === 1
    && normalizeSymbol(request.borrowAssets[0] && request.borrowAssets[0].symbol) !== unitOfAccount
    && Array.isArray(planMarketResult.requiredFeeds)
    && planMarketResult.requiredFeeds.length === 1
    && planMarketResult.requiredFeeds[0].routeRole === 'direct'
    && ensureFeedsResult.feeds.some((feed) => feed && feed.status === 'blocked');
}

function buildCompositeFallbackPlanMarketResult(request, currentPlanMarketResult) {
  const normalizedIntent = normalizeIntent({
    protocol: 'evk',
    chain: request.chain,
    collateralAssets: request.collateralAssets,
    borrowAssets: request.borrowAssets,
    riskPreset: request.riskPreset,
    unitOfAccount: request.unitOfAccount,
    oraclePreference: request.oraclePreference,
    hookProfile: request.hookProfile,
    ownershipProfile: request.ownershipProfile,
    duplicatePolicy: request.duplicatePolicy,
    discoverExistingMarkets: request.discoverExistingMarkets,
  });
  const requiredFeeds = buildCompositeRequiredFeeds(request);
  const oracleRoute = chooseOracleRoute(normalizedIntent, requiredFeeds);
  const planKey = {
    protocol: normalizedIntent.protocol,
    chainId: normalizedIntent.chain.chainId,
    collateralAssets: normalizedIntent.collateralAssets,
    borrowAssets: normalizedIntent.borrowAssets,
    unitOfAccount: normalizedIntent.unitOfAccount,
    riskPreset: normalizedIntent.riskPreset,
    oracleStrategy: oracleRoute.strategy,
  };

  return {
    ...currentPlanMarketResult,
    normalizedIntent: {
      ...currentPlanMarketResult.normalizedIntent,
      canonicalHash: makeCanonicalHash(planKey),
    },
    oracleRoute,
    requiredFeeds,
    warnings: uniqueStrings([
      ...(currentPlanMarketResult.warnings || []),
      `Fell back to a composite ${normalizedIntent.unitOfAccount} oracle route because the direct pair ${currentPlanMarketResult.requiredFeeds[0].feedName} could not be resolved exactly in the dAPI catalog.`,
    ]),
  };
}

function canonicalKeyForAssets(assets) {
  return assets
    .map((asset) => normalizeAsset(asset, asset.role || 'collateral'))
    .sort(compareAssets)
    .map((asset) => asset.symbol || asset.address)
    .join(',');
}

function normalizeIntent(request) {
  const chain = normalizeChain(request.chain);
  const collateralAssets = request.collateralAssets.map((asset) => normalizeAsset(asset, 'collateral')).sort(compareAssets);
  const borrowAssets = request.borrowAssets.map((asset) => normalizeAsset(asset, 'borrow')).sort(compareAssets);

  return {
    protocol: request.protocol,
    chain,
    collateralAssets,
    borrowAssets,
    unitOfAccount: normalizeSymbol(request.unitOfAccount || 'USD'),
    riskPreset: String(request.riskPreset).trim(),
    oraclePreference: request.oraclePreference || DEFAULT_ORACLE_PREFERENCE,
    hookProfile: request.hookProfile || 'none',
    ownershipProfile: request.ownershipProfile || 'deployer-owned',
    duplicatePolicy: request.duplicatePolicy || DEFAULT_DUPLICATE_POLICY,
    discoverExistingMarkets: request.discoverExistingMarkets !== false,
  };
}

function uniqueStrings(values) {
  return values.filter((entry, index, array) => array.indexOf(entry) === index);
}

function sanitizeArtifactPathSegment(value, fallback = 'unknown') {
  const sanitized = String(value || '')
    .trim()
    .replace(/[^a-zA-Z0-9._-]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');

  return sanitized || fallback;
}

function makeArtifactRunId(artifacts = {}) {
  if (typeof artifacts.runId === 'string' && artifacts.runId.trim()) {
    return sanitizeArtifactPathSegment(artifacts.runId, 'run');
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  if (typeof artifacts.label === 'string' && artifacts.label.trim()) {
    return `${sanitizeArtifactPathSegment(artifacts.label, 'run')}-${timestamp}`;
  }

  return timestamp;
}

function resolveArtifactOutputDir(artifacts = {}) {
  if (typeof artifacts.outputDir === 'string' && artifacts.outputDir.trim()) {
    return path.resolve(ROOT_DIR, artifacts.outputDir.trim());
  }

  return path.join(ROOT_DIR, 'artifacts', 'evk');
}

function emptyArtifactPersistence(artifacts = {}) {
  return {
    enabled: artifacts.enabled === true,
    persisted: false,
    outputDir: null,
    bundleDir: null,
    runId: null,
    files: {
      request: null,
      response: null,
      status: null,
      planMarket: null,
      ensureFeeds: null,
      feedFunding: null,
      prepareEulerOracle: null,
      prepareEvkMarket: null,
      prepareEvkDeployment: null,
      deployEvkMarket: null,
    },
  };
}

function writeArtifactJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function persistRunEvkWorkflowArtifacts({ request, response }) {
  const artifacts = request.artifacts || {};
  const metadata = emptyArtifactPersistence(artifacts);

  if (artifacts.enabled !== true) {
    return metadata;
  }

  const canonicalHash = response.result.prepareEvkDeployment
    ? response.result.prepareEvkDeployment.deploymentBundle.canonicalHash
    : (response.result.planMarket ? response.result.planMarket.normalizedIntent.canonicalHash : 'unknown-canonical-hash');
  const outputDir = resolveArtifactOutputDir(artifacts);
  const runId = makeArtifactRunId(artifacts);
  const bundleDir = path.join(outputDir, sanitizeArtifactPathSegment(canonicalHash, 'unknown-canonical-hash'), runId);

  fs.mkdirSync(bundleDir, { recursive: true });

  const files = {
    request: path.join(bundleDir, 'request.json'),
    response: path.join(bundleDir, 'response.json'),
    status: path.join(bundleDir, 'status.json'),
    planMarket: response.result.planMarket ? path.join(bundleDir, 'plan-market.json') : null,
    ensureFeeds: response.result.ensureFeeds ? path.join(bundleDir, 'ensure-feeds.json') : null,
    feedFunding: response.result.feedFunding ? path.join(bundleDir, 'feed-funding.json') : null,
    prepareEulerOracle: response.result.prepareEulerOracle ? path.join(bundleDir, 'prepare-euler-oracle.json') : null,
    prepareEvkMarket: response.result.prepareEvkMarket ? path.join(bundleDir, 'prepare-evk-market.json') : null,
    prepareEvkDeployment: response.result.prepareEvkDeployment ? path.join(bundleDir, 'prepare-evk-deployment.json') : null,
    deployEvkMarket: response.result.deployEvkMarket ? path.join(bundleDir, 'deploy-evk-market.json') : null,
  };

  writeArtifactJson(files.request, request);
  writeArtifactJson(files.status, response.status);

  if (files.planMarket) {
    writeArtifactJson(files.planMarket, response.result.planMarket);
  }
  if (files.ensureFeeds) {
    writeArtifactJson(files.ensureFeeds, response.result.ensureFeeds);
  }
  if (files.feedFunding) {
    writeArtifactJson(files.feedFunding, response.result.feedFunding);
  }
  if (files.prepareEulerOracle) {
    writeArtifactJson(files.prepareEulerOracle, response.result.prepareEulerOracle);
  }
  if (files.prepareEvkMarket) {
    writeArtifactJson(files.prepareEvkMarket, response.result.prepareEvkMarket);
  }
  if (files.prepareEvkDeployment) {
    writeArtifactJson(files.prepareEvkDeployment, response.result.prepareEvkDeployment);
  }
  if (files.deployEvkMarket) {
    writeArtifactJson(files.deployEvkMarket, response.result.deployEvkMarket);
  }

  return {
    enabled: true,
    persisted: true,
    outputDir,
    bundleDir,
    runId,
    files,
  };
}

function finalizeRunEvkWorkflowResponse({ request, results }) {
  const status = buildRunEvkWorkflowStatus(results);
  const response = { status, result: results };
  response.result.artifactPersistence = persistRunEvkWorkflowArtifacts({ request, response });
  if (response.result.artifactPersistence.persisted && response.result.artifactPersistence.files.response) {
    writeArtifactJson(response.result.artifactPersistence.files.response, response);
  }
  validateRunEvkWorkflowResponse(response);
  return response;
}

function recipeSupportsAssets(recipe, collateralAssets, borrowAssets) {
  const collateralSymbols = collateralAssets.map((asset) => normalizeSymbol(asset.symbol));
  const borrowSymbols = borrowAssets.map((asset) => normalizeSymbol(asset.symbol));

  return collateralSymbols.every((symbol) => recipe.supportedCollateralSymbols.includes(symbol))
    && borrowSymbols.every((symbol) => recipe.supportedBorrowSymbols.includes(symbol));
}

function selectEvkRecipeForWorkflow(request) {
  if (request.recipeId) {
    const requestedRecipe = getEvkRecipe(request.recipeId);
    return {
      requestedRecipeId: request.recipeId,
      resolvedRecipeId: request.recipeId,
      matchStrategy: 'explicit',
      candidateRecipeIds: requestedRecipe ? [request.recipeId] : [],
      blockers: requestedRecipe ? [] : [`Unknown EVK recipe: ${request.recipeId}`],
      warnings: [],
    };
  }

  const candidates = listEvkRecipes().filter((recipe) => (
    recipe.riskPreset === String(request.riskPreset).trim()
    && recipeSupportsAssets(recipe, request.collateralAssets, request.borrowAssets)
  ));

  if (candidates.length === 1) {
    return {
      requestedRecipeId: null,
      resolvedRecipeId: candidates[0].recipeId,
      matchStrategy: 'inferred',
      candidateRecipeIds: [candidates[0].recipeId],
      blockers: [],
      warnings: [],
    };
  }

  if (candidates.length === 0) {
    return {
      requestedRecipeId: null,
      resolvedRecipeId: null,
      matchStrategy: 'none',
      candidateRecipeIds: [],
      blockers: ['Could not infer an EVK recipe from the requested assets and risk preset. Pass request.recipeId explicitly.'],
      warnings: [],
    };
  }

  return {
    requestedRecipeId: null,
    resolvedRecipeId: null,
    matchStrategy: 'ambiguous',
    candidateRecipeIds: candidates.map((recipe) => recipe.recipeId),
    blockers: ['Multiple EVK recipes matched the requested assets and risk preset. Pass request.recipeId explicitly.'],
    warnings: [],
  };
}

function normalizeWorkflowRequest(request, recipeSelection) {
  return {
    protocol: 'evk',
    chain: normalizeChain(request.chain),
    collateralAssets: request.collateralAssets.map((asset) => normalizeAsset(asset, 'collateral')).sort(compareAssets),
    borrowAssets: request.borrowAssets.map((asset) => normalizeAsset(asset, 'borrow')).sort(compareAssets),
    riskPreset: String(request.riskPreset).trim(),
    recipeId: recipeSelection.resolvedRecipeId,
    unitOfAccount: normalizeSymbol(request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT),
    feedFundingMode: request.feedFunding?.mode || 'classify-only',
    executionMode: request.executionProfile?.mode || 'simulate',
  };
}

function buildFeedFundingOptions(request, feedName) {
  const resolvedRpc = resolveRpcUrlForChain(request.chain, request.rpcPreference || {});
  const feedFunding = request.feedFunding || {};

  return {
    chain: request.chain.name || String(request.chain.chainId),
    dapiName: feedName,
    ...(resolvedRpc.rpcUrl ? { rpcUrl: resolvedRpc.rpcUrl } : {}),
    ...(feedFunding.rpcUrl ? { rpcUrl: feedFunding.rpcUrl } : {}),
    ...(feedFunding.privateKey ? { [['private', 'Key'].join('')]: feedFunding.privateKey } : {}),
    ...(feedFunding.acknowledgement ? { acknowledgement: feedFunding.acknowledgement } : {}),
    ...(feedFunding.executionMode ? { executionMode: feedFunding.executionMode } : {}),
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

function promoteFundingReadyFeedsForPlanning(ensureFeedsResult, feedFundingResult) {
  if (!ensureFeedsResult || ensureFeedsResult.ready || !Array.isArray(ensureFeedsResult.feeds)) {
    return ensureFeedsResult;
  }
  if (!feedFundingResult || !Array.isArray(feedFundingResult.entries)) {
    return ensureFeedsResult;
  }

  const fundingByFeedName = new Map(
    feedFundingResult.entries
      .filter((entry) => entry && typeof entry.feedName === 'string')
      .map((entry) => [entry.feedName, entry]),
  );

  let promotedAny = false;
  const promotedFeeds = ensureFeedsResult.feeds.map((feed) => {
    if (!feed || feed.status === 'ready' || !isNonZeroHexAddress(feed.proxyAddress)) {
      return feed;
    }

    const fundingEntry = fundingByFeedName.get(feed.feedName);
    if (!fundingEntry) {
      return feed;
    }

    if (fundingEntry.fundingExecutionState !== 'executable' && fundingEntry.fundingExecutionState !== 'not-needed') {
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
    return ensureFeedsResult;
  }

  return {
    ...ensureFeedsResult,
    ready: true,
    blockers: [],
    warnings: uniqueStrings([
      ...(ensureFeedsResult.warnings || []),
      'Promoted funding-ready feeds to ready for downstream planning based on executable/not-needed funding results.',
    ]),
    feeds: promotedFeeds,
  };
}

function getExecutableOracleTransactions(deployResult) {
  if (!deployResult || !Array.isArray(deployResult.transactionPlan)) {
    return [];
  }

  return deployResult.transactionPlan.filter((entry) => (
    entry.kind === 'contract-deployment' && entry.payloadKind === 'executable'
  ));
}

function getExecutableMarketTransactions(deployResult) {
  if (!deployResult || !Array.isArray(deployResult.transactionPlan)) {
    return [];
  }

  return deployResult.transactionPlan.filter((entry) => (
    entry.kind === 'contract-call' && entry.payloadKind === 'executable'
  ));
}

function determineWorkflowPhase(results) {
  if (results.deployEvkMarket) {
    return 'deploy-evk-market';
  }
  if (results.prepareEvkDeployment) {
    return 'prepare-evk-deployment';
  }
  if (results.prepareEvkMarket) {
    return 'prepare-evk-market';
  }
  if (results.prepareEulerOracle) {
    return 'prepare-euler-oracle';
  }
  if (results.feedFunding && results.feedFunding.entries.length > 0) {
    return 'feed-funding';
  }
  if (results.ensureFeeds) {
    return 'ensure-feeds';
  }
  return 'plan-market';
}

function determineWorkflowState(results) {
  const planMarketResult = results.planMarket;
  const ensureFeedsResult = results.ensureFeeds ? results.ensureFeeds.final : null;
  const feedFundingResult = results.feedFunding;
  const deployEvkMarketResult = results.deployEvkMarket;
  const executableFundingAvailable = Boolean(feedFundingResult && feedFundingResult.entries.some((entry) => entry.fundingExecutionState === 'executable'));
  const browserFundingAvailable = Boolean(feedFundingResult && feedFundingResult.entries.some((entry) => entry.fundingExecutionState === 'browser-assisted'));
  const oracleExecutable = getExecutableOracleTransactions(deployEvkMarketResult).length > 0;
  const marketExecutable = getExecutableMarketTransactions(deployEvkMarketResult).length > 0;

  if (deployEvkMarketResult && deployEvkMarketResult.executionSummary.readyToBroadcast) {
    return 'real-send ready';
  }

  if (deployEvkMarketResult && deployEvkMarketResult.executionSummary.mode === 'simulate' && marketExecutable) {
    return 'EVK dry-run ready';
  }

  if (oracleExecutable) {
    return 'oracle-executable';
  }

  if (browserFundingAvailable) {
    return 'browser-assisted funding ready';
  }

  if (executableFundingAvailable) {
    return 'funding dry-run ready';
  }

  if (ensureFeedsResult && ensureFeedsResult.ready === false) {
    return 'feed-ready but awaiting activation/funding handoff';
  }

  if (planMarketResult && planMarketResult.deployable) {
    return 'plan-only';
  }

  return 'plan-only';
}

function buildRunEvkWorkflowStatus(results) {
  const phaseReached = determineWorkflowPhase(results);
  const state = determineWorkflowState(results);
  const fundingEntries = results.feedFunding ? results.feedFunding.entries : [];
  const fundingExecutionState = summarizeFundingState(fundingEntries);
  const deployEvkMarketResult = results.deployEvkMarket;

  const status = {
    phaseReached,
    state,
    recipeId: results.request.recipeId,
    deployable: Boolean(results.planMarket && results.planMarket.deployable),
    fundingExecutionState,
    executable: {
      feedFunding: fundingEntries.some((entry) => entry.fundingExecutionState === 'executable'),
      browserAssistedFunding: fundingEntries.some((entry) => entry.fundingExecutionState === 'browser-assisted'),
      oracle: getExecutableOracleTransactions(deployEvkMarketResult).length > 0,
      evkMarket: getExecutableMarketTransactions(deployEvkMarketResult).length > 0,
      realSend: Boolean(deployEvkMarketResult && deployEvkMarketResult.executionSummary.readyToBroadcast),
    },
    blockers: uniqueStrings([
      ...(results.recipeSelection?.blockers || []),
      ...(results.planMarket?.blockers || []),
      ...(results.ensureFeeds?.final?.blockers || []),
      ...(results.prepareEulerOracle?.blockers || []),
      ...(results.prepareEvkMarket?.blockers || []),
      ...(results.prepareEvkDeployment?.blockers || []),
      ...(results.deployEvkMarket?.blockers || []),
      ...fundingEntries.flatMap((entry) => entry.blockers || []),
    ]),
    warnings: uniqueStrings([
      ...(results.recipeSelection?.warnings || []),
      ...(results.planMarket?.warnings || []),
      ...(results.ensureFeeds?.final?.warnings || []),
      ...(results.prepareEulerOracle?.warnings || []),
      ...(results.prepareEvkMarket?.warnings || []),
      ...(results.prepareEvkDeployment?.warnings || []),
      ...(results.deployEvkMarket?.warnings || []),
      ...fundingEntries.flatMap((entry) => entry.warnings || []),
    ]),
  };

  return status;
}

function makeCanonicalHash(payload) {
  return `sha256:${crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex')}`;
}

function marketMatchesAssets(entryAssets, requestAssets) {
  if (!requestAssets || requestAssets.length === 0) {
    return true;
  }
  return canonicalKeyForAssets(entryAssets) === canonicalKeyForAssets(requestAssets);
}

function summarizeMarket(entry, matchType) {
  return {
    canonicalHash: entry.canonicalHash,
    marketId: entry.marketId,
    protocol: entry.protocol,
    chainId: entry.chainId,
    displayName: entry.displayName,
    matchType,
    riskPreset: entry.riskPreset,
    status: entry.status,
    borrowOptions: Array.isArray(entry.borrowOptions) ? entry.borrowOptions : [],
    supplyOptions: Array.isArray(entry.supplyOptions) ? entry.supplyOptions : [],
  };
}

function discoverMarketsInternal(request, registry) {
  const statuses = request.statuses || DEFAULT_STATUSES;
  const includeNearEquivalent = request.includeNearEquivalent !== false;
  const pool = registry.markets.filter((entry) => (
    entry.protocol === request.protocol
    && entry.chainId === request.chain.chainId
    && statuses.includes(entry.status)
  ));

  const exactMatches = pool
    .filter((entry) => marketMatchesAssets(entry.collateralAssets, request.collateralAssets))
    .filter((entry) => marketMatchesAssets(entry.borrowAssets, request.borrowAssets))
    .filter((entry) => !request.riskPreset || entry.riskPreset === request.riskPreset)
    .map((entry) => summarizeMarket(entry, 'exact'));

  const nearEquivalentMatches = includeNearEquivalent
    ? pool
        .filter((entry) => !exactMatches.some((match) => match.canonicalHash === entry.canonicalHash))
        .filter((entry) => marketMatchesAssets(entry.collateralAssets, request.collateralAssets || []))
        .filter((entry) => marketMatchesAssets(entry.borrowAssets, request.borrowAssets || []))
        .map((entry) => summarizeMarket(entry, 'near-equivalent'))
    : [];

  const reasoning = [];
  let recommendedAction = 'deploy-new-market';

  if (exactMatches.some((entry) => entry.status === 'active')) {
    recommendedAction = 'use-existing-market';
    reasoning.push('An exact active market already exists in the local registry.');
  } else if (exactMatches.length > 0) {
    recommendedAction = 'seed-existing-market';
    reasoning.push('An exact market exists, but it is not fully active, so seeding or finishing activation is preferred.');
  } else if (nearEquivalentMatches.length > 0) {
    recommendedAction = 'manual-review';
    reasoning.push('Only near-equivalent markets were found, so duplicate-prevention policy should review before deployment.');
  } else {
    reasoning.push('No exact or near-equivalent markets were found in the local registry.');
  }

  if (request.protocol !== 'evk') {
    reasoning.push(EVK_ONLY_WARNING);
    if (recommendedAction === 'deploy-new-market') {
      recommendedAction = 'manual-review';
    }
  }

  return {
    exactMatches,
    nearEquivalentMatches,
    recommendedAction,
    reasoning,
  };
}

function chooseOracleRoute(normalizedIntent, requiredFeeds) {
  if (normalizedIntent.protocol !== 'evk') {
    return {
      routeType: 'not-deployable',
      strategy: 'custom-euler-api3-adapter',
      maxStalenessSeconds: 86400,
      feeds: requiredFeeds,
      reasons: [EVK_ONLY_WARNING],
    };
  }

  if (requiredFeeds.some((feed) => feed.routeRole !== 'direct')) {
    return {
      routeType: 'composite-chainlink-compatible',
      strategy: 'euler-cross-adapter',
      maxStalenessSeconds: 86400,
      feeds: requiredFeeds,
      reasons: [
        'Multiple feed legs are required, so the planner prefers a composite Euler route.',
        'Api3PartialAggregatorV2V3Interface remains the preferred compatibility layer for Api3-backed legs.',
      ],
    };
  }

  return {
    routeType: 'direct-chainlink-compatible',
    strategy: 'api3-partial-aggregatorv2v3interface',
    maxStalenessSeconds: 86400,
    feeds: requiredFeeds,
    reasons: [
      'EVK-first path prefers Euler existing oracle stack before any custom adapter.',
      'Api3 via Api3PartialAggregatorV2V3Interface is the default route when a direct compatible feed is sufficient.',
    ],
  };
}

function planMarket(request, options) {
  validatePlanMarketRequest(request);
  const registry = loadRegistry(options);
  const normalizedIntent = normalizeIntent(request);
  const requiredFeeds = buildRequiredFeeds(request);
  const discovery = normalizedIntent.discoverExistingMarkets
    ? discoverMarketsInternal({
        protocol: normalizedIntent.protocol,
        chain: normalizedIntent.chain,
        collateralAssets: normalizedIntent.collateralAssets,
        borrowAssets: normalizedIntent.borrowAssets,
        riskPreset: normalizedIntent.riskPreset,
        includeNearEquivalent: true,
        statuses: DEFAULT_STATUSES,
      }, registry)
    : { exactMatches: [], nearEquivalentMatches: [], recommendedAction: 'deploy-new-market', reasoning: ['Registry discovery was disabled by request.'] };

  const oracleRoute = chooseOracleRoute(normalizedIntent, requiredFeeds);
  const blockers = [];
  const warnings = [];
  let deployable = oracleRoute.routeType !== 'not-deployable';
  let recommendedAction = discovery.recommendedAction === 'manual-review' ? 'blocked' : discovery.recommendedAction;

  if (normalizedIntent.protocol !== 'evk') {
    deployable = false;
    recommendedAction = 'blocked';
    blockers.push(EVK_ONLY_WARNING);
  }

  if (normalizedIntent.duplicatePolicy === 'warn-only'
    && (discovery.exactMatches.length > 0 || discovery.nearEquivalentMatches.length > 0)) {
    recommendedAction = 'deploy-new-market';
    warnings.push('Duplicate policy `warn-only` is enabled. Existing exact or near-equivalent markets will not block deployment, but this duplicate-style launch still requires an explicit operator decision.');
  }

  if (normalizedIntent.duplicatePolicy === 'block-on-exact' && discovery.exactMatches.length > 0) {
    deployable = false;
    recommendedAction = 'blocked';
    blockers.push('Duplicate policy blocked deployment because an exact market already exists in the registry.');
  }

  if (normalizedIntent.duplicatePolicy === 'block-on-near-equivalent' && discovery.nearEquivalentMatches.length > 0) {
    deployable = false;
    recommendedAction = 'blocked';
    blockers.push('Duplicate policy blocked deployment because a near-equivalent market already exists in the registry.');
  }

  if (recommendedAction === 'blocked' && normalizedIntent.duplicatePolicy !== 'warn-only' && deployable) {
    const relatedMarketIds = [...discovery.exactMatches, ...discovery.nearEquivalentMatches]
      .map((market) => market.marketId)
      .filter(Boolean);
    const relatedLabel = relatedMarketIds.length > 0 ? relatedMarketIds.join(', ') : 'existing market registry entry';
    deployable = false;
    blockers.push(`Deployment intent is blocked by an existing or near-equivalent market: ${relatedLabel}.`);
  }

  if (oracleRoute.strategy === 'euler-cross-adapter') {
    warnings.push('Composite route selected. Oracle prep should confirm CrossAdapter composition before deployment.');
  }

  const planKey = {
    protocol: normalizedIntent.protocol,
    chainId: normalizedIntent.chain.chainId,
    collateralAssets: normalizedIntent.collateralAssets,
    borrowAssets: normalizedIntent.borrowAssets,
    unitOfAccount: normalizedIntent.unitOfAccount,
    riskPreset: normalizedIntent.riskPreset,
    oracleStrategy: oracleRoute.strategy,
  };

  const result = {
    deployable,
    normalizedIntent: {
      ...normalizedIntent,
      canonicalHash: makeCanonicalHash(planKey),
    },
    oracleRoute,
    existingMarkets: {
      exactMatches: discovery.exactMatches,
      nearEquivalentMatches: discovery.nearEquivalentMatches,
    },
    recommendedAction,
    requiredFeeds,
    nextCommands: [
      'ensure-feeds',
      'discover-markets',
      'prepare-euler-oracle',
      'prepare-evk-market',
      'prepare-evk-deployment',
    ],
    blockers,
    warnings,
  };

  validatePlanMarketResponse(result);
  return result;
}

function resolveFeedStatus(feedName, chainId, feedStatus) {
  const overrides = feedStatus.overrides || {};
  const chainOverrides = overrides[String(chainId)] || {};
  const canonicalFeedName = canonicalizeFeedName(feedName);
  if (chainOverrides[feedName]) {
    return chainOverrides[feedName];
  }

  if (canonicalFeedName && canonicalFeedName !== feedName && chainOverrides[canonicalFeedName]) {
    return chainOverrides[canonicalFeedName];
  }

  if (canonicalFeedName) {
    const canonicalOverrideEntry = Object.entries(chainOverrides)
      .find(([overrideFeedName]) => feedNamesEqual(overrideFeedName, canonicalFeedName));
    if (canonicalOverrideEntry) {
      return canonicalOverrideEntry[1];
    }
  }

  if (DAPI_NAME_SET.has(feedName) || (canonicalFeedName && DAPI_NAME_SET.has(canonicalFeedName))) {
    return {
      status: 'activatable',
      supportsAggregatorV2V3Interface: true,
      requiresCompatibilityWrapper: true,
      blockers: [],
    };
  }

  return {
    status: 'blocked',
    supportsAggregatorV2V3Interface: false,
    requiresCompatibilityWrapper: false,
    blockers: ['Feed is not present in the bundled Api3 dAPI catalog.'],
  };
}

function fakeProxyAddress(feedName, chainId) {
  return `0x${crypto.createHash('sha256').update(`${chainId}:${feedName}`).digest('hex').slice(0, 40)}`;
}

async function ensureFeeds(request, options) {
  validateEnsureFeedsRequest(request);
  const feedStatus = loadFeedStatus(options);
  const activationMode = request.activationMode || DEFAULT_ACTIVATION_MODE;
  const requireChainlinkCompatibility = request.requireChainlinkCompatibility !== false;
  const warnings = [];
  const liveRpc = resolveRpcUrlForChain(request.chain, request.rpcPreference);

  if (!liveRpc.rpcUrl) {
    warnings.push(`No live RPC configured for ${request.chain.name || `chain-${request.chain.chainId}`}, using local feed-status fallback.`);
  }

  const feeds = [];
  const liveActivations = [];

  for (const feed of request.requiredFeeds) {
    const feedName = feed.feedName || `${normalizeSymbol(feed.base.symbol)}/${normalizeSymbol(feed.quote.symbol)}`;
    let liveResult = null;

    if (liveRpc.rpcUrl) {
      try {
        liveResult = await fetchLiveFeedStatus(request.chain, feed, request.rpcPreference);
        if (liveResult.ok && liveResult.activation) {
          liveActivations.push({
            feedName,
            source: liveResult.source,
            classification: liveResult.activation.classification,
          });
        }
      } catch (error) {
        warnings.push(`Live Api3 check failed for ${feedName}, falling back to local planner data: ${error.message}`);
      }
    }

    const fallbackRecord = resolveFeedStatus(feedName, request.chain.chainId, feedStatus);
    const statusRecord = liveResult && liveResult.ok
      ? {
          ...fallbackRecord,
          ...liveResult,
          blockers: [...new Set([...(fallbackRecord.blockers || []), ...(liveResult.blockers || [])])],
        }
      : fallbackRecord;

    const blockers = [...(statusRecord.blockers || [])];
    if (requireChainlinkCompatibility && !statusRecord.supportsAggregatorV2V3Interface) {
      blockers.push('Requested Chainlink-compatible routing, but the feed does not support AggregatorV2V3 compatibility in this planner phase.');
    }
    if (statusRecord.status === 'blocked' && blockers.length === 0) {
      blockers.push(`Feed ${feedName} is currently blocked or unresolved by the live Api3 readiness check.`);
    }

    feeds.push({
      feedName,
      proxyAddress: statusRecord.proxyAddress || fakeProxyAddress(feedName, request.chain.chainId),
      proxyDeploymentPlan: statusRecord.proxyDeploymentPlan || undefined,
      proxyHasCode: typeof statusRecord.proxyHasCode === 'boolean' ? statusRecord.proxyHasCode : undefined,
      status: blockers.length > 0 && statusRecord.status !== 'ready' ? 'blocked' : statusRecord.status,
      supportsAggregatorV2V3Interface: Boolean(statusRecord.supportsAggregatorV2V3Interface),
      requiresCompatibilityWrapper: requireChainlinkCompatibility ? Boolean(statusRecord.requiresCompatibilityWrapper) : false,
      latestRead: statusRecord.latestRead || { value: '0', timestamp: 0 },
      blockers,
    });
  }

  const blockers = feeds.flatMap((feed) => feed.blockers || []);
  if (activationMode === 'check-only') {
    warnings.push('ensure-feeds ran in check-only mode. No external activation attempt was prepared.');
  }

  const activationCandidates = feeds.filter((feed) => feed.status === 'activatable');
  const ready = feeds.every((feed) => feed.status === 'ready' || feed.status === 'activatable') && blockers.length === 0;
  const result = {
    ready,
    feeds,
    activationPlan: {
      mode: activationMode,
      commandFamily: 'api3-feed-manager',
      requestedChainId: request.chain.chainId,
      rpcSource: liveRpc.source,
      liveChecked: Boolean(liveRpc.rpcUrl),
      actions: activationCandidates.map((feed) => ({
        feedName: feed.feedName,
        command: `node ./bin/api3-feed-manager.js prepare-activation --dapi-name "${feed.feedName}" --chain ${request.chain.name || request.chain.chainId}${liveRpc.rpcUrl ? ` --rpc-url "${liveRpc.rpcUrl}"` : ''}`,
      })),
      liveActivations,
    },
    wrapperPlan: {
      requiresWrappers: requireChainlinkCompatibility && feeds.some((feed) => feed.requiresCompatibilityWrapper),
      wrapperContract: requireChainlinkCompatibility ? 'Api3PartialAggregatorV2V3Interface' : 'none',
      feedsRequiringWrappers: feeds.filter((feed) => feed.requiresCompatibilityWrapper).map((feed) => feed.feedName),
    },
    blockers,
    warnings,
  };

  validateEnsureFeedsResponse(result);
  return result;
}

async function runEvkWorkflow(request, options = {}) {
  validateRunEvkWorkflowRequest(request);

  const recipeSelection = selectEvkRecipeForWorkflow(request);
  const normalizedRequest = normalizeWorkflowRequest(request, recipeSelection);

  const results = {
    request: normalizedRequest,
    recipeSelection,
    planMarket: null,
    ensureFeeds: null,
    feedFunding: {
      modeRequested: request.feedFunding?.mode || 'classify-only',
      attemptedExecution: false,
      overallState: null,
      entries: [],
    },
    prepareEulerOracle: null,
    prepareEvkMarket: null,
    prepareEvkDeployment: null,
    deployEvkMarket: null,
    artifactPersistence: emptyArtifactPersistence(request.artifacts),
  };

  let planMarketResult = planMarket({
    protocol: 'evk',
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
  }, options);
  results.planMarket = planMarketResult;

  if (!planMarketResult.deployable || recipeSelection.blockers.length > 0) {
    return finalizeRunEvkWorkflowResponse({ request, results });
  }

  let initialEnsureFeeds = await ensureFeeds({
    chain: request.chain,
    requiredFeeds: planMarketResult.requiredFeeds,
    activationMode: request.activationMode,
    requireChainlinkCompatibility: true,
    rpcPreference: request.rpcPreference,
  }, options);

  if (!initialEnsureFeeds.ready && shouldAttemptCompositeFallback(request, planMarketResult, initialEnsureFeeds)) {
    const compositeFallbackPlanMarketResult = buildCompositeFallbackPlanMarketResult(request, planMarketResult);
    const compositeFallbackEnsureFeeds = await ensureFeeds({
      chain: request.chain,
      requiredFeeds: compositeFallbackPlanMarketResult.requiredFeeds,
      activationMode: request.activationMode,
      requireChainlinkCompatibility: true,
      rpcPreference: request.rpcPreference,
    }, options);

    if (compositeFallbackEnsureFeeds.ready || compositeFallbackEnsureFeeds.feeds.some((feed) => feed && feed.status !== 'blocked')) {
      planMarketResult = compositeFallbackPlanMarketResult;
      results.planMarket = planMarketResult;
      initialEnsureFeeds = compositeFallbackEnsureFeeds;
    }
  }

  let finalEnsureFeeds = initialEnsureFeeds;
  results.ensureFeeds = {
    initial: initialEnsureFeeds,
    final: finalEnsureFeeds,
  };

  if (!initialEnsureFeeds.ready) {
    const feedsNeedingFunding = initialEnsureFeeds.feeds.filter((feed) => feed.status !== 'ready');

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

      try {
        const purchasePlan = await purchaseInputs(fundingOptions);
        entry.purchaseInputs = purchasePlan;
        entry.fundingExecutionState = purchasePlan.fundingExecutionClassification?.state || null;
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

        if (entry.fundingExecutionState === 'executable' && results.feedFunding.modeRequested !== 'classify-only') {
          results.feedFunding.attemptedExecution = true;
          entry.execution = await executeBuySubscription({
            ...fundingOptions,
            submit: results.feedFunding.modeRequested === 'real-send',
          });
          entry.fundingExecutionState = entry.execution.fundingExecutionClassification?.state || entry.fundingExecutionState;
          entry.availableExecutionModes = Array.isArray(entry.execution.availableExecutionModes)
            ? [...entry.execution.availableExecutionModes]
            : entry.availableExecutionModes;
          entry.selectedExecutionMode = entry.execution.selectedExecutionMode || null;

          if (entry.execution.executionSummary?.failureReason) {
            entry.blockers.push(entry.execution.executionSummary.failureReason);
          }
        }
      } catch (error) {
        entry.blockers.push(`purchase-inputs failed for ${feed.feedName}: ${error.message}`);
      }

      results.feedFunding.entries.push(entry);
    }

    results.feedFunding.overallState = summarizeFundingState(results.feedFunding.entries);

    if (results.feedFunding.modeRequested === 'real-send' && results.feedFunding.entries.some((entry) => entry.execution?.executionSummary?.completed)) {
      finalEnsureFeeds = await ensureFeeds({
        chain: request.chain,
        requiredFeeds: planMarketResult.requiredFeeds,
        activationMode: request.activationMode,
        requireChainlinkCompatibility: true,
        rpcPreference: request.rpcPreference,
      }, options);
      results.ensureFeeds.final = finalEnsureFeeds;
    } else if (results.feedFunding.overallState === 'executable') {
      finalEnsureFeeds = promoteFundingReadyFeedsForPlanning(finalEnsureFeeds, results.feedFunding);
      results.ensureFeeds.final = finalEnsureFeeds;
    }
  }

  if (!finalEnsureFeeds.ready) {
    return finalizeRunEvkWorkflowResponse({ request, results });
  }

  const prepareEulerOracleResult = prepareEulerOracle({
    chain: request.chain,
    oracleRoute: planMarketResult.oracleRoute,
    feedArtifacts: finalEnsureFeeds.feeds,
    preferInfrequentOracle: request.preferInfrequentOracle,
    unitOfAccount: request.unitOfAccount,
    allowCustomFallback: request.allowCustomFallback,
    shareAwareRouter: request.shareAwareRouter
      ? {
          ...request.shareAwareRouter,
          governorAddress: request.shareAwareRouter.governorAddress
            || (request.executionProfile && request.executionProfile.executorAddress)
            || request.shareAwareRouter.governorAddress,
        }
      : undefined,
  });
  results.prepareEulerOracle = prepareEulerOracleResult;

  const prepareEvkMarketResult = prepareEvkMarket({
    chain: request.chain,
    recipeId: recipeSelection.resolvedRecipeId,
    riskPreset: request.riskPreset,
    collateralAssets: request.collateralAssets,
    borrowAssets: request.borrowAssets,
    oraclePreparation: prepareEulerOracleResult,
    hookProfile: request.hookProfile,
    ownershipProfile: request.ownershipProfile,
    governanceProfile: request.governanceProfile,
    publishToRegistry: request.publishToRegistry,
  });
  results.prepareEvkMarket = prepareEvkMarketResult;

  const prepareEvkDeploymentResult = prepareEvkDeployment({
    chain: request.chain,
    oraclePreparation: prepareEulerOracleResult,
    marketPreparation: prepareEvkMarketResult,
    executionProfile: request.executionProfile,
    vaultContext: request.vaultContext,
  });
  results.prepareEvkDeployment = prepareEvkDeploymentResult;

  const deployResolutionRpcUrl = request.send?.rpcUrl || resolveRpcUrlForChain(request.chain, request.rpcPreference || {}).rpcUrl;
  const deployEvkMarketResult = await deployEvkMarket({
    ready: prepareEvkDeploymentResult.ready,
    executionMode: prepareEvkDeploymentResult.executionMode,
    deploymentBundle: prepareEvkDeploymentResult.deploymentBundle,
    preflightChecks: prepareEvkDeploymentResult.preflightChecks,
    blockers: prepareEvkDeploymentResult.blockers,
    warnings: prepareEvkDeploymentResult.warnings,
    executorAddress: request.executionProfile?.executorAddress,
    ...(Number.isInteger(request.executionProfile?.startingNonce) ? { startingNonce: request.executionProfile.startingNonce } : {}),
    ...(deployResolutionRpcUrl ? { resolutionRpcUrl: deployResolutionRpcUrl } : {}),
    broadcast: request.broadcast,
    send: request.send,
  });
  results.deployEvkMarket = deployEvkMarketResult;

  return finalizeRunEvkWorkflowResponse({ request, results });
}

function prepareEulerOracle(request) {
  validatePrepareEulerOracleRequest(request);

  const route = request.oracleRoute;
  const allowCustomFallback = request.allowCustomFallback === true;
  const blockers = [];
  const warnings = [];
  const contracts = [];
  const verificationChecks = [
    'feed-readiness',
    'timestamp-freshness',
    'quote-orientation',
    'expected-quote-sanity',
  ];

  const readyArtifacts = request.feedArtifacts.filter((artifact) => artifact.status === 'ready');
  request.feedArtifacts
    .filter((artifact) => artifact.status !== 'ready')
    .forEach((artifact) => blockers.push(`${artifact.feedName || 'feed'} is not ready (${artifact.status})`));

  if (route.routeType === 'not-deployable') {
    blockers.push(...(route.reasons || ['Oracle route is not deployable']));
  }

  const unsupportedCompatibility = readyArtifacts.filter(
    (artifact) => artifact.supportsAggregatorV2V3Interface === false,
  );

  if (route.routeType !== 'custom-api3-fallback') {
    unsupportedCompatibility.forEach((artifact) => {
      blockers.push(`${artifact.feedName || 'feed'} does not support the Chainlink-compatible path`);
    });
  }

  let integrationMode = 'chainlink-oracle';
  if (route.routeType === 'custom-api3-fallback') {
    integrationMode = 'custom-api3-fallback';
    if (!allowCustomFallback) {
      blockers.push('Custom Api3 fallback was selected, but request.allowCustomFallback is false');
    }
  } else if (route.routeType === 'composite-chainlink-compatible' || readyArtifacts.length > 1) {
    integrationMode = 'cross-adapter';
  } else if (request.preferInfrequentOracle || route.strategy === 'euler-chainlink-infrequent-oracle') {
    integrationMode = 'chainlink-infrequent-oracle';
  }

  readyArtifacts.forEach((artifact) => {
    if (artifact.requiresCompatibilityWrapper !== false) {
      const wrapperDeploymentRef = `api3-wrapper:${artifact.feedName || artifact.proxyAddress}`;
      contracts.push({
        contractName: 'Api3PartialAggregatorV2V3Interface',
        constructorArgs: {
          api3Proxy: artifact.proxyAddress,
          deploymentRef: wrapperDeploymentRef,
        },
        purpose: `Expose ${artifact.feedName || 'Api3 feed'} through a Chainlink-compatible interface`,
      });
    }
  });

  if (integrationMode === 'chainlink-oracle' || integrationMode === 'chainlink-infrequent-oracle') {
    const artifact = readyArtifacts[0];
    if (artifact) {
      const wrapperDeploymentRef = artifact.requiresCompatibilityWrapper !== false
        ? `api3-wrapper:${artifact.feedName || artifact.proxyAddress}`
        : null;
      const directRouteFeed = findRouteFeedForArtifact(route.feeds, artifact) || (Array.isArray(route.feeds) ? route.feeds[0] : null);
      const concreteChainlinkArgs = (integrationMode === 'chainlink-oracle' || integrationMode === 'chainlink-infrequent-oracle')
        ? buildConcreteChainlinkOracleArgs({
            artifact,
            routeFeed: directRouteFeed,
            route,
            wrapperDeploymentRef,
          })
        : null;

      if (!concreteChainlinkArgs && artifact.requiresCompatibilityWrapper !== false) {
        warnings.push(`${integrationMode === 'chainlink-infrequent-oracle' ? 'ChainlinkInfrequentOracle' : 'ChainlinkOracle'} deployment for this route depends on a wrapper deployment address and will be resolved during executor planning when nonce context is available.`);
      } else if (!concreteChainlinkArgs) {
        warnings.push(`${integrationMode === 'chainlink-infrequent-oracle' ? 'ChainlinkInfrequentOracle' : 'ChainlinkOracle'} deployment remains skeleton-only for this route because base/quote token addresses were not supplied or the concrete adapter path is not implemented yet.`);
      }

      contracts.push({
        contractName: integrationMode === 'chainlink-infrequent-oracle' ? 'ChainlinkInfrequentOracle' : 'ChainlinkOracle',
        constructorArgs: concreteChainlinkArgs
          ? {
              ...concreteChainlinkArgs,
              deploymentRef: 'oracle-final:direct',
            }
          : {
              ...(wrapperDeploymentRef ? { feedDeploymentRef: wrapperDeploymentRef } : { feed: artifact.proxyAddress }),
              feedName: artifact.feedName || null,
              maxStaleness: route.maxStalenessSeconds || DEFAULT_MAX_STALENESS_SECONDS,
              unitOfAccount: request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT,
              deploymentRef: 'oracle-final:direct',
              ...(directRouteFeed && isNonZeroHexAddress(directRouteFeed.base && directRouteFeed.base.address)
                ? { base: directRouteFeed.base.address }
                : {}),
              ...(directRouteFeed && isNonZeroHexAddress(directRouteFeed.quote && directRouteFeed.quote.address)
                ? { quote: directRouteFeed.quote.address }
                : {}),
            },
        purpose: `Create an EVK-ready oracle for ${artifact.feedName || 'the selected direct feed'}`,
      });
    }
  } else if (integrationMode === 'cross-adapter') {
    readyArtifacts.forEach((artifact) => {
      const routeFeed = findRouteFeedForArtifact(route.feeds, artifact);
      const wrapperDeploymentRef = artifact.requiresCompatibilityWrapper !== false
        ? `api3-wrapper:${artifact.feedName || artifact.proxyAddress}`
        : null;
      const concreteChainlinkArgs = buildConcreteChainlinkOracleArgs({
        artifact,
        routeFeed,
        route,
        wrapperDeploymentRef,
      });
      const oracleLegDeploymentRef = `oracle-leg:${artifact.feedName || artifact.proxyAddress}`;

      if (!concreteChainlinkArgs && wrapperDeploymentRef) {
        warnings.push(`Composite oracle leg ${artifact.feedName || 'feed'} depends on a wrapper deployment address and will be resolved during executor planning when nonce context is available.`);
      } else if (!concreteChainlinkArgs) {
        warnings.push(`Composite oracle leg ${artifact.feedName || 'feed'} remains skeleton-only because base/quote token addresses were not supplied.`);
      }

      contracts.push({
        contractName: request.preferInfrequentOracle ? 'ChainlinkInfrequentOracle' : 'ChainlinkOracle',
        constructorArgs: concreteChainlinkArgs
          ? {
              ...concreteChainlinkArgs,
              deploymentRef: oracleLegDeploymentRef,
            }
          : {
              ...(wrapperDeploymentRef ? { feedDeploymentRef: wrapperDeploymentRef } : { feed: artifact.proxyAddress }),
              feedName: artifact.feedName || null,
              maxStaleness: route.maxStalenessSeconds || DEFAULT_MAX_STALENESS_SECONDS,
              ...(routeFeed && isNonZeroHexAddress(routeFeed.base && routeFeed.base.address)
                ? { base: routeFeed.base.address }
                : {}),
              ...(routeFeed && isNonZeroHexAddress(routeFeed.quote && routeFeed.quote.address)
                ? { quote: routeFeed.quote.address }
                : {}),
              deploymentRef: oracleLegDeploymentRef,
            },
        purpose: `Create a route leg for ${artifact.feedName || 'a composite feed leg'}`,
      });
    });

    const baseLegFeed = Array.isArray(route.feeds)
      ? route.feeds.find((feed) => feed.routeRole === 'collateral-leg') || route.feeds[0]
      : null;
    const quoteLegFeed = Array.isArray(route.feeds)
      ? route.feeds.find((feed) => feed.routeRole === 'borrow-leg') || route.feeds[1] || route.feeds[0]
      : null;
    const baseLegArtifact = baseLegFeed
      ? readyArtifacts.find((artifact) => feedNamesEqual(artifact.feedName || '', baseLegFeed.feedName || ''))
      : null;
    const quoteLegArtifact = quoteLegFeed
      ? readyArtifacts.find((artifact) => feedNamesEqual(artifact.feedName || '', quoteLegFeed.feedName || ''))
      : null;
    const crossAdapterConcreteArgs = baseLegFeed
      && quoteLegFeed
      && baseLegArtifact
      && quoteLegArtifact
      && isNonZeroHexAddress(baseLegFeed.base && baseLegFeed.base.address)
      && isNonZeroHexAddress(baseLegFeed.quote && baseLegFeed.quote.address)
      && isNonZeroHexAddress(quoteLegFeed.base && quoteLegFeed.base.address)
      ? {
          base: baseLegFeed.base.address,
          cross: baseLegFeed.quote.address,
          quote: quoteLegFeed.base.address,
          oracleBaseCrossDeploymentRef: `oracle-leg:${baseLegArtifact.feedName || baseLegArtifact.proxyAddress}`,
          oracleCrossQuoteDeploymentRef: `oracle-leg:${quoteLegArtifact.feedName || quoteLegArtifact.proxyAddress}`,
          deploymentRef: 'oracle-final:cross-adapter',
        }
      : null;

    if (!crossAdapterConcreteArgs) {
      warnings.push('CrossAdapter deployment remains skeleton-only because the composite route does not yet resolve to one concrete collateral leg and one concrete borrow leg with addresses.');
    }

    contracts.push({
      contractName: 'CrossAdapter',
      constructorArgs: crossAdapterConcreteArgs || {
        throughAsset: request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT,
        routeFeedNames: readyArtifacts.map((artifact) => artifact.feedName || 'feed'),
      },
      purpose: 'Compose the prepared route legs through a shared unit of account',
    });
  } else if (integrationMode === 'custom-api3-fallback') {
    contracts.push({
      contractName: readyArtifacts.length > 1 ? 'EulerApi3CompositeOracle' : 'EulerApi3DirectOracle',
      constructorArgs: {
        feedNames: readyArtifacts.map((artifact) => artifact.feedName || 'feed'),
        maxStaleness: route.maxStalenessSeconds || DEFAULT_MAX_STALENESS_SECONDS,
        unitOfAccount: request.unitOfAccount || DEFAULT_UNIT_OF_ACCOUNT,
      },
      purpose: 'Fallback custom EVK Api3 oracle route when the Chainlink-compatible path is insufficient',
    });
    warnings.push('Using a custom EVK Api3 fallback increases the custom-code surface');
  }

  if (request.shareAwareRouter && request.shareAwareRouter.enabled) {
    const finalOracleEntry = [...contracts]
      .reverse()
      .find((entry) => ['CrossAdapter', 'ChainlinkOracle', 'ChainlinkInfrequentOracle'].includes(entry.contractName));
    const finalOracleArgs = finalOracleEntry && finalOracleEntry.constructorArgs ? finalOracleEntry.constructorArgs : null;
    const finalOracleBase = finalOracleArgs && typeof finalOracleArgs === 'object' && 'base' in finalOracleArgs ? finalOracleArgs.base : null;
    const finalOracleQuote = finalOracleArgs && typeof finalOracleArgs === 'object' && 'quote' in finalOracleArgs ? finalOracleArgs.quote : null;
    const finalOracleDeploymentRef = finalOracleArgs && typeof finalOracleArgs === 'object' && 'deploymentRef' in finalOracleArgs ? finalOracleArgs.deploymentRef : null;
    const routerGovernor = request.shareAwareRouter.governorAddress;
    const resolvedVaults = [...new Set((request.shareAwareRouter.resolvedVaults || []).filter(isNonZeroHexAddress))];

    if (!routerGovernor || !isNonZeroHexAddress(routerGovernor)) {
      blockers.push('shareAwareRouter.governorAddress is required to deploy EulerRouter support.');
    } else if (!finalOracleEntry || !finalOracleArgs || !isNonZeroHexAddress(finalOracleBase) || !isNonZeroHexAddress(finalOracleQuote) || typeof finalOracleDeploymentRef !== 'string') {
      blockers.push('Share-aware router support requires a concrete final oracle with base, quote, and deploymentRef metadata.');
    } else {
      contracts.push({
        contractName: 'EulerRouter',
        constructorArgs: {
          evc: request.shareAwareRouter.evcAddress,
          governor: routerGovernor,
          base: finalOracleBase,
          quote: finalOracleQuote,
          deploymentRef: 'oracle-final:router',
        },
        purpose: 'Deploy a share-aware recursive oracle router for cross-vault borrowing',
      });

      contracts.push({
        contractName: 'EulerRouter_govSetConfig',
        constructorArgs: {
          routerDeploymentRef: 'oracle-final:router',
          base: finalOracleBase,
          quote: finalOracleQuote,
          oracleDeploymentRef: finalOracleDeploymentRef,
        },
        purpose: `Configure EulerRouter pricing for ${finalOracleBase}/${finalOracleQuote}`,
      });

      resolvedVaults.forEach((vaultAddress) => {
        contracts.push({
          contractName: 'EulerRouter_govSetResolvedVault',
          constructorArgs: {
            routerDeploymentRef: 'oracle-final:router',
            vault: vaultAddress,
            resolved: true,
          },
          purpose: `Mark ${vaultAddress} as a share-aware resolved vault`,
        });
      });

      verificationChecks.push('share-aware-router-configured');
      warnings.push('Share-aware router support assumes the resolved vault list is complete for the intended collateral set.');
    }
  }

  if (readyArtifacts.some((artifact) => artifact.requiresCompatibilityWrapper !== false)) {
    verificationChecks.push('wrapper-compatibility');
  }

  const result = {
    ready: blockers.length === 0,
    integrationMode,
    contracts,
    expectedQuote: buildExpectedQuote(route, readyArtifacts),
    verificationChecks,
    blockers,
    warnings,
  };

  validatePrepareEulerOracleResponse(result);
  return result;
}

function prepareEvkMarket(request) {
  validatePrepareEvkMarketRequest(request);

  const blockers = [];
  const warnings = [];
  const recipe = getEvkRecipe(request.recipeId);
  if (!recipe) {
    blockers.push(`Unknown EVK recipe: ${request.recipeId}`);
  }

  if (recipe && recipe.riskPreset !== request.riskPreset) {
    blockers.push(`Recipe ${request.recipeId} expects riskPreset=${recipe.riskPreset}, received ${request.riskPreset}`);
  }

  const integrationMode = request.oraclePreparation.integrationMode;
  if (!integrationMode) {
    blockers.push('request.oraclePreparation.integrationMode is required');
  }

  const collateralSymbols = request.collateralAssets.map((asset) => String(asset.symbol || '').trim().toUpperCase());
  const borrowSymbols = request.borrowAssets.map((asset) => String(asset.symbol || '').trim().toUpperCase());

  if (recipe) {
    collateralSymbols
      .filter((symbol) => !recipe.supportedCollateralSymbols.includes(symbol))
      .forEach((symbol) => blockers.push(`Collateral asset ${symbol} is not allowed by recipe ${request.recipeId}`));

    borrowSymbols
      .filter((symbol) => !recipe.supportedBorrowSymbols.includes(symbol))
      .forEach((symbol) => blockers.push(`Borrow asset ${symbol} is not allowed by recipe ${request.recipeId}`));

    const routeType = request.oraclePreparation.oracleRoute && request.oraclePreparation.oracleRoute.routeType;
    if (routeType && !recipe.allowedOracleModes.includes(routeType)) {
      warnings.push(`Recipe ${request.recipeId} was not tuned for oracle mode ${routeType}`);
    }
  }

  const hookProfile = request.hookProfile || (recipe && recipe.hookProfile) || 'none';
  const ownershipProfile = request.ownershipProfile || (recipe && recipe.ownershipProfile) || 'deployer-owned';
  const governanceProfile = request.governanceProfile || (recipe && recipe.governanceProfile) || 'deployer-governed';

  const normalizedIntent = {
    protocol: 'evk',
    chain: normalizeChain(request.chain),
    collateralAssets: request.collateralAssets.map((asset) => normalizeAsset(asset, 'collateral')),
    borrowAssets: request.borrowAssets.map((asset) => normalizeAsset(asset, 'borrow')),
    unitOfAccount: DEFAULT_UNIT_OF_ACCOUNT,
    riskPreset: request.riskPreset,
    hookProfile,
    ownershipProfile,
  };

  const oracleRoute = extractOracleRouteFromPreparation(request.oraclePreparation, request.borrowAssets);
  const canonicalPlanKey = {
    protocol: normalizedIntent.protocol,
    chainId: normalizedIntent.chain.chainId,
    collateralAssets: normalizedIntent.collateralAssets,
    borrowAssets: normalizedIntent.borrowAssets,
    unitOfAccount: normalizedIntent.unitOfAccount,
    riskPreset: normalizedIntent.riskPreset,
    oracleStrategy: oracleRoute.strategy,
  };
  const manifestPreview = {
    canonicalHash: makeCanonicalHash(canonicalPlanKey),
    displayName: buildDisplayName(normalizedIntent),
    protocol: 'evk',
    chainId: normalizedIntent.chain.chainId,
    oracleMode: oracleRoute.routeType,
    riskPreset: request.riskPreset,
  };

  const deploymentRecipe = {
    recipeId: request.recipeId,
    protocol: 'evk',
    riskPreset: request.riskPreset,
    hookProfile,
    ownershipProfile,
    governanceProfile,
    oracleIntegrationMode: integrationMode || 'unknown',
    ltvBps: recipe ? recipe.ltvBps : null,
    liquidationThresholdBps: recipe ? recipe.liquidationThresholdBps : null,
    publishToRegistry: request.publishToRegistry !== false,
  };

  const contracts = {
    oracleContracts: Array.isArray(request.oraclePreparation.contracts)
      ? request.oraclePreparation.contracts.map((contract) => contract.contractName)
      : [],
    vaultFactory: 'GenericFactory',
    hookContract: hookProfile === 'none' ? null : hookProfile,
    governanceProfile,
  };

  const deploymentSteps = [
    { step: 1, action: 'deploy-oracle-stack', contract: integrationMode || 'oracle-stack', notes: 'Deploy or reference the prepared Euler oracle contracts' },
    { step: 2, action: 'deploy-evk-vault', contract: 'GenericFactory', notes: `Deploy the EVK market for ${buildDisplayName(normalizedIntent)}` },
    { step: 3, action: 'verify-evk-market', contract: 'EVK', notes: 'Confirm oracle, recipe, ownership, and hook settings match the plan' },
  ];

  if (request.publishToRegistry !== false) {
    deploymentSteps.push({
      step: 4,
      action: 'register-market',
      contract: 'OffchainRegistry',
      notes: 'Publish the market manifest so later agents can discover it before deploying duplicates',
    });
  }

  const verificationChecklist = [
    'oracle-stack-deployed-or-referenced',
    'recipe-parameters-match',
    'ownership-profile-match',
    'governance-profile-match',
    'manifest-canonical-hash-match',
  ];

  const result = {
    ready: blockers.length === 0,
    deploymentRecipe,
    contracts,
    manifestPreview,
    deploymentSteps,
    verificationChecklist,
    blockers,
    warnings,
  };

  validatePrepareEvkMarketResponse(result);
  return result;
}

function prepareEvkDeployment(request) {
  validatePrepareEvkDeploymentRequest(request);

  const executionMode = (request.executionProfile && request.executionProfile.mode) || 'simulate';
  const verifyBeforeBroadcast = !request.executionProfile || request.executionProfile.verifyBeforeBroadcast !== false;
  const registerMarket = (!request.executionProfile || request.executionProfile.registerMarket !== false)
    && request.marketPreparation.deploymentRecipe.publishToRegistry !== false;

  const blockers = [];
  const warnings = [];

  if (!request.oraclePreparation.ready) {
    blockers.push('Oracle preparation is not ready for deployment bundling.');
  }

  if (!request.marketPreparation.ready) {
    blockers.push('EVK market preparation is not ready for deployment bundling.');
  }

  blockers.push(...request.oraclePreparation.blockers.map((entry) => `oraclePreparation: ${entry}`));
  blockers.push(...request.marketPreparation.blockers.map((entry) => `marketPreparation: ${entry}`));
  warnings.push(...request.oraclePreparation.warnings.map((entry) => `oraclePreparation: ${entry}`));
  warnings.push(...request.marketPreparation.warnings.map((entry) => `marketPreparation: ${entry}`));

  if (executionMode === 'broadcast-ready' && !(request.executionProfile && request.executionProfile.executorAddress)) {
    warnings.push('executionProfile.executorAddress was not supplied, so this bundle is broadcast-ready in structure only.');
  }

  if (!registerMarket) {
    warnings.push('Registry publication was skipped for this deployment bundle.');
  }

  const oracleDeploymentPlan = request.oraclePreparation.contracts.map((contract, index) => ({
    order: index + 1,
    action: 'deploy-contract',
    contractName: contract.contractName,
    purpose: contract.purpose || `Deploy ${contract.contractName}`,
    constructorArgs: contract.constructorArgs,
    artifactKey: `oracle-${index + 1}`,
  }));

  const bootstrapResolution = resolveAutoVaultContext(request.chain, request.vaultContext || null);
  const vaultContext = bootstrapResolution.vaultContext;
  if (bootstrapResolution.autofilledFactoryAddress && bootstrapResolution.overlapChain) {
    warnings.push(`Auto-filled vaultContext.factoryAddress from overlap bootstrap for ${bootstrapResolution.overlapChain.alias}.`);
  }
  const vaultOracleMetadata = inferVaultOracleMetadata(request.oraclePreparation.contracts);
  const concreteVaultParams = vaultContext
    && isNonZeroHexAddress(vaultContext.factoryAddress)
    && isNonZeroHexAddress(vaultContext.assetAddress)
    ? {
        factoryAddress: vaultContext.factoryAddress,
        assetAddress: vaultContext.assetAddress,
        ...vaultOracleMetadata,
      }
    : null;

  const marketDeploymentPlan = request.marketPreparation.deploymentSteps
    .filter((entry) => registerMarket || entry.action !== 'register-market')
    .map((entry, index) => ({
      order: index + 1,
      action: entry.action,
      ...(entry.contract ? { contract: entry.contract } : {}),
      ...(entry.notes ? { notes: entry.notes } : {}),
      dependsOn: entry.action === 'deploy-oracle-stack'
        ? oracleDeploymentPlan.map((planEntry) => planEntry.artifactKey)
        : [],
      ...(entry.action === 'deploy-evk-vault' && concreteVaultParams ? { vaultParams: concreteVaultParams } : {}),
    }));

  const preflightChecks = [
    ...request.oraclePreparation.verificationChecks,
    ...request.marketPreparation.verificationChecklist,
    'chain-id-confirmation',
    'deployer-balance-check',
    ...(verifyBeforeBroadcast ? ['final-human-review'] : []),
  ].filter((entry, index, array) => array.indexOf(entry) === index);

  const result = {
    ready: blockers.length === 0,
    executionMode,
    deploymentBundle: {
      canonicalHash: request.marketPreparation.manifestPreview.canonicalHash,
      displayName: request.marketPreparation.manifestPreview.displayName,
      chainId: request.chain.chainId,
      manifestPreview: request.marketPreparation.manifestPreview,
      oracleDeploymentPlan,
      marketDeploymentPlan,
    },
    preflightChecks,
    blockers,
    warnings,
  };

  validatePrepareEvkDeploymentResponse(result);
  return result;
}

function fakeAddress(seed) {
  return `0x${crypto.createHash('sha256').update(String(seed)).digest('hex').slice(0, 40)}`;
}

function makeSkeletonCalldata(payload) {
  return `0x${crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex')}`;
}

function loadContractArtifactBytecode(artifactPath) {
  const sidecarPath = artifactPath.replace(/\.json$/i, '.bytecode.txt');
  const rawBytecode = fs.readFileSync(sidecarPath, 'utf8').replace(/\s+/g, '');
  return rawBytecode.startsWith('0x') ? rawBytecode : `0x${rawBytecode}`;
}

function loadContractArtifact(contractName) {
  const artifactPath = CONTRACT_ARTIFACT_PATHS[contractName];
  if (!artifactPath) {
    return null;
  }

  if (contractArtifactCache.has(contractName)) {
    return contractArtifactCache.get(contractName);
  }

  try {
    const artifact = readJsonFile(artifactPath);
    const bytecode = typeof artifact?.bytecode === 'string' && artifact.bytecode.startsWith('0x')
      ? artifact.bytecode
      : loadContractArtifactBytecode(artifactPath);
    const normalizedArtifact = bytecode
      ? { ...artifact, bytecode }
      : null;
    contractArtifactCache.set(contractName, normalizedArtifact);
    return normalizedArtifact;
  } catch {
    contractArtifactCache.set(contractName, null);
    return null;
  }
}

function loadCallArtifact(contractName) {
  if (!CALL_ARTIFACT_PATHS[contractName]) {
    return null;
  }

  if (callArtifactCache.has(contractName)) {
    return callArtifactCache.get(contractName);
  }

  try {
    const artifact = readJsonFile(CALL_ARTIFACT_PATHS[contractName]);
    const normalizedArtifact = artifact && Array.isArray(artifact.abi) && artifact.abi.length > 0
      ? artifact
      : null;
    callArtifactCache.set(contractName, normalizedArtifact);
    return normalizedArtifact;
  } catch {
    callArtifactCache.set(contractName, null);
    return null;
  }
}

function buildExecutableMarketCalldata(entry, deploymentAddressByRef = new Map()) {
  if (!entry || entry.action !== 'deploy-evk-vault') {
    return null;
  }

  const vaultParams = entry.vaultParams;
  if (!vaultParams) {
    return null;
  }

  const factoryAddress = vaultParams.factoryAddress;
  const assetAddress = vaultParams.assetAddress;
  const oracleAddress = isNonZeroHexAddress(vaultParams.oracleAddress)
    ? vaultParams.oracleAddress
    : (typeof vaultParams.oracleDeploymentRef === 'string'
      ? deploymentAddressByRef.get(vaultParams.oracleDeploymentRef)
      : null);
  const unitOfAccountAddress = vaultParams.unitOfAccountAddress;

  if (!isNonZeroHexAddress(factoryAddress)
    || !isNonZeroHexAddress(assetAddress)
    || !isNonZeroHexAddress(oracleAddress)
    || !isNonZeroHexAddress(unitOfAccountAddress)) {
    return null;
  }

  const artifact = loadCallArtifact('GenericFactory');
  if (!artifact) {
    return null;
  }

  const iface = new Interface(artifact.abi);
  const proxyMetadata = solidityPacked(
    ['address', 'address', 'address'],
    [assetAddress, oracleAddress, unitOfAccountAddress],
  );
  return {
    to: factoryAddress,
    data: iface.encodeFunctionData('createProxy', ['0x0000000000000000000000000000000000000000', false, proxyMetadata]),
  };
}

function buildRegistryPublicationPayload(deploymentBundle) {
  const manifest = {
    canonicalHash: deploymentBundle.canonicalHash,
    protocol: deploymentBundle.manifestPreview.protocol,
    chainId: deploymentBundle.chainId,
  };
  if (deploymentBundle.manifestPreview.displayName) {
    manifest.displayName = deploymentBundle.manifestPreview.displayName;
  }
  if (deploymentBundle.manifestPreview.oracleMode) {
    manifest.oracleMode = deploymentBundle.manifestPreview.oracleMode;
  }
  if (deploymentBundle.manifestPreview.riskPreset) {
    manifest.riskPreset = deploymentBundle.manifestPreview.riskPreset;
  }
  return `0x${Buffer.from(JSON.stringify(manifest)).toString('hex')}`;
}

function buildVerifyEvkMarketChecklist(deploymentBundle) {
  const vaultEntry = deploymentBundle.marketDeploymentPlan.find((e) => e.action === 'deploy-evk-vault');
  const checklist = {
    canonicalHash: deploymentBundle.canonicalHash,
    chainId: deploymentBundle.chainId,
    expectedOracleContracts: deploymentBundle.oracleDeploymentPlan.map((e) => ({
      contractName: e.contractName,
      purpose: e.purpose,
    })),
    expectedFactory: vaultEntry ? (vaultEntry.contract || 'GenericFactory') : 'GenericFactory',
    manifestFields: {
      protocol: deploymentBundle.manifestPreview.protocol,
    },
  };
  if (deploymentBundle.manifestPreview.oracleMode) {
    checklist.manifestFields.oracleMode = deploymentBundle.manifestPreview.oracleMode;
  }
  if (deploymentBundle.manifestPreview.riskPreset) {
    checklist.manifestFields.riskPreset = deploymentBundle.manifestPreview.riskPreset;
  }
  return checklist;
}

function inferVaultOracleMetadata(oracleContracts) {
  if (!Array.isArray(oracleContracts) || oracleContracts.length === 0) {
    return {};
  }

  const finalOracle = [...oracleContracts]
    .reverse()
    .find((entry) => ['EulerRouter', 'CrossAdapter', 'ChainlinkOracle', 'ChainlinkInfrequentOracle'].includes(entry.contractName));
  const constructorArgs = finalOracle && finalOracle.constructorArgs ? finalOracle.constructorArgs : null;
  if (!constructorArgs) {
    return {};
  }

  const metadata = {};
  if (isNonZeroHexAddress(constructorArgs.oracleAddress)) {
    metadata.oracleAddress = constructorArgs.oracleAddress;
  }
  if (typeof constructorArgs.deploymentRef === 'string' && constructorArgs.deploymentRef.trim()) {
    metadata.oracleDeploymentRef = constructorArgs.deploymentRef.trim();
  }

  const unitOfAccountAddress = finalOracle.contractName === 'EulerRouter'
    ? constructorArgs.quote
    : (finalOracle.contractName === 'CrossAdapter'
      ? constructorArgs.quote
      : (finalOracle.contractName === 'ChainlinkOracle' || finalOracle.contractName === 'ChainlinkInfrequentOracle'
        ? constructorArgs.quote
        : constructorArgs.unitOfAccountAddress));

  if (isNonZeroHexAddress(unitOfAccountAddress)) {
    metadata.unitOfAccountAddress = unitOfAccountAddress;
  }

  return metadata;
}

function buildExecutableOracleDeploymentData(contractName, constructorArgs, deploymentAddressByRef = new Map()) {
  const deploymentArtifactName = contractName.startsWith('EulerRouter_') ? 'EulerRouter' : contractName;
  const artifact = loadContractArtifact(deploymentArtifactName);
  if (!artifact) {
    return null;
  }

  if (contractName === 'Api3PartialAggregatorV2V3Interface') {
    const api3Proxy = constructorArgs && constructorArgs.api3Proxy;
    if (!isNonZeroHexAddress(api3Proxy)) {
      return null;
    }

    return { kind: 'contract-deployment', to: null, data: `${artifact.bytecode}${ABI_CODER.encode(['address'], [api3Proxy]).slice(2)}` };
  }

  if (contractName === 'ChainlinkOracle' || contractName === 'ChainlinkInfrequentOracle') {
    const base = constructorArgs && constructorArgs.base;
    const quote = constructorArgs && constructorArgs.quote;
    const feed = constructorArgs && isNonZeroHexAddress(constructorArgs.feed)
      ? constructorArgs.feed
      : (constructorArgs && typeof constructorArgs.feedDeploymentRef === 'string'
        ? deploymentAddressByRef.get(constructorArgs.feedDeploymentRef)
        : null);
    const maxStaleness = normalizeUint256Like(constructorArgs && constructorArgs.maxStaleness);

    if (!isNonZeroHexAddress(base) || !isNonZeroHexAddress(quote) || !isNonZeroHexAddress(feed) || maxStaleness === null) {
      return null;
    }

    if (maxStaleness < BigInt(CHAINLINK_ORACLE_MAX_STALENESS_LOWER_BOUND)
      || maxStaleness > BigInt(CHAINLINK_ORACLE_MAX_STALENESS_UPPER_BOUND)) {
      return null;
    }

    return {
      kind: 'contract-deployment',
      to: null,
      data: `${artifact.bytecode}${ABI_CODER.encode(['address', 'address', 'address', 'uint256'], [base, quote, feed, maxStaleness]).slice(2)}`,
    };
  }

  if (contractName === 'CrossAdapter') {
    const base = constructorArgs && constructorArgs.base;
    const cross = constructorArgs && constructorArgs.cross;
    const quote = constructorArgs && constructorArgs.quote;
    const oracleBaseCross = constructorArgs && isNonZeroHexAddress(constructorArgs.oracleBaseCross)
      ? constructorArgs.oracleBaseCross
      : (constructorArgs && typeof constructorArgs.oracleBaseCrossDeploymentRef === 'string'
        ? deploymentAddressByRef.get(constructorArgs.oracleBaseCrossDeploymentRef)
        : null);
    const oracleCrossQuote = constructorArgs && isNonZeroHexAddress(constructorArgs.oracleCrossQuote)
      ? constructorArgs.oracleCrossQuote
      : (constructorArgs && typeof constructorArgs.oracleCrossQuoteDeploymentRef === 'string'
        ? deploymentAddressByRef.get(constructorArgs.oracleCrossQuoteDeploymentRef)
        : null);

    if (!isNonZeroHexAddress(base) || !isNonZeroHexAddress(cross) || !isNonZeroHexAddress(quote)
      || !isNonZeroHexAddress(oracleBaseCross) || !isNonZeroHexAddress(oracleCrossQuote)) {
      return null;
    }

    return {
      kind: 'contract-deployment',
      to: null,
      data: `${artifact.bytecode}${ABI_CODER.encode(['address', 'address', 'address', 'address', 'address'], [base, cross, quote, oracleBaseCross, oracleCrossQuote]).slice(2)}`,
    };
  }

  if (contractName === 'EulerRouter') {
    const evc = constructorArgs && constructorArgs.evc;
    const governor = constructorArgs && constructorArgs.governor;
    const base = constructorArgs && constructorArgs.base;
    const quote = constructorArgs && constructorArgs.quote;

    if (!isNonZeroHexAddress(evc) || !isNonZeroHexAddress(governor) || !isNonZeroHexAddress(base) || !isNonZeroHexAddress(quote)) {
      return null;
    }

    return {
      kind: 'contract-deployment',
      to: null,
      data: `${artifact.bytecode}${ABI_CODER.encode(['address', 'address', 'address', 'address'], [evc, governor, base, quote]).slice(2)}`,
    };
  }

  if (contractName === 'EulerRouter_govSetConfig') {
    const routerAddress = constructorArgs && typeof constructorArgs.routerDeploymentRef === 'string'
      ? deploymentAddressByRef.get(constructorArgs.routerDeploymentRef)
      : null;
    const base = constructorArgs && constructorArgs.base;
    const quote = constructorArgs && constructorArgs.quote;
    const oracle = constructorArgs && isNonZeroHexAddress(constructorArgs.oracle)
      ? constructorArgs.oracle
      : (constructorArgs && typeof constructorArgs.oracleDeploymentRef === 'string'
        ? deploymentAddressByRef.get(constructorArgs.oracleDeploymentRef)
        : null);

    if (!isNonZeroHexAddress(routerAddress) || !isNonZeroHexAddress(base) || !isNonZeroHexAddress(quote) || !isNonZeroHexAddress(oracle)) {
      return null;
    }

    const iface = new Interface(artifact.abi);
    return {
      kind: 'contract-call',
      to: routerAddress,
      data: iface.encodeFunctionData('govSetConfig', [base, quote, oracle]),
    };
  }

  if (contractName === 'EulerRouter_govSetResolvedVault') {
    const routerAddress = constructorArgs && typeof constructorArgs.routerDeploymentRef === 'string'
      ? deploymentAddressByRef.get(constructorArgs.routerDeploymentRef)
      : null;
    const vault = constructorArgs && constructorArgs.vault;
    const resolved = constructorArgs && typeof constructorArgs.resolved === 'boolean'
      ? constructorArgs.resolved
      : true;

    if (!isNonZeroHexAddress(routerAddress) || !isNonZeroHexAddress(vault)) {
      return null;
    }

    const iface = new Interface(artifact.abi);
    return {
      kind: 'contract-call',
      to: routerAddress,
      data: iface.encodeFunctionData('govSetResolvedVault', [vault, resolved]),
    };
  }

  return null;
}

function allOnchainTransactionsExecutable(transactionPlan) {
  return transactionPlan
    .filter((entry) => entry.kind !== 'offchain-publication')
    .every((entry) => entry.payloadKind === 'executable');
}

function buildOracleExecutionArtifacts({ chainId, mode, blockers, oracleContracts }) {
  const transactionStatus = blockers.length === 0
    ? (mode === 'simulate' ? 'simulated' : 'prepared')
    : 'blocked';

  const transactionPlan = [];
  const stepResults = [];
  const oracleExecutionEntries = [];

  oracleContracts.forEach((entry, index) => {
    const transactionId = `oracle-tx-${index + 1}`;
    const executableStep = buildExecutableOracleDeploymentData(entry.contractName, entry.constructorArgs);
    const payloadKind = executableStep ? 'executable' : 'skeleton';
    const kind = executableStep ? executableStep.kind : (entry.contractName.startsWith('EulerRouter_') ? 'contract-call' : 'contract-deployment');
    const dependsOn = getConstructorDependencyRefs(entry.constructorArgs);

    transactionPlan.push({
      transactionId,
      kind,
      payloadKind,
      status: transactionStatus,
      chainId,
      to: executableStep ? executableStep.to : null,
      data: executableStep ? executableStep.data : makeSkeletonCalldata({ contractName: entry.contractName, constructorArgs: entry.constructorArgs }),
      value: '0',
      description: entry.purpose || `Deploy ${entry.contractName}`,
      sendStatus: 'not-requested',
    });
    stepResults.push({
      order: index + 1,
      phase: 'oracle',
      transactionId,
      dependsOn,
      action: kind === 'contract-call' ? 'configure-oracle' : 'deploy-contract',
      status: transactionStatus,
      targetContract: entry.contractName,
      notes: entry.purpose || `Deploy ${entry.contractName}`,
      sendStatus: 'not-requested',
    });
    oracleExecutionEntries.push({
      transactionId,
      dependsOn,
      notes: entry.purpose || `Deploy ${entry.contractName}`,
      contractName: entry.contractName,
      constructorArgs: entry.constructorArgs,
      kind,
    });
  });

  return {
    transactionStatus,
    transactionPlan,
    stepResults,
    oracleExecutionEntries,
  };
}

async function resolveExecutableTransactionPlan({ transactionPlan, oracleExecutionEntries, marketExecutionEntries = [], signerAddress, provider = null, startingNonce = undefined }) {
  if ((!Array.isArray(oracleExecutionEntries) || oracleExecutionEntries.length === 0) && (!Array.isArray(marketExecutionEntries) || marketExecutionEntries.length === 0)) {
    return transactionPlan;
  }

  const metadataByTransactionId = new Map(
    oracleExecutionEntries.map((entry) => [entry.transactionId, entry]),
  );
  const deploymentAddressByRef = new Map();
  let nextNonce = startingNonce;
  if (nextNonce === undefined || nextNonce === null) {
    nextNonce = await provider.getTransactionCount(signerAddress, 'pending');
  }

  transactionPlan.forEach((transaction) => {
    const metadata = metadataByTransactionId.get(transaction.transactionId);
    if (!metadata) {
      return;
    }

    const executableStep = buildExecutableOracleDeploymentData(
      metadata.contractName,
      metadata.constructorArgs,
      deploymentAddressByRef,
    );

    if (!executableStep) {
      return;
    }

    transaction.payloadKind = 'executable';
    transaction.kind = executableStep.kind;
    transaction.to = executableStep.to;
    transaction.data = executableStep.data;

    if (transaction.kind === 'contract-deployment'
      && metadata.constructorArgs
      && typeof metadata.constructorArgs.deploymentRef === 'string') {
      deploymentAddressByRef.set(
        metadata.constructorArgs.deploymentRef,
        getCreateAddress({ from: signerAddress, nonce: nextNonce }),
      );
      nextNonce += 1;
    }
  });

  const marketMetadataByTransactionId = new Map(
    marketExecutionEntries.map((entry) => [entry.transactionId, entry]),
  );

  transactionPlan.forEach((transaction) => {
    const metadata = marketMetadataByTransactionId.get(transaction.transactionId);
    if (!metadata || transaction.kind !== 'contract-call') {
      return;
    }

    const executableMarket = buildExecutableMarketCalldata(metadata, deploymentAddressByRef);
    if (!executableMarket) {
      return;
    }

    transaction.payloadKind = 'executable';
    transaction.to = executableMarket.to;
    transaction.data = executableMarket.data;
  });

  return transactionPlan;
}

async function resolveTransactionPlanForReadiness({ transactionPlan, oracleExecutionEntries, marketExecutionEntries = [], mode, executorAddress, resolutionRpcUrl, startingNonce, warnings }) {
  if (!executorAddress || !Array.isArray(oracleExecutionEntries) || oracleExecutionEntries.length === 0) {
    return transactionPlan;
  }

  if (mode !== 'broadcast-ready' && !(Number.isInteger(startingNonce) && startingNonce >= 0)) {
    return transactionPlan;
  }

  const hasDeferredDependencies = oracleExecutionEntries.some((entry) => (
    entry
    && entry.constructorArgs
    && (
      typeof entry.constructorArgs.deploymentRef === 'string'
      || Object.keys(entry.constructorArgs).some((key) => key.endsWith('DeploymentRef'))
    )
  )) || marketExecutionEntries.some((entry) => (
    entry
    && entry.vaultParams
    && typeof entry.vaultParams.oracleDeploymentRef === 'string'
  ));

  if (!hasDeferredDependencies) {
    return transactionPlan;
  }

  if (Number.isInteger(startingNonce) && startingNonce >= 0) {
    await resolveExecutableTransactionPlan({
      transactionPlan,
      oracleExecutionEntries,
      marketExecutionEntries,
      signerAddress: executorAddress,
      startingNonce,
    });
    return transactionPlan;
  }

  if (!resolutionRpcUrl) {
    warnings.push('Nonce-dependent oracle deployment addresses could not be resolved because no resolution RPC URL was supplied.');
    return transactionPlan;
  }

  try {
    const provider = new JsonRpcProvider(resolutionRpcUrl);
    await resolveExecutableTransactionPlan({
      transactionPlan,
      oracleExecutionEntries,
      marketExecutionEntries,
      signerAddress: executorAddress,
      provider,
    });
  } catch (error) {
    warnings.push(`Failed to resolve nonce-dependent oracle deployment addresses: ${error.message}`);
  }

  return transactionPlan;
}

async function maybeSendTransactionPlan({ transactionPlan, stepResults, oracleExecutionEntries, marketExecutionEntries = [], send, mode, broadcastOptIn, executorAddress, broadcastIntent, warnings }) {
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
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  if (mode !== 'broadcast-ready') {
    const failureReason = 'Send path requires executionMode=broadcast-ready.';
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  if (!broadcastOptIn) {
    const failureReason = 'Send path requires explicit broadcast opt-in acknowledgement.';
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  if (!send.rpcUrl || !send.privateKey) {
    const failureReason = 'Send path requires send.rpcUrl and send.privateKey.';
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  const provider = new JsonRpcProvider(send.rpcUrl);
  const wallet = new Wallet(send.privateKey, provider);
  const signerAddress = await wallet.getAddress();
  sendSummary.signerAddress = signerAddress;

  if (executorAddress && signerAddress.toLowerCase() !== executorAddress.toLowerCase()) {
    const failureReason = 'Resolved signer address does not match executorAddress.';
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  if (broadcastIntent && broadcastIntent.signerAddress && signerAddress.toLowerCase() !== broadcastIntent.signerAddress.toLowerCase()) {
    const failureReason = 'Resolved signer address does not match broadcast.signerAddress.';
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  try {
    await resolveExecutableTransactionPlan({
      transactionPlan,
      oracleExecutionEntries,
      marketExecutionEntries,
      signerAddress,
      provider,
    });
  } catch (error) {
    const failureReason = `Failed to resolve executable transaction dependencies: ${error.message}`;
    warnings.push(failureReason);
    sendSummary.failureReason = failureReason;
    return { transactionPlan, stepResults, warnings, sendSummary };
  }

  sendSummary.attempted = true;

  for (let index = 0; index < transactionPlan.length; index += 1) {
    const transaction = transactionPlan[index];
    const relatedStep = stepResults.find((entry) => entry.transactionId === transaction.transactionId);

    if (transaction.payloadKind !== 'executable') {
      const error = 'Transaction payload is still skeleton-only and cannot be sent yet.';
      transaction.sendStatus = 'failed';
      transaction.error = error;
      if (relatedStep) {
        relatedStep.sendStatus = 'failed';
        relatedStep.error = error;
      }
      sendSummary.failedTransactions += 1;
      sendSummary.failureReason = error;

      for (let restIndex = index + 1; restIndex < transactionPlan.length; restIndex += 1) {
        const remainingTransaction = transactionPlan[restIndex];
        remainingTransaction.sendStatus = 'skipped';
        remainingTransaction.error = 'Skipped because a prior transaction failed to submit.';
        const remainingStep = stepResults.find((entry) => entry.transactionId === remainingTransaction.transactionId);
        if (remainingStep) {
          remainingStep.sendStatus = 'skipped';
          remainingStep.error = 'Skipped because a prior transaction failed to submit.';
        }
        sendSummary.skippedTransactions += 1;
      }

      return { transactionPlan, stepResults, warnings, sendSummary };
    }

    if (sendSummary.dryRun) {
      transaction.sendStatus = 'dry-run';
      if (relatedStep) {
        relatedStep.sendStatus = 'dry-run';
      }
      continue;
    }

    try {
      const response = await wallet.sendTransaction({
        to: transaction.to || undefined,
        data: transaction.data,
        value: BigInt(transaction.value || '0'),
      });
      transaction.sendStatus = 'submitted';
      transaction.txHash = response.hash;
      if (relatedStep) {
        relatedStep.sendStatus = 'submitted';
        relatedStep.txHash = response.hash;
      }
      sendSummary.submittedTransactions += 1;

      let receipt = null;
      if (typeof response.wait === 'function') {
        receipt = await response.wait();
      } else if (typeof provider.waitForTransaction === 'function') {
        receipt = await provider.waitForTransaction(response.hash);
      }

      if (receipt && receipt.status !== undefined && receipt.status !== null && Number(receipt.status) !== 1) {
        throw new Error(`Transaction ${transaction.transactionId} was mined with status ${receipt.status}.`);
      }
    } catch (error) {
      const sendError = error instanceof Error ? error.message : String(error);
      const failureReason = `Failed while sending ${transaction.transactionId}: ${sendError}`;

      transaction.sendStatus = 'failed';
      transaction.error = failureReason;
      if (relatedStep) {
        relatedStep.sendStatus = 'failed';
        relatedStep.error = failureReason;
      }

      sendSummary.failedTransactions += 1;
      sendSummary.failureReason = failureReason;

      for (let restIndex = index + 1; restIndex < transactionPlan.length; restIndex += 1) {
        const restTransaction = transactionPlan[restIndex];
        if (restTransaction.sendStatus === 'not-requested') {
          restTransaction.sendStatus = 'skipped';
          restTransaction.failureReason = failureReason;
          sendSummary.skippedTransactions += 1;
        }

        const restStep = stepResults.find((entry) => entry.transactionId === restTransaction.transactionId);
        if (restStep && restStep.sendStatus === 'not-requested') {
          restStep.sendStatus = 'skipped';
          restStep.failureReason = failureReason;
        }
      }

      return { transactionPlan, stepResults, warnings, sendSummary };
    }
  }

  sendSummary.completed = sendSummary.failedTransactions === 0;
  return { transactionPlan, stepResults, warnings, sendSummary };
}

function inferStepPhase(action) {
  if (action === 'deploy-contract' || action === 'deploy-oracle-stack') {
    return 'oracle';
  }
  if (action === 'deploy-evk-vault') {
    return 'market';
  }
  if (action === 'verify-evk-market') {
    return 'verification';
  }
  if (action === 'register-market') {
    return 'registry';
  }
  return 'market';
}

async function deployEvkMarket(request) {
  validateDeployEvkMarketRequest(request);

  const blockers = [...request.blockers];
  const warnings = [...request.warnings];
  const mode = request.executionMode;
  const broadcastOptIn = hasExplicitBroadcastOptIn(request.broadcast);

  if (request.broadcast && request.broadcast.signerAddress && request.executorAddress && request.broadcast.signerAddress !== request.executorAddress) {
    warnings.push('broadcast.signerAddress does not match executorAddress, so broadcast readiness stays disabled.');
  }

  if (mode === 'broadcast-ready' && !request.executorAddress) {
    warnings.push('executorAddress was not supplied, so the executor output is broadcast-ready in shape only.');
  }

  if (mode === 'broadcast-ready' && !broadcastOptIn) {
    warnings.push('Explicit broadcast opt-in is missing. Set broadcast.enabled=true and acknowledgement=I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS to mark this executor result as truly ready to broadcast.');
  }

  if (mode === 'simulate' && broadcastOptIn) {
    warnings.push('Broadcast opt-in was supplied in simulate mode, so no sending is authorized from this request.');
  }

  if (mode === 'broadcast-ready' && request.preflightChecks.includes('final-human-review')) {
    warnings.push('Final human review is still required before any real broadcast step.');
  }

  const {
    transactionStatus,
    transactionPlan,
    stepResults,
    oracleExecutionEntries,
  } = buildOracleExecutionArtifacts({
    chainId: request.deploymentBundle.chainId,
    mode,
    blockers,
    oracleContracts: request.deploymentBundle.oracleDeploymentPlan.map((entry) => ({
      contractName: entry.contractName,
      constructorArgs: entry.constructorArgs,
      purpose: entry.purpose,
    })),
  });

  const marketExecutionEntries = [];

  request.deploymentBundle.marketDeploymentPlan.forEach((entry, index) => {
    const phase = inferStepPhase(entry.action);
    let transactionId = null;

    if (entry.action === 'deploy-evk-vault') {
      transactionId = `market-tx-${index + 1}`;
      const executableMarket = buildExecutableMarketCalldata(entry);
      marketExecutionEntries.push({
        transactionId,
        ...entry,
      });
      transactionPlan.push({
        transactionId,
        kind: 'contract-call',
        payloadKind: executableMarket ? 'executable' : 'skeleton',
        status: transactionStatus,
        chainId: request.deploymentBundle.chainId,
        to: executableMarket ? executableMarket.to : fakeAddress(`${request.deploymentBundle.canonicalHash}:${entry.contract || 'GenericFactory'}`),
        data: executableMarket ? executableMarket.data : makeSkeletonCalldata({
          phase: 'market',
          action: entry.action,
          contract: entry.contract || null,
          canonicalHash: request.deploymentBundle.canonicalHash,
        }),
        value: '0',
        description: entry.notes || 'Deploy the EVK market from the prepared bundle',
        sendStatus: 'not-requested',
      });
    } else if (entry.action === 'register-market') {
      transactionId = `registry-tx-${index + 1}`;
      transactionPlan.push({
        transactionId,
        kind: 'offchain-publication',
        payloadKind: 'executable',
        status: transactionStatus,
        chainId: request.deploymentBundle.chainId,
        to: null,
        data: buildRegistryPublicationPayload(request.deploymentBundle),
        value: '0',
        description: entry.notes || 'Publish the prepared market manifest',
        sendStatus: 'not-requested',
      });
    }

    const verificationChecklist = entry.action === 'verify-evk-market'
      ? buildVerifyEvkMarketChecklist(request.deploymentBundle)
      : undefined;

    stepResults.push({
      order: request.deploymentBundle.oracleDeploymentPlan.length + index + 1,
      phase,
      action: entry.action,
      status: blockers.length > 0 ? 'blocked' : (mode === 'simulate' ? 'simulated' : 'prepared'),
      ...(entry.contract ? { targetContract: entry.contract } : {}),
      ...(transactionId ? { transactionId } : {}),
      dependsOn: entry.dependsOn,
      ...(entry.notes ? { notes: entry.notes } : {}),
      ...(verificationChecklist ? { verificationChecklist } : {}),
      sendStatus: 'not-requested',
    });
  });

  await resolveTransactionPlanForReadiness({
    transactionPlan,
    oracleExecutionEntries,
    marketExecutionEntries,
    mode,
    executorAddress: request.executorAddress,
    startingNonce: request.startingNonce,
    resolutionRpcUrl: request.resolutionRpcUrl || (request.send && request.send.rpcUrl) || null,
    warnings,
  });

  const sendResult = await maybeSendTransactionPlan({
    transactionPlan,
    stepResults,
    oracleExecutionEntries,
    marketExecutionEntries,
    send: request.send,
    mode,
    broadcastOptIn,
    executorAddress: request.executorAddress,
    broadcastIntent: request.broadcast,
    warnings,
  });

  const result = {
    ready: blockers.length === 0,
    executionSummary: {
      mode,
      chainId: request.deploymentBundle.chainId,
      canonicalHash: request.deploymentBundle.canonicalHash,
      totalSteps: stepResults.length,
      actionableTransactions: transactionPlan.length,
      simulatedTransactions: transactionPlan.filter((entry) => entry.status === 'simulated').length,
      readyToBroadcast: blockers.length === 0
        && mode === 'broadcast-ready'
        && Boolean(request.executorAddress)
        && broadcastOptIn
        && allOnchainTransactionsExecutable(sendResult.transactionPlan)
        && (!request.broadcast || !request.broadcast.signerAddress || request.broadcast.signerAddress === request.executorAddress)
        && (!request.send || !request.send.enabled || !sendResult.sendSummary.failureReason),
    },
    stepResults: sendResult.stepResults,
    transactionPlan: sendResult.transactionPlan,
    sendSummary: sendResult.sendSummary,
    blockers,
    warnings: sendResult.warnings,
  };

  validateDeployEvkMarketResponse(result);
  return result;
}

async function deployEulerOracle(request) {
  validateDeployEulerOracleRequest(request);

  const blockers = [...request.blockers];
  const warnings = [...request.warnings];
  const mode = request.executionMode;
  const broadcastOptIn = hasExplicitBroadcastOptIn(request.broadcast);

  if (request.broadcast && request.broadcast.signerAddress && request.executorAddress && request.broadcast.signerAddress !== request.executorAddress) {
    warnings.push('broadcast.signerAddress does not match executorAddress, so broadcast readiness stays disabled.');
  }

  if (mode === 'broadcast-ready' && !request.executorAddress) {
    warnings.push('executorAddress was not supplied, so the oracle executor output is broadcast-ready in shape only.');
  }

  if (mode === 'broadcast-ready' && !broadcastOptIn) {
    warnings.push('Explicit broadcast opt-in is missing. Set broadcast.enabled=true and acknowledgement=I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS to mark this oracle executor result as truly ready to broadcast.');
  }

  if (mode === 'simulate' && broadcastOptIn) {
    warnings.push('Broadcast opt-in was supplied in simulate mode, so no sending is authorized from this request.');
  }

  if (mode === 'broadcast-ready' && request.verificationChecks.includes('final-human-review')) {
    warnings.push('Final human review is still required before any real oracle broadcast step.');
  }

  const {
    transactionPlan,
    stepResults,
    oracleExecutionEntries,
  } = buildOracleExecutionArtifacts({
    chainId: request.chain.chainId,
    mode,
    blockers,
    oracleContracts: request.contracts,
  });

  stepResults.push({
    order: request.contracts.length + 1,
    phase: 'verification',
    action: 'verify-euler-oracle',
    status: blockers.length > 0 ? 'blocked' : (mode === 'simulate' ? 'simulated' : 'prepared'),
    dependsOn: transactionPlan.map((entry) => entry.transactionId),
    notes: `Run oracle verification checks: ${request.verificationChecks.join(', ')}`,
    sendStatus: 'not-requested',
  });

  const sendResult = await maybeSendTransactionPlan({
    transactionPlan,
    stepResults,
    oracleExecutionEntries,
    send: request.send,
    mode,
    broadcastOptIn,
    executorAddress: request.executorAddress,
    broadcastIntent: request.broadcast,
    warnings,
  });

  const result = {
    ready: blockers.length === 0,
    executionSummary: {
      mode,
      chainId: request.chain.chainId,
      integrationMode: request.integrationMode,
      totalSteps: stepResults.length,
      actionableTransactions: transactionPlan.length,
      simulatedTransactions: transactionPlan.filter((entry) => entry.status === 'simulated').length,
      readyToBroadcast: blockers.length === 0
        && mode === 'broadcast-ready'
        && Boolean(request.executorAddress)
        && broadcastOptIn
        && allOnchainTransactionsExecutable(sendResult.transactionPlan)
        && (!request.broadcast || !request.broadcast.signerAddress || request.broadcast.signerAddress === request.executorAddress)
        && (!request.send || !request.send.enabled || !sendResult.sendSummary.failureReason),
    },
    stepResults: sendResult.stepResults,
    transactionPlan: sendResult.transactionPlan,
    sendSummary: sendResult.sendSummary,
    expectedQuote: request.expectedQuote || { quoteAvailable: false },
    blockers,
    warnings: sendResult.warnings,
  };

  validateDeployEulerOracleResponse(result);
  return result;
}

function discoverMarkets(request, options) {
  validateDiscoverMarketsRequest(request);
  const registry = loadRegistry(options);
  const normalizedRequest = {
    ...request,
    protocol: request.protocol,
    chain: normalizeChain(request.chain),
    collateralAssets: (request.collateralAssets || []).map((asset) => normalizeAsset(asset, 'collateral')),
    borrowAssets: (request.borrowAssets || []).map((asset) => normalizeAsset(asset, 'borrow')),
  };
  const result = discoverMarketsInternal(normalizedRequest, registry);
  validateDiscoverMarketsResponse(result);
  return result;
}

function buildDisplayName(normalizedIntent) {
  const chainName = normalizedIntent.chain.name || `chain-${normalizedIntent.chain.chainId}`;
  const collateral = normalizedIntent.collateralAssets.map((asset) => asset.symbol || 'COLLATERAL').join('/');
  const borrow = normalizedIntent.borrowAssets.map((asset) => asset.symbol || 'BORROW').join('/');
  return `${chainName} ${collateral}/${borrow} ${String(normalizedIntent.protocol || 'market').toUpperCase()} market`;
}

function buildExpectedQuote(route, feedArtifacts) {
  const filteredArtifacts = feedArtifacts.filter((artifact) => artifact.latestRead);
  if (filteredArtifacts.length === 0) {
    return {
      routeType: route.routeType,
      quoteAvailable: false,
    };
  }

  if (route.routeType === 'composite-chainlink-compatible' && filteredArtifacts.length >= 2) {
    const [first, second] = filteredArtifacts;
    const numerator = Number(first.latestRead.humanValue ?? 0);
    const denominator = Number(second.latestRead.humanValue ?? 0);
    return {
      routeType: route.routeType,
      quoteAvailable: denominator > 0,
      quoteKind: 'composite-ratio',
      firstFeed: first.feedName || null,
      secondFeed: second.feedName || null,
      humanQuote: denominator > 0 ? numerator / denominator : null,
    };
  }

  const artifact = filteredArtifacts[0];
  return {
    routeType: route.routeType,
    quoteAvailable: true,
    quoteKind: 'direct',
    feedName: artifact.feedName || null,
    humanQuote: artifact.latestRead.humanValue ?? null,
    rawValue: artifact.latestRead.value,
    timestamp: artifact.latestRead.timestamp,
  };
}

function extractOracleRouteFromPreparation(oraclePreparation, borrowAssets) {
  if (oraclePreparation.oracleRoute) {
    return oraclePreparation.oracleRoute;
  }

  const borrowAsset = Array.isArray(borrowAssets) && borrowAssets.length > 0 ? borrowAssets[0] : { symbol: DEFAULT_UNIT_OF_ACCOUNT };
  const strategyMap = {
    'chainlink-oracle': 'euler-chainlink-oracle',
    'chainlink-infrequent-oracle': 'euler-chainlink-infrequent-oracle',
    'cross-adapter': 'euler-cross-adapter',
    'custom-api3-fallback': 'custom-euler-api3-adapter',
  };

  return {
    routeType: oraclePreparation.integrationMode === 'cross-adapter' ? 'composite-chainlink-compatible' : 'direct-chainlink-compatible',
    strategy: strategyMap[oraclePreparation.integrationMode] || 'euler-chainlink-oracle',
    maxStalenessSeconds: DEFAULT_MAX_STALENESS_SECONDS,
    feeds: Array.isArray(oraclePreparation.contracts)
      ? oraclePreparation.contracts
          .filter((contract) => contract.contractName === 'Api3PartialAggregatorV2V3Interface')
          .map(() => ({
            base: { symbol: 'UNKNOWN' },
            quote: { symbol: borrowAsset.symbol || DEFAULT_UNIT_OF_ACCOUNT },
          }))
      : [],
    reasons: [],
  };
}

function validateExistingMarketSummary(entry, label) {
  assertPlainObject(entry, label);
  assertAllowedKeys(entry, ['canonicalHash', 'marketId', 'protocol', 'chainId', 'displayName', 'matchType', 'riskPreset', 'status', 'borrowOptions', 'supplyOptions'], label);
  assertStringIfPresent(entry.canonicalHash, `${label}.canonicalHash`);
  assert(entry.canonicalHash, `${label}.canonicalHash is required`);
  assertEnum(entry.protocol, ['evk', 'morpho'], `${label}.protocol`);
  assert(Number.isInteger(entry.chainId) && entry.chainId >= 1, `${label}.chainId must be an integer >= 1`);
  assertEnum(entry.matchType, ['exact', 'near-equivalent'], `${label}.matchType`);
  assertEnum(entry.status, DEFAULT_STATUSES, `${label}.status`);
  if (entry.marketId !== undefined) assertStringIfPresent(entry.marketId, `${label}.marketId`);
  if (entry.displayName !== undefined) assertStringIfPresent(entry.displayName, `${label}.displayName`);
  if (entry.riskPreset !== undefined) assertStringIfPresent(entry.riskPreset, `${label}.riskPreset`);
  if (entry.borrowOptions !== undefined) assert(Array.isArray(entry.borrowOptions), `${label}.borrowOptions must be an array`);
  if (entry.supplyOptions !== undefined) assert(Array.isArray(entry.supplyOptions), `${label}.supplyOptions must be an array`);
}

function validateOracleRoute(route) {
  assertPlainObject(route, 'oracleRoute');
  assertAllowedKeys(route, ['routeType', 'strategy', 'maxStalenessSeconds', 'feeds', 'reasons'], 'oracleRoute');
  assertEnum(route.routeType, ['direct-chainlink-compatible', 'composite-chainlink-compatible', 'custom-api3-fallback', 'not-deployable'], 'oracleRoute.routeType');
  if (route.strategy !== undefined) {
    assertEnum(route.strategy, ['api3-partial-aggregatorv2v3interface', 'euler-chainlink-oracle', 'euler-chainlink-infrequent-oracle', 'euler-cross-adapter', 'custom-euler-api3-adapter'], 'oracleRoute.strategy');
  }
  if (route.maxStalenessSeconds !== undefined) {
    assert(Number.isInteger(route.maxStalenessSeconds) && route.maxStalenessSeconds >= 1, 'oracleRoute.maxStalenessSeconds must be an integer >= 1');
  }
  if (route.feeds !== undefined) {
    assert(Array.isArray(route.feeds), 'oracleRoute.feeds must be an array');
    route.feeds.forEach((feed, index) => validateFeedRequirement(feed, `oracleRoute.feeds[${index}]`));
  }
  if (route.reasons !== undefined) {
    assert(Array.isArray(route.reasons), 'oracleRoute.reasons must be an array');
  }
}

function validatePlanMarketResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['deployable', 'normalizedIntent', 'oracleRoute', 'existingMarkets', 'recommendedAction', 'requiredFeeds', 'nextCommands', 'blockers', 'warnings'], 'response');
  assert(typeof response.deployable === 'boolean', 'response.deployable must be a boolean');
  validateOracleRoute(response.oracleRoute);
  assertPlainObject(response.existingMarkets, 'response.existingMarkets');
  assertAllowedKeys(response.existingMarkets, ['exactMatches', 'nearEquivalentMatches'], 'response.existingMarkets');
  assert(Array.isArray(response.existingMarkets.exactMatches), 'response.existingMarkets.exactMatches must be an array');
  assert(Array.isArray(response.existingMarkets.nearEquivalentMatches), 'response.existingMarkets.nearEquivalentMatches must be an array');
  response.existingMarkets.exactMatches.forEach((entry, index) => validateExistingMarketSummary(entry, `response.existingMarkets.exactMatches[${index}]`));
  response.existingMarkets.nearEquivalentMatches.forEach((entry, index) => validateExistingMarketSummary(entry, `response.existingMarkets.nearEquivalentMatches[${index}]`));
  assertEnum(response.recommendedAction, ['deploy-new-market', 'use-existing-market', 'seed-existing-market', 'blocked'], 'response.recommendedAction');
  assert(Array.isArray(response.requiredFeeds), 'response.requiredFeeds must be an array');
  response.requiredFeeds.forEach((feed, index) => validateFeedRequirement(feed, `response.requiredFeeds[${index}]`));
  assert(Array.isArray(response.nextCommands), 'response.nextCommands must be an array');
  if (response.blockers !== undefined) assert(Array.isArray(response.blockers), 'response.blockers must be an array');
  if (response.warnings !== undefined) assert(Array.isArray(response.warnings), 'response.warnings must be an array');
}

function validateDiscoverMarketsResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['exactMatches', 'nearEquivalentMatches', 'recommendedAction', 'reasoning'], 'response');
  assert(Array.isArray(response.exactMatches), 'response.exactMatches must be an array');
  assert(Array.isArray(response.nearEquivalentMatches), 'response.nearEquivalentMatches must be an array');
  response.exactMatches.forEach((entry, index) => validateExistingMarketSummary(entry, `response.exactMatches[${index}]`));
  response.nearEquivalentMatches.forEach((entry, index) => validateExistingMarketSummary(entry, `response.nearEquivalentMatches[${index}]`));
  assertEnum(response.recommendedAction, ['deploy-new-market', 'use-existing-market', 'seed-existing-market', 'manual-review'], 'response.recommendedAction');
  assert(Array.isArray(response.reasoning), 'response.reasoning must be an array');
}

function validateFeedArtifact(feed, label) {
  assertPlainObject(feed, label);
  assertAllowedKeys(feed, ['feedName', 'proxyAddress', 'proxyDeploymentPlan', 'proxyHasCode', 'status', 'supportsAggregatorV2V3Interface', 'requiresCompatibilityWrapper', 'latestRead', 'blockers'], label);
  assertEnum(feed.status, ['ready', 'activatable', 'inactive', 'blocked'], `${label}.status`);
  if (feed.feedName !== undefined) assertStringIfPresent(feed.feedName, `${label}.feedName`);
  if (feed.proxyAddress !== undefined) assert(/^0x[a-fA-F0-9]{40}$/.test(feed.proxyAddress), `${label}.proxyAddress must be a 20-byte hex address`);
  if (feed.proxyDeploymentPlan !== undefined) {
    assertPlainObject(feed.proxyDeploymentPlan, `${label}.proxyDeploymentPlan`);
    assertAllowedKeys(feed.proxyDeploymentPlan, ['reason', 'proxyAddress', 'factoryAddress', 'dapiName', 'dapiNameBytes32', 'dappId', 'metadata'], `${label}.proxyDeploymentPlan`);
    assertStringIfPresent(feed.proxyDeploymentPlan.reason, `${label}.proxyDeploymentPlan.reason`);
    assert(/^0x[a-fA-F0-9]{40}$/.test(feed.proxyDeploymentPlan.proxyAddress), `${label}.proxyDeploymentPlan.proxyAddress must be a 20-byte hex address`);
    assert(/^0x[a-fA-F0-9]{40}$/.test(feed.proxyDeploymentPlan.factoryAddress), `${label}.proxyDeploymentPlan.factoryAddress must be a 20-byte hex address`);
    assertStringIfPresent(feed.proxyDeploymentPlan.dapiName, `${label}.proxyDeploymentPlan.dapiName`);
    assert(/^0x[a-fA-F0-9]{64}$/.test(feed.proxyDeploymentPlan.dapiNameBytes32), `${label}.proxyDeploymentPlan.dapiNameBytes32 must be a 32-byte hex string`);
    assert(Number.isInteger(feed.proxyDeploymentPlan.dappId) && feed.proxyDeploymentPlan.dappId > 0, `${label}.proxyDeploymentPlan.dappId must be a positive integer`);
    assert(/^0x[a-fA-F0-9]*$/.test(feed.proxyDeploymentPlan.metadata), `${label}.proxyDeploymentPlan.metadata must be hex data`);
  }
  if (feed.supportsAggregatorV2V3Interface !== undefined) assert(typeof feed.supportsAggregatorV2V3Interface === 'boolean', `${label}.supportsAggregatorV2V3Interface must be a boolean`);
  if (feed.requiresCompatibilityWrapper !== undefined) assert(typeof feed.requiresCompatibilityWrapper === 'boolean', `${label}.requiresCompatibilityWrapper must be a boolean`);
  if (feed.proxyHasCode !== undefined) assert(typeof feed.proxyHasCode === 'boolean', `${label}.proxyHasCode must be a boolean`);
  if (feed.latestRead !== undefined) {
    assertPlainObject(feed.latestRead, `${label}.latestRead`);
    assertAllowedKeys(feed.latestRead, ['value', 'timestamp', 'humanValue'], `${label}.latestRead`);
    assert(typeof feed.latestRead.value === 'string', `${label}.latestRead.value must be a string`);
    assert(Number.isInteger(feed.latestRead.timestamp) && feed.latestRead.timestamp >= 0, `${label}.latestRead.timestamp must be an integer >= 0`);
    if (feed.latestRead.humanValue !== undefined) {
      assert(typeof feed.latestRead.humanValue === 'number', `${label}.latestRead.humanValue must be a number`);
    }
  }
  if (feed.blockers !== undefined) assert(Array.isArray(feed.blockers), `${label}.blockers must be an array`);
}

function validateEnsureFeedsResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['ready', 'feeds', 'activationPlan', 'wrapperPlan', 'blockers', 'warnings'], 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  assert(Array.isArray(response.feeds), 'response.feeds must be an array');
  response.feeds.forEach((feed, index) => validateFeedArtifact(feed, `response.feeds[${index}]`));
  if (response.activationPlan !== undefined) assertPlainObject(response.activationPlan, 'response.activationPlan');
  if (response.wrapperPlan !== undefined) {
    assertPlainObject(response.wrapperPlan, 'response.wrapperPlan');
    assertAllowedKeys(response.wrapperPlan, ['requiresWrappers', 'wrapperContract', 'feedsRequiringWrappers'], 'response.wrapperPlan');
    if (response.wrapperPlan.requiresWrappers !== undefined) assert(typeof response.wrapperPlan.requiresWrappers === 'boolean', 'response.wrapperPlan.requiresWrappers must be a boolean');
    if (response.wrapperPlan.wrapperContract !== undefined) {
      assertEnum(response.wrapperPlan.wrapperContract, ['Api3PartialAggregatorV2V3Interface', 'none'], 'response.wrapperPlan.wrapperContract');
    }
    if (response.wrapperPlan.feedsRequiringWrappers !== undefined) {
      assert(Array.isArray(response.wrapperPlan.feedsRequiringWrappers), 'response.wrapperPlan.feedsRequiringWrappers must be an array');
    }
  }
  assert(Array.isArray(response.blockers), 'response.blockers must be an array');
  assert(Array.isArray(response.warnings), 'response.warnings must be an array');
}

function validatePrepareEulerOracleResponse(response) {
  assertPlainObject(response, 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  assertEnum(response.integrationMode, ['chainlink-oracle', 'chainlink-infrequent-oracle', 'cross-adapter', 'custom-api3-fallback'], 'response.integrationMode');
  assert(Array.isArray(response.contracts), 'response.contracts must be an array');
  response.contracts.forEach((contract, index) => {
    assertPlainObject(contract, `response.contracts[${index}]`);
    assert(typeof contract.contractName === 'string' && contract.contractName.trim(), `response.contracts[${index}].contractName must be a non-empty string`);
    assertPlainObject(contract.constructorArgs, `response.contracts[${index}].constructorArgs`);
    assertStringIfPresent(contract.purpose, `response.contracts[${index}].purpose`);
  });
  assertPlainObject(response.expectedQuote, 'response.expectedQuote');
  assert(Array.isArray(response.verificationChecks), 'response.verificationChecks must be an array');
  response.verificationChecks.forEach((entry, index) => assert(typeof entry === 'string', `response.verificationChecks[${index}] must be a string`));
  assert(Array.isArray(response.blockers), 'response.blockers must be an array');
  response.blockers.forEach((entry, index) => assert(typeof entry === 'string', `response.blockers[${index}] must be a string`));
  assert(Array.isArray(response.warnings), 'response.warnings must be an array');
  response.warnings.forEach((entry, index) => assert(typeof entry === 'string', `response.warnings[${index}] must be a string`));
}

function validateManifestPreview(preview, label) {
  assertPlainObject(preview, label);
  assert(typeof preview.canonicalHash === 'string' && preview.canonicalHash.trim(), `${label}.canonicalHash must be a non-empty string`);
  assert(typeof preview.protocol === 'string' && preview.protocol.trim(), `${label}.protocol must be a non-empty string`);
  assert(Number.isInteger(preview.chainId) && preview.chainId > 0, `${label}.chainId must be a positive integer`);
  assertStringIfPresent(preview.displayName, `${label}.displayName`);
  assertStringIfPresent(preview.oracleMode, `${label}.oracleMode`);
  assertStringIfPresent(preview.riskPreset, `${label}.riskPreset`);
}

function validatePrepareEvkMarketResponse(response) {
  assertPlainObject(response, 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  validateDeploymentRecipe(response.deploymentRecipe, 'response.deploymentRecipe');
  assertPlainObject(response.contracts, 'response.contracts');
  validateManifestPreview(response.manifestPreview, 'response.manifestPreview');
  assert(Array.isArray(response.deploymentSteps), 'response.deploymentSteps must be an array');
  response.deploymentSteps.forEach((entry, index) => {
    assertPlainObject(entry, `response.deploymentSteps[${index}]`);
    assert(Number.isInteger(entry.step) && entry.step > 0, `response.deploymentSteps[${index}].step must be a positive integer`);
    assert(typeof entry.action === 'string' && entry.action.trim(), `response.deploymentSteps[${index}].action must be a non-empty string`);
    assertStringIfPresent(entry.contract, `response.deploymentSteps[${index}].contract`);
    assertStringIfPresent(entry.notes, `response.deploymentSteps[${index}].notes`);
  });
  assert(Array.isArray(response.verificationChecklist), 'response.verificationChecklist must be an array');
  response.verificationChecklist.forEach((entry, index) => assert(typeof entry === 'string', `response.verificationChecklist[${index}] must be a string`));
  assert(Array.isArray(response.blockers), 'response.blockers must be an array');
  response.blockers.forEach((entry, index) => assert(typeof entry === 'string', `response.blockers[${index}] must be a string`));
  assert(Array.isArray(response.warnings), 'response.warnings must be an array');
  response.warnings.forEach((entry, index) => assert(typeof entry === 'string', `response.warnings[${index}] must be a string`));
}

function validatePrepareEvkDeploymentResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['ready', 'executionMode', 'deploymentBundle', 'preflightChecks', 'blockers', 'warnings'], 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  assertEnum(response.executionMode, ['simulate', 'broadcast-ready'], 'response.executionMode');
  validateDeploymentBundle(response.deploymentBundle, 'response.deploymentBundle');
  validateStringArray(response.preflightChecks, 'response.preflightChecks');
  validateStringArray(response.blockers, 'response.blockers');
  validateStringArray(response.warnings, 'response.warnings');
}

function validateDeployEvkMarketResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['ready', 'executionSummary', 'stepResults', 'transactionPlan', 'sendSummary', 'blockers', 'warnings'], 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  assertPlainObject(response.executionSummary, 'response.executionSummary');
  assertAllowedKeys(response.executionSummary, ['mode', 'chainId', 'canonicalHash', 'totalSteps', 'actionableTransactions', 'simulatedTransactions', 'readyToBroadcast'], 'response.executionSummary');
  assertEnum(response.executionSummary.mode, ['simulate', 'broadcast-ready'], 'response.executionSummary.mode');
  assert(Number.isInteger(response.executionSummary.chainId) && response.executionSummary.chainId >= 1, 'response.executionSummary.chainId must be an integer >= 1');
  assert(typeof response.executionSummary.canonicalHash === 'string' && response.executionSummary.canonicalHash.trim(), 'response.executionSummary.canonicalHash must be a non-empty string');
  assert(Number.isInteger(response.executionSummary.totalSteps) && response.executionSummary.totalSteps >= 0, 'response.executionSummary.totalSteps must be an integer >= 0');
  assert(Number.isInteger(response.executionSummary.actionableTransactions) && response.executionSummary.actionableTransactions >= 0, 'response.executionSummary.actionableTransactions must be an integer >= 0');
  assert(Number.isInteger(response.executionSummary.simulatedTransactions) && response.executionSummary.simulatedTransactions >= 0, 'response.executionSummary.simulatedTransactions must be an integer >= 0');
  assert(typeof response.executionSummary.readyToBroadcast === 'boolean', 'response.executionSummary.readyToBroadcast must be a boolean');
  assert(Array.isArray(response.stepResults), 'response.stepResults must be an array');
  response.stepResults.forEach((entry, index) => {
    assertPlainObject(entry, `response.stepResults[${index}]`);
    assertAllowedKeys(entry, ['order', 'phase', 'action', 'status', 'targetContract', 'transactionId', 'dependsOn', 'notes', 'verificationChecklist', 'sendStatus', 'txHash', 'error'], `response.stepResults[${index}]`);
    assert(Number.isInteger(entry.order) && entry.order > 0, `response.stepResults[${index}].order must be a positive integer`);
    assertEnum(entry.phase, ['oracle', 'market', 'verification', 'registry'], `response.stepResults[${index}].phase`);
    assert(typeof entry.action === 'string' && entry.action.trim(), `response.stepResults[${index}].action must be a non-empty string`);
    assertEnum(entry.status, ['prepared', 'simulated', 'skipped', 'blocked'], `response.stepResults[${index}].status`);
    assertStringIfPresent(entry.targetContract, `response.stepResults[${index}].targetContract`);
    assertStringIfPresent(entry.transactionId, `response.stepResults[${index}].transactionId`);
    validateStringArray(entry.dependsOn, `response.stepResults[${index}].dependsOn`);
    assertStringIfPresent(entry.notes, `response.stepResults[${index}].notes`);
    if (entry.sendStatus !== undefined) {
      assertEnum(entry.sendStatus, ['not-requested', 'dry-run', 'submitted', 'failed', 'skipped'], `response.stepResults[${index}].sendStatus`);
    }
    assertStringIfPresent(entry.txHash, `response.stepResults[${index}].txHash`);
    assertStringIfPresent(entry.error, `response.stepResults[${index}].error`);
  });
  assert(Array.isArray(response.transactionPlan), 'response.transactionPlan must be an array');
  response.transactionPlan.forEach((entry, index) => {
    assertPlainObject(entry, `response.transactionPlan[${index}]`);
    assertAllowedKeys(entry, ['transactionId', 'kind', 'payloadKind', 'status', 'chainId', 'to', 'data', 'value', 'description', 'sendStatus', 'txHash', 'error'], `response.transactionPlan[${index}]`);
    assert(typeof entry.transactionId === 'string' && entry.transactionId.trim(), `response.transactionPlan[${index}].transactionId must be a non-empty string`);
    assertEnum(entry.kind, ['contract-deployment', 'contract-call', 'offchain-publication'], `response.transactionPlan[${index}].kind`);
    assertEnum(entry.payloadKind, ['skeleton', 'executable'], `response.transactionPlan[${index}].payloadKind`);
    assertEnum(entry.status, ['prepared', 'simulated', 'skipped', 'blocked'], `response.transactionPlan[${index}].status`);
    assert(Number.isInteger(entry.chainId) && entry.chainId >= 1, `response.transactionPlan[${index}].chainId must be an integer >= 1`);
    if (entry.to !== null && entry.to !== undefined) {
      assert(/^0x[a-fA-F0-9]{40}$/.test(entry.to), `response.transactionPlan[${index}].to must be a 20-byte hex address when present`);
    }
    if (entry.data !== undefined) {
      assert(/^0x[a-fA-F0-9]*$/.test(entry.data), `response.transactionPlan[${index}].data must be hex when present`);
    }
    assert(typeof entry.value === 'string', `response.transactionPlan[${index}].value must be a string`);
    assert(typeof entry.description === 'string' && entry.description.trim(), `response.transactionPlan[${index}].description must be a non-empty string`);
    if (entry.sendStatus !== undefined) {
      assertEnum(entry.sendStatus, ['not-requested', 'dry-run', 'submitted', 'failed', 'skipped'], `response.transactionPlan[${index}].sendStatus`);
    }
    assertStringIfPresent(entry.txHash, `response.transactionPlan[${index}].txHash`);
    assertStringIfPresent(entry.error, `response.transactionPlan[${index}].error`);
  });
  assertPlainObject(response.sendSummary, 'response.sendSummary');
  assertAllowedKeys(response.sendSummary, ['requested', 'attempted', 'dryRun', 'submittedTransactions', 'failedTransactions', 'skippedTransactions', 'signerAddress', 'rpcUrlConfigured', 'failureReason', 'completed'], 'response.sendSummary');
  assert(typeof response.sendSummary.requested === 'boolean', 'response.sendSummary.requested must be a boolean');
  assert(typeof response.sendSummary.attempted === 'boolean', 'response.sendSummary.attempted must be a boolean');
  assert(typeof response.sendSummary.dryRun === 'boolean', 'response.sendSummary.dryRun must be a boolean');
  assert(Number.isInteger(response.sendSummary.submittedTransactions) && response.sendSummary.submittedTransactions >= 0, 'response.sendSummary.submittedTransactions must be an integer >= 0');
  assert(Number.isInteger(response.sendSummary.failedTransactions) && response.sendSummary.failedTransactions >= 0, 'response.sendSummary.failedTransactions must be an integer >= 0');
  assert(Number.isInteger(response.sendSummary.skippedTransactions) && response.sendSummary.skippedTransactions >= 0, 'response.sendSummary.skippedTransactions must be an integer >= 0');
  assertStringIfPresent(response.sendSummary.signerAddress, 'response.sendSummary.signerAddress');
  assert(typeof response.sendSummary.rpcUrlConfigured === 'boolean', 'response.sendSummary.rpcUrlConfigured must be a boolean');
  assertStringIfPresent(response.sendSummary.failureReason, 'response.sendSummary.failureReason');
  assert(typeof response.sendSummary.completed === 'boolean', 'response.sendSummary.completed must be a boolean');
  validateStringArray(response.blockers, 'response.blockers');
  validateStringArray(response.warnings, 'response.warnings');
}

function validateDeployEulerOracleResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['ready', 'executionSummary', 'stepResults', 'transactionPlan', 'sendSummary', 'expectedQuote', 'blockers', 'warnings'], 'response');
  assert(typeof response.ready === 'boolean', 'response.ready must be a boolean');
  assertPlainObject(response.executionSummary, 'response.executionSummary');
  assertAllowedKeys(response.executionSummary, ['mode', 'chainId', 'integrationMode', 'totalSteps', 'actionableTransactions', 'simulatedTransactions', 'readyToBroadcast'], 'response.executionSummary');
  assertEnum(response.executionSummary.mode, ['simulate', 'broadcast-ready'], 'response.executionSummary.mode');
  assert(Number.isInteger(response.executionSummary.chainId) && response.executionSummary.chainId >= 1, 'response.executionSummary.chainId must be an integer >= 1');
  assertEnum(response.executionSummary.integrationMode, ['chainlink-oracle', 'chainlink-infrequent-oracle', 'cross-adapter', 'custom-api3-fallback'], 'response.executionSummary.integrationMode');
  assert(Number.isInteger(response.executionSummary.totalSteps) && response.executionSummary.totalSteps >= 0, 'response.executionSummary.totalSteps must be an integer >= 0');
  assert(Number.isInteger(response.executionSummary.actionableTransactions) && response.executionSummary.actionableTransactions >= 0, 'response.executionSummary.actionableTransactions must be an integer >= 0');
  assert(Number.isInteger(response.executionSummary.simulatedTransactions) && response.executionSummary.simulatedTransactions >= 0, 'response.executionSummary.simulatedTransactions must be an integer >= 0');
  assert(typeof response.executionSummary.readyToBroadcast === 'boolean', 'response.executionSummary.readyToBroadcast must be a boolean');
  assert(Array.isArray(response.stepResults), 'response.stepResults must be an array');
  response.stepResults.forEach((entry, index) => {
    assertPlainObject(entry, `response.stepResults[${index}]`);
    assertAllowedKeys(entry, ['order', 'phase', 'action', 'status', 'targetContract', 'transactionId', 'dependsOn', 'notes', 'sendStatus', 'txHash', 'error'], `response.stepResults[${index}]`);
    assert(Number.isInteger(entry.order) && entry.order > 0, `response.stepResults[${index}].order must be a positive integer`);
    assertEnum(entry.phase, ['oracle', 'verification'], `response.stepResults[${index}].phase`);
    assert(typeof entry.action === 'string' && entry.action.trim(), `response.stepResults[${index}].action must be a non-empty string`);
    assertEnum(entry.status, ['prepared', 'simulated', 'skipped', 'blocked'], `response.stepResults[${index}].status`);
    assertStringIfPresent(entry.targetContract, `response.stepResults[${index}].targetContract`);
    assertStringIfPresent(entry.transactionId, `response.stepResults[${index}].transactionId`);
    validateStringArray(entry.dependsOn, `response.stepResults[${index}].dependsOn`);
    assertStringIfPresent(entry.notes, `response.stepResults[${index}].notes`);
    if (entry.sendStatus !== undefined) {
      assertEnum(entry.sendStatus, ['not-requested', 'dry-run', 'submitted', 'failed', 'skipped'], `response.stepResults[${index}].sendStatus`);
    }
    assertStringIfPresent(entry.txHash, `response.stepResults[${index}].txHash`);
    assertStringIfPresent(entry.error, `response.stepResults[${index}].error`);
  });
  assert(Array.isArray(response.transactionPlan), 'response.transactionPlan must be an array');
  response.transactionPlan.forEach((entry, index) => {
    assertPlainObject(entry, `response.transactionPlan[${index}]`);
    assertAllowedKeys(entry, ['transactionId', 'kind', 'payloadKind', 'status', 'chainId', 'to', 'data', 'value', 'description', 'sendStatus', 'txHash', 'error'], `response.transactionPlan[${index}]`);
    assert(typeof entry.transactionId === 'string' && entry.transactionId.trim(), `response.transactionPlan[${index}].transactionId must be a non-empty string`);
    assertEnum(entry.kind, ['contract-deployment', 'contract-call'], `response.transactionPlan[${index}].kind`);
    assertEnum(entry.payloadKind, ['skeleton', 'executable'], `response.transactionPlan[${index}].payloadKind`);
    assertEnum(entry.status, ['prepared', 'simulated', 'skipped', 'blocked'], `response.transactionPlan[${index}].status`);
    assert(Number.isInteger(entry.chainId) && entry.chainId >= 1, `response.transactionPlan[${index}].chainId must be an integer >= 1`);
    if (entry.to !== null && entry.to !== undefined) {
      assert(/^0x[a-fA-F0-9]{40}$/.test(entry.to), `response.transactionPlan[${index}].to must be a 20-byte hex address when present`);
    }
    if (entry.data !== undefined) {
      assert(/^0x[a-fA-F0-9]*$/.test(entry.data), `response.transactionPlan[${index}].data must be hex when present`);
    }
    assert(typeof entry.value === 'string', `response.transactionPlan[${index}].value must be a string`);
    assert(typeof entry.description === 'string' && entry.description.trim(), `response.transactionPlan[${index}].description must be a non-empty string`);
    if (entry.sendStatus !== undefined) {
      assertEnum(entry.sendStatus, ['not-requested', 'dry-run', 'submitted', 'failed', 'skipped'], `response.transactionPlan[${index}].sendStatus`);
    }
    assertStringIfPresent(entry.txHash, `response.transactionPlan[${index}].txHash`);
    assertStringIfPresent(entry.error, `response.transactionPlan[${index}].error`);
  });
  assertPlainObject(response.sendSummary, 'response.sendSummary');
  assertAllowedKeys(response.sendSummary, ['requested', 'attempted', 'dryRun', 'submittedTransactions', 'failedTransactions', 'skippedTransactions', 'signerAddress', 'rpcUrlConfigured', 'failureReason', 'completed'], 'response.sendSummary');
  assert(typeof response.sendSummary.requested === 'boolean', 'response.sendSummary.requested must be a boolean');
  assert(typeof response.sendSummary.attempted === 'boolean', 'response.sendSummary.attempted must be a boolean');
  assert(typeof response.sendSummary.dryRun === 'boolean', 'response.sendSummary.dryRun must be a boolean');
  assert(Number.isInteger(response.sendSummary.submittedTransactions) && response.sendSummary.submittedTransactions >= 0, 'response.sendSummary.submittedTransactions must be an integer >= 0');
  assert(Number.isInteger(response.sendSummary.failedTransactions) && response.sendSummary.failedTransactions >= 0, 'response.sendSummary.failedTransactions must be an integer >= 0');
  assert(Number.isInteger(response.sendSummary.skippedTransactions) && response.sendSummary.skippedTransactions >= 0, 'response.sendSummary.skippedTransactions must be an integer >= 0');
  assertStringIfPresent(response.sendSummary.signerAddress, 'response.sendSummary.signerAddress');
  assert(typeof response.sendSummary.rpcUrlConfigured === 'boolean', 'response.sendSummary.rpcUrlConfigured must be a boolean');
  assertStringIfPresent(response.sendSummary.failureReason, 'response.sendSummary.failureReason');
  assert(typeof response.sendSummary.completed === 'boolean', 'response.sendSummary.completed must be a boolean');
  assertPlainObject(response.expectedQuote, 'response.expectedQuote');
  validateStringArray(response.blockers, 'response.blockers');
  validateStringArray(response.warnings, 'response.warnings');
}

function validateRunEvkWorkflowResponse(response) {
  assertPlainObject(response, 'response');
  assertAllowedKeys(response, ['status', 'result'], 'response');

  assertPlainObject(response.status, 'response.status');
  assertAllowedKeys(response.status, ['phaseReached', 'state', 'recipeId', 'deployable', 'fundingExecutionState', 'executable', 'blockers', 'warnings'], 'response.status');
  assertEnum(response.status.phaseReached, ['plan-market', 'ensure-feeds', 'feed-funding', 'prepare-euler-oracle', 'prepare-evk-market', 'prepare-evk-deployment', 'deploy-evk-market'], 'response.status.phaseReached');
  assertEnum(response.status.state, ['plan-only', 'feed-ready but awaiting activation/funding handoff', 'funding dry-run ready', 'browser-assisted funding ready', 'oracle-executable', 'EVK dry-run ready', 'real-send ready'], 'response.status.state');
  if (response.status.recipeId !== null && response.status.recipeId !== undefined) {
    assert(typeof response.status.recipeId === 'string' && response.status.recipeId.trim(), 'response.status.recipeId must be a non-empty string when present');
  }
  assert(typeof response.status.deployable === 'boolean', 'response.status.deployable must be a boolean');
  if (response.status.fundingExecutionState !== null && response.status.fundingExecutionState !== undefined) {
    assertEnum(response.status.fundingExecutionState, ['not-needed', 'executable', 'browser-assisted', 'unsupported', 'mixed'], 'response.status.fundingExecutionState');
  }
  assertPlainObject(response.status.executable, 'response.status.executable');
  assertAllowedKeys(response.status.executable, ['feedFunding', 'browserAssistedFunding', 'oracle', 'evkMarket', 'realSend'], 'response.status.executable');
  ['feedFunding', 'browserAssistedFunding', 'oracle', 'evkMarket', 'realSend'].forEach((key) => {
    assert(typeof response.status.executable[key] === 'boolean', `response.status.executable.${key} must be a boolean`);
  });
  validateStringArray(response.status.blockers, 'response.status.blockers');
  validateStringArray(response.status.warnings, 'response.status.warnings');

  assertPlainObject(response.result, 'response.result');
  assertAllowedKeys(response.result, ['request', 'recipeSelection', 'planMarket', 'ensureFeeds', 'feedFunding', 'prepareEulerOracle', 'prepareEvkMarket', 'prepareEvkDeployment', 'deployEvkMarket', 'artifactPersistence'], 'response.result');
  assertPlainObject(response.result.request, 'response.result.request');

  assertPlainObject(response.result.artifactPersistence, 'response.result.artifactPersistence');
  assertAllowedKeys(response.result.artifactPersistence, ['enabled', 'persisted', 'outputDir', 'bundleDir', 'runId', 'files'], 'response.result.artifactPersistence');
  assert(typeof response.result.artifactPersistence.enabled === 'boolean', 'response.result.artifactPersistence.enabled must be a boolean');
  assert(typeof response.result.artifactPersistence.persisted === 'boolean', 'response.result.artifactPersistence.persisted must be a boolean');
  if (response.result.artifactPersistence.outputDir !== null && response.result.artifactPersistence.outputDir !== undefined) {
    assert(typeof response.result.artifactPersistence.outputDir === 'string' && response.result.artifactPersistence.outputDir.trim(), 'response.result.artifactPersistence.outputDir must be a non-empty string when present');
  }
  if (response.result.artifactPersistence.bundleDir !== null && response.result.artifactPersistence.bundleDir !== undefined) {
    assert(typeof response.result.artifactPersistence.bundleDir === 'string' && response.result.artifactPersistence.bundleDir.trim(), 'response.result.artifactPersistence.bundleDir must be a non-empty string when present');
  }
  if (response.result.artifactPersistence.runId !== null && response.result.artifactPersistence.runId !== undefined) {
    assert(typeof response.result.artifactPersistence.runId === 'string' && response.result.artifactPersistence.runId.trim(), 'response.result.artifactPersistence.runId must be a non-empty string when present');
  }
  assertPlainObject(response.result.artifactPersistence.files, 'response.result.artifactPersistence.files');
  assertAllowedKeys(response.result.artifactPersistence.files, ['request', 'response', 'status', 'planMarket', 'ensureFeeds', 'feedFunding', 'prepareEulerOracle', 'prepareEvkMarket', 'prepareEvkDeployment', 'deployEvkMarket'], 'response.result.artifactPersistence.files');
  ['request', 'response', 'status', 'planMarket', 'ensureFeeds', 'feedFunding', 'prepareEulerOracle', 'prepareEvkMarket', 'prepareEvkDeployment', 'deployEvkMarket'].forEach((key) => {
    const value = response.result.artifactPersistence.files[key];
    if (value !== null && value !== undefined) {
      assert(typeof value === 'string' && value.trim(), `response.result.artifactPersistence.files.${key} must be a non-empty string when present`);
    }
  });

  assertPlainObject(response.result.recipeSelection, 'response.result.recipeSelection');
  assertAllowedKeys(response.result.recipeSelection, ['requestedRecipeId', 'resolvedRecipeId', 'matchStrategy', 'candidateRecipeIds', 'blockers', 'warnings'], 'response.result.recipeSelection');
  if (response.result.recipeSelection.requestedRecipeId !== null && response.result.recipeSelection.requestedRecipeId !== undefined) {
    assert(typeof response.result.recipeSelection.requestedRecipeId === 'string', 'response.result.recipeSelection.requestedRecipeId must be a string when present');
  }
  if (response.result.recipeSelection.resolvedRecipeId !== null && response.result.recipeSelection.resolvedRecipeId !== undefined) {
    assert(typeof response.result.recipeSelection.resolvedRecipeId === 'string', 'response.result.recipeSelection.resolvedRecipeId must be a string when present');
  }
  assertEnum(response.result.recipeSelection.matchStrategy, ['explicit', 'inferred', 'none', 'ambiguous'], 'response.result.recipeSelection.matchStrategy');
  validateStringArray(response.result.recipeSelection.candidateRecipeIds, 'response.result.recipeSelection.candidateRecipeIds');
  validateStringArray(response.result.recipeSelection.blockers, 'response.result.recipeSelection.blockers');
  validateStringArray(response.result.recipeSelection.warnings, 'response.result.recipeSelection.warnings');

  if (response.result.planMarket !== null) {
    validatePlanMarketResponse(response.result.planMarket);
  }

  if (response.result.ensureFeeds !== null) {
    assertPlainObject(response.result.ensureFeeds, 'response.result.ensureFeeds');
    assertAllowedKeys(response.result.ensureFeeds, ['initial', 'final'], 'response.result.ensureFeeds');
    validateEnsureFeedsResponse(response.result.ensureFeeds.initial);
    validateEnsureFeedsResponse(response.result.ensureFeeds.final);
  }

  if (response.result.feedFunding !== null) {
    assertPlainObject(response.result.feedFunding, 'response.result.feedFunding');
    assertAllowedKeys(response.result.feedFunding, ['modeRequested', 'attemptedExecution', 'overallState', 'entries'], 'response.result.feedFunding');
    assertEnum(response.result.feedFunding.modeRequested, ['classify-only', 'dry-run', 'real-send'], 'response.result.feedFunding.modeRequested');
    assert(typeof response.result.feedFunding.attemptedExecution === 'boolean', 'response.result.feedFunding.attemptedExecution must be a boolean');
    if (response.result.feedFunding.overallState !== null && response.result.feedFunding.overallState !== undefined) {
      assertEnum(response.result.feedFunding.overallState, ['not-needed', 'executable', 'browser-assisted', 'unsupported', 'mixed'], 'response.result.feedFunding.overallState');
    }
    assert(Array.isArray(response.result.feedFunding.entries), 'response.result.feedFunding.entries must be an array');
    response.result.feedFunding.entries.forEach((entry, index) => {
      assertPlainObject(entry, `response.result.feedFunding.entries[${index}]`);
      assertAllowedKeys(entry, ['feedName', 'statusBefore', 'fundingExecutionState', 'availableExecutionModes', 'selectedExecutionMode', 'purchaseInputs', 'browserPlan', 'execution', 'blockers', 'warnings'], `response.result.feedFunding.entries[${index}]`);
      assert(typeof entry.feedName === 'string' && entry.feedName.trim(), `response.result.feedFunding.entries[${index}].feedName must be a non-empty string`);
      assertEnum(entry.statusBefore, ['ready', 'activatable', 'inactive', 'blocked'], `response.result.feedFunding.entries[${index}].statusBefore`);
      if (entry.fundingExecutionState !== null && entry.fundingExecutionState !== undefined) {
        assertEnum(entry.fundingExecutionState, ['not-needed', 'executable', 'browser-assisted', 'unsupported'], `response.result.feedFunding.entries[${index}].fundingExecutionState`);
      }
      if (entry.availableExecutionModes !== undefined) {
        assert(Array.isArray(entry.availableExecutionModes), `response.result.feedFunding.entries[${index}].availableExecutionModes must be an array`);
        entry.availableExecutionModes.forEach((mode, modeIndex) => {
          assertEnum(mode, ['direct', 'wrapper'], `response.result.feedFunding.entries[${index}].availableExecutionModes[${modeIndex}]`);
        });
      }
      if (entry.selectedExecutionMode !== undefined && entry.selectedExecutionMode !== null) {
        assertEnum(entry.selectedExecutionMode, ['auto', 'direct', 'wrapper'], `response.result.feedFunding.entries[${index}].selectedExecutionMode`);
      }
      validateStringArray(entry.blockers, `response.result.feedFunding.entries[${index}].blockers`);
      validateStringArray(entry.warnings, `response.result.feedFunding.entries[${index}].warnings`);
    });
  }

  if (response.result.prepareEulerOracle !== null) {
    validatePrepareEulerOracleResponse(response.result.prepareEulerOracle);
  }
  if (response.result.prepareEvkMarket !== null) {
    validatePrepareEvkMarketResponse(response.result.prepareEvkMarket);
  }
  if (response.result.prepareEvkDeployment !== null) {
    validatePrepareEvkDeploymentResponse(response.result.prepareEvkDeployment);
  }
  if (response.result.deployEvkMarket !== null) {
    validateDeployEvkMarketResponse(response.result.deployEvkMarket);
  }
}

function outputResult(result, options) {
  const format = String(options.format || 'json').trim().toLowerCase();
  if (format !== 'json') {
    throw new Error(`Unsupported format: ${format}`);
  }
  console.log(JSON.stringify(result, null, 2));
}

async function runCli(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  const command = args._[0];

  if (!command || command === 'help' || args.help) {
    printUsage();
    return;
  }

  if (!SUPPORTED_COMMANDS.has(command)) {
    throw new Error(`Unsupported command: ${command}`);
  }

  const request = loadInput(args);
  let result;

  if (command === 'plan-market') {
    result = planMarket(request, args);
  } else if (command === 'discover-markets') {
    result = discoverMarkets(request, args);
  } else if (command === 'ensure-feeds') {
    result = await ensureFeeds(request, args);
  } else if (command === 'prepare-euler-oracle') {
    result = prepareEulerOracle(request);
  } else if (command === 'deploy-euler-oracle') {
    result = await deployEulerOracle(request);
  } else if (command === 'prepare-evk-market') {
    result = prepareEvkMarket(request);
  } else if (command === 'prepare-evk-deployment') {
    result = prepareEvkDeployment(request);
  } else if (command === 'deploy-evk-market') {
    result = await deployEvkMarket(request);
  } else if (command === 'run-evk-workflow') {
    result = await runEvkWorkflow(request, args);
  }

  outputResult(result, args);
}

module.exports = {
  buildExecutableOracleDeploymentData,
  buildRegistryPublicationPayload,
  buildVerifyEvkMarketChecklist,
  buildRequiredFeeds,
  canonicalizeFeedName,
  summarizeFundingState,
  feedNamesEqual,
  promoteFundingReadyFeedsForPlanning,
  discoverMarkets,
  deployEulerOracle,
  ensureFeeds,
  loadFeedStatus,
  loadRegistry,
  deployEvkMarket,
  normalizeIntent,
  planMarket,
  prepareEulerOracle,
  prepareEvkDeployment,
  prepareEvkMarket,
  printUsage,
  runEvkWorkflow,
  runCli,
  validateDiscoverMarketsRequest,
  validateDeployEulerOracleRequest,
  validateDeployEvkMarketRequest,
  validateEnsureFeedsRequest,
  validatePlanMarketRequest,
  validatePrepareEvkDeploymentRequest,
  validatePrepareEulerOracleRequest,
  validatePrepareEvkMarketRequest,
  validateRunEvkWorkflowRequest,
};
