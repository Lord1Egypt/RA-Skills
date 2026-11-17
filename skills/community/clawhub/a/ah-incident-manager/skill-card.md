## Description:

Incident Manager provides incident response, analysis, prevention, classification, detection, and declaration guidance based on SRE, PagerDuty, and enterprise incident-response practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, incident commanders, and operations teams use this skill to declare, coordinate, communicate, analyze, and review service incidents. It provides structured templates for severity classification, response coordination, root cause analysis, post-mortems, metrics, and runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as incident, analysis, or prevention may activate the skill during general discussion.

Mitigation: Invoke the skill explicitly for incident workflows and review whether its templates are relevant before using them.

Risk: Incident classifications, communications, and post-mortem content can be incomplete or inaccurate if filled without operational review.

Mitigation: Have the incident commander or responsible operations owner validate severity, impact, timeline, customer messaging, and action items before relying on the output.

## Reference(s):

- [Incident Manager examples](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-incident-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown templates, checklists, tables, and inline shell command placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces incident-response templates and operational guidance; release security evidence reports no hidden access, persistence, credentials, or automatic execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
