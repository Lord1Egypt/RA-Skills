#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {
  JsonRpcProvider,
  Wallet,
  Contract,
  MaxUint256,
  parseUnits,
  formatUnits,
  formatEther,
  isAddress,
} = require('ethers');

const erc20Abi = [
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address,address) view returns (uint256)',
  'function approve(address,uint256) returns (bool)',
  'function decimals() view returns (uint8)'
];

const borrowVaultAbi = [
  'function repay(uint256,address) returns (uint256)',
  'function borrow(uint256,address) returns (uint256)',
  'function debtOf(address) view returns (uint256)',
  'function accountLiquidity(address,bool) view returns (uint256,uint256)',
  'function cash() view returns (uint256)'
];

const collateralVaultAbi = [
  'function deposit(uint256,address) returns (uint256)',
  'function balanceOf(address) view returns (uint256)',
  'function convertToAssets(uint256) view returns (uint256)'
];

const wrappedNativeAbi = [
  'function deposit() payable',
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address,address) view returns (uint256)',
  'function approve(address,uint256) returns (bool)',
  'function decimals() view returns (uint8)'
];

const routerAbi = [
  'function exactInputSingle((address tokenIn,address tokenOut,uint24 fee,address recipient,uint256 amountIn,uint256 amountOutMinimum,uint160 sqrtPriceLimitX96)) payable returns (uint256 amountOut)'
];

const evcAbi = [
  'function enableCollateral(address,address)',
  'function disableCollateral(address,address)',
  'function getCollaterals(address) view returns (address[] memory)',
  'function enableController(address,address)',
  'function disableController(address,address)'
];

const LIVE_ACKNOWLEDGEMENT = ['I', 'UNDERSTAND', 'THIS', 'WILL', 'SEND', 'TRANSACTIONS'].join('_');

function usage() {
  console.log([
    'Usage:',
    '  node scripts/evk_live_borrow_proof.js --config <path> [--live]',
    '',
    'Modes:',
    '  default   Preview only, no transactions sent',
    '  --live    Send transactions using signerEnvName from config',
    '',
    'Preview mode can run with only accountAddress set in the config.',
    'Live mode requires process.env[signerEnvName].',
    'Legacy configs may still use privateKeyEnv.',
    'Live mode also requires config.operatorAck to match the script\'s required live-send acknowledgement phrase.',
    'Legacy configs may still use liveAcknowledgement.'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = { live: false, configPath: null };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      args.help = true;
    } else if (arg === '--live') {
      args.live = true;
    } else if (arg === '--config') {
      args.configPath = argv[i + 1];
      i += 1;
    }
  }
  return args;
}

function fail(message) {
  throw new Error(message);
}

function requireAddress(label, value) {
  if (!value || !isAddress(value)) {
    fail(`Invalid ${label}: ${value}`);
  }
}

function loadConfig(configPath) {
  if (!configPath) fail('Missing --config <path>');
  const absolutePath = path.resolve(process.cwd(), configPath);
  const parsed = JSON.parse(fs.readFileSync(absolutePath, 'utf8'));

  if (!parsed.rpcUrl) fail('config.rpcUrl is required');
  if (!parsed.tokens) fail('config.tokens is required');
  if (!parsed.vaults) fail('config.vaults is required');
  if (!parsed.evc) fail('config.evc is required');
  if (!parsed.actions) fail('config.actions is required');

  requireAddress('tokens.wrappedNative.address', parsed.tokens.wrappedNative?.address);
  requireAddress('tokens.borrowAsset.address', parsed.tokens.borrowAsset?.address);
  requireAddress('tokens.collateralAsset.address', parsed.tokens.collateralAsset?.address);
  requireAddress('vaults.borrowVault.address', parsed.vaults.borrowVault?.address);
  requireAddress('vaults.collateralVault.address', parsed.vaults.collateralVault?.address);
  requireAddress('evc.address', parsed.evc.address);

  return { absolutePath, parsed };
}

function parseAmount(amount, decimals, label) {
  if (amount === undefined || amount === null) {
    fail(`Missing amount for ${label}`);
  }
  return parseUnits(String(amount), decimals);
}

function serialize(value) {
  return JSON.stringify(value, (_, inner) => (typeof inner === 'bigint' ? inner.toString() : inner), 2);
}

function log(label, data) {
  if (data === undefined) {
    console.log(`\n## ${label}`);
    return;
  }
  console.log(`\n## ${label}`);
  console.log(typeof data === 'string' ? data : serialize(data));
}

function makeToken(runner, config) {
  return new Contract(config.address, erc20Abi, runner);
}

async function sendOrPreview({ live, contract, fn, args = [], overrides = {}, label }) {
  if (!live) {
    log('preview', {
      label,
      target: contract.target,
      fn,
      args,
      overrides,
    });
    return null;
  }

  const tx = await contract[fn](...args, overrides);
  log('submitted', { label, target: contract.target, fn, txHash: tx.hash });
  const receipt = await tx.wait();
  log('confirmed', { label, txHash: tx.hash, blockNumber: receipt.blockNumber, status: receipt.status });
  return receipt;
}

async function ensureApproval({ live, token, owner, spender, amount, label }) {
  const allowance = await token.allowance(owner, spender);
  if (allowance >= amount) {
    log('approval-ok', { label, spender, allowance: allowance.toString(), needed: amount.toString() });
    return;
  }
  await sendOrPreview({ live, contract: token, fn: 'approve', args: [spender, MaxUint256], label });
}

async function maybeWrapNative({ live, wrappedNative, amount, label }) {
  if (!amount || amount <= 0n) return;
  await sendOrPreview({ live, contract: wrappedNative, fn: 'deposit', args: [], overrides: { value: amount }, label });
}

async function runSwap({ live, runner, walletAddress, swapConfig, label }) {
  if (!swapConfig?.enabled) return;

  requireAddress(`${label}.routerAddress`, swapConfig.routerAddress);
  requireAddress(`${label}.tokenIn.address`, swapConfig.tokenIn?.address);
  requireAddress(`${label}.tokenOut.address`, swapConfig.tokenOut?.address);

  const tokenIn = makeToken(runner, swapConfig.tokenIn);
  const router = new Contract(swapConfig.routerAddress, routerAbi, runner);
  const amountIn = parseAmount(swapConfig.amountIn || '0', swapConfig.tokenIn.decimals, `${label}.amountIn`);
  const amountOutMinimum = parseAmount(swapConfig.amountOutMinimum || '0', swapConfig.tokenOut.decimals, `${label}.amountOutMinimum`);
  const wrapNativeAmount = parseAmount(swapConfig.wrapNativeAmount || '0', 18, `${label}.wrapNativeAmount`);

  if (swapConfig.tokenIn.isWrappedNative && wrapNativeAmount > 0n) {
    const wrappedNative = new Contract(swapConfig.tokenIn.address, wrappedNativeAbi, runner);
    await maybeWrapNative({ live, wrappedNative, amount: wrapNativeAmount, label: `${label}:wrap-native` });
  }

  if (amountIn <= 0n) {
    log('swap-skip', { label, reason: 'amountIn is zero' });
    return;
  }

  await ensureApproval({
    live,
    token: tokenIn,
    owner: walletAddress,
    spender: swapConfig.routerAddress,
    amount: amountIn,
    label: `${label}:approve-router`,
  });

  await sendOrPreview({
    live,
    contract: router,
    fn: 'exactInputSingle',
    args: [[
      swapConfig.tokenIn.address,
      swapConfig.tokenOut.address,
      Number(swapConfig.fee || 0),
      walletAddress,
      amountIn,
      amountOutMinimum,
      0,
    ]],
    label,
  });
}

async function getState({ provider, walletAddress, nativeWrappedConfig, wrappedNative, borrowAsset, collateralAsset, borrowVault, collateralVault, evc }) {
  const collateralShares = await collateralVault.balanceOf(walletAddress);
  const collaterals = await evc.getCollaterals(walletAddress);
  const debt = await borrowVault.debtOf(walletAddress);
  const cash = await borrowVault.cash();
  const borrowAssetDecimals = await borrowAsset.decimals();
  const collateralAssetDecimals = await collateralAsset.decimals();
  let liquidity;

  try {
    const [collateralValue, liabilityValue] = await borrowVault.accountLiquidity(walletAddress, false);
    liquidity = {
      collateralValue: collateralValue.toString(),
      liabilityValue: liabilityValue.toString(),
    };
  } catch (error) {
    liquidity = { error: error.message };
  }

  return {
    native: formatEther(await provider.getBalance(walletAddress)),
    wrappedNative: formatUnits(await wrappedNative.balanceOf(walletAddress), nativeWrappedConfig.decimals),
    borrowAsset: formatUnits(await borrowAsset.balanceOf(walletAddress), borrowAssetDecimals),
    collateralAsset: formatUnits(await collateralAsset.balanceOf(walletAddress), collateralAssetDecimals),
    debt: formatUnits(debt, borrowAssetDecimals),
    cash: formatUnits(cash, borrowAssetDecimals),
    collateralVaultShares: collateralShares.toString(),
    collateralVaultAssets: formatUnits(await collateralVault.convertToAssets(collateralShares), collateralAssetDecimals),
    collaterals,
    liquidity,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }

  const { parsed: config, absolutePath } = loadConfig(args.configPath);
  const provider = new JsonRpcProvider(config.rpcUrl);
  const signerEnvName = config.signerEnvName || config.privateKeyEnv || null;
  const operatorAck = config.operatorAck || config.liveAcknowledgement || null;
  const privateKey = signerEnvName ? process.env[signerEnvName] : null;

  if (args.live && !privateKey) {
    fail(`Missing environment variable ${signerEnvName || '(unset signerEnvName)' } for live mode`);
  }

  if (args.live && operatorAck !== LIVE_ACKNOWLEDGEMENT) {
    fail('Live mode requires config.operatorAck to match the required live-send acknowledgement phrase');
  }

  const signer = privateKey ? new Wallet(privateKey, provider) : null;
  const walletAddress = signer ? await signer.getAddress() : config.accountAddress;
  requireAddress('accountAddress', walletAddress);

  if (args.live && config.accountAddress && signer && config.accountAddress.toLowerCase() !== walletAddress.toLowerCase()) {
    fail(`Signer address ${walletAddress} does not match config.accountAddress ${config.accountAddress}`);
  }

  const runner = signer && args.live ? signer : provider;

  const wrappedNative = new Contract(config.tokens.wrappedNative.address, wrappedNativeAbi, runner);
  const borrowAsset = makeToken(runner, config.tokens.borrowAsset);
  const collateralAsset = makeToken(runner, config.tokens.collateralAsset);
  const borrowVault = new Contract(config.vaults.borrowVault.address, borrowVaultAbi, runner);
  const collateralVault = new Contract(config.vaults.collateralVault.address, collateralVaultAbi, runner);
  const evc = new Contract(config.evc.address, evcAbi, runner);

  log('context', {
    configPath: absolutePath,
    chainLabel: config.chainLabel || null,
    mode: args.live ? 'live' : 'preview',
    walletAddress,
    borrowVault: config.vaults.borrowVault,
    collateralVault: config.vaults.collateralVault,
    evcAddress: config.evc.address,
    actions: config.actions,
  });

  const before = await getState({
    provider,
    walletAddress,
    nativeWrappedConfig: config.tokens.wrappedNative,
    wrappedNative,
    borrowAsset,
    collateralAsset,
    borrowVault,
    collateralVault,
    evc,
  });
  log('before', before);

  const debtRaw = await borrowVault.debtOf(walletAddress);
  const borrowAssetDecimals = await borrowAsset.decimals();
  const collateralAssetDecimals = await collateralAsset.decimals();

  if (config.actions.repayExistingDebt && debtRaw > 0n) {
    let borrowBalance = await borrowAsset.balanceOf(walletAddress);

    if (borrowBalance < debtRaw && config.repayTopUp?.enabled) {
      if (config.repayTopUp.mode !== 'wrap-native') {
        fail('repayTopUp currently supports only mode="wrap-native"');
      }
      if (config.tokens.borrowAsset.address.toLowerCase() !== config.tokens.wrappedNative.address.toLowerCase()) {
        fail('repayTopUp.wrap-native requires borrowAsset to equal wrappedNative');
      }
      const topUpAmount = parseAmount(config.repayTopUp.amount, config.tokens.wrappedNative.decimals, 'repayTopUp.amount');
      await maybeWrapNative({ live: args.live, wrappedNative, amount: topUpAmount, label: 'repay-top-up' });
      borrowBalance = await borrowAsset.balanceOf(walletAddress);
    }

    if (borrowBalance < debtRaw && config.repaySwap?.enabled) {
      await runSwap({
        live: args.live,
        runner,
        walletAddress,
        swapConfig: config.repaySwap,
        label: 'repay-swap',
      });
      borrowBalance = await borrowAsset.balanceOf(walletAddress);
    }

    if (borrowBalance < debtRaw) {
      fail(`Borrow asset balance ${borrowBalance.toString()} is still below debt ${debtRaw.toString()} after configured top-ups`);
    }

    await ensureApproval({
      live: args.live,
      token: borrowAsset,
      owner: walletAddress,
      spender: config.vaults.borrowVault.address,
      amount: debtRaw,
      label: 'approve-repay',
    });

    await sendOrPreview({
      live: args.live,
      contract: borrowVault,
      fn: 'repay',
      args: [MaxUint256, walletAddress],
      label: 'repay-old-debt',
    });
  }

  if (config.collateralSwap?.enabled) {
    await runSwap({
      live: args.live,
      runner,
      walletAddress,
      swapConfig: config.collateralSwap,
      label: 'collateral-swap',
    });
  }

  const walletCollateralBalance = await collateralAsset.balanceOf(walletAddress);
  if (config.actions.depositFullCollateralBalance && walletCollateralBalance > 0n) {
    await ensureApproval({
      live: args.live,
      token: collateralAsset,
      owner: walletAddress,
      spender: config.vaults.collateralVault.address,
      amount: walletCollateralBalance,
      label: 'approve-collateral-deposit',
    });

    await sendOrPreview({
      live: args.live,
      contract: collateralVault,
      fn: 'deposit',
      args: [walletCollateralBalance, walletAddress],
      label: 'deposit-collateral',
    });
  }

  const currentCollaterals = (await evc.getCollaterals(walletAddress)).map((entry) => entry.toLowerCase());
  for (const stale of config.vaults.disableCollateral || []) {
    if (!stale?.address) continue;
    if (currentCollaterals.includes(stale.address.toLowerCase())) {
      await sendOrPreview({
        live: args.live,
        contract: evc,
        fn: 'disableCollateral',
        args: [walletAddress, stale.address],
        label: `disable-collateral:${stale.label || stale.address}`,
      });
    }
  }

  const refreshedCollaterals = (await evc.getCollaterals(walletAddress)).map((entry) => entry.toLowerCase());
  if (!refreshedCollaterals.includes(config.vaults.collateralVault.address.toLowerCase())) {
    await sendOrPreview({
      live: args.live,
      contract: evc,
      fn: 'enableCollateral',
      args: [walletAddress, config.vaults.collateralVault.address],
      label: `enable-collateral:${config.vaults.collateralVault.label || config.vaults.collateralVault.address}`,
    });
  }

  for (const staleController of config.evc.controllersToDisable || []) {
    if (!staleController?.address) continue;
    await sendOrPreview({
      live: args.live,
      contract: evc,
      fn: 'disableController',
      args: [walletAddress, staleController.address],
      label: `disable-controller:${staleController.label || staleController.address}`,
    });
  }

  if (config.evc.enableController) {
    await sendOrPreview({
      live: args.live,
      contract: evc,
      fn: 'enableController',
      args: [walletAddress, config.vaults.borrowVault.address],
      label: `enable-controller:${config.vaults.borrowVault.label || config.vaults.borrowVault.address}`,
    });
  }

  let liquidity;
  try {
    const [collateralValue, liabilityValue] = await borrowVault.accountLiquidity(walletAddress, false);
    liquidity = {
      collateralValue: collateralValue.toString(),
      liabilityValue: liabilityValue.toString(),
      cash: formatUnits(await borrowVault.cash(), borrowAssetDecimals),
      enabledCollaterals: await evc.getCollaterals(walletAddress),
      collateralVaultAssets: formatUnits(
        await collateralVault.convertToAssets(await collateralVault.balanceOf(walletAddress)),
        collateralAssetDecimals,
      ),
    };
  } catch (error) {
    liquidity = { error: error.message };
  }
  log('liquidity-before-borrow', liquidity);

  const borrowAmount = parseAmount(config.actions.borrowAmount, borrowAssetDecimals, 'actions.borrowAmount');
  await sendOrPreview({
    live: args.live,
    contract: borrowVault,
    fn: 'borrow',
    args: [borrowAmount, walletAddress],
    label: 'borrow-proof',
  });

  if (!args.live) {
    log('preview-note', 'Preview mode does not mutate state. Review the planned calls, then rerun with --live for a real canary.');
    return;
  }

  const after = await getState({
    provider,
    walletAddress,
    nativeWrappedConfig: config.tokens.wrappedNative,
    wrappedNative,
    borrowAsset,
    collateralAsset,
    borrowVault,
    collateralVault,
    evc,
  });
  log('after', after);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
