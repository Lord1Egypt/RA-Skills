/**
 * @asgcard/sdk — x402 payment utilities for Stellar
 *
 * Builds and signs Soroban SAC USDC transfer transactions
 * for the x402 payment protocol.
 *
 * Uses the canonical AssembledTransaction + signAuthEntries() approach
 * as documented in the official Stellar docs and @x402/stellar.
 */
import {
  Keypair,
  Networks,
  TransactionBuilder,
  nativeToScVal,
  Address,
  Contract,
  rpc as StellarRpc,
  contract,
} from "@stellar/stellar-sdk";
import { PaymentError, InsufficientBalanceError } from "../errors";
import type {
  WalletAdapter,
  X402Accept,
  X402Challenge,
  X402PaymentPayload,
} from "../types";

const DEFAULT_FEE = "50000";
const DEFAULT_BASE_FEE_STROOPS = 10_000;
const SOROBAN_TIMEOUT = 300;
// Auth entry valid for ~1 minute (12 ledgers at ~5s each)
// Keep this small — facilitator rejects "too far" expirations
const AUTH_ENTRY_LEDGER_OFFSET = 12;
const RPC_URL = "https://mainnet.sorobanrpc.com";

// ── Challenge parsing ────────────────────────────────────

const isChallenge = (input: unknown): input is X402Challenge => {
  if (!input || typeof input !== "object") return false;
  const r = input as Record<string, unknown>;
  return r.x402Version === 2 && Array.isArray(r.accepts);
};

export const parseChallenge = (input: unknown): X402Accept => {
  if (!isChallenge(input) || input.accepts.length === 0) {
    throw new PaymentError("Invalid x402 challenge payload");
  }
  return input.accepts[0];
};

// ── Balance check ────────────────────────────────────────

export const checkBalance = async (params: {
  rpcServer: StellarRpc.Server;
  publicKey: string;
  asset: string;
  requiredAtomic: bigint;
}): Promise<void> => {
  const c = new Contract(params.asset);
  const account = await params.rpcServer.getAccount(params.publicKey);

  const tx = new TransactionBuilder(account, {
    fee: DEFAULT_FEE,
    networkPassphrase: Networks.PUBLIC,
  })
    .addOperation(
      c.call(
        "balance",
        new Address(params.publicKey).toScVal()
      )
    )
    .setTimeout(30)
    .build();

  const sim = await params.rpcServer.simulateTransaction(tx);
  if (!StellarRpc.Api.isSimulationSuccess(sim)) {
    throw new InsufficientBalanceError(params.requiredAtomic.toString(), "0");
  }

  const successSim = sim as StellarRpc.Api.SimulateTransactionSuccessResponse;
  const retVal = successSim.result?.retval;

  let balance = 0n;
  if (retVal) {
    try {
      // i128 returns a ChildStruct with _attributes.{hi, lo}
      const val = retVal.value() as any;
      if (val && typeof val === "object" && typeof val.lo === "function") {
        const lo = BigInt(val.lo()?.value?.() ?? val.lo()?._value ?? "0");
        const hi = BigInt(val.hi()?.value?.() ?? val.hi()?._value ?? "0");
        balance = (hi << 64n) + lo;
      } else {
        balance = BigInt(val?.toString() ?? "0");
      }
    } catch {
      balance = 0n;
    }
  }

  if (balance < params.requiredAtomic) {
    throw new InsufficientBalanceError(
      params.requiredAtomic.toString(),
      balance.toString()
    );
  }
};

// ── Build + sign payment transaction ─────────────────────

/**
 * Build a Soroban SAC USDC transfer transaction using AssembledTransaction,
 * then sign auth entries with signAuthEntries().
 *
 * This is the canonical x402 Stellar approach:
 * 1. AssembledTransaction.build() — simulates in Recording mode
 * 2. signAuthEntries() — converts SourceAccount → Address credentials
 * 3. simulate() — re-simulates in Enforcing mode to validate
 * 4. Return XDR (unsigned envelope — facilitator signs at settle)
 *
 * Reference:
 *   - https://developers.stellar.org/docs/build/guides/transactions/signing-soroban-invocations#method-2-auth-entry-signing
 *   - @x402/stellar exact/client/scheme.ts
 */
export const buildPaymentTransaction = async (params: {
  rpcServer: StellarRpc.Server;
  publicKey: string;
  accept: X402Accept;
  signer: Keypair;
}): Promise<string> => {
  const networkPassphrase = Networks.PUBLIC;

  // Step 1: Build + simulate (Recording Mode) via AssembledTransaction
  const tx = await contract.AssembledTransaction.build({
    contractId: params.accept.asset,
    method: "transfer",
    args: [
      nativeToScVal(params.publicKey, { type: "address" }),
      nativeToScVal(params.accept.payTo, { type: "address" }),
      nativeToScVal(BigInt(params.accept.amount), { type: "i128" }),
    ],
    networkPassphrase,
    rpcUrl: RPC_URL,
    parseResultXdr: (result: any) => result,
  });

  // Check simulation result
  if (
    !tx.simulation ||
    StellarRpc.Api.isSimulationError(tx.simulation)
  ) {
    const errMsg = tx.simulation
      ? (tx.simulation as StellarRpc.Api.SimulateTransactionErrorResponse).error
      : "No simulation result";
    throw new PaymentError(`Transaction simulation failed: ${errMsg}`);
  }

  // Step 2: Verify who needs to sign
  const missingSigners = tx.needsNonInvokerSigningBy();
  if (!missingSigners.includes(params.publicKey)) {
    throw new PaymentError(
      `Expected to sign with ${params.publicKey}, but got [${missingSigners.join(", ")}]`
    );
  }

  // Step 3: Sign auth entries — this converts SourceAccount → Address credentials
  const signer = contract.basicNodeSigner(params.signer, networkPassphrase);
  const latestLedger = (tx.simulation as StellarRpc.Api.SimulateTransactionSuccessResponse).latestLedger;
  const expiration = latestLedger + AUTH_ENTRY_LEDGER_OFFSET;

  await tx.signAuthEntries({
    address: params.publicKey,
    signAuthEntry: signer.signAuthEntry,
    expiration,
  });

  // Step 4: Re-simulate in Enforcing Mode to validate signatures
  await tx.simulate();
  if (
    !tx.simulation ||
    StellarRpc.Api.isSimulationError(tx.simulation)
  ) {
    const errMsg = tx.simulation
      ? (tx.simulation as StellarRpc.Api.SimulateTransactionErrorResponse).error
      : "No enforcing simulation result";
    throw new PaymentError(`Enforcing simulation failed: ${errMsg}`);
  }

  // Step 5: Verify all signatures collected
  const remainingSigners = tx.needsNonInvokerSigningBy();
  if (remainingSigners.length > 0) {
    throw new PaymentError(
      `Missing signatures from: [${remainingSigners.join(", ")}]`
    );
  }

  // Step 6: Build final TX with correct fee from Enforcing simulation
  const successSim = tx.simulation as StellarRpc.Api.SimulateTransactionSuccessResponse;
  const finalTx = TransactionBuilder.cloneFrom(tx.built!, {
    fee: (DEFAULT_BASE_FEE_STROOPS + parseInt(successSim.minResourceFee, 10)).toString(),
    sorobanData: tx.simulationData.transactionData,
    networkPassphrase,
  }).build();

  // Return unsigned envelope XDR — facilitator signs at settle time
  return finalTx.toXDR();
};

// ── Execute payment ──────────────────────────────────────

export const executePayment = async (params: {
  rpcServer: StellarRpc.Server;
  accept: X402Accept;
  keypair?: Keypair;
  walletAdapter?: WalletAdapter;
}): Promise<string> => {
  if (!params.keypair && !params.walletAdapter) {
    throw new PaymentError("No signing wallet configured");
  }

  const publicKey = params.keypair
    ? params.keypair.publicKey()
    : params.walletAdapter!.publicKey;

  // Optional balance check — non-critical
  try {
    await checkBalance({
      rpcServer: params.rpcServer,
      publicKey,
      asset: params.accept.asset,
      requiredAtomic: BigInt(params.accept.amount),
    });
  } catch (error) {
    if (error instanceof InsufficientBalanceError) throw error;
    // Swallow non-balance errors — facilitator will verify
  }

  // Build, simulate, sign auth entries
  if (params.keypair) {
    return buildPaymentTransaction({
      rpcServer: params.rpcServer,
      publicKey,
      accept: params.accept,
      signer: params.keypair,
    });
  }

  // WalletAdapter path — wallet must support signAuthEntry (SEP-43)
  const adapter = params.walletAdapter!;
  const c = new Contract(params.accept.asset);
  const sourceAccount = await params.rpcServer.getAccount(publicKey);

  const tx = new TransactionBuilder(sourceAccount, {
    fee: DEFAULT_FEE,
    networkPassphrase: Networks.PUBLIC,
  })
    .addOperation(
      c.call(
        "transfer",
        new Address(publicKey).toScVal(),
        new Address(params.accept.payTo).toScVal(),
        nativeToScVal(BigInt(params.accept.amount), { type: "i128" })
      )
    )
    .setTimeout(SOROBAN_TIMEOUT)
    .build();

  const sim = await params.rpcServer.simulateTransaction(tx);
  if (!StellarRpc.Api.isSimulationSuccess(sim)) {
    throw new PaymentError("Transaction simulation failed");
  }

  const assembled = StellarRpc.assembleTransaction(tx, sim).build();
  return adapter.signTransaction(assembled.toXDR(), Networks.PUBLIC);
};

// ── Build x402 PaymentPayload ────────────────────────────

export const buildPaymentPayload = (
  accepted: X402Accept,
  signedTransactionXDR: string
): string => {
  const payload: X402PaymentPayload = {
    x402Version: 2,
    accepted,
    payload: {
      transaction: signedTransactionXDR,
    },
  };

  return Buffer.from(JSON.stringify(payload), "utf8").toString("base64");
};

// ── Full handleX402Payment ───────────────────────────────

export const handleX402Payment = async (params: {
  rpcServer: StellarRpc.Server;
  challengePayload: unknown;
  keypair?: Keypair;
  walletAdapter?: WalletAdapter;
}): Promise<string> => {
  const accept = parseChallenge(params.challengePayload);

  const signedXDR = await executePayment({
    rpcServer: params.rpcServer,
    accept,
    keypair: params.keypair,
    walletAdapter: params.walletAdapter,
  });

  return buildPaymentPayload(accept, signedXDR);
};
