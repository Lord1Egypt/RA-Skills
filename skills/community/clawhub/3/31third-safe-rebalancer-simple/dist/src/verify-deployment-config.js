import { Contract, JsonRpcProvider, isAddress } from 'ethers';
import { assetUniversePolicyAbi, executorModuleAbi, priceOracleAbi, slippagePolicyAbi, staticAllocationPolicyAbi } from './contracts.js';
function readFirstEnv(names) {
    for (const name of names) {
        const value = process.env[name];
        if (value && value.trim()) {
            return value.trim();
        }
    }
    return undefined;
}
function readEnvAddress(names) {
    const value = readFirstEnv(names);
    if (!value)
        return undefined;
    return isAddress(value) ? value : undefined;
}
function parsePercent(value) {
    const normalized = value.replace('%', '').trim();
    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : undefined;
}
function readDeploymentEnvSnapshot() {
    return {
        safeAddress: readEnvAddress(['SAFE_ADDRESS']),
        executorModuleAddress: readEnvAddress(['EXECUTOR_MODULE_ADDRESS'])
    };
}
function firstAddressInText(value) {
    const match = value.match(/0x[a-fA-F0-9]{40}/);
    if (!match)
        return undefined;
    return isAddress(match[0]) ? match[0] : undefined;
}
function parseTroubleshootingSummary(input) {
    const parsed = {
        assetUniverseAssets: [],
        staticAllocationTargets: []
    };
    let section = null;
    const lines = input
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean);
    for (const line of lines) {
        if (line === 'AssetUniverseAssets:') {
            section = 'asset-universe-assets';
            continue;
        }
        if (line === 'StaticAllocationTargets:') {
            section = 'static-allocation-targets';
            continue;
        }
        if (line.startsWith('- ')) {
            const item = line.slice(2).trim();
            if (section === 'asset-universe-assets') {
                const address = firstAddressInText(item);
                if (address) {
                    parsed.assetUniverseAssets.push(address);
                }
            }
            else if (section === 'static-allocation-targets') {
                const address = firstAddressInText(item);
                const allocationMatch = item.match(/AllocationPercent\s*=\s*([0-9]*\.?[0-9]+)%/i);
                const allocationPercent = allocationMatch ? Number(allocationMatch[1]) : undefined;
                if (address && typeof allocationPercent === 'number' && Number.isFinite(allocationPercent)) {
                    parsed.staticAllocationTargets.push({ tokenAddress: address, allocationPercent });
                }
            }
            continue;
        }
        section = null;
        const separator = line.indexOf('=');
        if (separator <= 0)
            continue;
        const key = line.slice(0, separator).trim();
        const rawValue = line.slice(separator + 1).trim();
        const address = firstAddressInText(rawValue);
        if (key === 'Safe')
            parsed.safeAddress = address;
        if (key === 'ExecutorModule')
            parsed.executorModuleAddress = address;
        if (key === 'Executor')
            parsed.executor = address;
        if (key === 'Registry' && !parsed.executor)
            parsed.executor = address;
        if (key === 'BatchTrade')
            parsed.batchTrade = address;
        if (key === 'PriceOracle')
            parsed.priceOracle = address;
        if (key === 'FeedRegistry')
            parsed.feedRegistry = address;
        if (key === 'AssetUniversePolicy')
            parsed.assetUniversePolicy = address;
        if (key === 'StaticAllocationPolicy')
            parsed.staticAllocationPolicy = address;
        if (key === 'SlippagePolicy')
            parsed.slippagePolicy = address;
        if (key === 'CooldownSec') {
            const n = Number(rawValue.replace(/[^0-9.]/g, ''));
            if (Number.isFinite(n))
                parsed.cooldownSec = n;
        }
        if (key === 'StaticAllocationDriftThresholdPercent') {
            const n = parsePercent(rawValue);
            if (typeof n === 'number')
                parsed.staticAllocationDriftThresholdPercent = n;
        }
        if (key === 'StaticAllocationToleranceThresholdPercent') {
            const n = parsePercent(rawValue);
            if (typeof n === 'number')
                parsed.staticAllocationToleranceThresholdPercent = n;
        }
        if (key === 'MaxSlippagePercent') {
            const n = parsePercent(rawValue);
            if (typeof n === 'number')
                parsed.maxSlippagePercent = n;
        }
    }
    return parsed;
}
function normalizePolicyState(entry) {
    const policy = entry?.policy ?? (Array.isArray(entry) ? entry[0] : undefined);
    const policyType = entry?.policyType ?? (Array.isArray(entry) ? entry[1] : undefined);
    return {
        policy: typeof policy === 'string' ? policy : '',
        policyType: typeof policyType === 'string' ? policyType : ''
    };
}
function normalizePolicyType(value) {
    return value.toLowerCase().replace(/[^a-z]/g, '');
}
function bpsToPercent(bps) {
    return bps / 100;
}
async function defaultFetchOnChainDeployment(executorModuleAddress, rpcUrl) {
    const provider = new JsonRpcProvider(rpcUrl);
    const executorModule = new Contract(executorModuleAddress, executorModuleAbi, provider);
    const [safeAddress, executor, batchTrade, cooldownRaw, policiesRaw] = await Promise.all([
        executorModule.safe(),
        executorModule.executor(),
        executorModule.batchTrade(),
        executorModule.cooldown(),
        executorModule.getPoliciesWithTypes()
    ]);
    const policies = policiesRaw.map(normalizePolicyState);
    const policiesByType = new Map();
    for (const policy of policies) {
        const key = normalizePolicyType(policy.policyType);
        if (key && policy.policy && isAddress(policy.policy)) {
            policiesByType.set(key, policy.policy);
        }
    }
    const assetUniversePolicy = policiesByType.get('assetuniverse');
    const staticAllocationPolicy = policiesByType.get('staticallocation');
    const slippagePolicy = policiesByType.get('slippage');
    let assetUniverseAssets = [];
    if (assetUniversePolicy) {
        const assetUniverse = new Contract(assetUniversePolicy, assetUniversePolicyAbi, provider);
        assetUniverseAssets = await assetUniverse.getTokens();
    }
    let staticAllocationDriftThresholdPercent;
    let staticAllocationToleranceThresholdPercent;
    let staticAllocationTargets = [];
    let staticPriceOracle;
    let staticFeedRegistry;
    if (staticAllocationPolicy) {
        const staticAllocation = new Contract(staticAllocationPolicy, staticAllocationPolicyAbi, provider);
        const [driftThresholdBpsRaw, toleranceThresholdBpsRaw, targetsRaw, priceOracle] = await Promise.all([
            staticAllocation.driftThresholdBps(),
            staticAllocation.toleranceThresholdBps(),
            staticAllocation.getAllTargets(),
            staticAllocation.priceOracle()
        ]);
        staticAllocationDriftThresholdPercent = bpsToPercent(Number(driftThresholdBpsRaw));
        staticAllocationToleranceThresholdPercent = bpsToPercent(Number(toleranceThresholdBpsRaw));
        staticPriceOracle = priceOracle;
        staticFeedRegistry = await new Contract(priceOracle, priceOracleAbi, provider).feedRegistry();
        staticAllocationTargets = targetsRaw.map((target) => ({
            tokenAddress: target?.token ?? target?.[0],
            allocationPercent: bpsToPercent(Number(target?.bps ?? target?.[1]))
        }));
    }
    let maxSlippagePercent;
    let slippagePriceOracle;
    let slippageFeedRegistry;
    if (slippagePolicy) {
        const slippage = new Contract(slippagePolicy, slippagePolicyAbi, provider);
        const [maxSlippageBpsRaw, priceOracle] = await Promise.all([
            slippage.maxSlippageBps(),
            slippage.priceOracle()
        ]);
        maxSlippagePercent = bpsToPercent(Number(maxSlippageBpsRaw));
        slippagePriceOracle = priceOracle;
        slippageFeedRegistry = await new Contract(priceOracle, priceOracleAbi, provider).feedRegistry();
    }
    return {
        safeAddress,
        executorModuleAddress,
        executor,
        batchTrade,
        cooldownSec: Number(cooldownRaw),
        assetUniversePolicy,
        assetUniverseAssets,
        staticAllocationPolicy,
        staticAllocationDriftThresholdPercent,
        staticAllocationToleranceThresholdPercent,
        staticAllocationTargets,
        staticPriceOracle,
        staticFeedRegistry,
        slippagePolicy,
        maxSlippagePercent,
        slippagePriceOracle,
        slippageFeedRegistry
    };
}
function formatPercent(value) {
    return `${value.toFixed(2)}%`;
}
function formatAddressList(value) {
    return value.join(', ');
}
function formatTargets(value) {
    return value
        .map((entry) => `${entry.tokenAddress}:${formatPercent(entry.allocationPercent)}`)
        .join(', ');
}
function addressesEqual(a, b) {
    return a.toLowerCase() === b.toLowerCase();
}
function numbersEqual(a, b) {
    return Math.abs(a - b) < 1e-9;
}
function addressListsEqual(a, b) {
    if (a.length !== b.length)
        return false;
    const normalizedA = a.map((x) => x.toLowerCase()).sort();
    const normalizedB = b.map((x) => x.toLowerCase()).sort();
    return normalizedA.every((value, index) => value === normalizedB[index]);
}
function targetsEqual(a, b) {
    if (a.length !== b.length)
        return false;
    const mapA = new Map(a.map((entry) => [entry.tokenAddress.toLowerCase(), entry.allocationPercent]));
    const mapB = new Map(b.map((entry) => [entry.tokenAddress.toLowerCase(), entry.allocationPercent]));
    if (mapA.size !== mapB.size)
        return false;
    for (const [token, allocation] of mapA.entries()) {
        const other = mapB.get(token);
        if (typeof other !== 'number' || !numbersEqual(allocation, other)) {
            return false;
        }
    }
    return true;
}
function buildCheck(params) {
    const values = [];
    if (typeof params.envValue !== 'undefined')
        values.push({ source: 'env', value: params.envValue });
    if (typeof params.summaryValue !== 'undefined')
        values.push({ source: 'summary', value: params.summaryValue });
    if (typeof params.chainValue !== 'undefined')
        values.push({ source: 'chain', value: params.chainValue });
    const check = {
        field: params.field,
        status: 'missing',
        detail: ''
    };
    if (typeof params.envValue !== 'undefined')
        check.envValue = params.format(params.envValue);
    if (typeof params.summaryValue !== 'undefined')
        check.summaryValue = params.format(params.summaryValue);
    if (typeof params.chainValue !== 'undefined')
        check.chainValue = params.format(params.chainValue);
    if (values.length < 2) {
        check.status = 'missing';
        check.detail = 'Insufficient data to compare across sources.';
        return check;
    }
    const anchor = values[0].value;
    const mismatch = values.some((entry) => !params.equals(anchor, entry.value));
    if (mismatch) {
        check.status = 'mismatch';
        check.detail = values.map((entry) => `${entry.source}=${params.format(entry.value)}`).join(' | ');
        return check;
    }
    check.status = 'match';
    check.detail = values.map((entry) => `${entry.source} matches`).join(', ');
    return check;
}
export async function verify_deployment_config(params) {
    const envSnapshot = readDeploymentEnvSnapshot();
    const summary = parseTroubleshootingSummary(params.troubleshootingSummary);
    const executorModuleAddress = params.executorModuleAddress ?? envSnapshot.executorModuleAddress ?? summary.executorModuleAddress;
    if (!executorModuleAddress || !isAddress(executorModuleAddress)) {
        throw new Error('Unable to resolve ExecutorModule address. Provide params.executorModuleAddress, set EXECUTOR_MODULE_ADDRESS, or include ExecutorModule in troubleshootingSummary.');
    }
    const rpcUrl = params.rpcUrl ?? process.env.RPC_URL ?? 'https://mainnet.base.org';
    const fetchOnChainDeploymentFn = params.deps?.fetchOnChainDeploymentFn ?? defaultFetchOnChainDeployment;
    const chain = await fetchOnChainDeploymentFn(executorModuleAddress, rpcUrl);
    const chainPriceOracle = chain.staticPriceOracle ?? chain.slippagePriceOracle;
    const chainFeedRegistry = chain.staticFeedRegistry ?? chain.slippageFeedRegistry;
    const checks = [
        buildCheck({
            field: 'Safe',
            envValue: envSnapshot.safeAddress,
            summaryValue: summary.safeAddress,
            chainValue: chain.safeAddress,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'ExecutorModule',
            envValue: envSnapshot.executorModuleAddress,
            summaryValue: summary.executorModuleAddress,
            chainValue: chain.executorModuleAddress,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'Executor',
            summaryValue: summary.executor,
            chainValue: chain.executor,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'BatchTrade',
            summaryValue: summary.batchTrade,
            chainValue: chain.batchTrade,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'PriceOracle',
            summaryValue: summary.priceOracle,
            chainValue: chainPriceOracle,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'FeedRegistry',
            summaryValue: summary.feedRegistry,
            chainValue: chainFeedRegistry,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'CooldownSec',
            summaryValue: summary.cooldownSec,
            chainValue: chain.cooldownSec,
            equals: numbersEqual,
            format: (value) => String(value)
        }),
        buildCheck({
            field: 'AssetUniversePolicy',
            summaryValue: summary.assetUniversePolicy,
            chainValue: chain.assetUniversePolicy,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'AssetUniverseAssets',
            summaryValue: summary.assetUniverseAssets.length ? summary.assetUniverseAssets : undefined,
            chainValue: chain.assetUniverseAssets.length ? chain.assetUniverseAssets : undefined,
            equals: addressListsEqual,
            format: formatAddressList
        }),
        buildCheck({
            field: 'StaticAllocationPolicy',
            summaryValue: summary.staticAllocationPolicy,
            chainValue: chain.staticAllocationPolicy,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'StaticAllocationDriftThresholdPercent',
            summaryValue: summary.staticAllocationDriftThresholdPercent,
            chainValue: chain.staticAllocationDriftThresholdPercent,
            equals: numbersEqual,
            format: formatPercent
        }),
        buildCheck({
            field: 'StaticAllocationToleranceThresholdPercent',
            summaryValue: summary.staticAllocationToleranceThresholdPercent,
            chainValue: chain.staticAllocationToleranceThresholdPercent,
            equals: numbersEqual,
            format: formatPercent
        }),
        buildCheck({
            field: 'StaticAllocationTargets',
            summaryValue: summary.staticAllocationTargets.length ? summary.staticAllocationTargets : undefined,
            chainValue: chain.staticAllocationTargets.length ? chain.staticAllocationTargets : undefined,
            equals: targetsEqual,
            format: formatTargets
        }),
        buildCheck({
            field: 'SlippagePolicy',
            summaryValue: summary.slippagePolicy,
            chainValue: chain.slippagePolicy,
            equals: addressesEqual,
            format: (value) => value
        }),
        buildCheck({
            field: 'MaxSlippagePercent',
            summaryValue: summary.maxSlippagePercent,
            chainValue: chain.maxSlippagePercent,
            equals: numbersEqual,
            format: formatPercent
        })
    ];
    const warnings = [];
    if (chain.staticPriceOracle &&
        chain.slippagePriceOracle &&
        !addressesEqual(chain.staticPriceOracle, chain.slippagePriceOracle)) {
        warnings.push(`On-chain price oracles differ: staticAllocation=${chain.staticPriceOracle}, slippage=${chain.slippagePriceOracle}.`);
    }
    if (chain.staticFeedRegistry &&
        chain.slippageFeedRegistry &&
        !addressesEqual(chain.staticFeedRegistry, chain.slippageFeedRegistry)) {
        warnings.push(`On-chain feed registries differ: staticAllocation=${chain.staticFeedRegistry}, slippage=${chain.slippageFeedRegistry}.`);
    }
    const mismatches = checks
        .filter((check) => check.status === 'mismatch')
        .map((check) => `${check.field}: ${check.detail}`);
    const ok = mismatches.length === 0;
    return {
        ok,
        executorModuleAddress: chain.executorModuleAddress,
        rpcUrl,
        checks,
        mismatches,
        warnings,
        message: ok
            ? 'Deployment verification passed. Compared troubleshooting summary + env hints against on-chain state.'
            : `Deployment verification found ${mismatches.length} mismatch(es).`
    };
}
