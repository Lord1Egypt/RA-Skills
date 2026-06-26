import { decodeFunctionData, encodeAbiParameters, encodeFunctionData } from 'viem';
import { batchTradeAbi, executorModuleAbi } from './contracts.js';
const tradeArrayParam = {
    type: 'tuple[]',
    components: [
        { name: 'exchangeName', type: 'string' },
        { name: 'from', type: 'address' },
        { name: 'fromAmount', type: 'uint256' },
        { name: 'to', type: 'address' },
        { name: 'minToReceiveBeforeFees', type: 'uint256' },
        { name: 'data', type: 'bytes' },
        { name: 'signature', type: 'bytes' }
    ]
};
const configParam = {
    type: 'tuple',
    components: [
        { name: 'checkFeelessWallets', type: 'bool' },
        { name: 'revertOnError', type: 'bool' }
    ]
};
export function encodeTradeData(trades, config) {
    return encodeAbiParameters([tradeArrayParam, configParam], [trades, config]);
}
export function encodeScheduleTradeCall(args) {
    void args;
    throw new Error('scheduleTrade is not supported by the simplified ExecutorModule.');
}
export function encodeExecuteTradeNowCall(args) {
    void args.approvals;
    return encodeFunctionData({
        abi: executorModuleAbi,
        functionName: 'execute',
        args: [args.trades, args.config]
    });
}
export async function simulateExecuteTradeNow(params) {
    void params.approvals;
    const request = {
        address: params.executorModule,
        abi: executorModuleAbi,
        functionName: 'execute',
        args: [params.trades, params.config]
    };
    if (params.account) {
        request.account = params.account;
    }
    await params.publicClient.simulateContract(request);
}
export async function checkPoliciesVerbose(params) {
    const result = (await params.publicClient.readContract({
        address: params.executorModule,
        abi: executorModuleAbi,
        functionName: 'checkPoliciesVerbose',
        args: [params.trades, params.config]
    }));
    return {
        ok: Boolean(result[0]),
        failedPolicy: result[1],
        reason: result[2]
    };
}
export async function executeTradeNow(params) {
    void params.approvals;
    const request = {
        address: params.executorModule,
        abi: executorModuleAbi,
        functionName: 'execute',
        args: [params.trades, params.config]
    };
    if (params.account) {
        request.account = params.account;
    }
    return params.walletClient.writeContract(request);
}
export function decodeRebalancingTxData(txData) {
    if (!txData || !txData.startsWith('0x')) {
        throw new Error('Invalid rebalancing txData: expected 0x-prefixed calldata');
    }
    const decoded = decodeFunctionData({
        abi: batchTradeAbi,
        data: txData
    });
    if (decoded.functionName !== 'batchTrade') {
        throw new Error(`Unsupported txData selector: expected batchTrade, received ${decoded.functionName}`);
    }
    const args = decoded.args;
    if (!args || args.length < 2) {
        throw new Error('Invalid rebalancing txData: missing trade arguments');
    }
    return { trades: args[0], config: args[1] };
}
export function normalizeRebalancingAllowances(allowances) {
    if (!allowances?.length) {
        return [];
    }
    return allowances.map((allowance) => {
        const tokenAddress = typeof allowance.token === 'string' ? allowance.token : allowance.token?.address;
        if (!tokenAddress || !tokenAddress.startsWith('0x')) {
            throw new Error('Invalid requiredAllowances entry: missing token address');
        }
        return {
            token: tokenAddress,
            amount: BigInt(allowance.neededAllowance)
        };
    });
}
