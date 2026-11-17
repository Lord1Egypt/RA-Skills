## Description:

Data Leak Detector scans skills, files, or folders for potential data leaks, privacy risks, and suspicious behavior by detecting network calls, file access, process spawning, and environment variable access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to perform static checks on agent skills, files, or folders before installation or deployment. It produces a risk-oriented report that highlights possible network, file, process, and environment-variable access patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads target folders and files during static analysis, so sensitive content in scanned paths may be exposed to the agent performing the scan.

Mitigation: Run it only on folders you are comfortable letting the agent inspect, or isolate and minimize the scan target before use.

Risk: The release evidence notes an avoidable unused watchdog dependency.

Mitigation: Review, remove, or decline the unused dependency before installation, or install the skill in an isolated environment.

## Reference(s):

- [Data Leak Detector on ClawHub](https://clawhub.ai/tobewin/skills/data-leak-detector)
- [ToBeWin publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text security report with risk scores, category breakdowns, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static-analysis output only; no runtime monitoring or external API calls are described.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
