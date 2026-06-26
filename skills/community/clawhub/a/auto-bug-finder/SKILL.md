# Auto Bug Finder — Code Security Scanner

Iterative, LLM-inspired bug detection and fixing system for production code. Currently supports Solidity (Hardhat + Slither). Extensible to Node.js, Python, and other stacks. Inspired by Andrej Karpathy's methodology: analyze → find → fix → test → repeat until clean.

## What It Does

Runs multi-tool security scans in iterative sprints:

1. **Scan** — Compiles, runs tests, runs static analysis (Slither for Solidity), checks coverage
2. **Analyze** — Parses all tool outputs into structured findings (Critical/High/Medium/Low/Info)
3. **Fix** — Generates patches for each finding with documentation
4. **Verify** — Recompiles, retests, rescans to confirm fixes
5. **Loop** — Repeats until 0 Critical/High/Medium findings OR 10 sprints max

## When To Use

- **Before marking any Solidity contract as complete** (mandatory per Netrix policy)
- **Before mainnet deployment** — catch issues cheaply on testnet
- **After major refactors** — verify no regressions
- **As part of CI/CD** — automated security gate

## How To Use

### Quick Start

```bash
# Copy the skill into your contract project
cp skills/auto-bug-finder/auto-bug-finder.js projects/my-contract/auto-bug-finder.js

# Run from the project root (where hardhat.config.js lives)
cd projects/my-contract
node auto-bug-finder.js
```

### Requirements

- Node.js 18+
- Hardhat project with existing tests
- Slither (`pip install slither-analyzer`)
- Solidity 0.8.x contracts

### Output

The script creates in `auto-bug-finder/`:
- `FINAL-REPORT.md` — Executive summary with all findings
- `sprint-results.json` — Detailed per-sprint data
- `patches/patch-N.md` — Per-finding documentation with fix rationale

### Customization

Edit the config at the top of `auto-bug-finder.js`:
```js
const CONFIG = {
  contractDir: 'contracts',      // Solidity source directory
  testFile: 'test/AgentEscrow.test.js',  // Test file to run
  maxSprints: 10,                // Safety limit
  severityGate: ['Critical', 'High', 'Medium'],  // Stop when these are 0
  heuristics: true,              // Enable custom heuristic checks
};
```

## Heuristic Checks (Beyond Slither)

- Missing zero-address validation on sensitive parameters
- Missing event emissions on state changes
- Self-escrow / self-interaction risks
- Unreachable enum states
- State transition completeness
- Access control gaps

## Auto-Audit Policy (MANDATORY — All Code)
- **All final code** (smart contracts, APIs, services, frontends) must pass Auto Bug Finder before marking complete
- **Gate:** 0 Critical, 0 High, 0 Medium findings required
- **Max Sprints:** 10 (safety limit)
- **Output:** `FINAL-REPORT.md` in project `auto-bug-finder/` directory
- PM cron checks for `FINAL-REPORT.md` before allowing completion mark

## First Run: Agent Escrow (2026-03-16)

| Sprint | Findings | Critical | High | Medium | Low | Info |
|--------|----------|----------|------|--------|-----|------|
| 1      | 7        | 0        | 0    | 0      | 2   | 5    |
| 2      | 7 (same) | 0        | 0    | 0      | 2   | 5    |

**Result:** ✅ LOW RISK — 2 improvements applied (removed unused `Status.Created`, added `SelfEscrow` check)
