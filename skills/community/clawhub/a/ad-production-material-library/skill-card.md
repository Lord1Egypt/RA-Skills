## Description:

素材库管理技能 - 提供素材的存储、检索、版本管理

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising production teams and agents use this skill to track generated materials, search by tags, type, and format, create versions, archive items, and report library statistics in the OpenClaw command interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Material records are held in memory, so search, version, archive, and statistics results may not survive runtime restarts.

Mitigation: Use this release for transient library state unless it is connected to durable storage and reviewed for the intended retention requirements.

Risk: The upload command is not fully functional through the current command interface and reports that extra OpenClaw file integration is required.

Mitigation: Validate the file ingestion path before relying on the skill for production asset uploads.

Risk: Development dependency ranges are not pinned, which may reduce build reproducibility.

Mitigation: Pin or lock development dependencies before using repeatable builds as a release requirement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeyeshield/skills/ad-production-material-library)

## Skill Output:

**Output Type(s):** [text, structured data]

**Output Format:** [JSON-like command responses with material records, status flags, errors, and statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records are in-memory; the upload command currently reports that file upload needs additional OpenClaw integration.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
