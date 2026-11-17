## Description:

Beginner fishing skills covering licensing, gear, techniques, and catch-to-cook basics for people starting to fish for food, recreation, affordable outdoor activity, or a meditative physical practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to learn beginner fishing for food procurement, recreation, or a low-cost outdoor practice. It helps agents tailor guidance around licensing, starter gear, basic rigs, fishing locations, fish handling, and simple catch preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fishing licenses, seasons, size limits, bag limits, stocking schedules, and consumption advisories vary by jurisdiction and can change.

Mitigation: Verify current rules and advisories with official fish and wildlife agencies before acting on location-specific guidance.

Risk: The release declares filesystem tooling while the skill behavior expects live regulatory and stocking lookups.

Mitigation: Review the runtime environment before use and ensure any required live lookup capability is explicitly available and controlled.

Risk: The installer command uses an unpinned external CLI.

Mitigation: Review the package source and resolved version before installation, and prefer a pinned or otherwise controlled installation path where possible.

Risk: License-expiration reminders could store personal timing or licensing information.

Mitigation: Only create or retain reminder data with explicit user consent.

## Reference(s):

- [Take Me Fishing](https://www.takemefishing.org)
- [NOAA Recreational Fishing Data](https://www.fisheries.noaa.gov/topic/recreational-fishing-data)
- [State Fish & Wildlife Agencies](https://www.fishwildlife.org)
- [Field & Stream Beginner Guides](https://www.fieldandstream.com)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with lists and occasional inline reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include location-specific licensing, regulation, stocking, and fish-consumption advisory guidance when the user provides a jurisdiction or water body.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
