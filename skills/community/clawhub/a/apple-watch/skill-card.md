## Description:

Apple Watch Health Sync helps an agent set up and query Apple Watch health data through the Health Auto Export app, a local Python server, REST API calls, and a dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lainnet-42](https://clawhub.ai/user/lainnet-42)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to configure Apple Watch health-data ingestion from Health Auto Export, keep a local receiver running, query metrics such as sleep, heart rate, steps, and workouts, and troubleshoot the sync pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health records may be exposed if the local service is reachable on the LAN.

Mitigation: Bind the receiver to localhost unless LAN ingestion is required, restrict network access, and avoid exposing the dashboard or API outside trusted devices.

Risk: The API key is stored and reused in local files and templates.

Mitigation: Protect .env.json and generated templates, avoid sharing files that contain the key, and rotate the key if it is disclosed.

Risk: Persistent startup tasks can keep health-data ingestion running beyond the current agent session.

Mitigation: Install persistent services only with explicit user approval and review scheduled-task or launchd configuration before enabling it.

Risk: The setup flow can download mutable upstream content during installation.

Mitigation: Review or pin the upstream download path before running setup in a sensitive environment.

## Reference(s):

- [Health Auto Export App Store Listing](https://apps.apple.com/us/app/health-auto-export-json-csv/id1115567069)
- [Health Auto Export Server Reference Repository](https://github.com/HealthyApps/health-auto-export-server)
- [Apple Watch Health Sync ClawHub Page](https://clawhub.ai/lainnet-42/skills/apple-watch)
- [lainnet-42 Publisher Profile](https://clawhub.ai/user/lainnet-42)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, generated Python and HTML files, JSON configuration templates, REST API queries, and dashboard summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and user-controlled Apple Watch, iPhone, Health Auto Export, and same-LAN setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
