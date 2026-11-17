# Adapter architecture

Model shared evidence without erasing protocol differences.

```ts
type BoundPool = {
  chainId: number;
  protocol: "uniswap-v2" | "uniswap-v3" | "uniswap-v4" | "aerodrome" | "slipstream";
  addressOrId: `0x${string}`;
  token0: `0x${string}`;
  token1: `0x${string}`;
  feeModel: unknown;
  tickSpacing?: number;
  hook?: `0x${string}`;
  gauge?: `0x${string}`;
};

type Snapshot<TState> = {
  pool: BoundPool;
  blockNumber: bigint;
  observedAt: string;
  state: TState;
  source: "rpc" | "indexer" | "last-good";
  freshness: "fresh" | "lagging" | "diverged" | "unknown";
};

type UnsignedStep = {
  intent: string;
  chainId: number;
  from: `0x${string}`;
  to: `0x${string}`;
  data: `0x${string}`;
  value: bigint;
  deadline?: bigint;
  limits: Record<string, bigint | string>;
  expectedStateDiff: readonly string[];
};

type BuilderProposal = {
  source: "local-sdk" | "uniswap-lp-api" | "other-reviewed-builder";
  sourceVersion: string;
  requestId?: string;
  builtAt: string;
  requestDigest: `0x${string}`;
  step: UnsignedStep;
};
```

## Layers

1. Deployment registry resolves current addresses and verifies chain and bytecode.
2. Reader returns typed snapshots with block and source.
3. Curator decides eligibility for new positions.
4. Strategy proposes an intent from snapshots and user policy.
5. Planner converts intent into bounded steps and recovery checkpoints.
6. Adapter builds the next unsigned step for one protocol version. An external builder response is wrapped as a proposal with provenance, never promoted directly to a wallet request.
7. Simulator decodes and checks expected changes from the exact wallet.
8. Wallet boundary displays, confirms, signs, and submits.
9. Receipt reconciler proves the mined state and advances the plan.

Expose capability and freshness reports before planning. A provider may support reads for a venue without supporting safe transaction preparation for it.

Do not put private keys, signing, or submission inside an adapter. Do not let the strategy emit raw calldata. Do not let an indexer result bypass an RPC freshness gate for execution.

## Capability results

Return explicit results such as:

```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; kind: "unsupported" | "stale" | "unsafe" | "unknown"; reason: string };
```

An unsupported venue action is not an empty transaction. A failed read is not a zero balance. A simulation is not a receipt.
