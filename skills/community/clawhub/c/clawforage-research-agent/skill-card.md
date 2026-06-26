## Description: <br>
Deep domain research: entity extraction, cross-article connections, and structured domain reports from a local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dainash](https://clawhub.ai/user/dainash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill after running Knowledge Harvester to analyze saved articles, map entities and relationships, and produce recurring domain research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local articles in memory/knowledge and synthesizes them into new reports. <br>
Mitigation: Review or limit the knowledge files before running the skill, and check generated reports before sharing them. <br>
Risk: Generated reports may include misleading synthesis or source-priority mistakes if the saved articles or source whitelist are incomplete. <br>
Mitigation: Maintain the source whitelist, verify claims against cited sources, and rerun validation before relying on a report. <br>
Risk: The README describes automatic Monday and Thursday runs, which may write reports without an interactive prompt if a scheduler is configured. <br>
Mitigation: Confirm whether a scheduler is enabled and disable or adjust it when automatic report generation is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dainash/clawforage-research-agent) <br>
- [Publisher profile](https://clawhub.ai/user/dainash) <br>
- [InspireHub.ai](https://inspireehub.ai) <br>
- [README](artifact/README.md) <br>
- [Domain report template](artifact/templates/domain-report.md) <br>
- [Source whitelist template](artifact/templates/sources-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell command output used as analysis input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes domain reports under memory/research and may create source whitelist files under memory/clawforage/sources.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
