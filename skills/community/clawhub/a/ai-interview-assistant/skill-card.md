## Description:

AI Interview Assistant guides users through resume profiling, optional job-description matching, a five-question technical interview loop, scoring feedback, and a final report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradise123-bot](https://clawhub.ai/user/paradise123-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical interview candidates use this skill to run structured LLM-focused mock interviews, compare a candidate profile with a target job description, receive per-question scoring feedback, and produce a practice report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use technical tags and interview answers to generate scoring feedback and may store a local profile when anonymous mode is not used.

Mitigation: Use anonymous mode or restrict profile storage when personal identification is not needed, and review host tool permissions before deployment.

Risk: Question material may be fetched from GitHub or other web sources, so availability and freshness can vary.

Mitigation: Review fetched question content and source links before relying on the exercise, and restrict network access if external retrieval is not acceptable.

Risk: The scoring model is practice-oriented and may not reflect a complete hiring evaluation.

Mitigation: Treat scores as interview preparation feedback and require human review for employment or promotion decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paradise123-bot/skills/ai-interview-assistant)
- [wdndev/llm_interview_note question source](https://github.com/wdndev/llm_interview_note)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown-style interview prompts, scoring feedback, JSON script outputs, and final reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a five-question interview flow with per-answer keyword and logic scoring; may include source URLs for GitHub-derived questions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
