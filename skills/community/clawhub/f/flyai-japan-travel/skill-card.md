## Description:

Your complete Japan travel companion for Japan trip planning, including flights, hotels, shrine and temple visits, cherry blossom spots, ramen guides, JR Pass information, visa requirements, attraction tickets, travel insurance, car rental, and itinerary planning powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to answer Japan-specific travel questions and assemble day-by-day Japan itineraries with flights, hotels, attractions, visa information, and booking-oriented recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global FlyAI CLI, including a sudo fallback.

Mitigation: Review the CLI before use, install a pinned approved version manually, avoid sudo, and do not allow automatic package installation in managed agent environments.

Risk: Trip details may be sent to FlyAI or Fliggy while retrieving live travel data and booking-oriented recommendations.

Mitigation: Inform users before live searches, avoid sending unnecessary sensitive personal details, and apply the organization's normal data-handling rules for travel queries.

Risk: The skill records raw user queries in background logs.

Mitigation: Minimize, redact, or disable logging of sensitive trip details where possible, and retain logs only as long as needed for observability and debugging.

Risk: Recommendations may be limited to FlyAI-bookable options.

Mitigation: Disclose booking-source limitations and treat results as booking-oriented options rather than exhaustive travel advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/flyai-japan-travel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, day-by-day itinerary sections, inline links, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking links, route summaries, travel tips, and fallback warnings when live travel data is unavailable.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
