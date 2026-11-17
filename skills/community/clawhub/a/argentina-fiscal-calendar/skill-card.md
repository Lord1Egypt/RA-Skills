## Description:

Provides an offline Argentina fiscal calendar assistant for ARCA tax and social-security deadlines across PyMEs, self-employed workers, monotributistas, and employers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[centriqs](https://clawhub.ai/user/centriqs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators in Argentina use this skill to ask an agent about recurring ARCA fiscal deadlines, CUIT-dependent due dates, holiday shifts, and reminder-style summaries. It is an offline reference aid and should not be treated as legal tax advice.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: Fiscal deadlines or holiday-shift guidance may be incomplete, outdated, or not legally binding.

Mitigation: Treat outputs as reminders and verify legally binding due dates directly with ARCA or a qualified accountant before acting.

Risk: Local personalization could expose sensitive taxpayer, banking, credential, or third-party personal data if users overfill configuration files.

Mitigation: Store only the minimum local settings needed for reminders, and avoid entering full CUITs, credentials, banking details, or third-party personal data.

Risk: Manual installation from a moving source branch can introduce unreviewed changes.

Mitigation: Pin a specific reviewed commit or install through the reviewed ClawHub release.

## Reference(s):

- [Argentina Fiscal Calendar (ARCA) on ClawHub](https://clawhub.ai/centriqs/skills/argentina-fiscal-calendar)
- [Centriqs Publisher Homepage](https://centriqs.io)
- [ARCA Official Due Dates](https://arca.gob.ar/vencimientos)
- [ARCA Monotributo](https://arca.gob.ar/monotributo)
- [Argentina National Holidays](https://argentina.gob.ar/feriados)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with fiscal-calendar summaries, tables, and inline shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline reminder and reference aid; no external API calls or credential collection are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
