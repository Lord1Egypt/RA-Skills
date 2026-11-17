## Description:

Transforms website URLs into six-slide TikTok and Instagram carousel content, publishes posts through Upload-Post, and uses analytics to improve future carousels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouqkt](https://clawhub.ai/user/zhouqkt)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this agent to turn a target website into vertical carousel posts for TikTok and Instagram, publish them, and fold performance analytics into later content decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish public TikTok and Instagram posts without an approval step.

Mitigation: Require explicit human approval before publishing or granting accounts public posting authority.

Risk: The workflow sends website content and generated media through third-party APIs.

Mitigation: Use only approved URLs, accounts, and API keys, and review data-sharing expectations before execution.

Risk: The workflow can create recurring schedules for future posts.

Mitigation: Disable or review any recurring schedule until the owner confirms cadence, account scope, and approval requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouqkt/skills/agency-carousel-growth-engine)
- [Publisher profile](https://clawhub.ai/user/zhouqkt)
- [Upload-Post documentation](https://docs.upload-post.com)
- [Google AI Studio API key setup](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, JSON artifacts, image files, captions, and publishing status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces six JPG carousel slides, slide prompts, captions, publishing metadata, analytics summaries, and learning records when the workflow runs successfully.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
