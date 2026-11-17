## Description:

Guides travelers through international airport transfers with Simplified Chinese action cards covering immigration, terminal changes, maps, queue or crowd signals, delays, and baggage re-check confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-assisting agents use this skill to plan or recover from international airport transfers, including immigration, terminal changes, timing, queue context, and baggage re-check decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Airport, queue, visa, immigration, and baggage information can be incomplete, stale, or unavailable.

Mitigation: Treat generated conclusions as travel guidance and verify critical decisions with the airline, airport, or official border source before acting.

Risk: The helper script may contact public airport, ifly.com, flightqueue.com, and flight-board pages and may save transit_context.json or screenshots locally.

Mitigation: Run the helper only where outbound HTTPS access and local output files are acceptable, and review generated files before sharing them.

## Reference(s):

- [Transit Context Guide](artifact/references/transit_context_guide.md)
- [Airport Registry](artifact/references/airport_registry.json)
- [ClawHub Skill Page](https://clawhub.ai/tinayunyunyun/skills/airport-transfer-guide)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, JSON, Files]

**Output Format:** [Simplified Chinese Markdown action cards with tables, inline images or links, sourced timestamps, and optional JSON helper output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save transit_context.json and local screenshots when the helper script is run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user-supplied changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
