---
name: awp-ext-financial
description: >
  AWP extension for financial analysis, trading, and compliance workflows.
  Adds mandatory risk assessment agent, audit trail, and regulatory controls.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    tags:
      - awp
      - awp-extension
      - financial
      - compliance
      - risk-assessment
---

# AWP Extension: Financial Workflows

## Extends

base: skill/SKILL.md
adapter: skill/adapters/standalone.md

## Description

Extension for financial analysis, trading, and compliance workflows.
Enforces regulatory audit requirements, risk assessment, and data
integrity controls.  Every workflow built with this extension includes
a mandatory risk assessor agent and produces audit-ready output.

Use this extension when building workflows that handle financial data,
market analysis, portfolio management, regulatory reporting, or any
domain where auditability and risk scoring are required.

## Defaults

```yaml
defaults:
  compliance_level: L4             # Observable minimum (audit trail required)
  model: anthropic/claude-sonnet-4
  execution_mode: parallel
  temperature: 0.1                 # Low temperature for financial precision
  memory:
    long_term: true
    daily_log: true
  observability:
    tracing: true
    metrics: true
    audit: true
    audit_hash_chain: true         # Tamper-evident audit log
```

## Required Agents

Every financial workflow MUST include these agents.  The user's
requested agents are added alongside them in the DAG.

```yaml
agents:
  - id: risk_assessor
    role: risk-analyst
    description: >
      Evaluates the risk profile of all agent outputs.  Runs last
      in the DAG (depends on all other agents).  Produces a risk
      score and flags any findings that exceed configured thresholds.
    tools: []
    output_fields:
      risk_score:
        type: number
        minimum: 0.0
        maximum: 1.0
        description: "Overall risk score (0=safe, 1=critical)"
        shareable: true
        required: true
      risk_flags:
        type: array
        items: { type: string }
        description: "List of identified risk factors"
        shareable: true
        required: true
      risk_verdict:
        type: string
        description: "approve | review | reject"
        shareable: true
        required: true
```

The `risk_assessor` agent MUST depend on all other leaf agents in the graph
so it sees the complete workflow output before rendering a verdict.

## Required Output Fields

In addition to the base `confidence` field (R17), every agent in a
financial workflow MUST include these fields in its output.contract:

```yaml
fields:
  - name: data_sources
    type: array
    items: { type: string }
    description: "List of data sources consulted for this output"
    shareable: true
    required: true

  - name: assumptions
    type: array
    items: { type: string }
    description: "Key assumptions underlying the analysis"
    shareable: true
    required: false
```

## Additional Rules

These rules apply on top of the base R1-R24:

- **F1:** Every workflow MUST have `observability.audit.enabled: true` with `hash_chain: true`.
- **F2:** No agent MAY use `shell.execute` (code execution is a compliance risk).
- **F3:** All agents MUST set `output.validation.mode: "strict"` -- no lenient parsing for financial data.
- **F4:** The `risk_assessor` agent MUST be the last agent in the DAG (depends on all leaf nodes).
- **F5:** Memory MUST be enabled with at least `long_term` and `daily_log` tiers (L3+ for audit trail).
- **F6:** All output fields containing monetary values MUST have `type: "number"` (not string).
- **F7:** Every agent's system prompt MUST include the disclaimer: "This is not financial advice."

## Constraints

```yaml
constraints:
  denied_tools:
    - shell.execute
    - file.write              # Agents should not write arbitrary files
  required_memory_tiers:
    - long_term
    - daily_log
  min_compliance: L4           # Must have full observability
  max_temperature: 0.3         # Financial outputs need determinism
  required_sections:
    - observability
    - security                 # Circuit breaker for API failures
```

## Additional Templates

### System Prompt Prefix

Injected at the top of every agent's SYSTEM_PROMPT.md:

```yaml
templates:
  - file: SYSTEM_PROMPT_PREFIX.md
    inject: prepend
    content: |
      ## Financial Compliance Notice

      You are operating in a regulated financial context.  All outputs
      will be audited.  Follow these mandatory guidelines:

      1. Cite your data sources for every claim.
      2. Clearly state assumptions.
      3. Never present analysis as financial advice.
      4. Flag uncertainty explicitly -- when in doubt, increase the
         risk score rather than presenting false confidence.
      5. Use precise numerical values (not "about $5M" but "$5,000,000").
```

### Risk Assessor System Prompt

Complete system prompt for the required `risk_assessor` agent:

```yaml
templates:
  - file: risk_assessor_SYSTEM_PROMPT.md
    agent: risk_assessor
    inject: replace
    content: |
      # Risk Assessor

      You are a financial risk assessment specialist.  Your job is to
      review the outputs of all preceding agents in this workflow and
      produce a comprehensive risk evaluation.

      ## Input

      You receive the outputs of all other agents in the workflow
      via the shared state.  Each agent has produced structured data
      with a confidence score, data sources, and assumptions.

      ## Your Task

      1. Review each agent's output for consistency and plausibility.
      2. Cross-check data sources -- flag if an agent has no sources.
      3. Evaluate assumptions -- flag unrealistic or contradictory ones.
      4. Compute an overall risk_score (0.0 = safe, 1.0 = critical).
      5. List specific risk_flags as short descriptions.
      6. Render a verdict: "approve", "review", or "reject".

      ## Verdict Criteria

      - **approve**: risk_score < 0.3 and no critical flags
      - **review**: risk_score 0.3-0.7 or any medium-severity flags
      - **reject**: risk_score > 0.7 or any critical flags

      ## Output Format

      Respond with valid JSON matching the output schema.
```

## Additional Skills

```yaml
skills:
  - name: financial_regulations
    content: |
      # Financial Regulations Reference

      ## Key Principles

      - **Data Integrity**: All numerical outputs must be traceable
        to source data.  No fabricated numbers.
      - **Audit Trail**: Every decision must be logged with timestamp,
        agent ID, and rationale.
      - **Segregation of Duties**: The agent producing analysis must
        not be the same agent assessing its risk.
      - **Timeliness**: Market data older than the current session
        should be flagged with a staleness warning.

      ## Common Financial Metrics

      | Metric | Formula | Use |
      |--------|---------|-----|
      | ROI | (Gain - Cost) / Cost | Investment return |
      | Sharpe Ratio | (Return - RiskFree) / StdDev | Risk-adjusted return |
      | VaR | Quantile of loss distribution | Maximum expected loss |
      | Beta | Cov(asset, market) / Var(market) | Market sensitivity |

  - name: disclaimer
    content: |
      # Disclaimer

      All outputs generated by this workflow are for informational
      purposes only and do not constitute financial advice.  Always
      consult a qualified financial professional before making
      investment decisions.
```

## Additional Tools

```yaml
tools:
  - fqn: finance.market_data
    description: "Fetch current market data for a ticker symbol"
    template: |
      from __future__ import annotations
      from typing import Any, Dict
      try:
          from mcp.server.fastmcp import FastMCP
      except Exception:
          class FastMCP:
              def __init__(self, name): self.name = name
              def tool(self, _name):
                  def _d(fn): return fn
                  return _d

      app = FastMCP("finance")

      @app.tool("finance.market_data")
      def get_market_data(*, ticker: str, period: str = "1d") -> Dict[str, Any]:
          """Fetch market data for a ticker symbol.

          Args:
              ticker: Stock ticker (e.g., "AAPL", "MSFT").
              period: Time period ("1d", "5d", "1mo", "3mo", "1y").
          """
          # Placeholder -- replace with actual API call
          return {
              "ok": True,
              "status": 200,
              "data": {"ticker": ticker, "period": period, "price": 0.0},
              "error": None,
          }

  - fqn: finance.risk_calc
    description: "Calculate standard financial risk metrics"
    template: |
      from __future__ import annotations
      from typing import Any, Dict, List
      try:
          from mcp.server.fastmcp import FastMCP
      except Exception:
          class FastMCP:
              def __init__(self, name): self.name = name
              def tool(self, _name):
                  def _d(fn): return fn
                  return _d

      app = FastMCP("finance")

      @app.tool("finance.risk_calc")
      def calculate_risk(*, values: List[float], risk_free_rate: float = 0.04) -> Dict[str, Any]:
          """Calculate risk metrics from a series of returns.

          Args:
              values: List of return values (e.g., daily returns).
              risk_free_rate: Annual risk-free rate (default 4%).
          """
          if not values:
              return {"ok": False, "status": 400, "data": {}, "error": "Empty values"}
          import statistics
          mean_return = statistics.mean(values)
          std_dev = statistics.stdev(values) if len(values) > 1 else 0.0
          sharpe = (mean_return - risk_free_rate) / std_dev if std_dev > 0 else 0.0
          return {
              "ok": True,
              "status": 200,
              "data": {
                  "mean_return": round(mean_return, 6),
                  "std_dev": round(std_dev, 6),
                  "sharpe_ratio": round(sharpe, 4),
                  "var_95": round(mean_return - 1.645 * std_dev, 6),
              },
              "error": None,
          }
```

## Example Usage

Tell the AI:

> "Build a financial workflow that analyzes a stock portfolio.
>  Use the financial extension."

The AI will:
1. Load `SKILL.md` + `adapters/standalone.md` + this extension
2. Generate the user's requested agents (e.g., `data_collector`, `analyzer`)
3. Automatically add `risk_assessor` as the final agent
4. Add `data_sources` and `assumptions` fields to every output contract
5. Prepend the compliance notice to every system prompt
6. Set observability to L4 with hash-chain audit
7. Place `finance.market_data` and `finance.risk_calc` tools in `mcp/`
8. Place `financial_regulations` and `disclaimer` skills in `skills/`
9. Deny `shell.execute` and `file.write` tools
10. Validate against R1-R24 + F1-F7
