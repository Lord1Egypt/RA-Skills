## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to review third-party skills before installation, checking source reputation, permission scope, suspicious patterns, and documenting a risk-based verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A vetting report can be incomplete or mistaken if treated as a guarantee. <br>
Mitigation: Use the report as guidance and have a human review high-risk or ambiguous findings before installation. <br>
Risk: File or GitHub review actions could inspect sources the user did not intend to evaluate. <br>
Mitigation: Limit review commands and file reads to explicitly requested sources and verify repository identifiers before running optional commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinthqod/fox-skill-vetter) <br>
- [Publisher profile](https://clawhub.ai/user/qinthqod) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown checklist and vetting report with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a human-readable risk classification, verdict, red-flag summary, and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
