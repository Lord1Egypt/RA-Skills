## Description:

Analyzes image and video ad creatives to score ad quality, visual and messaging effectiveness, engagement potential, and cross-creative patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baitoxkevin](https://clawhub.ai/user/baitoxkevin)

### License/Terms of Use:


## Use Case:

Marketing teams, creative strategists, and agents use this skill to analyze folders of competitor or reference ad images, videos, and transcripts. It produces per-creative scoring and a summary of hooks, emotional appeals, CTA patterns, top performers, and improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads filenames, ad media, transcripts, and optional metadata from a user-provided directory.

Mitigation: Run it only on folders intended for ad review and avoid broad personal or business directories unrelated to the analysis task.

Risk: Creative quality scores and recommendations may be subjective and may not predict actual campaign performance.

Mitigation: Review recommendations before use and compare them with platform performance data, brand requirements, and campaign goals.

## Reference(s):

- [Ad Creative Analysis Framework](references/analysis-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/baitoxkevin/skills/ad-creative-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [JSON array with per-creative objects and a summary object; explanatory guidance may be returned in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes filenames, creative type, aspect ratio, platform fit, scores, extracted message elements, hook and CTA classifications, unreadable-file status, and cross-creative recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
