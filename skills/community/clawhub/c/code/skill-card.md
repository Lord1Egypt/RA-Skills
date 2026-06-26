## Description: <br>
Coding workflow with planning, implementation, verification, and testing for clean software development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill when they want an agent to follow a coding workflow for planning, implementation, verification, testing, and delivery. It also guides agents to store only explicitly requested local coding preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local preference memory could contain secrets or sensitive project details if a user asks the agent to save them. <br>
Mitigation: Review saved preferences in ~/code/memory.md and avoid storing secrets or sensitive project details unless they are intentionally meant for future agent sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/code) <br>
- [Skill Homepage](https://clawic.com/skills/code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local preference-memory content under ~/code/memory.md only when the user explicitly asks to save preferences.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
