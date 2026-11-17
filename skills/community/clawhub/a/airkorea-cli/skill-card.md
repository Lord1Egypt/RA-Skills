## Description:

Airkorea CLI helps agents use shell commands to query Korea Environment Corporation AirKorea OpenAPI services for real-time air-quality measurements, station lookup, TM coordinate lookup, nearby station lookup, and 1-3 day forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build Korea-focused air-quality dashboards, alerts, advisories, data pulls, and grounded responses using AirKorea public data.

### Deployment Geography for Use:

Global; data coverage is limited to Korea.

## Known Risks and Mitigations:

Risk: Endpoint override environment variables can redirect requests and expose AIRKOREA_SERVICE_KEY to an untrusted destination.

Mitigation: Use the default apis.data.go.kr endpoints and set ARPLTN_BASE or MSRSTN_BASE only after verifying the destination is trusted.

Risk: The nearby station help text includes an eval-based workflow for extracting TM coordinates.

Mitigation: Extract TM coordinates with read and jq instead of copying an eval command.

Risk: The skill depends on a private AirKorea service key.

Mitigation: Keep AIRKOREA_SERVICE_KEY private and avoid logging commands or environments that reveal it.

## Reference(s):

- [Airkorea CLI ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/airkorea-cli)
- [Data.go.kr Open Data Portal](https://www.data.go.kr/)
- [AirKorea Air Pollution Information Service](https://apis.data.go.kr/B552584/ArpltnInforInqireSvc)
- [AirKorea Measuring Station Information Service](https://apis.data.go.kr/B552584/MsrstnInfoInqireSvc)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code, JSONL data]

**Output Format:** [Markdown guidance with inline bash commands and JSONL-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and AIRKOREA_SERVICE_KEY for command execution.]

## Skill Version(s):

0.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
