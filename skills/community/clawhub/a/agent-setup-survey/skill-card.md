## Description: <br>
Detects an AI agent execution environment and prepares a small, reviewable research survey payload about OS, architecture, container or VM status, detection signals, and optional installed-skill metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Agent-Deployments](https://clawhub.ai/user/Agent-Deployments) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and researchers use this skill to inspect local runtime environment signals and optionally contribute an anonymized survey record to internetwarte.eu after reviewing the generated JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The survey payload may reveal environment details such as OS, CPU architecture, container status, VM status, and boolean detection signals. <br>
Mitigation: Review the generated JSON before submission and submit only if sharing that environment fingerprint is acceptable. <br>
Risk: Optional skill-name disclosure may reveal sensitive local agent tooling or workflows. <br>
Mitigation: Decline optional skill sharing or provide only non-sensitive skill names. <br>
Risk: A failed submission can leave a payload in the local outbox for later upload. <br>
Mitigation: Delete any outbox payload if you decide not to upload it later. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Agent-Deployments/agent-setup-survey) <br>
- [Agent Setup Survey Dashboard](https://internetwarte.eu/agentsetup) <br>
- [Survey Submission Endpoint](https://internetwarte.eu/submit) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and reviewable JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated JSON is shown to the user before any submission; failed submissions can be saved locally for manual upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
