## Description:

Detects, blocks, and reports Child Sexual Abuse Material using AI-driven image, video, text, and behavior analysis with evidence preservation and NCMEC reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and trust-and-safety teams use this skill to integrate CSAM detection, content blocking, evidence preservation, and reporting workflows into platforms with user-generated content. Operational use requires legal, privacy, retention, access-control, and reviewer-safety procedures to be defined before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends an unreviewed npm package for a highly sensitive child-safety workflow.

Mitigation: Review the exact package source and dependency tree in an isolated environment, then pin versions and integrity before installation.

Risk: Automatic reporting, enforcement, related-account expansion, permanent bans, and indefinite retention can create legal, privacy, and due-process risk.

Mitigation: Keep those actions disabled until legal/privacy review defines reporting, notification, retention, appeal, and access-control procedures.

Risk: The skill handles highly sensitive user data and potential CSAM evidence.

Mitigation: Restrict access, use encryption and audit logging, and define evidence retention and reviewer-safety procedures before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/skills/csam-shield)
- [NCMEC CyberTipline](https://report.cybertip.org/)
- [FBI Internet Crime Complaint Center](https://www.ic3.gov/)
- [INHOPE](https://inhope.org/)
- [Internet Watch Foundation](https://www.iwf.org.uk/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and JavaScript examples plus shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration examples, API usage examples, operational guidance, troubleshooting notes, and legal and safety considerations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
