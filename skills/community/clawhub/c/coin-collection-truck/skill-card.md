## Description:

Agent skill to search for the Hong Kong Coin Cart (收銀車) locations and schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sodiasm](https://clawhub.ai/user/sodiasm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong coin collection truck location, schedule, district, and suspension questions from bundled 2026 schedule data.

### Deployment Geography for Use:

Global; outputs are specific to Hong Kong coin collection truck locations.

## Known Risks and Mitigations:

Risk: The skill relies on bundled 2026 schedule data, which can become stale or incomplete for route decisions.

Mitigation: Tell users the schedule data is bundled for 2026 and advise verification against an official source for important visits.

Risk: Evidence guidance notes that one inspected record appears to have mismatched address and coordinate data.

Mitigation: Present both address and map details when available, and advise users to confirm locations before travel.

Risk: The skill runs a local Python script to query its bundled data.

Mitigation: Review and scan the script before deployment and run it only in the normal controlled agent environment.

## Reference(s):

- [Bundled coin collection truck schedule data](references/coin_collection_truck_hk.json)
- [ClawHub skill page](https://clawhub.ai/sodiasm/skills/coin-collection-truck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text schedule answers with optional map links; the local query script can also emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual addresses, service suspension notes, coordinates, and Google Maps links.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
