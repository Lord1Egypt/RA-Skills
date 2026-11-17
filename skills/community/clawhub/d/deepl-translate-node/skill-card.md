## Description:

Translate via DeepL when explicitly requested or when uncertainty could make a translation error materially consequential; confident everyday text can be translated directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbenben](https://clawhub.ai/user/rockbenben)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents can translate text through DeepL when requested or when uncertain wording has material consequences, while translating confident everyday prose directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence, but coverage is partial and the skill has no declared tool scope despite detected environment and network capabilities.

Mitigation: Review the executable and its network access before use; send only content authorized for external processing and keep API credentials out of translated text and command output.

## Reference(s):

- [DeepL supported languages](https://developers.deepl.com/docs/resources/supported-languages)
- [Skill homepage](https://github.com/rockbenben/aishort-skills/tree/main/skills/deepl-translate-node)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text translation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves paragraph breaks; translation should be checked against its source context.]

## Skill Version(s):

1.1.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
