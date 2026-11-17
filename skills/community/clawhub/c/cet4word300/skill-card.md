## Description:

Randomly generates one or more words from a curated database of 300 must-know College English Test Band 4 (CET-4) vocabulary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfeng1982](https://clawhub.ai/user/zfeng1982)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and study agents use this skill to retrieve random CET-4 vocabulary items with pronunciation, Chinese meaning, and bilingual example sentences for English exam practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares shell availability even though the visible behavior is limited to reading the bundled word list.

Mitigation: Install in environments where shell access is acceptable, and review future versions for a narrower or better documented runtime requirement.

Risk: The requested vocabulary count is not documented with a maximum.

Mitigation: Use a reasonable word count for study sessions and apply local limits if deploying the skill in a shared agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zfeng1982/skills/cet4word300)
- [Publisher profile](https://clawhub.ai/user/zfeng1982)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text vocabulary entries with word, phonetic spelling, meaning, English sentence, and Chinese sentence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The number of returned entries is derived from the user's requested count.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
