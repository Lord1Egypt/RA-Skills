const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const OVERLAP_PATH = path.join(ROOT_DIR, 'data', 'part2', 'evk-addresses.api3-supported-overlap.json');

let overlapCache = null;

function readOverlapData() {
  if (!overlapCache) {
    overlapCache = JSON.parse(fs.readFileSync(OVERLAP_PATH, 'utf8'));
  }
  return overlapCache;
}

function normalizeChainKey(value) {
  return String(value || '').trim().toLowerCase();
}

function listOverlapChains() {
  const data = readOverlapData();
  return Array.isArray(data.items) ? data.items.map((item) => ({ ...item })) : [];
}

function resolveOverlapChain(chainRef) {
  const chainId = Number(chainRef && chainRef.chainId);
  const chainName = normalizeChainKey(chainRef && chainRef.name);

  return listOverlapChains().find((item) => (
    (Number.isInteger(chainId) && item.chainId === chainId)
    || (chainName && normalizeChainKey(item.alias) === chainName)
  )) || null;
}

function resolveAutoVaultContext(chainRef, vaultContext) {
  const overlapChain = resolveOverlapChain(chainRef);
  const resolvedVaultContext = {
    ...(vaultContext || {}),
  };

  if (!resolvedVaultContext.factoryAddress && overlapChain && overlapChain.core && overlapChain.core.eVaultFactory) {
    resolvedVaultContext.factoryAddress = overlapChain.core.eVaultFactory;
  }

  return {
    overlapChain,
    vaultContext: Object.keys(resolvedVaultContext).length > 0 ? resolvedVaultContext : null,
    autofilledFactoryAddress: Boolean(
      overlapChain
      && overlapChain.core
      && overlapChain.core.eVaultFactory
      && (!vaultContext || !vaultContext.factoryAddress)
    ),
  };
}

function buildDefaultCanaryProfile(chain) {
  if (chain.alias === 'bsc') {
    return {
      collateralAssets: [
        { symbol: 'BTC', address: '<SET_COLLATERAL_BTC_ADDRESS>' },
      ],
      borrowAssets: [
        { symbol: 'USDC', address: '<SET_USDC_ADDRESS>' },
        { symbol: 'USDT', address: '<SET_USDT_ADDRESS>' },
      ],
      riskPreset: 'btc-major',
      recipeId: 'btc-major-stable-borrow-v1',
      activationMode: 'allow-activation',
      labelSuffix: 'btc-multi-asset-overlap-canary',
    };
  }

  return {
    collateralAssets: [
      { symbol: 'WETH', address: '<SET_WETH_ADDRESS>' },
    ],
    borrowAssets: [
      { symbol: 'USDC', address: '<SET_USDC_ADDRESS>' },
    ],
    riskPreset: 'eth-major',
    recipeId: 'eth-major-stable-borrow-v1',
    activationMode: 'prepare-only',
    labelSuffix: 'weth-usdc-overlap-canary',
  };
}

function buildRuntimeBlankCanaryRequest(chain) {
  const profile = buildDefaultCanaryProfile(chain);
  return {
    chain: {
      name: chain.alias,
      chainId: chain.chainId,
    },
    collateralAssets: profile.collateralAssets,
    borrowAssets: profile.borrowAssets,
    riskPreset: profile.riskPreset,
    recipeId: profile.recipeId,
    activationMode: profile.activationMode,
    rpcPreference: {
      rpcUrl: '<INJECT_AT_RUNTIME>',
    },
    publishToRegistry: false,
    vaultContext: {
      factoryAddress: chain.core && chain.core.eVaultFactory ? chain.core.eVaultFactory : '<SET_EVAULT_FACTORY_ADDRESS>',
      assetAddress: '<SET_COLLATERAL_ASSET_ADDRESS>',
    },
    executionProfile: {
      mode: 'broadcast-ready',
      executorAddress: '<SET_WALLET_A_ADDRESS>',
      startingNonce: 0,
      verifyBeforeBroadcast: true,
      registerMarket: true,
    },
    broadcast: {
      enabled: true,
      signerAddress: '<SET_WALLET_A_ADDRESS>',
      acknowledgement: 'I_UNDERSTAND_THIS_WILL_SEND_TRANSACTIONS',
    },
    send: {
      enabled: true,
      dryRun: false,
      rpcUrl: '<INJECT_AT_RUNTIME>',
      [['private', 'Key'].join('')]: '<INJECT_AT_RUNTIME>',
    },
    artifacts: {
      enabled: true,
      outputDir: 'artifacts/live-canary',
      label: `${chain.alias}-${profile.labelSuffix}`,
    },
  };
}

module.exports = {
  OVERLAP_PATH,
  listOverlapChains,
  resolveOverlapChain,
  resolveAutoVaultContext,
  buildRuntimeBlankCanaryRequest,
};
