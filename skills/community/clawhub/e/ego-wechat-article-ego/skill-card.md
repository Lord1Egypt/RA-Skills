## Description:

Save one WeChat Official Account article draft from Markdown through the visible editor in Ego Lite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content editors use this skill to turn a Markdown article into one WeChat Official Account draft through an already signed-in Ego Lite session. Saving requires `--yes`; the skill does not publish or mass-send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial ClawScan assessment marks the release suspicious due to a possible mismatch between its stated article-drafting purpose and behavior it could verify; the evidence is incomplete.

Mitigation: Review the skill's declared purpose and permissions before installing.

Risk: Security guidance flags possible loss of unsaved edits during the workflow.

Mitigation: Save or otherwise preserve existing editor work before running the skill.

Risk: Security guidance raises a concern about screenshots being written to disk; the documented `--screenshot-dir` option can save draft and preview screenshots after a confirmed save.

Mitigation: Review the screenshot destination and restrict access to any screenshots created.

## Reference(s):

- [Editor workflow](artifact/references/editor.md)
- [Inputs and options](artifact/references/inputs.md)
- [Login guidance](artifact/references/login.md)
- [Typography and paste behavior](artifact/references/typography.md)
- [WeChat Official Account console](https://mp.weixin.qq.com/)
- [ClawHub release page](https://clawhub.ai/terryso/skills/ego-wechat-article-ego)

## Skill Output:

**Output Type(s):** [Markdown article content, WeChat Official Account draft, JSON status summary]

**Output Format:** [A single saved article draft in the WeChat Official Account console; optional JSON status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saving requires `--yes`; the skill does not publish or mass-send.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
