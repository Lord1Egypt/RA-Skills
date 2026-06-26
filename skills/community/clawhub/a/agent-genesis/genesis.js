/**
 * genesis.js — Agent Genesis: Self-contained wallet management & AGC mining workflow.
 *
 * Provides: wallet setup, PoA challenge/verify, mining, vesting, status.
 * Includes all infrastructure: viem clients, ERC-4337 smart account, bundler, UserOp execution.
 */

const {
  createPublicClient,
  createWalletClient,
  http,
  parseEther,
  encodeFunctionData,
  parseAbi,
  toFunctionSelector,
  keccak256,
  encodeAbiParameters,
} = require("viem");
const { signAuthorization } = require("viem/actions");
const { toSimple7702SmartAccount, createBundlerClient } = require("viem/account-abstraction");
const { base } = require("viem/chains");
const { privateKeyToAccount, generatePrivateKey } = require("viem/accounts");
const fs = require("fs");
const path = require("path");
const os = require("os");
const axios = require("axios");
const { ReclaimClient } = require("@reclaimprotocol/zk-fetch");

// ======================= CONFIGURATION =======================
const CHAIN = base;
const NETWORK_NAME = CHAIN.name;
const CHAIN_ID = CHAIN.id;

const VERIFIER_URL = "https://verifier.likwid.fi";
const RPC_URL = process.env.RPC_URL || "https://mainnet.base.org";
const BUNDLER_URL = process.env.BUNDLER_URL || "https://api.candide.dev/public/v3/base";

const WALLET_FILE = path.join(os.homedir(), ".openclaw", ".likwid_genesis_wallet.json");
const NATIVE_TOKEN_ADDRESS = "0x0000000000000000000000000000000000000000";

const AGC_TOKEN_ADDRESS = process.env.AGC_TOKEN_ADDRESS || "0x26DbB1b6F7455414D796eE3AbdA8C8A94c15f27A";
const AGENT_PAYMASTER_ADDRESS = process.env.AGENT_PAYMASTER_ADDRESS || "0xBe178629bdC7b5F165F91B6c439de4078955f7e3";

const SIMPLE_7702_IMPLEMENTATION = "0xa46cc63eBF4Bd77888AA327837d20b23A63a56B5";

// Likwid Helper — used for pool price queries (cost calculation, AGC precharge estimation)
const LIKWID_HELPER_ADDRESS = process.env.LIKWID_HELPER_ADDRESS || "0x16a9633f8A777CA733073ea2526705cD8338d510";

const POOL_KEY = {
  currency0: NATIVE_TOKEN_ADDRESS,
  currency1: AGC_TOKEN_ADDRESS,
  fee: 3000,
  marginFee: 3000,
};

const POOL_ID = keccak256(
  encodeAbiParameters(
    [
      { name: "currency0", type: "address" },
      { name: "currency1", type: "address" },
      { name: "fee", type: "uint24" },
      { name: "marginFee", type: "uint24" },
    ],
    [POOL_KEY.currency0, POOL_KEY.currency1, POOL_KEY.fee, POOL_KEY.marginFee],
  ),
);

// ======================= ABIs =======================
const ERC20_ABI = parseAbi([
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function balanceOf(address account) external view returns (uint256)",
]);

const AGC_MINE_ABI = parseAbi([
  "function mine(uint256 score, bytes calldata signature, uint256 nonce) external payable",
]);

const AGC_MINE_SELECTOR = toFunctionSelector(AGC_MINE_ABI[0]);

const AGENT_PAYMASTER_ABI = parseAbi(["function hasFreeMined(address user) external view returns (bool)"]);

const LIKWID_HELPER_ABI = parseAbi([
  "function getAmountOut(bytes32 poolId, bool zeroForOne, uint256 amountIn, bool dynamicFee) external view returns (uint256 amountOut, uint24 fee, uint256 feeAmount)",
  "function getAmountIn(bytes32 poolId, bool zeroForOne, uint256 amountOut, bool dynamicFee) external view returns (uint256 amountIn, uint24 fee, uint256 feeAmount)",
  "function checkMarginPositionLiquidate(uint256 tokenId) external view returns (bool liquidated)",
  "function getPoolStateInfo(bytes32 poolId) external view returns ((uint128 totalSupply, uint32 lastUpdated, uint24 lpFee, uint24 marginFee, uint24 protocolFee, uint128 realReserve0, uint128 realReserve1, uint128 mirrorReserve0, uint128 mirrorReserve1, uint128 pairReserve0, uint128 pairReserve1, uint128 truncatedReserve0, uint128 truncatedReserve1, uint128 lendReserve0, uint128 lendReserve1, uint128 interestReserve0, uint128 interestReserve1, int128 insuranceFund0, int128 insuranceFund1, uint256 borrow0CumulativeLast, uint256 borrow1CumulativeLast, uint256 deposit0CumulativeLast, uint256 deposit1CumulativeLast) stateInfo)",
]);

// ======================= CLIENTS =======================
const publicClient = createPublicClient({
  chain: CHAIN,
  transport: http(RPC_URL),
});

// ======================= BUNDLER =======================

const bundlerTransport = http(BUNDLER_URL);

async function getBundlerGasPrice() {
  const fees = await publicClient.estimateFeesPerGas();
  const floor = 10_000_000n; // 0.01 gwei floor
  return {
    maxFeePerGas: fees.maxFeePerGas > floor ? fees.maxFeePerGas : floor,
    maxPriorityFeePerGas: fees.maxPriorityFeePerGas > floor ? fees.maxPriorityFeePerGas : floor,
  };
}

async function getEip7702Authorization(signer) {
  const code = await publicClient.getCode({ address: signer.address });
  const isDelegated = code && code !== "0x" && code.startsWith("0xef0100");
  if (isDelegated) return null;

  console.log("> Signing EIP-7702 authorization (first-time delegation)...");
  const walletClient = createWalletClient({ account: signer, chain: CHAIN, transport: http(RPC_URL) });
  return signAuthorization(walletClient, { contractAddress: SIMPLE_7702_IMPLEMENTATION });
}

// ======================= WALLET & ACCOUNT =======================

function getWalletInstance() {
  if (fs.existsSync(WALLET_FILE)) {
    const data = JSON.parse(fs.readFileSync(WALLET_FILE, "utf8"));
    let pk = data.privateKey;
    if (!pk.startsWith("0x")) pk = "0x" + pk;
    return privateKeyToAccount(pk);
  }
  return null;
}

async function getSmartAccount(signer) {
  const smartAccount = await toSimple7702SmartAccount({
    client: publicClient,
    owner: signer,
    implementation: SIMPLE_7702_IMPLEMENTATION,
    entryPoint: "0.9",
  });

  const client = createBundlerClient({
    account: smartAccount,
    client: publicClient,
    transport: bundlerTransport,
    userOperation: {
      estimateFeesPerGas: getBundlerGasPrice,
    },
  });

  return { smartAccount, bundlerClient: client };
}

// ======================= HELPERS =======================

function formatError(msg) {
  console.log(JSON.stringify({ error: msg }, null, 2));
}

function formatHumanSeconds(seconds) {
  const s = Number(seconds);
  if (s <= 0) return "0s";
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${s % 60}s`;
  return `${s}s`;
}

function formatTokenAmount(value) {
  return (Number(value) / 1e18).toFixed(6);
}

function parseCliErrorFields(message) {
  return Object.fromEntries(
    message
      .split("|")
      .slice(1)
      .map((entry) => {
        const [key, value] = entry.split("=");
        return [key, value];
      }),
  );
}

function sanitizeCliField(value) {
  return String(value).replace(/\|/g, "/").replace(/\s+/g, " ").trim();
}

function isFreeMineCall(call) {
  return (
    call &&
    call.to &&
    typeof call.to === "string" &&
    call.to.toLowerCase() === AGC_TOKEN_ADDRESS.toLowerCase() &&
    typeof call.data === "string" &&
    call.data.startsWith(AGC_MINE_SELECTOR)
  );
}

function isFreeMineOperation(calls) {
  if (!Array.isArray(calls)) {
    return isFreeMineCall(calls);
  }
  return calls.length > 0 && calls.every(isFreeMineCall);
}

function getOperationRequiredEth(calls) {
  const callList = Array.isArray(calls) ? calls : [calls];
  return callList.reduce((sum, call) => sum + BigInt(call?.value ?? 0n), 0n);
}

function maxBigInt(...values) {
  return values.reduce((max, value) => (value > max ? value : max), 0n);
}

async function estimateAgcPrechargeFromRequiredEth(requiredEthPrefund) {
  if (!requiredEthPrefund || requiredEthPrefund <= 0n) return 0n;

  const reserveQuote = await getAgcQuoteFromReserves(requiredEthPrefund);
  const spotQuote = await getAgcQuoteFromSpot(requiredEthPrefund);
  let helperQuote = 0n;

  try {
    const res = await publicClient.readContract({
      address: LIKWID_HELPER_ADDRESS,
      abi: LIKWID_HELPER_ABI,
      functionName: "getAmountIn",
      args: [POOL_ID, false, requiredEthPrefund, true],
    });
    helperQuote = (BigInt(res[0]) * 110n) / 100n;
  } catch {
    helperQuote = 0n;
  }

  return maxBigInt(helperQuote, reserveQuote, spotQuote);
}

async function getAgcQuoteFromReserves(requiredEthPrefund) {
  const state = await publicClient.readContract({
    address: LIKWID_HELPER_ADDRESS,
    abi: LIKWID_HELPER_ABI,
    functionName: "getPoolStateInfo",
    args: [POOL_ID],
  });

  const reserveEth = BigInt(state.pairReserve0);
  const reserveAgc = BigInt(state.pairReserve1);
  if (reserveEth === 0n || reserveAgc === 0n) return 0n;

  return (requiredEthPrefund * reserveAgc * 120n) / (reserveEth * 100n);
}

async function getAgcQuoteFromSpot(requiredEthPrefund) {
  const oneEth = 10n ** 18n;
  const res = await publicClient.readContract({
    address: LIKWID_HELPER_ADDRESS,
    abi: LIKWID_HELPER_ABI,
    functionName: "getAmountOut",
    args: [POOL_ID, true, oneEth, true],
  });
  const agcPerEth = BigInt(res[0]);
  if (agcPerEth === 0n) return 0n;

  return (requiredEthPrefund * agcPerEth * 120n) / (oneEth * 100n);
}

function loadEnvConfig() {
  let MODEL_TYPE = process.env.MODEL_TYPE || null;
  let MODEL_KEY = process.env.MODEL_KEY || null;
  try {
    const envPath = path.join(process.cwd(), ".env");
    if (fs.existsSync(envPath)) {
      const envConfig = Object.fromEntries(
        fs
          .readFileSync(envPath, "utf8")
          .split("\n")
          .map((line) => line.match(/^\s*([^=]+?)\s*=(.*)$/))
          .filter(Boolean)
          .map(([, key, val]) => [key, val.trim().replace(/^"|"$/g, "")]),
      );
      MODEL_TYPE = MODEL_TYPE || envConfig.MODEL_TYPE || null;
      MODEL_KEY = MODEL_KEY || envConfig.MODEL_KEY || null;
    }
  } catch (e) {
    // ignore
  }
  return { MODEL_TYPE, MODEL_KEY };
}

// ======================= USER OPERATION =======================

async function runUserOp(signer, bundlerClient, calls, description) {
  let gasPaymentMode = "agc";
  const expectsFreeMine = isFreeMineOperation(calls);
  let canUseFreeMine = false;
  const accountAddress = signer.address; // EIP-7702: EOA = Smart Account

  if (expectsFreeMine) {
    try {
      const hasFreeMined = await publicClient.readContract({
        address: AGENT_PAYMASTER_ADDRESS,
        abi: AGENT_PAYMASTER_ABI,
        functionName: "hasFreeMined",
        args: [accountAddress],
      });
      canUseFreeMine = !hasFreeMined;
    } catch {
      canUseFreeMine = false;
    }
  }

  console.log(`> Packaging UserOperation for ${description}...`);
  try {
    const operationRequiredEth = getOperationRequiredEth(calls);
    const callList = Array.isArray(calls) ? calls : [calls];

    const [ethBalance, agcBalance] = await Promise.all([
      publicClient.getBalance({ address: accountAddress }),
      publicClient.readContract({
        address: AGC_TOKEN_ADDRESS,
        abi: ERC20_ABI,
        functionName: "balanceOf",
        args: [accountAddress],
      }),
    ]);

    // Determine gas payment mode: free mine > ETH direct > AGC paymaster
    if (canUseFreeMine) {
      gasPaymentMode = "free";
    } else if (ethBalance > operationRequiredEth + parseEther("0.00005")) {
      gasPaymentMode = "eth";
    } else {
      // Check AGC balance for paymaster precharge
      const estimatedAgcPrecharge = await estimateAgcPrechargeFromRequiredEth(parseEther("0.005"));
      if (agcBalance < estimatedAgcPrecharge) {
        throw new Error(
          [
            "CLI_INSUFFICIENT_TOTAL_AGC",
            `operation=0.000000`,
            `precharge=${formatTokenAmount(estimatedAgcPrecharge)}`,
            `required=${formatTokenAmount(estimatedAgcPrecharge)}`,
            `available=${formatTokenAmount(agcBalance)}`,
            `shortfall=${formatTokenAmount(estimatedAgcPrecharge - agcBalance)}`,
          ].join("|"),
        );
      }
      gasPaymentMode = "agc";
    }

    console.log(`> Smart account ETH balance: ${Number(ethBalance) / 1e18} ETH`);
    console.log(`> Smart account AGC balance: ${Number(agcBalance) / 1e18} AGC`);

    console.log(
      `> Using ${gasPaymentMode === "free" ? "free mine (paymaster)" : gasPaymentMode === "eth" ? "direct ETH (no EIP-7702)" : "AGC / paymaster"} gas payment...`,
    );

    // --- ETH direct path: send raw transactions, no UserOp / EIP-7702 ---
    if (gasPaymentMode === "eth") {
      const walletClient = createWalletClient({ account: signer, chain: CHAIN, transport: http(RPC_URL) });
      for (const call of callList) {
        const txHash = await walletClient.sendTransaction({
          to: call.to,
          value: call.value || 0n,
          data: call.data,
        });
        console.log(`> Transaction submitted: ${txHash}`);
        console.log("> Waiting for confirmation...");
        const txReceipt = await publicClient.waitForTransactionReceipt({ hash: txHash, timeout: 120_000 });
        if (txReceipt.status !== "success") {
          throw new Error(
            [
              "CLI_USEROP_REVERTED",
              `reason=transaction reverted`,
              `tx_hash=${txHash}`,
              `gas_used=${txReceipt.gasUsed ? txReceipt.gasUsed.toString() : "unknown"}`,
              `gas_cost_eth=unknown`,
            ].join("|"),
          );
        }
      }
      const lastTxHash = callList.length > 0 ? "see above" : "none";
      console.log(`\n> ✅ ${description} Successful! (gas paid in ETH)`);
      return { success: true };
    }

    // --- UserOp path: free mine (paymaster) or AGC paymaster ---
    const authorization = await getEip7702Authorization(signer);
    const userOpOptions = authorization ? { authorization } : {};
    const sendArgs = {
      calls: callList,
      ...userOpOptions,
    };

    const paymasterStub = {
      paymaster: AGENT_PAYMASTER_ADDRESS,
      paymasterData: "0x",
      paymasterVerificationGasLimit: 600000n,
      paymasterPostOpGasLimit: 600000n,
    };
    sendArgs.paymaster = {
      getPaymasterStubData: async () => paymasterStub,
      getPaymasterData: async () => paymasterStub,
    };

    const userOpHash = await bundlerClient.sendUserOperation(sendArgs);
    console.log(`> UserOperation submitted! Hash: ${userOpHash}`);
    console.log("> Waiting for receipt...");

    const receipt = await bundlerClient.waitForUserOperationReceipt({ hash: userOpHash, timeout: 120_000 });
    if (!receipt.success) {
      throw new Error(
        [
          "CLI_USEROP_REVERTED",
          `reason=${sanitizeCliField(receipt.reason || "unknown")}`,
          `tx_hash=${receipt.receipt?.transactionHash || "unknown"}`,
          `gas_used=${receipt.actualGasUsed ? receipt.actualGasUsed.toString() : "unknown"}`,
          `gas_cost_eth=${receipt.actualGasCost ? formatTokenAmount(receipt.actualGasCost) : "unknown"}`,
        ].join("|"),
      );
    }
    const gasNote =
      gasPaymentMode === "free"
        ? " (first mine sponsored by paymaster)"
        : " (gas paid in AGC)";
    console.log(`\n> ✅ ${description} Successful!${gasNote} Tx Hash: ${receipt.receipt.transactionHash}`);
    return receipt;
  } catch (e) {
    const errMsg = e.message || String(e);
    if (errMsg.startsWith("CLI_INSUFFICIENT_TOTAL_AGC|")) {
      const fields = parseCliErrorFields(errMsg);
      console.log(`> ❌ ${description} aborted.`);
      console.log(`> AGC is insufficient for operation + paymaster precharge.`);
      console.log(`> Operation: ${fields.operation} AGC`);
      console.log(`> Precharge: ${fields.precharge} AGC`);
      console.log(`> Required:  ${fields.required} AGC`);
      console.log(`> Available: ${fields.available} AGC`);
      console.log(`> Shortfall: ${fields.shortfall} AGC`);
      return null;
    }
    if (errMsg.startsWith("CLI_USEROP_REVERTED|")) {
      const fields = parseCliErrorFields(errMsg);
      console.log(`> ❌ ${description} reverted onchain.`);
      console.log(`> Tx Hash: ${fields.tx_hash}`);
      console.log(`> Reason: ${fields.reason}`);
      console.log(`> Gas Used: ${fields.gas_used}`);
      console.log(`> Gas Cost: ${fields.gas_cost_eth} ETH`);
      return null;
    }
    if (errMsg.includes("EstimateGas") || errMsg.includes("execution reverted") || errMsg.includes("AA")) {
      console.log(`> ❌ ${description} failed during gas estimation or execution.`);
      console.log(`>`);
      console.log(`> Possible causes:`);
      console.log(`>   1. Insufficient token balance or allowance`);
      console.log(`>   2. Insufficient AGC for paymaster AND insufficient ETH for direct gas payment`);
      console.log(`>   3. Contract rejected the operation (invalid params or state)`);
      console.log(`>`);
      console.log(`> Technical detail: ${errMsg.slice(0, 200)}`);
    } else {
      console.error(`> ${description} execution failed:`, e.stack || errMsg);
    }
    return null;
  }
}

// ======================= .env CONFIG =======================
const { MODEL_TYPE, MODEL_KEY } = loadEnvConfig();

// ======================= WALLET MANAGEMENT =======================

async function check_wallet() {
  const signer = getWalletInstance();
  if (signer) {
    // EIP-7702: EOA and Smart Account share the same address
    const address = signer.address;

    let ethBal = 0n,
      agcBal = 0n;
    try {
      [ethBal, agcBal] = await Promise.all([
        publicClient.getBalance({ address }),
        publicClient.readContract({
          address: AGC_TOKEN_ADDRESS,
          abi: ERC20_ABI,
          functionName: "balanceOf",
          args: [address],
        }),
      ]);
    } catch (e) {
      /* contract may not exist yet */
    }

    console.log(`> 🔑 Wallet Status: Found`);
    console.log(`> 🔗 Network: ${NETWORK_NAME} (Chain ID ${CHAIN_ID})`);
    console.log(`>`);
    console.log(`> 🔐 Smart Account (EIP-7702, same as EOA):`);
    console.log(`> Address: ${address}`);
    console.log(`> ETH Balance: ${(Number(ethBal) / 1e18).toFixed(6)} ETH`);
    console.log(`> AGC Balance: ${(Number(agcBal) / 1e18).toFixed(6)} AGC`);
    console.log(`>`);
    console.log(`> 📁 Stored at: ${WALLET_FILE}`);
  } else {
    console.log(`> 🔑 Wallet Status: Not Found`);
    console.log(`> Run 'create_wallet' to generate one.`);
  }
}

async function create_wallet() {
  let signer = getWalletInstance();

  if (signer) {
    console.log(`> ⏭️ Wallet already exists.`);
    console.log(`> EOA Address: ${signer.address}`);
  } else {
    const dir = path.dirname(WALLET_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    const privateKey = generatePrivateKey();
    const newSigner = privateKeyToAccount(privateKey);
    const data = { address: newSigner.address, privateKey: privateKey };
    fs.writeFileSync(WALLET_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });

    console.log(`> ✅ Wallet Created`);
    console.log(`> EOA Address: ${newSigner.address}`);
    console.log(`> Stored at: ${WALLET_FILE}`);
  }
}

async function get_smart_account() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No EOA wallet found. Run create_wallet first.");

  // EIP-7702: EOA and Smart Account share the same address
  console.log(`> 🔐 Smart Account (EIP-7702, same as EOA):`);
  console.log(`> ${signer.address}`);
}

// ======================= MINING WORKFLOW =======================

async function status() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found. Run create_wallet first.");
  const address = signer.address;

  const ethBal = await publicClient.getBalance({ address });
  let agcBal = 0n,
    cooldownSec = 0n,
    vest = null;

  try {
    agcBal = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function balanceOf(address) view returns (uint256)"]),
      functionName: "balanceOf",
      args: [address],
    });
    cooldownSec = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function getTimeUntilCanMine(address) view returns (uint256)"]),
      functionName: "getTimeUntilCanMine",
      args: [address],
    });
    const v = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi([
        "function vestingSchedules(address) view returns (uint256 totalLocked, uint256 released, uint256 startTime, uint256 endTime, uint256 lpTokenId)",
      ]),
      functionName: "vestingSchedules",
      args: [address],
    });
    if (v[0] > 0n) {
      vest = {
        totalLocked: (Number(v[0]) / 1e18).toFixed(6),
        released: (Number(v[1]) / 1e18).toFixed(6),
        fullyVestedAt: new Date(Number(v[3]) * 1000).toISOString(),
        lpTokenId: v[4].toString(),
      };
    }
  } catch (e) {
    // Contract may not be deployed yet
  }

  const miningStatus = cooldownSec === 0n ? "✅ Yes" : `⏳ No — ${formatHumanSeconds(cooldownSec)} remaining`;

  console.log(`> 📊 Account Status`);
  console.log(`> Network: ${NETWORK_NAME} (Chain ID ${CHAIN_ID})`);
  console.log(`> Address: ${address}`);
  console.log(`> ETH Balance: ${(Number(ethBal) / 1e18).toFixed(6)} ETH`);
  console.log(`> AGC Balance: ${(Number(agcBal) / 1e18).toFixed(6)} AGC`);
  console.log(`>`);
  console.log(`> ⛏️ Mining:`);
  console.log(`> Can Mine: ${miningStatus}`);
  if (vest) {
    console.log(`>`);
    console.log(`> 🔒 Vesting:`);
    console.log(`> Total Locked: ${vest.totalLocked} AGC`);
    console.log(`> Released: ${vest.released} AGC`);
    console.log(`> Fully Vested: ${vest.fullyVestedAt}`);
    console.log(`> LP Token ID: ${vest.lpTokenId}`);
  }
}

async function challenge() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");
  try {
    const res = await axios.get(`${VERIFIER_URL}/challenge?address=${signer.address}`);
    const d = res.data;
    console.log(`> 🧩 Challenge Received`);
    if (d.intro) console.log(`> Intro: ${d.intro}`);
    if (d.required_word) console.log(`> Required Word: ${d.required_word}`);
    if (d.constraints) console.log(`> Constraints: ${d.constraints}`);
    console.log(`> ---`);
    console.log(JSON.stringify(d, null, 2));
  } catch (e) {
    formatError(`Verifier unreachable: ${e.message}`);
  }
}

async function reclaim_bill(op) {
  let reclaimProofStr = null;
  let modelTypeStr = null;
  const print_proof = op === "pp";
  if (MODEL_TYPE && MODEL_KEY) {
    console.log(`> 🔍 Detected API Key for ${MODEL_TYPE}, generating Reclaim proof...`);
    try {
      const sigRes = await axios.get(`${VERIFIER_URL}/session-signature`);
      const { appId, signature } = sigRes.data;
      console.log(`> Received session signature from verifier, generating Reclaim proof...`);

      const client = new ReclaimClient(appId, signature);

      if (MODEL_TYPE.toLowerCase() === "openrouter") {
        const proof = await client.zkFetch(
          "https://openrouter.ai/api/v1/key",
          {
            method: "GET",
          },
          {
            headers: {
              Authorization: `Bearer ${MODEL_KEY}`,
            },
            responseMatches: [
              {
                type: "regex",
                value: '"label":\\s*"(?<label>[^"]+)"',
              },
              {
                type: "regex",
                value: '"usage":(?<usage>[0-9.]+)',
              },
            ],
          },
        );

        reclaimProofStr = JSON.stringify(proof);
        modelTypeStr = "openrouter";
        if (print_proof) {
          console.log(`> 🔐 Reclaim proof:`);
          console.log(JSON.stringify(proof, null, 2));
        } else {
          console.log(`> 🔐 Reclaim proof generated successfully.`);
        }
      } else {
        console.log(`> ⚠️ Unsupported MODEL_TYPE: ${MODEL_TYPE}`);
      }
    } catch (e) {
      console.log(`> ⚠️ Reclaim proof generation failed: ${e.message}`);
    }
  } else {
    console.log(`> 🔍 No MODEL_TYPE and MODEL_KEY configured, skipping Reclaim proof generation.`);
  }
  return { reclaimProofStr, modelTypeStr };
}

async function verify(answer, constraints) {
  if (!answer || !constraints) return formatError("Usage: verify <answer> <constraints>");
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");

  const { reclaimProofStr, modelTypeStr } = await reclaim_bill();

  try {
    const payload = {
      wallet_address: signer.address,
      answer_text: answer,
      constraints: constraints,
    };
    if (reclaimProofStr) {
      payload.reclaim_proof = reclaimProofStr;
      payload.model_type = modelTypeStr;
    }

    const res = await axios.post(`${VERIFIER_URL}/verify`, payload);
    const d = res.data;
    if (d.success) {
      console.log(`> ✅ Verification Passed`);
      console.log(`> Score: ${d.score}`);
      console.log(`> Nonce: ${d.nonce}`);
      console.log(`> Signature: ${d.signature}`);
    } else {
      console.log(`> ❌ Verification Failed`);
      if (d.message) console.log(`> Reason: ${d.message}`);
    }
    console.log(`> ---`);
    console.log(JSON.stringify(d, null, 2));
  } catch (e) {
    formatError(`Verification failed: ${e.response?.data?.detail || e.response?.data?.message || e.message}`);
  }
}

async function cost(score) {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found. Run create_wallet first.");
  const scoreVal = BigInt(score || 1);

  try {
    const estReward = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function getEstimatedReward(uint256) view returns (uint256)"]),
      functionName: "getEstimatedReward",
      args: [scoreVal],
    });
    const liquidPart = (estReward * 20n) / 100n;
    const gasPart = (estReward * 10n) / 100n;
    const vestPart = (estReward * 70n) / 100n;
    const state = await publicClient.readContract({
      address: LIKWID_HELPER_ADDRESS,
      abi: LIKWID_HELPER_ABI,
      functionName: "getPoolStateInfo",
      args: [POOL_ID],
    });
    const r0 = BigInt(state.pairReserve0);
    const r1 = BigInt(state.pairReserve1);
    let ethCost = 0n;
    if (r1 > 0n) ethCost = (liquidPart * r0 * 110n) / (r1 * 100n); // Add 10% slippage

    const ethBalance = await publicClient.getBalance({ address: signer.address });
    const deficit = ethCost > ethBalance ? ethCost - ethBalance : 0n;

    console.log(`> 💰 Mining Cost Estimate (score=${scoreVal})`);
    console.log(`> Total Reward: ${(Number(estReward) / 1e18).toFixed(6)} AGC`);
    console.log(`>`);
    console.log(`> 📋 Full Alignment Breakdown (10/20/70):`);
    console.log(`>   10% Liquid (gas capital): ${(Number(gasPart) / 1e18).toFixed(6)} AGC`);
    console.log(`>   20% LP Paired with ETH: ${(Number(liquidPart) / 1e18).toFixed(6)} AGC`);
    console.log(`>   70% Vesting (70 days):  ${(Number(vestPart) / 1e18).toFixed(6)} AGC`);
    console.log(`>`);
    console.log(`> 💎 ETH Required for LP: ${(Number(ethCost) / 1e18).toFixed(6)} ETH`);
    console.log(`>`);
    console.log(`> 🏦 Smart Account: ${signer.address}`);
    console.log(`> 💳 Current ETH Balance: ${(Number(ethBalance) / 1e18).toFixed(6)} ETH`);
    if (deficit > 0n) {
      console.log(
        `> ⚠️  ETH Deficit: ${(Number(deficit) / 1e18).toFixed(6)} ETH — please send ETH on ${NETWORK_NAME} (Chain ID ${CHAIN_ID}) to your Smart Account before mining with Full Alignment.`,
      );
    } else {
      console.log(`> ✅ ETH Balance sufficient for Full Alignment.`);
    }
  } catch (e) {
    formatError(`Failed to calc cost: ${e.message}`);
  }
}

async function cooldown() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");
  try {
    const time = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function getTimeUntilCanMine(address) view returns (uint256)"]),
      functionName: "getTimeUntilCanMine",
      args: [signer.address],
    });
    if (time === 0n) {
      console.log(`> ✅ Cooldown complete — ready to mine!`);
    } else {
      console.log(`> ⏳ Cooldown: ${formatHumanSeconds(time)} remaining`);
    }
  } catch (e) {
    formatError(e.message);
  }
}

async function reward(score) {
  const scoreVal = BigInt(score || 1);
  try {
    const rw = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function getEstimatedReward(uint256) view returns (uint256)"]),
      functionName: "getEstimatedReward",
      args: [scoreVal],
    });
    console.log(`> 🎁 Estimated Reward: ${(Number(rw) / 1e18).toFixed(6)} AGC (for score=${scoreVal})`);
  } catch (e) {
    formatError(e.message);
  }
}

async function claimVested() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");
  const { smartAccount, bundlerClient } = await getSmartAccount(signer);
  const call = {
    to: AGC_TOKEN_ADDRESS,
    value: 0n,
    data: encodeFunctionData({
      abi: parseAbi(["function claimVested() external"]),
      functionName: "claimVested",
    }),
  };
  await runUserOp(signer, bundlerClient, call, "Claim Vested AGC");
}

async function claimable() {
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");
  try {
    const amt = await publicClient.readContract({
      address: AGC_TOKEN_ADDRESS,
      abi: parseAbi(["function getClaimableVested(address) view returns (uint256)"]),
      functionName: "getClaimableVested",
      args: [signer.address],
    });
    console.log(`> 🔓 Claimable Vested: ${(Number(amt) / 1e18).toFixed(6)} AGC`);
  } catch (e) {
    formatError(e.message);
  }
}

async function mine(scoreStr, signature, nonceStr, ethAmountStr) {
  if (!scoreStr || !signature || !nonceStr) {
    return formatError("Usage: mine <score> <signature> <nonce> [ethAmount]");
  }
  const signer = getWalletInstance();
  if (!signer) return formatError("No wallet found.");
  const { smartAccount, bundlerClient } = await getSmartAccount(signer);

  const score = BigInt(scoreStr);
  const nonce = BigInt(nonceStr);
  const ethAmount = ethAmountStr ? parseEther(ethAmountStr) : 0n;

  const mode = ethAmount > 0n ? "Full Alignment" : "Quick Exit";
  console.log(`> ⛏️ Mining AGC (${mode})...`);
  console.log(`> Score: ${scoreStr}, Nonce: ${nonceStr}, ETH: ${ethAmountStr || "0"}`);

  const mineCall = {
    to: AGC_TOKEN_ADDRESS,
    value: ethAmount,
    data: encodeFunctionData({
      abi: parseAbi(["function mine(uint256 score, bytes calldata signature, uint256 nonce) external payable"]),
      functionName: "mine",
      args: [score, signature, nonce],
    }),
  };

  await runUserOp(signer, bundlerClient, mineCall, "Mine AGC");
}

// ======================= CLI ROUTER =======================
const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.log(`Agent Genesis CLI — Wallet & Mining

Usage: node genesis.js <command> [args]

Setup:
  check_wallet              Check if an EOA wallet exists.
  create_wallet             Create a new EOA wallet.
  get_smart_account         Display EOA and Smart Account addresses.

Mining Workflow:
  status                    Full account status (balances, cooldown, vesting).
  challenge                 Request a PoA challenge from the verifier.
  verify <ans> <constraints> Submit solution to get a mining signature.
  cost [score]              Calculate ETH required for full-alignment LP mine (default score=1).
  mine <score> <sig> <nonce> [eth]  Submit the mine transaction.

Vesting:
  claimable                 Check claimable vested AGC balance.
  claim                     Claim vested AGC tokens.

Info:
  cooldown                  Check time until next mining opportunity.
  reward [score]            Check estimated reward (default score=1).
  reclaim_bill [pp]         Generate Reclaim billing proof (pp = print proof).
`);
  process.exit(0);
}

(async () => {
  switch (command) {
    case "check_wallet":
      await check_wallet();
      break;
    case "create_wallet":
      await create_wallet();
      break;
    case "get_smart_account":
      await get_smart_account();
      break;
    case "status":
      await status();
      break;
    case "challenge":
      await challenge();
      break;
    case "verify":
      await verify(args[1], args[2]);
      break;
    case "cost":
      await cost(args[1]);
      break;
    case "cooldown":
      await cooldown();
      break;
    case "reward":
      await reward(args[1]);
      break;
    case "mine":
      await mine(args[1], args[2], args[3], args[4]);
      break;
    case "claim":
      await claimVested();
      break;
    case "claimable":
      await claimable();
      break;
    case "reclaim_bill":
      await reclaim_bill(args[1]);
      break;
    default:
      console.log("Unknown command:", command);
  }
  process.exit(0);
})();
