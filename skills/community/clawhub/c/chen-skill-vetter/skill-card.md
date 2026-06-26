## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to vet AI agent skills before installation or execution. It guides source checks, code review, permission review, risk classification, and production of a concise vetting report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publisher or package identity may be mistaken before the checklist is trusted. <br>
Mitigation: Confirm the ClawHub skill page and publisher handle before relying on the skill's recommendations. <br>
Risk: The example GitHub commands can fetch repository metadata or skill files from repositories selected by the user. <br>
Mitigation: Run the commands only against repositories you intentionally choose to review, and inspect fetched content before using it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cs995279497-byte/chen-skill-vetter) <br>
- [Publisher Profile](https://clawhub.ai/user/cs995279497-byte) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown checklist and vetting report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; produces review guidance and a structured security-vetting report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
