## Description:

Generates evidence-backed A-share daily market review reports from Tushare Pro daily data and Baostock style indexes, covering index trend, market style, sentiment, turnover concentration, money effect, leading themes, catalysts, sublines, heavy-volume declines, feature groups, and factor-mining research while avoiding buy/sell advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinfi-codex](https://clawhub.ai/user/chinfi-codex)

### License/Terms of Use:

MIT-0

## Use Case:

Market-research agents and analysts use this skill to generate post-market A-share review reports, HTML report views, lifecycle records, and factor-mining evidence packs from local market data and API-backed inputs. It is intended for evidence-based market commentary and research workflow support, not trading instructions, order execution, or portfolio optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access, Tushare/Tavily credentials, and write access to a dedicated alpha_data database.

Mitigation: Install only in an environment where those permissions are acceptable, use a dedicated database, and scope credentials to the intended data workflow.

Risk: The search launcher can execute a local file outside the packaged skill before falling back to the bundled implementation.

Mitigation: Before use, remove or reverse the external-path precedence in scripts/web_search.py so the packaged implementation is used by default.

Risk: Offline or private HTML reports may expose network requests through remote font loading.

Mitigation: Disable remote fonts for offline or private report generation.

Risk: Market research outputs could be misread as investment instructions.

Mitigation: Keep the documented output discipline: cite evidence, disclose data gaps, and avoid buy, sell, stop-loss, target-price, order-execution, or portfolio-allocation instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chinfi-codex/skills/a-stock-daily-market-sense)
- [CLI Reference](references/cli_reference.md)
- [Report Template](references/report_template.md)
- [Output Discipline](references/methodology/output_discipline.md)
- [Catalyst and Subline Mining Methodology](references/methodology/catalyst_subline_mining.md)
- [Factor Mining Methodology](references/methodology/factor_mining.md)
- [Theme Lifecycle Reference](references/theme_lifecycle.md)
- [PostgreSQL Setup Notes](scripts/_shared/POSTGRESQL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON evidence and context files, optional HTML reports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic data scripts plus model-authored analysis; report outputs should disclose data gaps and avoid investment advice.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
