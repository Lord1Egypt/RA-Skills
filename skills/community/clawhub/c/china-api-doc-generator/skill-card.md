## Description:

Generates Chinese-style API documentation for Chinese developer audiences, including REST API references, error-code tables, SDK examples, signature-authentication docs, changelogs, and migration guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to draft API documentation tailored for Chinese developer platforms, with detailed request and response tables, localized examples, error remediation, SDK snippets, and migration notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's signature-authentication template includes MD5 and app_secret guidance that may be inappropriate for production security designs.

Mitigation: Review or replace generated authentication guidance with an approved production signing scheme before publishing or implementing it.

Risk: Generated documentation may preserve defaults such as Beijing time or Chinese documentation conventions even when a project requires different locale, timezone, or platform standards.

Mitigation: Review generated examples, timestamps, rate limits, and terminology against the target API's actual regional and product requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/china-api-doc-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/lm203688)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with API reference tables, JSON examples, SDK code snippets, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Java, Python, Node.js, and Go SDK examples, Chinese error-code tables, signature-authentication documentation, changelog entries, and migration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
