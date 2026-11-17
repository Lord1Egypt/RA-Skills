## Description:

Generates a product-specific urgency calendar and weekly pool of honest sales urgency reasons by combining a structured business brief, real niche dates researched through Tavily/Composio, and the FÓRMULA 100K urgency framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, founders, educators, and operators use this skill to plan honest urgency campaigns for a product, program, service, or community. The skill gathers a brief, researches relevant seasonal and commercial dates, and produces monthly urgency themes plus reusable weekly urgency reasons grounded in real assets or verified events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Excel files from web results and user-provided business text, which may include hidden spreadsheet formulas.

Mitigation: Treat generated workbooks as untrusted until spreadsheet-writing code escapes formula-like cell values; review the XLSX before sharing or opening in a privileged environment.

Risk: The skill relies on an external f100k-puente bridge skill that is referenced but not bundled in this artifact.

Mitigation: Review and install the expected bridge skill before relying on this package, and confirm that its tool and path translations match the current agent environment.

Risk: Tavily/Composio searches may expose product brief details or local business context used to find niche dates.

Mitigation: Minimize sensitive brief content, verify Tavily/Composio access and data handling expectations, and avoid including private customer or financial data in search queries.

Risk: Seasonal or commercial dates found through web search may be weak, outdated, or unverifiable.

Mitigation: Keep the skill's verification markings for uncertain dates and confirm sources before using the generated calendar in a live sales campaign.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/calendarizador-urgencias-formula100k)
- [Anatomia de la urgencia](references/anatomia-urgencia.md)
- [Pool semanal templates](references/pool-semanal-templates.md)
- [Ejemplos de briefs rellenos](references/ejemplos-briefs-rellenos.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report, JSON intermediate data, and optionally an XLSX workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The XLSX workbook requires openpyxl; when unavailable, the skill falls back to Markdown and JSON outputs. Web-date research requires Tavily/Composio access.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
