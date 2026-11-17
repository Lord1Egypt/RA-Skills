## Description:

Triage call-centre and voice support transcripts into summaries, sentiment, urgency, routing queues, and follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Contact centre operators, support teams, councils, clinics, and SMEs use this skill to turn raw transcripts or voice-agent notes into routing-ready JSON with a short summary, sentiment, urgency, queue recommendation, follow-up actions, and evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call transcripts and generated routing output may contain customer or sensitive information.

Mitigation: Handle outputs with the same care as the original transcripts, avoid shared output paths unless needed, and store results only where customer data is permitted.

Risk: Heuristic sentiment, urgency, and routing labels may be incomplete or unsuitable for direct case-system updates.

Mitigation: Review the JSON result before sending summaries, routes, or actions into CRM or helpdesk workflows.

## Reference(s):

- [Contact Centre Grok Pack on ClawHub](https://clawhub.ai/stevojarvisai-star/skills/contact-centre-grok-pack)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [JSON object with summary, sentiment, urgency, route, actions, and evidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write the JSON result to a local output path; it does not make calls, contact customers, or write to external systems.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
