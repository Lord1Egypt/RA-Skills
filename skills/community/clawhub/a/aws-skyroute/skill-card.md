## Description:

3D globe visualization of global traffic flowing to AWS regions, with latency-colored arcs, CloudFront edge panels, P95/P99 metrics, error rate alerts, and sparkline trends for traffic monitoring dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengcecho](https://clawhub.ai/user/chengcecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and incident response teams can use this skill to set up or adapt a static WebGL dashboard for visualizing global user traffic to AWS-backed applications. It is suited to NOC displays, executive dashboards, incident response views, presentations, and demo environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard loads mutable third-party JavaScript from a CDN when opened.

Mitigation: Vendor or pin the external script and add integrity checks before hosting it on a sensitive origin or internal dashboard.

Risk: The visualized traffic, latency, error rate, and request metrics are simulated by default.

Mitigation: Label the default view as simulated and connect a reviewed data source before using it for operational decisions.

Risk: Some UI labels are Chinese-localized, which can affect review and operational interpretation for other audiences.

Mitigation: Review and localize dashboard text for the intended operators before deployment.

## Reference(s):

- [SkyRoute Live Demo](https://chengcecho.github.io/skyroute/)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [MaxMind GeoLite2 Signup](https://www.maxmind.com/en/geolite2/signup)
- [ClawHub Skill Page](https://clawhub.ai/chengcecho/skills/aws-skyroute)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, JavaScript, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on a static HTML/WebGL dashboard and real-data integration points; default traffic and metrics are simulated.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
