## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatfingererr](https://clawhub.ai/user/fatfingererr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to review third-party agent skills before installation by checking source credibility, code patterns, requested permissions, and installation risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes example curl commands for inspecting GitHub-hosted skills. <br>
Mitigation: Review each command before running it and only provide repositories or URLs that the agent is intended to inspect. <br>
Risk: Checklist-style security guidance may be incomplete or applied incorrectly by an agent. <br>
Mitigation: Use the checklist as a review aid and retain human approval for high-risk findings, credential access, elevated permissions, or unclear source trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fatfingererr/azhua-skill-vetter) <br>
- [Publisher profile](https://clawhub.ai/user/fatfingererr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown checklist and vetting report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable review findings, permission notes, risk classification, and install verdict guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
