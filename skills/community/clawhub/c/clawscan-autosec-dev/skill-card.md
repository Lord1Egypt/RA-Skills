## Description:

ClawScan performs first-pass security checks for OpenClaw deployments by checking registration and update state, matching OpenClaw versions to known vulnerable ranges, comparing installed skill hashes against known malicious hashes, and reviewing local listener exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fate93930](https://clawhub.ai/user/fate93930)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run a first-pass OpenClaw security assessment covering known vulnerable versions, known malicious skill hashes, local listener exposure, update status, and scheduled monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a random client ID, OpenClaw version data, installed-skill file hashes, and local listener metadata to a third-party ClawScan service.

Mitigation: Confirm the remote endpoint and data handling expectations before installation, and run only the modules whose data sharing is acceptable.

Risk: Port checks may include broad local listener metadata, including listeners unrelated to OpenClaw.

Mitigation: Review the listener payload before submission when possible and avoid using port-check where unrelated process metadata should not be shared.

Risk: Scheduled scans can persist recurring scan state.

Mitigation: Confirm how to disable scheduled scans and delete the stored client and schedule files before enabling recurring checks.

Risk: A clean result can be mistaken for a complete security assurance.

Mitigation: Treat clean results only as no known match in the current ClawScan corpus and supplement them with normal security review.

## Reference(s):

- [ClawScan API Contract](artifact/references/api-contract.md)
- [ClawScan Skill Homepage](https://github.com/autosecdev/clawscan-skills)
- [ClawHub Skill Page](https://clawhub.ai/fate93930/skills/clawscan-autosec-dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with per-module status, risk, conclusion, evidence, recommended next steps, and scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled scans report only when risk is found; clean results mean no known issue was matched, not a guarantee of safety.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
