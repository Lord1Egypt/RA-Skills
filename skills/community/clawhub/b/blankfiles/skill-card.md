## Description:

Use blankfiles.com as a binary test-file gateway: discover formats, filter by type/category, and return direct download URLs from the public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seblavoie](https://clawhub.ai/user/seblavoie)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to find real downloadable blank binary files for upload, parser, and file-handling tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns external download URLs for blank test files.

Mitigation: Treat returned URLs as external downloads and verify availability through the documented API before relying on them.

Risk: The artifact includes maintainer publishing commands as reference material.

Mitigation: Do not run publishing commands unless intentionally managing a release and after verifying the ClawHub CLI source and version.

## Reference(s):

- [Blank Files](https://blankfiles.com)
- [Blank Files API Reference](references/endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/seblavoie/skills/blankfiles)
- [Publisher Profile](https://clawhub.ai/user/seblavoie)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with direct download URLs and concise file metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses typically include format, category, download_url, and brief testing notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
