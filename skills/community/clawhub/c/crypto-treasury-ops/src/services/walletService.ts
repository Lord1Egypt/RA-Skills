import {
  createPublicClient,
  createWalletClient,
  fallback,
  formatUnits,
  http,
  type Address,
  type Hash,
  type Hex,
  type PublicClient,
  type WalletClient
} from "viem";
import { privateKeyToAccount, type PrivateKeyAccount } from "viem/accounts";
import { appConfig } from "../config.js";
import { getChainConfig } from "../chains/index.js";
import type { ChainName } from "../types.js";

export class WalletService {
  private readonly publicClients = new Map<ChainName, PublicClient>();
  private readonly walletClients = new Map<ChainName, WalletClient>();
  private readonly account?: PrivateKeyAccount;

  public constructor() {
    if (appConfig.wallet.privateKey) {
      this.account = privateKeyToAccount(appConfig.wallet.privateKey);
    }
  }

  public requireAccount(): PrivateKeyAccount {
    if (!this.account) {
      throw new Error("TREASURY_PRIVATE_KEY is required for execution tools.");
    }

    return this.account;
  }

  public getTreasuryAddress(): Address {
    return appConfig.wallet.treasuryAddressOverride ?? this.requireAccount().address;
  }

  public getPublicClient(chain: ChainName): PublicClient {
    const existing = this.publicClients.get(chain);
    if (existing) {
      return existing;
    }

    const config = getChainConfig(chain);
    const client = createPublicClient({
      chain: config.viemChain,
      transport: fallback(
        appConfig.rpcUrls[chain].map((url) =>
          http(url, {
            retryCount: 1,
            timeout: 10_000
          })
        ),
        {
          rank: false
        }
      )
    });
    this.publicClients.set(chain, client);
    return client;
  }

  public getWalletClient(chain: ChainName): WalletClient {
    const existing = this.walletClients.get(chain);
    if (existing) {
      return existing;
    }

    const config = getChainConfig(chain);
    const client = createWalletClient({
      account: this.requireAccount(),
      chain: config.viemChain,
      transport: fallback(
        appConfig.rpcUrls[chain].map((url) =>
          http(url, {
            retryCount: 1,
            timeout: 10_000
          })
        ),
        {
          rank: false
        }
      )
    });
    this.walletClients.set(chain, client);
    return client;
  }

  public async getNativeBalance(chain: ChainName, address: Address): Promise<bigint> {
    return this.getPublicClient(chain).getBalance({ address });
  }

  public async getNativeBalanceFormatted(chain: ChainName, address: Address): Promise<string> {
    const balance = await this.getNativeBalance(chain, address);
    return formatUnits(balance, getChainConfig(chain).decimals);
  }

  public async getGasPrice(chain: ChainName): Promise<bigint> {
    return this.getPublicClient(chain).getGasPrice();
  }

  public async sendTransaction(chain: ChainName, request: {
    to: Address;
    data?: Hex;
    value?: bigint;
    gas?: bigint;
  }): Promise<Hash> {
    const walletClient = this.getWalletClient(chain);
    return walletClient.sendTransaction({
      account: this.requireAccount(),
      chain: getChainConfig(chain).viemChain,
      to: request.to,
      data: request.data,
      value: request.value,
      gas: request.gas
    });
  }

  public async waitForReceipt(chain: ChainName, hash: Hash) {
    return this.getPublicClient(chain).waitForTransactionReceipt({ hash });
  }
}
