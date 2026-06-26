---
name: abi-toolchain
description: |
  ABI lifecycle management for smart contract projects. Use when your frontend is out of sync with contract changes, when you need to set up ABI generation in CI/CD, when dealing with ABI drift between deployments, managing proxy contract ABIs, or working with typechain/wagmi-generate/viem ABI types. Triggers on: ABI, typechain, wagmi generate, viem ABI, contract types, ABI drift, ABI mismatch, frontend out of sync with contract, ABI versioning, deployment artifacts, or any question about syncing frontend code to contract changes.
---

# ABI Toolchain

Treat your ABI like any other versioned artifact. Most frontend-contract sync bugs are ABI lifecycle problems in disguise.

## Scripts

Ready-to-use tools in `scripts/`:

| Script | Purpose |
|--------|---------|
| `sync-abi.sh` | Sync compiled ABIs from Foundry/Hardhat artifacts to frontend |
| `abi-diff.js` | Compare two ABI files: find added/removed/changed, flag breaking changes |

### sync-abi.sh

```bash
# Set which contracts to sync: create .abi-sync in your project root
echo "MyToken" >> .abi-sync
echo "MyVault:Vault" >> .abi-sync   # writes as Vault.json

# Run from your project root
ABI_SOURCE=out ABI_DEST=frontend/src/abis bash path/to/sync-abi.sh

# Or use defaults (Foundry: out/ → frontend/src/abis/)
bash scripts/sync-abi.sh
```

Handles both Foundry (`out/Foo.sol/Foo.json`) and Hardhat (`artifacts/contracts/`) artifacts. Uses `jq` if available, falls back to Python.

### abi-diff.js

```bash
node scripts/abi-diff.js old/MyToken.json new/MyToken.json
# → { added: [], removed: [], changed: [], breaking: false, summary: "0 added, 0 removed, 1 changed" }

# Exit code 1 if breaking changes (useful in CI):
node scripts/abi-diff.js prev.json current.json || echo "BREAKING CHANGE"
```

Accepts raw ABI arrays or Foundry/Hardhat artifacts (auto-detected).

## ABI Types Reference

See `references/abi-formats.md` for complete coverage of ABI entry types, function selectors, event topics, Foundry artifact structure, and common gotchas (tuples, uint vs uint256, `as const`).

## The Core Problem

When a contract changes:
1. New ABI gets compiled by Foundry/Hardhat
2. Frontend still imports the old ABI from a file that wasn't updated
3. Calls either fail silently or revert on-chain

The fix isn't careful manual updating — it's making the pipeline impossible to get wrong.

## Pattern 1: Foundry → TypeScript Auto-Sync

After every `forge build`, auto-export ABIs to your frontend:

```bash
# scripts/sync-abi.sh
#!/bin/bash
set -e
CONTRACTS=("MyToken" "MyVault" "MyFactory")
SRC="out"           # Foundry output dir
DEST="frontend/src/abis"

mkdir -p $DEST

for contract in "${CONTRACTS[@]}"; do
  jq '.abi' "$SRC/$contract.sol/$contract.json" > "$DEST/$contract.json"
  echo "✅ Synced $contract ABI"
done
```

Add to `foundry.toml` as a post-build hook or wire into `package.json`:
```json
{
  "scripts": {
    "build:contracts": "forge build && bash scripts/sync-abi.sh",
    "dev": "npm run build:contracts && next dev"
  }
}
```

## Pattern 2: Typed ABIs with Viem (no codegen)

Viem's `as const` trick gives you full TypeScript types directly from your ABI JSON:

```typescript
// abis/MyToken.ts — export from your synced JSON
export const myTokenAbi = [
  {
    name: 'transfer',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [{ name: 'to', type: 'address' }, { name: 'amount', type: 'uint256' }],
    outputs: [{ name: '', type: 'bool' }],
  },
  // ...
] as const   // ← critical: makes TypeScript infer exact types

// Now readContract/writeContract will type-check function names and args
const result = await client.readContract({
  abi: myTokenAbi,
  functionName: 'transfer',  // ← autocompletes, typos caught at compile time
  args: ['0x...', 100n],     // ← arg types inferred
})
```

## Pattern 3: Wagmi CLI Code Generation

For large projects, `@wagmi/cli` generates fully typed React hooks from your ABIs:

```bash
npm install --save-dev @wagmi/cli
```

```typescript
// wagmi.config.ts
import { defineConfig } from '@wagmi/cli'
import { foundry, react } from '@wagmi/cli/plugins'

export default defineConfig({
  out: 'src/generated.ts',
  plugins: [
    foundry({ project: '../contracts' }),  // reads Foundry artifacts directly
    react(),                                // generates useReadMyToken, useWriteMyToken, etc.
  ],
})
```

```bash
npx wagmi generate   # regenerate on every contract change
```

Add to CI: `npx wagmi generate && git diff --exit-code src/generated.ts` — fails if ABI was changed but not regenerated.

## Pattern 4: Proxy Contract ABIs

Proxy contracts (UUPS, Transparent) have two ABIs:
1. **Proxy ABI** — just `upgradeTo`, `upgradeToAndCall`, admin functions
2. **Implementation ABI** — your actual business logic

Always use the **implementation ABI** for user-facing calls, pointed at the **proxy address**:

```typescript
// WRONG: using proxy ABI loses all your functions
const client = getContract({ address: proxyAddr, abi: proxyAbi })

// RIGHT: implementation ABI + proxy address
const client = getContract({ address: proxyAddr, abi: myContractV2Abi })
```

For Hardhat upgrades, the generated `.json` artifacts include the merged ABI automatically. For Foundry, merge manually:

```bash
# Merge proxy + implementation ABIs
jq -s '.[0].abi + .[1].abi | unique_by(.name)' \
  out/ERC1967Proxy.sol/ERC1967Proxy.json \
  out/MyContractV2.sol/MyContractV2.json \
  > frontend/src/abis/MyContractProxy.json
```

## Pattern 5: CI/CD Enforcement

Block merges where ABI changed but frontend wasn't updated:

```yaml
# .github/workflows/abi-check.yml
- name: Check ABI sync
  run: |
    forge build
    bash scripts/sync-abi.sh
    git diff --exit-code frontend/src/abis/
    # Fails if any ABI file was changed without committing the update
```

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `function not found` on-chain | Calling old function name that was renamed | Re-sync ABI, check function selector |
| TypeScript accepts wrong arg type | `as const` missing on ABI | Add `as const` to ABI definition |
| Proxy call reverts | Using proxy ABI instead of implementation ABI | Always use implementation ABI at proxy address |
| Works in dev, fails on mainnet | ABI from local build ≠ deployed contract | Pin ABI to verified deployment, not latest build |
| Wagmi hook types wrong | Generated file not up to date | Re-run `npx wagmi generate` |

## References

- **ABI formats, types, selectors, gotchas:** `references/abi-formats.md`
- Viem ABI types: https://viem.sh/docs/glossary/types#abi
- Wagmi CLI: https://wagmi.sh/cli/getting-started
- Foundry artifacts format: https://book.getfoundry.sh/reference/forge/forge-build
