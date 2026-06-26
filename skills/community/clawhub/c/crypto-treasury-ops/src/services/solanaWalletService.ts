import bs58 from "bs58";
import {
  Connection,
  Keypair,
  type SendOptions,
  type Transaction,
  type VersionedTransaction
} from "@solana/web3.js";
import { appConfig } from "../config.js";

function parseSolanaPrivateKey(rawValue: string): Uint8Array {
  const trimmed = rawValue.trim();
  if (!trimmed) {
    throw new Error("SOLANA_TREASURY_PRIVATE_KEY is empty.");
  }

  if (trimmed.startsWith("[")) {
    const parsed = JSON.parse(trimmed);
    if (!Array.isArray(parsed)) {
      throw new Error("SOLANA_TREASURY_PRIVATE_KEY JSON format must be an array of bytes.");
    }

    return Uint8Array.from(parsed.map((value) => Number(value)));
  }

  if (trimmed.includes(",")) {
    return Uint8Array.from(trimmed.split(",").map((value) => Number(value.trim())));
  }

  return Uint8Array.from(bs58.decode(trimmed));
}

export class SolanaWalletService {
  private readonly connections = appConfig.solana.rpcUrls.map(
    (rpcUrl) => new Connection(rpcUrl, "confirmed")
  );

  private readonly keypair = appConfig.solana.privateKey
    ? Keypair.fromSecretKey(parseSolanaPrivateKey(appConfig.solana.privateKey))
    : undefined;

  public requireKeypair(): Keypair {
    if (!this.keypair) {
      throw new Error("SOLANA_TREASURY_PRIVATE_KEY is required for Solana execution tools.");
    }

    return this.keypair;
  }

  public getTreasuryAddress(): string {
    return appConfig.solana.treasuryAddressOverride ?? this.requireKeypair().publicKey.toBase58();
  }

  public getPrimaryConnection(): Connection {
    const [connection] = this.connections;
    if (!connection) {
      throw new Error("At least one Solana RPC URL is required.");
    }

    return connection;
  }

  public getExtraRpcUrls(): string[] {
    return appConfig.solana.rpcUrls.slice(1);
  }

  public async withFallback<T>(operation: (connection: Connection) => Promise<T>): Promise<T> {
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

  public async signLegacyTransaction(transaction: Transaction): Promise<Transaction> {
    const keypair = this.requireKeypair();
    transaction.partialSign(keypair);
    return transaction;
  }

  public async signVersionedTransaction(transaction: VersionedTransaction): Promise<VersionedTransaction> {
    const keypair = this.requireKeypair();
    transaction.sign([keypair]);
    return transaction;
  }

  public async confirmSignature(signature: string, sendOptions?: SendOptions): Promise<void> {
    await this.withFallback((connection) =>
      connection.confirmTransaction(signature, sendOptions?.preflightCommitment ?? "confirmed").then(() => undefined)
    );
  }
}
