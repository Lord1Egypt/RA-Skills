## Description: <br>
When the user wants to audit, review, or diagnose SEO issues on their site, this skill uses live web data via the Bright Data CLI for accurate detection of JS-injected schema, hreflang, canonicals, and live SERP-based ranking checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO practitioners use this skill to run evidence-backed technical and on-page SEO audits with Bright Data CLI commands, rendered HTML checks, SERP diagnostics, and prioritized Markdown recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a direct remote installer command for the Bright Data CLI. <br>
Mitigation: Review the installation path first and prefer a package-manager or documented install method; only run the remote installer if the source is trusted. <br>
Risk: SEO audits send site URLs and keyword queries through Bright Data tooling. <br>
Mitigation: Run audits only for sites and keywords the user is authorized to analyze and share with Bright Data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meirk-brd/brightdata-seo-audit) <br>
- [Audit Framework](references/audit-framework.md) <br>
- [bdata Recipes](references/bdata-recipes.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Site Type Playbooks](references/site-type-playbooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and evidence excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by issue, impact, evidence, fix, and priority; unsupported measurements are routed to out-of-scope notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
