## Description:

Generate 7-day or 30-day social media content calendars for any niche. Outputs structured JSON + human-readable schedule with hooks, body copy, CTAs, and hashtags per post. Free tier: 7-day calendar. Premium: 30-day, multi-platform, A/B variants, CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, creators, and business operators use this skill to generate ready-to-review social media calendars for a chosen niche, audience, platform, and tone. It can produce short sample calendars, 7-day calendars, 30-day calendars, multi-platform variants, JSON, human-readable schedules, and CSV exports for scheduler workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing prompts may be sent to Anthropic or a local LLM, depending on the selected backend.

Mitigation: Avoid entering confidential customer details, business secrets, or sensitive campaign information in niche, audience, or prompt fields.

Risk: CSV exports can carry spreadsheet and scheduler workflow risk if generated content is opened or imported without review.

Mitigation: Review and sanitize CSV output before opening it in spreadsheet tools or importing it into Buffer, Hootsuite, Notion, or another scheduler.

Risk: Generated marketing copy can be inaccurate, noncompliant, or unsuitable for regulated topics such as mortgage, real estate, healthcare, or crypto.

Mitigation: Require human review before posting and use the compliance-only check as a first-pass screen, not as final compliance approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/dfw-content-calendar)
- [Skill homepage](https://github.com/dfw-area-house-hunt/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, JSON, CSV]

**Output Format:** [Human-readable schedule, structured JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated calendars to an output file when requested; supports 7-day or 30-day calendars, platform selection, tone selection, A/B hook variants, and compliance-only checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
