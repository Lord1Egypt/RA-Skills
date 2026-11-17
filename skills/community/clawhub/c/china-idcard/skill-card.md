## Description:

Parses and validates Chinese mainland ID card numbers offline, extracting province, city, district, birthdate, gender, age, and checksum status while providing format guidance for related permit and passport numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and support staff can use the skill to parse or validate Chinese mainland ID card numbers, extract non-sensitive attributes, and explain why a number is invalid. It should be used only when the user is authorized to process the ID number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal personal attributes encoded in an ID number.

Mitigation: Use it only for ID numbers the user is authorized to process and keep outputs redacted.

Risk: Checksum validation can be mistaken for proof that an ID is real or belongs to a person.

Mitigation: State that validation only confirms internal format consistency and does not verify issuance or identity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-idcard)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with redacted ID-number displays and validation explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline guidance only; no API keys, network calls, persistence, or code execution required.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
