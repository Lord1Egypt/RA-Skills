## Description: <br>
Helps agents search birthday-trip flights and related travel options with the flyai CLI, then present comparison tables with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to collect trip parameters, run flyai CLI searches for birthday getaways, and present birthday-friendly flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and rely on an external global flyai CLI package for networked travel searches. <br>
Mitigation: Review the CLI provider and package before installation, and require approval before global npm installs or CLI execution. <br>
Risk: The runbook allows local `.flyai-execution-log.json` logging of travel-search activity. <br>
Mitigation: Disable, redact, or clear local execution logs when queries may contain personal travel details. <br>
Risk: Travel results and booking links depend on external flyai CLI output. <br>
Mitigation: Use only returned `detailUrl` booking links, disclose CLI failures, and avoid substituting unsourced travel claims. <br>


## Reference(s): <br>
- [Templates - birthday-trip](references/templates.md) <br>
- [Playbooks - birthday-trip](references/playbooks.md) <br>
- [Fallbacks - Flight Category (Birthday Trip)](references/fallbacks.md) <br>
- [Runbook - Execution Log Schema (Universal)](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the source of travel data and includes booking detail URLs when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
