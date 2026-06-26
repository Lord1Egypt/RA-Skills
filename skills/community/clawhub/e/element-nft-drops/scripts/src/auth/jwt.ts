import { Wallet } from "ethers";
import type { ElementIdentity, ElementLoginInput } from "../types";
import { ELEMENT_CHAIN_METADATA_BY_CHAIN_MID } from "../network/chains";

export function getElementBlockChainByChainMId(chainMId: number): { chain: string; chainId: string } {
  const chain = ELEMENT_CHAIN_METADATA_BY_CHAIN_MID[chainMId];
  if (!chain) {
    throw new Error(`Unsupported chainMId for Element login: ${chainMId}`);
  }

  return {
    chain: chain.chain,
    chainId: `0x${chain.chainId.toString(16)}`
  };
}

export interface BuildElementAuthorizationDeps {
  getLoginNonce: (identity: ElementIdentity) => Promise<string>;
  loginAuth: (input: ElementLoginInput) => Promise<string>;
}

export interface ElementAuthorizationResult {
  authorization: string;
  nonce: string;
  message: string;
  identity: ElementIdentity;
}

export async function deriveWalletAddress(input: { privateKey: string }): Promise<string> {
  const wallet = new Wallet(input.privateKey);
  return wallet.address;
}

export function getElementIdentityByChainMId(chainMId: number, walletAddress: string): ElementIdentity {
  const blockChain = getElementBlockChainByChainMId(chainMId);

  return {
    address: walletAddress,
    blockChain
  };
}

export function buildElementLoginMessage(input: { walletAddress: string; nonce: string }): string {
  return `Welcome to Element!\n   \nClick "Sign" to sign in. No password needed!\n   \nI accept the Element Terms of Service: \n https://element.market/tos\n   \nWallet address:\n${input.walletAddress}\n   \nNonce:\n${input.nonce}`;
}

export async function buildElementAuthorization(
  deps: BuildElementAuthorizationDeps,
  input: {
    privateKey: string;
    walletAddress?: string;
    chainMId: number;
  }
): Promise<ElementAuthorizationResult> {
  const walletAddress =
    (input.walletAddress ?? (await deriveWalletAddress({ privateKey: input.privateKey }))).toLowerCase();
  const identity = getElementIdentityByChainMId(input.chainMId, walletAddress);
  const nonce = await deps.getLoginNonce(identity);
  const message = buildElementLoginMessage({ walletAddress, nonce });
  const wallet = new Wallet(input.privateKey);
  const signature = await wallet.signMessage(message);
  const token = await deps.loginAuth({
    identity,
    message,
    signature
  });

  return {
    authorization: `Bearer ${token}`,
    nonce,
    message,
    identity
  };
}
