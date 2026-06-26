import {
  erc20Abi,
  formatUnits,
  getAddress,
  isAddress,
  maxUint256,
  parseUnits,
  type Address,
  type Hash
} from "viem";
import {
  findConfiguredTokenByAddress,
  findConfiguredTokenBySymbol,
  getConfiguredStablecoins,
  getNativeToken
} from "../chains/index.js";
import type { ChainName, TokenBalance, TokenInfo } from "../types.js";
import { formatTokenAmount } from "../utils/formatting.js";
import { WalletService } from "./walletService.js";

export class TokenService {
  public constructor(private readonly walletService: WalletService) {}

  public async resolveToken(chain: ChainName, tokenRef: string): Promise<TokenInfo> {
    if (isAddress(tokenRef)) {
      const normalizedAddress = getAddress(tokenRef);
      const configured = findConfiguredTokenByAddress(chain, normalizedAddress);
      if (configured) {
        return configured;
      }

      const publicClient = this.walletService.getPublicClient(chain);
      const [symbol, decimals, name] = await Promise.all([
        publicClient.readContract({
          address: normalizedAddress,
          abi: erc20Abi,
          functionName: "symbol"
        }),
        publicClient.readContract({
          address: normalizedAddress,
          abi: erc20Abi,
          functionName: "decimals"
        }),
        publicClient.readContract({
          address: normalizedAddress,
          abi: erc20Abi,
          functionName: "name"
        })
      ]);

      return {
        chain,
        symbol,
        decimals,
        address: normalizedAddress,
        name,
        isNative: false
      };
    }

    const configured = findConfiguredTokenBySymbol(chain, tokenRef);
    if (!configured) {
      throw new Error(`Unsupported token "${tokenRef}" on ${chain}.`);
    }

    return configured;
  }

  public async getTokenBalance(chain: ChainName, walletAddress: Address, token: TokenInfo): Promise<TokenBalance> {
    if (token.isNative) {
      const rawAmount = await this.walletService.getNativeBalance(chain, walletAddress);
      return {
        token,
        rawAmount: rawAmount.toString(),
        amount: formatTokenAmount(rawAmount, token.decimals)
      };
    }

    const publicClient = this.walletService.getPublicClient(chain);
    const rawAmount = await publicClient.readContract({
      address: token.address! as Address,
      abi: erc20Abi,
      functionName: "balanceOf",
      args: [walletAddress]
    });

    return {
      token,
      rawAmount: rawAmount.toString(),
      amount: formatTokenAmount(rawAmount, token.decimals)
    };
  }

  public async getConfiguredBalances(chain: ChainName, walletAddress: Address): Promise<{
    nativeBalance: TokenBalance;
    stablecoinBalances: TokenBalance[];
  }> {
    const nativeToken = getNativeToken(chain);
    const stablecoins = getConfiguredStablecoins(chain);

    const nativeBalance = await this.getTokenBalance(chain, walletAddress, nativeToken);
    const stablecoinBalances = await Promise.all(
      stablecoins.map((token) => this.getTokenBalance(chain, walletAddress, token))
    );

    return {
      nativeBalance,
      stablecoinBalances
    };
  }

  public async estimateTransferGas(
    chain: ChainName,
    sender: Address,
    recipient: Address,
    token: TokenInfo,
    amount: bigint
  ): Promise<bigint> {
    const publicClient = this.walletService.getPublicClient(chain);

    if (token.isNative) {
      return publicClient.estimateGas({
        account: sender,
        to: recipient,
        value: amount
      });
    }

    try {
      return await publicClient.estimateContractGas({
        account: sender,
        address: token.address! as Address,
        abi: erc20Abi,
        functionName: "transfer",
        args: [recipient, amount]
      });
    } catch (error) {
      const message = error instanceof Error ? error.message.toLowerCase() : String(error).toLowerCase();
      if (
        message.includes("transfer amount exceeds balance") ||
        message.includes("insufficient balance") ||
        message.includes("insufficient funds")
      ) {
        // Quotes and dry-runs may estimate a transfer before the bridged token arrives on the destination chain.
        return 65_000n;
      }
      throw error;
    }
  }

  public async transferToken(
    chain: ChainName,
    recipient: Address,
    token: TokenInfo,
    amount: bigint
  ): Promise<Hash> {
    if (token.isNative) {
      return this.walletService.sendTransaction(chain, {
        to: recipient,
        value: amount
      });
    }

    const walletClient = this.walletService.getWalletClient(chain);
    return walletClient.writeContract({
      account: this.walletService.requireAccount(),
      chain: this.walletService.getPublicClient(chain).chain,
      address: token.address! as Address,
      abi: erc20Abi,
      functionName: "transfer",
      args: [recipient, amount]
    });
  }

  public async ensureAllowance(
    chain: ChainName,
    token: TokenInfo,
    owner: Address,
    spender: Address,
    amount: bigint
  ): Promise<Hash | undefined> {
    if (token.isNative) {
      return undefined;
    }

    const publicClient = this.walletService.getPublicClient(chain);
    const currentAllowance = await publicClient.readContract({
      address: token.address! as Address,
      abi: erc20Abi,
      functionName: "allowance",
      args: [owner, spender]
    });

    if (currentAllowance >= amount) {
      return undefined;
    }

    const walletClient = this.walletService.getWalletClient(chain);
    const approvalHash = await walletClient.writeContract({
      account: this.walletService.requireAccount(),
      chain: publicClient.chain,
      address: token.address! as Address,
      abi: erc20Abi,
      functionName: "approve",
      args: [spender, maxUint256]
    });

    await this.walletService.waitForReceipt(chain, approvalHash);
    return approvalHash;
  }

  public amountToRaw(amount: string, token: TokenInfo): bigint {
    return parseUnits(amount, token.decimals);
  }

  public formatRawAmount(rawAmount: bigint, token: TokenInfo): string {
    return formatUnits(rawAmount, token.decimals);
  }
}
