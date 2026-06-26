## Description: <br>
Helps agents search eco-hotel and sustainable travel flights by using flyai CLI results and returning booking-ready Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers or travel support agents use this skill to collect route and date preferences, run real-time flight searches, and return booking options with Book links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an external global CLI package to fetch travel results. <br>
Mitigation: Review the @fly-ai/flyai-cli package source, install it in an isolated environment when possible, and use the skill only for the documented flight-search flows. <br>
Risk: The skill advertises broader travel capabilities than its documented workflows support. <br>
Mitigation: Limit use to the documented flight search commands unless additional workflows are reviewed and added with matching parameters and validation. <br>
Risk: Travel answers can be misleading if they are produced from model knowledge instead of live CLI output. <br>
Mitigation: Require CLI output as the data source and verify every displayed result includes a Book link derived from detailUrl. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/eco-hotel) <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel search results with booking links and occasional shell commands for CLI execution or installation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLI-derived results; each listed result must include a Book link when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
