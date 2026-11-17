## Description:

Chinese Sensitive Words helps agents check Chinese marketing, social, live-streaming, and product copy for sensitive or prohibited terms and suggest safer replacements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccpan](https://clawhub.ai/user/cccpan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and marketing teams use this skill through an agent to check Chinese copy for platform-sensitive terms, compliance risks, and replacement suggestions before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked text is sent to the configured API service, which may include the default hosted endpoint.

Mitigation: Avoid submitting confidential, personal, or regulated text unless the service operator is trusted; configure SENSITIVE_WORDS_API_BASE to a trusted private deployment when needed.

Risk: Free usage is quota-limited and may block checks after the monthly allowance is exhausted.

Mitigation: Configure SENSITIVE_WORDS_TOKEN for normal operational use and handle rate-limit failures in the surrounding workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cccpan/skills/chinese-sensitive-words)
- [Publisher profile](https://clawhub.ai/user/cccpan)
- [Token request issues](https://github.com/CCCpan/chinese-sensitive-words/issues)
- [Default API endpoint](https://www.xdhdancer.top/api8888)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted terminal output with risk summaries, detected terms, categories, and replacement suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; SENSITIVE_WORDS_TOKEN enables unlimited use, and SENSITIVE_WORDS_API_BASE can point to a trusted private service.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
