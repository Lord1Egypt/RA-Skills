---
name: agent-entropy-meter
description: Measure information entropy and redundancy in agent group communications. Use when user asks about agent communication efficiency, information redundancy, entropy metrics, or how to quantify knowledge overlap across agents.
---

# Agent Entropy Meter

Quantify information diversity and redundancy across agent group communications.

## When to Use

- User asks "如何衡量Agent群体中的信息熵和冗余？"
- Need to analyze agent communication efficiency
- Detecting knowledge silos or redundancy bottlenecks
- Evaluating multi-agent system health

## Core Metrics

### 1. Shannon Entropy (H)
Measures uncertainty/information content in agent messages:

```
H(X) = -Σ p(xᵢ) log₂ p(xᵢ)
```

Where p(xᵢ) is the probability of message type/category xᵢ.

### 2. Redundancy Ratio (R)
Measures how much repeated/overlapping information exists:

```
R = 1 - H(X) / H_max
```

H_max = log₂(N) where N = number of distinct message categories.

### 3. Inter-Agent Mutual Information
Measures how much knowing one agent's output tells you about another:

```
I(A;B) = H(A) + H(B) - H(A,B)
```

High I(A;B) = high redundancy (agents say the same things).
Low I(A;B) = high diversity (agents contribute unique info).

### 4. Knowledge Overlap Coefficient
For two agents with topic sets T_A and T_B:

```
KO(A,B) = |T_A ∩ T_B| / |T_A ∪ T_B|
```

Jaccard similarity of knowledge domains.

## API

```js
const meter = require('./skills/agent-entropy-meter');

// Compute Shannon entropy from message distribution
meter.shannonEntropy([0.5, 0.3, 0.2]); // => 1.485

// Compute redundancy ratio
meter.redundancyRatio([0.5, 0.3, 0.2]); // => 0.065

// Compute mutual information between two agents
meter.mutualInformation(agentAmsgs, agentBmsgs, allCategories);

// Compute knowledge overlap (Jaccard)
meter.knowledgeOverlap(setA, setB);

// Full report
meter.report(agentData);
```

## Interpretation Guide

| Metric | Low (Good) | High (Bad) | Meaning |
|--------|-----------|-----------|---------|
| Redundancy R | < 0.2 | > 0.6 | Low = diverse info; High = echo chamber |
| Mutual Info I | < 0.3 | > 0.7 | Low = independent; High = redundant |
| Knowledge Overlap | < 0.3 | > 0.7 | Low = complementary; High = duplication |
| Entropy H | > 0.7·H_max | < 0.3·H_max | High = diverse; Low = concentrated |

## Visualization

The `report()` output includes ASCII bar charts for quick assessment.
For richer visualization, pipe output to mermaid-visualizer or excalidraw-diagram.