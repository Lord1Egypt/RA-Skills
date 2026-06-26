## Description: <br>
Detect, investigate, and contain malicious or compromised bots using behavior analysis, policy enforcement, and escalation protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arhadnane](https://clawhub.ai/user/arhadnane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing multi-bot systems use this skill to score bot behavior, flag malicious indicators, and recommend watch, block, or quarantine responses for incident triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated block or quarantine recommendations could disrupt legitimate bots if applied without review. <br>
Mitigation: Keep enforcement permissions scoped and require human approval for block or quarantine actions unless the deployment has a tested policy threshold. <br>
Risk: Bot-risk scoring may miss context or over-weight noisy incident and anomaly inputs. <br>
Mitigation: Review logs, message traces, and severity classification before using the recommendations for incident response. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/arhadnane/bot-police) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object with scan counts, per-bot risk scores, indicators, recommended actions, and summary counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions are recommendations generated from input bot telemetry; containment authority depends on the hosting agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
