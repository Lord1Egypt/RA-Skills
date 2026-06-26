## Description: <br>
A 股投研指挥官 orchestrates multiple A-share stock analysis skills into workflows for sector scanning, sector analysis, individual stock research, and portfolio review, then produces structured investment briefs and archives them to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jioup777](https://clawhub.ai/user/jioup777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to coordinate A-share market research workflows, including hotspot discovery, sector research, single-stock deep dives, and portfolio health checks. It is intended to synthesize outputs from other analysis skills into readable briefs, research reports, debate summaries, and operational guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include real portfolio holdings, profit/loss details, client data, or private strategy notes and may be stored in the configured Feishu space. <br>
Mitigation: Require manual confirmation before publishing to Feishu, or use a local-only/redacted workflow for sensitive holdings and strategy information. <br>
Risk: Generated market research can be misread as final investment advice, especially when workflows produce ratings, target prices, and trading actions. <br>
Mitigation: Label outputs as research support, review data freshness and assumptions, and require a human decision-maker before acting on the recommendations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jioup777/a-stock-orchestrator) <br>
- [Sub-skill quick reference](artifact/references/sub-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports with tables, links, command snippets, and optional chart image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create separate Feishu documents for the summary brief, deep research report, and bull-bear debate when configured.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
