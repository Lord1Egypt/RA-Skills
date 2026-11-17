## Description:

English Word Coach helps users analyze and collect English vocabulary, maintain local Markdown vocabulary files, and run spaced-repetition daily review sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hushenglang](https://clawhub.ai/user/hushenglang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to get Chinese-language explanations and professional-context examples for English words, save vocabulary progress, and review due words through a local spaced-repetition workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores vocabulary history and review progress in local Markdown files under the current working directory.

Mitigation: Run it only in a workspace where writing memory/ENGLISH_WORDS.md and daily review files is acceptable, and avoid repositories or synced folders that should not contain vocabulary history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hushenglang/skills/english-word-coach)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with vocabulary tables and review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory/ENGLISH_WORDS.md and memory/DAILY_REVIEW_YYYYMMDD.md files in the current working directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
