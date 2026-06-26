import { parseAbi } from 'viem';
import { calculateRebalancing } from '@31third/sdk';
import { priceOracleAbi } from './contracts.js';
const erc20Abi = parseAbi([
    'function balanceOf(address account) view returns (uint256)',
    'function decimals() view returns (uint8)',
    'function symbol() view returns (string)'
]);
function tenPow(decimals) {
    return 10n ** BigInt(decimals);
}
function absDiff(a, b) {
    return a > b ? a - b : b - a;
}
function toPercentageString(bps) {
    return (bps / 100).toFixed(2);
}
async function readTokenSymbol(publicClient, token) {
    try {
        return (await publicClient.readContract({
            address: token,
            abi: erc20Abi,
            functionName: 'symbol'
        }));
    }
    catch {
        return `${token.slice(0, 6)}...${token.slice(-4)}`;
    }
}
async function readTokenDecimals(publicClient, token) {
    const decimals = (await publicClient.readContract({
        address: token,
        abi: erc20Abi,
        functionName: 'decimals'
    }));
    return Number(decimals);
}
async function readPrice18(publicClient, priceOracle, token) {
    return (await publicClient.readContract({
        address: priceOracle,
        abi: priceOracleAbi,
        functionName: 'getPrice18',
        args: [token]
    }));
}
function usdValue18(amount, tokenDecimals, price18) {
    if (amount === 0n || price18 === 0n) {
        return 0n;
    }
    return (amount * price18) / tenPow(tokenDecimals);
}
export async function checkDrift(params) {
    const { publicClient, safeAddress, priceOracle, policies } = params;
    if (policies.targetAllocations.length === 0) {
        return {
            totalUsd18: 0n,
            thresholdBps: 0,
            exceedsThreshold: false,
            maxDriftBps: 0,
            tokens: [],
            explanation: 'No StaticAllocation policy detected. Drift checks require target allocations.'
        };
    }
    const thresholdBps = policies.driftThresholdBps ?? 0;
    const tokens = policies.targetAllocations.map((item) => item.token);
    const raw = await Promise.all(tokens.map(async (token) => {
        const [symbol, decimals, balance, price18] = await Promise.all([
            readTokenSymbol(publicClient, token),
            readTokenDecimals(publicClient, token),
            publicClient.readContract({
                address: token,
                abi: erc20Abi,
                functionName: 'balanceOf',
                args: [safeAddress]
            }),
            readPrice18(publicClient, priceOracle, token)
        ]);
        if (price18 <= 0n) {
            throw new Error(`Missing or stale price for ${token} on PriceOracle ${priceOracle}.`);
        }
        return {
            token,
            symbol,
            balance,
            valueUsd18: usdValue18(balance, decimals, price18)
        };
    }));
    const totalUsd18 = raw.reduce((sum, item) => sum + item.valueUsd18, 0n);
    const driftTokens = raw.map((item) => {
        const target = policies.targetAllocations.find((entry) => entry.token.toLowerCase() === item.token.toLowerCase());
        const targetWeightBps = target ? Number(target.bps) : 0;
        const currentWeightBps = totalUsd18 === 0n ? 0 : Number((item.valueUsd18 * 10000n) / totalUsd18);
        const driftBps = absDiff(currentWeightBps, targetWeightBps);
        return {
            token: item.token,
            symbol: item.symbol,
            balance: item.balance,
            valueUsd18: item.valueUsd18,
            currentWeightBps,
            targetWeightBps,
            driftBps
        };
    });
    const maxDrift = driftTokens.reduce((max, item) => (item.driftBps > max ? item.driftBps : max), 0);
    const mostDrifted = driftTokens.find((item) => item.driftBps === maxDrift);
    const exceedsThreshold = maxDrift >= thresholdBps;
    const explanation = mostDrifted
        ? `${mostDrifted.symbol} is at ${toPercentageString(mostDrifted.currentWeightBps)}%, target ${toPercentageString(mostDrifted.targetWeightBps)}% (drift ${mostDrifted.driftBps} bps).`
        : 'No tracked assets found for drift calculation.';
    return {
        totalUsd18,
        thresholdBps,
        exceedsThreshold,
        maxDriftBps: maxDrift,
        tokens: driftTokens,
        explanation
    };
}
export async function validateTrade(params) {
    const { publicClient, priceOracle, policies, trade } = params;
    if (policies.assetUniverseTokens.length > 0) {
        const normalized = new Set(policies.assetUniverseTokens.map((token) => token.toLowerCase()));
        if (!normalized.has(trade.from.toLowerCase())) {
            return { ok: false, reason: `Asset Universe violation: from token ${trade.from} is not allowed.` };
        }
        if (!normalized.has(trade.to.toLowerCase())) {
            return { ok: false, reason: `Asset Universe violation: to token ${trade.to} is not allowed.` };
        }
    }
    if (typeof policies.maxSlippageBps === 'number') {
        if (!priceOracle) {
            return {
                ok: false,
                reason: 'Slippage validation failed: no priceOracle configured on the active policies.'
            };
        }
        const [fromPrice18, toPrice18, fromTokenDecimals, toTokenDecimals] = await Promise.all([
            readPrice18(publicClient, priceOracle, trade.from),
            readPrice18(publicClient, priceOracle, trade.to),
            readTokenDecimals(publicClient, trade.from),
            readTokenDecimals(publicClient, trade.to)
        ]);
        if (fromPrice18 === 0n || toPrice18 === 0n) {
            return {
                ok: false,
                reason: 'Slippage validation failed: missing valid price for one or more trade tokens.'
            };
        }
        const expectedTo = (trade.fromAmount * fromPrice18 * tenPow(toTokenDecimals)) /
            (tenPow(fromTokenDecimals) * toPrice18);
        const minAllowed = (expectedTo * BigInt(10_000 - policies.maxSlippageBps)) / 10000n;
        if (trade.minToReceiveBeforeFees < minAllowed) {
            return {
                ok: false,
                reason: `Slippage violation: minToReceive ${trade.minToReceiveBeforeFees.toString()} below minimum ${minAllowed.toString()}.`,
                minAllowedToReceive: minAllowed
            };
        }
    }
    return { ok: true, reason: 'Trade validated against Asset Universe and Slippage boundaries.' };
}
export async function buildBaseEntriesFromAssetUniverse(params) {
    if (params.assetUniverseTokens.length === 0) {
        return [];
    }
    const balances = await Promise.all(params.assetUniverseTokens.map(async (token) => {
        const balance = (await params.publicClient.readContract({
            address: token,
            abi: erc20Abi,
            functionName: 'balanceOf',
            args: [params.safeAddress]
        }));
        return { tokenAddress: token, balance };
    }));
    return balances
        .filter((entry) => entry.balance > 0n)
        .map((entry) => ({
        tokenAddress: entry.tokenAddress,
        amount: entry.balance.toString()
    }));
}
export async function planRebalancingWithSdk(input) {
    return calculateRebalancing({
        apiBaseUrl: 'https://api.31third.com/1.3',
        apiKey: input.apiKey,
        chainId: input.chainId,
        payload: {
            wallet: input.safeAddress,
            signer: input.signerAddress,
            chainId: input.chainId,
            minTradeValue: input.minTradeValue,
            baseEntries: input.baseEntries ?? [],
            targetEntries: input.targetAllocations.map((target) => ({
                tokenAddress: target.token,
                allocation: target.bps / 10_000
            }))
        }
    });
}
