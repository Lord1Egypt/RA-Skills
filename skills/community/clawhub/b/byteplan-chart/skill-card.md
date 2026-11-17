## Description:

BytePlan AI chart generation skill that sends a natural-language BytePlan data query to the configured BytePlan service and renders the returned chart data as a local PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshuaiitr-ai](https://clawhub.ai/user/wangshuaiitr-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn BytePlan data-analysis requests into charts, including line, bar, pie, scatter, heatmap, table, pivot-table, and dual-axis visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BytePlan credentials and endpoint configuration require trust in both the publisher and the configured remote service.

Mitigation: Install only after verifying the publisher and BytePlan endpoint; keep BYTEPLAN_BASE_URL pinned to the intended HTTPS host and use least-privileged or read-only credentials where possible.

Risk: User query text and related BytePlan analysis data are sent to the configured remote service.

Mitigation: Avoid submitting sensitive or unauthorized data and review applicable data-handling requirements before use.

Risk: Some artifact installation guidance uses system-level or relative shared-script dependency steps.

Mitigation: Use an isolated virtual environment for dependencies and avoid the --system and ../../scripts installation paths called out by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshuaiitr-ai/skills/byteplan-chart)
- [Artifact README](artifact/README.md)
- [Artifact release notes](artifact/RELEASE-NOTES.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Console text plus timestamped PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates chart images in the configured chart output directory and may print remote API responses, extracted chart fields, and chart data to the console.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
