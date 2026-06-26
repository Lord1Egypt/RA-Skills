# Autoimprove Examples

Complete `improve.md` templates for different domains. Use `/autoimprove init --type <type>` to scaffold these.

## Types

| Type | What it optimizes | Typical metric | Typical budget |
|------|-------------------|----------------|----------------|
| `perf` | Code performance | Requests/sec, time, allocations | 4-8h |
| `ml` | ML training | Validation loss, accuracy, BPB | 8-24h |
| `docker` | Container image | Image size in bytes | 1-2h |
| `k8s` | Cluster health | Running pod count, error rate | 1-2h |
| `prompt` | LLM prompt quality | F1, accuracy, similarity score | 1-2h |
| `sql` | Query performance | Execution time in ms | 1-2h |
| `frontend` | Bundle size | Bundle bytes | 2-4h |
| `ci` | CI/build speed | Build time in seconds | 2-4h |
| `automl` | Tabular ML (churn, fraud, scoring) | AUC-ROC, F1, accuracy | 4-8h |
| `rag` | RAG pipeline (retrieval + generation) | Answer relevancy, faithfulness, RAGAS | 4-8h |

## perf — Code Performance

```markdown
# autoimprove: faster-<component>

## Change
files: <hot-path source files>
context: <test files, benchmarks>

## Check
run: <test suite> && <benchmark command>
score: <benchmark metric extraction>
goal: lower
timeout: 5m

## Stop
budget: 4h
stale: 15

## Instructions

Focus on reducing allocations and avoiding unnecessary work in hot paths.

Patterns to try:
- Fast-path with fallback — handle common cases with optimized code, fall back to general path for edge cases
- Reduce object allocations — reuse buffers, avoid temporary arrays/maps
- Byte-level operations instead of string operations in parsing
- Cache repeated computations (small integer to_s, frozen strings)
- Splat-free method dispatch for frequently called methods
- instance_of? over is_a? in hot loops (skip inheritance chain)

What NOT to try:
- Don't change the public API
- Don't add external dependencies
- Don't sacrifice readability for marginal gains (<0.1%)
- Complexity must pay for itself
```

## ml — ML Training

```markdown
# autoimprove: better-<model>

## Change
files: train.py
context: prepare.py, data/

## Check
run: python train.py
score: SCORE: {value}
goal: lower
timeout: 5m

## Stop
budget: 8h
stale: 20

## Instructions

Improve validation loss within the fixed training time budget.

Patterns to try:
- Architecture (attention patterns, activation functions, normalization layers)
- Optimizer (learning rate schedules, weight decay, momentum)
- Embeddings (positional encoding variants, value embeddings)
- Training dynamics (warmup, gradient clipping, batch size)
- Regularization (dropout, label smoothing, data augmentation)

What NOT to try:
- Don't modify the data pipeline or evaluation
- Don't add dependencies
- Simplicity over marginal gains
- Deleting code for equal results IS an improvement
```

## docker — Container Image Size

```markdown
# autoimprove: slim-<image>

## Change
files: Dockerfile
context: <build context files>

## Check
run: docker build -t test . && echo SCORE: $(docker image inspect test --format '{{.Size}}')
goal: lower
timeout: 5m

## Stop
rounds: 30

## Instructions

Reduce image size without breaking runtime behavior.

Patterns to try:
- Multi-stage builds (build stage + minimal runtime stage)
- Alpine or distroless base images
- Combine RUN layers to reduce intermediate layer count
- Remove build tools, caches, and dev deps from final stage
- Use scratch for static binaries
- .dockerignore to exclude unnecessary build context

What NOT to try:
- Don't remove runtime dependencies
- Don't use UPX (breaks debugging and coredumps)
- The app must still start and pass health checks
```

## k8s — Kubernetes Health

```markdown
# autoimprove: fix-<issue>

## Change
files: <deployment/service YAML files>
context: k8s/

## Check
run: kubectl apply -f k8s/ && sleep 60 && <health check command>
score: SCORE: {value}
goal: higher
timeout: 3m

## Stop
target: <desired healthy count>
rounds: 20

## Instructions

Get pods to healthy Running state.

Patterns to try:
- Resource requests and limits (memory/CPU)
- Liveness and readiness probe tuning
- Pod anti-affinity rules
- Environment variable and config fixes
- HPA min/max replicas and target utilization
- Init container dependencies

What NOT to try:
- Don't change container images
- Don't delete and recreate namespaces
- Don't modify service mesh config
- One manifest change per experiment
```

## prompt — Prompt Engineering

```markdown
# autoimprove: better-<task>-prompt

## Change
files: prompts/<task>.txt
context: eval/golden_set.jsonl

## Check
run: python eval/run_eval.py --prompt prompts/<task>.txt
score: <metric>: ([\d.]+)
goal: higher
timeout: 2m

## Stop
budget: 1h
target: 0.95

## Instructions

Improve prompt accuracy on the evaluation set.

Patterns to try:
- Few-shot examples (pick diverse, representative cases)
- Chain-of-thought before final answer
- Structured output format (JSON with typed fields)
- Negative examples (what NOT to do)
- Simplify — shorter prompts often outperform verbose ones
- Role/persona framing

What NOT to try:
- Don't modify the evaluation script
- Don't overfit to specific test cases
- Keep prompt under 2000 tokens
- Don't use model-specific tricks that break portability
```

## sql — Query Performance

```markdown
# autoimprove: faster-<query>

## Change
files: queries/<name>.sql
context: schema.sql, indexes.sql

## Check
run: psql -f queries/<name>.sql -c '\timing' 2>&1
score: Time: ([\d.]+) ms
goal: lower
timeout: 1m

## Stop
stale: 10

## Instructions

Reduce query time without changing result set.

Patterns to try:
- Replace correlated subqueries with JOINs
- Use EXISTS instead of IN for existence checks
- Add covering index hints via query restructuring
- Partition large scans with range predicates
- Materialize expensive CTEs if they're scanned multiple times

What NOT to try:
- Don't modify schema or indexes
- Results must be identical (same rows, same order)
- Don't use database-specific extensions not in the schema
```

## frontend — Bundle Size

```markdown
# autoimprove: smaller-<app>

## Change
files: src/index.ts, package.json, <build config>
context: src/

## Check
run: npm run build && echo SCORE: $(stat -f%z dist/index.js)
goal: lower
timeout: 2m

## Stop
budget: 2h

## Instructions

Reduce production bundle size.

Patterns to try:
- Dynamic imports for routes and heavy components
- Replace heavy libraries with lighter alternatives (moment→dayjs, lodash→lodash-es)
- Tree shaking configuration
- Remove unused exports
- Code splitting by route or feature
- Externalize large dependencies

What NOT to try:
- Don't remove features
- Don't break lazy loading
- Don't switch build tools
- App must still work in the browser
```

## ci — Build Speed

```markdown
# autoimprove: faster-<pipeline>

## Change
files: .github/workflows/ci.yml, <build config files>
context: src/, package.json

## Check
run: time <build command> 2>&1 | tail -1
score: real\s+(\d+\.\d+)
goal: lower
timeout: 10m

## Stop
stale: 15

## Instructions

Reduce build/CI time without skipping quality checks.

Patterns to try:
- Parallel jobs in CI workflow
- Caching (node_modules, build artifacts, docker layers)
- Incremental compilation
- Split test suites into parallel shards
- Conditional steps (skip unchanged paths)

What NOT to try:
- Don't skip tests or linting
- Don't remove type checking
- Don't change output artifacts
- Pipeline must remain correct
```

## automl — Tabular ML (Churn, Fraud, Scoring)

The most common ML task across companies. Unlike traditional AutoML (AutoSklearn, FLAML, AutoGluon) which searches a predefined parameter grid, autoimprove can engineer new features, rewrite preprocessing pipelines, swap models, and combine approaches creatively.

Applies to: churn prediction, fraud detection, credit scoring, lead conversion, demand forecasting, insurance pricing, recommendation ranking, customer lifetime value.

```markdown
# autoimprove: better-<prediction>-model

## Change
files: train.py
context: data/train.csv, data/test.csv, evaluate.py

## Check
run: python train.py && python evaluate.py
score: auc_roc: ([\d.]+)
goal: higher
timeout: 3m

## Stop
budget: 4h
target: 0.95
stale: 20

## Instructions

Improve AUC-ROC on the holdout test set.
The training data has structured columns: demographics, usage metrics,
billing history, support tickets, engagement signals.

Feature engineering to try:
- Ratio features (e.g., support_tickets / months_active)
- Rolling aggregates (7d, 30d, 90d windows over usage metrics)
- Interaction terms between high-importance features
- Binning continuous variables (tenure buckets, spend tiers)
- Target encoding for high-cardinality categoricals
- Recency features (days since last login, last purchase)
- Trend features (is usage increasing or decreasing?)

Model changes to try:
- XGBoost, LightGBM, CatBoost — compare all three
- Hyperparameters: learning_rate, max_depth, n_estimators, subsample, colsample_bytree
- Class imbalance: scale_pos_weight, SMOTE, undersampling
- Ensemble: stack top 2-3 models with logistic regression meta-learner
- Calibration: isotonic or Platt scaling

Preprocessing to try:
- Missing values: median, mode, or indicator columns
- Log-transform skewed features
- Remove highly correlated features (>0.95)
- Feature selection: drop low-importance features to reduce noise

What NOT to try:
- Don't modify evaluate.py or the test data
- Don't use the test set during training (no leakage)
- Don't add deep learning for tabular data — tree models win here
- Don't add more than 2 new dependencies
- Keep the pipeline reproducible (set random seeds)
```

## rag — RAG Pipeline Optimization

RAG pipelines have many interacting knobs — chunking, embedding, retrieval, reranking,
prompt template, context window management. Small changes compound: better chunking
improves retrieval which improves generation quality. Autoimprove can explore this
combinatorial space much faster than manual tuning.

Applies to: internal knowledge bases, customer support bots, documentation search,
legal document retrieval, code search, research assistants, enterprise Q&A.

```markdown
# autoimprove: better-rag-answers

## Change
scope: the RAG pipeline — chunking, retrieval, and generation
exclude: data/, eval/

## Check
test: python -m pytest tests/test_pipeline.py -x
test-files: tests/
run: python eval/run_eval.py
score: answer_relevancy: ([\d.]+)
goal: higher
timeout: 5m

## Stop
budget: 6h
target: 0.92
stale: 15

## Instructions

Improve answer relevancy on the evaluation set of 50 question-answer pairs.

Chunking strategies to try:
- Vary chunk size (256, 512, 1024, 2048 tokens) and overlap (50, 100, 200)
- Semantic chunking — split on topic boundaries instead of fixed token counts
- Hierarchical chunking — parent chunks for context, child chunks for retrieval
- Document-aware splitting — respect headers, paragraphs, code blocks, tables
- Sentence-level chunking with sliding window for dense passages

Retrieval strategies to try:
- Adjust top-k (3, 5, 10, 15)
- Hybrid search — combine dense (embedding) and sparse (BM25) retrieval
- Add a cross-encoder reranker after initial retrieval
- Query expansion — rephrase the query multiple ways, merge results
- Query decomposition — split complex questions into sub-questions
- MMR (Maximal Marginal Relevance) — diversify retrieved chunks

Embedding changes to try:
- Switch embedding model (nomic-embed, bge-large, e5-mistral, cohere-embed-v3)
- Instruction-prefixed embeddings
- Normalize embeddings for cosine similarity

Generation prompt to try:
- Structured context presentation (numbered sources with metadata)
- Chain-of-thought before answering
- Citation-required format ("Answer based on sources. Cite [Source N].")
- "If context doesn't contain the answer, say so" (reduce hallucination)
- Concise vs. detailed instruction tuning

Context window management to try:
- Reorder chunks — most relevant first vs. most relevant in the middle
- Compress context — summarize long chunks before passing to LLM
- Dynamic context sizing — more chunks for complex questions
- Deduplication — remove near-duplicate chunks

What NOT to try:
- Don't modify the evaluation script or golden answers
- Don't change the LLM used for generation (separate variable)
- Don't add more than 3 new dependencies
- Don't switch to a different document corpus
- Keep inference cost per query reasonable
```

Swap the metric based on what matters most: `faithfulness` to reduce hallucination,
`context_precision` to improve retrieval accuracy, or a composite RAGAS score for
overall pipeline quality.
