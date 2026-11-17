## Description:

Generates a daily technology briefing focused on industry news, with fixed OpenClaw coverage and ClawHub items gathered through the CLI first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce a source-grounded daily technology briefing or podcast outline covering Elon Musk, Tesla, xAI, major AI and technology news, OpenClaw updates, and ClawHub skill discoveries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current news research can include stale, unverifiable, or misleading items if source checks are skipped.

Mitigation: Require original or authoritative source links for each item and omit claims that cannot be confirmed.

Risk: Automated cron use may execute a caller-specified briefing or podcast script outside the skill's Markdown-only behavior.

Mitigation: Review the caller-specified script separately before allowing scheduled execution.

Risk: ClawHub coverage may be incomplete when the ClawHub CLI is unavailable.

Mitigation: Clearly disclose the fallback reason in the generated briefing when CLI access is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/daily-tech-brief)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown briefing with sourced news items and operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is Chinese and is structured for daily briefing or podcast preparation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
