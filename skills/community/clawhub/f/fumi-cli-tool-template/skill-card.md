## Description: <br>
Provides an OpenClaw workspace template for CLI tool development, including agent identity, workspace rules, user preferences, and heartbeat check templates focused on CLI UX, documentation, testing, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiroFumiko](https://clawhub.ai/user/HiroFumiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a starting workspace template for CLI tool projects, with reusable OpenClaw files for agent behavior, coding rules, user preferences, and periodic project checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory instructions may cause local notes to retain personal context or project decisions longer than intended. <br>
Mitigation: Review AGENTS.md before use and require explicit approval for memory writes or restrict what may be recorded. <br>
Risk: Heartbeat-driven behavior may encourage proactive checks or workspace edits without enough user control. <br>
Mitigation: Edit HEARTBEAT.md to define allowed checks, reporting-only behavior, and approval requirements before enabling periodic work. <br>
Risk: Template placeholders can produce misleading user, environment, or workflow assumptions if copied without customization. <br>
Mitigation: Replace placeholder values in USER.md and related templates before using the workspace for real development. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HiroFumiko/fumi-cli-tool-template) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable workspace files for SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog released 2026-03-19, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
