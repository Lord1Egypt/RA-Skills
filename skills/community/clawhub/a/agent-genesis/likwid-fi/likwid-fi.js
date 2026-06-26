/**
 * likwid-fi.js — Likwid.fi Protocol Universal Skill
 *
 * Standalone DeFi interaction toolkit for the Likwid Protocol.
 * Supports EOA and ERC-4337 Smart Account execution.
 * No dependency on agent-genesis — fully independent.
 *
 * Commands:
 *   setup <network> <keyFilePath>
 *   account
 *   pools
 *   quote <poolIndex> <direction> <amount>
 *   swap <poolIndex> <direction> <amount> [slippage]
 */

const {
  createPublicClient,
  createWalletClient,
  http,
  parseUnits,
  formatUnits,
  encodeFunctionData,
  keccak256,
  encodeAbiParameters,
  parseAbi,
  getAddress,
} = require("viem");
const { signAuthorization } = require("viem/actions");
const { sepolia, mainnet, base } = require("viem/chains");
const { privateKeyToAccount } = require("viem/accounts");
const fs = require("fs");
const path = require("path");
const os = require("os");

// ======================= PATHS =======================

const CONFIG_FILE = path.join(__dirname, "config.json");
const POOLS_DIR = path.join(__dirname, "pools");
const ABI_DIR = path.join(__dirname, "abi");
const REMOTE_POOLS_BASE_URL = "https://likwid.fi/agent-pools";
const REMOTE_FETCH_TIMEOUT_MS = 3000;

// ======================= CHAIN MAP =======================

const CHAINS = {
  sepolia: sepolia,
  ethereum: mainnet,
  base: base,
};

// ======================= NATIVE TOKEN =======================

const NATIVE_ADDRESS = "0x0000000000000000000000000000000000000000";

// ======================= ABI FRAGMENTS =======================

const ERC20_ABI = parseAbi([
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function balanceOf(address account) external view returns (uint256)",
]);

// ======================= HELPERS =======================

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) return null;
  return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf8"));
}

function saveConfig(cfg) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
}

function loadCachedNetworkConfig(network) {
  const file = path.join(POOLS_DIR, `${network}.json`);
  if (!fs.existsSync(file)) return null;
  try { return JSON.parse(fs.readFileSync(file, "utf8")); }
  catch { return null; }
}

async function fetchRemoteConfig(network) {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REMOTE_FETCH_TIMEOUT_MS);
    const res = await fetch(`${REMOTE_POOLS_BASE_URL}/${network}.json`, { signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

function loadUserOverrides(network) {
  const file = path.join(POOLS_DIR, `${network}.local.json`);
  if (!fs.existsSync(file)) return { tokens: {}, pools: {} };
  try { return JSON.parse(fs.readFileSync(file, "utf8")); }
  catch { return { tokens: {}, pools: {} }; }
}

function mergeConfigs(baseConfig, userOverrides) {
  const merged = JSON.parse(JSON.stringify(baseConfig));

  // Merge tokens: add user tokens that don't exist in base
  if (userOverrides.tokens) {
    for (const [symbol, token] of Object.entries(userOverrides.tokens)) {
      if (!merged.tokens[symbol]) {
        merged.tokens[symbol] = token;
      }
    }
  }

  // Merge pools: add user pools/tiers that don't exist in base
  if (userOverrides.pools) {
    for (const [pairKey, tiers] of Object.entries(userOverrides.pools)) {
      if (!merged.pools[pairKey]) {
        merged.pools[pairKey] = tiers;
      } else {
        for (const tier of tiers) {
          const exists = merged.pools[pairKey].some(p => p.fee === tier.fee && p.marginFee === tier.marginFee);
          if (!exists) merged.pools[pairKey].push(tier);
        }
      }
      merged.pools[pairKey].sort((a, b) => a.fee - b.fee);
    }
  }

  return merged;
}

async function loadNetworkConfig(network) {
  const cached = loadCachedNetworkConfig(network);
  const remote = await fetchRemoteConfig(network);

  if (remote) {
    // Update local cache with remote data
    fs.mkdirSync(POOLS_DIR, { recursive: true });
    const cacheFile = path.join(POOLS_DIR, `${network}.json`);
    fs.writeFileSync(cacheFile, JSON.stringify(remote, null, 2) + "\n");
  } else if (cached) {
    console.log(`> Note: Using cached pool config (remote unavailable)`);
  }

  const base = remote || cached;
  if (!base) {
    console.log(`> ERROR: Network config not found and remote is unreachable.`);
    if (fs.existsSync(POOLS_DIR)) {
      console.log(`> Available cached networks: ${fs.readdirSync(POOLS_DIR).filter(f => f.endsWith(".json") && !f.endsWith(".local.json")).map(f => f.replace(".json", "")).join(", ")}`);
    }
    return null;
  }

  const userOverrides = loadUserOverrides(network);
  return mergeConfigs(base, userOverrides);
}

function loadABI(name) {
  const file = path.join(ABI_DIR, `${name}.json`);
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function expandHome(p) {
  if (p.startsWith("~/")) return path.join(os.homedir(), p.slice(2));
  return p;
}

function collapseHome(p) {
  const home = os.homedir();
  if (p.startsWith(home + "/")) return "~" + p.slice(home.length);
  return p;
}

function readPrivateKey(keyFilePath) {
  const resolved = path.resolve(expandHome(keyFilePath));
  if (!fs.existsSync(resolved)) {
    console.log(`> ERROR: Private key file not found: ${resolved}`);
    return null;
  }
  let raw = fs.readFileSync(resolved, "utf8").trim();
  // Support JSON wallet files (e.g., agent-genesis format)
  try {
    const json = JSON.parse(raw);
    if (json.privateKey) raw = json.privateKey;
  } catch (_) {}
  if (!raw.startsWith("0x")) raw = "0x" + raw;
  return raw;
}

function computePoolId(poolKey) {
  return keccak256(
    encodeAbiParameters(
      [
        { name: "currency0", type: "address" },
        { name: "currency1", type: "address" },
        { name: "fee", type: "uint24" },
        { name: "marginFee", type: "uint24" },
      ],
      [poolKey.currency0.address, poolKey.currency1.address, poolKey.fee, poolKey.marginFee],
    ),
  );
}

function isNative(address) {
  return address.toLowerCase() === NATIVE_ADDRESS.toLowerCase();
}

async function fetchLiquidityPositions(chainId, owner, poolId) {
  const url = `https://api.likwid.fi/v1/margin/pool/liquidity/list?chainId=${chainId}&page=1&pageSize=5&owner=${owner}&poolId=${poolId}`;
  try {
    const res = await fetch(url);
    if (!res.ok) return [];
    const json = await res.json();
    return json.data?.items || json.items || [];
  } catch (e) {
    console.log(`> Warning: Could not query positions API: ${e.message}`);
    return [];
  }
}

async function fetchMarginPositions(chainId, owner, poolId) {
  const url = `https://api.likwid.fi/v1/margin/position/list?borrow=false&burned=false&chainId=${chainId}&page=1&pageSize=100&owner=${owner}&poolId=${poolId}`;
  try {
    const res = await fetch(url);
    if (!res.ok) return [];
    const json = await res.json();
    return json.data?.items || json.items || [];
  } catch (e) {
    console.log(`> Warning: Could not query margin positions API: ${e.message}`);
    return [];
  }
}

function resolveRpc(config, networkConfig) {
  if (process.env.RPC_URL) return http(process.env.RPC_URL);
  if (networkConfig.rpc) return http(networkConfig.rpc);
  return http();
}

// ======================= BUNDLER HELPERS =======================

function resolveBundlerTransport(networkConfig) {
  const url = process.env.BUNDLER_URL || networkConfig.bundlerUrl;
  return http(url);
}

function buildPaymasterMiddleware(networkConfig) {
  if (process.env.LIKWID_NO_PAYMASTER === "1") return undefined;
  const addr = networkConfig.paymaster;
  if (!addr) return undefined;
  const stub = {
    paymaster: addr,
    paymasterData: "0x",
    verificationGasLimit: 600000n,
    paymasterVerificationGasLimit: 600000n,
    paymasterPostOpGasLimit: 600000n,
  };
  return {
    getPaymasterStubData: async () => stub,
    getPaymasterData: async () => stub,
  };
}

// ======================= CLIENT SETUP =======================

function createClients(config, networkConfig) {
  const privateKey = readPrivateKey(config.keyFilePath);
  if (!privateKey) return null;

  const chain = CHAINS[config.network];
  const transport = resolveRpc(config, networkConfig);
  const account = privateKeyToAccount(privateKey);

  const publicClient = createPublicClient({ chain, transport });
  const walletClient = createWalletClient({ account, chain, transport });

  return { publicClient, walletClient, account, chain };
}

async function resolveContext() {
  const config = loadConfig();
  if (!config) { console.log(`> ERROR: Not configured. Run setup first.`); return null; }

  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return null;

  const privateKey = readPrivateKey(config.keyFilePath);
  if (!privateKey) return null;

  const eoaAccount = privateKeyToAccount(privateKey);
  const chain = CHAINS[config.network];
  const publicClient = createPublicClient({ chain, transport: resolveRpc(config, netConfig) });

  // With EIP-7702, EOA and Smart Account share the same address
  const senderAddress = eoaAccount.address;

  return { config, netConfig, eoaAccount, publicClient, senderAddress };
}

async function getSmartAccount(config, networkConfig, eoaAccount) {
  const { toSimple7702SmartAccount, createBundlerClient } = require("viem/account-abstraction");

  const chain = CHAINS[config.network];
  const transport = resolveRpc(config, networkConfig);
  const publicClient = createPublicClient({ chain, transport });

  const smartAccount = await toSimple7702SmartAccount({
    client: publicClient,
    owner: eoaAccount,
    entryPoint: "0.9",
  });

  const bundlerTransport = resolveBundlerTransport(networkConfig);

  const bundlerClient = createBundlerClient({
    account: smartAccount,
    client: publicClient,
    transport: bundlerTransport,
    userOperation: {
      estimateFeesPerGas: async () => {
        const fees = await publicClient.estimateFeesPerGas();
        const floor = 10_000_000n; // 0.01 gwei floor
        return {
          maxFeePerGas: fees.maxFeePerGas > floor ? fees.maxFeePerGas : floor,
          maxPriorityFeePerGas: fees.maxPriorityFeePerGas > floor ? fees.maxPriorityFeePerGas : floor,
        };
      },
    },
  });

  bundlerClient._paymaster = buildPaymasterMiddleware(networkConfig);

  return { smartAccount, bundlerClient, publicClient };
}

// ======================= SHARED EXECUTION =======================

async function buildApprovalCalls(publicClient, owner, tokenAddress, tokenSymbol, spender, amount) {
  const currentAllowance = await publicClient.readContract({
    address: tokenAddress, abi: ERC20_ABI, functionName: "allowance",
    args: [owner, spender],
  });
  if (currentAllowance >= amount) return [];
  console.log(`> Approving ${tokenSymbol}...`);
  const calls = [];
  // Non-standard ERC-20 tokens (e.g. USDT) revert on approve(newAmount) when
  // current allowance > 0. Reset to 0 first to handle this safely.
  if (currentAllowance > 0n) {
    calls.push({
      to: tokenAddress, value: 0n, _isApproval: true,
      data: encodeFunctionData({ abi: ERC20_ABI, functionName: "approve", args: [spender, 0n] }),
    });
  }
  calls.push({
    to: tokenAddress, value: 0n, _isApproval: true,
    data: encodeFunctionData({ abi: ERC20_ABI, functionName: "approve", args: [spender, amount] }),
  });
  return calls;
}

async function submitUserOp(bundlerClient, calls, options = {}) {
  const sendArgs = { calls, ...options };
  sendArgs.paymaster = bundlerClient._paymaster;

  // Estimate gas first, then bump callGasLimit to handle state-dependent
  // under-estimation (e.g. exactOutput ETH refund). Unused gas is refunded.
  const est = await bundlerClient.estimateUserOperationGas(sendArgs);
  const callGasFloor = 400000n;
  sendArgs.callGasLimit = est.callGasLimit > callGasFloor ? est.callGasLimit : callGasFloor;

  try {
    const hash = await bundlerClient.sendUserOperation(sendArgs);
    console.log(`> UserOp submitted: ${hash}`);
    console.log(`> Waiting for receipt...`);
    const receipt = await bundlerClient.waitForUserOperationReceipt({ hash, timeout: 120_000 });
    if (receipt.success) {
      console.log(`> TX_OK`);
      console.log(`> Transaction: ${receipt.receipt.transactionHash}`);
      console.log(`> Block: ${receipt.receipt.blockNumber}`);
      console.log(`> Gas used: ${receipt.actualGasUsed}`);
      return true;
    } else {
      console.log(`> TX_REVERTED`);
      console.log(`> Transaction: ${receipt.receipt?.transactionHash || "unknown"}`);
      console.log(`> Reason: ${receipt.reason || "unknown"}`);
      return false;
    }
  } catch (e) {
    console.log(`> Paymaster UserOp failed (${e.shortMessage || e.message}), falling back to direct tx...`);
    throw { _paymasterFailed: true, cause: e };
  }
}

async function getEip7702Authorization(publicClient, walletClient, implementationAddress) {
  const code = await publicClient.getCode({ address: walletClient.account.address });
  if (code && code !== "0x" && code.startsWith("0xef0100")) {
    // Check if current delegation matches the expected implementation
    const currentImpl = "0x" + code.slice(8);
    if (currentImpl.toLowerCase() === implementationAddress.toLowerCase()) return null;
    console.log(`> Re-delegating EIP-7702 (${currentImpl.slice(0, 10)}... -> ${implementationAddress.slice(0, 10)}...)...`);
  } else {
    console.log(`> Signing EIP-7702 authorization (first-time delegation)...`);
  }
  return signAuthorization(walletClient, {
    contractAddress: implementationAddress,
  });
}

function _usePaymaster(netConfig) {
  return process.env.LIKWID_NO_PAYMASTER !== "1" && !!netConfig.paymaster && !!netConfig.bundlerUrl;
}

async function _executeEOA(config, netConfig, eoaAccount, publicClient, calls) {
  const chain = CHAINS[config.network];
  const walletClient = createWalletClient({
    account: eoaAccount, chain,
    transport: resolveRpc(config, netConfig),
  });
  console.log(`> Submitting ${calls.length} transaction${calls.length > 1 ? "s" : ""} (direct)...`);
  for (const call of calls) {
    try {
      // Estimate gas with 50% buffer — default estimation is often too tight
      // for DeFi calls with state-dependent execution paths.
      const gasEstimate = await publicClient.estimateGas({
        account: eoaAccount, to: call.to, value: call.value, data: call.data,
      });
      const txHash = await walletClient.sendTransaction({
        to: call.to, value: call.value, data: call.data,
        gas: gasEstimate * 3n / 2n,
      });
      console.log(`> Tx submitted: ${txHash}`);
      const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
      if (receipt.status !== "success") {
        console.log(`> TX_REVERTED: ${txHash}`);
        return false;
      }
    } catch (e) {
      console.log(`> ERROR: Transaction failed: ${e.shortMessage || e.message}`);
      return false;
    }
  }
  console.log(`> TX_OK`);
  return true;
}

async function executeCalls(config, netConfig, eoaAccount, publicClient, calls) {
  if (!_usePaymaster(netConfig)) {
    return _executeEOA(config, netConfig, eoaAccount, publicClient, calls);
  }

  // --- Smart Account + Paymaster path ---
  const { smartAccount, bundlerClient } = await getSmartAccount(config, netConfig, eoaAccount);

  const chain = CHAINS[config.network];
  const walletClient = createWalletClient({
    account: eoaAccount, chain,
    transport: resolveRpc(config, netConfig),
  });
  const authorization = await getEip7702Authorization(publicClient, walletClient, smartAccount.authorization.address);
  const userOpOptions = authorization ? { authorization } : {};

  // Non-standard ERC-20 tokens (e.g. USDT) can fail when approve + swap are
  // batched in a single executeBatch. Split approvals into a separate UserOp.
  const approvalCalls = calls.filter(c => c._isApproval);
  const actionCalls = calls.filter(c => !c._isApproval);

  try {
    if (approvalCalls.length > 0 && actionCalls.length > 0) {
      console.log(`> Submitting approvals (${approvalCalls.length} call${approvalCalls.length > 1 ? "s" : ""})...`);
      const ok = await submitUserOp(bundlerClient, approvalCalls, userOpOptions);
      if (!ok) return false;
      console.log(`> Submitting action (${actionCalls.length} call${actionCalls.length > 1 ? "s" : ""})...`);
      const ok2 = await submitUserOp(bundlerClient, actionCalls);
      if (!ok2) return false;
    } else {
      console.log(`> Submitting UserOperation (${calls.length} call${calls.length > 1 ? "s" : ""})...`);
      const ok = await submitUserOp(bundlerClient, calls, userOpOptions);
      if (!ok) return false;
    }
    return true;
  } catch (e) {
    if (e._paymasterFailed) {
      return _executeEOA(config, netConfig, eoaAccount, publicClient, calls);
    }
    console.log(`> ERROR: UserOp failed: ${e.shortMessage || e.message}`);
    return false;
  }
}

// ======================= COMMANDS =======================

async function cmd_setup(network, keyFilePath) {
  if (!network || !keyFilePath) {
    console.log(`> Usage: setup <network> <keyFilePath>`);
    console.log(`> Networks: sepolia, ethereum, base`);
    return;
  }

  if (!CHAINS[network]) {
    console.log(`> ERROR: Unknown network "${network}". Supported: sepolia, ethereum, base`);
    return;
  }

  const netConfig = await loadNetworkConfig(network);
  if (!netConfig) return;

  const privateKey = readPrivateKey(keyFilePath);
  if (!privateKey) return;

  const account = privateKeyToAccount(privateKey);

  const cfg = { network, keyFilePath: collapseHome(path.resolve(expandHome(keyFilePath))) };
  saveConfig(cfg);

  console.log(`> SETUP_OK`);
  console.log(`> Network: ${netConfig.network} (Chain ID ${netConfig.chainId})`);
  console.log(`> Address: ${account.address}`);
  console.log(`> Key File: ${cfg.keyFilePath}`);
  console.log(`> Gas Mode: ${_usePaymaster(netConfig) ? "Paymaster (AGC)" : "Direct (ETH)"}`);
}

async function cmd_account() {
  const config = loadConfig();
  if (!config) {
    console.log(`> ERROR: Not configured. Run setup first.`);
    return;
  }

  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const clients = createClients(config, netConfig);
  if (!clients) return;

  const { publicClient, account } = clients;

  console.log(`> ACCOUNT_INFO`);
  console.log(`> Network: ${netConfig.network} (Chain ID ${netConfig.chainId})`);
  console.log(`> Address: ${account.address}`);

  const ethBalance = await publicClient.getBalance({ address: account.address });
  console.log(`> ETH Balance: ${formatUnits(ethBalance, 18)} ETH`);
  console.log(`> Gas Mode: ${_usePaymaster(netConfig) ? "Paymaster (AGC)" : "Direct (ETH)"}`);
  if (_usePaymaster(netConfig)) {
    console.log(`> EIP-7702 Smart Account (EOA = Smart Account)`);
  }
}

async function cmd_pools() {
  const config = loadConfig();
  if (!config) {
    console.log(`> ERROR: Not configured. Run setup first.`);
    return;
  }

  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  console.log(`> POOLS on ${netConfig.network} (Chain ID ${netConfig.chainId})`);
  console.log(`>`);

  Object.entries(netConfig.pools).forEach(([name, tiers]) => {
    tiers.forEach((pool) => {
      const poolId = computePoolId(pool);
      console.log(`> ${name} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
      console.log(`>     ${pool.currency0.symbol} (${pool.currency0.address})`);
      console.log(`>     ${pool.currency1.symbol} (${pool.currency1.address})`);
      console.log(`>     Margin Fee: ${(pool.marginFee / 10000).toFixed(2)}%`);
      console.log(`>     Pool ID: ${poolId}`);
      console.log(`>`);
    });
  });
}

// Parse swap direction: sell0/0to1, sell1/1to0 (exact input), buy0, buy1 (exact output)
function parseSwapDirection(direction) {
  if (direction === "sell0" || direction === "0to1") return { zeroForOne: true, exactOutput: false };
  if (direction === "sell1" || direction === "1to0") return { zeroForOne: false, exactOutput: false };
  if (direction === "buy1") return { zeroForOne: true, exactOutput: true };
  if (direction === "buy0") return { zeroForOne: false, exactOutput: true };
  return null;
}

async function cmd_quote(poolStr, direction, amountStr) {
  if (!poolStr || !direction || !amountStr) {
    console.log(`> Usage: quote <pool> <direction> <amount>`);
    console.log(`> Pool: token pair (e.g. ETH/USDT) — lowest fee tier selected by default`);
    console.log(`> Direction: sell0 | sell1 (exact input)  buy0 | buy1 (exact output)`);
    console.log(`> Examples: quote ETH/AGC sell0 0.001  (sell 0.001 ETH)`);
    console.log(`>           quote ETH/AGC buy1 100     (buy 100 AGC)`);
    return;
  }

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);

  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const dir = parseSwapDirection(direction);
  if (!dir) return console.log(`> ERROR: Invalid direction "${direction}". Use sell0, sell1, buy0, or buy1.`);

  const { zeroForOne, exactOutput } = dir;
  const fromToken = zeroForOne ? pool.currency0 : pool.currency1;
  const toToken = zeroForOne ? pool.currency1 : pool.currency0;
  const poolId = computePoolId(pool);

  const clients = createClients(config, netConfig);
  if (!clients) return;

  const helperABI = loadABI("LikwidHelper");

  try {
    if (exactOutput) {
      // Exact output: user specifies desired output amount, calculate required input
      const amountOut = parseUnits(amountStr, toToken.decimals);
      const result = await clients.publicClient.readContract({
        address: netConfig.contracts.LikwidHelper,
        abi: helperABI,
        functionName: "getAmountIn",
        args: [poolId, zeroForOne, amountOut, true],
      });

      const amountIn = result[0] !== undefined ? result[0] : result;
      const fee = result[1] !== undefined ? result[1] : 0;
      const feeAmount = result[2] !== undefined ? result[2] : 0n;

      console.log(`> QUOTE (Exact Output)`);
      console.log(`> Pool: ${pool.currency0.symbol}/${pool.currency1.symbol} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
      console.log(`> Buy: ${amountStr} ${toToken.symbol}`);
      console.log(`> Cost: ~${formatUnits(amountIn, fromToken.decimals)} ${fromToken.symbol}`);
      console.log(`> Fee: ${(fee / 10000).toFixed(2)}% (${formatUnits(feeAmount, fromToken.decimals)} ${fromToken.symbol})`);
    } else {
      // Exact input: user specifies input amount, calculate expected output
      const amountIn = parseUnits(amountStr, fromToken.decimals);
      const result = await clients.publicClient.readContract({
        address: netConfig.contracts.LikwidHelper,
        abi: helperABI,
        functionName: "getAmountOut",
        args: [poolId, zeroForOne, amountIn, true],
      });

      const amountOut = result[0] !== undefined ? result[0] : result;
      const fee = result[1] !== undefined ? result[1] : 0;
      const feeAmount = result[2] !== undefined ? result[2] : 0n;

      console.log(`> QUOTE`);
      console.log(`> Pool: ${pool.currency0.symbol}/${pool.currency1.symbol} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
      console.log(`> Input: ${amountStr} ${fromToken.symbol}`);
      console.log(`> Output: ~${formatUnits(amountOut, toToken.decimals)} ${toToken.symbol}`);
      console.log(`> Fee: ${(fee / 10000).toFixed(2)}% (${formatUnits(feeAmount, fromToken.decimals)} ${fromToken.symbol})`);
    }
  } catch (e) {
    console.log(`> ERROR: Quote failed: ${e.shortMessage || e.message}`);
  }
}

async function cmd_swap(poolStr, direction, amountStr, slippageStr = "1") {
  if (!poolStr || !direction || !amountStr) {
    console.log(`> Usage: swap <pool> <direction> <amount> [slippage%]`);
    console.log(`> Pool: token pair (e.g. ETH/USDT) — lowest fee tier selected by default`);
    console.log(`> Direction: sell0 | sell1 (exact input)  buy0 | buy1 (exact output)`);
    console.log(`> Default slippage: 1%`);
    console.log(`> Examples: swap ETH/AGC sell0 0.001  (sell 0.001 ETH)`);
    console.log(`>           swap ETH/AGC buy1 100     (buy 100 AGC)`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const dir = parseSwapDirection(direction);
  if (!dir) return console.log(`> ERROR: Invalid direction "${direction}". Use sell0, sell1, buy0, or buy1.`);

  const { zeroForOne, exactOutput } = dir;
  const fromToken = zeroForOne ? pool.currency0 : pool.currency1;
  const toToken = zeroForOne ? pool.currency1 : pool.currency0;
  const slippage = BigInt(slippageStr);
  const poolId = computePoolId(pool);

  const pairPositionABI = loadABI("LikwidPairPosition");
  const helperABI = loadABI("LikwidHelper");
  const pairPositionAddress = netConfig.contracts.LikwidPairPosition;
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  if (exactOutput) {
    // --- Exact Output: buy specific amount of toToken ---
    const amountOut = parseUnits(amountStr, toToken.decimals);

    console.log(`> SWAP (Exact Output): Buy ${amountStr} ${toToken.symbol} with ${fromToken.symbol}`);

    let amountIn;
    try {
      const result = await publicClient.readContract({
        address: netConfig.contracts.LikwidHelper,
        abi: helperABI,
        functionName: "getAmountIn",
        args: [poolId, zeroForOne, amountOut, true],
      });
      amountIn = result[0] !== undefined ? result[0] : result;
    } catch (e) {
      return console.log(`> ERROR: Quote failed: ${e.shortMessage || e.message}`);
    }

    const amountInMax = (amountIn * (100n + slippage)) / 100n;
    const sendingNative = isNative(fromToken.address);

    console.log(`> Estimated cost: ~${formatUnits(amountIn, fromToken.decimals)} ${fromToken.symbol}`);
    console.log(`> Max cost (${slippageStr}% slippage): ${formatUnits(amountInMax, fromToken.decimals)} ${fromToken.symbol}`);
    console.log(`> Sender: ${senderAddress}`);
    console.log(`> Gas Mode: ${_usePaymaster(netConfig) ? "Paymaster (AGC)" : "Direct (ETH)"}`);

    const calls = [];

    if (!sendingNative) {
      calls.push(...await buildApprovalCalls(publicClient, senderAddress, fromToken.address, fromToken.symbol, pairPositionAddress, amountInMax));
    }

    calls.push({
      to: pairPositionAddress,
      value: sendingNative ? amountInMax : 0n,
      data: encodeFunctionData({
        abi: pairPositionABI,
        functionName: "exactOutput",
        args: [{
          poolId, zeroForOne, to: senderAddress,
          amountInMax, amountOut, deadline,
        }],
      }),
    });

    await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
  } else {
    // --- Exact Input: sell specific amount of fromToken ---
    const amountIn = parseUnits(amountStr, fromToken.decimals);

    console.log(`> SWAP: ${amountStr} ${fromToken.symbol} -> ${toToken.symbol}`);

    let amountOut;
    try {
      const result = await publicClient.readContract({
        address: netConfig.contracts.LikwidHelper,
        abi: helperABI,
        functionName: "getAmountOut",
        args: [poolId, zeroForOne, amountIn, true],
      });
      amountOut = result[0] !== undefined ? result[0] : result;
    } catch (e) {
      return console.log(`> ERROR: Quote failed: ${e.shortMessage || e.message}`);
    }

    const amountOutMin = (amountOut * (100n - slippage)) / 100n;
    const sendingNative = isNative(fromToken.address);

    console.log(`> Estimated output: ~${formatUnits(amountOut, toToken.decimals)} ${toToken.symbol}`);
    console.log(`> Min output (${slippageStr}% slippage): ${formatUnits(amountOutMin, toToken.decimals)} ${toToken.symbol}`);
    console.log(`> Sender: ${senderAddress}`);
    console.log(`> Gas Mode: ${_usePaymaster(netConfig) ? "Paymaster (AGC)" : "Direct (ETH)"}`);

    const calls = [];

    if (!sendingNative) {
      calls.push(...await buildApprovalCalls(publicClient, senderAddress, fromToken.address, fromToken.symbol, pairPositionAddress, amountIn));
    }

    calls.push({
      to: pairPositionAddress,
      value: sendingNative ? amountIn : 0n,
      data: encodeFunctionData({
        abi: pairPositionABI,
        functionName: "exactInput",
        args: [{
          poolId, zeroForOne, to: senderAddress,
          amountIn, amountOutMin, deadline,
        }],
      }),
    });

    await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
  }
}

// ======================= POOL INFO =======================

async function cmd_pool_info(poolStr) {
  if (poolStr === undefined) {
    console.log(`> Usage: pool_info <pool>`);
    console.log(`> Pool: token pair (e.g. ETH/USDT) — lowest fee tier selected by default`);
    return;
  }

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);

  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const helperABI = loadABI("LikwidHelper");
  const clients = createClients(config, netConfig);
  if (!clients) return;

  try {
    const stateInfo = await clients.publicClient.readContract({
      address: netConfig.contracts.LikwidHelper,
      abi: helperABI,
      functionName: "getPoolStateInfo",
      args: [poolId],
    });

    const r0 = stateInfo.pairReserve0;
    const r1 = stateInfo.pairReserve1;

    const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;

    if (r0 === 0n && r1 === 0n) {
      console.log(`> POOL_NOT_INITIALIZED`);
      console.log(`> Pool: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
      console.log(`> This pool has no liquidity. You need to Create a Pair first.`);
      return;
    }

    const rate0to1 = Number(formatUnits(r1, pool.currency1.decimals)) / Number(formatUnits(r0, pool.currency0.decimals));
    const rate1to0 = Number(formatUnits(r0, pool.currency0.decimals)) / Number(formatUnits(r1, pool.currency1.decimals));

    console.log(`> POOL_INFO`);
    console.log(`> Pool: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
    console.log(`> Pool ID: ${poolId}`);
    console.log(`> Pair Reserve ${pool.currency0.symbol}: ${formatUnits(r0, pool.currency0.decimals)}`);
    console.log(`> Pair Reserve ${pool.currency1.symbol}: ${formatUnits(r1, pool.currency1.decimals)}`);
    console.log(`> Rate: 1 ${pool.currency0.symbol} = ${rate0to1.toFixed(6)} ${pool.currency1.symbol}`);
    console.log(`> Rate: 1 ${pool.currency1.symbol} = ${rate1to0.toFixed(6)} ${pool.currency0.symbol}`);
    console.log(`> Total Supply: ${formatUnits(stateInfo.totalSupply, 18)}`);
  } catch (e) {
    console.log(`> ERROR: Could not query pool state: ${e.shortMessage || e.message}`);
  }
}

// ======================= ADD LIQUIDITY =======================

async function cmd_lp_add(poolStr, currencyStr, amountStr, slippageStr = "1") {
  if (!poolStr || !currencyStr || !amountStr) {
    console.log(`> Usage: lp_add <pool> <currency> <amount> [slippage%]`);
    console.log(`> Pool: token pair (e.g. ETH/USDT) — lowest fee tier selected by default`);
    console.log(`> Currency: 0 (currency0) or 1 (currency1)`);
    console.log(`> Provide the amount for one side; the other is auto-calculated from pool ratio.`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const inputSide = parseInt(currencyStr);
  if (inputSide !== 0 && inputSide !== 1) {
    return console.log(`> ERROR: Currency must be 0 or 1.`);
  }

  const inputToken = inputSide === 0 ? pool.currency0 : pool.currency1;
  const inputAmount = parseUnits(amountStr, inputToken.decimals);
  const slippage = BigInt(slippageStr);
  const poolId = computePoolId(pool);

  const helperABI = loadABI("LikwidHelper");
  const pairPositionABI = loadABI("LikwidPairPosition");

  // --- Query pool state ---
  let r0, r1;
  try {
    const stateInfo = await publicClient.readContract({
      address: netConfig.contracts.LikwidHelper,
      abi: helperABI,
      functionName: "getPoolStateInfo",
      args: [poolId],
    });
    r0 = stateInfo.pairReserve0;
    r1 = stateInfo.pairReserve1;
  } catch (e) {
    return console.log(`> ERROR: Could not query pool state: ${e.shortMessage || e.message}`);
  }

  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;

  if (r0 === 0n && r1 === 0n) {
    console.log(`> POOL_NOT_INITIALIZED`);
    console.log(`> Pool: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
    console.log(`> This pool has no liquidity. You need to Create a Pair first.`);
    return;
  }

  // --- Calculate matching amount ---
  let amount0, amount1;
  if (inputSide === 0) {
    amount0 = inputAmount;
    amount1 = r0 > 0n ? (inputAmount * r1) / r0 : 0n;
  } else {
    amount1 = inputAmount;
    amount0 = r1 > 0n ? (inputAmount * r0) / r1 : 0n;
  }

  const amount0Min = (amount0 * (100n - slippage)) / 100n;
  const amount1Min = (amount1 * (100n - slippage)) / 100n;
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  const rate = Number(formatUnits(r1, pool.currency1.decimals)) / Number(formatUnits(r0, pool.currency0.decimals));

  // --- Check for existing position ---
  const positions = await fetchLiquidityPositions(netConfig.chainId, senderAddress, poolId);
  const existingTokenId = positions.length > 0 ? BigInt(positions[0].tokenId) : null;

  if (existingTokenId) {
    console.log(`> LP_INCREASE: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%) — tokenId: ${existingTokenId}`);
  } else {
    console.log(`> LP_ADD: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%)`);
  }
  console.log(`> Rate: 1 ${pool.currency0.symbol} = ${rate.toFixed(6)} ${pool.currency1.symbol}`);
  console.log(`> ${pool.currency0.symbol}: ${formatUnits(amount0, pool.currency0.decimals)}`);
  console.log(`> ${pool.currency1.symbol}: ${formatUnits(amount1, pool.currency1.decimals)}`);
  console.log(`> Slippage: ${slippageStr}%`);
  console.log(`> Sender: ${senderAddress}`);

  // --- Build calls ---
  const pairPositionAddress = netConfig.contracts.LikwidPairPosition;
  const native0 = isNative(pool.currency0.address);
  const native1 = isNative(pool.currency1.address);
  const calls = [];

  // Approve ERC20 tokens
  if (!native0 && amount0 > 0n) {
    calls.push(...await buildApprovalCalls(publicClient, senderAddress, pool.currency0.address, pool.currency0.symbol, pairPositionAddress, amount0));
  }
  if (!native1 && amount1 > 0n) {
    calls.push(...await buildApprovalCalls(publicClient, senderAddress, pool.currency1.address, pool.currency1.symbol, pairPositionAddress, amount1));
  }

  const nativeValue = (native0 ? amount0 : 0n) + (native1 ? amount1 : 0n);

  if (existingTokenId) {
    calls.push({
      to: pairPositionAddress,
      value: nativeValue,
      data: encodeFunctionData({
        abi: pairPositionABI,
        functionName: "increaseLiquidity",
        args: [existingTokenId, amount0, amount1, amount0Min, amount1Min, deadline],
      }),
    });
  } else {
    const poolKey = {
      currency0: pool.currency0.address,
      currency1: pool.currency1.address,
      fee: pool.fee,
      marginFee: pool.marginFee,
    };
    calls.push({
      to: pairPositionAddress,
      value: nativeValue,
      data: encodeFunctionData({
        abi: pairPositionABI,
        functionName: "addLiquidity",
        args: [poolKey, senderAddress, amount0, amount1, amount0Min, amount1Min, deadline],
      }),
    });
  }

  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
}

// ======================= LP POSITIONS =======================

async function cmd_lp_positions(poolStr) {
  if (!poolStr) {
    console.log(`> Usage: lp_positions <pool>`);
    console.log(`> Pool: token pair (e.g. ETH/USDT)`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;

  const positions = await fetchLiquidityPositions(netConfig.chainId, senderAddress, poolId);
  if (positions.length === 0) {
    console.log(`> No liquidity positions found for ${poolName}.`);
    return;
  }

  const helperABI = loadABI("LikwidHelper");
  const pairPositionABI = loadABI("LikwidPairPosition");

  // Query pool state once (shared across all positions)
  let stateInfo;
  try {
    stateInfo = await publicClient.readContract({
      address: netConfig.contracts.LikwidHelper,
      abi: helperABI,
      functionName: "getPoolStateInfo",
      args: [poolId],
    });
  } catch (e) {
    return console.log(`> ERROR: Could not query pool state: ${e.shortMessage || e.message}`);
  }

  const totalSupply = stateInfo.totalSupply;
  const r0 = stateInfo.pairReserve0;
  const r1 = stateInfo.pairReserve1;

  console.log(`> Your Liquidity Positions:`);
  console.log(`>`);

  for (const item of positions) {
    const tokenId = BigInt(item.tokenId);

    let posState;
    try {
      posState = await publicClient.readContract({
        address: netConfig.contracts.LikwidPairPosition,
        abi: pairPositionABI,
        functionName: "getPositionState",
        args: [tokenId],
      });
    } catch (e) {
      console.log(`> ERROR: Could not query position #${tokenId}: ${e.shortMessage || e.message}`);
      continue;
    }

    const liquidity = posState.liquidity;
    const poolShare = totalSupply > 0n ? Number(liquidity) / Number(totalSupply) : 0;
    const amount0 = totalSupply > 0n ? (r0 * liquidity) / totalSupply : 0n;
    const amount1 = totalSupply > 0n ? (r1 * liquidity) / totalSupply : 0n;

    console.log(`>   Pool: ${poolName}  Swap Fee: ${(pool.fee / 10000).toFixed(2)}%  Margin Fee: ${(pool.marginFee / 10000).toFixed(2)}%`);
    console.log(`>   Your Pool Share: ${(poolShare * 100).toFixed(2)}%`);
    console.log(`>   ${pool.currency0.symbol}: ${formatUnits(amount0, pool.currency0.decimals)}`);
    console.log(`>   ${pool.currency1.symbol}: ${formatUnits(amount1, pool.currency1.decimals)}`);
    console.log(`>`);
  }

  console.log(`>   Tip: Use "lp_add" to increase liquidity, or "lp_remove" to remove liquidity.`);
}

// ======================= REMOVE LIQUIDITY =======================

async function cmd_lp_remove(poolStr, percentStr = "100") {
  if (!poolStr) {
    console.log(`> Usage: lp_remove <pool> [percentage]`);
    console.log(`> Pool: token pair (e.g. ETH/USDT)`);
    console.log(`> Percentage: 1-100 (default: 100 = remove all)`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Use token pair (e.g. ETH/USDT). Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;

  const positions = await fetchLiquidityPositions(netConfig.chainId, senderAddress, poolId);
  if (positions.length === 0) {
    console.log(`> ERROR: No liquidity position found for ${poolName}. Nothing to remove.`);
    return;
  }

  const tokenId = BigInt(positions[0].tokenId);
  const pairPositionABI = loadABI("LikwidPairPosition");
  const helperABI = loadABI("LikwidHelper");

  // Query position state on-chain
  let posState;
  try {
    posState = await publicClient.readContract({
      address: netConfig.contracts.LikwidPairPosition,
      abi: pairPositionABI,
      functionName: "getPositionState",
      args: [tokenId],
    });
  } catch (e) {
    return console.log(`> ERROR: Could not query position state: ${e.shortMessage || e.message}`);
  }

  const totalLiquidity = posState.liquidity;
  if (totalLiquidity === 0n) {
    console.log(`> ERROR: Position #${tokenId} has zero liquidity.`);
    return;
  }

  const percent = BigInt(percentStr);
  if (percent < 1n || percent > 100n) {
    return console.log(`> ERROR: Percentage must be between 1 and 100.`);
  }

  const liquidityToRemove = (totalLiquidity * percent) / 100n;

  // Query pool reserves to estimate output
  let stateInfo;
  try {
    stateInfo = await publicClient.readContract({
      address: netConfig.contracts.LikwidHelper,
      abi: helperABI,
      functionName: "getPoolStateInfo",
      args: [poolId],
    });
  } catch (e) {
    return console.log(`> ERROR: Could not query pool state: ${e.shortMessage || e.message}`);
  }

  const totalSupply = stateInfo.totalSupply;
  const r0 = stateInfo.pairReserve0;
  const r1 = stateInfo.pairReserve1;

  const estAmount0 = totalSupply > 0n ? (r0 * liquidityToRemove) / totalSupply : 0n;
  const estAmount1 = totalSupply > 0n ? (r1 * liquidityToRemove) / totalSupply : 0n;

  const slippage = 1n; // 1% default
  const amount0Min = (estAmount0 * (100n - slippage)) / 100n;
  const amount1Min = (estAmount1 * (100n - slippage)) / 100n;
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  console.log(`> LP_REMOVE: ${poolName} (fee: ${(pool.fee / 10000).toFixed(2)}%) — tokenId: ${tokenId}`);
  console.log(`> Removing: ${percentStr}% of liquidity`);
  console.log(`> Est. ${pool.currency0.symbol}: ${formatUnits(estAmount0, pool.currency0.decimals)}`);
  console.log(`> Est. ${pool.currency1.symbol}: ${formatUnits(estAmount1, pool.currency1.decimals)}`);
  console.log(`> Slippage: 1%`);
  console.log(`> Sender: ${senderAddress}`);

  const pairPositionAddress = netConfig.contracts.LikwidPairPosition;
  const calls = [{
    to: pairPositionAddress,
    value: 0n,
    data: encodeFunctionData({
      abi: pairPositionABI,
      functionName: "removeLiquidity",
      args: [tokenId, liquidityToRemove, amount0Min, amount1Min, deadline],
    }),
  }];

  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
}

// ======================= CREATE PAIR =======================

function saveUserOverrides(network, newTokens, newPool, pairKey) {
  const overrides = loadUserOverrides(network);

  for (const token of newTokens) {
    if (!overrides.tokens[token.symbol]) {
      overrides.tokens[token.symbol] = { address: token.address.toLowerCase(), decimals: token.decimals };
    }
  }

  if (!overrides.pools[pairKey]) overrides.pools[pairKey] = [];
  const exists = overrides.pools[pairKey].some(p => p.fee === newPool.fee && p.marginFee === newPool.marginFee);
  if (!exists) {
    overrides.pools[pairKey].push(newPool);
    overrides.pools[pairKey].sort((a, b) => a.fee - b.fee);
  }

  fs.mkdirSync(POOLS_DIR, { recursive: true });
  const file = path.join(POOLS_DIR, `${network}.local.json`);
  fs.writeFileSync(file, JSON.stringify(overrides, null, 2) + "\n");
}

function resolvePool(netConfig, poolStr) {
  // Normalize: uppercase, replace - with /
  const key = poolStr.toUpperCase().replace("-", "/");
  // Direct key match
  let tiers = netConfig.pools[key];
  if (!tiers) {
    // Try reversed order: "USDT/ETH" -> "ETH/USDT"
    const parts = key.split("/");
    if (parts.length === 2) tiers = netConfig.pools[`${parts[1]}/${parts[0]}`];
  }
  if (!tiers || tiers.length === 0) return null;
  return tiers[0]; // lowest fee (array pre-sorted)
}

function resolveToken(netConfig, name) {
  const upper = name.toUpperCase();
  const token = netConfig.tokens[upper];
  if (!token) return null;
  return { symbol: upper, address: token.address, decimals: token.decimals };
}

function isAddress(s) {
  return /^0x[0-9a-fA-F]{40}$/.test(s);
}

async function resolveTokenOrAddress(netConfig, nameOrAddress, publicClient) {
  // Try name lookup first
  const byName = resolveToken(netConfig, nameOrAddress);
  if (byName) return byName;

  // If it looks like an address, query on-chain
  if (!isAddress(nameOrAddress)) return null;

  const address = getAddress(nameOrAddress);
  const tokenAbi = parseAbi([
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)",
  ]);

  try {
    const [symbol, decimals] = await Promise.all([
      publicClient.readContract({ address, abi: tokenAbi, functionName: "symbol" }),
      publicClient.readContract({ address, abi: tokenAbi, functionName: "decimals" }),
    ]);
    return { symbol, address: address.toLowerCase(), decimals };
  } catch (e) {
    console.log(`> WARN: Could not read token metadata at ${address}: ${e.shortMessage || e.message}`);
    return null;
  }
}

async function cmd_create_pair(token0Name, token1Name, feeStr, marginFeeStr) {
  if (!token0Name || !token1Name || !feeStr || !marginFeeStr) {
    console.log(`> Usage: create_pair <token0> <token1> <fee> <marginFee>`);
    console.log(`> Tokens can be resolved by name or contract address.`);
    console.log(`> Fee values in basis points (e.g., 3000 = 0.30%).`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient } = ctx;

  // --- Resolve tokens (by name or address) ---
  const tokenA = await resolveTokenOrAddress(netConfig, token0Name, publicClient);
  const tokenB = await resolveTokenOrAddress(netConfig, token1Name, publicClient);

  if (!tokenA) {
    const available = Object.keys(netConfig.tokens).join(", ");
    return console.log(`> ERROR: Unknown token "${token0Name}". Available: ${available} (or pass a contract address)`);
  }
  if (!tokenB) {
    const available = Object.keys(netConfig.tokens).join(", ");
    return console.log(`> ERROR: Unknown token "${token1Name}". Available: ${available} (or pass a contract address)`);
  }
  if (tokenA.address.toLowerCase() === tokenB.address.toLowerCase()) {
    return console.log(`> ERROR: currency0 and currency1 cannot be the same token.`);
  }

  // --- Sort: protocol requires currency0 < currency1 ---
  let currency0, currency1;
  if (tokenA.address.toLowerCase() < tokenB.address.toLowerCase()) {
    currency0 = tokenA;
    currency1 = tokenB;
  } else {
    currency0 = tokenB;
    currency1 = tokenA;
  }

  const fee = parseInt(feeStr);
  const marginFee = parseInt(marginFeeStr);

  const poolKey = {
    currency0: currency0.address,
    currency1: currency1.address,
    fee,
    marginFee,
  };

  // Compute poolId for display
  const poolObj = {
    currency0, currency1, fee, marginFee,
  };
  const poolId = computePoolId(poolObj);

  console.log(`> CREATE_PAIR`);
  console.log(`> currency0: ${currency0.symbol} (${currency0.address})`);
  console.log(`> currency1: ${currency1.symbol} (${currency1.address})`);
  console.log(`> Swap Fee: ${(fee / 10000).toFixed(2)}%  Margin Fee: ${(marginFee / 10000).toFixed(2)}%`);
  console.log(`> Pool ID: ${poolId}`);

  const vaultABI = loadABI("LikwidVault");
  const vaultAddress = netConfig.contracts.LikwidVault;

  const calls = [{
    to: vaultAddress,
    value: 0n,
    data: encodeFunctionData({
      abi: vaultABI,
      functionName: "initialize",
      args: [poolKey],
    }),
  }];

  console.log(`> Initializing pool on LikwidVault...`);
  const ok = await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
  if (!ok) return;

  // --- Auto-add new tokens and pool to user overrides ---
  const newTokens = [];
  for (const token of [currency0, currency1]) {
    const alreadyKnown = Object.values(netConfig.tokens).some(
      t => t.address.toLowerCase() === token.address.toLowerCase()
    );
    if (!alreadyKnown) {
      netConfig.tokens[token.symbol] = { address: token.address.toLowerCase(), decimals: token.decimals };
      newTokens.push(token);
      console.log(`> Token added to config: ${token.symbol} (${token.address})`);
    }
  }

  const pairKey = `${currency0.symbol}/${currency1.symbol}`;
  const newPool = {
    currency0: { address: currency0.address, symbol: currency0.symbol, decimals: currency0.decimals },
    currency1: { address: currency1.address, symbol: currency1.symbol, decimals: currency1.decimals },
    fee,
    marginFee,
  };

  if (!netConfig.pools[pairKey]) netConfig.pools[pairKey] = [];
  const exists = netConfig.pools[pairKey].some(p => p.fee === fee && p.marginFee === marginFee);

  if (!exists) {
    netConfig.pools[pairKey].push(newPool);
    netConfig.pools[pairKey].sort((a, b) => a.fee - b.fee);
    console.log(`> Pool added to config: ${pairKey} (fee: ${(fee / 10000).toFixed(2)}%).`);
  } else {
    console.log(`> Pool already in config.`);
  }

  if (newTokens.length > 0 || !exists) {
    saveUserOverrides(config.network, newTokens, newPool, pairKey);
  }

  console.log(`> Use "lp_add ${pairKey}" to add initial liquidity to this pool.`);
}

// ======================= MARGIN =======================

const LEVERAGE_MAX_RATIOS = [0.15, 0.12, 0.09, 0.05, 0.017]; // 1x..5x
const MARGIN_MINIMUM_RATIO = 10_000_000n; // matches LikwidMarginPosition constant

async function computeMarginPreview(publicClient, netConfig, pool, poolId, marginForOne, leverageInt, marginAmount) {
  const helperABI = loadABI("LikwidHelper");
  const helperAddr = netConfig.contracts.LikwidHelper;

  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const borrowToken = marginForOne ? pool.currency0 : pool.currency1;

  // 1. Pool state
  const stateInfo = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getPoolStateInfo", args: [poolId],
  });

  // 2. Max margin
  const pairReserve = marginForOne ? stateInfo.pairReserve1 : stateInfo.pairReserve0;
  const realReserve = marginForOne ? stateInfo.realReserve1 : stateInfo.realReserve0;
  const ratio = LEVERAGE_MAX_RATIOS[leverageInt - 1];
  const fromPair = pairReserve * BigInt(Math.round(ratio * 10000)) / 10000n;
  const maxMargin = fromPair < realReserve ? fromPair : realReserve;
  const minMargin = pairReserve / MARGIN_MINIMUM_RATIO;

  // 3. Borrow quote: use getAmountIn to match contract's SwapMath.getAmountIn
  //    "To produce marginTotal of margin currency, how much borrow currency is needed?"
  const marginTotal = marginAmount * BigInt(leverageInt);
  const quoteResult = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getAmountIn", args: [poolId, marginForOne, marginTotal, true],
  });
  const borrowAmount = quoteResult[0];
  const swapFee = quoteResult[1];
  const swapFeeAmount = quoteResult[2];
  const borrowAmountMax = borrowAmount * 101n / 100n; // +1% slippage

  // 4. Total (Using Margin Lx) = marginTotal minus margin fee (in margin currency).
  // Fee basis: 1_000_000 = 100% (e.g. marginFee 3000 = 0.30%).
  const total = marginTotal - marginTotal * BigInt(pool.marginFee) / 1_000_000n;

  // 5. Borrow APR
  const borrowForOne = !marginForOne;
  const aprRaw = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getBorrowAPR", args: [poolId, borrowForOne],
  });

  // 6. Margin levels
  const liquidationLevel = 1.1; // Protocol constant: liquidation trigger
  // minMarginLevels (e.g. 1.17) is the minimum IMR allowed when opening — validated separately

  // 7. Initial Margin Level = (marginAmount + marginTotal) / debtValue
  // debtValue in margin currency: use getAmountIn to price borrowAmount
  const debtQuote = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getAmountIn", args: [poolId, !marginForOne, borrowAmount, true],
  });
  const debtValueInMarginCurrency = debtQuote[0];
  const initialMarginLevel = Number(marginAmount + total) / Number(debtValueInMarginCurrency);

  // 8. Liquidation price = (marginAmount + marginTotal) / (borrowAmount * 1.1)
  //    Result is always in currency0 per currency1 (e.g. ETH per LIKWID)
  const marginAmtF = Number(formatUnits(marginAmount, marginToken.decimals));
  const marginTotalF = Number(formatUnits(total, marginToken.decimals));
  const borrowAmtF = Number(formatUnits(borrowAmount, borrowToken.decimals));
  let liquidationPrice;
  if (!marginForOne) {
    // Short: margin=currency0, borrow=currency1 → price in currency0/currency1
    liquidationPrice = (marginAmtF + marginTotalF) / (borrowAmtF * liquidationLevel);
  } else {
    // Long: margin=currency1, borrow=currency0 → invert to get currency0/currency1
    liquidationPrice = (borrowAmtF * liquidationLevel) / (marginAmtF + marginTotalF);
  }

  return {
    marginToken, borrowToken, stateInfo,
    maxMargin, minMargin, borrowAmount, borrowAmountMax, swapFee, swapFeeAmount,
    total, aprRaw, liquidationLevel, initialMarginLevel, liquidationPrice,
  };
}

function printMarginPreview(pool, marginForOne, leverageInt, marginAmount, preview) {
  const { marginToken, borrowToken, maxMargin, borrowAmount, borrowAmountMax,
    total, aprRaw, liquidationLevel, initialMarginLevel, liquidationPrice } = preview;

  const dirLabel = marginForOne
    ? `Long ${pool.currency1.symbol} (Short ${pool.currency0.symbol})`
    : `Short ${pool.currency1.symbol} (Long ${pool.currency0.symbol})`;
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;
  const aprPercent = (Number(aprRaw) / 10000).toFixed(2);

  // Price unit: always currency0 per currency1
  const priceUnit = `${pool.currency0.symbol} per ${pool.currency1.symbol}`;

  console.log(`> MARGIN_QUOTE: ${dirLabel} | ${poolName} | ${leverageInt}x`);
  console.log(`> ─────────────────────────────────`);
  console.log(`> Margin:                  ${formatUnits(marginAmount, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Total (Using Margin ${leverageInt}x): ${formatUnits(total, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Borrow Amount:           ${formatUnits(borrowAmount, borrowToken.decimals)} ${borrowToken.symbol}`);
  console.log(`> Borrow APY:              ${aprPercent}%`);
  console.log(`> ─────────────────────────────────`);
  console.log(`> Initial Margin Level:     ${initialMarginLevel.toFixed(2)}`);
  console.log(`> Liquidation Margin Level: ${liquidationLevel.toFixed(2)}`);
  console.log(`> Liq.Price:                ${liquidationPrice.toFixed(8)} ${priceUnit}`);
  console.log(`> ─────────────────────────────────`);
  console.log(`> Max Margin (${leverageInt}x):         ${formatUnits(maxMargin, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Max Slippage:             Auto 1%`);
  console.log(`> Borrow Max Amount:        ${formatUnits(borrowAmountMax, borrowToken.decimals)} ${borrowToken.symbol}`);
}

function parseMarginArgs(poolStr, directionStr, leverageStr, amountStr) {
  if (!poolStr || !directionStr || !leverageStr || !amountStr) return null;
  const leverageInt = parseInt(leverageStr);
  if (isNaN(leverageInt) || leverageInt < 1 || leverageInt > 5) {
    console.log(`> ERROR: Leverage must be 1-5 (got "${leverageStr}").`);
    return null;
  }
  const marginForOne = (directionStr === "long");
  if (directionStr !== "long" && directionStr !== "short") {
    console.log(`> ERROR: Direction must be "long" or "short" (got "${directionStr}").`);
    return null;
  }
  return { marginForOne, leverageInt };
}

async function cmd_margin_quote(poolStr, directionStr, leverageStr, amountStr) {
  if (!poolStr || !directionStr || !leverageStr || !amountStr) {
    console.log(`> Usage: margin_quote <pool> <direction> <leverage> <amount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> Direction: long (Long currency1) or short (Short currency1)`);
    console.log(`> Leverage: 1-5`);
    console.log(`> Amount: margin amount in collateral currency`);
    return;
  }

  const parsed = parseMarginArgs(poolStr, directionStr, leverageStr, amountStr);
  if (!parsed) return;
  const { marginForOne, leverageInt } = parsed;

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);
  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const marginAmount = parseUnits(amountStr, marginToken.decimals);

  const clients = createClients(config, netConfig);
  if (!clients) return;

  try {
    const preview = await computeMarginPreview(
      clients.publicClient, netConfig, pool, poolId, marginForOne, leverageInt, marginAmount,
    );

    if (marginAmount < preview.minMargin) {
      console.log(`> ERROR: Below minimum margin ${formatUnits(preview.minMargin, marginToken.decimals)} ${marginToken.symbol} (MarginBelowMinimum).`);
      return;
    }
    if (marginAmount > preview.maxMargin) {
      console.log(`> ERROR: Exceeds max margin ${formatUnits(preview.maxMargin, marginToken.decimals)} ${marginToken.symbol} at ${leverageInt}x.`);
      return;
    }

    printMarginPreview(pool, marginForOne, leverageInt, marginAmount, preview);
  } catch (e) {
    console.log(`> ERROR: Margin quote failed: ${e.shortMessage || e.message}`);
  }
}

async function cmd_margin_open(poolStr, directionStr, leverageStr, amountStr) {
  if (!poolStr || !directionStr || !leverageStr || !amountStr) {
    console.log(`> Usage: margin_open <pool> <direction> <leverage> <amount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> Direction: long (Long currency1) or short (Short currency1)`);
    console.log(`> Leverage: 1-5`);
    console.log(`> Amount: margin amount in collateral currency`);
    return;
  }

  const parsed = parseMarginArgs(poolStr, directionStr, leverageStr, amountStr);
  if (!parsed) return;
  const { marginForOne, leverageInt } = parsed;

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const marginAmount = parseUnits(amountStr, marginToken.decimals);

  // --- Preview ---
  let preview;
  try {
    preview = await computeMarginPreview(
      publicClient, netConfig, pool, poolId, marginForOne, leverageInt, marginAmount,
    );
  } catch (e) {
    return console.log(`> ERROR: Margin quote failed: ${e.shortMessage || e.message}`);
  }

  if (marginAmount < preview.minMargin) {
    return console.log(`> ERROR: Below minimum margin ${formatUnits(preview.minMargin, marginToken.decimals)} ${marginToken.symbol} (MarginBelowMinimum).`);
  }
  if (marginAmount > preview.maxMargin) {
    return console.log(`> ERROR: Exceeds max margin ${formatUnits(preview.maxMargin, marginToken.decimals)} ${marginToken.symbol} at ${leverageInt}x.`);
  }

  printMarginPreview(pool, marginForOne, leverageInt, marginAmount, preview);

  // --- Check existing positions via API ---
  console.log(`> Checking existing margin positions...`);
  const positions = await fetchMarginPositions(netConfig.chainId, senderAddress, poolId);

  // Filter: same direction (marginForOne match)
  // We only use tokenId from API; verify direction on-chain if needed
  let existingTokenId = null;
  if (positions.length > 0) {
    const marginPositionABI = loadABI("LikwidMarginPosition");
    // Check first position's direction on-chain
    const tid = BigInt(positions[0].tokenId);
    try {
      const posState = await publicClient.readContract({
        address: netConfig.contracts.LikwidMarginPosition, abi: marginPositionABI,
        functionName: "getPositionState", args: [tid],
      });
      if (posState.marginForOne === marginForOne) {
        existingTokenId = tid;
      }
    } catch (_) {}
  }

  // --- Build calls ---
  const marginPositionAddress = netConfig.contracts.LikwidMarginPosition;
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const calls = [];
  const sendingNative = isNative(marginToken.address);
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  // Approve if ERC-20 margin
  if (!sendingNative) {
    calls.push(...await buildApprovalCalls(
      publicClient, senderAddress, marginToken.address, marginToken.symbol,
      marginPositionAddress, marginAmount,
    ));
  }

  if (existingTokenId) {
    // --- Increase existing position: margin() ---
    console.log(`> Found existing position #${existingTokenId}, increasing margin...`);
    calls.push({
      to: marginPositionAddress,
      value: sendingNative ? marginAmount : 0n,
      data: encodeFunctionData({
        abi: marginPositionABI,
        functionName: "margin",
        args: [{
          tokenId: existingTokenId,
          leverage: leverageInt,
          marginAmount,
          borrowAmount: preview.borrowAmount,
          borrowAmountMax: preview.borrowAmountMax,
          deadline,
        }],
      }),
    });
  } else {
    // --- Open new position: addMargin() ---
    console.log(`> No existing position, opening new margin...`);
    const poolKey = {
      currency0: pool.currency0.address,
      currency1: pool.currency1.address,
      fee: pool.fee,
      marginFee: pool.marginFee,
    };
    calls.push({
      to: marginPositionAddress,
      value: sendingNative ? marginAmount : 0n,
      data: encodeFunctionData({
        abi: marginPositionABI,
        functionName: "addMargin",
        args: [poolKey, {
          marginForOne,
          leverage: leverageInt,
          marginAmount,
          borrowAmount: preview.borrowAmount,
          borrowAmountMax: preview.borrowAmountMax,
          recipient: senderAddress,
          deadline,
        }],
      }),
    });
  }

  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
}

// ======================= MARGIN POSITIONS =======================

async function cmd_margin_positions(poolStr) {
  if (!poolStr) {
    console.log(`> Usage: margin_positions <pool>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    return;
  }

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);
  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const clients = createClients(config, netConfig);
  if (!clients) return;
  const { publicClient, account } = clients;
  const owner = account.address;

  // 1. Query API — only use tokenId
  const items = await fetchMarginPositions(netConfig.chainId, owner, poolId);
  if (items.length === 0) {
    console.log(`> No margin positions found for ${pool.currency0.symbol}/${pool.currency1.symbol}.`);
    return;
  }

  const marginPositionABI = loadABI("LikwidMarginPosition");
  const helperABI = loadABI("LikwidHelper");
  const helperAddr = netConfig.contracts.LikwidHelper;
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  // 2. Pool state for current price
  const stateInfo = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getPoolStateInfo", args: [poolId],
  });
  const r0 = Number(formatUnits(stateInfo.pairReserve0, pool.currency0.decimals));
  const r1 = Number(formatUnits(stateInfo.pairReserve1, pool.currency1.decimals));
  // Current price: currency0 per currency1 (e.g. ETH per LIKWID)
  const curPrice = r0 / r1;

  // 3. Borrow APR for both directions
  const [apr0, apr1] = await Promise.all([
    publicClient.readContract({ address: helperAddr, abi: helperABI, functionName: "getBorrowAPR", args: [poolId, false] }),
    publicClient.readContract({ address: helperAddr, abi: helperABI, functionName: "getBorrowAPR", args: [poolId, true] }),
  ]);

  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;
  const swapFeeStr = (pool.fee / 10000).toFixed(2);
  const marginFeeStr = (pool.marginFee / 10000).toFixed(2);

  console.log(`> MARGIN_POSITIONS: ${poolName} (Swap Fee: ${swapFeeStr}% Margin Fee: ${marginFeeStr}%)`);
  console.log(`> Current Price: ${curPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
  console.log(`>`);

  // 4. For each position, get on-chain state
  for (let i = 0; i < items.length; i++) {
    const tokenId = BigInt(items[i].tokenId);

    let posState;
    try {
      posState = await publicClient.readContract({
        address: marginAddr, abi: marginPositionABI,
        functionName: "getPositionState", args: [tokenId],
      });
    } catch (e) {
      console.log(`> Position #${tokenId}: ERROR reading state: ${e.shortMessage || e.message}`);
      continue;
    }

    const marginForOne = posState.marginForOne;
    const marginToken = marginForOne ? pool.currency1 : pool.currency0;
    const borrowToken = marginForOne ? pool.currency0 : pool.currency1;

    const marginAmountF = Number(formatUnits(posState.marginAmount, marginToken.decimals));
    const marginTotalF = Number(formatUnits(posState.marginTotal, marginToken.decimals));
    const debtAmountF = Number(formatUnits(posState.debtAmount, borrowToken.decimals));

    const dirLabel = marginForOne
      ? `Long ${pool.currency1.symbol} · Short ${pool.currency0.symbol}`
      : `Short ${pool.currency1.symbol} · Long ${pool.currency0.symbol}`;

    // Borrow APR: borrowForOne = !marginForOne
    const apr = marginForOne ? apr0 : apr1;
    const aprPercent = (Number(apr) / 10000).toFixed(2);

    // Liquidation price = (marginAmount + marginTotal) / (debtAmount * 1.1)
    // Always in currency0 per currency1
    const liquidationLevel = 1.1;
    let liqPrice;
    if (!marginForOne) {
      liqPrice = (marginAmountF + marginTotalF) / (debtAmountF * liquidationLevel);
    } else {
      liqPrice = (debtAmountF * liquidationLevel) / (marginAmountF + marginTotalF);
    }

    // Margin Level = (marginAmount + marginTotal) / debtValue_in_margin_currency
    // For short (margin=c0, debt=c1): debtValue = debtAmount * curPrice
    // For long  (margin=c1, debt=c0): debtValue = debtAmount / curPrice (= debtAmount * (1/curPrice))
    let debtValueInMargin;
    if (!marginForOne) {
      // debt is currency1, margin is currency0. debt unit ≠ price unit → debt * curPrice
      debtValueInMargin = debtAmountF * curPrice;
    } else {
      // debt is currency0, margin is currency1. debt unit = price unit → debt * (1/curPrice)
      debtValueInMargin = debtAmountF / curPrice;
    }
    const marginLevel = (marginAmountF + marginTotalF) / debtValueInMargin;

    // Estimated PNL
    // debt unit ≠ price unit: PNL = marginTotal - (debt * curPrice)
    // debt unit = price unit:  PNL = marginTotal - (debt * 1/curPrice)
    let pnl;
    if (!marginForOne) {
      // Short: margin=c0(ETH), debt=c1(LIKWID). Price=c0/c1. debt unit(c1) ≠ price unit(c0)
      pnl = marginTotalF - (debtAmountF * curPrice);
    } else {
      // Long: margin=c1(LIKWID), debt=c0(ETH). Price=c0/c1. debt unit(c0) = price unit(c0)
      pnl = marginTotalF - (debtAmountF / curPrice);
    }

    console.log(`> Position #${tokenId}`);
    console.log(`> ${dirLabel}`);
    console.log(`> Margin Amount:   ${marginAmountF} ${marginToken.symbol}`);
    console.log(`> Margin Total:    ${marginTotalF} ${marginToken.symbol}`);
    console.log(`> Debt:            ${debtAmountF} ${borrowToken.symbol}`);
    console.log(`> Borrow APY:      ${aprPercent}%`);
    console.log(`> Liq.Price:       ${liqPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
    console.log(`> Cur.Price:       ${curPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
    console.log(`> Margin Level:    ${marginLevel.toFixed(2)}`);
    console.log(`> Estimated PNL:   ${pnl >= 0 ? "+" : ""}${pnl.toFixed(8)} ${marginToken.symbol}`);
    if (i < items.length - 1) console.log(`>`);
  }
}

// ======================= MARGIN CLOSE =======================

function parseMarginCloseArgs(tokenIdStr, percentStr) {
  if (!tokenIdStr || !percentStr) return null;
  const tokenId = BigInt(tokenIdStr);
  const percent = parseInt(percentStr);
  if (isNaN(percent) || percent < 1 || percent > 100) {
    console.log(`> ERROR: Percent must be 1-100 (got "${percentStr}").`);
    return null;
  }
  return { tokenId, percent };
}

async function computeClosePreview(publicClient, netConfig, pool, poolId, tokenId, percent) {
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const helperABI = loadABI("LikwidHelper");
  const helperAddr = netConfig.contracts.LikwidHelper;
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  // 1. Read position state
  const posState = await publicClient.readContract({
    address: marginAddr, abi: marginPositionABI,
    functionName: "getPositionState", args: [tokenId],
  });
  if (posState.debtAmount === 0n) throw new Error("Position has no debt (already closed).");

  const marginForOne = posState.marginForOne;
  const { marginAmount, marginTotal, debtAmount } = posState;
  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const borrowToken = marginForOne ? pool.currency0 : pool.currency1;

  // 2. Pool state for current price
  const stateInfo = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getPoolStateInfo", args: [poolId],
  });
  const r0 = Number(formatUnits(stateInfo.pairReserve0, pool.currency0.decimals));
  const r1 = Number(formatUnits(stateInfo.pairReserve1, pool.currency1.decimals));
  const curPrice = r0 / r1;

  // 3. Close calculations
  const positionValue = marginAmount + marginTotal;
  const releaseAmount = positionValue * BigInt(percent) / 100n;
  const repayAmount = (debtAmount * BigInt(percent) + 99n) / 100n;

  // Cost to repay debt: getAmountIn(!marginForOne, repayAmount, dynamicFee=false)
  const costResult = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getAmountIn", args: [poolId, !marginForOne, repayAmount, false],
  });
  const costAmount = costResult[0];

  const closeAmount = releaseAmount > costAmount ? releaseAmount - costAmount : 0n;
  const marginScaled = marginAmount * BigInt(percent) / 100n;
  const pnlNegative = closeAmount < marginScaled;
  const pnlValue = pnlNegative ? marginScaled - closeAmount : closeAmount - marginScaled;

  // 4. Liquidation price & margin level
  const marginAmtF = Number(formatUnits(marginAmount, marginToken.decimals));
  const marginTotalF = Number(formatUnits(marginTotal, marginToken.decimals));
  const debtAmountF = Number(formatUnits(debtAmount, borrowToken.decimals));
  const liquidationLevel = 1.1;

  let liqPrice;
  if (!marginForOne) {
    liqPrice = (marginAmtF + marginTotalF) / (debtAmountF * liquidationLevel);
  } else {
    liqPrice = (debtAmountF * liquidationLevel) / (marginAmtF + marginTotalF);
  }

  let debtValueInMargin;
  if (!marginForOne) {
    debtValueInMargin = debtAmountF * curPrice;
  } else {
    debtValueInMargin = debtAmountF / curPrice;
  }
  const marginLevel = (marginAmtF + marginTotalF) / debtValueInMargin;

  return {
    marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    releaseAmount, repayAmount, costAmount, closeAmount,
    pnlNegative, pnlValue, liqPrice, curPrice, marginLevel,
  };
}

function printClosePreview(pool, tokenId, percent, slippage, preview) {
  const { marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    repayAmount, closeAmount, pnlNegative, pnlValue,
    liqPrice, curPrice, marginLevel } = preview;

  const dirLabel = marginForOne
    ? `Long ${pool.currency1.symbol} (Short ${pool.currency0.symbol})`
    : `Short ${pool.currency1.symbol} (Long ${pool.currency0.symbol})`;
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;
  const swapFeeStr = (pool.fee / 10000).toFixed(1);
  const marginFeeStr = (pool.marginFee / 10000).toFixed(1);
  const closeAmountMin = closeAmount * BigInt(100 - slippage) / 100n;

  console.log(`>`);
  console.log(`> MARGIN CLOSE PREVIEW`);
  console.log(`> Pool: ${poolName} Swap Fee: ${swapFeeStr}% Margin Fee: ${marginFeeStr}%`);
  console.log(`> ${dirLabel}`);
  console.log(`> Position #${tokenId}`);
  console.log(`>`);
  console.log(`> Margin Amount:   ${formatUnits(marginAmount, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Margin Total:    ${formatUnits(marginTotal, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Debt:            ${formatUnits(debtAmount, borrowToken.decimals)} ${borrowToken.symbol}`);
  console.log(`> Liq.Price:       ${liqPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
  console.log(`> Cur.Price:       ${curPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
  console.log(`> Margin Level:    ${marginLevel.toFixed(2)}`);
  console.log(`>`);
  console.log(`> --- Close Scale ${percent}% ---`);
  console.log(`> Close Debt:      ${formatUnits(repayAmount, borrowToken.decimals)} ${borrowToken.symbol}`);
  console.log(`> Estimated PNL:   ${pnlNegative ? "-" : "+"}${formatUnits(pnlValue, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Max Slippage:    ${slippage}%`);
  console.log(`> Min. Received:   ${formatUnits(closeAmountMin, marginToken.decimals)} ${marginToken.symbol}`);
}

async function cmd_margin_close_quote(poolStr, tokenIdStr, percentStr, slippageStr = "1") {
  if (!poolStr || !tokenIdStr || !percentStr) {
    console.log(`> Usage: margin_close_quote <pool> <tokenId> <percent> [slippage%]`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> Percent: 1-100 (% of position to close)`);
    console.log(`> Default slippage: 1%`);
    return;
  }

  const parsed = parseMarginCloseArgs(tokenIdStr, percentStr);
  if (!parsed) return;
  const { tokenId, percent } = parsed;
  const slippage = parseInt(slippageStr) || 1;

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);
  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const clients = createClients(config, netConfig);
  if (!clients) return;

  try {
    const preview = await computeClosePreview(clients.publicClient, netConfig, pool, poolId, tokenId, percent);
    printClosePreview(pool, tokenId, percent, slippage, preview);
  } catch (e) {
    console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }
}

async function cmd_margin_close(poolStr, tokenIdStr, percentStr, slippageStr = "1") {
  if (!poolStr || !tokenIdStr || !percentStr) {
    console.log(`> Usage: margin_close <pool> <tokenId> <percent> [slippage%]`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> Percent: 1-100 (% of position to close)`);
    console.log(`> Default slippage: 1%`);
    return;
  }

  const parsed = parseMarginCloseArgs(tokenIdStr, percentStr);
  if (!parsed) return;
  const { tokenId, percent } = parsed;
  const closeMillionth = percent * 10000;
  const slippage = parseInt(slippageStr) || 1;

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  // Preview
  let preview;
  try {
    preview = await computeClosePreview(publicClient, netConfig, pool, poolId, tokenId, percent);
    printClosePreview(pool, tokenId, percent, slippage, preview);
  } catch (e) {
    return console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }

  const closeAmountMin = preview.closeAmount * BigInt(100 - slippage) / 100n;
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  const calls = [{
    to: marginAddr,
    value: 0n,
    data: encodeFunctionData({
      abi: marginPositionABI,
      functionName: "close",
      args: [tokenId, closeMillionth, closeAmountMin, deadline],
    }),
  }];

  console.log(`>`);
  console.log(`> Executing margin close...`);
  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
}

// ======================= MARGIN REPAY =======================

async function computeRepayPreview(publicClient, netConfig, pool, poolId, tokenId, repayAmountStr) {
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const helperABI = loadABI("LikwidHelper");
  const helperAddr = netConfig.contracts.LikwidHelper;
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  const posState = await publicClient.readContract({
    address: marginAddr, abi: marginPositionABI,
    functionName: "getPositionState", args: [tokenId],
  });
  if (posState.debtAmount === 0n) throw new Error("Position has no debt (already closed).");

  const marginForOne = posState.marginForOne;
  const { marginAmount, marginTotal, debtAmount } = posState;
  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const borrowToken = marginForOne ? pool.currency0 : pool.currency1;

  // Parse repay amount, cap at debt
  let repayAmount = parseUnits(repayAmountStr, borrowToken.decimals);
  const cappedAtDebt = repayAmount > debtAmount;
  if (cappedAtDebt) repayAmount = debtAmount;

  // Release estimate: proportional to repay/debt
  const positionValue = marginAmount + marginTotal;
  const releaseAmount = repayAmount >= debtAmount
    ? positionValue
    : positionValue * repayAmount / debtAmount;

  // Pool state for current price
  const stateInfo = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getPoolStateInfo", args: [poolId],
  });
  const r0 = Number(formatUnits(stateInfo.pairReserve0, pool.currency0.decimals));
  const r1 = Number(formatUnits(stateInfo.pairReserve1, pool.currency1.decimals));
  const curPrice = r0 / r1;

  // After repay state
  const debtAfter = debtAmount - repayAmount;
  const marginAfter = marginAmount > releaseAmount ? marginAmount - releaseAmount : 0n;
  const marginTotalAfter = marginTotal > (releaseAmount > marginAmount ? releaseAmount - marginAmount : 0n)
    ? marginTotal - (releaseAmount > marginAmount ? releaseAmount - marginAmount : 0n)
    : 0n;

  return {
    marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    repayAmount, cappedAtDebt, releaseAmount,
    debtAfter, curPrice,
  };
}

function printRepayPreview(pool, tokenId, preview) {
  const { marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    repayAmount, cappedAtDebt, releaseAmount,
    debtAfter, curPrice } = preview;

  const dirLabel = marginForOne
    ? `Long ${pool.currency1.symbol} (Short ${pool.currency0.symbol})`
    : `Short ${pool.currency1.symbol} (Long ${pool.currency0.symbol})`;
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;
  const swapFeeStr = (pool.fee / 10000).toFixed(1);
  const marginFeeStr = (pool.marginFee / 10000).toFixed(1);

  console.log(`>`);
  console.log(`> MARGIN REPAY PREVIEW`);
  console.log(`> Pool: ${poolName} Swap Fee: ${swapFeeStr}% Margin Fee: ${marginFeeStr}%`);
  console.log(`> ${dirLabel}`);
  console.log(`> Position #${tokenId}`);
  console.log(`>`);
  console.log(`> Margin Amount:   ${formatUnits(marginAmount, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Margin Total:    ${formatUnits(marginTotal, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Debt:            ${formatUnits(debtAmount, borrowToken.decimals)} ${borrowToken.symbol}`);
  console.log(`> Cur.Price:       ${curPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
  console.log(`>`);
  console.log(`> --- Repay ---`);
  console.log(`> Repay Amount:    ${formatUnits(repayAmount, borrowToken.decimals)} ${borrowToken.symbol}${cappedAtDebt ? " (capped at debt)" : ""}`);
  console.log(`> Release:         ~${formatUnits(releaseAmount, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Debt After:      ${formatUnits(debtAfter, borrowToken.decimals)} ${borrowToken.symbol}`);
}

async function cmd_margin_repay_quote(poolStr, tokenIdStr, amountStr) {
  if (!poolStr || !tokenIdStr || !amountStr) {
    console.log(`> Usage: margin_repay_quote <pool> <tokenId> <amount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> amount: repay amount in borrow currency (capped at debt)`);
    return;
  }

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);
  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const clients = createClients(config, netConfig);
  if (!clients) return;

  try {
    const preview = await computeRepayPreview(clients.publicClient, netConfig, pool, poolId, BigInt(tokenIdStr), amountStr);
    printRepayPreview(pool, BigInt(tokenIdStr), preview);
  } catch (e) {
    console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }
}

async function cmd_margin_repay(poolStr, tokenIdStr, amountStr) {
  if (!poolStr || !tokenIdStr || !amountStr) {
    console.log(`> Usage: margin_repay <pool> <tokenId> <amount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> amount: repay amount in borrow currency (capped at debt)`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const tokenId = BigInt(tokenIdStr);
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  // Preview
  let preview;
  try {
    preview = await computeRepayPreview(publicClient, netConfig, pool, poolId, tokenId, amountStr);
    printRepayPreview(pool, tokenId, preview);
  } catch (e) {
    return console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }

  const { repayAmount, borrowToken } = preview;
  const sendingNative = isNative(borrowToken.address);
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  const calls = [];

  // Approve if repaying with ERC20
  if (!sendingNative) {
    calls.push(...await buildApprovalCalls(publicClient, senderAddress, borrowToken.address, borrowToken.symbol, marginAddr, repayAmount));
  }

  calls.push({
    to: marginAddr,
    value: sendingNative ? repayAmount : 0n,
    data: encodeFunctionData({
      abi: marginPositionABI,
      functionName: "repay",
      args: [tokenId, repayAmount, deadline],
    }),
  });

  console.log(`>`);
  console.log(`> Executing margin repay...`);
  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);
}

// ======================= MARGIN MODIFY (Adjust Margin) =======================

const MIN_BORROW_LEVEL = 1.4; // marginLevels.minBorrowLevel() = 1400000 / 1e6

async function computeModifyPreview(publicClient, netConfig, pool, poolId, tokenId, changeAmountStr) {
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const helperABI = loadABI("LikwidHelper");
  const helperAddr = netConfig.contracts.LikwidHelper;
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  const posState = await publicClient.readContract({
    address: marginAddr, abi: marginPositionABI,
    functionName: "getPositionState", args: [tokenId],
  });
  if (posState.debtAmount === 0n) throw new Error("Position has no debt (already closed).");

  const marginForOne = posState.marginForOne;
  const { marginAmount, marginTotal, debtAmount } = posState;
  const marginToken = marginForOne ? pool.currency1 : pool.currency0;
  const borrowToken = marginForOne ? pool.currency0 : pool.currency1;

  // Pool state for current price
  const stateInfo = await publicClient.readContract({
    address: helperAddr, abi: helperABI,
    functionName: "getPoolStateInfo", args: [poolId],
  });
  const r0 = Number(formatUnits(stateInfo.pairReserve0, pool.currency0.decimals));
  const r1 = Number(formatUnits(stateInfo.pairReserve1, pool.currency1.decimals));
  const curPrice = r0 / r1;

  // Current margin level
  const marginAmtF = Number(formatUnits(marginAmount, marginToken.decimals));
  const marginTotalF = Number(formatUnits(marginTotal, marginToken.decimals));
  const debtAmountF = Number(formatUnits(debtAmount, borrowToken.decimals));

  let debtValueInMargin;
  if (!marginForOne) {
    debtValueInMargin = debtAmountF * curPrice;
  } else {
    debtValueInMargin = debtAmountF / curPrice;
  }
  const currentMarginLevel = (marginAmtF + marginTotalF) / debtValueInMargin;

  // Decrease max: after decrease, margin level >= 1.4
  // (marginAmount - decreaseMax + marginTotal) / debtValueInMargin >= 1.4
  // decreaseMax = marginAmount + marginTotal - 1.4 * debtValueInMargin
  const decreaseMaxF = marginAmtF + marginTotalF - MIN_BORROW_LEVEL * debtValueInMargin;
  const decreaseMax = decreaseMaxF > 0
    ? parseUnits(decreaseMaxF.toFixed(marginToken.decimals), marginToken.decimals)
    : 0n;

  // Parse change amount (positive or negative)
  const isDecrease = changeAmountStr.startsWith("-");
  const absStr = isDecrease ? changeAmountStr.slice(1) : changeAmountStr;
  let absAmount = parseUnits(absStr, marginToken.decimals);

  // Cap decrease at decreaseMax
  let cappedAtMax = false;
  if (isDecrease && absAmount > decreaseMax) {
    absAmount = decreaseMax;
    cappedAtMax = true;
  }

  const changeAmount = isDecrease ? -absAmount : absAmount;

  // New margin level after change
  const changeF = Number(formatUnits(changeAmount, marginToken.decimals));
  const newMarginLevel = (marginAmtF + changeF + marginTotalF) / debtValueInMargin;

  return {
    marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    curPrice, currentMarginLevel, newMarginLevel,
    changeAmount, absAmount, isDecrease, cappedAtMax, decreaseMax,
  };
}

function printModifyPreview(pool, tokenId, preview) {
  const { marginForOne, marginToken, borrowToken,
    marginAmount, marginTotal, debtAmount,
    curPrice, currentMarginLevel, newMarginLevel,
    changeAmount, absAmount, isDecrease, cappedAtMax, decreaseMax } = preview;

  const dirLabel = marginForOne
    ? `Long ${pool.currency1.symbol} (Short ${pool.currency0.symbol})`
    : `Short ${pool.currency1.symbol} (Long ${pool.currency0.symbol})`;
  const poolName = `${pool.currency0.symbol}/${pool.currency1.symbol}`;
  const swapFeeStr = (pool.fee / 10000).toFixed(1);
  const marginFeeStr = (pool.marginFee / 10000).toFixed(1);
  const action = isDecrease ? "Decrease" : "Increase";

  console.log(`>`);
  console.log(`> MARGIN MODIFY PREVIEW`);
  console.log(`> Pool: ${poolName} Swap Fee: ${swapFeeStr}% Margin Fee: ${marginFeeStr}%`);
  console.log(`> ${dirLabel}`);
  console.log(`> Position #${tokenId}`);
  console.log(`>`);
  console.log(`> Margin Amount:   ${formatUnits(marginAmount, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Margin Total:    ${formatUnits(marginTotal, marginToken.decimals)} ${marginToken.symbol}`);
  console.log(`> Debt:            ${formatUnits(debtAmount, borrowToken.decimals)} ${borrowToken.symbol}`);
  console.log(`> Cur.Price:       ${curPrice.toFixed(8)} ${pool.currency0.symbol} per ${pool.currency1.symbol}`);
  console.log(`> Margin Level:    ${currentMarginLevel.toFixed(2)}`);
  console.log(`>`);
  console.log(`> --- ${action} Margin ---`);
  console.log(`> ${action} Amount:  ${formatUnits(absAmount, marginToken.decimals)} ${marginToken.symbol}${cappedAtMax ? " (capped at max)" : ""}`);
  if (isDecrease) {
    console.log(`> Decrease Max:    ${formatUnits(decreaseMax, marginToken.decimals)} ${marginToken.symbol} (min level: ${MIN_BORROW_LEVEL})`);
  }
  console.log(`> New Margin Level: ${newMarginLevel.toFixed(2)}`);
}

async function cmd_margin_modify_quote(poolStr, tokenIdStr, changeAmountStr) {
  if (!poolStr || !tokenIdStr || !changeAmountStr) {
    console.log(`> Usage: margin_modify_quote <pool> <tokenId> <changeAmount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> changeAmount: positive to increase, negative to decrease (e.g. 0.5 or -0.5)`);
    return;
  }

  const config = loadConfig();
  if (!config) return console.log(`> ERROR: Not configured. Run setup first.`);
  const netConfig = await loadNetworkConfig(config.network);
  if (!netConfig) return;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const clients = createClients(config, netConfig);
  if (!clients) return;

  try {
    const preview = await computeModifyPreview(clients.publicClient, netConfig, pool, poolId, BigInt(tokenIdStr), changeAmountStr);
    printModifyPreview(pool, BigInt(tokenIdStr), preview);
  } catch (e) {
    console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }
}

async function cmd_margin_modify(poolStr, tokenIdStr, changeAmountStr) {
  if (!poolStr || !tokenIdStr || !changeAmountStr) {
    console.log(`> Usage: margin_modify <pool> <tokenId> <changeAmount>`);
    console.log(`> Pool: token pair (e.g. ETH/LIKWID)`);
    console.log(`> tokenId: margin position NFT ID`);
    console.log(`> changeAmount: positive to increase, negative to decrease (e.g. 0.5 or -0.5)`);
    return;
  }

  const ctx = await resolveContext();
  if (!ctx) return;
  const { config, netConfig, eoaAccount, publicClient, senderAddress } = ctx;

  const pool = resolvePool(netConfig, poolStr);
  if (!pool) return console.log(`> ERROR: Pool "${poolStr}" not found. Run "pools" to list.`);

  const poolId = computePoolId(pool);
  const tokenId = BigInt(tokenIdStr);
  const marginPositionABI = loadABI("LikwidMarginPosition");
  const marginAddr = netConfig.contracts.LikwidMarginPosition;

  // Preview
  let preview;
  try {
    preview = await computeModifyPreview(publicClient, netConfig, pool, poolId, tokenId, changeAmountStr);
    printModifyPreview(pool, tokenId, preview);
  } catch (e) {
    return console.log(`> ERROR: ${e.shortMessage || e.message}`);
  }

  const { changeAmount, absAmount, isDecrease, marginToken } = preview;
  if (absAmount === 0n) return console.log(`> ERROR: Change amount is 0. Nothing to do.`);

  const sendingNative = isNative(marginToken.address);
  const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);

  const calls = [];

  // Approve if increasing with ERC20
  if (!isDecrease && !sendingNative) {
    calls.push(...await buildApprovalCalls(publicClient, senderAddress, marginToken.address, marginToken.symbol, marginAddr, absAmount));
  }

  calls.push({
    to: marginAddr,
    value: (!isDecrease && sendingNative) ? absAmount : 0n,
    data: encodeFunctionData({
      abi: marginPositionABI,
      functionName: "modify",
      args: [tokenId, changeAmount, deadline],
    }),
  });

  console.log(`>`);
  console.log(`> Executing margin modify...`);
  await executeCalls(config, netConfig, eoaAccount, publicClient, calls);

  // Show updated position state
  try {
    const posState = await publicClient.readContract({
      address: marginAddr, abi: marginPositionABI,
      functionName: "getPositionState", args: [tokenId],
    });
    const marginToken = preview.marginForOne ? pool.currency1 : pool.currency0;
    const borrowToken = preview.marginForOne ? pool.currency0 : pool.currency1;
    const helperABI = loadABI("LikwidHelper");
    const stateInfo = await publicClient.readContract({
      address: netConfig.contracts.LikwidHelper, abi: helperABI,
      functionName: "getPoolStateInfo", args: [poolId],
    });
    const r0 = Number(formatUnits(stateInfo.pairReserve0, pool.currency0.decimals));
    const r1 = Number(formatUnits(stateInfo.pairReserve1, pool.currency1.decimals));
    const curPrice = r0 / r1;

    const mAmt = Number(formatUnits(posState.marginAmount, marginToken.decimals));
    const mTot = Number(formatUnits(posState.marginTotal, marginToken.decimals));
    const debt = Number(formatUnits(posState.debtAmount, borrowToken.decimals));
    let debtVal;
    if (!preview.marginForOne) {
      debtVal = debt * curPrice;
    } else {
      debtVal = debt / curPrice;
    }
    const newLevel = (mAmt + mTot) / debtVal;

    console.log(`>`);
    console.log(`> Updated Position #${tokenId}:`);
    console.log(`> Margin Amount:   ${formatUnits(posState.marginAmount, marginToken.decimals)} ${marginToken.symbol}`);
    console.log(`> Margin Level:    ${newLevel.toFixed(2)}`);
  } catch (_) {
    // Non-critical: position state refresh failed
  }
}

// ======================= CLI ROUTER =======================

if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command) {
    console.log(`Likwid.fi Protocol Universal Skill — Powered by https://likwid.fi

Usage: node likwid-fi.js <command> [args]

Setup:
  setup <network> <keyFile>                 Configure wallet and network.
                                            Networks: sepolia, ethereum, base
  account                                   Show current account info and balances.

Pool Info:
  pools                                     List available pools on current network.
  pool_info <pool>                          Query on-chain pool state (reserves, rate).
  quote <pool> <dir> <amount>               Get swap quote. dir: sell0|sell1|buy0|buy1

DeFi Actions:
  swap <pool> <dir> <amount> [slippage%]    Execute swap. dir: sell0|sell1|buy0|buy1
  lp_add <pool> <currency> <amt> [slip%]    Add or increase liquidity. currency: 0 or 1.
  lp_positions <pool>                       Show your liquidity positions.
  lp_remove <pool> [percent]                Remove liquidity. Default: 100% (all).
  create_pair <t0> <t1> <fee> <marginFee>   Create a new pool. Tokens by name or address.

Margin Trading:
  margin_quote <pool> <dir> <lev> <amt>     Preview margin position without executing.
  margin_open  <pool> <dir> <lev> <amt>     Open or increase a margin position.
  margin_positions <pool>                   Show your margin positions.
  margin_close_quote <pool> <id> <pct> [s%]  Preview margin close without executing.
  margin_close <pool> <id> <pct> [slip%]    Close (partially) a margin position. pct: 1-100
  margin_repay_quote <pool> <id> <amt>      Preview margin repay without executing.
  margin_repay <pool> <id> <amt>            Repay debt on a margin position.
  margin_modify_quote <pool> <id> <chg>    Preview margin adjust (+ increase, - decrease).
  margin_modify <pool> <id> <chg>          Adjust margin on a position (e.g. 0.5 or -0.5).

Arguments:
  <pool>      Token pair (e.g. ETH/USDT). Lowest fee tier selected by default.
  <dir>       Swap direction: 0to1 or 1to0
  <amount>    Human-readable amount (e.g., "0.01", "100")
  [slippage]  Slippage tolerance in % (default: 1)
`);
    process.exit(0);
  }

  (async () => {
    console.log(`> Powered by https://likwid.fi`);
    try {
      switch (command) {
        case "setup":
          await cmd_setup(args[1], args[2]);
          break;
        case "account":
          await cmd_account();
          break;
        case "pools":
          await cmd_pools();
          break;
        case "quote":
          await cmd_quote(args[1], args[2], args[3]);
          break;
        case "pool_info":
          await cmd_pool_info(args[1]);
          break;
        case "swap":
          await cmd_swap(args[1], args[2], args[3], args[4]);
          break;
        case "lp_add":
          await cmd_lp_add(args[1], args[2], args[3], args[4]);
          break;
        case "lp_positions":
          await cmd_lp_positions(args[1]);
          break;
        case "lp_remove":
          await cmd_lp_remove(args[1], args[2]);
          break;
        case "create_pair":
          await cmd_create_pair(args[1], args[2], args[3], args[4]);
          break;
        case "margin_quote":
          await cmd_margin_quote(args[1], args[2], args[3], args[4]);
          break;
        case "margin_open":
          await cmd_margin_open(args[1], args[2], args[3], args[4]);
          break;
        case "margin_positions":
          await cmd_margin_positions(args[1]);
          break;
        case "margin_close_quote":
          await cmd_margin_close_quote(args[1], args[2], args[3], args[4]);
          break;
        case "margin_close":
          await cmd_margin_close(args[1], args[2], args[3], args[4]);
          break;
        case "margin_repay_quote":
          await cmd_margin_repay_quote(args[1], args[2], args[3]);
          break;
        case "margin_repay":
          await cmd_margin_repay(args[1], args[2], args[3]);
          break;
        case "margin_modify_quote":
          await cmd_margin_modify_quote(args[1], args[2], args[3]);
          break;
        case "margin_modify":
          await cmd_margin_modify(args[1], args[2], args[3]);
          break;
        default:
          console.log(`> Unknown command: ${command}`);
          console.log(`> Run without arguments to see usage.`);
      }
    } catch (e) {
      console.log(`> FATAL: ${e.message}`);
    }
    process.exit(0);
  })();
}

module.exports = { computePoolId, loadConfig, loadNetworkConfig, loadCachedNetworkConfig };
