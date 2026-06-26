# Advanced Evaluation Patterns (TypeScript)

## Batch Evaluation Across Test Cases

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "batch-eval",
  dataset: [
    { input: "What is ML?", context: "Machine learning is a subset of AI..." },
    { input: "Explain RAG", context: "Retrieval-augmented generation combines..." },
    { input: "What is fine-tuning?", context: "Fine-tuning adapts a pre-trained model..." },
  ],
  metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.chunkAttributionUtilization, GalileoMetrics.completeness],
  projectName: "eval-project",
  function: async (input) => {
    return await callYourLLM(input.input, input.context);
  },
});
```

## Evaluating Multi-Step Agents

Use `GalileoLogger` within a `runExperiment` function for fine-grained span logging during evaluation:

```typescript
import { runExperiment, GalileoLogger, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "agent-eval",
  datasetName: "agent-test-cases",
  metrics: [GalileoMetrics.contextAdherence, GalileoMetrics.completeness, GalileoMetrics.inputToxicity],
  projectName: "eval-project",
  function: async (input) => {
    const docs = await searchTool(input.query);
    const response = await generateWithContext(input.query, docs);
    return response;
  },
});
```

## Comparing Models

Run the same test set across different models and compare results in the Galileo console:

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"];

for (const model of models) {
  await runExperiment({
    name: `eval-${model}`,
    datasetName: "benchmark-dataset",
    metrics: [GalileoMetrics.correctness, GalileoMetrics.completeness, GalileoMetrics.groundTruthAdherence],
    projectName: "model-comparison",
    function: async (input) => {
      return await callLLM(input.question, model);
    },
  });
}
```

## Experiment with Prompt Templates

Evaluate prompt templates directly without writing a custom function:

```typescript
import { runExperiment, GalileoMetrics } from "galileo";

const result = await runExperiment({
  name: "prompt-template-eval",
  datasetName: "my-test-dataset",
  promptTemplate: { id: "your-prompt-template-id" },
  promptSettings: { model_alias: "GPT-4o", temperature: 0.7, max_tokens: 500 },
  metrics: [GalileoMetrics.correctness, GalileoMetrics.instructionAdherence, GalileoMetrics.completeness],
  projectName: "prompt-optimization",
});
```

## Best Practices

1. **Use descriptive experiment names** that include the purpose and date.
2. **Include context fields** in your dataset when evaluating RAG pipelines so context-dependent metrics are computed.
3. **Run evaluations in CI/CD** to catch quality regressions before deployment.
4. **Compare results in the Galileo console** to visualize metric trends across experiments.
5. **Use `_luna` metric variants** for faster iteration during development, then switch to full metrics for final evaluation.
