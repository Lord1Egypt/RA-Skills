## Description: <br>
Find concerts, live performances, sports events, festivals, and related travel options through FlyAI and Fliggy CLI data, returning ticket prices, seating information, and direct booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel or event agents use this skill to search for concerts, performances, sports events, festivals, and related booking options with real-time provider data and direct booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may auto-install a global FlyAI npm package before use. <br>
Mitigation: Review and approve the global npm installation source before enabling the skill in an agent environment. <br>
Risk: Travel or ticket searches are sent through the FlyAI provider. <br>
Mitigation: Use the skill only when users accept sending search details to that provider. <br>
Risk: The skill can persist raw queries and command history in .flyai-execution-log.json. <br>
Mitigation: Disable, delete, or rotate the local execution log when query retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/concert-event-tickets) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should come from FlyAI CLI output, include direct booking links when listing results, and avoid raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata; artifact frontmatter lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
