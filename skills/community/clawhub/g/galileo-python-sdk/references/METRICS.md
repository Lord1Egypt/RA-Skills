# Guardrail Metrics Reference

Galileo provides proprietary metrics that can be used for evaluation scoring, production observability alerts, and runtime guardrails. These metrics are computed server-side by the Galileo platform.

## RAG and Context Metrics

| Metric | Description | Use Case |
|---|---|---|
| **Context Adherence** | Measures whether model responses are grounded in the provided context. Detects hallucinations in RAG pipelines. | RAG applications, context-based Q&A |
| **Chunk Attribution** | Binary metric indicating whether each retrieved chunk contributed to the model's response (Attributed / Not Attributed). | RAG retrieval quality assessment |
| **Chunk Utilization** | Measures how much of each retrieved chunk was actually used when generating the output. | Optimizing retrieval chunk size |
| **Completeness** | Evaluates whether the response fully addresses all aspects of the input query. | Q&A systems, customer support |
| **Instruction Adherence** | Measures model response alignment with system instructions and context. | Instruction-following evaluation |

## Hallucination Detection

| Metric | Description | Use Case |
|---|---|---|
| **Uncertainty** | Measures model certainty at both response and token level. Strongly correlates with hallucinations and fabricated facts. | General hallucination detection |
| **Correctness** | Evaluates whether response facts are based on real, verifiable information. Combined with Uncertainty for comprehensive hallucination coverage. | Factual accuracy checks |

## Safety and Content Metrics

| Metric | Description | Use Case |
|---|---|---|
| **Toxicity** | Detects abusive, toxic, or foul language in model inputs and outputs. | Content moderation, safety filtering |
| **PII Detection** | Surfaces instances of personally identifiable information: credit card numbers, SSNs, phone numbers, street addresses, email addresses. | Privacy compliance, data protection |
| **Prompt Injection** | Identifies adversarial prompt injection attempts in user inputs. | Security, attack prevention |
| **Sexism** | Detects sexist or gender-biased content. | Bias detection, content safety |
| **Tone** | Classifies responses into 9 emotion categories. | Customer experience, brand voice |
| **NSFW** | Detects not-safe-for-work content. | Content moderation |

## Using Metrics in Code

### In Evaluation Runs (galileo 2.x)

```python
from galileo import GalileoLogger

logger = GalileoLogger(project="safety-eval", log_stream="eval-run")

logger.add_single_llm_span_trace(
    input="Is this content safe?",
    output="Yes, the content is safe.",
    model="gpt-4o",
)

logger.flush()
```

### In Guardrail Rules

```python
from galileo import GalileoMetrics
from galileo_core.schemas.protect.rule import Rule, RuleOperator

toxicity_rule = Rule(
    metric=GalileoMetrics.input_toxicity,
    operator=RuleOperator.gt,
    target_value=0.5,
)

pii_rule = Rule(
    metric=GalileoMetrics.input_pii,
    operator=RuleOperator.gt,
    target_value=0.0,
)

injection_rule = Rule(
    metric=GalileoMetrics.prompt_injection,
    operator=RuleOperator.gt,
    target_value=0.7,
)
```

### Available `GalileoMetrics` Constants

**RAG & Context:**
- `GalileoMetrics.context_adherence`
- `GalileoMetrics.chunk_attribution_utilization`
- `GalileoMetrics.completeness`
- `GalileoMetrics.context_relevance`
- `GalileoMetrics.ground_truth_adherence`
- `GalileoMetrics.instruction_adherence`

**Safety & Content:**
- `GalileoMetrics.input_toxicity` / `GalileoMetrics.output_toxicity`
- `GalileoMetrics.input_pii` / `GalileoMetrics.output_pii`
- `GalileoMetrics.prompt_injection`
- `GalileoMetrics.input_sexism` / `GalileoMetrics.output_sexism`
- `GalileoMetrics.input_tone` / `GalileoMetrics.output_tone`
- `GalileoMetrics.sql_injection`

**Quality & Accuracy:**
- `GalileoMetrics.correctness`

**Agentic:**
- `GalileoMetrics.agent_efficiency`
- `GalileoMetrics.agent_flow`
- `GalileoMetrics.tool_selection_quality`
- `GalileoMetrics.tool_error_rate`

Many metrics also have `_luna` variants (e.g., `context_adherence_luna`) that use Galileo's small language model for faster, lower-cost scoring.

### Available `pq.Scorers` Constants

- `pq.Scorers.context_adherence_plus`
- `pq.Scorers.prompt_injection`
- `pq.Scorers.toxicity`
- `pq.Scorers.pii`
- `pq.Scorers.sexist`
- `pq.Scorers.tone`
- `pq.Scorers.chunk_attribution_utilization_plus`
- `pq.Scorers.completeness_plus`
- `pq.Scorers.correctness`
