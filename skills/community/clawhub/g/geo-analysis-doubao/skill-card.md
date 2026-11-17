## Description:

Evaluates whether brand, product, or article copy is easy for Doubao to understand, quote, and recommend, then returns a concise Chinese GEO audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams, marketers, content creators, and agent operators use this skill to audit supplied Chinese brand or product content for Doubao-oriented GEO readiness. It scores the content across clarity, structure, quoteability, and recommendation triggers, then suggests concise improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sparse or vague source text can lead to low-confidence GEO scores or incomplete diagnosis.

Mitigation: Provide complete brand, product, audience, scenario, and FAQ content, and review any "insufficient information" findings before acting on the report.

Risk: The skill is oriented to Chinese Doubao GEO analysis and may not fit multilingual or non-Doubao review needs without adaptation.

Mitigation: Confirm the target language and model context before use, and adapt prompts or report criteria when evaluating other generative engines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljseeking/skills/geo-analysis-doubao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compact mode by default; includes score, diagnosis, recommendations, FAQ suggestions, and a final conclusion based only on user-provided content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
