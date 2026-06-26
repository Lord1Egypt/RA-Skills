# Industry Terms: Data / Analytics

> **Usage note:** This file is for data engineering, analytics engineering, BI, and analytics-facing data work. Use this file to catch colloquial or informal descriptions and map them to the recognized industry terms that belong on a resume or portfolio. If the user's work is more about query engines, transactions, indexing, or database internals, use the data management file instead.

---

## Data Modeling & Warehousing

| User's description | Industry term |
|---|---|
| "moved raw data into cleaned layers" | Medallion Architecture (Bronze/Silver/Gold) |
| "organized tables for business reporting" | Dimensional Modeling / Star Schema |
| "kept one official definition for each metric" | Semantic Layer / Metrics Governance |
| "made business data easier to query" | Data Mart / Analytical Modeling |
| "handled attributes that changed over time" | Slowly Changing Dimensions (SCD) |
| "stored raw and structured data in one platform" | Data Lakehouse Architecture |
| "joined event and business data into one view" | Customer 360 / Unified Data Model |
| "built datasets for downstream teams, not just one-off analysis" | Data Product / Reusable Data Asset |

## Pipelines & Reliability

| User's description | Industry term |
|---|---|
| "loaded data first and transformed it in the warehouse later" | ELT (Extract, Load, Transform) |
| "moved cleaned warehouse data back into operational tools" | Reverse ETL / Operational Analytics |
| "reprocessed history to fix old records" | Historical Backfill / Replay |
| "caught broken or stale pipelines quickly" | Data Observability / Freshness Monitoring |
| "tracked upstream and downstream impact of changes" | Data Lineage / Impact Analysis |
| "agreed schemas before teams shipped integrations" | Data Contracts / Schema Governance |
| "scheduled pipelines with retries and dependencies" | Workflow Orchestration / DAG Scheduling |
| "gave datasets owners and reliability expectations" | Data SLA / Data Reliability Engineering |

## Analytics & Decision Support

| User's description | Industry term |
|---|---|
| "answered business questions without writing ad hoc SQL every time" | Self-Serve BI / Governed Analytics |
| "built dashboards leaders could actually trust" | Executive Dashboarding / Single Source of Truth |
| "turned event logs into business metrics" | Event Instrumentation / Analytics Engineering |
| "measured how different user groups behaved over time" | Cohort Analysis / Segmentation Analytics |
| "found where users or revenue dropped off" | Funnel Analytics / Conversion Analysis |
| "set common metric definitions across teams" | Business Glossary / Metric Standardization |
| "made experiment results reusable for decision-making" | Experiment Readouts / Decision Intelligence |
| "modeled revenue or ops metrics directly in code" | Metrics-as-Code / Analytics Engineering |
