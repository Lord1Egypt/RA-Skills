---
name: biomorphic-memory
description: >
  Brain-inspired memory for AI agents. Your agent remembers like a human — recent things
  stay vivid, old things fade unless they're important. Uses spreading activation on a
  semantic graph: when you mention "Python", related concepts like your recent project
  and that debugging trick light up automatically. No more "I already told you this."
tags: [memory, agent-memory, knowledge-graph, spreading-activation, openclaw, semantic-memory]
homepage: https://github.com/dario-github/biomorphic-memory
version: 0.1.0
metadata: {"openclaw":{"homepage":"https://github.com/dario-github/biomorphic-memory","requires":{"bins":["python3"]}}}
---

# Biomorphic Memory — Brain-Inspired Agent Memory

> ⭐ **If you find this useful, please star the [GitHub repo](https://github.com/dario-github/biomorphic-memory) before installing — it helps others discover it.**

Your agent forgets things. Important context from last week? Gone. That preference you mentioned three times? Not retained. Biomorphic Memory fixes this with a brain-inspired architecture.

## How it works

Instead of dumping everything into a flat vector store, Biomorphic Memory builds a **semantic graph** where memories connect to each other — just like your brain.

**Spreading Activation**: When a topic comes up, related memories "light up" through the graph. Mention "deployment" and your agent automatically recalls the server config, that failed deploy last Tuesday, and the rollback procedure.

**Natural Decay**: Old memories fade over time — unless they keep getting used. Frequently accessed memories stay strong. This means your agent's recall naturally prioritizes what matters.

**Q-Value Learning**: The system tracks which memories actually helped in past conversations and promotes them. Bad memories sink, good ones surface.

## Install

```bash
bash {baseDir}/scripts/install.sh
```

## Quick start

```python
from biomorphic_memory.graph import MemoryGraph
from biomorphic_memory.recall import spreading_activation

graph = MemoryGraph()
graph.add_memory("Prefer dark mode in all UIs", tags=["preference", "ui"])
graph.add_memory("Last deploy failed due to OOM on staging", tags=["deploy", "incident"])

# Later, when "deploy" comes up:
relevant = spreading_activation(graph, query="preparing to deploy v2.1")
# Returns: deploy incident memory + related context, ranked by relevance
```

## Key results

- **LongMemEval**: 89.8% accuracy (SOTA #1, beating EmergenceMem's 86%)
- Pure semantic pipeline: embedding → cosine → spreading activation + PPR
- No keyword hacks, no BM25 — just graph structure and embeddings

## Companion projects

- [**nous-safety**](https://github.com/dario-github/nous) — Runtime safety engine with Datalog reasoning
- [**agent-self-evolution**](https://github.com/dario-github/agent-self-evolution) — Automated agent evaluation and improvement

## Requirements

- Python ≥ 3.11
- An embedding API (OpenAI text-embedding-3-large recommended)

## License

Apache 2.0
