## Description: <br>
Generates CTO and CISO training plans, exams, certificates, progress reports, and compliance follow-up artifacts for an agent-led training workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Training and security operations agents use this skill to turn a CHO training plan into local courseware, exam scoring, certificate files, progress summaries, compliance reports, and action items. It is intended for controlled internal training workflows where human reviewers approve official records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scores, certificates, signatures, and escalation reports may look official. <br>
Mitigation: Require separate human approval and real cryptographic signing before using any generated artifact as an authoritative personnel, training, or compliance record. <br>
Risk: Training records can contain sensitive personnel and compliance data. <br>
Mitigation: Run the skill only in a controlled internal workspace and restrict access to generated files under knowledge-base/training/. <br>
Risk: The release requests a wallet-related capability without clear need in the evidence. <br>
Mitigation: Avoid granting wallet or other sensitive capabilities unless the publisher documents why they are required for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/cto-ciso-training) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Security review](artifact/SECURITY_REVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Local files and Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes training plans, exam results, certificate artifacts, audit trails, progress reports, compliance reports, and action items under knowledge-base/training/.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
