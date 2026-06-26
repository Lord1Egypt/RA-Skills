## Description: <br>
Adversarial plan review using two different AI models, with static and alternating review modes for substantial implementation plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Don-GBot](https://clawhub.ai/user/Don-GBot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to run multi-model adversarial reviews of non-trivial implementation plans before coding. It is intended for plans involving sensitive areas such as authentication, payments, data models, or work expected to take more than about an hour. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plan content, codebase context, or architecture details may be sent to selected model providers during review. <br>
Mitigation: Do not include secrets, credentials, PII, or confidential architecture details unless the selected providers and retention policies are acceptable. <br>
Risk: Review runs persist local artifacts such as plans, reviewer responses, issue trackers, and summaries under tasks/reviews. <br>
Mitigation: Review and manage generated artifacts according to the workspace's data retention requirements. <br>
Risk: Broad activation phrases such as "review this plan" can start an automated multi-model workflow. <br>
Mitigation: Use the skill only when automated review of a substantial implementation plan is intended. <br>
Risk: Prompt-level untrusted-content delimiters reduce prompt injection risk but do not create an isolation boundary. <br>
Mitigation: Treat reviewer output as advice to inspect, and avoid placing adversarial untrusted code or sensitive content into review context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Don-GBot/cross-model-review) <br>
- [Publisher profile](https://clawhub.ai/user/Don-GBot) <br>
- [README](README.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON review records, and review workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates review artifacts under tasks/reviews, including issue trackers, round outputs, final plans, changelogs, and summaries.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
