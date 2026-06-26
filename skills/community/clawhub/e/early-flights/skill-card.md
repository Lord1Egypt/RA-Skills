## Description: <br>
Finds early departing flights and related travel options through the flyai CLI, using live command output and booking links rather than model knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agent operators use this skill to find early flights, compare live travel options, and return concise booking-oriented Markdown results. It is intended for requests where current travel availability, price, and booking links must come from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local execution of the flyai CLI for travel searches. <br>
Mitigation: Install and review the flyai CLI yourself, avoid sudo when possible, and run it only in an environment where outbound travel search requests are acceptable. <br>
Risk: Travel queries may be persisted in a hidden local execution log. <br>
Mitigation: Review or disable .flyai-execution-log.json logging before use, especially when queries include personal travel details. <br>
Risk: Travel workflows can involve sensitive personal, passport, payment, or booking-reference details. <br>
Mitigation: Do not enter sensitive booking details unless you understand how the CLI and provider handle that data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/early-flights) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are expected to include flyai-derived booking links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
