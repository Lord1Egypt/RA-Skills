## Description: <br>
OpenClaw agent starter kit that provides templates and customization guidance for SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and HEARTBEAT.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiroFumiko](https://clawhub.ai/user/HiroFumiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this starter kit to create a new agent workspace from reusable identity, behavior, user-profile, memory, and heartbeat templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future agents created from the templates may perform broad background checks against email, calendar, social, memory, or repository state without clear approval boundaries. <br>
Mitigation: Review and edit the templates before starting an agent; remove or tighten background checks and require explicit approval before external account access. <br>
Risk: Template memory rules may encourage storing sensitive personal details in persistent files. <br>
Mitigation: Avoid storing secrets or sensitive personal information in persistent memory, and restrict memory loading or sharing in group and shared contexts. <br>
Risk: Template behavior may allow remote repository changes such as git push without enough review. <br>
Mitigation: Require explicit approval for remote changes and review generated agent rules before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HiroFumiko/fumi-agent-starter-kit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces starter template files for an agent workspace; users are expected to edit the templates before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
