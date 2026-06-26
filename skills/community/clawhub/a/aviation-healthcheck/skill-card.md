## Description: <br>
Aviation Healthcheck guides agents through daily aviation maintenance information checks and local OpenClaw system health reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwzh](https://clawhub.ai/user/jiangwzh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and maintenance-support users can use this skill to collect aviation airworthiness and industry updates, run local OpenClaw and disk-health checks, and produce a daily review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include local system status, audit output, and disk-space information. <br>
Mitigation: Review reports before sharing them outside the intended operational audience. <br>
Risk: The skill suggests recurring cron execution for daily checks. <br>
Mitigation: Enable scheduled execution only when recurring aviation and local health checks are intended. <br>


## Reference(s): <br>
- [FAA Airworthiness Directives](https://ad.faa.gov) <br>
- [EASA Airworthiness Directives](https://ad.easa.europa.eu) <br>
- [Civil Aviation Administration of China](https://www.caac.gov.cn) <br>
- [FAA Safety Alerts](https://www.faa.gov/news/safety_alerts) <br>
- [EASA Safety Information](https://www.easa.europa.eu/safety-info) <br>
- [Avionics International MRO News](https://www.aviationtoday.com/category/mro/) <br>
- [Leeham News](https://leehamnews.com) <br>
- [Simple Flying](https://simpleflying.com) <br>
- [Air Cargo News](https://aircargonews.com) <br>
- [Aviation Herald](https://avherald.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include aviation update summaries, local OpenClaw status, security audit output, and disk-space information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
