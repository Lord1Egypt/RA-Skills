# Tool contracts

Use this with [adapter architecture](adapter-architecture.md). Expose live LP capabilities and uncertainty as data. Do not make an agent infer them from prose or a failed transaction.

## Capability report

Return a versioned report for each chain and protocol:

```ts
type CapabilityReport = {
  schemaVersion: string;
  observedAt: string;
  chains: readonly {
    chainId: number;
    protocol: string;
    read: readonly string[];
    prepare: readonly string[];
    unsupported: readonly { action: string; reason: string }[];
  }[];
};
```

Capabilities come from deployed-code and integration checks, not a static marketing list. Name read, quote, prepare, simulate, submit, and confirm separately.

## Freshness report

Every indexed result should carry its chain anchor and lag:

```ts
type Freshness = {
  chainId: number;
  observedAt: string;
  rpcBlock: bigint;
  indexedBlock?: bigint;
  databaseBlock?: bigint;
  maxAgeSeconds: number;
  status: "fresh" | "lagging" | "diverged" | "unknown";
  reason?: string;
};
```

Execution must not treat `lagging`, `diverged`, or `unknown` snapshots as authority. It may continue only after fresh direct reads. Research may display the last good observation as labeled history.

## Prepared action union

Use mutually exclusive states:

```ts
type PreparedAction =
  | { status: "blocked"; reason: string; retryable: boolean }
  | {
      status: "approval-required";
      planDigest: `0x${string}`;
      approvals: readonly UnsignedStep[];
      rebuildAfterReceipts: true;
    }
  | {
      status: "ready";
      planDigest: `0x${string}`;
      transaction: UnsignedStep;
      decodedCalls: readonly string[];
      simulation: SimulationResult;
      expiresAt: string;
    };
```

Never return approvals and a ready action in the same result. Approval receipts change executable state, so rebuild and issue a new digest. A ready result contains one exact next write, not a queue of speculative calldata.

The digest binds schema version, chain, wallet, nonce policy, pool, position, inputs, recipients, targets, calldata, native value, limits, quote provenance, observation block, and expiry. Canonicalize the encoding before hashing.

## Confirmation and receipts

Keep these types distinct:

```ts
type SimulationResult = {
  blockNumber: bigint;
  success: boolean;
  gasEstimate: bigint;
  expectedStateDiff: readonly string[];
};

type ReceiptConfirmation = {
  planDigest: `0x${string}`;
  transactionHash: `0x${string}`;
  blockNumber: bigint;
  success: boolean;
  exactTransactionMatch: boolean;
  stateDiffMatch: boolean;
};
```

Confirmation verifies sender, chain, target, calldata, native value, receipt status, and expected state changes. Make receipt confirmation idempotent. Transaction preparation is freshness-sensitive and must not be treated as idempotent across state changes.

## Schema rules

- Reject unknown fields at wallet and execution boundaries.
- Carry integer amounts as decimal strings or big integers, never floating-point JSON numbers.
- Normalize addresses for comparison without discarding checksum presentation.
- Keep protocol identifiers, network identifiers, and schema versions separate.
- Paginate public position and pool lists. Do not silently exhaust large accounts.
- Return `unsupported`, `stale`, `unsafe`, and `unknown` as explicit states, never empty calldata or zero balances.

These contracts are provider-neutral. A local RPC adapter, indexer, official protocol builder, or another reviewed source can implement them without changing wallet authority.
