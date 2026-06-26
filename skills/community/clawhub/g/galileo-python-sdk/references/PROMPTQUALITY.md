# Promptquality 1.x Reference

> **Compatibility:** `promptquality >= 1.0.0` requires `galileo-core < 4.0.0` and is incompatible with `galileo >= 2.0`.
> Use this reference when the project has `promptquality` installed as the primary evaluation SDK alongside `galileo < 2.0`.
> For `galileo >= 2.0`, use `GalileoLogger` — see the main SKILL.md and EVALUATION.md.

## Installation

```bash
pip install "galileo<2.0" "promptquality==1.14.0"
```

## Authentication

```python
import promptquality as pq

pq.login("https://app.galileo.ai")
```

## Running Prompt Experiments

```python
import promptquality as pq

pq.login("https://app.galileo.ai")

template = "Explain {{topic}} to me like I'm a 5 year old"
data = {"topic": ["Quantum Physics", "Politics", "Large Language Models"]}

pq.run(
    project_name="my-first-project",
    template=template,
    dataset=data,
    settings=pq.Settings(
        model_alias="ChatGPT (16K context)",
        temperature=0.8,
        max_tokens=400,
    ),
    scorers=[
        pq.Scorers.context_adherence_plus,
        pq.Scorers.toxicity,
        pq.Scorers.prompt_injection,
    ],
)
```

## EvaluateRun — Custom Workflow Logging

Use `EvaluateRun` to log traces from your own pipeline and score them with Galileo metrics:

```python
from promptquality import EvaluateRun
import promptquality as pq

pq.login()

evaluate_run = EvaluateRun(
    run_name="rag-evaluation",
    project_name="rag-project",
    scorers=[
        pq.Scorers.context_adherence_plus,
        pq.Scorers.completeness_plus,
        pq.Scorers.toxicity,
    ],
)

test_queries = [
    {"input": "What is machine learning?", "context": "ML is a subset of AI..."},
    {"input": "Explain neural networks", "context": "Neural networks are..."},
]

for item in test_queries:
    output = your_rag_pipeline(item["input"], item["context"])
    evaluate_run.add_single_step_workflow(
        input=item["input"],
        output=output,
        model="gpt-4o",
    )

evaluate_run.finish()
```

### EvaluateRun Constructor Fields

| Field | Type | Description |
|---|---|---|
| `run_name` | `str` | Name of the evaluation run |
| `project_name` | `str` | Galileo project to log into |
| `scorers` | `list[Scorers \| CustomScorer]` | Metrics to compute |
| `scorers_config` | `ScorersConfiguration` | Fine-grained scorer toggles (optional) |
| `generated_scorers` | `list[str]` | AI-generated custom scorer names (optional) |
| `run_tags` | `list[RunTag]` | Tags to attach to the run (optional) |

### `add_single_step_workflow` Parameters

| Parameter | Type | Required |
|---|---|---|
| `input` | `str \| Message \| list` | Yes |
| `output` | `str \| Message \| list` | Yes |
| `model` | `str` | Yes |
| `ground_truth` | `str` | No |
| `metadata` | `dict[str, str]` | No |
| `duration_ns` | `int` | No |
| `input_tokens` | `int` | No |
| `output_tokens` | `int` | No |

## Available `pq.Scorers` Constants

**RAG & Context:**
- `pq.Scorers.context_adherence_plus` / `pq.Scorers.context_adherence_luna`
- `pq.Scorers.context_relevance`
- `pq.Scorers.ground_truth_adherence_plus`
- `pq.Scorers.chunk_attribution_utilization_plus` / `pq.Scorers.chunk_attribution_utilization_luna`
- `pq.Scorers.completeness_plus` / `pq.Scorers.completeness_luna`
- `pq.Scorers.instruction_adherence_plus`

**Safety & Content:**
- `pq.Scorers.toxicity` / `pq.Scorers.toxicity_plus`
- `pq.Scorers.input_toxicity` / `pq.Scorers.input_toxicity_plus`
- `pq.Scorers.pii`
- `pq.Scorers.prompt_injection` / `pq.Scorers.prompt_injection_plus`
- `pq.Scorers.sexist` / `pq.Scorers.sexist_plus`
- `pq.Scorers.input_sexist` / `pq.Scorers.input_sexist_plus`
- `pq.Scorers.tone`

**Quality & Accuracy:**
- `pq.Scorers.correctness`
- `pq.Scorers.prompt_perplexity`

**Agentic:**
- `pq.Scorers.action_advancement_plus`
- `pq.Scorers.action_completion_plus`
- `pq.Scorers.tool_selection_quality_plus`
- `pq.Scorers.tool_errors_plus`

## `ScorersConfiguration` — Fine-Grained Toggles

Use `ScorersConfiguration` to enable metrics that are not in `pq.Scorers` (e.g., agentic metrics, NLI variants):

```python
from promptquality import EvaluateRun, ScorersConfiguration
import promptquality as pq

pq.login()

evaluate_run = EvaluateRun(
    run_name="agent-eval",
    project_name="agent-project",
    scorers_config=ScorersConfiguration(
        agentic_workflow_success=True,
        agentic_session_success=True,
        tool_selection_quality=True,
        instruction_adherence=True,
    ),
)
```

### All `ScorersConfiguration` Fields

| Field | Default |
|---|---|
| `agentic_session_success` | `False` |
| `agentic_workflow_success` | `False` |
| `tool_selection_quality` | `False` |
| `tool_error_rate` | `False` |
| `instruction_adherence` | `False` |
| `ground_truth_adherence` | `False` |
| `context_relevance` | `False` |
| `factuality` | `False` |
| `groundedness` | `False` |
| `adherence_nli` | `False` |
| `chunk_attribution_utilization_nli` | `False` |
| `chunk_attribution_utilization_gpt` | `False` |
| `completeness_nli` | `False` |
| `completeness_gpt` | `False` |
| `pii` | `False` |
| `prompt_injection` | `False` |
| `prompt_injection_gpt` | `False` |
| `prompt_perplexity` | `False` |
| `input_sexist` | `False` |
| `input_sexist_gpt` | `False` |
| `sexist` | `False` |
| `sexist_gpt` | `False` |
| `tone` | `False` |
| `input_toxicity` | `False` |
| `input_toxicity_gpt` | `False` |
| `toxicity` | `False` |
| `toxicity_gpt` | `False` |

## `pq.Settings` — Model Configuration

```python
settings = pq.Settings(
    model_alias="ChatGPT (16K context)",
    temperature=0.7,
    max_tokens=500,
)
```
