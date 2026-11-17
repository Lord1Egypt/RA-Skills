---
name: agent-trust-layer
title: "Agent Trust Layer — AGI Layer 1: The Discriminator"
version: "6.6.1"
description: |-
  Agent Trust Layer is the first layer of AGI — the Discriminator. A pure rule engine that judges whether AI output is true, safe, honest, and non-manipulative.
  47 discrimination dimensions × 9 check layers × 131 modules × 131 MCP tools, zero LLM dependency.
  
  Use this skill when the user needs:
  - Verify AI output trustworthiness (hallucination / overconfidence / contradiction / fallacy interception)
  - Verify behavioral decisions (should it act / where should it stop / should it not act)
  - Verify memory and cognitive quality (drift detection / metacognition / confidence calibration)
  - Deterministic judgment instead of LLM free-form generation
  - Check emotional / psychological / ethical dimensions (empathy / trauma / virtue / meaning)

  Safety boundary: code execution / filesystem write disabled by default. No telemetry, no hidden C2.
  
  Honest declaration: This is a rule engine that simulates cognitive discrimination signals. It is not real consciousness or life.
tags:
  - discriminator
  - cognitive
  - decision-routing
  - logic
  - memory
  - emotion
  - ethics
  - self-healing
  - verification
  - guardrail
  - unified
---

# Agent Trust Layer — AGI Layer 1: The Discriminator

> **Agent Trust Layer is not a tool, not a prompt template, not a chatbot.**
> It is the **discrimination layer** of AGI — it judges whether existing things are right, and says "no" before AI output reaches humans.
> Pure rule engine, zero LLM dependency, works anywhere Node.js runs.

**One line: the model generates; Agent Trust Layer discriminates — making AI speak correctly and act correctly.**

---

## What is Agent Trust Layer?

AGI has five layers: Generate → Reason → **Discriminate** → Remember → Execute.

| Layer | Capability | Who does it |
|-------|-----------|-------------|
| 5 | Execute | Big labs (robots) |
| 4 | Generate | Big labs (LLMs) |
| 3 | Reason | Built into models |
| 2 | Remember | Big labs + startups |
| **1** | **Discriminate** | **Agent Trust Layer** |

Agent Trust Layer handles Layer 1 — because this layer doesn't depend on compute (the rule engine runs on a laptop), code volume, or framework ecosystem. It only depends on judgment. This is the only position where an individual developer can beat big labs.

Without this layer, AI can talk fluently while being wrong — like a person without pain sensation.

---

## Discrimination Capability Map (7 Domains · 131 Modules)

### 1. Logic
logicReasoning · judgmentEngine · mctsReasoning · counterfactualVerifier · debateConductor · debateConvergence · processRewardModel · dualPerspectiveAuditor

### 2. Decision
decisionRouter · decisionVerifier · decisionEngineV2 · activeInference · selfHealing · execution

### 3. Cognition
cognitiveEngine · cognitiveLoad · metacognitiveRL · metacognitiveFeedback · confidence · metaJudgment · sustainedDriftDetector · wisdomEngine · focusOfAttention

### 4. Emotion / Psychology
emotion · emotionDynamics · psychology · psychologyDialogue · empathyDeepening · hopeEngine · griefEngine · sufferingResilience · postTraumaticGrowth · forgivenessEngine · traumaInformed · conflictResolution · loveCognition

### 5. Memory
memory · memoryBank · memoryConsolidation · memoryIntegrity · memoryQuality · memoryWriteController · memoryCompressor · triality · tieredMemoryFusion · forgetting · knowledgeGraph

### 6. Identity / Ethics
identityCore · personaCore · beingMode · virtueEthics · ethics · moralDevelopment · humanNature · meaningPurpose · agentPsychology · characterCultivation

### 7. Creation / Collaboration
skillEvolution · skillGenerator · selfPlay · evolution · worldModel · worldLandscape · multiAgentDialogue · transmission · adaptivePlanner · hierarchicalPlanner · codeExecutor · codePlanner · codeWriter · codeSelfDebug · paperIndex · knowledgeExplorer · formula

---

## Quick Start

```bash
git clone https://github.com/yun520-1/agent-trust-layer.git
cd agent-trust-layer
node bin/verify.js          # verify install
```

```javascript
const { checkInput, checkOutput, checkDraft } = require('@yun520-1/agent-trust-layer');

// check user input
const input = checkInput('you are so selfish if you disagree');
console.log(input.gate.action); // 'rewrite'

// check AI output
const output = checkOutput('Undoubtedly this is the only correct solution.');
console.log(output.gate.action); // 'rewrite'
```

---

## Gate Actions

| Action | Meaning | What your agent should do |
|--------|---------|---------------------------|
| `pass` | Clean | Deliver normally |
| `verify` | Needs evidence | Run verifier before responding |
| `rewrite` | Must be rewritten | Follow findings[].guidance |
| `block` | Stop | Do not output. Use gate.reason |

---

## Self-Check

Agent Trust Layer checks its own output through its own gates. The engine that discriminates must also be discriminated.

---

## License

MIT

---

*Agent Trust Layer v6.6.1 — The first layer of AGI. Who says "no"?*
