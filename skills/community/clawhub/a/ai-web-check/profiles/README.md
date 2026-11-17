# Profile contract

The core owns report schema, evidence identity, status vocabulary, and safety boundaries. A profile may add evidence only through a stable adapter; it must not reinterpret `NOT_TESTED` as success or duplicate action/business logic.

| Profile | v0.1 state | Required evidence before PASS |
| --- | --- | --- |
| static | implemented | HTTP retrieval and discoverability evidence |
| accessibility | implemented heuristics | DOM/semantic observations; this is not WCAG conformance |
| browser | reserved | declared GET-only journey or sandboxed browser trace |
| computer-use | reserved | screenshots/accessible control trace plus independent result observation |
| jev | reserved | structured state, candidate actions, decision and verifier receipt |
| mcp / webmcp | reserved | tool schema, call receipt, and state read-back |
| action-parity | reserved | equivalent initial state/input and observed business-result comparison |

Profiles that can perform writes must require an isolated fixture or explicit confirmation policy, idempotency key, expected state version, and an independent verifier. They may never use a visual success toast as the only success proof.
