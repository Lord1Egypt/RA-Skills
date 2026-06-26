## Description: <br>
Better Every Run turns explicit /ber corrections into preferred future outcomes through a small fix, remember, and report flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to explicitly capture corrections, preferences, and reusable lessons from a run, then review whether they should stay local or become durable memory, skill behavior, or eval coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local correction records may contain secrets, private identifiers, or workspace-specific details if users include them in lessons. <br>
Mitigation: Review .better-every-run before sharing a workspace and avoid recording secrets or private identifiers. <br>
Risk: Promoting lessons too broadly can cause future agents to follow stale or overly specific behavior. <br>
Mitigation: Approve memory or skill promotions only when the lesson should truly affect future agent behavior. <br>
Risk: Incorrect correction proposals could introduce misleading guidance into memory, skills, or eval fixtures. <br>
Mitigation: Use the reviewed card and promote flow, require a clean scanner verdict, and quarantine or supersede lessons that should not become durable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/better-every-run) <br>
- [README](README.md) <br>
- [Better Every Run Workflow](references/workflow.md) <br>
- [Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise chat text with optional shell command output and JSON/JSONL eval fixtures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records explicit lessons in a local .better-every-run store; durable promotions require a reviewed card, a stable target hash, and a clean scanner verdict.] <br>

## Skill Version(s): <br>
0.5.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
