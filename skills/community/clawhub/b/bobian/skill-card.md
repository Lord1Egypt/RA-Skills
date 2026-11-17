## Description:

分析普通中文博文呈现出的 AI 写作风格和论证结构，并生成最多 140 个英文等价字符的支持或反对评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gordonlu](https://clawhub.ai/user/gordonlu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to analyze Chinese social or blog posts for AI-style writing signals, argument structure, and grounded support or opposition comments. It is intended for style analysis and concise comment drafting, not authorship attribution or automated engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompts such as article analysis or support/opposition comments may activate the skill outside the user's intended workflow.

Mitigation: Invoke it when the user specifically wants AI-style writing analysis or short grounded comments for Chinese posts.

Risk: Readers may mistake an AI-style score for proof of authorship or proof that generative AI was used.

Mitigation: Present the score only as a measure of visible writing-style signals and avoid using it for identity claims, discipline, legal conclusions, or attribution.

Risk: Generated stance comments could be misused for political, high-risk, harassing, or bulk engagement scenarios.

Mitigation: Apply the skill's content eligibility checks, refuse political and high-risk content, and generate only one grounded comment without auto-posting or multi-account behavior.

Risk: The skill does not fetch linked content, so analyzing a link alone could miss the actual text.

Mitigation: Require the user to provide the post text directly and analyze only the supplied text.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with concise Chinese comments and length accounting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comments are capped at 140 English-equivalent characters; outputs may include AI-style analysis, argument structure, support comments, opposition comments, or refusal text.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
