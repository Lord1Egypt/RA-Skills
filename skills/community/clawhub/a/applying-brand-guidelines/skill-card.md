## Description:

This skill applies consistent corporate branding and styling to generated documents, including colors, fonts, layouts, and messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external communications teams, developers, and document-producing agents use this skill to apply Acme Corporation brand colors, typography, templates, logo placement, tone guidance, and validation checks to presentations, spreadsheets, PDFs, and related content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may apply Acme-specific branding to documents where Acme branding is not appropriate.

Mitigation: Install or invoke it only in workflows where Acme branding is required, especially for external communications.

Risk: Default US currency and date conventions may be unsuitable for other locales.

Mitigation: Review region-specific documents and override date, currency, and formatting conventions when local requirements differ.

Risk: Broad guidance for any document may be too strict for internal drafts, special projects, or non-Acme work.

Mitigation: Apply documented exceptions and human review before finalizing documents outside the normal Acme external-communications use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/applying-brand-guidelines)
- [Brand Guidelines Reference](artifact/REFERENCE.md)
- [Brand reference image](artifact/CCB排名.png)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with optional Python-derived document configuration dictionaries and validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in Acme-specific brand standards and may include checks for colors, fonts, tone, logo usage, document layout, number formatting, and locale-sensitive date or currency conventions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
