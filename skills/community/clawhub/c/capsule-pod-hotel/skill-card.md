## Description: <br>
Find capsule hotels and pod-style accommodations with real-time travel data and booking links through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to find low-cost capsule or pod lodging, compare live hotel results, and return booking links in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and rely on the global @fly-ai/flyai-cli package and send travel queries through it. <br>
Mitigation: Review the CLI package provenance before use, install it explicitly when possible, and run the skill in a contained workspace. <br>
Risk: The skill can retain raw travel queries in a local .flyai-execution-log.json file when filesystem writes are available. <br>
Mitigation: Delete or disable the local execution log if query retention is not desired. <br>


## Reference(s): <br>
- [Capsule Pod Hotel on ClawHub](https://clawhub.ai/dingtom336-gif/capsule-pod-hotel) <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Capsule Hotel Playbooks](references/playbooks.md) <br>
- [Hotel Fallbacks](references/fallbacks.md) <br>
- [Execution Log Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI data and booking detailUrl links; raw JSON is not returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
