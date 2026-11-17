## Description:

Search Google Flights for current flight prices, schedules, cabin comparisons, and booking-provider links using browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillhq-ai](https://clawhub.ai/user/skillhq-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search Google Flights for airfare, schedules, cabin price deltas, and booking-provider links. The skill supports comparison and handoff workflows, but does not complete purchases or enter personal or payment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight searches are sent to Google Flights, and booking links may lead to third-party airline or OTA sites with separate privacy and payment practices.

Mitigation: Tell users when third-party services are involved, present links as handoffs, and do not complete purchases or enter personal or payment data.

Risk: The skill depends on browser automation against a live web interface, so consent banners, CAPTCHA, locale differences, or UI changes can block or alter results.

Mitigation: Use fresh snapshots, follow the documented fallback interactions, and stop rather than attempting to solve CAPTCHA challenges.

Risk: Installing the skill or its browser automation dependency from unpinned external sources can create supply-chain exposure.

Mitigation: Install from trusted, pinned revisions when possible and review or scan the skill before deployment.

## Reference(s):

- [Google Flights](https://www.google.com/travel/flights)
- [agent-browser CLI](https://github.com/nicobailey/agent-browser)
- [Google Flights Interaction Patterns](artifact/references/interaction-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown flight summaries with optional booking-provider links and browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps the browser results session available for booking-link extraction and stops before purchase or payment steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
