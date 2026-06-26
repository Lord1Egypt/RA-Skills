const {
  AbiCoder,
  JsonRpcProvider,
  Wallet,
  encodeBytes32String,
  decodeBytes32String,
  getAddress,
  isAddress,
  keccak256,
  solidityPackedKeccak256,
} = require('ethers');
const {
  AirseekerRegistry__factory,
  Api3MarketV2__factory,
  Api3ReaderProxyV1__factory,
  Api3ReaderProxyV1Factory__factory,
  Api3ServerV1__factory,
  computeCommunalApi3ReaderProxyV1Address,
} = require('@api3/contracts');
const deploymentAddresses = require('@api3/contracts/dist/deployments/addresses.json');
const dapiCatalog = require('@api3/dapi-management/dist/data/dapis.json');
const chainCatalog = require('@api3/dapi-management/dist/data/chains.json');
const {
  api3ApiIntegrations,
  dapiManagementMerkleTreeData,
  deriveSponsorWalletAddress,
} = require('@api3/dapi-management');

const ABI_CODER = AbiCoder.defaultAbiCoder();
const MARKET_BASE_URL = 'https://market.api3.org';
const MARKET_PRICING_BASE_URL = 'https://api3dao.github.io/data-feeds/market/dapi-pricing';
const ZERO_BYTES32 = `0x${'00'.repeat(32)}`;
const HEARTBEAT_SECONDS = 24 * 60 * 60;
const MAINNET_SUBSCRIPTION_DURATION_DAYS = 90;
const TESTNET_SUBSCRIPTION_DURATION_DAYS = 7;
const SUPPORTED_DEVIATION_CHOICES_PERCENT = [5, 2.5, 1, 0.5, 0.25];
const DEFAULT_DEVIATION_CHOICE_PERCENT = '0.5';
const SEND_ACKNOWLEDGEMENT = 'I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS';
let liveDapiManagementMerkleTreeDataPromise = null;
const CHAIN_ALIASES = {
  arbitrum: 42161,
  'arbitrum-one': 42161,
  arb1: 42161,
  ethereum: 1,
  mainnet: 1,
  base: 8453,
  optimism: 10,
  op: 10,
  linea: 59144,
};

function parseArgs(argv) {
  const parsed = { _: [] };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (!token.startsWith('--')) {
      parsed._.push(token);
      continue;
    }

    const [rawKey, inlineValue] = token.slice(2).split('=', 2);
    const key = rawKey.replace(/-([a-z])/g, (_, char) => char.toUpperCase());

    if (inlineValue !== undefined) {
      parsed[key] = inlineValue;
      continue;
    }

    const nextToken = argv[index + 1];
    if (!nextToken || nextToken.startsWith('--')) {
      parsed[key] = true;
      continue;
    }

    parsed[key] = nextToken;
    index += 1;
  }

  return parsed;
}

function printUsage() {
  console.error(`Usage:
  api3-feed-manager resolve \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager discover \
    --query ETH \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager ensure-active \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager prepare-activation \
    --dapi-name STX/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager browser-plan \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager contract-plan \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager queue-plan \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum

  api3-feed-manager purchase-inputs \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --deviation-choice 0.5 \
    --duration 7776000

  api3-feed-manager prepare-contract-call \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --deviation-choice 0.5 \
    --duration 7776000

  api3-feed-manager execute-buy-subscription \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --deviation-choice 0.5 \
    --duration 7776000 \
    --private-key <private-key-hex>

  api3-feed-manager execute-buy-subscription \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --execution-mode wrapper \
    --private-key <private-key-hex>

  api3-feed-manager deploy-communal-proxy \
    --dapi-name ETH/USD \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --private-key <private-key-hex>

  api3-feed-manager coverage-audit \
    --rpc-url https://arb1.arbitrum.io/rpc \
    --chain arbitrum \
    --limit 20

  api3-feed-manager coverage-audit \
    --chains arbitrum,base,optimism \
    --query ETH \
    --format csv

  api3-feed-manager coverage-matrix \
    --chains arbitrum,base,optimism \
    --query ETH

  api3-feed-manager supported-chains

Optional overrides:
  --api3-server <address>
  --airseeker-registry <address>
  --chain-id <number>
  --limit <number>
  --chains <chainA,chainB,...>
  --category <category-or-blocker>
  --format <json|csv>
  --csv
  --json
`);
}

function normalizeChainId(input) {
  if (input === undefined || input === null || input === '') {
    return undefined;
  }

  if (typeof input === 'number') {
    return input;
  }

  const normalized = String(input).trim().toLowerCase();
  if (/^\d+$/.test(normalized)) {
    return Number(normalized);
  }

  return CHAIN_ALIASES[normalized];
}

function getDefaultAddresses(chainId) {
  const normalizedChainId = String(chainId);

  return {
    api3Server: deploymentAddresses.Api3ServerV1?.[normalizedChainId],
    airseekerRegistry: deploymentAddresses.AirseekerRegistry?.[normalizedChainId],
    api3ReaderProxyV1Factory: deploymentAddresses.Api3ReaderProxyV1Factory?.[normalizedChainId],
  };
}

function decodeDataFeedDetails(dataFeedDetails) {
  const byteLength = (dataFeedDetails.length - 2) / 2;

  if (byteLength === 64) {
    const [airnode, templateId] = ABI_CODER.decode(['address', 'bytes32'], dataFeedDetails);
    return {
      kind: 'beacon',
      byteLength,
      airnodes: [airnode],
      templateIds: [templateId],
    };
  }

  const [airnodes, templateIds] = ABI_CODER.decode(['address[]', 'bytes32[]'], dataFeedDetails);
  return {
    kind: 'beacon-set',
    byteLength,
    airnodes: [...airnodes],
    templateIds: [...templateIds],
  };
}

function deriveCurrentPublicDataFeedModel({ dapiName, providerAliases }) {
  if (!dapiName || !Array.isArray(providerAliases) || providerAliases.length === 0) {
    return null;
  }

  try {
    const beaconMetadata = providerAliases.map((providerAlias) => {
      const airnode = api3ApiIntegrations.getAirnodeAddressByAlias(providerAlias);
      const oisTitle = api3ApiIntegrations.getOisTitleByFeedNameAndAirnodeAddress(dapiName, airnode);
      const templateId = api3ApiIntegrations.deriveTemplateId({
        feedName: dapiName,
        oisTitle,
        airnodeAddress: airnode,
      });
      const beaconId = solidityPackedKeccak256(['address', 'bytes32'], [airnode, templateId]);

      return {
        providerAlias,
        airnode,
        oisTitle,
        templateId,
        beaconId,
      };
    });

    const beaconIds = beaconMetadata.map((entry) => entry.beaconId);
    const dataFeedId = beaconIds.length === 1
      ? beaconIds[0]
      : keccak256(ABI_CODER.encode(['bytes32[]'], [beaconIds]));

    return {
      derivable: true,
      dapiName,
      providerAliases: [...providerAliases],
      beaconMetadata,
      dataFeedId,
      dataFeedDetails: ABI_CODER.encode([
        'address[]',
        'bytes32[]',
      ], [
        beaconMetadata.map((entry) => entry.airnode),
        beaconMetadata.map((entry) => entry.templateId),
      ]),
    };
  } catch (error) {
    return {
      derivable: false,
      dapiName,
      providerAliases: [...providerAliases],
      failureReason: error?.message || String(error),
    };
  }
}

function decodeUpdateParameters(updateParameters) {
  const [deviationThresholdPpm, heartbeatInterval, timeout] = ABI_CODER.decode(
    ['uint256', 'int224', 'uint256'],
    updateParameters
  );

  return {
    deviationThresholdPpm: deviationThresholdPpm.toString(),
    heartbeatInterval: heartbeatInterval.toString(),
    timeout: timeout.toString(),
  };
}

const DAPI_SYMBOL_ALIASES = Object.freeze({
  WETH: 'ETH',
  WBTC: 'BTC',
  CBBTC: 'BTC',
  TBTC: 'BTC',
});

function normalizeDapiName(name) {
  const normalized = String(name || '').trim().toUpperCase();
  if (!normalized) {
    return normalized;
  }

  if (!normalized.includes('/')) {
    return DAPI_SYMBOL_ALIASES[normalized] || normalized;
  }

  return normalized
    .split('/')
    .map((segment) => DAPI_SYMBOL_ALIASES[segment] || segment)
    .join('/');
}

function normalizeLiteralDapiName(name) {
  return String(name || '').trim().toUpperCase();
}

function findLiteralExactMatches(matches, requestedName) {
  const normalizedRequested = normalizeLiteralDapiName(requestedName);
  return matches.filter((match) => normalizeLiteralDapiName(match.dapiName) === normalizedRequested);
}

function findNormalizedExactMatches(matches, requestedName) {
  const normalizedRequested = normalizeDapiName(requestedName);
  return matches.filter((match) => normalizeDapiName(match.dapiName) === normalizedRequested);
}

function selectPreferredExactMatches(matches, requestedName) {
  const literalExactMatches = findLiteralExactMatches(matches, requestedName);
  if (literalExactMatches.length > 0) {
    return {
      matchMode: 'literal',
      preferredMatch: literalExactMatches[0],
      exactMatches: literalExactMatches,
      ambiguous: literalExactMatches.length > 1,
    };
  }

  const normalizedExactMatches = findNormalizedExactMatches(matches, requestedName);
  return {
    matchMode: 'normalized',
    preferredMatch: normalizedExactMatches[0] || null,
    exactMatches: normalizedExactMatches,
    ambiguous: normalizedExactMatches.length > 1,
  };
}

function slugifyDapiName(name) {
  return String(name || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function getChainCatalogEntry(chainInput, chainId) {
  const normalizedInput = String(chainInput || '').trim().toLowerCase();
  const candidates = new Set([
    normalizedInput,
    String(chainId || ''),
    ...Object.entries(CHAIN_ALIASES)
      .filter(([, mappedChainId]) => mappedChainId === chainId)
      .map(([alias]) => alias),
  ]);

  return chainCatalog.find((entry) => candidates.has(String(entry.alias || '').toLowerCase()));
}

function getMarketChainSlug(chainInput, chainId) {
  const chainCatalogEntry = getChainCatalogEntry(chainInput, chainId);
  return String(chainCatalogEntry?.alias || chainInput || chainId).trim().toLowerCase();
}

function parseChainTargetsInput(value) {
  if (value === undefined || value === null || value === '') {
    return [];
  }

  return String(value)
    .split(',')
    .map((entry) => entry.trim())
    .filter(Boolean);
}

function getPreferredChainLabel(chainInput, chainId) {
  const chainCatalogEntry = getChainCatalogEntry(chainInput, chainId);
  return String(chainCatalogEntry?.alias || chainInput || chainId).trim().toLowerCase();
}

async function resolveCoverageChainTargets(options) {
  const requestedChains = parseChainTargetsInput(options.chains);

  if (requestedChains.length > 0) {
    return requestedChains.map((chainInput) => {
      const chainId = normalizeChainId(chainInput);
      if (!chainId) {
        throw new Error(`Unsupported chain in --chains: ${chainInput}`);
      }

      return {
        chainId,
        requested: chainInput,
        label: getPreferredChainLabel(chainInput, chainId),
      };
    });
  }

  if (options.rpcUrl) {
    const { chainId, chainInput } = await getProviderAndChain(options);
    return [{
      chainId,
      requested: chainInput,
      label: getPreferredChainLabel(chainInput, chainId),
    }];
  }

  const singleChainInput = options.chainId ?? options.chain;
  const chainId = normalizeChainId(singleChainInput);
  if (!chainId) {
    throw new Error('Missing required --chain, --chain-id, --chains, or --rpc-url');
  }

  return [{
    chainId,
    requested: singleChainInput,
    label: getPreferredChainLabel(singleChainInput, chainId),
  }];
}

function buildMarketUrls({ chainInput, chainId, dapiName }) {
  const chainSlug = getMarketChainSlug(chainInput, chainId);
  const dapiSlug = slugifyDapiName(dapiName);
  const basePath = `${MARKET_BASE_URL}/${chainSlug}/${dapiSlug}`;

  return {
    chainSlug,
    dapiSlug,
    marketBaseUrl: MARKET_BASE_URL,
    marketListUrl: `${MARKET_BASE_URL}/dapis?chains=${encodeURIComponent(chainSlug)}`,
    marketSearchUrl: `${MARKET_BASE_URL}/dapis?chains=${encodeURIComponent(chainSlug)}&search=${encodeURIComponent(
      dapiName
    )}`,
    marketPageUrl: basePath,
    activationUrl: `${basePath}/activate?default=1`,
    integrationUrl: basePath,
  };
}

function buildPricingFileUrl(chainId, dapiName) {
  const pricingSlug = String(dapiName || '')
    .trim()
    .replace(/\//g, '-')
    .replace(/\s+/g, ' ');

  return `${MARKET_PRICING_BASE_URL}/${chainId}/${pricingSlug}.json`;
}
function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function extractLiveDapiManagementMerkleTreeDataFromBundleSource(bundleSource) {
  const objectMatch = bundleSource.match(/\{timestamp:([A-Za-z_$][\w$]*),hash:([A-Za-z_$][\w$]*),signatures:([A-Za-z_$][\w$]*),merkleTreeValues:([A-Za-z_$][\w$]*)\}/);
  if (!objectMatch) {
    throw new Error('Could not locate dAPI management Merkle tree metadata in the Api3 Market bundle.');
  }

  const [, timestampVariable, hashVariable, signaturesVariable, merkleTreeValuesVariable] = objectMatch;
  const timestampMatch = bundleSource.match(new RegExp(String.raw`(?:^|[,;\n])${escapeRegExp(timestampVariable)}=(\d{10,})`));
  const hashMatch = bundleSource.match(new RegExp(String.raw`(?:^|[,;\n])${escapeRegExp(hashVariable)}=("0x[0-9a-fA-F]{64}")`));
  const merkleTreeValuesMatch = bundleSource.match(new RegExp(`${escapeRegExp(merkleTreeValuesVariable)}=JSON\\.parse\\('([\\s\\S]*?)'\\)`));

  if (!timestampMatch || !hashMatch || !merkleTreeValuesMatch) {
    throw new Error('Could not resolve the dAPI management Merkle tree variables from the Api3 Market bundle.');
  }

  const signaturesStart = bundleSource.indexOf(`${signaturesVariable}=`);
  const merkleTreeValuesStart = bundleSource.indexOf(`,${merkleTreeValuesVariable}=`, signaturesStart);
  if (signaturesStart === -1 || merkleTreeValuesStart === -1) {
    throw new Error('Could not isolate the dAPI management signature map in the Api3 Market bundle.');
  }

  const signaturesSource = bundleSource.slice(signaturesStart + signaturesVariable.length + 1, merkleTreeValuesStart);

  return {
    timestamp: Number(timestampMatch[1]),
    hash: JSON.parse(hashMatch[1]),
    signatures: JSON.parse(signaturesSource),
    merkleTreeValues: JSON.parse(merkleTreeValuesMatch[1]),
  };
}

async function fetchCurrentMarketBundleUrl() {
  const response = await fetch(`${MARKET_BASE_URL}/`);
  if (!response.ok) {
    throw new Error(`Failed to fetch Api3 Market homepage: HTTP ${response.status}`);
  }

  const html = await response.text();
  const bundleMatch = html.match(/\/assets\/index-[^"'\s>]+\.js/);
  if (!bundleMatch) {
    throw new Error('Could not locate the current Api3 Market frontend bundle URL.');
  }

  return new URL(bundleMatch[0], `${MARKET_BASE_URL}/`).toString();
}

async function fetchLiveDapiManagementMerkleTreeData() {
  if (!liveDapiManagementMerkleTreeDataPromise) {
    liveDapiManagementMerkleTreeDataPromise = (async () => {
      const bundleUrl = await fetchCurrentMarketBundleUrl();
      const bundleResponse = await fetch(bundleUrl);
      if (!bundleResponse.ok) {
        throw new Error(`Failed to fetch Api3 Market bundle: HTTP ${bundleResponse.status}`);
      }

      const bundleSource = await bundleResponse.text();
      return {
        ...extractLiveDapiManagementMerkleTreeDataFromBundleSource(bundleSource),
        bundleUrl,
      };
    })().catch((error) => {
      liveDapiManagementMerkleTreeDataPromise = null;
      throw error;
    });
  }

  return liveDapiManagementMerkleTreeDataPromise;
}

function selectPreferredDapiManagementMerkleTreeData({ localTreeData, liveTreeData, onChainRegisteredRoots }) {
  const onChainRoot = onChainRegisteredRoots?.dapiManagementMerkleRoot || null;

  if (!onChainRoot) {
    return {
      treeData: localTreeData,
      selectedSource: 'local-package',
      reason: 'On-chain dAPI management Merkle root is unavailable, so the local package snapshot remains the only source.',
    };
  }

  if (localTreeData?.hash === onChainRoot) {
    return {
      treeData: localTreeData,
      selectedSource: 'local-package',
      reason: 'The local @api3/dapi-management snapshot already matches the on-chain dAPI management Merkle root.',
    };
  }

  if (liveTreeData?.hash === onChainRoot) {
    return {
      treeData: liveTreeData,
      selectedSource: 'live-market-bundle',
      reason: 'The live Api3 Market bundle contains a newer dAPI management Merkle tree that matches the on-chain root.',
    };
  }

  return {
    treeData: localTreeData,
    selectedSource: 'local-package',
    reason: 'Neither the local package snapshot nor the fetched live Market bundle matched the on-chain dAPI management Merkle root.',
  };
}

function ppmToPercentString(ppm) {
  const percent = Number(ppm) / 1000000;
  return Number.isFinite(percent) ? String(percent) : null;
}

async function fetchJsonWithStatus(url) {
  const response = await fetch(url);
  const text = await response.text();
  let json = null;

  if (text) {
    try {
      json = JSON.parse(text);
    } catch {
      json = null;
    }
  }

  return {
    ok: response.ok,
    status: response.status,
    url,
    json,
    bodySnippet: text ? text.slice(0, 500) : '',
  };
}

async function fetchSignedApiSnapshot({ signedApiUrl, airnode, providerAlias }) {
  if (!signedApiUrl) {
    throw new Error(`No Signed API URL is configured for provider ${providerAlias || airnode}.`);
  }

  const response = await fetchJsonWithStatus(`${signedApiUrl}/public/${airnode}`);
  if (!response.ok || !response.json?.data) {
    throw new Error(`Signed API fetch failed for ${providerAlias || airnode}: HTTP ${response.status}`);
  }

  return response.json;
}

async function fetchCurrentSignedBeaconData({ beaconMetadata }) {
  const signedApiSnapshotByAirnode = new Map();

  return Promise.all(beaconMetadata.map(async (beacon) => {
    const signedApiUrl = api3ApiIntegrations.getApiUrls(beacon.airnode).signedApiUrl;
    let signedApiSnapshot = signedApiSnapshotByAirnode.get(beacon.airnode);

    if (!signedApiSnapshot) {
      signedApiSnapshot = await fetchSignedApiSnapshot({
        signedApiUrl,
        airnode: beacon.airnode,
        providerAlias: beacon.providerAlias,
      });
      signedApiSnapshotByAirnode.set(beacon.airnode, signedApiSnapshot);
    }

    const signedBeaconData = signedApiSnapshot.data?.[beacon.beaconId];
    if (!signedBeaconData) {
      throw new Error(`Signed API payload missing for provider ${beacon.providerAlias} beacon ${beacon.beaconId}.`);
    }

    return {
      providerAlias: beacon.providerAlias,
      airnode: beacon.airnode,
      templateId: beacon.templateId,
      beaconId: beacon.beaconId,
      signedApiUrl,
      timestamp: signedBeaconData.timestamp,
      encodedValue: signedBeaconData.encodedValue,
      signature: signedBeaconData.signature,
    };
  }));
}

function buildWrapperReadyingPlan({ currentPublicDataFeedModel, signedBeaconUpdates }) {
  const marketInterface = Api3MarketV2__factory.createInterface();
  const tryMulticallData = [];
  const steps = [];

  const registerDataFeedCalldata = marketInterface.encodeFunctionData('registerDataFeed', [
    currentPublicDataFeedModel.dataFeedDetails,
  ]);
  tryMulticallData.push(registerDataFeedCalldata);
  steps.push({
    step: 1,
    functionName: 'registerDataFeed',
    purpose: 'Register the current public data-feed composition before attempting the wrapped purchase.',
    calldata: registerDataFeedCalldata,
    arguments: {
      dataFeedDetails: currentPublicDataFeedModel.dataFeedDetails,
    },
  });

  signedBeaconUpdates.forEach((signedBeaconUpdate, index) => {
    const calldata = marketInterface.encodeFunctionData('updateBeaconWithSignedData', [
      signedBeaconUpdate.airnode,
      signedBeaconUpdate.templateId,
      signedBeaconUpdate.timestamp,
      signedBeaconUpdate.encodedValue,
      signedBeaconUpdate.signature,
    ]);
    tryMulticallData.push(calldata);
    steps.push({
      step: index + 2,
      functionName: 'updateBeaconWithSignedData',
      purpose: `Refresh the ${signedBeaconUpdate.providerAlias} beacon with live Signed API payloads.`,
      calldata,
      arguments: {
        airnode: signedBeaconUpdate.airnode,
        templateId: signedBeaconUpdate.templateId,
        timestamp: signedBeaconUpdate.timestamp,
        encodedValue: signedBeaconUpdate.encodedValue,
        signature: signedBeaconUpdate.signature,
      },
      signedApiUrl: signedBeaconUpdate.signedApiUrl,
      beaconId: signedBeaconUpdate.beaconId,
      providerAlias: signedBeaconUpdate.providerAlias,
    });
  });

  const beaconIds = currentPublicDataFeedModel.beaconMetadata.map((entry) => entry.beaconId);
  const updateBeaconSetCalldata = marketInterface.encodeFunctionData('updateBeaconSetWithBeacons', [beaconIds]);
  tryMulticallData.push(updateBeaconSetCalldata);
  steps.push({
    step: steps.length + 1,
    functionName: 'updateBeaconSetWithBeacons',
    purpose: 'Refresh the aggregate data feed from the freshly updated beacon set before buying the subscription.',
    calldata: updateBeaconSetCalldata,
    arguments: { beaconIds },
  });

  return {
    activationPath: 'register-data-feed-update-beacons-and-wrap-buy-subscription',
    tryMulticallData,
    readyingPlan: {
      callCount: tryMulticallData.length,
      steps,
    },
    signedBeaconUpdates,
  };
}

function decodePricingLeaf(leaf) {
  const [dapiNameBytes32, chainId, updateParameters, duration, price] = leaf.value;
  const decodedUpdateParameters = decodeUpdateParameters(updateParameters);

  return {
    dapiNameBytes32,
    chainId: Number(chainId),
    updateParameters,
    decodedUpdateParameters: {
      ...decodedUpdateParameters,
      deviationThresholdPercent: ppmToPercentString(decodedUpdateParameters.deviationThresholdPpm),
    },
    duration: String(duration),
    durationDays: Number(duration) / (24 * 60 * 60),
    price: String(price),
    proof: Array.isArray(leaf.proof) ? leaf.proof : [],
  };
}

function compareHex(a, b) {
  const normalizedA = String(a || '').toLowerCase();
  const normalizedB = String(b || '').toLowerCase();

  if (normalizedA < normalizedB) {
    return -1;
  }
  if (normalizedA > normalizedB) {
    return 1;
  }
  return 0;
}

function standardLeafHash(types, values) {
  return keccak256(keccak256(ABI_CODER.encode(types, values)));
}

function standardNodeHash(left, right) {
  const [first, second] = [left, right].sort(compareHex);
  return keccak256(`${first}${second.slice(2)}`);
}

function buildStandardMerkleTree(values, types) {
  if (!Array.isArray(values) || values.length === 0) {
    return null;
  }

  const hashedValues = values
    .map((value, originalIndex) => ({
      value,
      originalIndex,
      hash: standardLeafHash(types, value),
    }))
    .sort((a, b) => compareHex(a.hash, b.hash));

  const tree = new Array(2 * hashedValues.length - 1);
  for (const [leafIndex, entry] of hashedValues.entries()) {
    tree[tree.length - 1 - leafIndex] = entry.hash;
  }
  for (let index = tree.length - 1 - hashedValues.length; index >= 0; index -= 1) {
    tree[index] = standardNodeHash(tree[2 * index + 1], tree[2 * index + 2]);
  }

  const originalIndexToTreeIndex = new Map();
  for (const [leafIndex, entry] of hashedValues.entries()) {
    originalIndexToTreeIndex.set(entry.originalIndex, tree.length - 1 - leafIndex);
  }

  return {
    root: tree[0],
    tree,
    hashedValues,
    originalIndexToTreeIndex,
  };
}

function getMerkleProof(tree, treeIndex) {
  const proof = [];
  const path = [];
  let index = treeIndex;

  while (index > 0) {
    const siblingIndex = index % 2 === 0 ? index - 1 : index + 1;
    proof.push(tree[siblingIndex]);
    path.push({
      treeIndex: index,
      siblingTreeIndex: siblingIndex,
      siblingHash: tree[siblingIndex],
    });
    index = Math.floor((index - 1) / 2);
  }

  return { proof, path };
}

function processMerkleProof(leafHash, proof) {
  return proof.reduce((hash, siblingHash) => standardNodeHash(hash, siblingHash), leafHash);
}

function selectPricingOption(options, pricingOptions) {
  const requestedDuration = options.duration ? String(options.duration) : null;
  const requestedDurationDays = options.durationDays ? String(options.durationDays) : null;
  const requestedDeviation = options.deviationChoice
    || options.deviationPercent
    || options.deviation;
  const preferredDeviation = requestedDeviation || DEFAULT_DEVIATION_CHOICE_PERCENT;

  return (
    pricingOptions.find((entry) => {
      const durationMatches = requestedDuration
        ? entry.duration === requestedDuration
        : requestedDurationDays
          ? String(entry.durationDays) === requestedDurationDays
          : true;
      const deviationMatches = entry.decodedUpdateParameters.deviationThresholdPercent === String(preferredDeviation);

      return durationMatches && deviationMatches;
    })
    || pricingOptions.find((entry) => {
      const durationMatches = requestedDuration
        ? entry.duration === requestedDuration
        : requestedDurationDays
          ? String(entry.durationDays) === requestedDurationDays
          : true;

      return durationMatches;
    })
    || pricingOptions.find(
      (entry) => entry.decodedUpdateParameters.deviationThresholdPercent === DEFAULT_DEVIATION_CHOICE_PERCENT,
    )
    || pricingOptions[0]
    || null
  );
}

function compareQueuePriority(a, b) {
  const deviationA = Number(a?.decodedUpdateParameters?.deviationThresholdPercent);
  const deviationB = Number(b?.decodedUpdateParameters?.deviationThresholdPercent);

  if (Number.isFinite(deviationA) && Number.isFinite(deviationB) && deviationA !== deviationB) {
    return deviationA - deviationB;
  }

  const durationA = Number(a?.duration);
  const durationB = Number(b?.duration);
  if (Number.isFinite(durationA) && Number.isFinite(durationB) && durationA !== durationB) {
    return durationA - durationB;
  }

  return String(a?.price || '').localeCompare(String(b?.price || ''));
}

function buildQueueSubscriptionChoices({ pricingOptions, chosenSubscriptionOption, sponsorWallet }) {
  const sortedOptions = [...pricingOptions].sort(compareQueuePriority);

  return {
    queueModel: 'single-feed-single-sponsor-wallet',
    sponsorWallet,
    summary:
      'All subscription tiers are queue entries for the same feed and sponsor wallet. Smaller deviation thresholds get queue priority.',
    queuePriorityRule: 'Smaller deviation thresholds are prioritized first within the feed subscription queue.',
    queueEntries: sortedOptions.map((entry, index) => ({
      queuePriority: index + 1,
      selected:
        Boolean(chosenSubscriptionOption)
        && entry.duration === chosenSubscriptionOption.duration
        && entry.updateParameters === chosenSubscriptionOption.updateParameters
        && entry.price === chosenSubscriptionOption.price,
      deviationThresholdPercent: entry.decodedUpdateParameters.deviationThresholdPercent,
      heartbeatInterval: entry.decodedUpdateParameters.heartbeatInterval,
      timeout: entry.decodedUpdateParameters.timeout,
      duration: entry.duration,
      durationDays: entry.durationDays,
      price: entry.price,
      updateParameters: entry.updateParameters,
    })),
  };
}

function getDapiManagementEntry(dapiNameBytes32, managementMerkleTreeData = dapiManagementMerkleTreeData) {
  const entryIndex = managementMerkleTreeData.merkleTreeValues.findIndex((leaf) => leaf[0] === dapiNameBytes32);
  if (entryIndex === -1) {
    return null;
  }

  const value = managementMerkleTreeData.merkleTreeValues[entryIndex];
  const merkleTree = buildStandardMerkleTree(managementMerkleTreeData.merkleTreeValues, ['bytes32', 'bytes32', 'address']);
  const treeIndex = merkleTree?.originalIndexToTreeIndex.get(entryIndex);
  const proofData = treeIndex !== undefined && merkleTree ? getMerkleProof(merkleTree.tree, treeIndex) : null;
  const leafHash = standardLeafHash(['bytes32', 'bytes32', 'address'], value);
  const computedRoot = proofData ? processMerkleProof(leafHash, proofData.proof) : null;

  return {
    entryIndex,
    dapiNameBytes32: value[0],
    dataFeedId: value[1],
    sponsorWallet: value[2],
    leaf: value,
    leafHash,
    merkleRoot: merkleTree?.root || null,
    proof: proofData?.proof || null,
    proofPath: proofData?.path || null,
    proofMatchesMerkleRoot: proofData ? computedRoot === managementMerkleTreeData.hash : false,
  };
}

function buildMarketExecutionPlan({ chainInput, chainId, dapiName, classification, chainState }) {
  const market = buildMarketUrls({ chainInput, chainId, dapiName });
  const isActive = Boolean(chainState?.isActiveOnChain);
  const communalProxy = chainState?.communalProxy || computeCommunalApi3ReaderProxyV1Address(chainId, dapiName);

  return {
    status: classification,
    chain: {
      chainId,
      requested: chainInput || null,
      marketChainSlug: market.chainSlug,
    },
    dapiName,
    slug: market.dapiSlug,
    communalProxy,
    market,
    executionSurface: 'market.api3.org',
    walletInteractionRequired: !isActive,
    userApprovalExpected: !isActive,
    automatedTransactionExecution: false,
    recommendedAction: isActive ? 'integrate-existing-feed' : 'open-market-and-activate-feed',
    orderedSteps: isActive
      ? [
          {
            step: 1,
            intent: 'Open the Market feed page to confirm the feed and inspect integration details.',
            action: 'open-url',
            url: market.marketPageUrl,
          },
          {
            step: 2,
            intent: 'Use the integration page or the communal proxy directly. No purchase flow is needed.',
            action: 'open-url',
            url: market.integrationUrl,
          },
          {
            step: 3,
            intent: 'Read from the communal proxy on-chain to verify the feed remains operational.',
            action: 'verify-onchain',
            target: communalProxy,
            method: 'Api3ReaderProxyV1.read()',
          },
        ]
      : [
          {
            step: 1,
            intent: 'Open the activation URL in Api3 Market for this chain and dAPI.',
            action: 'open-url',
            url: market.activationUrl,
          },
          {
            step: 2,
            intent: 'Confirm the page is the correct chain and dAPI, then review activation pricing and terms.',
            action: 'confirm-page-context',
            url: market.marketPageUrl,
          },
          {
            step: 3,
            intent: 'Connect a wallet in the Market UI if the page requires it before purchase.',
            action: 'connect-wallet-if-needed',
            requiresWalletInteraction: true,
          },
          {
            step: 4,
            intent: 'Proceed through the Market purchase or activation flow until the wallet confirmation step is shown.',
            action: 'navigate-to-purchase-flow',
            requiresWalletInteraction: true,
          },
          {
            step: 5,
            intent: 'Pause for user wallet review, approval, and signature. Do not claim this is automated unless a browser or wallet tool actually handles it.',
            action: 'await-user-wallet-approval',
            requiresUserApproval: true,
          },
          {
            step: 6,
            intent: 'After completion, re-run ensure-active or resolve to confirm the feed is now operational.',
            action: 'recheck-feed-status',
            verificationCommand: 'ensure-active',
          },
        ],
  };
}

function buildBrowserPlan({ chainInput, chainId, dapiName, chainState }) {
  const market = buildMarketUrls({ chainInput, chainId, dapiName });
  const isActive = Boolean(chainState?.isActiveOnChain);
  const communalProxy = chainState?.communalProxy || computeCommunalApi3ReaderProxyV1Address(chainId, dapiName);

  const header = {
    schema: 'openclaw-browser-plan/v1',
    automatedTransactionExecution: false,
    walletSigningAutomated: false,
    executionSurface: 'market.api3.org',
    dapiName,
    chainId,
    chainSlug: market.chainSlug,
    communalProxy,
    isActive,
  };

  if (isActive) {
    return {
      ...header,
      planType: 'integrate-existing-feed',
      steps: [
        {
          step: 1,
          driverAction: 'navigate',
          url: market.marketPageUrl,
          pauseForUser: false,
          waitFor: { type: 'url-contains', value: market.dapiSlug },
          intent: 'Navigate to the Market feed page to confirm correct chain and feed.',
        },
        {
          step: 2,
          driverAction: 'assert-text',
          contains: dapiName,
          pauseForUser: false,
          intent: 'Verify the page displays the expected feed name.',
        },
        {
          step: 3,
          driverAction: 'extract-integration-details',
          url: market.integrationUrl,
          communalProxy,
          pauseForUser: false,
          intent: 'Collect the proxy address and ABI for integration. No purchase flow needed.',
        },
        {
          step: 4,
          driverAction: 'verify-onchain',
          target: communalProxy,
          method: 'Api3ReaderProxyV1.read()',
          pauseForUser: false,
          intent: 'Confirm the communal proxy returns a live value before integrating.',
        },
      ],
    };
  }

  return {
    ...header,
    planType: 'activate-and-fund-feed',
    steps: [
      {
        step: 1,
        driverAction: 'navigate',
        url: market.activationUrl,
        pauseForUser: false,
        waitFor: { type: 'url-contains', value: market.dapiSlug },
        intent: 'Open the Market activation page for this chain and dAPI.',
      },
      {
        step: 2,
        driverAction: 'assert-page-context',
        expectedChain: market.chainSlug,
        expectedFeed: dapiName,
        pauseForUser: false,
        intent: 'Confirm the page is for the correct chain and feed before continuing.',
      },
      {
        step: 3,
        driverAction: 'connect-wallet',
        pauseForUser: true,
        pauseReason: 'User must select and connect a wallet via the Market UI. Cannot be automated by the driver.',
        requiresUserAction: true,
        intent: 'Connect a wallet in the Market UI if the page prompts for it.',
      },
      {
        step: 4,
        driverAction: 'click-activate-or-fund',
        pauseForUser: false,
        waitFor: {
          type: 'any-selector',
          values: ['[data-action="activate"]', '[data-action="fund"]', '.purchase-flow'],
        },
        intent: 'Click the activation or fund button to enter the purchase flow.',
        note: 'Selector hints are best-effort; update if the Market UI changes.',
      },
      {
        step: 5,
        driverAction: 'await-user-wallet-approval',
        pauseForUser: true,
        pauseReason:
          'User must review, approve, and sign the transaction in their wallet. This step cannot be automated.',
        requiresUserAction: true,
        automatedTransactionExecution: false,
        intent: 'Hold until the user approves the wallet transaction. Do not proceed until approval is confirmed.',
      },
      {
        step: 6,
        driverAction: 'recheck-feed-status',
        command: 'ensure-active',
        commandArgs: { '--dapi-name': dapiName, '--chain': chainInput || String(chainId) },
        pauseForUser: false,
        intent: 'Re-run ensure-active to confirm the feed is now live on-chain after activation.',
      },
    ],
  };
}

function isTestnetChain(chainCatalogEntry) {
  return String(chainCatalogEntry?.stage || '').toLowerCase() === 'testnet';
}

function getLikelySubscriptionDurationDays(chainCatalogEntry) {
  return isTestnetChain(chainCatalogEntry)
    ? TESTNET_SUBSCRIPTION_DURATION_DAYS
    : MAINNET_SUBSCRIPTION_DURATION_DAYS;
}

function classifyMarketActivationCoverage({ dapiName, pricingResponse, pricingOptions, chosenSubscriptionOption, dapiManagementEntry }) {
  const pricingFileMissing = !pricingResponse.ok;
  const pricingLeavesMissing = pricingResponse.ok && pricingOptions.length === 0;
  const requestedPricingOptionMissing = pricingOptions.length > 0 && !chosenSubscriptionOption;
  const dapiManagementEntryMissing = !dapiManagementEntry;
  const dapiManagementEntryZeroed = dapiManagementEntry?.dataFeedId === ZERO_BYTES32;
  const lifecycleStage = String(getCatalogDapiEntry(dapiName)?.stage || 'unknown').toLowerCase();

  if (lifecycleStage === 'retired') {
    return {
      code: 'retired-delisted',
      label: 'feed appears retired/delisted and is not intended for activation',
      activatableViaMarketContractPath: false,
      blockerCategory: 'retired-delisted',
      lifecycleStage,
    };
  }

  if (pricingFileMissing || pricingLeavesMissing) {
    return {
      code: 'missing-market-pricing-coverage',
      label: 'feed discoverable but missing queue subscription coverage in Market pricing data',
      activatableViaMarketContractPath: false,
      blockerCategory: 'missing-queue-coverage',
      lifecycleStage,
    };
  }

  if (dapiManagementEntryMissing || dapiManagementEntryZeroed) {
    return {
      code: 'zeroed-or-missing-dapi-management-entry',
      label: 'feed present in catalog but missing live feed-level management entry',
      activatableViaMarketContractPath: false,
      blockerCategory: dapiManagementEntryMissing ? 'missing-feed-management-entry' : 'zeroed-feed-management-entry',
      lifecycleStage,
    };
  }

  if (requestedPricingOptionMissing) {
    return {
      code: 'market-covered-but-requested-tier-unavailable',
      label: 'feed has queue coverage, but the requested queue entry is unavailable',
      activatableViaMarketContractPath: false,
      blockerCategory: 'requested-queue-entry-unavailable',
      lifecycleStage,
    };
  }

  return {
    code: 'market-contract-path-available',
    label: 'feed fully activatable via Market contract path',
    activatableViaMarketContractPath: true,
    blockerCategory: null,
    lifecycleStage,
  };
}

function buildWrapperCallDiagnostics({ chainState, exactMerkleDataBundle, marketActivationCoverage, dapiManagementEntry, chosenSubscriptionOption, currentPublicDataFeedModel }) {
  const isActiveOnChain = Boolean(chainState?.isActiveOnChain);

  if (!exactMerkleDataBundle || !dapiManagementEntry || !chosenSubscriptionOption) {
    return {
      wrapperCallSupported: false,
      wrapperCallPreparationSupported: false,
      reason: 'Wrapper preparation is blocked because the exact Market purchase prerequisites are incomplete.',
      blockers: ['buySubscription arguments are incomplete, so the wrapper call cannot be prepared either.'],
      exactTryMulticallDataDerivable: false,
      tryMulticallData: null,
      currentPublicDataFeedModel: currentPublicDataFeedModel || null,
    };
  }

  if (isActiveOnChain) {
    return {
      wrapperCallSupported: true,
      wrapperCallPreparationSupported: true,
      reason: 'The feed is already active on-chain, so the wrapper can be prepared exactly with an empty tryMulticallData array.',
      blockers: [],
      exactTryMulticallDataDerivable: true,
      tryMulticallData: [],
      activationPath: 'already-active-no-prep-calls-needed',
      currentPublicDataFeedModel: currentPublicDataFeedModel || null,
    };
  }

  if (!marketActivationCoverage?.activatableViaMarketContractPath) {
    return {
      wrapperCallSupported: false,
      wrapperCallPreparationSupported: false,
      reason: 'Wrapper preparation is not the blocker here. The feed lacks the upstream Market coverage needed for activation.',
      blockers: [`coverage classification: ${marketActivationCoverage?.label || 'unknown'}`],
      exactTryMulticallDataDerivable: false,
      tryMulticallData: null,
      activationPath: 'blocked-by-market-coverage',
      currentPublicDataFeedModel: currentPublicDataFeedModel || null,
    };
  }

  if (currentPublicDataFeedModel?.derivable === false) {
    return {
      wrapperCallSupported: false,
      wrapperCallPreparationSupported: false,
      reason: 'The current public provider metadata for this feed is incomplete, so the wrapper readying path cannot be reconstructed exactly.',
      blockers: [
        `Current public provider metadata derivation failed: ${currentPublicDataFeedModel.failureReason || 'unknown reason'}`,
        'Without a derivable current public data-feed model, the repo cannot safely build updateDapiName/registerDataFeed/updateBeacon* pre-calls.',
      ],
      exactTryMulticallDataDerivable: false,
      tryMulticallData: null,
      activationPath: 'current-public-data-feed-model-underdetermined',
      currentPublicDataFeedModel,
    };
  }

  if (currentPublicDataFeedModel?.derivable && currentPublicDataFeedModel.dataFeedId !== dapiManagementEntry.dataFeedId) {
    return {
      wrapperCallSupported: false,
      wrapperCallPreparationSupported: false,
      reason: 'The live dAPI-management leaf points to a different dataFeedId than the one derivable from the current public provider catalog, so the exact wrapper readying sequence is still underdetermined.',
      blockers: [
        `dAPI management leaf dataFeedId: ${dapiManagementEntry.dataFeedId}`,
        `Current public provider catalog derives dataFeedId: ${currentPublicDataFeedModel.dataFeedId}`,
        'This means the current public provider list does not reconstruct the exact feed that buySubscription expects, even though fresher signed data exists for the current catalog-backed feed.',
        'Without the exact historical/legacy provider composition for the leaf dataFeedId, the repo cannot safely fabricate the updateDapiName/registerDataFeed/updateBeacon* pre-calls for the wrapper path.',
      ],
      exactTryMulticallDataDerivable: false,
      tryMulticallData: null,
      activationPath: 'leaf-data-feed-id-differs-from-current-public-provider-catalog',
      currentPublicDataFeedModel,
    };
  }

  return {
    wrapperCallSupported: false,
    wrapperCallPreparationSupported: false,
    reason:
      'The wrapper function signature is known, but the exact tryMulticallData payload is not safely derivable from the public/frontend inputs available in this project for an inactive feed.',
    blockers: [
      'Inactive feeds may need pre-purchase readying calls such as updateDapiName, updateSignedApiUrl, updateBeaconWithSignedData, or updateBeaconSetWithBeacons.',
      'Those readying calls need exact signed payloads, signed API URL Merkle proofs, or fresh off-chain beacon signatures that are not exposed by @api3/dapi-management or the current public pricing files used here.',
      'Claiming a wrapper payload without those exact bytes would be guesswork, so this tool refuses to fabricate it.',
    ],
    exactTryMulticallDataDerivable: false,
    tryMulticallData: null,
    activationPath: 'inactive-feed-needs-underdetermined-readying-calls',
    currentPublicDataFeedModel: currentPublicDataFeedModel || null,
  };
}

function buildUnsupportedPurchaseDiagnostics({ dapiName, pricingResponse, pricingFileUrl, pricingOptions, chosenSubscriptionOption, dapiManagementEntry, chainState }) {
  const pricingFileMissing = !pricingResponse.ok;
  const pricingLeavesMissing = pricingResponse.ok && pricingOptions.length === 0;
  const requestedPricingOptionMissing = pricingOptions.length > 0 && !chosenSubscriptionOption;
  const dapiManagementEntryMissing = !dapiManagementEntry;
  const dapiManagementEntryZeroed = dapiManagementEntry?.dataFeedId === ZERO_BYTES32;
  const marketActivationCoverage = classifyMarketActivationCoverage({
    dapiName,
    pricingResponse,
    pricingOptions,
    chosenSubscriptionOption,
    dapiManagementEntry,
  });

  const missingPrerequisites = [];
  if (pricingFileMissing) {
    missingPrerequisites.push(`pricing file missing: ${pricingFileUrl} (HTTP ${pricingResponse.status})`);
  }
  if (pricingLeavesMissing) {
    missingPrerequisites.push('pricing file contained zero pricing leaves');
  }
  if (requestedPricingOptionMissing) {
    missingPrerequisites.push('no pricing leaf matched the requested duration/deviation filters');
  }
  if (dapiManagementEntryMissing) {
    missingPrerequisites.push('dAPI management entry missing from @api3/dapi-management');
  }
  if (dapiManagementEntryZeroed) {
    missingPrerequisites.push('dAPI management entry is zeroed, so there is no live dataFeedId purchase target');
  }
  if (marketActivationCoverage.code === 'retired-delisted') {
    missingPrerequisites.push('feed is marked retired/delisted and is not intended to be activated');
  }

  return {
    marketActivationCoverage,
    queueCoverageDiagnostics: {
      pricingFileMissing,
      pricingFileStatus: pricingResponse.status,
      pricingLeavesMissing,
      requestedQueueEntryMissing: requestedPricingOptionMissing,
      availableQueueEntries: pricingOptions.length,
      blockerCategory: marketActivationCoverage.blockerCategory,
    },
    feedManagementDiagnostics: {
      dapiManagementEntryMissing,
      dapiManagementEntryZeroed,
      hasLiveFeedManagementEntry: !dapiManagementEntryMissing && !dapiManagementEntryZeroed,
    },
    pricingFileMissing,
    pricingFileStatus: pricingResponse.status,
    pricingLeavesMissing,
    requestedPricingOptionMissing,
    dapiManagementEntryMissing,
    dapiManagementEntryZeroed,
    chainState: {
      isActiveOnChain: Boolean(chainState?.isActiveOnChain),
      dataFeedId: chainState?.dataFeedId || null,
    },
    missingPrerequisites,
  };
}

function classifyFundingExecution({ chainState, exactTransactionExecutionSupported, wrapperCallDiagnostics, unsupportedDiagnostics }) {
  const availableExecutionModes = [];

  if (exactTransactionExecutionSupported) {
    availableExecutionModes.push('direct');
  }

  if (wrapperCallDiagnostics && wrapperCallDiagnostics.wrapperCallPreparationSupported) {
    availableExecutionModes.push('wrapper');
  }

  if (chainState && chainState.isActiveOnChain) {
    return {
      state: 'not-needed',
      reason: 'Feed is already active onchain, so no funding execution is required.',
      availableExecutionModes,
    };
  }

  if (availableExecutionModes.length > 0) {
    return {
      state: 'executable',
      reason: 'The repo can already derive an exact executable funding call for this feed.',
      availableExecutionModes,
    };
  }

  if (unsupportedDiagnostics && unsupportedDiagnostics.marketActivationCoverage && unsupportedDiagnostics.marketActivationCoverage.activatableViaMarketContractPath) {
    return {
      state: 'browser-assisted',
      reason: 'Funding appears possible through the Market activation path, but this repo cannot yet derive an exact executable call for it.',
      availableExecutionModes,
    };
  }

  return {
    state: 'unsupported',
    reason: 'No supported executable or browser-assisted funding path is currently available for this feed.',
    availableExecutionModes,
  };
}

function parseBooleanOption(value, defaultValue = false) {
  if (value === undefined) {
    return defaultValue;
  }

  if (typeof value === 'boolean') {
    return value;
  }

  const normalized = String(value).trim().toLowerCase();
  if (['1', 'true', 'yes', 'y', 'on'].includes(normalized)) {
    return true;
  }
  if (['0', 'false', 'no', 'n', 'off'].includes(normalized)) {
    return false;
  }

  throw new Error(`Could not parse boolean option from: ${value}`);
}

function normalizeTransactionValue(value) {
  if (typeof value === 'bigint') {
    return value;
  }

  if (typeof value === 'number' && Number.isInteger(value) && value >= 0) {
    return BigInt(value);
  }

  if (typeof value === 'string' && /^0x[0-9a-fA-F]+$/.test(value)) {
    return BigInt(value);
  }

  if (typeof value === 'string' && /^[0-9]+$/.test(value)) {
    return BigInt(value);
  }

  throw new Error(`Unsupported transaction value: ${value}`);
}

function describeExecutionError(error) {
  const candidates = [
    error?.info?.error?.message,
    error?.error?.message,
    error?.shortMessage,
    error?.reason,
    error?.message,
  ];

  for (const candidate of candidates) {
    if (typeof candidate === 'string' && candidate.trim()) {
      return candidate.replace(/^err:\s*/i, '').trim();
    }
  }

  return String(error);
}

async function simulatePreparedContractCallSupport({ provider, preparedContractCall }) {
  if (!preparedContractCall?.targetContractAddress || !preparedContractCall?.calldata) {
    return {
      attempted: false,
      supported: false,
      failureReason: 'Prepared contract call data is incomplete.',
    };
  }

  try {
    await provider.call({
      to: preparedContractCall.targetContractAddress,
      data: preparedContractCall.calldata,
      value: normalizeTransactionValue(preparedContractCall.value || 0n),
      from: '0x000000000000000000000000000000000000dEaD',
    });
    return {
      attempted: true,
      supported: true,
      failureReason: null,
    };
  } catch (error) {
    return {
      attempted: true,
      supported: false,
      failureReason: describeExecutionError(error),
    };
  }
}

async function executePreparedContractCall({ preparedContractCall, rpcUrl, privateKey, submit, acknowledgement, simulationFromAddress }) {
  const executionSummary = {
    requested: true,
    dryRun: !submit,
    attempted: false,
    simulated: false,
    submitted: false,
    completed: false,
    signerAddress: null,
    simulationFromAddress: null,
    txHash: null,
    failureReason: null,
  };

  if (!preparedContractCall || preparedContractCall.sendTransactionSupported === false) {
    executionSummary.failureReason = 'Prepared contract call is unavailable or unsupported for sending.';
    return { executionSummary, transactionRequest: null, callResult: null };
  }

  if (!rpcUrl || !privateKey) {
    executionSummary.failureReason = 'Execution requires rpcUrl and privateKey.';
    return { executionSummary, transactionRequest: null, callResult: null };
  }

  if (submit && acknowledgement !== SEND_ACKNOWLEDGEMENT) {
    executionSummary.failureReason = `Submitting requires acknowledgement=${SEND_ACKNOWLEDGEMENT}.`;
    return { executionSummary, transactionRequest: null, callResult: null };
  }

  const provider = new JsonRpcProvider(rpcUrl);
  const wallet = new Wallet(privateKey, provider);
  const signerAddress = await wallet.getAddress();
  executionSummary.signerAddress = signerAddress;

  const callFromAddress = !submit && simulationFromAddress
    ? getAddress(simulationFromAddress)
    : signerAddress;
  if (!submit && simulationFromAddress) {
    executionSummary.simulationFromAddress = callFromAddress;
  }

  const transactionRequest = {
    to: preparedContractCall.targetContractAddress,
    data: preparedContractCall.calldata,
    value: normalizeTransactionValue(preparedContractCall.value || '0'),
    from: callFromAddress,
  };

  executionSummary.attempted = true;

  try {
    if (!submit) {
      const callResult = await provider.call(transactionRequest);
      executionSummary.simulated = true;
      executionSummary.completed = true;
      return { executionSummary, transactionRequest, callResult };
    }

    const response = await wallet.sendTransaction({
      to: transactionRequest.to,
      data: transactionRequest.data,
      value: transactionRequest.value,
    });
    executionSummary.submitted = true;
    executionSummary.completed = true;
    executionSummary.txHash = response.hash;
    return { executionSummary, transactionRequest, callResult: null };
  } catch (error) {
    executionSummary.failureReason = describeExecutionError(error);
    return { executionSummary, transactionRequest, callResult: null };
  }
}

async function deployCommunalProxy(options) {
  const submit = parseBooleanOption(options.submit, false);
  const executionSummary = {
    requested: true,
    dryRun: !submit,
    attempted: false,
    simulated: false,
    submitted: false,
    completed: false,
    signerAddress: null,
    txHash: null,
    failureReason: null,
    alreadyDeployed: false,
  };

  const dapiName = normalizeLiteralDapiName(options.dapiName);
  const { provider, rpcUrl, chainId } = await getProviderAndChain(options);
  const addresses = getResolvedAddresses(chainId, options);
  const factoryAddress = addresses.api3ReaderProxyV1Factory;
  const proxyAddress = computeCommunalApi3ReaderProxyV1Address(chainId, dapiName);
  const dapiNameBytes32 = encodeBytes32String(dapiName);

  if (!factoryAddress) {
    executionSummary.failureReason = `No Api3ReaderProxyV1Factory is configured for chain ${chainId}.`;
    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress: null,
      executionSummary,
      transactionRequest: null,
      verification: null,
    };
  }

  const existingCode = await provider.getCode(proxyAddress);
  if (existingCode && existingCode !== '0x') {
    executionSummary.completed = true;
    executionSummary.alreadyDeployed = true;
    const communalProxyContract = Api3ReaderProxyV1__factory.connect(proxyAddress, provider);
    const [value, timestamp] = await communalProxyContract.read();
    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress,
      executionSummary,
      transactionRequest: null,
      verification: {
        proxyHasCode: true,
        method: 'Api3ReaderProxyV1.read()',
        value: value.toString(),
        timestamp: Number(timestamp),
        timestampIso: new Date(Number(timestamp) * 1000).toISOString(),
      },
    };
  }

  if (!options.privateKey) {
    executionSummary.failureReason = 'Execution requires rpcUrl and privateKey.';
    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress,
      executionSummary,
      transactionRequest: null,
      verification: { proxyHasCode: false },
    };
  }

  if (submit && options.acknowledgement !== SEND_ACKNOWLEDGEMENT) {
    executionSummary.failureReason = `Submitting requires acknowledgement=${SEND_ACKNOWLEDGEMENT}.`;
    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress,
      executionSummary,
      transactionRequest: null,
      verification: { proxyHasCode: false },
    };
  }

  const wallet = new Wallet(options.privateKey, provider);
  const signerAddress = await wallet.getAddress();
  executionSummary.signerAddress = signerAddress;

  const factoryInterface = Api3ReaderProxyV1Factory__factory.createInterface();
  const transactionRequest = {
    to: factoryAddress,
    data: factoryInterface.encodeFunctionData('deployApi3ReaderProxyV1', [dapiNameBytes32, 1, '0x']),
    value: 0n,
    from: signerAddress,
  };

  executionSummary.attempted = true;

  try {
    if (!submit) {
      await provider.call(transactionRequest);
      executionSummary.simulated = true;
      executionSummary.completed = true;
      return {
        command: 'deploy-communal-proxy',
        chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
        dapiName,
        communalProxy: proxyAddress,
        factoryAddress,
        executionSummary,
        transactionRequest: {
          to: transactionRequest.to,
          data: transactionRequest.data,
          value: transactionRequest.value.toString(),
          from: transactionRequest.from,
        },
        verification: { proxyHasCode: false },
      };
    }

    const response = await wallet.sendTransaction({
      to: transactionRequest.to,
      data: transactionRequest.data,
      value: transactionRequest.value,
    });
    const receipt = await response.wait();
    executionSummary.submitted = true;
    executionSummary.completed = Boolean(receipt?.status === 1);
    executionSummary.txHash = response.hash;
    if (receipt?.status !== 1) {
      executionSummary.failureReason = `Proxy deployment transaction reverted with status ${receipt?.status}.`;
    }

    const finalCode = await provider.getCode(proxyAddress);
    const communalProxyContract = Api3ReaderProxyV1__factory.connect(proxyAddress, provider);
    const [value, timestamp] = await communalProxyContract.read();

    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress,
      executionSummary,
      transactionRequest: {
        to: transactionRequest.to,
        data: transactionRequest.data,
        value: transactionRequest.value.toString(),
        from: transactionRequest.from,
      },
      receipt: receipt
        ? {
            blockNumber: receipt.blockNumber,
            status: receipt.status,
            gasUsed: receipt.gasUsed.toString(),
          }
        : null,
      verification: {
        proxyHasCode: Boolean(finalCode && finalCode !== '0x'),
        method: 'Api3ReaderProxyV1.read()',
        value: value.toString(),
        timestamp: Number(timestamp),
        timestampIso: new Date(Number(timestamp) * 1000).toISOString(),
      },
    };
  } catch (error) {
    executionSummary.failureReason = describeExecutionError(error);
    return {
      command: 'deploy-communal-proxy',
      chain: { chainId, requested: options.chainId ?? options.chain, rpcUrl },
      dapiName,
      communalProxy: proxyAddress,
      factoryAddress,
      executionSummary,
      transactionRequest: {
        to: transactionRequest.to,
        data: transactionRequest.data,
        value: transactionRequest.value.toString(),
        from: transactionRequest.from,
      },
      verification: { proxyHasCode: false },
    };
  }
}

function buildPreparedBuySubscriptionCall({ api3MarketV2Address, partialArgumentBundle, wrapperCallDiagnostics, exactTransactionExecutionSupported }) {
  if (!api3MarketV2Address || !partialArgumentBundle?.dapiManagementAndDapiPricingMerkleData) {
    return null;
  }

  const marketInterface = Api3MarketV2__factory.createInterface();
  const functionFragment = marketInterface.getFunction('buySubscription');
  const wrapperFunctionFragment = marketInterface.getFunction('tryMulticallAndBuySubscription');
  const orderedArguments = [
    partialArgumentBundle.dapiName,
    partialArgumentBundle.dataFeedId,
    partialArgumentBundle.sponsorWallet,
    partialArgumentBundle.updateParameters,
    partialArgumentBundle.duration,
    partialArgumentBundle.price,
    partialArgumentBundle.dapiManagementAndDapiPricingMerkleData,
  ];

  const sendTransactionSupported = Boolean(exactTransactionExecutionSupported);

  return {
    sendTransactionSupported,
    calldataDerivable: true,
    preparedButNotTransmitted: true,
    note: sendTransactionSupported
      ? 'This phase prepares the exact buySubscription call data for one selected queue entry only. It does not send or broadcast any transaction.'
      : 'The exact buySubscription calldata is derivable from local inputs, but the on-chain Merkle roots do not match the local data. Direct execution would revert. Use browser-assisted funding instead.',
    targetContractAddress: api3MarketV2Address,
    functionName: functionFragment.name,
    functionSignature: functionFragment.format('sighash'),
    abiFragment: functionFragment.format('full'),
    stateMutability: functionFragment.stateMutability,
    value: partialArgumentBundle.price,
    arguments: {
      ordered: orderedArguments,
      named: {
        dapiName: partialArgumentBundle.dapiName,
        dataFeedId: partialArgumentBundle.dataFeedId,
        sponsorWallet: partialArgumentBundle.sponsorWallet,
        updateParameters: partialArgumentBundle.updateParameters,
        duration: partialArgumentBundle.duration,
        price: partialArgumentBundle.price,
        dapiManagementAndDapiPricingMerkleData: partialArgumentBundle.dapiManagementAndDapiPricingMerkleData,
      },
    },
    calldata: marketInterface.encodeFunctionData('buySubscription', /** @type {any} */ (orderedArguments)),
    multicallPreparation: {
      functionName: wrapperFunctionFragment.name,
      functionSignature: wrapperFunctionFragment.format('sighash'),
      abiFragment: wrapperFunctionFragment.format('full'),
      stateMutability: wrapperFunctionFragment.stateMutability,
      supported: Boolean(wrapperCallDiagnostics?.wrapperCallSupported),
      wrapperCallSupported: Boolean(wrapperCallDiagnostics?.wrapperCallSupported),
      wrapperCallPreparationSupported: Boolean(wrapperCallDiagnostics?.wrapperCallPreparationSupported),
      exactTryMulticallDataDerivable: Boolean(wrapperCallDiagnostics?.exactTryMulticallDataDerivable),
      reason: wrapperCallDiagnostics?.reason || 'Wrapper preparation diagnostics unavailable.',
      blockers: wrapperCallDiagnostics?.blockers || [],
      tryMulticallData: Array.isArray(wrapperCallDiagnostics?.tryMulticallData)
        ? wrapperCallDiagnostics.tryMulticallData
        : null,
      activationPath: wrapperCallDiagnostics?.activationPath || null,
      readyingPlan: wrapperCallDiagnostics?.readyingPlan || null,
      signedBeaconUpdates: wrapperCallDiagnostics?.signedBeaconUpdates || [],
      preparedWrapperCall:
        wrapperCallDiagnostics?.wrapperCallPreparationSupported
        && Array.isArray(wrapperCallDiagnostics?.tryMulticallData)
          ? {
              preparedButNotTransmitted: true,
              sendTransactionSupported: Boolean(wrapperCallDiagnostics?.wrapperCallSupported),
              targetContractAddress: api3MarketV2Address,
              functionName: wrapperFunctionFragment.name,
              functionSignature: wrapperFunctionFragment.format('sighash'),
              abiFragment: wrapperFunctionFragment.format('full'),
              stateMutability: wrapperFunctionFragment.stateMutability,
              value: partialArgumentBundle.price,
              arguments: {
                ordered: [wrapperCallDiagnostics.tryMulticallData, ...orderedArguments],
                named: {
                  tryMulticallData: wrapperCallDiagnostics.tryMulticallData,
                  dapiName: partialArgumentBundle.dapiName,
                  dataFeedId: partialArgumentBundle.dataFeedId,
                  sponsorWallet: partialArgumentBundle.sponsorWallet,
                  updateParameters: partialArgumentBundle.updateParameters,
                  duration: partialArgumentBundle.duration,
                  price: partialArgumentBundle.price,
                  dapiManagementAndDapiPricingMerkleData: partialArgumentBundle.dapiManagementAndDapiPricingMerkleData,
                },
              },
              calldata: marketInterface.encodeFunctionData('tryMulticallAndBuySubscription', /** @type {any} */ ([
                wrapperCallDiagnostics.tryMulticallData,
                ...orderedArguments,
              ])),
            }
          : null,
    },
  };
}

function buildContractActivationPlan({ chainInput, chainId, dapiName, chainState }) {
  const chainCatalogEntry = getChainCatalogEntry(chainInput, chainId);
  const dapiNameBytes32 = encodeBytes32String(dapiName);
  const dapiNameHash = keccak256(dapiNameBytes32);
  const api3MarketV2Address = deploymentAddresses.Api3MarketV2?.[String(chainId)] || null;
  const likelyDurationDays = getLikelySubscriptionDurationDays(chainCatalogEntry);
  const likelyDurationSeconds = likelyDurationDays * 24 * 60 * 60;

  return {
    executionSurface: 'Api3MarketV2',
    chain: {
      chainId,
      requested: chainInput || null,
      catalogAlias: chainCatalogEntry?.alias || null,
      catalogStage: chainCatalogEntry?.stage || 'unknown',
      isTestnet: isTestnetChain(chainCatalogEntry),
    },
    dapiName,
    dapiNameBytes32,
    dapiNameHash,
    dataFeedId: chainState?.dataFeedId || null,
    api3MarketV2Address,
    communalProxy:
      chainState?.communalProxy || computeCommunalApi3ReaderProxyV1Address(chainId, dapiName),
    likelySubscription: {
      durationDays: likelyDurationDays,
      durationSeconds: likelyDurationSeconds,
      heartbeatSeconds: HEARTBEAT_SECONDS,
      supportedDeviationChoicesPercent: SUPPORTED_DEVIATION_CHOICES_PERCENT,
      defaultProxyKind: 'communal',
      oevAssumption: 'none',
    },
    requiredFunctions: [
      'buySubscription(bytes32 dapiName, bytes32 dataFeedId, address sponsorWallet, bytes updateParameters, uint256 duration, uint256 price, bytes dapiManagementAndDapiPricingMerkleData)',
      'getDapiData(bytes32 dapiName)',
    ],
    derivationCommand: {
      command: 'prepare-contract-call',
      purpose: 'Derive the exact non-sending buySubscription() call data when pricing and Merkle prerequisites are available.',
      fallbackCommand: 'purchase-inputs',
    },
    contractExecutionReadiness: {
      canDeriveContractAddress: Boolean(api3MarketV2Address),
      canDeriveDapiHash: true,
      canDeriveDuration: true,
      canDeriveHeartbeat: true,
      canDeriveDeviationChoices: true,
      canDeriveFeedLevelSponsorWallet: true,
      canDeriveDataFeedIdWithoutExtraInputs: Boolean(chainState?.dataFeedId),
      blockedByUnknownInputs: true,
      missingInputs: [
        'selected queue subscription entry (duration + deviation threshold)',
        'updateParameters bytes for the selected subscription tier',
        'price',
        'dapiManagementAndDapiPricingMerkleData',
      ],
      note:
        'Use the prepare-contract-call command to derive an exact non-sending buySubscription() payload for a chosen queue entry. If prerequisites are missing, it will report explicit unsupported diagnostics instead of pretending the transaction path is ready.',
    },
    notes: [
      'Heartbeat is explicitly 24 hours.',
      'Supported deviation choices are queue subscription options for the same feed-level sponsor wallet, not separate wallet paths.',
      'Smaller deviation thresholds get queue priority.',
      'Use the communal/generic proxy path by default. No dApp-specific OEV assumptions are made.',
      'Contract-level activation is a promising path, but full execution remains blocked until the pricing and merkle purchase payloads are reproduced or sourced reliably.',
    ],
  };
}

async function queuePlan(options) {
  const purchasePlan = await purchaseInputs(options);

  return {
    command: 'queue-plan',
    chain: purchasePlan.chain,
    dapiName: purchasePlan.dapiName,
    dapiNameBytes32: purchasePlan.dapiNameBytes32,
    communalProxy: purchasePlan.communalProxy,
    queueSubscriptionModel: purchasePlan.queueSubscriptionModel,
    chosenQueueEntry: purchasePlan.chosenQueueEntry,
    unsupportedDiagnostics: purchasePlan.unsupportedDiagnostics,
  };
}

function buildActivationMetadata({ chainInput, chainId, dapiName, classification, chainState }) {
  const marketExecutionPlan = buildMarketExecutionPlan({
    chainInput,
    chainId,
    dapiName,
    classification,
    chainState,
  });
  const isActive = Boolean(chainState?.isActiveOnChain);

  return {
    isActive,
    requiresFunding: !isActive,
    recommendedAction: isActive ? 'integrate' : 'activate-and-fund-in-market',
    status: classification,
    market: marketExecutionPlan.market,
    marketExecutionPlan,
    browserAutomationPlan: marketExecutionPlan,
    contractActivationPlan: buildContractActivationPlan({
      chainInput,
      chainId,
      dapiName,
      chainState,
    }),
    nextSteps: isActive
      ? ['Feed is already operational on this chain.', 'Use the communal proxy or Market integration page.']
      : [
          'Feed is not operational on this chain yet.',
          'Open the activation URL in Api3 Market.',
          'Fund and activate the feed there, then re-run ensure-active or resolve.',
        ],
  };
}

function buildCatalogIndex() {
  return dapiCatalog.map((entry) => ({
    name: entry.name,
    normalizedName: normalizeDapiName(entry.name),
    stage: entry.stage || 'unknown',
    metadata: entry.metadata || {},
    providers: Array.isArray(entry.providers) ? entry.providers : [],
  }));
}

function getCatalogDapiEntry(dapiName) {
  const normalizedName = normalizeDapiName(dapiName);
  return dapiCatalog.find((entry) => normalizeDapiName(entry.name) === normalizedName) || null;
}

async function getProviderAndChain(options) {
  const rpcUrl = options.rpcUrl;
  if (!rpcUrl) {
    throw new Error('Missing required --rpc-url');
  }

  const provider = new JsonRpcProvider(rpcUrl);
  const providerNetwork = await provider.getNetwork();
  const inferredChainId = Number(providerNetwork.chainId);
  const chainInput = options.chainId ?? options.chain;
  const requestedChainId = normalizeChainId(chainInput);
  const chainId = requestedChainId ?? inferredChainId;

  if (requestedChainId && requestedChainId !== inferredChainId) {
    throw new Error(
      `Chain mismatch: provider returned ${inferredChainId}, but input requested ${requestedChainId}`
    );
  }

  return { provider, rpcUrl, chainId, chainInput };
}

function getResolvedAddresses(chainId, options) {
  const defaults = getDefaultAddresses(chainId);
  const api3Server = options.api3Server ? getAddress(options.api3Server) : defaults.api3Server;
  const airseekerRegistry = options.airseekerRegistry
    ? getAddress(options.airseekerRegistry)
    : defaults.airseekerRegistry;
  const api3ReaderProxyV1Factory = options.api3ReaderProxyV1Factory
    ? getAddress(options.api3ReaderProxyV1Factory)
    : defaults.api3ReaderProxyV1Factory;

  if (!api3Server || !isAddress(api3Server)) {
    throw new Error(`Missing Api3ServerV1 address for chain ${chainId}. Pass --api3-server explicitly.`);
  }

  if (!airseekerRegistry || !isAddress(airseekerRegistry)) {
    throw new Error(
      `Missing AirseekerRegistry address for chain ${chainId}. Pass --airseeker-registry explicitly.`
    );
  }

  return { api3Server, airseekerRegistry, api3ReaderProxyV1Factory };
}

async function fetchActiveFeeds(provider, airseekerRegistry) {
  const airseekerRegistryContract = AirseekerRegistry__factory.connect(airseekerRegistry, provider);
  const count = Number(await airseekerRegistryContract.activeDataFeedCount());
  const items = [];

  for (let index = 0; index < count; index += 1) {
    const activeFeed = await airseekerRegistryContract.activeDataFeed(index);
    const dapiName = decodeBytes32String(activeFeed.dapiName);
    items.push({
      index,
      dataFeedId: activeFeed.dataFeedId,
      dapiName,
      normalizedName: normalizeDapiName(dapiName),
      dataFeedDetails: activeFeed.dataFeedDetails,
      decodedDataFeedDetails: decodeDataFeedDetails(activeFeed.dataFeedDetails),
      dataFeedValue: activeFeed.dataFeedValue.toString(),
      dataFeedTimestamp: Number(activeFeed.dataFeedTimestamp),
      dataFeedTimestampIso: new Date(Number(activeFeed.dataFeedTimestamp) * 1000).toISOString(),
      beaconValues: activeFeed.beaconValues.map((value) => value.toString()),
      beaconTimestamps: activeFeed.beaconTimestamps.map((value) => Number(value)),
      updateParameters: activeFeed.updateParameters,
      decodedUpdateParameters: decodeUpdateParameters(activeFeed.updateParameters),
      signedApiUrls: [...activeFeed.signedApiUrls],
    });
  }

  return items;
}

function buildDiscoveryMatches({ query, catalogEntries, activeFeeds, chainInput, chainId }) {
  const normalizedQuery = normalizeDapiName(query);
  const activeByName = new Map(activeFeeds.map((item) => [item.normalizedName, item]));

  const catalogMatches = catalogEntries.filter(({ normalizedName }) => {
    if (!normalizedQuery) {
      return true;
    }

    return normalizedName.includes(normalizedQuery);
  });

  const activeOnlyMatches = activeFeeds.filter(
    ({ normalizedName }) => !catalogMatches.some((entry) => entry.normalizedName === normalizedName)
  );

  const extraActiveMatches = normalizedQuery
    ? activeOnlyMatches.filter(({ normalizedName }) => normalizedName.includes(normalizedQuery))
    : activeOnlyMatches;

  const chainCatalogEntry = getChainCatalogEntry(chainInput, chainId);

  const matches = catalogMatches.map((entry) => {
    const active = activeByName.get(entry.normalizedName);
    const classification = active ? (entry.stage === 'active' ? 'active' : 'ambiguous') : 'inactive';
    const chainState = active
      ? {
          isActiveOnChain: true,
          dataFeedId: active.dataFeedId,
          communalProxy: computeCommunalApi3ReaderProxyV1Address(chainId, entry.name),
          dataFeedTimestamp: active.dataFeedTimestamp,
          dataFeedTimestampIso: active.dataFeedTimestampIso,
          decodedDataFeedDetails: active.decodedDataFeedDetails,
          decodedUpdateParameters: active.decodedUpdateParameters,
        }
      : {
          isActiveOnChain: false,
          communalProxy: computeCommunalApi3ReaderProxyV1Address(chainId, entry.name),
        };

    return {
      dapiName: entry.name,
      classification,
      catalog: {
        stage: entry.stage,
        metadata: entry.metadata,
        providers: entry.providers,
      },
      chainState,
      activation: buildActivationMetadata({
        chainInput,
        chainId,
        dapiName: entry.name,
        classification,
        chainState,
      }),
      notes:
        classification === 'ambiguous'
          ? ['Catalog stage and on-chain activity disagree, treat this as ambiguous.']
          : [],
    };
  });

  for (const active of extraActiveMatches) {
    const chainState = {
      isActiveOnChain: true,
      dataFeedId: active.dataFeedId,
      communalProxy: computeCommunalApi3ReaderProxyV1Address(chainId, active.dapiName),
      dataFeedTimestamp: active.dataFeedTimestamp,
      dataFeedTimestampIso: active.dataFeedTimestampIso,
      decodedDataFeedDetails: active.decodedDataFeedDetails,
      decodedUpdateParameters: active.decodedUpdateParameters,
    };

    matches.push({
      dapiName: active.dapiName,
      classification: 'ambiguous',
      catalog: null,
      chainState,
      activation: buildActivationMetadata({
        chainInput,
        chainId,
        dapiName: active.dapiName,
        classification: 'ambiguous',
        chainState,
      }),
      notes: ['Feed is active on-chain but missing from local dAPI catalog.'],
    });
  }

  matches.sort((left, right) => left.dapiName.localeCompare(right.dapiName));

  return {
    chain: {
      chainId,
      requested: chainInput || null,
      catalogAlias: chainCatalogEntry?.alias || null,
      catalogStage: chainCatalogEntry?.stage || 'unknown',
      marketChainSlug: getMarketChainSlug(chainInput, chainId),
    },
    query: query || null,
    totalCatalogEntries: catalogEntries.length,
    activeFeedCount: activeFeeds.length,
    matchCount: matches.length,
    matches,
  };
}

async function discoverFeeds(options) {
  const query = options.query || options.dapiName || options.dapi || options.name || '';
  const limit = Number(options.limit || 20);
  const { provider, chainId } = await getProviderAndChain(options);
  const { airseekerRegistry } = getResolvedAddresses(chainId, options);
  const catalogEntries = buildCatalogIndex();
  const activeFeeds = await fetchActiveFeeds(provider, airseekerRegistry);
  const result = buildDiscoveryMatches({
    query,
    catalogEntries,
    activeFeeds,
    chainInput: options.chainId ?? options.chain,
    chainId,
  });

  return {
    ...result,
    matches: result.matches.slice(0, limit),
    truncated: result.matches.length > limit,
    addresses: {
      airseekerRegistry,
    },
  };
}

async function fetchPricingCoverageStatus(url) {
  const response = await fetch(url, {
    method: 'HEAD',
    headers: { 'User-Agent': 'openclaw-api3-feed-manager/1.0' },
  });

  return {
    url,
    ok: response.ok,
    status: response.status,
  };
}

function buildCoverageClassification({ lifecycleStage, pricingFile, dapiManagementEntry, dapiManagementEntryZeroed }) {
  if (lifecycleStage === 'retired' || lifecycleStage === 'delisted') {
    return {
      code: 'retired-delisted',
      blockerCategory: 'retired-delisted',
      lifecycleStage,
      activatable: false,
    };
  }

  if (!pricingFile.ok) {
    return {
      code: 'missing-market-pricing-coverage',
      blockerCategory: 'missing-queue-coverage',
      lifecycleStage,
      activatable: false,
    };
  }

  if (!dapiManagementEntry || dapiManagementEntryZeroed) {
    return {
      code: 'zeroed-or-missing-dapi-management-entry',
      blockerCategory: !dapiManagementEntry ? 'missing-feed-management-entry' : 'zeroed-feed-management-entry',
      lifecycleStage,
      activatable: false,
    };
  }

  return {
    code: 'market-contract-path-available',
    blockerCategory: null,
    lifecycleStage,
    activatable: true,
  };
}

async function buildCoverageItemsForChain({ chainTarget, catalogEntries }) {
  const items = [];
  const concurrency = 15;

  for (let index = 0; index < catalogEntries.length; index += concurrency) {
    const chunk = catalogEntries.slice(index, index + concurrency);
    const chunkItems = await Promise.all(chunk.map(async (entry) => {
      const pricingFile = await fetchPricingCoverageStatus(buildPricingFileUrl(chainTarget.chainId, entry.name));
      const dapiManagementEntry = getDapiManagementEntry(encodeBytes32String(entry.name));
      const lifecycleStage = String(entry.stage || 'unknown').toLowerCase();
      const dapiManagementEntryZeroed = dapiManagementEntry?.dataFeedId === ZERO_BYTES32;
      const coverage = buildCoverageClassification({
        lifecycleStage,
        pricingFile,
        dapiManagementEntry,
        dapiManagementEntryZeroed,
      });

      return {
        chain: chainTarget.label,
        chainId: chainTarget.chainId,
        dapiName: entry.name,
        category: coverage.code,
        blockerCategory: coverage.blockerCategory,
        lifecycleStage: coverage.lifecycleStage,
        activatable: coverage.activatable,
        pricingStatus: pricingFile.ok ? 'available' : `missing:${pricingFile.status}`,
        pricingFile,
        dapiManagementEntryZeroed,
        providers: entry.providers,
      };
    }));
    items.push(...chunkItems);
  }

  return items;
}

function filterCoverageItems(items, requestedCategory) {
  if (!requestedCategory) {
    return items;
  }

  return items.filter((item) => item.category === requestedCategory || item.blockerCategory === requestedCategory);
}

function buildCoverageSummary(items) {
  return items.reduce((acc, item) => {
    acc[item.category] = (acc[item.category] || 0) + 1;
    return acc;
  }, {});
}

function buildCoverageAuditChainResult({ chainTarget, items, requestedCategory, limit }) {
  const filteredItems = filterCoverageItems(items, requestedCategory);
  const limitedItems = filteredItems.slice(0, limit);

  return {
    chain: {
      chainId: chainTarget.chainId,
      requested: chainTarget.requested,
      marketChainSlug: getMarketChainSlug(chainTarget.requested, chainTarget.chainId),
      label: chainTarget.label,
    },
    filters: {
      category: requestedCategory || null,
      limit,
    },
    totals: {
      scanned: items.length,
      matched: filteredItems.length,
      returned: limitedItems.length,
      activatable: filteredItems.filter((item) => item.activatable).length,
      blocked: filteredItems.filter((item) => !item.activatable).length,
    },
    summaryCounts: buildCoverageSummary(filteredItems),
    items: limitedItems,
  };
}

function buildCsv(rows) {
  if (!rows.length) {
    return '';
  }

  const headers = [...rows.reduce((set, row) => {
    Object.keys(row).forEach((key) => set.add(key));
    return set;
  }, new Set())];

  const escapeCell = (value) => {
    const stringValue = value === null || value === undefined
      ? ''
      : typeof value === 'object'
        ? JSON.stringify(value)
        : String(value);

    if (!/[",\n]/.test(stringValue)) {
      return stringValue;
    }

    return `"${stringValue.replace(/"/g, '""')}"`;
  };

  return [
    headers.join(','),
    ...rows.map((row) => headers.map((header) => escapeCell(row[header])).join(',')),
  ].join('\n');
}

function flattenCoverageAuditRows(result) {
  const chainResults = Array.isArray(result.chains) ? result.chains : [result];

  return chainResults.flatMap((chainResult) => chainResult.items.map((item) => ({
    chain: item.chain,
    chainId: item.chainId,
    dapiName: item.dapiName,
    category: item.category,
    blockerCategory: item.blockerCategory,
    lifecycleStage: item.lifecycleStage,
    activatable: item.activatable,
    pricingStatus: item.pricingStatus,
    dapiManagementEntryZeroed: item.dapiManagementEntryZeroed,
  })));
}

function flattenCoverageMatrixRows(result) {
  return result.rows.flatMap((row) => row.chains.map((chainEntry) => ({
    dapiName: row.dapiName,
    chain: chainEntry.chain,
    chainId: chainEntry.chainId,
    category: chainEntry.category,
    blockerCategory: chainEntry.blockerCategory,
    lifecycleStage: chainEntry.lifecycleStage,
    activatable: chainEntry.activatable,
    pricingStatus: chainEntry.pricingStatus,
    dapiManagementEntryZeroed: chainEntry.dapiManagementEntryZeroed,
  })));
}

function outputResult(command, result, options) {
  const format = String(options.format || (options.csv ? 'csv' : 'json')).trim().toLowerCase();

  if (format === 'csv') {
    if (command === 'coverage-audit') {
      console.log(buildCsv(flattenCoverageAuditRows(result)));
      return;
    }

    if (command === 'coverage-matrix') {
      console.log(buildCsv(flattenCoverageMatrixRows(result)));
      return;
    }

    if (command === 'supported-chains') {
      console.log(buildCsv(result.items));
      return;
    }

    throw new Error(`CSV output is not supported for command: ${command}`);
  }

  console.log(JSON.stringify(result, null, 2));
}

async function coverageAudit(options) {
  const query = String(options.query || '').trim();
  const requestedCategory = String(options.category || options.status || '').trim().toLowerCase();
  const limit = Number(options.limit || 50);
  const normalizedQuery = query ? normalizeDapiName(query) : '';
  const chainTargets = await resolveCoverageChainTargets(options);

  const catalogEntries = buildCatalogIndex().filter((entry) => (
    !normalizedQuery || entry.normalizedName.includes(normalizedQuery)
  ));

  const chainResults = await Promise.all(chainTargets.map(async (chainTarget) => {
    const items = await buildCoverageItemsForChain({ chainTarget, catalogEntries });
    return buildCoverageAuditChainResult({ chainTarget, items, requestedCategory, limit });
  }));

  if (chainResults.length === 1) {
    return {
      command: 'coverage-audit',
      ...chainResults[0],
      filters: {
        query: query || null,
        category: requestedCategory || null,
        limit,
      },
    };
  }

  return {
    command: 'coverage-audit',
    filters: {
      query: query || null,
      category: requestedCategory || null,
      limit,
    },
    totals: {
      chainsScanned: chainResults.length,
      scanned: chainResults.reduce((sum, chainResult) => sum + chainResult.totals.scanned, 0),
      matched: chainResults.reduce((sum, chainResult) => sum + chainResult.totals.matched, 0),
      returned: chainResults.reduce((sum, chainResult) => sum + chainResult.totals.returned, 0),
    },
    chains: chainResults,
  };
}

async function coverageMatrix(options) {
  const query = String(options.query || options.dapiName || '').trim();
  if (!query) {
    throw new Error('Missing required --query for coverage-matrix');
  }

  const requestedCategory = String(options.category || options.status || '').trim().toLowerCase();
  const limit = Number(options.limit || 25);
  const chainTargets = await resolveCoverageChainTargets(options);
  const normalizedQuery = normalizeDapiName(query);
  const catalogEntries = buildCatalogIndex()
    .filter((entry) => entry.normalizedName.includes(normalizedQuery))
    .slice(0, limit);

  const chainItemMaps = new Map();
  for (const chainTarget of chainTargets) {
    const items = await buildCoverageItemsForChain({ chainTarget, catalogEntries });
    chainItemMaps.set(chainTarget.label, new Map(items.map((item) => [item.dapiName, item])));
  }

  const rows = catalogEntries.map((entry) => {
    const chainEntries = chainTargets.map((chainTarget) => {
      const item = chainItemMaps.get(chainTarget.label)?.get(entry.name);
      return item ? {
        chain: item.chain,
        chainId: item.chainId,
        category: item.category,
        blockerCategory: item.blockerCategory,
        lifecycleStage: item.lifecycleStage,
        activatable: item.activatable,
        pricingStatus: item.pricingStatus,
        dapiManagementEntryZeroed: item.dapiManagementEntryZeroed,
      } : null;
    }).filter(Boolean);

    return {
      dapiName: entry.name,
      lifecycleStage: String(entry.stage || 'unknown').toLowerCase(),
      chains: chainEntries,
      availableOnChains: chainEntries.filter((chainEntry) => chainEntry.activatable).map((chainEntry) => chainEntry.chain),
      unavailableOnChains: chainEntries.filter((chainEntry) => !chainEntry.activatable).map((chainEntry) => chainEntry.chain),
    };
  }).filter((row) => {
    if (!requestedCategory) {
      return true;
    }

    return row.chains.some((chainEntry) => (
      chainEntry.category === requestedCategory || chainEntry.blockerCategory === requestedCategory
    ));
  });

  return {
    command: 'coverage-matrix',
    filters: {
      query,
      category: requestedCategory || null,
      limit,
      chains: chainTargets.map((chainTarget) => chainTarget.label),
    },
    totals: {
      matchedFeeds: rows.length,
      chainsScanned: chainTargets.length,
    },
    rows,
  };
}

async function supportedChains(options) {
  const requestedStage = String(options.stage || '').trim().toLowerCase();
  const requestedQuery = String(options.query || '').trim().toLowerCase();

  const items = chainCatalog
    .map((entry) => ({
      alias: entry.alias,
      stage: entry.stage || 'unknown',
    }))
    .filter((entry) => (!requestedStage || entry.stage === requestedStage))
    .filter((entry) => (!requestedQuery || entry.alias.includes(requestedQuery)))
    .sort((left, right) => left.alias.localeCompare(right.alias));

  const stageCounts = items.reduce((acc, entry) => {
    acc[entry.stage] = (acc[entry.stage] || 0) + 1;
    return acc;
  }, {});

  return {
    command: 'supported-chains',
    filters: {
      stage: requestedStage || null,
      query: requestedQuery || null,
    },
    total: items.length,
    stageCounts,
    items,
  };
}

async function resolveFeed(options) {
  const dapiName = options.dapiName || options.dapi || options.name;
  if (!dapiName) {
    throw new Error('Missing required --dapi-name');
  }

  const { provider, rpcUrl, chainId } = await getProviderAndChain(options);
  const addresses = getResolvedAddresses(chainId, options);
  const { api3Server, airseekerRegistry } = addresses;
  const dapiNameBytes32 = encodeBytes32String(dapiName);
  const dapiNameHash = keccak256(dapiNameBytes32);
  const communalProxyAddress = computeCommunalApi3ReaderProxyV1Address(chainId, dapiName);
  const api3ReaderProxyV1Factory = deploymentAddresses.Api3ReaderProxyV1Factory?.[String(chainId)] || null;

  const api3ServerContract = Api3ServerV1__factory.connect(api3Server, provider);
  const airseekerRegistryContract = AirseekerRegistry__factory.connect(airseekerRegistry, provider);

  const dataFeedId = await api3ServerContract.dapiNameHashToDataFeedId(dapiNameHash);
  if (!dataFeedId || dataFeedId === ZERO_BYTES32) {
    throw new Error(`No data feed ID found for ${dapiName} on chain ${chainId}.`);
  }

  const dataFeedDetails = await airseekerRegistryContract.dataFeedIdToDetails(dataFeedId);
  const decodedDataFeedDetails = decodeDataFeedDetails(dataFeedDetails);
  const communalProxyCode = await provider.getCode(communalProxyAddress);
  const communalProxyHasCode = Boolean(communalProxyCode && communalProxyCode !== '0x');

  let value;
  let timestamp;
  let verificationMethod = 'Api3ReaderProxyV1.read()';
  try {
    if (!communalProxyHasCode) {
      throw new Error('Communal proxy is not deployed on-chain.');
    }

    const communalProxyContract = Api3ReaderProxyV1__factory.connect(communalProxyAddress, provider);
    [value, timestamp] = await communalProxyContract.read();
  } catch {
    [value, timestamp] = await api3ServerContract.readDataFeedWithDapiNameHash(dapiNameHash);
    verificationMethod = 'Api3ServerV1.readDataFeedWithDapiNameHash()';
  }

  const latestRead = {
    value: value.toString(),
    timestamp: Number(timestamp),
    timestampIso: new Date(Number(timestamp) * 1000).toISOString(),
  };

  const discovery = await discoverFeeds({
    ...options,
    query: dapiName,
    limit: 10,
  });
  const exactMatchSelection = selectPreferredExactMatches(discovery.matches, dapiName);

  return {
    chainId,
    rpcUrl,
    dapiName,
    addresses: {
      api3Server,
      airseekerRegistry,
      api3ReaderProxyV1Factory,
      communalProxy: communalProxyAddress,
    },
    market: buildMarketUrls({
      chainInput: options.chainId ?? options.chain,
      chainId,
      dapiName,
    }),
    canonicalResolution: {
      dapiNameBytes32,
      dapiNameHash,
      dataFeedId,
      dataFeedDetails,
      decodedDataFeedDetails,
    },
    discovery: {
      exactMatchCount: exactMatchSelection.exactMatches.length,
      exactMatchMode: exactMatchSelection.matchMode,
      matches: exactMatchSelection.exactMatches,
    },
    latestRead,
    proxyDeploymentPlan: !communalProxyHasCode && api3ReaderProxyV1Factory
      ? {
          reason: 'The communal Api3ReaderProxyV1 address is predictable but not deployed on-chain yet.',
          proxyAddress: communalProxyAddress,
          factoryAddress: api3ReaderProxyV1Factory,
          dapiName,
          dapiNameBytes32,
          dappId: 1,
          metadata: '0x',
        }
      : null,
    verification: {
      method: verificationMethod,
      ...latestRead,
      proxyHasCode: communalProxyHasCode,
    },
    activation: buildActivationMetadata({
      chainInput: options.chainId ?? options.chain,
      chainId,
      dapiName,
      classification: 'active',
      chainState: {
        isActiveOnChain: true,
        dataFeedId,
        communalProxy: communalProxyAddress,
      },
    }),
  };
}

function rankCandidateMatches(matches, requestedName) {
  const literalRequested = normalizeLiteralDapiName(requestedName);
  const normalizedRequested = normalizeDapiName(requestedName);
  const literalExact = [];
  const exact = [];
  const partial = [];

  for (const match of matches) {
    if (normalizeLiteralDapiName(match.dapiName) === literalRequested) {
      literalExact.push(match);
    } else if (normalizeDapiName(match.dapiName) === normalizedRequested) {
      exact.push(match);
    } else {
      partial.push(match);
    }
  }

  return [...literalExact, ...exact, ...partial];
}

async function ensureActive(options) {
  const requestedName = options.dapiName || options.dapi || options.name || options.query;
  if (!requestedName) {
    throw new Error('Missing required --dapi-name or --query');
  }

  const { chainId, rpcUrl } = await getProviderAndChain(options);
  const discovery = await discoverFeeds({
    ...options,
    query: requestedName,
    limit: Number(options.limit || 10),
  });
  const rankedMatches = rankCandidateMatches(discovery.matches, requestedName);
  const exactMatchSelection = selectPreferredExactMatches(rankedMatches, requestedName);
  const exactMatches = exactMatchSelection.exactMatches;

  if (exactMatchSelection.ambiguous) {
    return {
      status: 'blocked-ambiguous',
      reason: 'Multiple exact catalog matches were returned for the requested dAPI name.',
      chainId,
      rpcUrl,
      requestedName,
      matchMode: exactMatchSelection.matchMode,
      candidateMatches: exactMatches,
    };
  }

  if (exactMatches.length === 1) {
    const exactMatch = exactMatchSelection.preferredMatch;

    if (exactMatch.chainState?.isActiveOnChain) {
      const resolution = await resolveFeed({
        ...options,
        dapiName: exactMatch.dapiName,
      });

      return {
        status: 'active',
        reason: 'Feed is already operational on-chain and usable now.',
        chainId,
        rpcUrl,
        requestedName,
        match: exactMatch,
        marketExecutionPlan: resolution.activation.marketExecutionPlan,
        browserAutomationPlan: resolution.activation.browserAutomationPlan,
        resolution,
      };
    }

    return {
      status: 'inactive',
      reason: 'Feed exists in discovery/catalog state but is not operational on this chain yet.',
      chainId,
      rpcUrl,
      requestedName,
      match: exactMatch,
      marketExecutionPlan: exactMatch.activation.marketExecutionPlan,
      browserAutomationPlan: exactMatch.activation.browserAutomationPlan,
      handoff: exactMatch.activation,
    };
  }

  return {
    status: 'blocked-unavailable',
    reason: 'No exact dAPI match found. Human or agent should pick from candidate matches or broaden the search.',
    chainId,
    rpcUrl,
    requestedName,
    marketSearchUrl: buildMarketUrls({
      chainInput: options.chainId ?? options.chain,
      chainId,
      dapiName: requestedName,
    }).marketSearchUrl,
    candidateMatches: rankedMatches,
  };
}

async function prepareActivation(options) {
  return ensureActive(options);
}

async function browserPlan(options) {
  const rawName = options.dapiName || options.dapi || options.name;
  if (!rawName) {
    throw new Error('Missing required --dapi-name for browser-plan command');
  }

  const { chainId } = await getProviderAndChain(options);
  const chainInput = options.chainId ?? options.chain;

  const discovery = await discoverFeeds({ ...options, query: rawName, limit: 5 });
  const exactMatch = selectPreferredExactMatches(discovery.matches, rawName).preferredMatch;

  const chainState = exactMatch?.chainState || { isActiveOnChain: false, communalProxy: null };

  const plan = buildBrowserPlan({
    chainInput,
    chainId,
    dapiName: exactMatch?.dapiName || normalizeDapiName(rawName),
    chainState,
  });

  return {
    ...plan,
    contractActivationPlan: buildContractActivationPlan({
      chainInput,
      chainId,
      dapiName: exactMatch?.dapiName || normalizeDapiName(rawName),
      chainState,
    }),
  };
}

async function contractPlan(options) {
  const rawName = options.dapiName || options.dapi || options.name;
  if (!rawName) {
    throw new Error('Missing required --dapi-name for contract-plan command');
  }

  const { chainId } = await getProviderAndChain(options);
  const chainInput = options.chainId ?? options.chain;
  const discovery = await discoverFeeds({ ...options, query: rawName, limit: 5 });
  const exactMatch = selectPreferredExactMatches(discovery.matches, rawName).preferredMatch;
  const normalizedName = exactMatch?.dapiName || normalizeDapiName(rawName);
  const chainState = exactMatch?.chainState || {
    isActiveOnChain: false,
    communalProxy: computeCommunalApi3ReaderProxyV1Address(chainId, normalizedName),
  };

  return buildContractActivationPlan({
    chainInput,
    chainId,
    dapiName: normalizedName,
    chainState,
  });
}

async function purchaseInputs(options) {
  const rawName = options.dapiName || options.dapi || options.name;
  if (!rawName) {
    throw new Error('Missing required --dapi-name for purchase-inputs command');
  }

  const { provider, chainId } = await getProviderAndChain(options);
  const chainInput = options.chainId ?? options.chain;
  const discovery = await discoverFeeds({ ...options, query: rawName, limit: 5 });
  const exactMatch = selectPreferredExactMatches(discovery.matches, rawName).preferredMatch;
  const dapiName = exactMatch?.dapiName || normalizeDapiName(rawName);
  const dapiNameBytes32 = encodeBytes32String(dapiName);
  const pricingFileUrl = buildPricingFileUrl(chainId, dapiName);
  const pricingResponse = await fetchJsonWithStatus(pricingFileUrl);
  const pricingOptions = pricingResponse.ok && Array.isArray(pricingResponse.json?.leaves)
    ? pricingResponse.json.leaves.map(decodePricingLeaf)
    : [];
  const chosenSubscriptionOption = selectPricingOption(options, pricingOptions);
  const derivedSponsorWallet = deriveSponsorWalletAddress(dapiNameBytes32);
  const api3MarketV2Address = deploymentAddresses.Api3MarketV2?.[String(chainId)] || null;
  const communalProxy = exactMatch?.chainState?.communalProxy || computeCommunalApi3ReaderProxyV1Address(chainId, dapiName);

  let onChainRegisteredRoots = null;
  if (api3MarketV2Address) {
    const market = Api3MarketV2__factory.connect(api3MarketV2Address, provider);
    const dapiManagementHashType = await market.DAPI_MANAGEMENT_MERKLE_ROOT_HASH_TYPE();
    const dapiPricingHashType = await market.DAPI_PRICING_MERKLE_ROOT_HASH_TYPE();
    onChainRegisteredRoots = {
      dapiManagementMerkleRoot: await market.getHashValue(dapiManagementHashType),
      dapiPricingMerkleRoot: await market.getHashValue(dapiPricingHashType),
    };
  }

  let liveDapiManagementMerkleTreeData = null;
  let liveDapiManagementFetchError = null;
  if (onChainRegisteredRoots?.dapiManagementMerkleRoot && dapiManagementMerkleTreeData.hash !== onChainRegisteredRoots.dapiManagementMerkleRoot) {
    try {
      liveDapiManagementMerkleTreeData = await fetchLiveDapiManagementMerkleTreeData();
    } catch (error) {
      liveDapiManagementFetchError = error;
    }
  }
  const dapiManagementSourceSelection = selectPreferredDapiManagementMerkleTreeData({
    localTreeData: dapiManagementMerkleTreeData,
    liveTreeData: liveDapiManagementMerkleTreeData,
    onChainRegisteredRoots,
  });
  const activeDapiManagementMerkleTreeData = dapiManagementSourceSelection.treeData;
  const dapiManagementEntry = getDapiManagementEntry(dapiNameBytes32, activeDapiManagementMerkleTreeData);
  const currentPublicProviderAliases = Array.isArray(exactMatch?.providers) && exactMatch.providers.length > 0
    ? exactMatch.providers
    : (dapiCatalog.find((entry) => entry.name === dapiName)?.providers || []);
  const currentPublicDataFeedModel = deriveCurrentPublicDataFeedModel({
    dapiName,
    providerAliases: currentPublicProviderAliases,
  });

  const unsupportedDiagnostics = buildUnsupportedPurchaseDiagnostics({
    dapiName,
    pricingResponse,
    pricingFileUrl,
    pricingOptions,
    chosenSubscriptionOption,
    dapiManagementEntry,
    chainState: exactMatch?.chainState,
  });

  const blockers = [...unsupportedDiagnostics.missingPrerequisites];
  if (dapiManagementEntry && dapiManagementEntry.sponsorWallet !== derivedSponsorWallet) {
    blockers.push('Derived sponsor wallet does not match the sponsor wallet in the exported dAPI management leaf.');
  }
  if (dapiManagementEntry && !dapiManagementEntry.proofMatchesMerkleRoot) {
    blockers.push('The reconstructed dAPI management proof did not hash back to the reconstructed dAPI management Merkle root.');
  }

  const pricingProofBundle = chosenSubscriptionOption
    ? {
        merkleRoot: pricingResponse.json?.merkleRoot || null,
        proof: chosenSubscriptionOption.proof,
        proofMatchesMerkleRoot:
          Boolean(pricingResponse.json?.merkleRoot)
          && processMerkleProof(
            standardLeafHash(
              ['bytes32', 'uint256', 'bytes', 'uint256', 'uint256'],
              [
                chosenSubscriptionOption.dapiNameBytes32,
                chosenSubscriptionOption.chainId,
                chosenSubscriptionOption.updateParameters,
                chosenSubscriptionOption.duration,
                chosenSubscriptionOption.price,
              ]
            ),
            chosenSubscriptionOption.proof
          ) === pricingResponse.json?.merkleRoot,
      }
    : null;

  const exactMerkleDataBundle = chosenSubscriptionOption && dapiManagementEntry && pricingProofBundle?.merkleRoot
    ? ABI_CODER.encode(
        ['bytes32', 'bytes32[]', 'bytes32', 'bytes32[]'],
        [
          dapiManagementEntry.merkleRoot,
          dapiManagementEntry.proof,
          pricingProofBundle.merkleRoot,
          pricingProofBundle.proof,
        ]
      )
    : null;

  const partialArgumentBundle = chosenSubscriptionOption && dapiManagementEntry
    ? {
        dapiName: dapiNameBytes32,
        dataFeedId: dapiManagementEntry.dataFeedId,
        sponsorWallet: dapiManagementEntry.sponsorWallet,
        updateParameters: chosenSubscriptionOption.updateParameters,
        duration: chosenSubscriptionOption.duration,
        price: chosenSubscriptionOption.price,
        dapiManagementAndDapiPricingMerkleData: exactMerkleDataBundle,
      }
    : null;

  const wrapperCallDiagnostics = buildWrapperCallDiagnostics({
    chainState: exactMatch?.chainState,
    exactMerkleDataBundle,
    marketActivationCoverage: unsupportedDiagnostics.marketActivationCoverage,
    dapiManagementEntry,
    chosenSubscriptionOption,
    currentPublicDataFeedModel,
  });

  if (
    !wrapperCallDiagnostics.wrapperCallPreparationSupported
    && exactMerkleDataBundle
    && dapiManagementEntry
    && currentPublicDataFeedModel?.derivable
    && currentPublicDataFeedModel.dataFeedId === dapiManagementEntry.dataFeedId
    && unsupportedDiagnostics.marketActivationCoverage.activatableViaMarketContractPath
    && !exactMatch?.chainState?.isActiveOnChain
  ) {
    try {
      const wrapperReadyingPlan = buildWrapperReadyingPlan({
        currentPublicDataFeedModel,
        signedBeaconUpdates: await fetchCurrentSignedBeaconData({
          beaconMetadata: currentPublicDataFeedModel.beaconMetadata,
        }),
      });

      wrapperCallDiagnostics.wrapperCallPreparationSupported = true;
      wrapperCallDiagnostics.reason = 'The wrapper readying sequence is derivable from the current public provider catalog and live Signed API payloads.';
      wrapperCallDiagnostics.blockers = [];
      wrapperCallDiagnostics.exactTryMulticallDataDerivable = true;
      wrapperCallDiagnostics.tryMulticallData = wrapperReadyingPlan.tryMulticallData;
      wrapperCallDiagnostics.activationPath = wrapperReadyingPlan.activationPath;
      wrapperCallDiagnostics.readyingPlan = wrapperReadyingPlan.readyingPlan;
      wrapperCallDiagnostics.signedBeaconUpdates = wrapperReadyingPlan.signedBeaconUpdates;
    } catch (error) {
      wrapperCallDiagnostics.reason = 'The wrapper readying sequence is structurally known, but fetching the live Signed API payloads failed, so the exact multicall bytes could not be prepared.';
      wrapperCallDiagnostics.blockers = [error?.message || String(error)];
      wrapperCallDiagnostics.activationPath = 'signed-api-fetch-failed';
    }
  }

  const queueSubscriptionModel = buildQueueSubscriptionChoices({
    pricingOptions,
    chosenSubscriptionOption,
    sponsorWallet: dapiManagementEntry?.sponsorWallet || derivedSponsorWallet,
  });
  const directMerklePrerequisitesSatisfied =
    Boolean(exactMerkleDataBundle)
    && dapiManagementEntry?.proofMatchesMerkleRoot === true
    && pricingProofBundle?.proofMatchesMerkleRoot === true
    && (dapiManagementEntry?.merkleRoot === onChainRegisteredRoots?.dapiManagementMerkleRoot || !onChainRegisteredRoots?.dapiManagementMerkleRoot)
    && (pricingProofBundle?.merkleRoot === onChainRegisteredRoots?.dapiPricingMerkleRoot || !onChainRegisteredRoots?.dapiPricingMerkleRoot);
  const preparedContractCall = buildPreparedBuySubscriptionCall({
    api3MarketV2Address,
    partialArgumentBundle,
    wrapperCallDiagnostics,
    exactTransactionExecutionSupported: directMerklePrerequisitesSatisfied,
  });
  const directExecutionSimulation = directMerklePrerequisitesSatisfied && preparedContractCall
    ? await simulatePreparedContractCallSupport({ provider, preparedContractCall })
    : {
        attempted: false,
        supported: false,
        failureReason: null,
      };
  const wrapperPreparedCall = preparedContractCall?.multicallPreparation?.preparedWrapperCall || null;
  const wrapperExecutionSimulation = wrapperPreparedCall
    ? await simulatePreparedContractCallSupport({ provider, preparedContractCall: wrapperPreparedCall })
    : {
        attempted: false,
        supported: false,
        failureReason: null,
      };

  if (preparedContractCall?.multicallPreparation) {
    preparedContractCall.multicallPreparation.readyingPlan = wrapperCallDiagnostics.readyingPlan || null;
    preparedContractCall.multicallPreparation.signedBeaconUpdates = wrapperCallDiagnostics.signedBeaconUpdates || [];
    preparedContractCall.multicallPreparation.simulation = wrapperExecutionSimulation;
  }

  if (wrapperPreparedCall) {
    wrapperPreparedCall.sendTransactionSupported = wrapperExecutionSimulation.supported;
    wrapperPreparedCall.note = wrapperExecutionSimulation.supported
      ? 'This phase prepares the exact wrapper-assisted tryMulticallAndBuySubscription call data only. It does not send or broadcast any transaction.'
      : `The wrapper-assisted calldata is derivable, but a wrapped dry-run still reverts for this feed (${wrapperExecutionSimulation.failureReason || 'unknown error'}).`;
  }

  if (wrapperPreparedCall && wrapperExecutionSimulation.supported) {
    wrapperCallDiagnostics.wrapperCallSupported = true;
  } else if (wrapperPreparedCall && !wrapperExecutionSimulation.supported) {
    wrapperCallDiagnostics.wrapperCallPreparationSupported = false;
    wrapperCallDiagnostics.reason = `The wrapper readying sequence is derivable, but the wrapped dry-run still reverts (${wrapperExecutionSimulation.failureReason || 'unknown error'}).`;
    wrapperCallDiagnostics.blockers = [
      ...(wrapperCallDiagnostics.blockers || []),
      `Wrapped dry-run failed: ${wrapperExecutionSimulation.failureReason || 'unknown error'}`,
    ];
  }

  const exactTransactionExecutionSupported = directMerklePrerequisitesSatisfied && directExecutionSimulation.supported;
  if (preparedContractCall && directMerklePrerequisitesSatisfied && !directExecutionSimulation.supported) {
    preparedContractCall.sendTransactionSupported = false;
    preparedContractCall.note = directExecutionSimulation.failureReason
      ? `The exact buySubscription calldata is derivable from current public inputs, but a direct call simulation still reverts for this feed (${directExecutionSimulation.failureReason}).${wrapperExecutionSimulation.supported ? ' Use wrapper execution instead.' : ' Use browser-assisted funding instead.'}`
      : `The exact buySubscription calldata is derivable from current public inputs, but a direct call simulation still reverts for this feed.${wrapperExecutionSimulation.supported ? ' Use wrapper execution instead.' : ' Use browser-assisted funding instead.'}`;
  }
  const fundingExecutionClassification = classifyFundingExecution({
    chainState: exactMatch?.chainState,
    exactTransactionExecutionSupported,
    wrapperCallDiagnostics,
    unsupportedDiagnostics,
  });

  return {
    command: 'purchase-inputs',
    chain: {
      chainId,
      requested: chainInput || null,
      marketChainSlug: getMarketChainSlug(chainInput, chainId),
    },
    dapiName,
    dapiNameBytes32,
    communalProxy,
    pricingFile: {
      url: pricingFileUrl,
      exists: pricingResponse.ok,
      status: pricingResponse.status,
      merkleRoot: pricingResponse.json?.merkleRoot || null,
      matchesOnChainRegisteredRoot:
        pricingResponse.json?.merkleRoot && onChainRegisteredRoots?.dapiPricingMerkleRoot
          ? pricingResponse.json.merkleRoot === onChainRegisteredRoots.dapiPricingMerkleRoot
          : null,
    },
    availableSubscriptionOptions: pricingOptions,
    chosenSubscriptionOption,
    queueSubscriptionModel,
    chosenQueueEntry: chosenSubscriptionOption
      ? {
          sponsorWallet: queueSubscriptionModel.sponsorWallet,
          queuePriority:
            queueSubscriptionModel.queueEntries.find((entry) => entry.selected)?.queuePriority || null,
          deviationThresholdPercent: chosenSubscriptionOption.decodedUpdateParameters.deviationThresholdPercent,
          duration: chosenSubscriptionOption.duration,
          durationDays: chosenSubscriptionOption.durationDays,
          price: chosenSubscriptionOption.price,
          updateParameters: chosenSubscriptionOption.updateParameters,
        }
      : null,
    dapiManagement: {
      timestamp: activeDapiManagementMerkleTreeData.timestamp,
      signatures: activeDapiManagementMerkleTreeData.signatures,
      packageTreeHash: dapiManagementMerkleTreeData.hash,
      selectedTreeHash: activeDapiManagementMerkleTreeData.hash,
      selectedTreeSource: dapiManagementSourceSelection.selectedSource,
      selectedTreeReason: dapiManagementSourceSelection.reason,
      liveMarketTreeHash: liveDapiManagementMerkleTreeData?.hash || null,
      liveMarketBundleUrl: liveDapiManagementMerkleTreeData?.bundleUrl || null,
      liveMarketFetchError: liveDapiManagementFetchError ? liveDapiManagementFetchError.message : null,
      currentPublicDataFeedModel,
      onChainRegisteredMerkleRoot: onChainRegisteredRoots?.dapiManagementMerkleRoot || null,
      entry: dapiManagementEntry
        ? {
            entryIndex: dapiManagementEntry.entryIndex,
            dapiNameBytes32: dapiManagementEntry.dapiNameBytes32,
            dataFeedId: dapiManagementEntry.dataFeedId,
            sponsorWallet: dapiManagementEntry.sponsorWallet,
            leaf: dapiManagementEntry.leaf,
            leafHash: dapiManagementEntry.leafHash,
          }
        : null,
      merkleRoot: dapiManagementEntry?.merkleRoot || null,
      proof: dapiManagementEntry?.proof || null,
      proofPath: dapiManagementEntry?.proofPath || null,
      proofDerivableToday: Boolean(dapiManagementEntry?.proof?.length),
      proofMatchesMerkleRoot: dapiManagementEntry?.proofMatchesMerkleRoot || false,
      reconstructedRootMatchesPackageHash: dapiManagementEntry?.merkleRoot === dapiManagementMerkleTreeData.hash,
      reconstructedRootMatchesSelectedSourceHash: dapiManagementEntry?.merkleRoot === activeDapiManagementMerkleTreeData.hash,
      reconstructedRootMatchesOnChain:
        dapiManagementEntry?.merkleRoot && onChainRegisteredRoots?.dapiManagementMerkleRoot
          ? dapiManagementEntry.merkleRoot === onChainRegisteredRoots.dapiManagementMerkleRoot
          : null,
      derivedSponsorWallet,
    },
    targetContract: {
      api3MarketV2Address,
      communalProxy,
      likelyPurchaseMethod: wrapperCallDiagnostics.wrapperCallSupported
        ? 'tryMulticallAndBuySubscription'
        : 'buySubscription',
      directMethodAlternative: 'buySubscription',
      multicallAssumption: exactMatch?.chainState?.isActiveOnChain
        ? 'optional-and-now-exactly-derivable-as-empty-array'
        : unsupportedDiagnostics.marketActivationCoverage.activatableViaMarketContractPath
          ? 'possible-in-principle-but-not-exactly-derivable-from-public-inputs-for-inactive-feed'
          : 'blocked-upstream-before-wrapper-reconstruction-matters',
    },
    pricingProofBundle,
    exactMerkleDataBundle,
    directExecutionSimulation,
    wrapperCallDiagnostics,
    unsupportedDiagnostics,
    fundingExecutionClassification,
    exactTransactionExecutionSupported,
    sendTransactionSupported: exactTransactionExecutionSupported,
    preparedContractCall: preparedContractCall || {
      sendTransactionSupported: false,
      preparedButNotTransmitted: true,
      note: 'This phase does not send transactions. Contract call preparation is blocked until the missing prerequisites below are available.',
      targetContractAddress: api3MarketV2Address,
      functionName: 'buySubscription',
      functionSignature: 'buySubscription(bytes32,bytes32,address,bytes,uint256,uint256,bytes)',
      abiFragment:
        'function buySubscription(bytes32 dapiName, bytes32 dataFeedId, address sponsorWallet, bytes updateParameters, uint256 duration, uint256 price, bytes dapiManagementAndDapiPricingMerkleData) payable',
      multicallPreparation: wrapperCallDiagnostics,
      unsupportedDiagnostics,
    },
    partialArgumentBundle,
    blockers,
  };
}

function selectPreparedExecution(prepared, requestedMode = 'auto') {
  const normalizedMode = String(requestedMode || 'auto').trim().toLowerCase();
  const directPreparedCall = prepared.preparedContractCall || null;
  const wrapperPreparedCall = directPreparedCall?.multicallPreparation?.preparedWrapperCall || null;

  const directSupported = Boolean(directPreparedCall?.sendTransactionSupported !== false && directPreparedCall?.targetContractAddress && directPreparedCall?.calldata);
  const wrapperSupported = Boolean(wrapperPreparedCall?.sendTransactionSupported !== false && wrapperPreparedCall?.targetContractAddress && wrapperPreparedCall?.calldata);

  if (normalizedMode === 'direct') {
    return directSupported
      ? { mode: 'direct', preparedCall: directPreparedCall, availableModes: [
          ...(directSupported ? ['direct'] : []),
          ...(wrapperSupported ? ['wrapper'] : []),
        ] }
      : { mode: 'direct', preparedCall: null, availableModes: [
          ...(directSupported ? ['direct'] : []),
          ...(wrapperSupported ? ['wrapper'] : []),
        ], failureReason: 'Direct buySubscription execution is not supported for this feed.' };
  }

  if (normalizedMode === 'wrapper') {
    return wrapperSupported
      ? { mode: 'wrapper', preparedCall: wrapperPreparedCall, availableModes: [
          ...(directSupported ? ['direct'] : []),
          ...(wrapperSupported ? ['wrapper'] : []),
        ] }
      : { mode: 'wrapper', preparedCall: null, availableModes: [
          ...(directSupported ? ['direct'] : []),
          ...(wrapperSupported ? ['wrapper'] : []),
        ], failureReason: 'Wrapper execution is not supported for this feed.' };
  }

  if (directSupported) {
    return { mode: 'direct', preparedCall: directPreparedCall, availableModes: [
      ...(directSupported ? ['direct'] : []),
      ...(wrapperSupported ? ['wrapper'] : []),
    ] };
  }

  if (wrapperSupported) {
    return { mode: 'wrapper', preparedCall: wrapperPreparedCall, availableModes: [
      ...(directSupported ? ['direct'] : []),
      ...(wrapperSupported ? ['wrapper'] : []),
    ] };
  }

  return {
    mode: 'auto',
    preparedCall: null,
    availableModes: [],
    failureReason: 'No executable direct or wrapper call is available for this feed.',
  };
}

async function executeBuySubscription(options) {
  const prepared = await prepareContractCall(options);
  const submit = parseBooleanOption(options.submit, false);
  const deployCommunalProxyAfterBuy = parseBooleanOption(options.deployCommunalProxy, false);

  const classificationState = prepared.fundingExecutionClassification?.state;
  if (classificationState && classificationState !== 'executable' && classificationState !== 'not-needed') {
    return {
      command: 'execute-buy-subscription',
      chain: prepared.chain,
      dapiName: prepared.dapiName,
      dapiNameBytes32: prepared.dapiNameBytes32,
      communalProxy: prepared.communalProxy,
      targetContract: prepared.targetContract,
      sendTransactionSupported: prepared.sendTransactionSupported,
      exactTransactionExecutionSupported: prepared.exactTransactionExecutionSupported,
      fundingExecutionClassification: prepared.fundingExecutionClassification,
      preparedContractCall: prepared.preparedContractCall,
      selectedExecutionMode: null,
      availableExecutionModes: [],
      executionSummary: {
        requested: true,
        dryRun: !submit,
        attempted: false,
        simulated: false,
        submitted: false,
        completed: false,
        signerAddress: null,
        txHash: null,
        failureReason: `Execution blocked: funding classification is '${classificationState}'. ${prepared.fundingExecutionClassification?.reason || ''}`.trimEnd(),
      },
      transactionRequest: null,
      simulationCallResult: null,
      wrapperCallDiagnostics: prepared.wrapperCallDiagnostics,
      unsupportedDiagnostics: prepared.unsupportedDiagnostics,
      blockers: prepared.blockers,
      sourceCommand: 'prepare-contract-call',
    };
  }

  const executionSelection = selectPreparedExecution(prepared, options.executionMode);
  const executionTarget = executionSelection.preparedCall
    ? executionSelection.preparedCall
    : {
        sendTransactionSupported: false,
      };
  const { executionSummary, transactionRequest, callResult } = await executePreparedContractCall({
    preparedContractCall: executionTarget,
    rpcUrl: options.rpcUrl,
    privateKey: options.privateKey,
    submit,
    acknowledgement: options.acknowledgement,
    simulationFromAddress: options.simulationFromAddress,
  });

  let communalProxyDeployment = null;
  if (deployCommunalProxyAfterBuy) {
    const shouldAttemptProxyDeployment = submit
      ? executionSummary.submitted && executionSummary.failureReason === null
      : executionSummary.completed && executionSummary.failureReason === null;

    if (shouldAttemptProxyDeployment || prepared.fundingExecutionClassification?.state === 'not-needed') {
      communalProxyDeployment = await deployCommunalProxy({
        ...options,
        dapiName: prepared.dapiName,
        submit: submit ? 'true' : 'false',
      });
    }
  }

  if (executionSelection.failureReason && !executionSummary.failureReason) {
    executionSummary.failureReason = executionSelection.failureReason;
  }

  return {
    command: 'execute-buy-subscription',
    chain: prepared.chain,
    dapiName: prepared.dapiName,
    dapiNameBytes32: prepared.dapiNameBytes32,
    communalProxy: prepared.communalProxy,
    targetContract: prepared.targetContract,
    sendTransactionSupported: prepared.sendTransactionSupported,
    exactTransactionExecutionSupported: prepared.exactTransactionExecutionSupported,
    fundingExecutionClassification: prepared.fundingExecutionClassification,
    preparedContractCall: prepared.preparedContractCall,
    selectedExecutionMode: executionSelection.mode,
    availableExecutionModes: executionSelection.availableModes,
    executionSummary,
    communalProxyDeployment,
    transactionRequest: transactionRequest
      ? {
          to: transactionRequest.to,
          data: transactionRequest.data,
          value: transactionRequest.value.toString(),
          from: transactionRequest.from,
        }
      : null,
    simulationCallResult: callResult,
    wrapperCallDiagnostics: prepared.wrapperCallDiagnostics,
    unsupportedDiagnostics: prepared.unsupportedDiagnostics,
    blockers: prepared.blockers,
    sourceCommand: 'prepare-contract-call',
  };
}

async function prepareContractCall(options) {
  const purchasePlan = await purchaseInputs(options);

  return {
    command: 'prepare-contract-call',
    chain: purchasePlan.chain,
    dapiName: purchasePlan.dapiName,
    dapiNameBytes32: purchasePlan.dapiNameBytes32,
    communalProxy: purchasePlan.communalProxy,
    queueSubscriptionModel: purchasePlan.queueSubscriptionModel,
    chosenQueueEntry: purchasePlan.chosenQueueEntry,
    targetContract: purchasePlan.targetContract,
    sendTransactionSupported: purchasePlan.sendTransactionSupported,
    preparedButNotTransmitted: true,
    preparedContractCall: purchasePlan.preparedContractCall,
    wrapperCallDiagnostics: purchasePlan.wrapperCallDiagnostics,
    unsupportedDiagnostics: purchasePlan.unsupportedDiagnostics,
    fundingExecutionClassification: purchasePlan.fundingExecutionClassification,
    exactTransactionExecutionSupported: purchasePlan.exactTransactionExecutionSupported,
    blockers: purchasePlan.blockers,
    sourceCommand: 'purchase-inputs',
  };
}

async function runCli(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  const command = args._[0] || 'resolve';

  if (command === 'help' || args.help) {
    printUsage();
    return;
  }

  if (command === 'resolve') {
    const result = await resolveFeed(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'discover') {
    const result = await discoverFeeds(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'ensure-active') {
    const result = await ensureActive(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'prepare-activation' || command === 'prepare-market-flow') {
    const result = await prepareActivation(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'browser-plan') {
    const result = await browserPlan(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'contract-plan' || command === 'prepare-contract-activation') {
    const result = await contractPlan(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'coverage-audit') {
    const result = await coverageAudit(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'coverage-matrix') {
    const result = await coverageMatrix(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'supported-chains') {
    const result = await supportedChains(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'queue-plan' || command === 'feed-activation-plan') {
    const result = await queuePlan(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'purchase-inputs' || command === 'trace-purchase-inputs') {
    const result = await purchaseInputs(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'prepare-contract-call' || command === 'prepare-buy-subscription') {
    const result = await prepareContractCall(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'execute-buy-subscription') {
    const result = await executeBuySubscription(args);
    outputResult(command, result, args);
    return;
  }

  if (command === 'deploy-communal-proxy') {
    const result = await deployCommunalProxy(args);
    outputResult(command, result, args);
    return;
  }

  throw new Error(`Unsupported command: ${command}`);
}

module.exports = {
  CHAIN_ALIASES,
  buildActivationMetadata,
  buildContractActivationPlan,
  buildBrowserPlan,
  buildCatalogIndex,
  buildMarketExecutionPlan,
  buildMarketUrls,
  buildWrapperReadyingPlan,
  browserPlan,
  coverageAudit,
  coverageMatrix,
  contractPlan,
  queuePlan,
  purchaseInputs,
  supportedChains,
  buildWrapperCallDiagnostics,
  decodeDataFeedDetails,
  deriveCurrentPublicDataFeedModel,
  decodeUpdateParameters,
  discoverFeeds,
  ensureActive,
  extractLiveDapiManagementMerkleTreeDataFromBundleSource,
  fetchActiveFeeds,
  getDefaultAddresses,
  getMarketChainSlug,
  findLiteralExactMatches,
  findNormalizedExactMatches,
  normalizeChainId,
  normalizeDapiName,
  normalizeLiteralDapiName,
  parseArgs,
  prepareActivation,
  prepareContractCall,
  deployCommunalProxy,
  executePreparedContractCall,
  executeBuySubscription,
  classifyFundingExecution,
  selectPreferredExactMatches,
  selectPreferredDapiManagementMerkleTreeData,
  selectPreparedExecution,
  printUsage,
  resolveFeed,
  runCli,
  slugifyDapiName,
};
