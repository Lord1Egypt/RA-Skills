## Description:

Comprehensive family emergency preparedness planning. Use when someone wants to create a household emergency plan, prepare for natural disasters, build a go-bag, or ensure their family can communicate and reunite during a crisis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create practical household emergency plans covering fire escape routes, communication plans, document kits, go-bags, evacuation routes, utility shut-offs, and special-needs planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the skill asks for filesystem capability even though it is primarily emergency-planning guidance.

Mitigation: Install only if filesystem access is acceptable for the agent environment, and avoid letting the agent read or store scans of sensitive identity, financial, medical, insurance, or legal documents unless explicitly intended.

Risk: The server security guidance notes that the installer resolves the current clawhub package through an unpinned npx command.

Mitigation: Prefer a pinned or verified installer path where available before deployment.

## Reference(s):

- [Family Emergency Planning on ClawHub](https://clawhub.ai/howtousehumans/skills/family-emergency-planning)
- [FEMA Ready.gov Plan](https://www.ready.gov/plan)
- [American Red Cross Emergency Preparedness](https://www.redcross.org/get-help/how-to-prepare-for-emergencies.html)
- [CDC Emergency Preparedness](https://www.cdc.gov/prepyourhealth/)
- [NOAA Weather Safety](https://www.weather.gov/safety/)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with checklists, templates, and structured planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user for household, regional, medical, document, and emergency-contact details to tailor the plan.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
