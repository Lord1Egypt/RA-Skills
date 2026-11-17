## Description:

Parses and validates Chinese bank card numbers offline, identifying likely issuer, card type, card network, card length, and Luhn checksum status for common Chinese bank BINs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, support teams, and developers use this skill to inspect a provided Chinese bank card number, validate its format, and return masked issuer, network, type, length, and checksum guidance without network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes bank card numbers supplied by the user.

Mitigation: Mask card numbers in responses, retaining only limited leading and trailing digits, and do not ask for CVV, PIN, passwords, or other payment secrets.

Risk: Luhn validation can confirm only checksum format, not whether an account exists or can be used.

Mitigation: State that a passing Luhn result is not proof of account validity and direct users to official bank channels for authoritative confirmation.

Risk: The embedded BIN list covers common Chinese banks and may miss or misclassify newer, regional, or uncommon card ranges.

Mitigation: Describe unknown BINs as not covered by the local database and recommend verification through official banking sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/china-bankcard)
- [Publisher Profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text analysis with masked card-number examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fully offline; should mask card numbers and avoid requesting CVV, PIN, passwords, or other payment secrets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
