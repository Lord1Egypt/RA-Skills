## Description: <br>
Live geopolitical intelligence analysis with 39 analytical modules and real-time data integration. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimaansari](https://clawhub.ai/user/nimaansari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to structure geopolitical assessments, gather public-source context from live data sources, identify intelligence gaps, and produce scenario-oriented analysis for countries, regions, or conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided topics, country values, and optional ACLED credentials to external public APIs. <br>
Mitigation: Use only topics and credentials approved for external API disclosure, and review data-flow disclosures before deployment. <br>
Risk: Geopolitical outputs may be speculative or misleading if treated as authoritative intelligence. <br>
Mitigation: Use outputs as analytical assistance and require human review, source verification, and confidence checks before operational decisions. <br>
Risk: Local tracking guidance can write to tracking_log.jsonl. <br>
Mitigation: Require confirmation before creating or appending tracking logs and review stored content for sensitivity. <br>
Risk: Documentation claims no credentials are required and lists runtime files that are not present in the artifact. <br>
Mitigation: Verify runtime file availability and credential requirements before installation or execution. <br>
Risk: Unpinned dependencies may resolve to different package versions over time. <br>
Mitigation: Pin and review dependency versions in a controlled environment before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nimaansari/geopolitical-analyst-skill) <br>
- [Data Sources Reference](references/sources.md) <br>
- [Analysis of Competing Hypotheses (ACH)](references/ach.md) <br>
- [Actor Classification Reference](references/actors.md) <br>
- [Early Warning System](references/early-warning.md) <br>
- [Scenario Simulation & Futures Modeling](references/scenario-modeling.md) <br>
- [Verification Challenge & Verifiability Assessment](references/verification-challenge.md) <br>
- [Sanctions Evasion & Counter-Sanctions Strategy](references/sanctions-evasion.md) <br>
- [Longitudinal Tracking Reference](references/tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analytical guidance with optional shell commands and JSON-like structured assessment fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence scoring, scenario cases, intelligence gaps, live public-source data summaries, and local tracking guidance.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
