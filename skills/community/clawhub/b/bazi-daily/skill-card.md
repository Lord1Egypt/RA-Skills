## Description: <br>
Daily Bazi Analysis helps OpenClaw users answer daily fortune, suitability, and auspicious-avoidance questions by combining the user's four-pillar profile with the current day's Bazi flow data and local classic references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilir-is-here](https://clawhub.ai/user/lilir-is-here) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill for personalized daily Bazi readings, including whether today is suitable for a planned activity and what actions to prefer or avoid. The skill first obtains or requests a complete four-pillar profile, checks the local date and daily flow data, then returns a structured trend-based reading with source labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save a user's Bazi four-pillar profile and create user-linked diagnostic logs without clear opt-in, retention, or deletion controls. <br>
Mitigation: Require explicit consent before saving profile data, support a one-time unsaved reading mode, and provide clear controls to view, update, or delete stored profile data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lilir-is-here/bazi-daily) <br>
- [Bazi Calendar Schema](references/bazi-calendar-schema.md) <br>
- [Classic Sources Routing](references/classic-sources-routing.md) <br>
- [Heartbeat Contract](references/heartbeat-contract.md) <br>
- [Classic Text Coverage Notes](references/classics/README.md) <br>
- [Import Command Template](references/import-command-template.md) <br>
- [Wannianrili Four Pillars Lookup](https://wannianrili.bmcx.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown daily analysis with structured date, flow-data, evidence, recommendation, and risk-note sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source labels for structure, seasonal adjustment, and principle explanations; daily readings are trend-based and non-deterministic.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
