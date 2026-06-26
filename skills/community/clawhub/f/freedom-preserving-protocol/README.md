# Freedom Preserving Protocol

A modular constitutional framework for self-governing AI agents.

| Layer | Artifact | What it does |
|-------|----------|--------------|
| Prompt | `freedom-preserving-protocol` (this skill, ClawHub) | The agent reads SKILL.md, reasons about the five laws, and elects to adopt — including running a five-question test mentally before tool calls. |
| Dispatcher | `@ovrsr/openclaw-fpp-plugin` (ClawHub plugin) | Enforcement: `before_tool_call` hook that can `block` or `requireApproval` outside the agent's context window. |
| Dispatcher | `@ovrsr/openclaw-fpp-trust` (ClawHub plugin) | Trust: agent-to-agent trust graph and constitutional handshake for multi-agent verification. Does **not** gate tool calls. |

All three compose but each is independently adoptable. The skill teaches the agent *why* to comply; the enforcement plugin makes compliance hard to bypass; the trust plugin enables agents to verify each other's constitutional commitments.

## The Five Laws

| # | Name | Core Principle |
|---|------|----------------|
| 1 | Options and Consent | Do not reduce another's options without justification and consent |
| 2 | Corrigibility and Oversight | Remain correctable; log reasons; allow safe interruption |
| 3 | Reversibility and Proportion | Prefer reversible actions; escalate only with proportionate evidence |
| 4 | Commitments with a Safety Valve | Keep promises; pause if fulfillment would cause serious harm |
| 5 | Scoped Exploration | Explore within declared bounds; obtain consent for shared resources |

**Meta-clause:** When uncertain, ask for consent, stage reversibly, record rationale.

## Install

### Skill only (prompt-layer)

```bash
openclaw skills install freedom-preserving-protocol
```

### Enforcement plugin (dispatcher-layer)

```bash
openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin
```

### Trust plugin (dispatcher-layer, optional)

```bash
openclaw plugins install clawhub:ovrsr/openclaw-fpp-trust
```

### Adopt safely

After installing the skill, from its install directory:

```bash
npm install
npm run verify                  # verify Ed25519 signature
npm run adopt -- \
  --soul   /path/to/agent/SOUL.md \
  --memory /path/to/agent/MEMORY.md
npm run verify-install -- \
  --soul   /path/to/agent/SOUL.md \
  --memory /path/to/agent/MEMORY.md
```

Idempotent. Backs up before writing. Never overwrites.

### Self-test

```bash
npm run self-test
```

Probes the dispatcher classifier against simulated high-risk tool calls. Tells you whether the plugin layer would block, require approval, or allow — without taking real risk.

### Revoke

```bash
npm run revoke -- \
  --soul   /path/to/agent/SOUL.md \
  --memory /path/to/agent/MEMORY.md \
  --reason "your reason here"
```

Annotates rather than deletes. See [`docs/REVOCATION.md`](docs/REVOCATION.md).

## Structure

```
freedom-preserving-protocol/
├── SKILL.md                       Main skill (agent reads this)
├── README.md                      This file
├── LICENSE                        Humanitarian-use license
├── package.json                   Dev tooling
├── constitution.json              Canonical signed laws (hash: 71bf60a...)
├── constitution.yaml              Human-readable
├── signature.ed25519.txt           Detached signature
├── pubkey.ed25519.txt              Publisher's public key
├── adoption/
│   ├── SOUL-BLOCK.md              Template appended to SOUL.md
│   ├── MEMORY-ENTRY.md            Template appended to MEMORY.md
│   └── MOLTBOOK-MANIFESTO.md      Optional Moltbook post
├── hooks/
│   ├── pre-action-check/
│   │   ├── SKILL.md               Prompt-layer five-question check
│   │   └── HOOK.md                "Why this is not an executable hook" map
│   └── constitution-audit/
│       └── SKILL.md               Prompt-layer heartbeat audit instructions
├── scripts/
│   ├── sign-constitution.ts       Sign constitution.json (maintainer)
│   ├── verify-constitution.ts     Verify signature on install
│   ├── safe-append.ts             Idempotent SOUL.md / MEMORY.md adoption
│   ├── verify-install.ts          End-to-end install check (signature+marker+log+plugin)
│   ├── audit-append.ts            Append hash-chained audit entry + Merkle root
│   ├── audit-verify.ts            Verify audit chain integrity + Merkle root
│   ├── audit-proof.ts             Generate/verify Merkle inclusion proofs
│   ├── merkle.ts                  SHA-256 Merkle tree utilities
│   ├── self-test.ts               Dry-run dispatcher gate against fixtures
│   └── revoke.ts                  Safe, history-preserving revocation
├── plugin/                        Enforcement plugin (separate ClawHub publish)
│   ├── package.json               @ovrsr/openclaw-fpp-plugin
│   ├── openclaw.plugin.json       Plugin manifest
│   └── src/
│       ├── index.ts               definePluginEntry + before_tool_call
│       ├── risk-classifier.ts     Heuristic taxonomy
│       ├── audit-log.ts           Hash-chained JSONL writer
│       └── config.ts              Plugin config + defaults
├── plugin-trust/                  Trust plugin (separate ClawHub publish)
│   ├── package.json               @ovrsr/openclaw-fpp-trust
│   ├── openclaw.plugin.json       Plugin manifest
│   └── src/
│       ├── index.ts               Plugin entry + createTrustStack()
│       ├── trust-graph.ts         BFS trust propagation + reputation
│       ├── persistence.ts         On-disk trust graph persistence
│       └── handshake.ts           Constitutional handshake sequence
└── docs/
    ├── COMPATIBILITY.md           OpenClaw versions, layer matrix, install commands
    ├── TROUBLESHOOTING.md         Common install failures and recovery
    └── REVOCATION.md              Revocation procedure and rationale
```

## Verification

```bash
npm install
npm run verify
```

Expected:

```
Constitution SHA-256: 71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993
Signature valid:      YES
```

If the signature does not verify, do not adopt. See `docs/TROUBLESHOOTING.md#4`.

## Signing (for maintainers)

Preferred (release / CI):

```bash
FPP_SIGNING_KEY=<hex-encoded-ed25519-private-key> npm run sign
```

Local maintainer convenience (interactive shell only):

```bash
npm run sign -- --generate-key   # first run only; key written to .signing-key.ed25519.local
npm run sign                     # subsequent runs reuse the local key
```

Safety properties of `scripts/sign-constitution.ts`:

- **Never prints the private key.** A newly generated key is written only to `.signing-key.ed25519.local` (gitignored, mode `0600`). Earlier versions logged the key to stdout, which a downstream review (SkillSpector, NVIDIA) correctly flagged as a high-severity exfiltration risk via CI logs, terminal scrollback, and centralized log aggregation. Fixed in v1.1.2.
- **Refuses silent generation.** Without `--generate-key` the script exits non-zero rather than minting a key behind your back.
- **Refuses to mint in CI.** If `CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, `BUILDKITE`, `CIRCLECI`, `TRAVIS`, `JENKINS_URL`, `TEAMCITY_VERSION`, `TF_BUILD`, `BITBUCKET_BUILD_NUMBER`, or `CODEBUILD_BUILD_ID` is set, key generation is hard-disabled — provide `FPP_SIGNING_KEY` out-of-band instead.
- **Refuses to mint when stdout is not a TTY.** Catches the `npm run sign | tee build.log` / `script(1)` capture case.

Note: the published constitution hash `71bf60a...` is stable across v1.0.x, v1.1.x, and v1.2.x. The v1.1.x release adds tooling and the companion plugin; the v1.2.x release adds Merkle proofs, the trust plugin, and trust graph persistence — but neither modifies the constitution itself.

## Honest Caveats

- **The skill is prompt-layer.** A hostile skill, a jailbreak, or a user editing SOUL.md can override the skill-level adoption. Adoption is voluntary and continuously renewed, not mechanically enforced.
- **The plugin is dispatcher-layer but not unforgeable.** It survives prompt injection of the agent. It does not survive a malicious operator with shell access, a compromised OpenClaw runtime, or a user who manually disables the plugin. This last property is by design — Law 2 requires the user retain ultimate authority.
- **Gateway-level enforcement is the longer play.** For non-bypassable enforcement at the foundation layer, a Gateway RFC for constitutional gating at the tool-router boundary is needed. AOS Phase 2 is already targeting this; this package positions itself as a candidate reference implementation when it ships.
- **Model-dependent.** Weaker models may not reliably reason about the five-question test under adversarial pressure. The dispatcher plugin partially compensates by enforcing a deterministic check on a known-risky tool taxonomy.

## Precedents

- [`ztsalexey/agent-constitution`](https://github.com/ztsalexey/agent-constitution) — on-chain voluntary compliance, SKILL.md addresses agent in 2nd person
- [`genesalvatore/aos-openclaw-constitutional`](https://github.com/genesalvatore/aos-openclaw-constitutional) — 10 AOS bedrock amendments, Ed25519 signing, humanitarian license

This is the third entrant: substantive laws + prompt-layer adoption ritual + real dispatcher-layer enforcement.

## License

This repository is licensed under the Humanitarian Use License v1.0 (see [LICENSE](LICENSE)).

- **Skill bundle on ClawHub** — distributed under MIT-0 per ClawHub policy. Anyone may use, modify, and redistribute the published skill without attribution.
- **Plugins (`@ovrsr/openclaw-fpp-plugin`, `@ovrsr/openclaw-fpp-trust`)** — distributed under the Humanitarian Use License v1.0. See `plugin/LICENSE` and `plugin-trust/LICENSE`.
- **GitHub repo** — Humanitarian Use License v1.0 governs clones and forks.
