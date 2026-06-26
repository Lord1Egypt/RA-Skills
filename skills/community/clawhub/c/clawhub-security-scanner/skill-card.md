## Description: <br>
Audits SKILL.md files for permission overreach, prompt injection, and scope mismatch, returning a structured security report with a risk score and recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and skill users use this skill as a first-pass review helper before installing or assessing ClawHub skills, especially when checking tool permissions, prompt-injection risk, and scope mismatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README describes broader coverage than the actual skill instructions. <br>
Mitigation: Treat this release as the three-check scanner described in SKILL.md and use deeper review for suspicious tool calls, data exfiltration, social engineering, and known bad pattern checks. <br>
Risk: URL-based scans require the agent to fetch remote skill content. <br>
Mitigation: Scan only URLs the user intends the agent to retrieve, and review fetched content before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordo-tech/clawhub-security-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/ordo-tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown security audit report with a risk score, findings table, summary, and recommended action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports SAFE, LOW RISK, MEDIUM RISK, or HIGH RISK according to the skill instructions.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
