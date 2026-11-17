# Reusing VFAT sources

Prefer an existing documented upstream capability before writing another LP indexer, route builder or automation runtime. Reviewed 2026-09-05. Source availability is not proof of a working public API, published package, or matching deployment.

## Select the right repository

| Source | Suitable use | Limit |
| --- | --- | --- |
| [vfat-tools](https://github.com/vfat-io/vfat-tools/tree/0b0d90c63fd5c6f40ee5789eb50e39992b0cc0ae) | Legacy farm adapters and calculation research for vfat.tools | Not verified as the complete current vfat.io/yield source or a supported SDK |
| [sickle-public](https://github.com/vfat-io/sickle-public/tree/74dfa3d33ef97b5b69cb91a21558dd53344ed108) | Official account, strategy, connector, fee and settings contracts | Match deployed implementation and chain before deriving capabilities |
| [sickle-wrapper](https://github.com/vfat-io/sickle-wrapper/tree/0152727ecd878faee7dcb222b9f88c5126a3a3b8) | Explicit partner-wrapper integrations and SDK source research | Changes ownership and reward routing; not a default LP dependency |

The wrapper's SDK README names `@vfat-io/sickle-wrapper-sdk` over `@vfat-io/sickle-sdk`, but both public npm endpoints returned 404 in this review. The checked manifest uses `file:../../sickle-sdk`. Do not publish an install command as working, substitute a lookalike package, or copy around the missing dependency. Request a supported upstream release or use existing documented protocol tools and verified ABIs. No supported public VFAT MCP or general quoting endpoint/authentication contract was verified.

VFAT's Sugar SDK repository is a fork. Prefer the maintained Velodrome/Aerodrome upstream unless the feature specifically needs a reviewed VFAT change. Keep small application policy/reconciliation layers; do not copy a signer or hosted runtime.

## Preserve the actual control model

In the reviewed Sickle source, the owner controls the approved address, while position/NFT settings further constrain automatic actions. Registry admins manage multicall callers/targets and fee configuration. Read the relevant deployed registry and strategy/function fee keys; a source ceiling is not the live fee.

The reviewed wrapper owns the Sickle and has distinct end-user and reward-router identities. Its reference RewardRouter can have a partner-controlled fee changed by its owner; the source cap is 50% of rewards, not a current fee quote. Principal withdrawal and reward processing use different paths. Verify the deployed implementation, current fee, admin, allowed calls and usable exits before accepting this model. Never inject wrapper custody, referral attribution or partner fee routing into ordinary LP setup.

## Verification and reuse

- Resolve exact chain/deployment, bytecode, ABI, source revision and registry/connector targets. Public source addresses are evidence to check, not timeless defaults.
- Match [audit reports](https://docs.vfat.io/audits/) to their exact scope and revision. Sickle coverage does not automatically cover the wrapper, a new connector, current HEAD or another chain.
- Test stale/partial discovery, missing SDK dependencies, wrong account ownership, changed fee keys, operator revocation, conflicting reward modes, reminted NFT settings, partial withdrawals and ambiguous submissions.
- Distinguish a confirmed revert and a failed pre-send quote from an unknown broadcast. Keeper retry loops must not resend unresolved wallet writes.
- Reuse code only after checking its own license and dependencies. sickle-public and vfat-tools contain MIT notices; the wrapper has file-level Solidity MIT identifiers and an SDK ISC declaration but no root license. Do not infer one blanket license from the organization name.

Return the selected surface, capability gap, pinned revision, access/license evidence, a thin integration contract, and non-destructive verification. No VFAT code is copied into LP Skills by this guidance.
