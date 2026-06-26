## Description: <br>
Run longitudinal, in-context diary studies for product teams and convert weekly participant entries into concise User Signals + Recommendations with evidence, confidence, and experiment-ready actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product teams, founders, PMs, and researchers use this skill to run lightweight diary studies, compare behavior over time, and produce weekly evidence-backed product signals with experiment-ready recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Participant research data may include direct identifiers or sensitive context. <br>
Mitigation: Collect explicit consent, redact synthesized outputs, separate raw entries from reports, and enforce retention and deletion rules before launch. <br>
Risk: Enabled integrations can expose more data than the study requires. <br>
Mitigation: Enable only needed integrations, scope API tokens narrowly, and leave credentials unset for disabled integrations. <br>
Risk: Attachments such as screenshots, photos, or audio may leak private information if copied into reports. <br>
Mitigation: Store attachments in restricted storage, reference attachment IDs or metadata in reports, and use signed URLs with expiry where links are required. <br>
Risk: Weekly recommendations may overstate weak or contradictory qualitative evidence. <br>
Mitigation: Require evidence-linked signals, confidence reasons, saturation checks, and low-risk experiments when confidence is low. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nicolas-m-design/continuous-user-research) <br>
- [Publisher Profile](https://clawhub.ai/user/nicolas-m-design) <br>
- [Project Homepage](https://github.com/nicolas-m-design/user-research-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API calls, Configuration guidance] <br>
**Output Format:** [Markdown and JSON study artifacts, including study briefs, consent messages, diary prompts, weekly signal reports, and optional issue payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are expected to use redacted participant evidence, confidence labels, and experiment plans.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
