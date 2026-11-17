# Convbox-DiagClaw

**Your Marketing Doctor**

Maintained by [RTOAI](https://www.rto.ai/).

[简体中文](README.zh-CN.md)

Convbox-DiagClaw is a lightweight, open Agent Skill for DTC ecommerce
marketing diagnosis. It turns natural-language questions into focused
analysis using Convbox first-party attribution data, then returns quantified
findings, prioritized next steps, and daily, weekly, or custom-window reports.

> **Status: Preview.** Convbox-DiagClaw is a starting point toward
> diagnosis-as-a-service. It is ready for evaluation and analyst-assisted
> workflows, but recommendations still require human review before execution.

## Diagnose Before You Optimize

Dashboards show what changed. Convbox-DiagClaw is designed to help explain
why it changed and what should be investigated next.

The working loop is:

```text
Natural-language question
        -> automatic scenario routing
        -> first-party data retrieval
        -> diagnosis and comparison
        -> prioritized recommendations
        -> daily / weekly / custom report
```

The skill does not depend on users memorizing analysis-plan names. It detects
intent, selects the relevant diagnostic workflow, keeps metric definitions
consistent, and states when missing data prevents a reliable conclusion.

## Capability Layers

| Layer | What it covers | Representative outputs |
|---|---|---|
| Monitor and diagnose | Growth anomalies, ROAS and CPA changes, attribution gaps, tracking health, creative and campaign performance, funnel loss, profit quality | Root-cause findings, quantified gaps, ranked issues |
| Optimize | Budget allocation, scaling decisions, bid strategy, audience efficiency, retargeting incrementality | Prioritized recommendations with supporting evidence |
| Report | Daily pulse, weekly review, monthly or custom-window analysis, role-specific reporting | Decision-ready summaries for marketing teams and operators |

Monitoring is host-triggered or scheduled batch analysis. It is not a
real-time streaming alert service.

## Why Convbox-DiagClaw

- **First-party data as the decision foundation:** Convbox attribution metrics
  are the primary source of truth for diagnosis; Meta and Google self-reported
  metrics are comparison signals.
- **Automatic routing:** users ask a business question in natural language and
  the skill selects the relevant analysis plan or plan chain.
- **Quantified attribution discrepancies:** the skill can calculate and rank
  platform over-reporting by percentage and conversion-value gap instead of
  only saying that numbers disagree.
- **Portable across agent ecosystems:** the same open skill is designed for
  Claude Code, Codex, OpenClaw, Hermes, WorkBuddy, GitHub Copilot, and other
  hosts that support `SKILL.md` workflows and HTTPS access.
- **Open and adaptable:** customers and contributors can inspect the rules,
  adjust analysis plans, or propose new diagnostic scenarios.
- **Human-controlled execution:** the skill recommends and explains; it does
  not silently change campaigns, bids, budgets, or storefronts.

## Example Questions

```text
My Meta ROAS fell last week. Can you diagnose the cause?
Why do Meta and Google report more conversions than our first-party data?
Which channels can safely receive more budget?
Where are customers dropping out of the onsite funnel?
Create a weekly paid-media review and prioritize what we should fix first.
```

Representative workflows include:

- Growth health and campaign anomaly diagnosis
- ROAS decline and CPA increase decomposition
- Platform-reported versus first-party attribution discrepancy analysis
- Tracking and match-rate health checks
- Channel, campaign, audience, and creative performance analysis
- Site funnel, landing-page reception, and add-to-cart diagnosis
- Budget allocation, scaling, and bid-strategy guidance
- Profit quality and retargeting incrementality analysis

## Install

### Ask your agent

```text
Inspect https://github.com/RTOAI/Convbox-DiagClaw and its SKILL.md first.
Then install the convbox-diagclaw skill for my agent. After installation,
help me configure CONVBOX_API_KEY using secure environment settings. Never
print the key or write it into the repository, prompts, or logs.
```

### One command

Install with the open Agent Skills CLI (Node.js 18+):

```bash
npx skills add RTOAI/Convbox-DiagClaw --skill convbox-diagclaw -g
```

The installer detects supported agents and lets the user select the target.
To install manually for Codex:

```bash
git clone https://github.com/RTOAI/Convbox-DiagClaw.git \
  ~/.codex/skills/convbox-diagclaw
```

For another agent client, clone the repository into its documented skill
directory or point the client at this repository root.

## Requirements

- A skill-capable AI agent that can read `SKILL.md` and make HTTPS requests
- A Convbox account with a valid API key
- Python 3.10+ and PyYAML 6.x only for the optional health checker

The hosted Convbox API is a separate service. The repository license does not
grant API access or override the service terms associated with a Convbox
account.

Configure the API key in the process environment. Do not add the real value to
an `.env` file that may be committed.

macOS or Linux:

```bash
export CONVBOX_API_KEY="your-key"
```

Windows PowerShell:

```powershell
$env:CONVBOX_API_KEY = "your-key"
```

## Verify The Installation

Install the optional health-check dependency and validate local configuration:

```bash
python -m pip install -r requirements.txt
python utilities/config-health-check/config_health_check.py --config-only
```

Probe the documented API endpoints with a recent window:

```bash
python utilities/config-health-check/config_health_check.py \
  --recent-window 7 --strict
```

The checker never prints the API key. It reports `OK`, `WARN`, `FAIL`, or
`SKIP` for each check.

## How Analysis Is Routed

1. `SKILL.md` identifies intent and required business context.
2. `functions.md` selects the scenario, data interfaces, tier, and readiness.
3. `access.yaml` defines exact API request and response fields.
4. The matching file in `plans/` defines data preparation, comparison,
   diagnosis, and recommended next steps.
5. The agent reports the plans used and states data or business-input limits.

## Repository Layout

```text
.
|-- SKILL.md                 # Agent entry point, routing, and safety rules
|-- functions.md             # Data contracts and scenario catalog
|-- access.yaml              # Convbox API request and response dictionary
|-- plans/                   # Atomic analysis blueprints
|-- utilities/
|   `-- config-health-check/ # Credential, connectivity, and schema checker
|-- CONTRIBUTING.md
|-- SECURITY.md
`-- LICENSE
```

## Data And Safety Boundaries

- The skill consumes aggregated Convbox API responses; it does not perform
  customer-level ETL.
- Platform passthrough data is for discrepancy analysis and must not be added
  directly to first-party attribution metrics.
- Profit analysis requires configured cost data. Precise bid guidance requires
  a confirmed gross margin or an explicit user assumption.
- Empty or unavailable data is reported as a limitation, never fabricated.
- Outputs can vary by model. Validate high-impact recommendations with a human
  analyst and the relevant platform before execution.
- Do not include customer exports, API responses, account IDs, or validation
  evidence in issues or pull requests.

## Direction

The current release focuses on diagnosis, recommendations, and reporting.
Future directions may include a unified severity framework, human-approved
execution, persistent customer context, recommendation feedback loops, and
shareable report artifacts. These are roadmap directions, not current release
commitments.

Scenario readiness is authoritative in the **Development status** column of
[`functions.md`](functions.md). A plan file alone does not imply production
readiness.

## Contributing And Security

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing metric definitions, API
fields, or recommendation thresholds. Report credentials, unauthorized data
exposure, and authorization issues through [SECURITY.md](SECURITY.md), not a
public issue.

## License

The repository is available under the [MIT-0 license](LICENSE). Access to the
hosted Convbox API is separate and requires an authorized account.

Convbox names and logos are trademarks of RTOAI. MIT-0 grants no trademark
rights.
