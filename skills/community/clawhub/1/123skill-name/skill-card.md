## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in local markdown logs so future sessions can review and promote durable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suncrespo](https://clawhub.ai/user/suncrespo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record command failures, user corrections, knowledge gaps, and feature requests in `.learnings/` markdown files. They can then review, resolve, and promote recurring lessons into agent guidance files or reusable skill scaffolds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local persistent learning logs may retain sensitive prompts, command output, secrets, or private implementation details if users log raw context. <br>
Mitigation: Use short summaries or redacted excerpts, avoid secrets and raw transcripts, and keep logs scoped to trusted project or workspace locations. <br>
Risk: Optional hook scripts can inspect prompt or command-output context and inject reminders during agent workflows. <br>
Mitigation: Prefer project-level hooks over global hooks, add matchers when prompts may contain sensitive material, and review hook scripts before enabling them. <br>
Risk: Promoting unreviewed entries into long-lived agent guidance can preserve incorrect or misleading instructions. <br>
Mitigation: Manually review and approve entries before promoting them into persistent guidance files or extracted skills. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/suncrespo/123skill-name) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown entries and setup guidance with bash, JSON, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local `.learnings/` markdown files and may provide hook setup or reusable skill scaffold instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
