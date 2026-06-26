## Description: <br>
Provides OpenClaw workspace templates for data analysis projects, including data-driven decision-making, exploratory data analysis, and model development principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiroFumiko](https://clawhub.ai/user/HiroFumiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and teams use this skill to create an OpenClaw workspace for repeatable data analysis and machine learning projects. It supplies Markdown templates for agent identity, operating rules, user preferences, monitoring, and data-analysis practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The copied workspace rules include autonomous-action language that may be broader than a user's operating policy. <br>
Mitigation: Review AGENTS.md and HEARTBEAT.md before use, then narrow or remove the 'Don't ask permission' language where approvals are required. <br>
Risk: Workspace memory files could accumulate sensitive project context if used without boundaries. <br>
Mitigation: Keep MEMORY.md and daily notes limited to project context that is acceptable to reuse in future sessions. <br>
Risk: Credential preferences or access notes could be written into Markdown workspace files. <br>
Mitigation: Do not store raw API keys, database passwords, or other secrets in the generated templates or memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HiroFumiko/fumi-data-analysis-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/HiroFumiko) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with installation and customization commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace files for SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
