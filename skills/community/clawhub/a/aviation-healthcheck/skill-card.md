## Description:

航空维修健康检查 - FAA/EASA/CAAC适航指令、航空安全通告、MRO行业新闻、波音空客技术通告、OpenClaw状态、磁盘空间

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwzh](https://clawhub.ai/user/jiangwzh)

### License/Terms of Use:


## Use Case:

Developers, operators, and aviation maintenance reviewers use this skill to collect daily FAA, EASA, CAAC, safety bulletin, MRO, Boeing, and Airbus updates while also checking local OpenClaw status, disk space, and security/update status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact external aviation websites whose availability, access terms, or content can change.

Mitigation: Review cited sources and confirm critical aviation findings against authoritative FAA, EASA, CAAC, Boeing, or Airbus channels before operational use.

Risk: The skill may execute local OpenClaw status, health, security-audit, update-status, and disk-space commands.

Mitigation: Run it only in environments where local system inspection commands are approved and expected.

Risk: The suggested cron schedule can create recurring checks several times per day.

Mitigation: Enable scheduled execution only when repeated external checks and local health checks are desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangwzh/skills/aviation-healthcheck)
- [FAA Airworthiness Directives](https://ad.faa.gov)
- [EASA Airworthiness Directives](https://ad.easa.europa.eu)
- [CAAC](https://www.caac.gov.cn)
- [FAA Safety Alerts](https://www.faa.gov/news/safety_alerts)
- [EASA Safety Information](https://www.easa.europa.eu/safety-info)
- [Avionics International MRO](https://www.aviationtoday.com/category/mro/)
- [Leeham News](https://leehamnews.com)
- [Simple Flying](https://simpleflying.com)
- [Air Cargo News](https://aircargonews.com)
- [Aviation Herald](https://avherald.com)
- [Boeing ADS](https://myboeingfleet.com)
- [Airbus Airworthiness](https://myairbusfleet.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style maintenance and health-check report with command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes aviation update counts, local system status, security audit status, recommended actions, and optional cron scheduling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
