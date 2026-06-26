## Description: <br>
Capture durable lessons from debugging, user corrections, missing capabilities, and repeated workflow friction so future sessions avoid the same mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture reusable corrections, non-obvious failures, project conventions, feature gaps, and proven fixes so future sessions can avoid repeated mistakes. It supports workspace-level learning logs, promotion into durable project memory, and extraction of recurring patterns into standalone skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace learning logs may persist sensitive project details if an agent records too much context. <br>
Mitigation: Keep `.learnings/` out of commits when it may contain sensitive details and review entries before sharing or promoting them. <br>
Risk: Promoting an incorrect lesson into project memory can steer future sessions toward bad guidance. <br>
Mitigation: Review learning entries before moving them into `AGENTS.md`, `CLAUDE.md`, or similar instruction files, and promote only short proven prevention rules. <br>
Risk: Optional hooks can add recurring reminders to future sessions. <br>
Mitigation: Enable hook helpers only when persistent self-improvement reminders are desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/actual-self-improvement) <br>
- [Entry Formats](references/entry-formats.md) <br>
- [Examples](references/examples.md) <br>
- [Promotion and Extraction](references/promotion-and-extraction.md) <br>
- [Platform Setup](references/platform-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Evaluation Plan](references/evaluation.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace-level .learnings Markdown logs and propose short project-memory rules when lessons are promoted.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
