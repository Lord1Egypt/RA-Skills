## Description:

Generate secure passwords via the AceToolz API, with passwords generated and returned in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acetoolz](https://clawhub.ai/user/acetoolz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate random passwords with requested length and character-type options. The skill calls the AceToolz API and returns the generated password with a short summary of the selected character settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords are created through a third-party API, so password material may be handled outside the user's local environment.

Mitigation: Use the skill only when the user accepts AceToolz handling password generation; prefer local generation for important accounts or highly sensitive credentials.

Risk: The skill executes outbound shell and network commands to request passwords from the AceToolz service.

Mitigation: Review the command target and request parameters before execution, and do not use the skill where outbound network calls are disallowed.

## Reference(s):

- [AceToolz Password Generator Skill Page](https://clawhub.ai/acetoolz/skills/acetoolz-password)
- [AceToolz Password Generator Homepage](https://www.acetoolz.com/generate/tools/password-generator)
- [AceToolz Publisher Profile](https://clawhub.ai/user/acetoolz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown text with an inline generated password and character-setting summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Password length and character classes depend on the user's requested options and API response.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
