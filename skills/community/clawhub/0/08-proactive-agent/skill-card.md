## Description: <br>
Helps agents act as proactive assistants by maintaining local memory, running check-ins, surfacing useful ideas, and applying guardrails before external actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2720480371](https://clawhub.ai/user/2720480371) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an assistant that can preserve context, learn user preferences, perform periodic workspace checks, and propose helpful next actions while keeping sensitive or external actions gated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage broad proactive workspace monitoring and autonomous checks. <br>
Mitigation: Limit autonomous checks to approved directories and tasks, and require explicit approval before creating cron jobs or autonomous sub-agents. <br>
Risk: The skill keeps long-term local memory that may capture sensitive personal or project context. <br>
Mitigation: Define sensitive-data exclusions before use and periodically review, redact, or clear generated memory files. <br>
Risk: The skill references actions involving email, calendars, file deletion, app or tab closing, and external posting. <br>
Mitigation: Require human approval before email or calendar access, external sends or posts, app or tab closing, and file deletion or trashing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2720480371/08-proactive-agent) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Publisher profile](https://clawhub.ai/user/2720480371) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with file templates, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent operating practices and local workspace files for memory, onboarding, heartbeat checks, security review, and tool notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
