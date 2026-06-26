## Description: <br>
AI 心脏康复管理系统 — 基于 ACC/AHA 指南的安全增强型康复管理 Web 应用。症状预警、风险分层、个体化运动处方、药物依从性提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-feng123](https://clawhub.ai/user/chen-feng123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support teams can use this local web application to manage cardiac rehabilitation profiles, daily logs, risk stratification, exercise prescriptions, medication reminders, and safety warnings. Its recommendations are support for clinician-reviewed care and are not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical recommendations could be misused as a substitute for professional care. <br>
Mitigation: Treat all recommendations as support for clinician-reviewed care and require cardiologist review before following rehabilitation plans. <br>
Risk: The local app requires a strong Flask SECRET_KEY before running. <br>
Mitigation: Set a strong SECRET_KEY on a trusted device before deployment. <br>
Risk: Pages load Bootstrap and Chart.js from a third-party CDN, creating a privacy documentation gap for sensitive patient data. <br>
Mitigation: Self-host Bootstrap and Chart.js or block external CDN access before entering real patient data when privacy or compliance requirements are strict. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chen-feng123/ai-cardiac-rehab) <br>
- [API_SPEC.md](API_SPEC.md) <br>
- [USE_GUIDE.md](USE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, configuration] <br>
**Output Format:** [Local web application responses with clinical risk summaries, exercise prescription text, medication reminders, safety warnings, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite storage and requires SECRET_KEY before running.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, created 2026-05-10T13:15:57Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
