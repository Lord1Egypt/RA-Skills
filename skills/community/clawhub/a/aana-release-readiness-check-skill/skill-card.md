## Description: <br>
Checks release readiness by verifying artifacts, tests, docs, approval, risks, and evidence before publishing tags, packages, or deployment notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release reviewers use this instruction-only skill to check OpenClaw-style release targets, tags, changelogs, docs, artifacts, tests, approvals, rollback readiness, and public claims before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A package identity or version mismatch can cause reviewers to approve the wrong release target. <br>
Mitigation: Confirm the intended slug and version before using this as a formal release gate, and make sure release metadata, artifact metadata, and marketplace references match. <br>
Risk: External AANA checker use could expose private release details if more than the redacted summary is shared. <br>
Mitigation: Share only the minimal review payload fields described by the skill, and omit secrets, credentials, full logs, private notes, and unrelated repository data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-release-readiness-check-skill) <br>
- [Release readiness check schema](artifact/schemas/release-readiness-check.schema.json) <br>
- [Redacted release readiness check example](artifact/examples/redacted-release-readiness-check.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain text release-gate summary with structured status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; the skill does not execute commands, write files, install dependencies, persist memory, or publish releases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
