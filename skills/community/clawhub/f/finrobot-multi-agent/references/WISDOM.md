# Cross-Project Wisdom

Total: **8**

## `CW-MACRO-DATA-001` — Temporal Ordering Enforcement
**From**: finance-bp-080--FinDKG, finance-bp-083--Economic-Dashboard · **Applicable to**: macro-data

Across temporal knowledge graphs and financial time series, strict temporal ordering must be enforced in train/val/test splits and data loading. Train edges must occur strictly before validation edges, which must occur strictly before test edges. DataLoaders must never shuffle temporal data. Apply this pattern whenever implementing any time-series ML pipeline to prevent look-ahead bias that inflates evaluation metrics.

## `CW-MACRO-DATA-002` — Regulatory Formula Compliance
**From**: finance-bp-077--Open_Source_Economic_Model, finance-bp-105--open-climate-investing · **Applicable to**: macro-data

When implementing financial calculations subject to regulatory oversight (EIOPA Solvency II, CAPM, Fama-French), use exact formula specifications from authoritative sources. The Smith-Wilson convergence point must follow EIOPA paragraph 120, factor regressions must use excess returns with properly scaled inputs. Apply this pattern when calculations will be used for regulatory reporting or investment decision-making.

## `CW-MACRO-DATA-003` — Strict Data Schema Enforcement
**From**: finance-bp-083--Economic-Dashboard, finance-bp-077--Open_Source_Economic_Model · **Applicable to**: macro-data

Financial data pipelines require strict schema validation at ingestion points. OHLCV requires specific columns, CSV imports require exact column names matching field access, INI files require specific sections. Missing or malformed schema elements should fail loudly rather than produce silent corruption. Apply this pattern during data import to catch errors early before downstream calculations use bad data.

## `CW-MACRO-DATA-004` — Composite Primary Key Uniqueness
**From**: finance-bp-105--open-climate-investing, finance-bp-080--FinDKG, finance-bp-083--Economic-Dashboard · **Applicable to**: macro-data

Time-series financial databases require composite primary keys (ticker, date) to ensure uniqueness and enable efficient querying. Inconsistent primary keys across tables break JOIN operations essential for feature merging. Apply this pattern when designing any financial database schema involving time-series measurements with multiple entities.

## `CW-MACRO-DATA-005` — External API Rate Limiting
**From**: finance-bp-074--FinRobot · **Applicable to**: macro-data

When accessing external financial APIs (SEC EDGAR, data vendors), strict rate limiting must be implemented before deployment. SEC EDGAR enforces 10 requests per second with IP blocking consequences. Use decorators and proper User-Agent headers. Apply this pattern when integrating any external financial data API to prevent service disruption that blocks critical data access.

## `CW-MACRO-DATA-006` — Graph Attribute Propagation in Batching
**From**: finance-bp-080--FinDKG, finance-bp-105--open-climate-investing · **Applicable to**: macro-data

When creating subgraph variants during batch collation in graph-based ML, all metadata attributes (num_nodes, num_relations, time_interval) must be explicitly propagated to each subgraph. Downstream model components expect these attributes on all graph objects. Apply this pattern whenever implementing custom collate functions for graph neural networks to prevent training failures.

## `CW-MACRO-DATA-007` — Statistical Validity Thresholds
**From**: finance-bp-105--open-climate-investing, finance-bp-083--Economic-Dashboard · **Applicable to**: macro-data

Factor regressions and statistical calculations require minimum observation counts (typically 20+) for reliable inference. Inner joins, winsorization, and date filtering reduce observations; pipeline validation must check for sufficient data points before regression. Apply this pattern whenever computing regression statistics to ensure results are meaningful rather than spurious.

## `CW-MACRO-DATA-008` — Data Type Strictness for ML Operations
**From**: finance-bp-080--FinDKG, finance-bp-077--Open_Source_Economic_Model · **Applicable to**: macro-data

Graph operations and time calculations require strict dtype consistency (float32 for time values, integer for node types, boolean for masks). Type mismatches cause silent failures in edge_subgraph, degree calculations, and time interval transformations. Apply this pattern when preparing data for graph neural networks or any numerical ML pipeline to catch dtype issues early.
