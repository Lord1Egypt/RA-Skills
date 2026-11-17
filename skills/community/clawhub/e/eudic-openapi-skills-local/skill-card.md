## Description:

Provides OpenAPI guidance for using Eudic and related language assistant services to manage vocabulary books, words, notes, and English pronunciation scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink-kai](https://clawhub.ai/user/ink-kai)

### License/Terms of Use:

MIT-0

## Use Case:

Language learners and developers use this skill to operate Eudic vocabulary, note, and pronunciation evaluation workflows through an agent using documented API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Eudic API token that can access account data.

Mitigation: Use secure token handling and avoid sharing tokens in transcripts or logs.

Risk: The skill can create, rename, and delete vocabulary books, words, and notes.

Mitigation: Require clear user confirmation before delete or destructive update requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ink-kai/skills/eudic-openapi-skills-local)
- [Eudic OpenAPI Authorization](https://my.eudic.net/OpenAPI/Authorization)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples that require a user-provided Eudic API token.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
