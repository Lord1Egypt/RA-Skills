## Description:

Provides Chinese-language emoji meaning lookup, Chinese keyword emoji search, and simple text-to-emoji conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up emoji meanings, find emoji from Chinese keywords, and convert simple Chinese text phrases into emoji-enhanced text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation and command output are primarily Chinese, which may be unclear for users who do not read Chinese.

Mitigation: Confirm expected command behavior with sample inputs before relying on the output in a workflow.

Risk: The README includes promotional AISoBrand links even though the reviewed code does not contact those sites.

Mitigation: Review external links before visiting them and treat them separately from the local emoji helper behavior.

Risk: Text-to-emoji conversion performs simple keyword replacement and may change wording in ways the user did not intend.

Mitigation: Review converted text before publishing or using it in user-facing content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-emoji-tool)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit JSON when the command-line helper is run with its JSON option.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
