## Description: <br>
Automatically reviews client claim authorization notice letters against configured insurance templates and sends review results to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulong423401-coder](https://clawhub.ai/user/liulong423401-coder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Insurance claim operations and compliance reviewers use this skill to check whether client claim authorization notice letters contain required authorization documents and handwritten signatures. The skill is intended to reduce manual review effort and notify reviewers through Feishu after each review cycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates decisions in a sensitive insurance claim-review workflow, including first-run auto-approval. <br>
Mitigation: Review before installing, require explicit approval for automated approval behavior, and disable first-run auto-approval unless it is required by policy. <br>
Risk: Runtime behavior and key controls are unclear because the submitted artifact references a runtime entry point that is not included. <br>
Mitigation: Verify the complete runtime code before deployment and confirm that it cannot approve or mutate claim-review tasks beyond the intended scope. <br>
Risk: Feishu notifications and audit logs may expose regulated or sensitive review information. <br>
Mitigation: Confirm webhook destinations, message contents, log retention, and access controls against privacy and compliance requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liulong423401-coder/compliance-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text or notification content, with JavaScript configuration for review rules and integrations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configured behavior includes Feishu notifications and 90-day JSONL audit logs when implemented by the runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/package.json, artifact/SKILL.md, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
