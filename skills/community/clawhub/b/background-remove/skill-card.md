## Description:

Removes image backgrounds with AI and returns transparent PNG output for JPG, PNG, or WebP local files and remote URLs at one credit per image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alouhaou](https://clawhub.ai/user/alouhaou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove backgrounds from local or remote images through the verging.ai API and receive transparent PNG result links or downloaded files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote image URLs can target internal, access-controlled, localhost, cloud metadata, or intranet resources.

Mitigation: Use local files or known public, non-sensitive URLs; avoid internal network and access-controlled URLs.

Risk: Image contents are uploaded to a third-party service for processing.

Mitigation: Avoid sensitive images unless the user has reviewed the service terms and data handling expectations.

Risk: API credentials are required for job creation, polling, and credit checks.

Mitigation: Set VERGING_API_KEY through the environment and avoid exposing keys in shared logs, prompts, or repositories.

Risk: The release evidence recommends review and a pinned install source before deployment.

Mitigation: Review the skill before installing and prefer a pinned source for operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alouhaou/skills/background-remove)
- [verging.ai](https://verging.ai)
- [verging.ai API Docs](https://verging.ai/docs/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, API result URLs, and optional transparent PNG file download.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VERGING_API_KEY and curl; accepts JPG, PNG, or WebP input up to 10MB and consumes one credit per image.]

## Skill Version(s):

1.2.0 (source: evidence.release.version and skill.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
