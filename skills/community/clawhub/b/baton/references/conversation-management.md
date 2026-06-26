# Conversational Baton management

The main agent can operate Baton via natural language.

## Examples

User: "Rescan providers and models for Baton."
Action: run `baton-model-manager.mjs scan --write`, then show added/removed/discovered counts.

User: "Add Claude Sonnet to Baton and use it for writing and validation."
Action: add the ref if discoverable, then add to `creative` and `strong_reasoning` tiers.

User: "Remove OpenAI from Baton for now."
Action: list matching OpenAI refs, remove/block them after confirmation if broad/destructive.

User: "Set Baton to careful mode for this agent."
Action: update agent overlay config with `executionMode: "careful"`.

User: "Don't hit Anthropic rate limits."
Action: reduce Anthropic provider concurrency and increase cooldown in `rate-limits.json`.

## Ambiguity handling

If a model name is ambiguous, show matching refs and ask for selection. If the user supplied an exact `provider/model` ref, act directly.
