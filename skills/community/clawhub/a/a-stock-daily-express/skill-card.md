## Description:

Automatically gathers China A-share market data, ranks daily movers and sectors, and generates ready-to-publish Chinese social posts for Xiaohongshu, WeChat, and Moments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudagebil11-jpg](https://clawhub.ai/user/rudagebil11-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, analysts, and agent users use this skill to turn daily China A-share market data into concise Chinese social-media market summaries. The generated content is intended for review and editing before publication, especially where readers may treat it as financial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves market data through Python and Akshare, so execution depends on external network data sources and the local Python environment.

Mitigation: Run it only in an environment approved for Akshare data retrieval and verify that required dependencies are installed from reviewed versions.

Risk: Generated summaries may be inaccurate, stale, or interpreted by readers as investment advice.

Mitigation: Review, fact-check, and edit generated market summaries before posting, and add appropriate financial-content disclaimers where needed.

Risk: Unpinned dependencies can introduce supply-chain or behavior changes over time.

Mitigation: Pin and review dependency versions when stronger supply-chain control is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Markdown or HTML social-media report text with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates platform-specific Chinese copy for Xiaohongshu, WeChat, or Moments using externally retrieved market data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
