## Description:

Extracts video details, descriptions, spoken transcripts, and concise copy from publicly accessible Douyin videos supplied by URL, share text, or aweme ID, and can check an existing job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to extract a Douyin video's available details, original description, and spoken transcript for review and content organization. They can submit a public video URL, share text, or aweme ID, then check an existing job until it completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted video information is sent to SocialDataX for processing.

Mitigation: Submit only video information you are comfortable sharing with SocialDataX.

Risk: The CLI commands use an unpinned package version that may change over time.

Mitigation: Review the package release before installation and use a pinned version when reproducibility matters.

Risk: The security scan was partial because some referenced paths had no matching bundled artifact.

Mitigation: Review the referenced material and package behavior before installation.

## Reference(s):

- [SocialDataX service and API key information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/douyin-copy-extract-v2)
- [Publisher profile](https://clawhub.ai/user/devinchen2014)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown transcript and copy-ready text, with JSON task status and result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only fields returned by the service; pending jobs are checked with the same job ID. Optional SRT file export is available when requested through the CLI.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
