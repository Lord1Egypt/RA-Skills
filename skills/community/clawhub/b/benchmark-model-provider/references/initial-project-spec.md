# Initial Project Specification  
## benchmark-model-provider

---

## 1. Introduction / Why This Skill Exists

People constantly ask practical questions such as:

- *Is this model actually good enough?*
- *Which model is smarter?*
- *Which model is more cost-efficient?*
- *Which model is worth using every day?*
- *Should I run a local model or use an external service?*
- *Which option is the most optimal for my own situation?*

> There is no universally best model for everyone.

Different users have different:

- goals
- budgets
- working domains
- technical constraints
- levels of technical understanding

The same model may feel excellent for one person and disappointing for another, not because one person is right and the other is wrong, but because their real usage context is different.

This skill exists to give users a repeatable way to evaluate models based on their own needs rather than relying on generic recommendations or broad public opinion.

### Core idea

1. Build a small set of highly specific benchmark questions that reflect the user’s real work.
2. Run multiple models independently on the same benchmark.
3. Measure the outputs using a consistent scoring framework.
4. Rank the results in a way that helps the user choose the most suitable model for their own workflow.

---

## 2. Project Goal and Scope

### 2.1 Goal

The goal of this project is to build a reusable skill that can:

- benchmark multiple providers and models against the same benchmark set
- score them across meaningful evaluation axes
- generate reports
- help the user decide which model is most suitable for their own use case

### 2.2 Benchmark source of truth

The benchmark set must **not** be generic by default.

It should be derived from the user’s actual context, especially:

- the user’s purpose for using the bot
- the domain or field they work in
- the frequency and intensity of usage

### 2.3 Initial scope

The initial scope is focused on:

- text-based LLM benchmarking
- local and service-based model comparison
- report generation
- reruns and re-ranking

### 2.4 Out of primary scope for v1

The following are **not** the primary focus of the initial version:

- complex multimodal benchmarking
- heavy tool-use benchmarking
- video/audio-first benchmark systems

---

## 3. Core Benchmark Philosophy

This project is built around a **fit-to-user** philosophy rather than a vanity leaderboard philosophy.

### Core principles

- the benchmark must be built around the user’s real needs
- compared models must be evaluated on the same benchmark set
- models must run independently
- results must remain auditable and reusable
- the default benchmark mode should maximize fairness and reproducibility
- benchmark outputs must support later re-scoring and report rebuilding

### Guiding question

> “Which model is best for me?”  
> not  
> “Which model is best in the abstract?”

---

## 4. Benchmark Construction Logic

Before running any benchmark, the skill should first collect **benchmark context** from the user.

### 4.1 Required context inputs

At minimum:

- the main purpose for using the bot
- the domain or field of work
- the usage frequency and expected workload

### 4.2 Benchmark size

From that context, the system should generate a compact but representative benchmark set, typically:

- **5 to 10 highly specific questions**

### 4.3 Benchmark composition

A well-constructed benchmark set may include:

- **core recurring tasks**
- **high-value tasks**
- **deep-analysis / reasoning-heavy tasks**
- **lighter tasks** where responsiveness still matters operationally

### 4.4 Design rule

Each question should be specific enough to reveal meaningful differences between models, while the total benchmark should remain small enough to rerun when needed.

---

## 5. Benchmark Input Modes

The skill must support **two explicit benchmark input modes**.

### 5.1 `prompt_only` (default)

This is the default and fairness-first mode.

#### Rules
- send only the raw benchmark prompt
- do not inject additional context
- do not inject custom benchmark system prompts
- do not inject memory
- do not inject few-shot examples
- do not inject hidden scaffolding

#### Purpose
Measure the raw performance of models under the same direct input.

---

### 5.2 `agent_context`

This mode is intended for cases where the user wants a benchmark that reflects a more realistic agent environment.

#### Rules
- the model receives the benchmark prompt plus a fixed shared system/context layer
- the context must be consistent across all compared models in the same run
- the context must be documented in the benchmark metadata/spec
- the run must remain reproducible

#### Purpose
Measure performance in a more realistic agent-like setup while keeping the benchmark controlled.

---

## 6. Scoring System

### 6.1 Measured Axes

The system measures **four distinct axes**:

- **quality**
- **depth**
- **cost**
- **speed**

---

### 6.2 Default Overall Formula

The default overall ranking should be calculated from:

- **quality: 45%**
- **depth: 35%**
- **cost: 20%**

```text
overall_default =
  0.45 * quality_score +
  0.35 * depth_score +
  0.20 * cost_score
```

---

### 6.3 Why Speed Is Measured but Excluded from Default Overall

Speed must still be recorded and reported, but it should **not** be included in the default overall formula.

#### Reason
Latency is often strongly affected by:

- reasoning depth
- thinking mode
- answer length
- model behavior

A slower model is not necessarily worse if the extra time produces better reasoning or deeper analysis.

#### Rule
- speed is a required operational metric
- speed is shown in reports
- speed is excluded from the default overall score
- speed may be optionally included in custom scoring profiles

---

### 6.4 Per-Question Evaluation

Quality and depth should both be scored **per question**.

#### Recommended default
- each question receives a **0–10 quality score**
- each question receives a **0–10 depth score**

These raw scores are then aggregated and normalized for comparison across models.

---

### 6.5 Quality Criteria

Quality scoring should consider factors such as:

- instruction fit
- correctness or plausibility
- clarity and structure
- practical usefulness
- immediate usability

---

### 6.6 Depth Criteria

Depth scoring should consider factors such as:

- number of analytical layers
- breadth of context integration
- comparison or counterpoint capability
- ability to go beyond surface-level response
- richness of reasoning structure

---

### 6.7 Cost Scoring

Cost should be derived from token usage and available pricing sources.

Because cheaper models are more cost-efficient, cost must not be used as a raw score directly.

#### Rule
- cost should be normalized inversely
- lower cost → higher cost score

---

### 6.8 Custom Scoring Profiles

The system should support custom scoring profiles and weight overrides.

Examples:

- **research-heavy profile** → prioritize quality and depth
- **daily lightweight profile** → prioritize cost and optionally speed
- **operations profile** → prioritize quality and responsiveness

---

## 7. Metrics and Measurement Rules

The system should capture and preserve raw benchmark metrics whenever possible.

### 7.1 Important metrics

- input tokens
- output tokens
- total tokens
- execution time
- estimated or actual cost
- evidence/citation quality when relevant
- per-question timing when available
- total benchmark runtime

---

### 7.2 Data separation

The system must clearly separate:

#### Raw Data
- prompt
- system/context if applicable
- raw answer
- token counts
- latency
- raw cost figures

#### Derived Data
- normalized scores
- cost score
- overall score
- rankings
- summaries and reports

---

### 7.3 Estimation rule

If token or pricing values are estimated rather than returned directly by the provider, that estimated status must be clearly marked.

---

## 8. Execution Strategies

The skill must support **two execution strategies**.

### 8.1 Sequential

In sequential mode, models are benchmarked one after another.

#### Useful when
- the batch is small
- debugging is needed
- the user prefers simplicity
- orchestration overhead is unnecessary

---

### 8.2 Subagent-Orchestrated

In orchestrated mode, one orchestrator agent manages the benchmark run and multiple subagents handle model-specific execution.

#### Orchestrator responsibilities
- read the benchmark spec
- dispatch benchmark jobs
- ensure execution consistency
- track progress
- collect results from subagents
- validate completeness and format
- aggregate outputs into a single benchmark result set

#### Subagent responsibilities
- receive one model plus the benchmark spec
- run the benchmark for that model
- store raw answers
- store raw metrics
- return the result to the orchestrator

#### Benefit
This architecture improves scalability and is better suited for larger model batches.

---

## 9. Operational Modes

The skill should support **four high-level operational modes**:

### `prepare`
- collect benchmark context
- generate or refine the benchmark spec
- do not run the benchmark yet

### `run`
- execute the benchmark
- compute metrics
- score results
- generate local outputs
- do not publish automatically

### `publish`
- prepare delivery outputs
- ask the user which output form they want
- publish or export accordingly

### `rerank`
- do not rerun models
- reuse raw benchmark outputs and metrics
- apply a new scoring formula or weight profile
- rebuild ranking and reports

> `rerank` is a required capability, not an optional add-on.

---

## 10. End-to-End Workflow

A standard benchmark flow should follow these steps:

1. **Collect benchmark context**
2. **Build or select a benchmark spec**
3. **Verify the model list**
4. **Run the benchmark**
5. **Compute metrics**
6. **Score the models**
7. **Build outputs**
8. **Ask the user how they want the final result delivered**
9. **Publish or export if requested**

### Workflow qualities
The flow must remain:

- understandable
- reproducible
- user-visible

---

## 11. Data and File Structure

The skill should preserve a structured file layout that separates:

- source definitions
- raw outputs
- metrics
- score breakdown
- final reports

### 11.1 Expected data categories

- benchmark specs
- raw per-model answer files
- raw metrics
- score breakdown
- markdown summaries
- HTML report output

### 11.2 Required metadata per benchmark run

- benchmark name
- benchmark version
- timestamp
- benchmark mode
- optional context profile

### 11.3 Purpose
This structure enables:

- reruns
- audits
- re-ranking
- report regeneration

without losing source state.

---

## 12. Script Responsibilities

The initial skill design should include the following scripts.

### 12.1 `build_benchmark_spec.py`
- build a benchmark spec from benchmark context
- save a versioned benchmark spec

### 12.2 `run_benchmark.py`
- load a benchmark spec
- execute model runs
- support sequential and orchestrated execution
- save raw answers and run metadata

### 12.3 `estimate_tokens.py`
- estimate token usage when provider usage is unavailable

### 12.4 `resolve_pricing.py`
- map models to pricing data
- store source and confidence
- distinguish estimated values from official pricing
- handle local-model infrastructure estimates

### 12.5 `score_models.py`
- combine raw metrics and manual/semi-manual quality and depth scores
- normalize values
- compute cost score
- compute overall score
- support reranking

### 12.6 `build_report.py`
- generate markdown summaries
- generate HTML report output
- prepare report artifacts for delivery

### 12.7 `publish_report.py`
- publish to Vercel when requested
- export or package PDF output when requested
- return delivery results such as URLs or output file references

---

## 13. Reporting and Delivery Options

The skill should support multiple output forms rather than assuming one default delivery channel.

### 13.1 Supported outputs
- markdown summary
- HTML landing page
- Vercel web deployment
- PDF export

### 13.2 Delivery question
At the delivery stage, the user should be explicitly asked which output they want:

- **web page on Vercel**
- **PDF**
- **both**

### 13.3 Rule
The skill should **not auto-deploy to Vercel** without asking first at the final delivery step.

---

## 14. Progress Feedback Rules

A benchmark run can take long enough that the user may feel the process is stuck if no status updates are shown.

To avoid this, the skill must provide progress feedback at each major workflow step.

### 14.1 Required behavior
- announce the current major step
- announce when a major step is completed
- announce which next step is starting

### 14.2 Long-run behavior
For long-running operations, especially orchestrated multi-model runs, the skill should also provide intermediate progress updates such as:

- number of completed model runs
- number of remaining model runs
- current aggregation/scoring stage

### 14.3 Goal
Make the process feel transparent rather than frozen.

---

## 15. Initial References and Examples Package

The initial version of the skill should include a reference and example package strong enough to guide future implementation.

### 15.1 Required reference files
- `benchmark-schema.md`
- `scoring-rubric.md`
- `pricing-sources.md`
- `execution-modes.md`
- `output-modes.md`

### 15.2 Required example files
- `vietnam-market-5q.yaml`
- `benchmark-context-template.yaml`
- `benchmark-context-template-en.yaml`
- `benchmark-context-template-zh.yaml`
- `sample-benchmark-en.yaml`
- `sample-benchmark-zh.yaml`
- `sample-benchmark-coding.yaml`
- `sample-benchmark-research.yaml`

### 15.3 Language coverage
Examples should support multilingual usage, especially:

- **Vietnamese**
- **English**
- **Chinese**

### 15.4 Domain coverage
The example set should also demonstrate that the skill is **not limited to finance**.

---

## 16. Non-Goals and Boundaries

The initial version of this project is **not** intended to be:

- a universal “best model” oracle
- a benchmark that assumes one model fits everyone
- an implementation-detail dump
- a multimodal/video benchmark system in v1
- a heavy tool-use benchmark framework in its initial form

### Boundary statement
The project is meant to provide a disciplined, reusable benchmarking workflow centered on:

- user fit
- transparent scoring
- reproducible evaluation

---

## 17. Next Implementation Steps

After this initial spec is approved, the project should proceed in the following order:

1. write and save `references/initial-project-spec.md`
2. update `SKILL.md` to align with the approved design
3. expand the `references/` package
4. expand the `examples/` package
5. upgrade the existing script skeletons into working implementations
6. prepare the skill for eventual publishing to ClawdHub
