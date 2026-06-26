## Description: <br>
Helps agents plan family vacations by using flyai CLI results for flights, hotels, attractions, itineraries, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to assemble family-focused travel options, including kid-friendly lodging, attractions, routes, and booking links from real-time flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global flyai CLI package before use. <br>
Mitigation: Require explicit approval before installing @fly-ai/flyai-cli globally and review the package under the organization's dependency policy. <br>
Risk: Travel searches may be sent to the flyai provider for real-time results. <br>
Mitigation: Tell users that live search requests leave the local agent environment and avoid including unnecessary sensitive family travel details. <br>
Risk: Execution logs can retain raw travel requests locally. <br>
Mitigation: Disable or delete .flyai-execution-log.json when local retention of family travel details is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/family-trip) <br>
- [README](artifact/README.md) <br>
- [Templates reference](artifact/references/templates.md) <br>
- [Playbooks reference](artifact/references/playbooks.md) <br>
- [Fallbacks reference](artifact/references/fallbacks.md) <br>
- [Runbook reference](artifact/references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output for real-time travel results and should not expose raw JSON to users.] <br>

## Skill Version(s): <br>
v3.2.3 (source: server release metadata; SKILL.md frontmatter says 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
