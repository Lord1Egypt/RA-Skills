## Description:

事实核查与辟谣工具。当用户提供链接/图片/视频/文字要求事实核查时触发。覆盖两类场景：自查信息真伪，或核查别人分享的内容并生成回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tino-chen](https://clawhub.ai/user/tino-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check claims from links, screenshots, videos, or pasted text and produce a structured fact-check report. When social context is present, it also drafts a reply that communicates corrections in a chosen tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local browser may be launched against user-provided URLs, and the security summary flags under-scoped SSRF protections.

Mitigation: Avoid using the skill on untrusted links in cloud, corporate, or private-network environments unless network egress blocks metadata services and internal or private addresses.

Risk: The security summary flags covert or evasive persuasion patterns in the social reply guidance.

Mitigation: Review generated replies for transparency and prefer direct corrections that do not hide known falsehoods or manipulate the recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tino-chen/skills/debunk)
- [Workflow guide](https://tino-chen.github.io/notes/workflows/debunk.html)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown fact-check report plus plain-text reply templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cited sources for each checked claim; social replies are typically 200-400 Chinese characters.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
