## Description: <br>
Book flights for coffee tours to famous coffee origins and cafe culture destinations, with support for related travel booking tasks through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search coffee-tour flights, compare options, and produce booking-oriented Markdown grounded in flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can instruct an agent to install a persistent global npm CLI before searching flights. <br>
Mitigation: Require user or operator approval before installing the CLI, and verify the npm package source and version before use. <br>
Risk: Travel-search details may be sent to the flyai or Fliggy provider during CLI execution. <br>
Mitigation: Use the skill only when the user accepts provider-mediated travel search, and avoid submitting unnecessary personal or sensitive details. <br>
Risk: The skill scope is broader than its coffee-tour framing and can cover other travel booking categories. <br>
Mitigation: Prefer narrower skills for non-coffee or non-flight travel requests, and confirm that this skill is appropriate before activation. <br>


## Reference(s): <br>
- [coffee-tour release page](https://clawhub.ai/xiejinsong/coffee-tour) <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight options must be based on flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
