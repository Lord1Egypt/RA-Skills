## Description:

Generates a structured HTML futures morning brief from a user-provided page or the default SteelX2 source, covering overview, highlights, market snapshots, macro news, and industry news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirenming](https://clawhub.ai/user/lirenming)

### License/Terms of Use:

MIT-0

## Use Case:

Futures researchers, black-industry analysts, steel trading teams, and financial news editors use this skill to turn current market and industry-news content into a daily HTML morning brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include branded or promotional footer/link content and third-party remote resources.

Mitigation: Review the generated HTML before sharing or opening it broadly, and remove or neutralize external links and remote images when they are not needed.

Risk: The workflow can fetch a default web source, write an HTML file to the desktop, and open it for screenshot verification.

Mitigation: Run the skill only with trusted URLs or the accepted default source, and review the generated local file before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lirenming/skills/futures-morning-brief)
- [HTML Output Format](references/output-format.md)
- [HTML Template Asset](assets/template.html)
- [Default SteelX2 Source](https://www.steelx2.com/)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Shell commands, Guidance]

**Output Format:** [HTML report file with concise agent status or verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report follows fixed sections for overview, three highlights, market snapshots, ten macro news items, six industry news items, and a footer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
