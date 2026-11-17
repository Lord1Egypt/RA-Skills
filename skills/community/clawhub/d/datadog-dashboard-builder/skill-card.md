## Description:

Design Datadog dashboards and monitors — recommend metrics, widget layouts, alerting thresholds, and SLO definitions. Analyze existing dashboards for blind spots and noise. Use when asked to build monitoring, set up alerts, or improve observability in Datadog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and platform engineers use this skill to design or audit Datadog dashboards, monitors, and SLOs for production services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested alert thresholds or notification routes may not match a production service's business impact or on-call process.

Mitigation: Review thresholds, severity levels, and notification routes with service owners before applying them in production.

Risk: Sample Datadog or Terraform snippets may need adaptation to local metric names, tags, environments, and dashboard conventions.

Mitigation: Validate generated queries and configuration against the target Datadog account before rollout.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Datadog query examples, YAML monitor templates, JSON widget snippets, and step-by-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service profiles, dashboard layouts, monitor thresholds, SLO targets, audit findings, and implementation steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
