## Description:

Count words, characters, sentences, paragraphs, and reading time for any text using AceToolz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acetoolz](https://clawhub.ai/user/acetoolz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send text to AceToolz for word, character, sentence, paragraph, and reading-time statistics, then present a concise Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for counting is sent to an external AceToolz API without clear consent, privacy, or retention details in the artifact.

Mitigation: Use the skill only for non-sensitive text unless the publisher provides explicit privacy and retention terms or a local-processing option.

Risk: The external API may be rate-limited, reject long text, or be temporarily unreachable.

Mitigation: Surface API errors to the user, ask them to retry after rate limits, and direct them to the AceToolz website when the API is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/acetoolz/skills/acetoolz-word-counter)
- [AceToolz Publisher Profile](https://clawhub.ai/user/acetoolz)
- [AceToolz Word Counter](https://www.acetoolz.com/text/tools/word-counter)
- [AceToolz Word Counter API](https://www.acetoolz.com/api/openclaw/word-counter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown summary with optional PowerShell or curl command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns word, character, sentence, paragraph, and reading-time counts; API errors may include rate-limit, length, or availability messages.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
