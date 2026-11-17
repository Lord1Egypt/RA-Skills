## Description:

Cycle Sync Training helps agents plan workouts around menstrual-cycle phases, log symptoms, adjust training intensity, and predict high-energy training windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kritsanan1](https://clawhub.ai/user/kritsanan1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to provide cycle-aware fitness guidance, workout planning, intensity adjustments, and energy-window predictions for people who choose to share menstrual-cycle and symptom information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive menstrual-cycle and symptom data with under-specified backend and messaging controls.

Mitigation: Require explicit user consent before logging cycle data, configure per-user Supabase access controls, keep service credentials server-side, and avoid sending health details through LINE or Facebook by default.

Risk: Broad activation rules may apply cycle-aware guidance to general women's fitness requests.

Mitigation: Confirm that the user wants cycle-aware guidance before collecting, logging, or using menstrual-cycle information.

Risk: Deployment instructions list dependencies without version pins.

Mitigation: Pin dependencies before deployment and review the package set before installation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/kritsanan1/cycle-sync-training)
- [ClawHub skill page](https://clawhub.ai/kritsanan1/skills/cycle-sync-training)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or JSON-like tool guidance with configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workout recommendations, phase tips, avoid lists, intensity adjustments, scheduling windows, and backend configuration guidance.]

## Skill Version(s):

0.1.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
