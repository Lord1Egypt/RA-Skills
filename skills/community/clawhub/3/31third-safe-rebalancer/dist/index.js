import { privateKeyToAccount } from 'viem/accounts';
import { createPublicClient, createWalletClient, formatUnits, http, isAddress } from 'viem';
import { buildBaseEntriesFromAssetUniverse, checkDrift, planRebalancingWithSdk, validateTrade } from './src/balancer.js';
import { checkPoliciesVerbose, decodeRebalancingTxData, executeTradeNow, normalizeRebalancingAllowances, simulateExecuteTradeNow } from './src/executor.js';
import { readPolicySnapshot } from './src/policies.js';
const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';
function assertAddress(value, fieldName) {
    if (!value || !isAddress(value)) {
        throw new Error(`Invalid or missing ${fieldName}`);
    }
    return value;
}
function parseRequiredInteger(value, fieldName, fallback) {
    const raw = value ?? (typeof fallback === 'number' ? String(fallback) : undefined);
    const parsed = raw ? Number(raw) : Number.NaN;
    if (!Number.isInteger(parsed) || parsed <= 0) {
        throw new Error(`Invalid ${fieldName}: expected a positive integer`);
    }
    return parsed;
}
function parseOptionalInteger(value, fieldName, fallback) {
    if (!value) {
        return fallback;
    }
    const parsed = Number(value);
    if (!Number.isInteger(parsed) || parsed <= 0) {
        throw new Error(`Invalid ${fieldName}: expected a positive integer`);
    }
    return parsed;
}
export function readConfigFromEnv() {
    const oracleMaxAgeSecondsRaw = process.env.ORACLE_MAX_AGE_SECONDS;
    const heartbeatIntervalSecondsRaw = process.env.HEARTBEAT_INTERVAL_SECONDS;
    return {
        safeAddress: assertAddress(process.env.SAFE_ADDRESS, 'SAFE_ADDRESS'),
        chainId: parseRequiredInteger(process.env.CHAIN_ID, 'CHAIN_ID', 8453),
        rpcUrl: process.env.RPC_URL ?? 'https://mainnet.base.org',
        executorModuleAddress: assertAddress(process.env.EXECUTOR_MODULE_ADDRESS, 'EXECUTOR_MODULE_ADDRESS'),
        oracleMaxAgeSeconds: parseOptionalInteger(oracleMaxAgeSecondsRaw, 'ORACLE_MAX_AGE_SECONDS', 3600),
        heartbeatIntervalSeconds: parseOptionalInteger(heartbeatIntervalSecondsRaw, 'HEARTBEAT_INTERVAL_SECONDS', 6 * 60 * 60),
        totApiKey: process.env.TOT_API_KEY,
        executorWalletPrivateKey: process.env.EXECUTOR_WALLET_PRIVATE_KEY
    };
}
export function createViemClients(config) {
    const chain = { id: config.chainId };
    const publicClient = createPublicClient({
        chain,
        transport: http(config.rpcUrl)
    });
    if (!config.executorWalletPrivateKey) {
        return { publicClient };
    }
    const account = privateKeyToAccount(config.executorWalletPrivateKey);
    const walletClient = createWalletClient({
        account,
        chain,
        transport: http(config.rpcUrl)
    });
    return { publicClient, walletClient };
}
export async function check_drift(params) {
    const publicClient = params.publicClient ?? createViemClients(params.config).publicClient;
    const policies = params.policies ?? await readPolicySnapshot(publicClient, params.config.executorModuleAddress);
    if (policies.targetAllocations.length === 0) {
        return {
            shouldRebalance: false,
            thresholdBps: 0,
            maxDriftBps: 0,
            explanation: 'No StaticAllocation policy detected. Drift checks require target allocations.',
            why: 'No StaticAllocation policy detected. Drift checks require target allocations.',
            tokens: []
        };
    }
    if (!policies.priceOracle) {
        return {
            shouldRebalance: false,
            thresholdBps: policies.driftThresholdBps ?? 0,
            maxDriftBps: 0,
            explanation: 'No priceOracle configured on StaticAllocation policy.',
            why: 'Drift is unavailable because the active StaticAllocation policy has no priceOracle.',
            tokens: []
        };
    }
    const drift = await checkDrift({
        publicClient,
        safeAddress: params.config.safeAddress,
        priceOracle: policies.priceOracle,
        policies
    });
    const why = drift.exceedsThreshold
        ? `${drift.explanation} Rebalancing is recommended because drift exceeds the ${drift.thresholdBps} bps threshold.`
        : `${drift.explanation} Drift is below the ${drift.thresholdBps} bps threshold.`;
    return {
        shouldRebalance: drift.exceedsThreshold,
        thresholdBps: drift.thresholdBps,
        maxDriftBps: drift.maxDriftBps,
        explanation: drift.explanation,
        why,
        tokens: drift.tokens.map((token) => ({
            token: token.token,
            symbol: token.symbol,
            currentWeightPct: (token.currentWeightBps / 100).toFixed(2),
            targetWeightPct: (token.targetWeightBps / 100).toFixed(2),
            driftBps: token.driftBps
        }))
    };
}
export async function validate_trade(params) {
    const publicClient = params.publicClient ?? createViemClients(params.config).publicClient;
    const policies = params.policies ?? await readPolicySnapshot(publicClient, params.config.executorModuleAddress);
    const validation = await validateTrade({
        publicClient,
        priceOracle: policies.priceOracle,
        policies,
        trade: params.trade
    });
    return {
        valid: validation.ok,
        reason: validation.reason,
        minAllowedToReceive: validation.minAllowedToReceive ? validation.minAllowedToReceive.toString() : undefined
    };
}
export async function automation(params) {
    const heartbeatSeconds = params.config.heartbeatIntervalSeconds ?? 6 * 60 * 60;
    const HEARTBEAT_MS = heartbeatSeconds * 1000;
    const now = params.nowMs ?? Date.now();
    const lastHeartbeatAt = params.state?.lastHeartbeatAt ?? 0;
    const due = now - lastHeartbeatAt >= HEARTBEAT_MS;
    if (!due) {
        return {
            checked: false,
            nextHeartbeatInSeconds: Math.ceil((HEARTBEAT_MS - (now - lastHeartbeatAt)) / 1000),
            notify: false,
            message: 'Heartbeat not due yet.'
        };
    }
    const drift = await check_drift({
        config: params.config,
        publicClient: params.publicClient,
        policies: params.policies
    });
    if (drift.shouldRebalance) {
        return {
            checked: true,
            nextHeartbeatInSeconds: heartbeatSeconds,
            notify: true,
            message: `Drift alert: ${drift.why}`
        };
    }
    return {
        checked: true,
        nextHeartbeatInSeconds: heartbeatSeconds,
        notify: false,
        message: `Heartbeat complete. ${drift.why}`
    };
}
export async function execute_rebalance(params) {
    const { walletClient: providedWalletClient } = params;
    const { publicClient: configuredPublicClient, walletClient: configuredWalletClient } = createViemClients(params.config);
    const publicClient = params.publicClient ?? configuredPublicClient;
    const walletClient = providedWalletClient ?? configuredWalletClient;
    if (!walletClient) {
        throw new Error('EXECUTOR_WALLET_NOT_SET: set EXECUTOR_WALLET_PRIVATE_KEY or inject walletClient.');
    }
    const executor = (await publicClient.readContract({
        address: params.config.executorModuleAddress,
        abi: [
            { type: 'function', name: 'executor', stateMutability: 'view', inputs: [], outputs: [{ type: 'address' }] }
        ],
        functionName: 'executor'
    }));
    const walletAddress = await resolveWalletAddress(walletClient);
    if (!walletAddress) {
        throw new Error('EXECUTOR_WALLET_NOT_SET: executor wallet address unavailable from wallet client.');
    }
    if (walletAddress.toLowerCase() === ZERO_ADDRESS) {
        throw new Error('EXECUTOR_WALLET_ZERO_ADDRESS: executor wallet cannot be zero address.');
    }
    if (walletAddress.toLowerCase() !== executor.toLowerCase()) {
        throw new Error(`EXECUTOR_WALLET_NOT_EXECUTOR: wallet=${walletAddress} executor=${executor}`);
    }
    const defaultBatchConfig = {
        checkFeelessWallets: true,
        revertOnError: true
    };
    const batchConfig = params.batchConfig ?? defaultBatchConfig;
    const executionArgs = resolveExecutionArgs({
        trades: params.trades,
        approvals: params.approvals,
        rebalancing: params.rebalancing,
        batchConfig
    });
    const policyCheck = await checkPoliciesVerbose({
        publicClient,
        executorModule: params.config.executorModuleAddress,
        trades: executionArgs.trades,
        config: executionArgs.config
    });
    if (!policyCheck.ok) {
        throw new Error(`FAILED_POLICY_CHECK: policy=${policyCheck.failedPolicy} reason=${policyCheck.reason || 'Unknown policy failure'}`);
    }
    const maxAttempts = params.maxAttempts ?? 2;
    const retryDelayMs = params.retryDelayMs ?? 2000;
    let txHash;
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            await simulateExecuteTradeNow({
                publicClient,
                executorModule: params.config.executorModuleAddress,
                approvals: executionArgs.approvals,
                trades: executionArgs.trades,
                config: executionArgs.config,
                account: walletClient.account ?? walletAddress
            });
            txHash = await executeTradeNow({
                walletClient,
                executorModule: params.config.executorModuleAddress,
                approvals: executionArgs.approvals,
                trades: executionArgs.trades,
                config: executionArgs.config,
                account: walletClient.account ?? walletAddress
            });
            break;
        }
        catch (error) {
            const classified = classifyExecutionFailure(error);
            if (classified.kind === 'skip') {
                throw new Error(`SKIPPED_MIN_TRADE_VALUE: ${classified.reason}`);
            }
            if (classified.kind === 'fail') {
                throw new Error(`FAILED_TOKEN_NOT_TRADEABLE: ${classified.reason}`);
            }
            if (attempt >= maxAttempts) {
                throw new Error(`FAILED_EXECUTION_UNKNOWN: ${classified.reason}`);
            }
            if (retryDelayMs > 0) {
                await new Promise((resolve) => setTimeout(resolve, retryDelayMs));
            }
        }
    }
    if (!txHash) {
        throw new Error('FAILED_EXECUTION_UNKNOWN: execution did not produce a transaction hash');
    }
    const why = `Execution submitted via ExecutorModule ${params.config.executorModuleAddress}.`;
    return { txHash, why };
}
function resolveExecutionArgs(input) {
    if (input.rebalancing) {
        const decoded = decodeRebalancingTxData(input.rebalancing.txData);
        return {
            trades: decoded.trades,
            approvals: normalizeRebalancingAllowances(input.rebalancing.requiredAllowances),
            config: decoded.config
        };
    }
    if (!input.trades) {
        throw new Error('Provide either { rebalancing } or { trades }.');
    }
    return {
        trades: input.trades,
        approvals: input.approvals ?? [],
        config: input.batchConfig
    };
}
async function resolveWalletAddress(walletClient) {
    const accountAddress = walletClient?.account?.address;
    if (accountAddress) {
        return accountAddress;
    }
    const getAddresses = walletClient?.getAddresses;
    if (typeof getAddresses === 'function') {
        const addresses = await getAddresses.call(walletClient);
        if (Array.isArray(addresses) && addresses[0]) {
            return addresses[0];
        }
    }
    return undefined;
}
export async function plan_rebalance(params) {
    if (!params.config.totApiKey) {
        throw new Error('Missing TOT_API_KEY for rebalancing plan.');
    }
    const publicClient = params.publicClient ?? createViemClients(params.config).publicClient;
    const policies = params.policies ?? await readPolicySnapshot(publicClient, params.config.executorModuleAddress);
    if (policies.targetAllocations.length === 0) {
        throw new Error('Cannot plan rebalance: no StaticAllocation policy / target allocations found.');
    }
    const baseEntries = policies.assetUniverseTokens.length > 0
        ? await buildBaseEntriesFromAssetUniverse({
            publicClient,
            safeAddress: params.config.safeAddress,
            assetUniverseTokens: policies.assetUniverseTokens
        })
        : [];
    const response = await planRebalancingWithSdk({
        apiKey: params.config.totApiKey,
        chainId: params.config.chainId,
        safeAddress: params.config.safeAddress,
        signerAddress: params.signerAddress,
        minTradeValue: params.minTradeValue,
        baseEntries,
        targetAllocations: policies.targetAllocations
    });
    return {
        why: 'Plan generated from deployed target allocations via 31Third SDK.',
        response
    };
}
export async function rebalance_now(params) {
    const { publicClient: configuredPublicClient, walletClient: configuredWalletClient } = createViemClients(params.config);
    const publicClient = params.publicClient ?? configuredPublicClient;
    const walletClient = params.walletClient ?? configuredWalletClient;
    if (!walletClient) {
        throw new Error('EXECUTOR_WALLET_NOT_SET: set EXECUTOR_WALLET_PRIVATE_KEY or inject walletClient.');
    }
    const policies = params.policies ?? await readPolicySnapshot(publicClient, params.config.executorModuleAddress);
    if (policies.targetAllocations.length === 0) {
        return {
            executed: false,
            skipped: true,
            reason: 'Skipped: no StaticAllocation policy / target allocations found on ExecutorModule.'
        };
    }
    if (!params.force) {
        const drift = await check_drift({
            config: params.config,
            publicClient,
            policies
        });
        if (!drift.shouldRebalance) {
            return {
                executed: false,
                skipped: true,
                reason: `Skipped: ${drift.why}`
            };
        }
    }
    const signerAddress = params.signerAddress
        ?? walletClient.account?.address;
    if (!signerAddress) {
        throw new Error('Missing signer address: pass signerAddress or configure EXECUTOR_WALLET_PRIVATE_KEY.');
    }
    const plan = await plan_rebalance({
        config: params.config,
        signerAddress,
        minTradeValue: params.minTradeValue,
        publicClient,
        policies
    });
    const execution = await execute_rebalance({
        config: params.config,
        publicClient,
        walletClient,
        rebalancing: plan.response,
        maxAttempts: params.maxAttempts,
        retryDelayMs: params.retryDelayMs
    });
    return {
        executed: true,
        skipped: false,
        reason: execution.why,
        txHash: execution.txHash
    };
}
function classifyExecutionFailure(error) {
    const reason = extractErrorText(error).toLowerCase();
    if (reason.includes('mintradevalue') || reason.includes('minimum trade value')) {
        return { kind: 'skip', reason: extractErrorText(error) };
    }
    if (reason.includes('tokennotbuyable') ||
        reason.includes('tokennotsellable') ||
        reason.includes('not tradeable') ||
        reason.includes('not tradable')) {
        return { kind: 'fail', reason: extractErrorText(error) };
    }
    return { kind: 'retryable', reason: extractErrorText(error) };
}
function extractErrorText(error) {
    if (error instanceof Error) {
        return error.message;
    }
    if (typeof error === 'string') {
        return error;
    }
    try {
        return JSON.stringify(error);
    }
    catch {
        return String(error);
    }
}
export function summarizeTradeReason(input) {
    return `${input.symbol} is at ${formatUnits(BigInt(input.currentWeightBps), 2)}%, rebalancing to ${formatUnits(BigInt(input.targetWeightBps), 2)}%.`;
}
export function help() {
    return {
        summary: 'Policy-aware Safe rebalancing for 31Third ExecutorModule, with drift checks, trade validation, and execution.',
        capabilities: [
            'check_drift: read policies and compare current allocation vs target allocation',
            'validate_trade: enforce Asset Universe and Slippage policy boundaries',
            'automation: configurable heartbeat that emits alert payloads when drift exceeds threshold',
            'plan_rebalance: build a rebalance plan from Safe balances (asset-universe bounded) + deployed target allocations via 31Third SDK',
            'execute_rebalance: accepts SDK rebalancing response or explicit trades, verifies the signer matches ExecutorModule.executor, runs checkPoliciesVerbose + simulation, retries unknown failures once, then executes through ExecutorModule',
            'Execution authorization: the signing wallet must equal ExecutorModule.executor, otherwise execution is rejected',
            'rebalance_now: one-step rebalance from on-chain policies (drift check -> plan -> execute) for single-wallet executor setups',
            'Execution contract: decode txData as batchTrade(trades,config), run checkPoliciesVerbose, and submit execute(trades,config) through ExecutorModule',
            'smoke (CLI): read-only preflight for config, chain/policy access, drift, optional planning, and optional simulation'
        ],
        requiredEnv: [
            'SAFE_ADDRESS',
            'EXECUTOR_MODULE_ADDRESS',
            'TOT_API_KEY (required for plan_rebalance)',
            'CHAIN_ID (default 8453)',
            'RPC_URL (default https://mainnet.base.org)',
            'EXECUTOR_WALLET_PRIVATE_KEY (required for execute_rebalance)',
            'HEARTBEAT_INTERVAL_SECONDS (optional, default 21600)',
            'ORACLE_MAX_AGE_SECONDS (optional, default 3600)'
        ],
        setupSteps: [
            'Deploy policy stack with the 31Third Safe policy wizard: https://app.31third.com/safe-policy-deployer',
            'Use two wallets: (1) Safe owner wallet for ownership/governance actions, (2) executor wallet configured on ExecutorModule for trade execution.',
            'Never share the Safe owner private key. Only the executor wallet private key should be provided to this skill for execution.',
            'Attach policies to the ExecutorModule (partial policy stacks are allowed)',
            'Use the wizard final step summary: it lists the required environment variables to copy into this skill configuration.',
            'Request a TOT_API_KEY (31Third API key) via https://31third.com or dev@31third.com.',
            'Run smoke preflight before execution: npm run smoke -- --signer 0xYourSigner',
            'Set environment variables and test read-only tools first (check_drift, validate_trade, automation)',
            'For the smoothest path, run one command: npm run cli -- rebalance-now',
            'Only then enable execution with EXECUTOR_WALLET_PRIVATE_KEY and run execute_rebalance'
        ]
    };
}
