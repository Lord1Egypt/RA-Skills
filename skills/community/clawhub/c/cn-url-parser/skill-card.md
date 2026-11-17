## Description:

Cn Url Parser is a Chinese-language developer utility for parsing URLs into components and query parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect URL structure and extract query parameters with a local Python helper. It is most useful for debugging web links and checking parsed URL components during development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes encode, decode, build, and batch parsing features that are not implemented in the included script.

Mitigation: Use the current release for basic URL parsing only unless the missing behaviors are implemented and tested.

Risk: The skill is a Chinese-language developer utility, which may make usage details harder to review for non-Chinese-speaking teams.

Mitigation: Have a Chinese-capable reviewer confirm the intended commands and outputs before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-url-parser)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the included parser script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Python standard library and does not require external services or API keys.]

## Skill Version(s):

1.2.7 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
