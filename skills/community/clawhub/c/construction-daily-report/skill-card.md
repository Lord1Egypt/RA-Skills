## Description:

Generate a structured daily site progress report from unstructured input such as voice transcription, rough notes, or conversational messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitevity](https://clawhub.ai/user/nitevity)

### License/Terms of Use:

MIT-0

## Use Case:

Construction site engineers use this skill to turn rough daily site notes, voice transcriptions, or messages into a structured Daily Site Progress Report. It also prompts for missing critical fields such as weather, workforce count, work completed, safety observations, and delays before finalizing the report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on generic daily-report wording outside a construction context.

Mitigation: Apply construction-context judgment before activation and route non-construction report requests to a more appropriate skill.

Risk: Generated reports may include unwanted branding or an external-domain footer.

Mitigation: Review generated reports before filing and remove any branding or external links that are not appropriate for the project record.

Risk: Daily reports assembled from rough notes may contain missing or misunderstood site details.

Mitigation: Answer the skill's follow-up questions for critical fields and review the final report for accuracy before filing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nitevity/skills/construction-daily-report)
- [Publisher profile](https://clawhub.ai/user/nitevity)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily report with tables, section headings, follow-up questions, and review prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a filing-ready daily construction site report from a single stream of user-provided notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
