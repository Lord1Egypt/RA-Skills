---
name: mermaid-diagrams
description: >
  Generate architecture diagrams (network, system, cloud, microservices) and sequence diagrams
  (API flows, auth flows, data flows) as PNG files using Mermaid. Use when asked to create,
  draw, or diagram anything including system architecture, network topology, cloud infrastructure,
  API request flows, authentication flows, CI/CD pipelines, database flows, or any other technical
  diagram. Triggers on phrases like "create a diagram", "draw", "diagram this", "architecture
  diagram", "sequence diagram", "flow diagram", "network diagram", "system design diagram".
---

# Mermaid Diagrams Skill

Generates Mermaid diagrams and renders them to PNG using the `mmdc` CLI.

## Reference Files
- **Architecture patterns** (flowchart, C4, cloud, network, microservices) → `references/architecture-patterns.md`
- **Sequence diagram patterns** (API flows, auth, CI/CD, DLP flows) → `references/sequence-patterns.md`

Load the relevant reference file based on diagram type requested.

## Rendering Tool

Use **mermaid.ink** (free online renderer, no browser/install needed):

```bash
mkdir -p /home/bcaddy/.openclaw/workspace/diagrams
ENCODED=$(cat <input.mmd> | base64 -w 0)
curl -s "https://mermaid.ink/img/${ENCODED}?bgColor=white&width=2048" \
  -o /home/bcaddy/.openclaw/workspace/diagrams/<name>.png
```

- Output directory: `/home/bcaddy/.openclaw/workspace/diagrams/`
- Width: 2048px default; increase for very wide diagrams (`&width=3000`)
- Always create output directory first: `mkdir -p /home/bcaddy/.openclaw/workspace/diagrams`

## Workflow

### 1. Identify Diagram Type
- Network/system/cloud/microservices → use `flowchart` or `C4Context`
- API/auth/data flows, step-by-step processes → use `sequenceDiagram`
- When in doubt: sequence for "how does X work step by step", architecture for "what does X look like"

### 2. Load Reference File
- Architecture → `references/architecture-patterns.md`
- Sequence → `references/sequence-patterns.md`

### 3. Generate Mermaid Code
- Write complete, valid Mermaid syntax
- Use descriptive node labels (not just A, B, C)
- Use subgraphs to group related components in architecture diagrams
- Use alt/loop/note blocks to add clarity in sequence diagrams
- Match the style of the patterns in the reference file

### 4. Save .mmd File
Save to: `/home/bcaddy/.openclaw/workspace/diagrams/<descriptive-name>.mmd`

Use kebab-case, descriptive filenames: `auth-flow.mmd`, `aws-architecture.mmd`, `api-gateway-sequence.mmd`

### 5. Render to PNG via mermaid.ink
```bash
ENCODED=$(cat /home/bcaddy/.openclaw/workspace/diagrams/<name>.mmd | base64 -w 0)
curl -s "https://mermaid.ink/img/${ENCODED}?bgColor=white&width=2048" \
  -o /home/bcaddy/.openclaw/workspace/diagrams/<name>.png
```

### 6. Confirm Output
Report the full path to the saved PNG. Offer to adjust layout, add components, or generate a `.mmd` file for further editing in mermaid.live or VS Code.

## Tips
- `flowchart LR` for left-to-right pipelines and network flows
- `flowchart TD` for top-down hierarchies and cloud stacks
- Wide diagrams: increase `-w` (width); tall diagrams: increase `-H` (height)
- For very complex diagrams, break into multiple diagrams
- Always include a title comment at the top of the .mmd file: `%% Title: ...`
