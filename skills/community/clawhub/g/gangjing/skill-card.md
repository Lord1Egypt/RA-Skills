## Description: <br>
Gangjing is a bilingual contrarian review and red-team skill that challenges product, architecture, and code decisions, escalating to controlled code attack harnesses only when explicitly requested or when users make strong claims about workspace code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blurooo](https://clawhub.ai/user/blurooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical reviewers use this skill to stress-test requirements, architecture choices, API designs, data models, and code-quality claims before committing to a decision. It can provide verbal critique by default and, when explicitly permitted, generate and run local attack harnesses against workspace code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and run local attack harnesses against workspace code. <br>
Mitigation: Require explicit user confirmation before code execution and run harnesses only in an isolated workspace or container. <br>
Risk: Attack harnesses may execute target module top-level code and could expose secrets or production data if pointed at sensitive repositories. <br>
Mitigation: Avoid repositories with credentials, production data, unsafe top-level code, or paths outside the intended workspace. <br>
Risk: The skill is intentionally adversarial and may produce forceful critique. <br>
Mitigation: Use it for review and red-team workflows where contrarian feedback is desired, and validate recommendations before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blurooo/gangjing) <br>
- [Skill homepage](https://github.com/agent-dance/harness-engineering/tree/main/skills/gangjing) <br>
- [Attack dimensions](references/attack-dimensions.md) <br>
- [Attack patterns](references/attack-patterns.md) <br>
- [Intensity calibration](references/intensity-calibration.md) <br>
- [Tool integration](references/tool-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with optional JSON configuration and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local attack configuration, temporary harness code, result summaries, and remediation recommendations when code execution is explicitly allowed.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
