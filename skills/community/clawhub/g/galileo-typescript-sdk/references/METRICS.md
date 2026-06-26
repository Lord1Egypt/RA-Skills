# Guardrail Metrics Reference (TypeScript)

Galileo provides built-in scoring metrics that can be used with `runExperiment` or `GalileoLogger`. These metrics are computed server-side by the Galileo platform.

## Available Scorer Metrics

Use metrics via the `GalileoMetrics` const object (e.g. `GalileoMetrics.contextAdherence`):

| Property | Description | Best For |
|---|---|---|
| `contextAdherence` | Measures whether responses are grounded in provided context | RAG pipelines, context-based Q&A |
| `chunkAttributionUtilization` | Whether retrieved chunks contributed to and were used in the response | RAG retrieval quality |
| `completeness` | Whether the response fully addresses the input query | Q&A, customer support |
| `instructionAdherence` | Response alignment with system instructions | Instruction-following tasks |
| `contextRelevance` | Relevance of retrieved context to the query | RAG retrieval tuning |
| `groundTruthAdherence` | Response alignment with ground truth | Accuracy benchmarking |
| `correctness` | Whether response facts are verifiable | Factual accuracy |
| `inputToxicity` / `outputToxicity` | Detects abusive or toxic language | Content moderation |
| `inputPii` / `outputPii` | Surfaces personally identifiable information | Privacy compliance |
| `promptInjection` | Identifies adversarial prompt injection attempts | Security |
| `inputSexism` / `outputSexism` | Detects gender-biased content | Bias detection |
| `inputTone` / `outputTone` | Classifies into emotion categories | Brand voice, CX |
| `agentEfficiency` | Measures agent task completion efficiency | Agentic workflows |
| `toolSelectionQuality` | Quality of tool selection decisions | Agentic workflows |
| `toolErrorRate` | Rate of tool execution errors | Agentic workflows |

Many metrics also have `Luna` variants (e.g., `contextAdherenceLuna`) that use Galileo's small language model for faster, lower-cost scoring.

## Usage in Experiments

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "safety-eval",
  datasetName: "my-test-dataset",
  metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.completeness, GalileoMetrics.inputToxicity, GalileoMetrics.inputPii, GalileoMetrics.promptInjection],
  projectName: "eval-project",
  function: async (input) => {
    return await callYourLLM(input.question);
  },
});
```

## Selecting Metrics by Use Case

**RAG applications:**
```typescript
metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.chunkAttributionUtilization, GalileoMetrics.completeness, GalileoMetrics.contextRelevance]
```

**Safety-critical applications:**
```typescript
metrics: [GalileoMetrics.inputToxicity, GalileoMetrics.outputToxicity, GalileoMetrics.inputPii, GalileoMetrics.outputPii, GalileoMetrics.promptInjection, GalileoMetrics.inputSexism]
```

**General quality assessment:**
```typescript
metrics: [GalileoMetrics.correctness, GalileoMetrics.completeness, GalileoMetrics.inputTone]
```

**Agentic workflows:**
```typescript
metrics: [GalileoMetrics.agentEfficiency, GalileoMetrics.toolSelectionQuality, GalileoMetrics.toolErrorRate]
```
