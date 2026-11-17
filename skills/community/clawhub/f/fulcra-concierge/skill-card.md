## Description:

Orchestrates the Fulcra personal-concierge experience as a single flow, routing start-of-day, end-of-day, and mid-day requests to the right concierge sub-skills while degrading gracefully when a dependency is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill as the main entry point for a Fulcra personal concierge workflow, including morning check-ins and briefings, evening debriefs, weekly cadence insights, and contextual routing to relationship, event, place-rating, and calendar skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can touch sensitive personal data, including feelings, sleep, calendar, relationships, and CRM context.

Mitigation: Use it only in trusted private contexts, avoid broad automatic invocation for sensitive workflows, and do not expose personal specifics in public or group settings.

Risk: Routine checks and shared helpers can depend on sensitive credentials, mutable local code, unpinned external tools, and broad API base environment overrides.

Mitigation: Install only from a trusted local Fulcra concierge directory, verify the Fulcra CLI supply chain, confirm API base environment variables point to intended Fulcra and Attio hosts, and keep credentials out of logs.

Risk: Some routed helper operations may update or delete high-impact personal or CRM data.

Mitigation: Require explicit user intent before running delete or update helpers, use dry-run behavior where available, and clearly state which steps ran, stored data, or were skipped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-concierge)
- [Publisher profile](https://clawhub.ai/user/keng009)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report skipped sub-skills, readiness status, and privacy-sensitive workflow results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
