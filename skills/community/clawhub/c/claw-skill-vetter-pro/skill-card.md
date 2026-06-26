## Description: <br>
Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources, with checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to vet AI agent skills before installation by checking source trust, file contents, permission scope, red flags, and risk level. It produces a standardized report that supports installation decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The vetting report is guidance and may miss malicious or misleading behavior in a skill. <br>
Mitigation: Review all skill files and scan results before installation, and treat the report as a decision aid rather than a guarantee. <br>
Risk: Source checks may require network access to external repositories. <br>
Mitigation: Allow network access only for intended lookups and avoid exposing credentials or private source unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwang-wh/claw-skill-vetter-pro) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown report with checklist sections and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source, author, version, metrics, red flags, permissions, risk level, verdict, and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
