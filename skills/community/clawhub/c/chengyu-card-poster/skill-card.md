## Description:

Generates a Xiaohongshu-ready Chinese idiom card caption from an idiom name, including a title, parent-friendly explanatory content, an interaction question, and required tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiderzhcl](https://clawhub.ai/user/spiderzhcl)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, parents, and education-oriented social media operators use this skill to draft Chinese idiom posts for Xiaohongshu. It helps turn a provided idiom into a publishable Markdown caption with a varied title, concise extra explanation, and an open-ended discussion prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a local Markdown draft and may be invoked accidentally by broad Chinese idiom-related triggers.

Mitigation: Confirm the requested idiom and output filename before saving when workspace clutter or accidental invocation matters.

Risk: Generated idiom explanations and exam guidance may be inaccurate if the model supplies unsupported cultural or educational details.

Mitigation: Review the caption for factual accuracy before publishing or using it with children.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/spiderzhcl/skills-spiderzhcl/tree/master/chengyu-card-poster)
- [ClawHub skill page](https://clawhub.ai/spiderzhcl/skills/chengyu-card-poster)
- [Publisher profile](https://clawhub.ai/user/spiderzhcl)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown file containing a Xiaohongshu caption draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local draft named output/xhs-{idiom}.md and presents it for review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
