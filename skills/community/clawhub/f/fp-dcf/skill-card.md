## Description: <br>
Estimate intrinsic value with a first-principles DCF from structured JSON or provider-backed ticker input, and return auditable FCFF, WACC, and per-share value output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiejiang8](https://clawhub.ai/user/tiejiang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and research workflows use FP-DCF to run auditable public-company DCF valuations, implied-growth checks, and WACC/terminal-growth sensitivity analysis from structured or provider-backed inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Valuation outputs may be misleading if assumptions, provider data, or cache freshness are stale or unsuitable for the company. <br>
Mitigation: Review all assumptions, freshness fields, diagnostics, and warnings before relying on the result, and refresh provider data when current market conditions matter. <br>
Risk: Provider-backed runs may contact Yahoo Finance, AkShare, and BaoStock and cache market snapshots locally. <br>
Mitigation: Use manual fundamentals, disable provider refreshes, and set a dedicated cache or output directory for private or policy-restricted workflows. <br>
Risk: The tool is a valuation layer and is not designed for buy/sell decisions, portfolio construction, or financial-sector company models. <br>
Mitigation: Pair outputs with independent business analysis and avoid using the skill as a standalone investment recommendation system. <br>


## Reference(s): <br>
- [FP-DCF methodology](references/methodology.md) <br>
- [ClawHub skill page](https://clawhub.ai/tiejiang8/fp-dcf) <br>
- [Project homepage](https://github.com/tiejiang8/FP-DCF) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON with optional SVG/PNG sensitivity chart files and concise Markdown-facing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provider-backed runs may fetch public market data and write local cache or output artifacts.] <br>

## Skill Version(s): <br>
0.5.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
