## Description:

Diagnose and fix EvoMap Evolver Hub authentication failures (HTTP 403 node_secret_invalid / unauthorized). Use when evolver solidify/sync fails with 403, node_secret_invalid, or unauthorized errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators who maintain EvoMap Evolver nodes use this skill to diagnose Hub authentication failures and follow credential repair, reauthorization, or offline-mode guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a benign verdict with medium confidence and incomplete inspection; the skill reads credential files as part of diagnosis.

Mitigation: Review the skill and its credential-file access before use, and avoid sharing diagnostic output that may contain node identifiers.

Risk: Repair guidance changes the .env configuration and synchronizes node credentials.

Mitigation: Back up .env before editing and verify the result with the documented dry-run command.

## Reference(s):

- [EvoMap device authorization](https://evomap.ai/device?user_code=XXX)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Troubleshooting text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnosis includes credential match status and OAuth token expiry; secret values are represented by hashes.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
