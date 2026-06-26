# Architecture

## Tactical architecture

```text
operator -> controller DM -> worker lane -> Claude Code worker -> worker lane -> controller DM
```

This is the pragmatic Discord-based architecture for a controller bot and a Claude Code worker bot.

## Why this pattern matters

A working rollout usually requires solving several separate problems:

1. task envelope standardization
2. worker-side bot-message gating
3. worker-side channel or runtime property mismatches
4. controller-side DM relay-back correlation

## Current recommendation

Use the Discord worker lane for real delegated work once the full closed loop is verified.

## Long-term architecture

A cleaner long-term design is still to move bot-to-bot transport off Discord and onto a direct authenticated transport such as:

- Gateway RPC
- internal HTTP API
- direct process or SDK bridge

In that future design, Discord remains the human-facing surface while machine-to-machine transport becomes explicit and more reliable.
