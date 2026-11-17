## Description:

This skill guides an agent through publishing long-form Xiaohongshu posts in the web creator platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to have an agent enter title and body content, apply formatting, choose a template, and publish long-form Xiaohongshu notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real Xiaohongshu publishing flow and may click the publish button.

Mitigation: Require explicit final user confirmation before the agent clicks publish.

Risk: Drafting-style requests may activate the skill even when the user does not intend to publish.

Mitigation: Use the skill only when the user clearly asks to publish to Xiaohongshu, and confirm intent before starting the publish flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blockcloud/skills/cpskilltest123456)
- [Xiaohongshu Creator Publishing Page](https://creator.xiaohongshu.com/publish/publish?source=official)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions for browser interaction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish real Xiaohongshu content when followed in an authenticated browser session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
