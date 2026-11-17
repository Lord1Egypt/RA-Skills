## Description:

Cn Text Summary summarizes Chinese text locally without an API key and can extract keywords with optional jieba support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and external users can use this skill to produce concise summaries and keywords from Chinese articles, emails, research notes, product copy, and similar long-form text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential text supplied as a command-line argument may be exposed through shell history or process listings.

Mitigation: Use the skill for non-sensitive text, or wrap it with stdin or another protected input path for private documents.

Risk: The optional jieba dependency can affect keyword extraction behavior if installed without version control.

Mitigation: Pin and review the jieba package version before installing it in shared or production environments.

## Reference(s):

- [Cn Text Summary on ClawHub](https://clawhub.ai/freedompixels/skills/cn-text-summary)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object with original length, summary length, summary text, and keywords.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally; optional jieba support improves Chinese keyword extraction when installed.]

## Skill Version(s):

1.2.7 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
