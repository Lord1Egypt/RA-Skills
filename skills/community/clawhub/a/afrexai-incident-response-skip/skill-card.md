## Description:

Guides IT and business teams through incident classification, response checklists, communication plans, timelines, and post-mortems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shark1973](https://clawhub.ai/user/shark1973)

### License/Terms of Use:

MIT-0

## Use Case:

Business, IT, and incident-response teams use this skill to classify incidents, generate response checklists and communications, maintain timelines, and draft post-mortems from incident descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident descriptions and timelines may contain secrets, credentials, personal data, regulated records, or legally privileged details.

Mitigation: Redact sensitive data unless the agent environment is approved for that data class.

Risk: Generated severity classifications, stakeholder communications, or response actions may be incomplete or operationally inappropriate.

Mitigation: Have the incident commander or accountable responder review proposed communications and actions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shark1973/skills/afrexai-incident-response-skip)
- [Industry Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with severity ratings, checklists, communications, timelines, and post-mortem sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include P1-P4 severity classification, incident-type-specific actions, stakeholder updates, timeline entries, and root-cause-analysis prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
