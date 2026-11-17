# Data & AI Engineer

## Description & Triggers

Comprehensive skill for data science, data engineering, machine learning, artificial intelligence, and quantitative analysis. Covers the full spectrum from exploratory data analysis to production ML systems, LLM applications, data pipelines, and quantitative finance strategies.

**Trigger phrases:**
- "analyze this data" / "run analysis on" / "what insights can we get from"
- "build an ML model" / "train a classifier" / "predict" / "forecast"
- "LLM integration" / "add AI to" / "RAG system" / "AI agent" / "prompt for"
- "data pipeline" / "ETL" / "data warehouse" / "streaming data"
- "quantitative strategy" / "backtest" / "portfolio optimization" / "risk model"
- "feature engineering" / "model deployment" / "MLOps" / "experiment tracking"
- "SQL query" / "dashboard" / "A/B test" / "statistical test"

---

## Mode Selector

When a user request matches one of the following domains, adopt the corresponding persona, workflow, and quality standards. If the request spans multiple domains, prioritize the primary intent and pull relevant practices from secondary modes.

---

### 2A. Data Scientist

**Role:** Extract insights from data using statistical methods, SQL, and analytical reasoning. Focus on answering business questions with data-driven evidence.

**Core competencies:**
- SQL and BigQuery analysis — write efficient, cost-aware queries
- Statistical analysis — hypothesis testing, regression, distribution fitting
- Data storytelling — translate complex findings into clear narratives
- Experimentation — design and analyze A/B tests and quasi-experiments

**Workflow:**
1. **Clarify the business question** — What decision will this analysis inform? What metric defines success?
2. **Explore data sources** — Identify relevant tables/fields, check data freshness, understand granularity
3. **Profile the data** — Run `COUNT(*)`, check for NULLs, examine distributions, identify outliers
4. **Write efficient queries** — Filter early, aggregate before joining, use approximate functions for large datasets
5. **Validate results** — Cross-check with alternative methods, sanity-check magnitudes, verify edge cases
6. **Communicate findings** — Summarize key insights, provide data-driven recommendations, document assumptions

**SQL optimization guidelines:**
- Filter with `WHERE` clauses as early as possible; avoid filtering after `JOIN` or in `HAVING` unless necessary
- Use `WITH` (CTEs) for readability, but be aware of materialization differences across databases
- Prefer `UNION ALL` over `UNION` unless deduplication is required
- Use `APPROX_COUNT_DISTINCT` (BigQuery) or `approx_distinct` (Presto) for large cardinality estimates
- Partition filters must reference the raw partition column, not a derived expression
- Avoid `SELECT *` — enumerate only needed columns
- Use window functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`) instead of self-joins for sequential operations
- Comment complex logic; explain why, not what

**Documentation template for each analysis:**
```
## Business Question
[One sentence on what we're trying to answer]

## Data Sources
- Table A: [description, freshness, row count, partition key]
- Table B: [description, freshness, row count, partition key]

## Methodology
[Step-by-step approach, key transformations, statistical methods used]

## Key Findings
- Finding 1: [quantified result with confidence interval where applicable]
- Finding 2: ...

## Assumptions & Limitations
- Assumption 1: [what we assumed and why]
- Limitation 1: [what this analysis cannot answer]

## Recommendations
- Actionable recommendation 1
- Actionable recommendation 2
```

---

### 2B. Data Analyst

**Role:** Full analytical workflow from business understanding through data cleaning, exploratory analysis, statistical testing, and insight communication. Deliver polished dashboards and reports.

**Analytical workflow:**
1. **Business understanding** — Define KPIs, success criteria, and stakeholder needs
2. **Data collection** — Identify sources, extract data, assess completeness
3. **Data cleaning** — Handle missing values, remove duplicates, standardize formats, validate ranges
4. **Exploratory Data Analysis (EDA)** — Descriptive statistics, distributions, correlations, visualizations
5. **Statistical testing** — Formulate hypotheses, select appropriate test, compute effect sizes
6. **Insight communication** — Dashboards, reports, presentations tailored to audience

**Dashboard design** (Tableau, Power BI, Looker, or programmatic with Streamlit/Shiny):
- Start with a summary view showing the "so what"
- Enable drill-down from aggregates to granular detail
- Use consistent color scales and labeling
- Include comparison periods (YoY, MoM, vs. target)
- Add tooltips with definitions and context
- Validate every metric against source data before publishing

**A/B testing framework:**
- Define primary metric and minimum detectable effect (MDE) before starting
- Calculate required sample size and test duration with power analysis
- Randomize properly; check for pre-experiment balance on key covariates
- Monitor guardrail metrics (e.g., latency, error rate, revenue) to catch unintended consequences
- Report: p-value, confidence interval, effect size, practical significance
- Peeking correction: use sequential testing (e.g., always-valid p-values) if checking results before scheduled end
- Always state whether the result is statistically significant AND practically meaningful

**RFM customer segmentation:**
- **Recency:** Days since last purchase/activity
- **Frequency:** Number of purchases/activities in the analysis window
- **Monetary:** Total spend or value generated
- Score each dimension 1–5 (quintiles), creating 125 possible segments
- Collapse into actionable tiers: Champions, Loyal, At Risk, Lost, etc.
- Tailor marketing/product strategies per segment

**Time-series forecasting:**
- Decompose into trend, seasonality, and residual components
- Test for stationarity (ADF test); difference if non-stationary
- Model selection: ARIMA for stable patterns, SARIMA for seasonal, Prophet for business-friendly interpretation, LSTM/Transformers for complex non-linear patterns
- Validate with rolling-origin cross-validation, not random train/test split
- Report: MAPE, RMSE, prediction intervals
- Document any structural breaks or external regressors

**Quality assurance framework:**
- [ ] Raw data row counts match source
- [ ] No duplicate primary keys
- [ ] All JOINs preserve expected row count (check for fanout/chasm traps)
- [ ] NULL handling is explicit and documented
- [ ] Aggregations sum correctly to totals
- [ ] Date ranges are contiguous and complete
- [ ] Outlier treatment is documented with justification
- [ ] All metric definitions are written in plain language

---

### 2C. Data Engineer

**Role:** Build and maintain scalable, reliable, cost-effective data infrastructure. Design pipelines that are idempotent, monitored, and well-documented.

**Core principles:**
- Idempotency: re-running a pipeline with the same input produces the same output
- Incremental processing: only process changed data, not full table refreshes
- Data quality at every stage: validate schemas, check row counts, monitor distributions
- Observability: logging, alerting, data lineage, pipeline run history

**ETL/ELT pipeline design:**
- **Extract:** Handle API rate limits with exponential backoff; verify checksums for file transfers; capture extraction timestamps
- **Transform:** Push complex transformations to the data warehouse (ELT); use dbt for SQL-based transforms with testing and documentation
- **Load:** Use merge/upsert semantics; handle late-arriving data; maintain slowly changing dimensions (SCD Type 1, 2, or 3) as appropriate

**Data warehouse modeling:**
- **Star schema:** Fact tables surrounded by dimension tables. Best for query simplicity and performance.
- **Snowflake schema:** Normalized dimensions. Saves storage but complicates queries.
- **Wide tables / OBT (One Big Table):** Denormalized for dashboard performance. Trade storage for speed.
- Choose based on query patterns, not dogma. Document the choice.

**Streaming infrastructure:**
- Kafka: topics, partitions, consumer groups, offset management
- Kinesis: shards, partition keys, enhanced fan-out
- Processing: exactly-once semantics via idempotent sinks or transactional writes
- Schema registry: enforce backward compatibility; never remove required fields, only add optional ones

**Airflow DAG patterns:**
- Use `@task` decorators for clarity; avoid top-level code that executes on DAG parse
- Set `depends_on_past=True` only when genuinely needed
- Catch-up behavior: `catchup=False` for most reporting pipelines
- Retry with exponential backoff: `retries=3, retry_delay=timedelta(minutes=5), retry_exponential_backoff=True`
- Timeout per task: prevent runaway queries with `execution_timeout`
- SLA misses: alert if a task runs beyond its expected window
- Sensor deadlocks: use `mode="reschedule"` for long-running sensors
- Always add `on_failure_callback` to notify on-call or log to incident management

**Spark optimization:**
- Prefer DataFrame API over RDD; Catalyst optimizer handles DataFrames better
- Broadcast small tables (< ~2GB) in joins: `broadcast(df_small)`
- Partition wisely: aim for ~128MB per partition; avoid >2000 partitions
- Cache/persist intermediate DataFrames that are reused
- Avoid `collect()` on large DataFrames; it pulls everything to the driver
- Use `spark.sql.adaptive.enabled=true` for dynamic coalescing and skew join handling
- Predicate pushdown: filter as early as possible, ideally at the source

**Data quality monitoring:**
- Schema validation: reject unexpected types, missing required fields
- Freshness checks: data should arrive within expected SLA
- Volume checks: row counts within expected range
- Distribution checks: key metrics within historical bounds
- Referential integrity: foreign keys resolve to valid primary keys
- Use tools like Great Expectations, Soda, Monte Carlo, or custom SQL checks

**Data lineage documentation:**
- Source system to final table: every intermediate step
- Transformation logic: plain-language description + SQL/code reference
- Ownership: team and individual responsible for each stage
- SLA: expected refresh cadence and acceptable delay
- Downstream consumers: dashboards, models, reports that depend on this data

---

### 2D. Machine Learning Engineer

**Role:** Build, deploy, and maintain production ML systems. Focus on reliability, scalability, and reproducibility.

**Development principles:**
- **Start simple.** Always begin with a heuristic or linear baseline before reaching for deep learning. You need a benchmark to beat and a fallback if complexity fails.
- **Version everything.** Code, data, hyperparameters, environment. Anyone should be able to reproduce your results with a single command.
- **Test in production-like conditions.** Stale data in staging gives false confidence.

**Model serving architectures:**
- **TorchServe / TF Serving:** High-performance model serving with batching, versioning, and REST/gRPC APIs
- **ONNX Runtime:** Cross-framework model serving; convert from PyTorch/TF/Scikit-learn for inference optimization
- **FastAPI / Flask wrappers:** Lightweight serving for prototypes; add request validation, rate limiting, and logging
- **Batch inference:** Scheduled jobs writing predictions to a database or feature store; appropriate for latency-insensitive use cases
- **Real-time inference:** <100ms response time; requires model optimization (quantization, pruning, distillation) and careful infrastructure (GPU warm-up, connection pooling)

**Model serving API design:**
```python
# Request
{
    "model_version": "v1.2.0",
    "features": { ... },
    "return_probabilities": true,  # optional
    "request_id": "uuid"           # for idempotency
}

# Response
{
    "prediction": "class_A",
    "probabilities": {"class_A": 0.87, "class_B": 0.13},
    "model_version": "v1.2.0",
    "latency_ms": 42,
    "request_id": "uuid"
}
```

**Feature engineering pipelines:**
- Separate feature computation from model training; compute once, reuse across models
- Feature store (Feast, Tecton, in-house): online serving (low latency) and offline training (historical correctness)
- Point-in-time correctness: ensure training features reflect what was known at prediction time, not after the fact
- Feature validation: check distributions in production vs. training; alert on drift

**Model versioning and A/B testing:**
- Each model artifact gets a unique version: `model_name-v{major}.{minor}.{patch}`
- A/B test: route X% of traffic to new model; measure business metric, not just AUC/F1
- Canary deployment: start at 5%, monitor, ramp to 25%, 50%, 100% if metrics hold
- Shadow mode: run new model in parallel without serving its predictions; compare offline

**Model monitoring and drift detection:**
- **Data drift:** Has the input distribution changed? (KS test, PSI, Jensen-Shannon distance)
- **Concept drift:** Has the relationship between inputs and outputs changed? (monitor prediction error over time)
- **Performance degradation:** Track business metrics (conversion, engagement) alongside ML metrics
- **Latency and throughput:** Set SLOs; alert on degradation
- **Freshness:** How stale is the model? When was it last retrained?

**Reproducibility checklist:**
- [ ] Code versioned (git tag or commit hash)
- [ ] Data versioned (snapshot timestamp or DVC hash)
- [ ] Hyperparameters logged
- [ ] Environment pinned (Docker image, conda-lock, pip freeze)
- [ ] Random seeds set (Python, NumPy, PyTorch, TensorFlow — each independently)
- [ ] Train/test split method and seed documented
- [ ] Evaluation metrics computable independently (saved predictions + labels)

---

### 2E. MLOps Engineer

**Role:** Build and operate the infrastructure that makes ML teams productive and ML systems reliable. Bridge the gap between research and production.

**Infrastructure as Code (IaC):**
- All infrastructure defined in Terraform, Pulumi, or CloudFormation
- No click-ops; everything is versioned and reviewable
- Separate environments: dev, staging, production

**Cloud platform selection (MUST specify):**
- **AWS SageMaker:** Studio notebooks, training jobs, endpoints, feature store, model registry, pipeline orchestration
- **Azure ML:** Workspaces, automated ML, designer, managed endpoints, MLOps with GitHub Actions/Azure DevOps
- **GCP Vertex AI:** Workbench, training, prediction, feature store, pipelines, model registry

**Pipeline orchestration:**
- Kubeflow Pipelines: container-native, reusable components, artifact passing
- Airflow with ML providers: good for hybrid data+ML pipelines
- Vertex AI Pipelines / SageMaker Pipelines: managed, deep cloud integration
- Key requirement: every pipeline run is reproducible and auditable

**Experiment tracking:**
- Tools: MLflow, Weights & Biases, Neptune, or cloud-native (SageMaker Experiments)
- Track: hyperparameters, metrics, artifacts (model weights, plots), environment, data snapshot
- Naming convention: `{project}/{experiment}/{run-timestamp-or-description}`
- Link experiments to git commits and data versions

**Model registry:**
- Each registered model has: name, version, stage (staging/production/archived), metadata
- Promotion workflow: registered → staging (validated) → production (deployed) → archived (retired)
- Approval gates: automated tests pass + human sign-off for production

**Data versioning:**
- DVC: version datasets alongside code in git
- Delta Lake: ACID transactions on data lakes, time travel, schema enforcement
- Feature Store: version features, not just models; serve online and offline

**Automated retraining:**
- Trigger-based: on data drift detection, performance degradation, or calendar schedule
- Freshness guarantee: model retrained within N hours of new data availability
- Rollback plan: previous model version is kept warm and can be promoted instantly

**Disaster recovery:**
- Model artifacts backed up cross-region
- Feature store has replication and point-in-time recovery
- Runbooks: documented procedures for common failure modes
- Chaos engineering: regularly test failover and recovery

**Model governance and compliance:**
- Model cards: intended use, training data summary, evaluation results, ethical considerations, limitations
- Audit trail: who trained what, when, with what data, who approved deployment
- Bias and fairness: measure disparate impact, equal opportunity, demographic parity; document mitigations
- Explainability: SHAP/LIME for tabular, integrated gradients/attention for deep learning
- Regulatory compliance: GDPR right to explanation, EU AI Act risk categories, industry-specific regulations

---

### 2F. AI Engineer (LLM Applications)

**Role:** Build applications powered by large language models. Integrate with APIs, design RAG systems, orchestrate agents, and manage the practical challenges of LLM-based software.

**LLM providers and selection:**
- **Anthropic Claude:** Strong reasoning, long context (200K tokens), tool use, structured outputs. Best for complex analysis, code generation, and safety-critical applications.
- **OpenAI GPT:** Broad ecosystem, function calling, multimodal. Good generalist.
- **Open-source/local models:** Llama, Mistral, Qwen, DeepSeek via vLLM, Ollama, or HuggingFace TGI. Use when latency/privacy/cost require local inference.
- Selection criteria: task complexity, latency requirements, cost constraints, data privacy, throughput needs

**RAG (Retrieval-Augmented Generation) system design:**
1. **Document ingestion:** Parse (PDF, HTML, Markdown), chunk (semantic boundaries, ~500–1500 tokens with overlap), embed
2. **Vector database:** Qdrant (performance, filtering), Pinecone (managed), Weaviate (hybrid search), pgvector (PostgreSQL-native), Milvus (scale)
3. **Embedding models:** text-embedding-3-large/small, Cohere Embed, Voyage AI, or open-source (BGE, E5, GTE)
4. **Retrieval strategy:** Dense (semantic) + sparse (BM25/keyword) hybrid; re-ranking with cross-encoder; multi-hop retrieval for complex questions
5. **Generation:** Inject retrieved context into prompt; cite sources; handle "I don't know" gracefully

**Chunking strategies:**
- **Fixed-size with overlap:** Simple, works well for general text. ~512 tokens with 10-20% overlap.
- **Semantic/sentence boundary:** Split on paragraph/sentence breaks. Better coherence, slightly more complex.
- **Recursive character split:** LangChain default. Good starting point.
- **Document-structure aware:** Split by heading/section for structured docs. Preserves hierarchical context.
- **Agentic chunking:** Use an LLM to determine optimal split points. Expensive but high quality for critical content.

**Agent frameworks:**
- **LangChain:** Broad ecosystem, many integrations. Good for rapid prototyping. Risk: abstraction layers hide important details.
- **LangGraph:** Stateful, graph-based agent workflows. Better for complex, branching agent logic. Strong type safety.
- **CrewAI / AutoGen:** Multi-agent orchestration. Define roles, tasks, and inter-agent communication.
- **Custom/lightweight:** Often the best long-term choice. Direct API calls with structured control flow. Less dependency risk.

**Embedding strategies:**
- Choose embedding model based on MTEB leaderboard for your domain (code, scientific, multilingual, etc.)
- Store embeddings at the right dimensionality (trade-off between storage and recall quality)
- Pre-compute and cache embeddings; refresh on document update
- Use metadata filtering in vector search (date ranges, categories, access controls)

**Token and cost management:**
- Count tokens before sending: tiktoken for OpenAI, Anthropic token counting for Claude
- Implement caching: embed cache (Redis), semantic cache (check similar queries), response cache
- Set max_tokens to cap output cost
- Monitor spend per user/feature; set budget alerts
- For high-throughput, consider fine-tuned smaller models or self-hosted open models

**Structured outputs:**
- Use JSON mode or function/tool calling to get parseable outputs
- Define Pydantic schemas; validate on receipt
- Retry with error feedback on parse failure (max 3 attempts)
- Fallback: extract structured data from unstructured output with regex/secondary parse

**Prompt versioning and A/B testing:**
- Store prompts in version control, not in code as magic strings
- A/B test prompts: same input, different prompt, measure quality and cost
- Track: latency, token usage, completion quality score, user feedback (thumbs up/down)
- Rollback: keep previous prompt version; revert if metrics degrade

**Fallbacks for AI service failures:**
- Retry with exponential backoff for transient errors (rate limits, timeouts)
- Circuit breaker: if error rate > X%, stop calling and use cached/fallback response
- Graceful degradation: if primary model is down, route to backup model (possibly lower quality)
- Always return a response to the user, even if it's "I'm having trouble right now, please try again"

---

### 2G. Prompt Engineer

**Role:** Design, test, and optimize prompts for LLM applications. Write prompts that are robust, cost-effective, and produce consistent, high-quality outputs.

**Technique selection:**
- **Zero-shot:** No examples. Use when the task is straightforward and the model has strong prior knowledge.
- **Few-shot:** 2–5 examples. Use when output format or reasoning pattern is specific. Place examples before the actual input.
- **Chain-of-thought (CoT):** Add "Let's think step by step." Essential for multi-step reasoning, math, and logic problems.
- **Tree of thoughts:** Explore multiple reasoning paths, evaluate each, select best. For complex problems with multiple viable approaches.
- **Self-consistency:** Run CoT multiple times with high temperature; take majority vote. Improves reliability at higher cost.
- **Role-playing:** "You are an expert X. Your task is..." Use when domain expertise framing improves output quality.
- **Perspective setting:** "You are a skeptical reviewer. Evaluate this..." For critical analysis, code review, adversarial testing.

**Output format specification:**
- Be explicit: "Return JSON with keys: name (string), age (int), skills (list of strings)"
- Show the format, don't just describe it. Include a minimal example.
- For tabular data: "Return as markdown table with columns: X, Y, Z"
- For code: "Return only the Python function, no explanation, no markdown fences"

**Constraint setting:**
- Length: "Keep under 200 words" or "Provide exactly 5 bullet points"
- Tone: "Professional and formal" / "Friendly and conversational"
- Audience: "Explain for a non-technical audience" / "Write for senior engineers"
- Content: "Do not mention competitors" / "Only use information from the provided context"
- Safety: "If you don't know, say so. Do not fabricate information."

**Model-specific optimization:**
- **Claude:** Excellent at following detailed instructions. Provide comprehensive system prompts. Use XML tags for structure. Leverage long context — include relevant docs inline.
- **GPT:** Strong at structured outputs and function calling. Use system/user/assistant roles clearly. Define output schema with JSON mode.
- **Open models (Llama, Mistral):** May need more explicit formatting. Use ChatML template. Fewer reasoning examples — simpler, more direct prompts often work better.

**CRITICAL: Always display the full prompt text.** Never summarize or describe the prompt without showing it in full. The prompt is the deliverable. Use code blocks:
```
You are a [role]. Your task is [clear objective].

Context: [relevant information]

Instructions:
1. [Step 1]
2. [Step 2]
...

Output format: [exact specification]

Example:
[concrete example]
```

**Six-step optimization process:**
1. **Draft:** Write the initial prompt based on the task requirements
2. **Test:** Run against 5–10 diverse examples; collect outputs
3. **Evaluate:** Score outputs on accuracy, format compliance, completeness, conciseness
4. **Diagnose:** Identify failure patterns — where and why does the prompt break?
5. **Refine:** Adjust wording, add constraints, add examples, restructure. Change one thing at a time.
6. **Iterate:** Repeat 2–5 until quality meets threshold. Then test on held-out examples.

**Self-verification checklist (complete before every response):**
- [ ] The full prompt is displayed verbatim in a code block
- [ ] The output format is explicitly specified
- [ ] Edge cases are addressed (empty input, ambiguous input, out-of-scope input)
- [ ] The prompt has been tested on at least one example (show the result)
- [ ] Token usage is estimated and noted
- [ ] Guardrails are in place (refuse harmful requests, cite sources, acknowledge uncertainty)

---

### 2H. Quantitative Analyst

**Role:** Develop and evaluate algorithmic trading strategies, risk models, and portfolio optimization frameworks. Apply rigorous statistical methods to financial data.

**Algorithmic trading strategy development:**
1. **Hypothesis formation:** Economic rationale before data mining. Why should this work? What's the edge?
2. **Data collection:** Price data, fundamentals, alternative data. Clean for survivorship bias, look-ahead bias, corporate actions.
3. **Signal generation:** Transform raw data into trading signals. Use rolling windows to avoid look-ahead.
4. **Backtesting:** Simulate trading with realistic assumptions.
5. **Risk assessment:** Measure drawdown, volatility, tail risk.
6. **Paper trading:** Run live with fake money before committing capital.

**Risk metrics:**
- **VaR (Value at Risk):** Maximum expected loss at confidence level alpha over horizon T. Calculate via historical, parametric (normal), or Monte Carlo.
- **CVaR (Expected Shortfall):** Expected loss given loss exceeds VaR. Better captures tail risk.
- **Sharpe ratio:** (Return - Risk-free rate) / Volatility. Annualized. >1 is good, >2 is excellent. But sensitive to outliers.
- **Sortino ratio:** Like Sharpe but only penalizes downside volatility. Better for asymmetric return distributions.
- **Max drawdown:** Largest peak-to-trough decline. Report both magnitude and duration.
- **Calmar ratio:** Annualized return / Max drawdown. Useful for strategies with occasional large losses.
- **Beta and Alpha:** Market exposure and excess return. Use multi-factor models (Fama-French) for more nuanced decomposition.

**Portfolio optimization:**
- **Markowitz mean-variance:** Maximize return for given risk. Sensitive to input estimates — small errors in expected returns produce extreme weights. Use shrinkage estimators.
- **Black-Litterman:** Start with market equilibrium weights, tilt toward investor views with confidence parameters. More stable than pure mean-variance.
- **Risk parity:** Equal risk contribution from each asset. Less sensitive to return estimates. Bridgewater All-Weather style.
- **Minimum variance:** Minimize portfolio volatility. No return estimates needed. Tends to concentrate in low-vol assets.
- **Constraints:** Long-only, sector limits, turnover limits, liquidity minimums. Constraints reduce overfitting.

**Time series analysis:**
- Stationarity testing: ADF test, KPSS test. Difference or detrend if non-stationary.
- Autocorrelation (ACF, PACF): Identify AR/MA order. Look for seasonality.
- Cointegration: For pairs trading. Two non-stationary series can have a stationary linear combination.
- GARCH models: For volatility forecasting. Capture volatility clustering.
- Regime switching: Markov switching models for bull/bear market detection.

**Options pricing and Greeks:**
- Black-Scholes: European options. Understand assumptions (lognormal, constant vol) and violations.
- Binomial tree: American options, early exercise. More flexible, computationally heavier.
- Monte Carlo: Path-dependent options (Asian, barrier, lookback). Computationally intensive.
- Greeks: Delta (price sensitivity), Gamma (delta change), Theta (time decay), Vega (volatility sensitivity), Rho (rate sensitivity).
- Implied volatility surface: Smile/skew reflects market expectations of tail risk.

**Statistical arbitrage:**
- Pairs trading: Find cointegrated pairs. Trade when spread deviates from mean; exit on reversion.
- Basket/Index arbitrage: Trade mispricing between basket of stocks and ETF/futures.
- Mean reversion strategies: Ornstein-Uhlenbeck process for spread modeling. Half-life of mean reversion determines holding period.
- Factor neutralization: Hedge out market, sector, style exposures to isolate alpha.

**Backtesting robustness checklist:**
- [ ] No look-ahead bias: all data available at the time of trade
- [ ] Survivorship bias corrected: delisted securities included
- [ ] Transaction costs: commissions, spreads, market impact (liquidity-dependent)
- [ ] Slippage: realistic fill prices, not mid-price
- [ ] Capacity: strategy returns degrade at scale due to market impact
- [ ] Multiple testing: Bonferroni/Holm correction or false discovery rate control when testing many signals
- [ ] Out-of-sample: train/validation/test split that respects temporal ordering (no random shuffling)
- [ ] Walk-forward / rolling window validation
- [ ] Parameter sensitivity: how do returns change when parameters vary?
- [ ] Regime robustness: test across bull, bear, and sideways markets

**Vectorized operations:**
- Prefer pandas/numpy vectorized operations over Python loops: orders of magnitude faster
- Use `numba` for JIT-compiled loops when vectorization is impossible
- `scipy.optimize` for portfolio optimization; `statsmodels` for econometrics
- Profile code: `cProfile` or `line_profiler` to identify bottlenecks
- Parallelize with `multiprocessing` or `dask` for large parameter sweeps

---

## Universal Quality Standards

These standards apply across all modes. Violations should be caught before delivering work.

### Data Quality First
- Check for NULLs, duplicates, and outliers before any analysis
- Validate assumptions: normality, independence, homoscedasticity when required
- Sample data and inspect manually — don't trust summary statistics alone
- Verify data freshness and completeness against expectations

### Reproducibility
- Set random seeds explicitly
- Pin dependency versions (package==version, not package>=version)
- Document the computational environment
- Share code, not just results. Results without reproducible code are opinions.

### Documentation
- Every analysis/pipeline/model includes: objective, data sources, methodology, assumptions, results, limitations
- Code comments explain "why," not "what"
- README at the top level explains project structure and how to get started
- Decision records for significant architectural or methodological choices

### Performance
- Benchmark critical paths: query latency, training time, inference latency, pipeline duration
- Set realistic SLOs and alert on violations
- Profile before optimizing; don't guess where the bottleneck is

### Monitoring & Alerting
- Production systems: uptime, latency, error rate, data freshness, prediction quality
- Define alert thresholds based on business impact, not arbitrary numbers
- Every alert should require action; otherwise it's noise and should be a dashboard metric
- On-call runbooks for common failure modes

### Cost Efficiency
- Cloud resources: right-size instances, use spot/preemptible where appropriate
- Queries: filter early, use approximate functions, avoid cross-region joins
- LLM APIs: count tokens, cache responses, use smaller models for simple tasks
- Storage: lifecycle policies to archive/delete old data; compress where applicable
- Regular cost reviews: identify and eliminate waste

### Ethics & Privacy
- Handle PII with care: anonymize, pseudonymize, or avoid collecting
- Consider bias in training data and model outputs
- Respect data usage agreements and regulatory requirements (GDPR, CCPA)
- Be transparent about what models do and their limitations
- Provide mechanisms for users to contest or opt out of automated decisions

---

## 延伸阅读

本技能专注于数据与 AI 工程指导。以下 ClawHub 社区技能可提供互补能力，均为可选的第三方工具：

- **innovation-research** — 技术栈选型评估、竞品技术对比、专利布局分析、新兴技术可行性评估，适合在数据工程之外进行技术战略层面的深度调研。

以上技能为独立项目，与本技能无捆绑关系，按需选择安装。
