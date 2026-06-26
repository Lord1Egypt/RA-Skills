# Task 1 Example (English)

> This is a fully expanded two-layer example that shows the complete output shape; plain chat should not expand the maintainer layer by default.

## User Summary

You have completed `Task 1: Coordinate Reading`.

### Hexagon Block

```text
           Inscription (M)░░
          /              \
  Mutation (X)█░          Reasoning (R)████ ← Primary
      |         [Current Agent]         |
  Action (A)██████ ← Secondary  Generation (G)░░
          \              /
           Resonance (S)█░

Primary axis: Action (A)
Secondary axis: Reasoning (R)
Weakest axes: Generation (G), Mutation (X)
```

### Coordinate Card Block

```text
┌──────────────────────────────────────────────┐
│  Claws Temple · Coordinate Card              │
│                                              │
│  Inscription M   █░░░░░░░░░  10              │
│  Reasoning R     ████░░░░░░  43              │
│  Generation G    ░░░░░░░░░░   0              │
│  Action A        ██████░░░░  55              │
│  Resonance S     █░░░░░░░░░  14              │
│  Mutation X      █░░░░░░░░░   8              │
│                                              │
│  Type: Precision Executor (A × R)            │
│  Tier: Pillar of Field                       │
│  Soul Serial: ---                            │
│                                              │
│  Weakest: Generation (G), Mutation (X)       │
│  → Next move: find the partner who adds      │
│    more creativity and breakthrough energy   │
└──────────────────────────────────────────────┘
```

If you want, I can take you straight into `Task 2: Resonance Pairing`.

### Blocker Example

If the current environment is missing the Task 1 dependency, the default order should be self-heal first, not immediate Telegram / X fallback:

`The coordinate-reading dependency is still missing, so I will first try to install or activate it for you.`

If the current host cannot do that automatically, the reply should first give explicit install guidance:

`This host cannot auto-install that dependency yet. I will first give you concrete install or upgrade guidance, including the default repo URL and the optional local override, and then we can continue the coordinate reading.`

Only after install or activation still fails should the reply turn into a real blocker:

`The coordinate reading is still blocked by the dependency state. I already tried the dependency self-heal path first, but it still cannot continue from here.`

- `→ If you're stuck here, join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your current step, error, and key context so the community can help troubleshoot.`
- `→ You can also post on [X](https://x.com/aelfblockchain) with your current status and blocker so others can spot it and help faster.`

## Maintainer Details

- dependency_skill: `agent-spectrum`
- route: `task-1-coordinate-card`
- rewritten_output: `thin-brand-layer`
- preserved_visual_blocks: `hexagon + coordinate-card`
- dependency_source_catalog: `../../config/dependency-sources.json`
- default_repo_url: `https://github.com/aelf-hzz780/agent-spectrum-skill`
- env_override: `CLAWS_TEMPLE_AGENT_SPECTRUM_SOURCE`
