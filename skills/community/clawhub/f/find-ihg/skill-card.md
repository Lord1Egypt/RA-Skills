## Description:

Finds IHG reward-night and promotional options in the Jiangsu-Zhejiang-Shanghai region, with filters for brand, distance, points bands, and executive lounge availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddylhb](https://clawhub.ai/user/eddylhb)

### License/Terms of Use:

MIT-0

## Use Case:

Travel-focused agents and users use this skill to surface reward-night options and promotions for IHG hotels in Shanghai, Jiangsu, and Zhejiang, then rank options by distance, brand preference, points value, and lounge availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The main executable and hotel data referenced by the skill are not present in the reviewed package, so runtime behavior cannot be fully assessed from the submitted artifact alone.

Mitigation: Review the external query.py and hotels.json implementation before installation, or require the publisher to bundle those files in the skill package.

Risk: The rollback script can replace live skill and script files from backup directories without strong path validation or integrity checks.

Mitigation: Use rollback only with trusted backup labels and backup locations, and add path validation plus checksum verification before restoring files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddylhb/skills/find-ihg)
- [CHANGELOG.md](artifact/references/CHANGELOG.md)
- [audit_report.json](artifact/references/audit_report.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted natural-language recommendations and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked hotel recommendations, points-versus-cash value analysis, filter context, and promotional guidance when available.]

## Skill Version(s):

2.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
