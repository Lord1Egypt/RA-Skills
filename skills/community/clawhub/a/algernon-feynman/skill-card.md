## Description:

Runs a Feynman Technique study session for OpenAlgernon that prompts users to teach concepts in their own words, identifies gaps with Socratic follow-ups, and reveals reference answers only after repeated unsuccessful attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run guided OpenAlgernon study sessions that test understanding of material through self-explanation, Socratic follow-up questions, and concise session summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe database and shell command patterns could mishandle untrusted material names or card content.

Mitigation: Use trusted material names and card content, validate slugs, prefer parameterized SQLite queries, and review proposed commands before use.

Risk: Study summaries may be saved locally or exported to Notion without clear per-run consent.

Mitigation: Ask before sending summaries to Notion or saving learning-history notes, and write summaries safely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antoniovfranco/skills/algernon-feynman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with prompts, evaluation guidance, summary text, and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 3-5 concept study flow, per-concept feedback, optional Notion export content, and optional local learning-history notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
