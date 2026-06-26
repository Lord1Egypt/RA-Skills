import { Connection, PublicKey } from "@solana/web3.js";
import { appConfig } from "../config.js";
import type { TokenBalance, TokenInfo } from "../types.js";
import { formatTokenAmount } from "../utils/formatting.js";

const SPL_TOKEN_PROGRAM_ID = new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA");

export class SolanaBalanceService {
  private readonly connections = appConfig.solana.rpcUrls.map(
    (rpcUrl) => new Connection(rpcUrl, "confirmed")
  );

  public async getConfiguredBalances(walletAddress: string): Promise<{
    nativeBalance: TokenBalance;
    stablecoinBalances: TokenBalance[];
  }> {
    const owner = new PublicKey(walletAddress);
    const nativeLamports = await this.withFallback((connection) => connection.getBalance(owner));
    const nativeToken: TokenInfo = {
      chain: "solana",
      symbol: "SOL",
      name: "Solana",
      decimals: 9,
      isNative: true
    };

    const tokenAccounts = await this.withFallback((connection) =>
      connection.getParsedTokenAccountsByOwner(
        owner,
        { programId: SPL_TOKEN_PROGRAM_ID },
        "confirmed"
      )
    );

    const balancesByMint = new Map<string, bigint>();
    for (const account of tokenAccounts.value) {
      const parsedData = account.account.data;
      if (!("parsed" in parsedData)) {
        continue;
      }

      const info = parsedData.parsed.info as {
        mint?: string;
        tokenAmount?: {
          amount?: string;
        };
      };

      if (!info.mint || !info.tokenAmount?.amount) {
        continue;
      }

      const current = balancesByMint.get(info.mint) ?? 0n;
      balancesByMint.set(info.mint, current + BigInt(info.tokenAmount.amount));
    }

    const stablecoinBalances = appConfig.solana.trackedTokens.map((token) => {
      const tokenInfo: TokenInfo = {
        chain: "solana",
        symbol: token.symbol,
        name: token.symbol,
        decimals: token.decimals,
        address: token.mint,
        isNative: false
      };
      const rawAmount = balancesByMint.get(token.mint) ?? 0n;
      return {
        token: tokenInfo,
        rawAmount: rawAmount.toString(),
        amount: this.formatSolanaAmount(rawAmount, token.decimals)
      };
    });

    return {
      nativeBalance: {
        token: nativeToken,
        rawAmount: nativeLamports.toString(),
        amount: this.formatSolanaAmount(BigInt(nativeLamports), 9)
      },
      stablecoinBalances
    };
  }

  private formatSolanaAmount(rawAmount: bigint, decimals: number): string {
    return formatTokenAmount(rawAmount, decimals);
  }

  private async withFallback<T>(operation: (connection: Connection) => Promise<T>): Promise<T> {
    let lastError: unknown;

    for (const connection of this.connections) {
      try {
        return await operation(connection);
      } catch (error) {
        lastError = error;
      }
    }

    throw lastError instanceof Error ? lastError : new Error("All Solana RPC endpoints failed.");
  }
}
