import { Interface, JsonRpcProvider, Wallet } from "ethers";
import { getRequiredWalletPrivateKey } from "../env";
import type { EncodedTransaction, ExecutedTransactionResult } from "../types";

const TOKEN_FACTORY_INTERFACE = new Interface([
  "event CreateToken(address indexed tokenAddress, uint8 tokenType, string name, string symbol, address implementation, address protocolRecipient, uint16 protocolPoint)"
]);

function getConfiguredMinPriorityFeePerGasWei(): bigint | undefined {
  const configured = process.env.ELEMENT_MIN_PRIORITY_FEE_PER_GAS_WEI;
  if (!configured) {
    return undefined;
  }
  const parsed = BigInt(configured);
  if (parsed <= 0n) {
    throw new Error("ELEMENT_MIN_PRIORITY_FEE_PER_GAS_WEI must be greater than 0");
  }
  return parsed;
}

export function buildFeeOverrides(input: {
  maxFeePerGas?: bigint | null;
  maxPriorityFeePerGas?: bigint | null;
  gasPrice?: bigint | null;
  minPriorityFeePerGas?: bigint;
}) {
  const minPriorityFeePerGas = input.minPriorityFeePerGas ?? getConfiguredMinPriorityFeePerGasWei();
  if (input.maxFeePerGas !== null && input.maxFeePerGas !== undefined) {
    const feeOverrides: { maxFeePerGas: bigint; maxPriorityFeePerGas?: bigint } = {
      maxFeePerGas: input.maxFeePerGas
    };
    const priorityFee =
      input.maxPriorityFeePerGas !== null && input.maxPriorityFeePerGas !== undefined
        ? minPriorityFeePerGas !== undefined && input.maxPriorityFeePerGas < minPriorityFeePerGas
          ? minPriorityFeePerGas
          : input.maxPriorityFeePerGas
        : minPriorityFeePerGas;
    if (priorityFee !== undefined) {
      feeOverrides.maxPriorityFeePerGas = priorityFee;
      if (feeOverrides.maxFeePerGas < priorityFee) {
        feeOverrides.maxFeePerGas = priorityFee;
      }
    }
    return feeOverrides;
  }
  if (input.gasPrice !== null && input.gasPrice !== undefined) {
    return {
      gasPrice:
        minPriorityFeePerGas !== undefined && input.gasPrice < minPriorityFeePerGas
          ? minPriorityFeePerGas
          : input.gasPrice
    };
  }
  return minPriorityFeePerGas === undefined
    ? {}
    : {
        maxPriorityFeePerGas: minPriorityFeePerGas,
        maxFeePerGas: minPriorityFeePerGas
      };
}

export function parseMinimumTipCapWei(error: unknown): bigint | null {
  const message = error instanceof Error ? error.message : String(error);
  const match = message.match(/minimum needed\s+(\d+)/i);
  return match ? BigInt(match[1]) : null;
}

export async function sendEncodedTransaction(input: {
  rpcUrl: string;
  transaction: EncodedTransaction;
  waitConfirmations?: number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}): Promise<ExecutedTransactionResult> {
  input.logger?.("send transaction:start", {
    rpcUrl: input.rpcUrl,
    to: input.transaction.to,
    value: input.transaction.value,
    waitConfirmations: input.waitConfirmations ?? 1
  });
  const privateKey = getRequiredWalletPrivateKey();
  const provider = new JsonRpcProvider(input.rpcUrl);
  const wallet = new Wallet(privateKey, provider);
  let minPriorityFeePerGas: bigint | undefined;
  let response;
  for (let attempt = 1; attempt <= 2; attempt += 1) {
    const feeData = await provider.getFeeData();
    const feeOverrides = buildFeeOverrides({
      maxFeePerGas: feeData.maxFeePerGas,
      maxPriorityFeePerGas: feeData.maxPriorityFeePerGas,
      gasPrice: feeData.gasPrice,
      minPriorityFeePerGas
    });
    try {
      response = await wallet.sendTransaction({
        to: input.transaction.to,
        value: input.transaction.value,
        data: input.transaction.data,
        ...feeOverrides
      });
      break;
    } catch (error) {
      const minimumTipCapWei = parseMinimumTipCapWei(error);
      if (attempt >= 2 || minimumTipCapWei === null) {
        throw error;
      }
      minPriorityFeePerGas = minimumTipCapWei;
      input.logger?.("send transaction:retry-min-tip-cap", {
        minimumTipCapWei: minimumTipCapWei.toString()
      });
    }
  }
  if (!response) {
    throw new Error("Transaction response missing after send attempt");
  }
  const receipt = await response.wait(input.waitConfirmations ?? 1);
  if (!receipt) {
    throw new Error(`Transaction receipt missing for ${response.hash}`);
  }
  if (receipt.status !== 1) {
    throw new Error(`Transaction failed: ${response.hash}`);
  }

  let contractAddress: string | undefined;
  for (const log of receipt.logs) {
    try {
      const parsed = TOKEN_FACTORY_INTERFACE.parseLog(log);
      if (parsed?.name === "CreateToken") {
        contractAddress = String(parsed.args.tokenAddress).toLowerCase();
        break;
      }
    } catch {
      // ignore unrelated logs
    }
  }

  input.logger?.("send transaction:confirmed", {
    hash: response.hash,
    blockNumber: receipt.blockNumber,
    contractAddress
  });

  return {
    hash: response.hash,
    contractAddress,
    receipt: {
      hash: receipt.hash,
      blockNumber: receipt.blockNumber,
      status: receipt.status,
      gasUsed: receipt.gasUsed.toString()
    }
  };
}
