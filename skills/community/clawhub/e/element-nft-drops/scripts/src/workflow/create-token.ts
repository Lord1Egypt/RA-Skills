import { buildElementAuthorization, deriveWalletAddress } from "../auth/jwt";
import { getRequiredWalletPrivateKey } from "../env";
import { getRpcUrlForChainMId } from "../network/rpc";
import { sendEncodedTransaction } from "../network/transaction";
import { normalizeCreateDropInput } from "../schema";
import type {
  CreateDropInput,
  CreateTokenPreflight,
  ElementApiResponse,
  EncodedTransaction,
  ExecutedTransactionResult
} from "../types";

export interface CreateTokenFlowDeps {
  deriveAddress: typeof deriveWalletAddress;
  resolveRpcUrl: typeof getRpcUrlForChainMId;
  createAuthorization: (input: {
    privateKey: string;
    walletAddress?: string;
    chainMId: number;
  }) => Promise<{
    authorization: string;
    nonce: string;
    message: string;
    identity: {
      address: string;
      blockChain: {
        chain: string;
        chainId: string;
      };
    };
  }>;
  postCreateToken: (
    authorization: string,
    body: { chainMId: number; name: string; symbol: string },
    walletAddress?: string
  ) => Promise<ElementApiResponse<EncodedTransaction>>;
  sendTransaction: typeof sendEncodedTransaction;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

export async function createTokenFlow(input: CreateDropInput, deps: CreateTokenFlowDeps) {
  const parsed = normalizeCreateDropInput(input);
  const privateKey = getRequiredWalletPrivateKey();
  const walletAddress = (await deps.deriveAddress({ privateKey })).toLowerCase();
  const rpcUrl = await deps.resolveRpcUrl(parsed.chainMId);
  const auth = await deps.createAuthorization({
    privateKey,
    walletAddress,
    chainMId: parsed.chainMId
  });
  const response = await deps.postCreateToken(
    auth.authorization,
    {
      chainMId: parsed.chainMId,
      name: parsed.name,
      symbol: parsed.symbol
    },
    walletAddress
  );

  if (response.code !== 0) {
    throw new Error(`createToken failed: ${response.message}`);
  }
  const transaction = await deps.sendTransaction({
    rpcUrl,
    transaction: response.data,
    logger: deps.logger
  });

  return {
    ...response,
    transaction: transaction satisfies ExecutedTransactionResult,
    preflight: {
      walletAddress,
      rpcUrl,
      authorization: auth.authorization,
      nonce: auth.nonce,
      loginMessage: auth.message,
      identity: auth.identity
    } satisfies CreateTokenPreflight
  };
}
