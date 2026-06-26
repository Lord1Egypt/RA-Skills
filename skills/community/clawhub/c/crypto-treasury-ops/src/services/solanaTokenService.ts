import { PublicKey } from "@solana/web3.js";
import type { TokenBalance, TokenInfo } from "../types.js";
import { formatTokenAmount } from "../utils/formatting.js";
import { SolanaWalletService } from "./solanaWalletService.js";

const SPL_TOKEN_PROGRAM_ID = new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA");

const SOLANA_NATIVE_TOKEN: TokenInfo = {
  chain: "solana",
  symbol: "SOL",
  name: "Solana",
  decimals: 9,
  address: "0x0000000000000000000000000000000000000000",
  isNative: true
};

const DEFAULT_TRACKED_TOKENS: TokenInfo[] = [
  SOLANA_NATIVE_TOKEN,
  {
    chain: "solana",
    symbol: "USDC",
    name: "USD Coin",
    decimals: 6,
    address: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    isNative: false
  },
  {
    chain: "solana",
    symbol: "USDT",
    name: "Tether USD",
    decimals: 6,
    address: "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    isNative: false
  }
];

export class SolanaTokenService {
  public constructor(private readonly solanaWalletService: SolanaWalletService) {}

  public resolveToken(tokenRef: string): TokenInfo {
    const normalized = tokenRef.trim().toUpperCase();
    const matched = DEFAULT_TRACKED_TOKENS.find((token) => token.symbol === normalized);
    if (!matched) {
      throw new Error(`Unsupported token "${tokenRef}" on Solana.`);
    }

    return matched;
  }

  public async getTokenBalance(walletAddress: string, token: TokenInfo): Promise<TokenBalance> {
    const owner = new PublicKey(walletAddress);
    if (token.isNative) {
      const lamports = await this.solanaWalletService.withFallback((connection) => connection.getBalance(owner));
      return {
        token,
        rawAmount: lamports.toString(),
        amount: formatTokenAmount(BigInt(lamports), token.decimals)
      };
    }

    const tokenAccounts = await this.solanaWalletService.withFallback((connection) =>
      connection.getParsedTokenAccountsByOwner(
        owner,
        { programId: SPL_TOKEN_PROGRAM_ID },
        "confirmed"
      )
    );

    const mintAddress = token.address;
    const rawAmount = tokenAccounts.value.reduce((sum, account) => {
      const parsedData = account.account.data;
      if (!("parsed" in parsedData)) {
        return sum;
      }

      const info = parsedData.parsed.info as {
        mint?: string;
        tokenAmount?: {
          amount?: string;
        };
      };

      if (!info.mint || info.mint !== mintAddress || !info.tokenAmount?.amount) {
        return sum;
      }

      return sum + BigInt(info.tokenAmount.amount);
    }, 0n);

    return {
      token,
      rawAmount: rawAmount.toString(),
      amount: formatTokenAmount(rawAmount, token.decimals)
    };
  }
}
