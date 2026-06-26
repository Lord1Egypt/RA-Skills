## Description: <br>
Scans skills, files, and folders for potential data leaks, privacy risks, and suspicious behavior by checking for network calls, file access, process spawning, and environment variable access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to triage skills, files, or folders for possible data-leak and privacy-risk patterns before installation or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static pattern matching can miss issues or flag benign code as risky. <br>
Mitigation: Use results as preliminary triage and review the scanned code and report before relying on the assessment. <br>
Risk: Broad scans may inspect private files or sensitive directories. <br>
Mitigation: Run it against specific files, folders, or named skills and review reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/data-leak-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text security report with risk score and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static-analysis results are advisory and should be reviewed before sharing or relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
