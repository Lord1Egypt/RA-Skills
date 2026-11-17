## Description:

Extracts transcripts from batches of Douyin videos and saves each result as a Markdown file with an index; optional modes include on-screen text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and analysts use it to organize a batch of Douyin videos into per-video transcripts and an index for content research, topic libraries, and drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch script may submit requests without an extraction depth, which can result in higher-cost full extraction instead of speech-only processing.

Mitigation: Set --depth script for speech-only extraction and check the service's credit behavior before processing a batch.

Risk: The security scan has partial coverage because some referenced local paths were missing from the supplied artifact.

Mitigation: Confirm referenced files are present and review them before running the skill.

## Reference(s):

- [LinkDigest Douyin batch extraction](https://linkdigest.dev/zh/douyin-wenan-piliang-tiqu?ref=skill-douyin-batch-to-text)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Per-video Markdown transcripts and an index.md summary table]

**Output Parameters:** [Batch of video links or share text; extraction depth can be script, transcript, or full]

**Other Properties Related to Output:** [Writes one Markdown file per successfully read video and lists unreadable items in the index.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
