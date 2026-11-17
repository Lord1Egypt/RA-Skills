# POC Technology Selection Guide

## Principles

Start by deducing the minimum technical path from the business results to be verified, failure modes, and customer constraints. Don’t write it as the default answer just because the team is familiar with a certain framework or a certain architecture is popular in the market.

## Do you need generative AI?

| Mission Characteristics | Preferred Direction | Reason |
|---|---|---|
| Rules are stable, inputs are structured, answers are certain | Traditional code, rules or workflows | Cheaper, predictable, easy to test |
| Need to extract, summarize or generate from long text | Single model call | Verify first whether the model really adds value |
| Requires citation of customer knowledge | Search enhancement + controlled generation | Incorporate provenance, freshness and conflicts into validation |
| Requires multi-step tool invocation and stable paths | Deterministic workflow | Explicit control of order, permissions, and failures |
| Paths vary with context but have clear boundaries | Single agent + minimal toolset | Increase autonomy only when dynamic decision-making is needed |
| Multiple independent roles or contexts must be isolated | Multi-agent | Used only when the benefits of division of labor are greater than the cost of coordination |

## Rapid prototyping interface

| Target | Optional forms | Applicable conditions | Not applicable conditions |
|---|---|---|---|
| Demonstrate algorithm or model behavior | Command line/Notebook | Technicians only, no real workflow required | To verify frontline adoption and interactions |
| Internal forms, views and single processes | Lightweight Web pages | Quickly allow users to complete real tasks | Complex permissions, multi-role production processes |
| Conversation and quote validation | Controlled chat pages | Tasks are naturally conversational and must show the source | Tasks are more suitable for structured forms or batch processing |
| API and system integration | Minimal service interface | Core risks are at data and system boundaries | No proven issues or input contracts yet |
| Batch processing/data pipeline | Scheduled tasks or workflows | Tasks do not require real-time interaction | Instant human judgment and feedback are required |

Tool names are only used as candidates and are not included in the core rules. When choosing Streamlit, Gradio, FastAPI, React, a low-code platform, or the customer's existing platform, document: team capabilities, target platform, data boundaries, identity, observability, deployment constraints, supply chain risks, and migration costs.

## Data path selection

| Paths | When to choose | Extrapolation restrictions that must be stated |
|---|---|---|
| Synthetic data | Verified pages, processes, and obvious guardrails | Not a representation of quality, distribution, privacy, or integration |
| de-identified snapshot | Verify representative input and offline evaluation | Does not represent timeliness, real-time failure and permissions |
| Controlled Mock | Protect cycles and freeze interface contracts | Does not represent real quotas, delays and errors |
| Tests read-only interface | Verifies identity, integration, and timeliness | Does not represent write operations and production capacity |
| Production shadow mode | Verify true distribution without changing business | Privacy, monitoring and exit authorization still required |
| Controlled write operations | Core values must be verified when written | Must be manually confirmed, idempotent, compensated, audited, and rolled back |

## Model and supplier selection

Don’t just choose based on a single benchmark score. At least compare:

- Task quality and critical failure distribution;
- Data usage, retention, geography and training policies;
- Latency, throughput, limits, availability and degradation;
- Context, tool invocation, structured output and observability;
- Cost per transaction, retries, caching, manual review and full run costs;
- Version pinning, change notification, regression and exit migration capabilities.

The POC can first select a candidate model, but must freeze versions and configurations and state that no multi-vendor sourcing or production resilience assessment has been completed.

## Architecture complexity upgrade gate

The next level of complexity is added only when the current solution cannot meet the freezing criteria:

1. Static or rule reference implementation;
2. Single model call;
3. Search or tools;
4. Deterministic multi-step workflow;
5. Single-agent dynamic orchestration;
6. Multi-agent;
7. High autonomy write operations.

Each upgrade is recorded: current failure evidence, alternatives, expected benefits, new risks, evaluation methods and fallback paths.

## Decision record

```markdown
| Objective/Risk | Minimal Candidate | More Complex Candidate | Choice | Evidence | New Risk | Fallback |
|---|---|---|---|---|---|---|
| | | | | | | |
```

The Technology Selection Guide provides decision-making issues and does not replace customer enterprise architecture, security, procurement or production change approvals.
