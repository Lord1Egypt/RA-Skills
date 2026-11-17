## Description:

Travel Itinerary Planner by Chaceclaw helps an agent turn destination, duration, budget, traveler type, and interests into a detailed travel itinerary with budget estimates, restaurant suggestions, transportation guidance, checklists, and practical travel advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to collect trip requirements and produce day-by-day itineraries, cost breakdowns, transportation notes, pre-trip checklists, and optional travel journal or expense-tracking outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather, emergency, visa, exchange-rate, booking, sharing, and budget-accuracy outputs may be examples or static estimates rather than verified live data.

Mitigation: Treat these outputs as planning drafts and independently verify safety-critical or time-sensitive travel information before booking or travel.

Risk: The skill can store trip details in local files under ~/.travel-planner.

Mitigation: Review stored content for sensitive personal or travel data, restrict access to the local directory, and avoid running it with untrusted inputs.

Risk: Local file-writing behavior has weak filename/path controls.

Mitigation: Harden filename handling and constrain writes to expected directories before use in shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ling-qian/skills/chaceclaw-travel-itinerary)
- [Publisher profile](https://clawhub.ai/user/ling-qian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown itinerary plans, checklist text, budget summaries, Python helper output, and optional local JSON or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist itinerary, expense, diary, and related travel files under ~/.travel-planner when the Python helper code is run.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
