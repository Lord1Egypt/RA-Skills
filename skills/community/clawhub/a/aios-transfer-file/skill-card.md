## Description:

AIOS File Transfer handles OpenClaw and AIOS agent file transfers through an S3-compatible SDK, downloading file_input:// objects into the current senderId workspace or uploading files from that workspace as file_output:// URIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AIOS/OpenClaw operators use this skill when an agent must receive a user-provided file or return a generated file while preserving per-sender workspace isolation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sender workspace isolation can be bypassed in the current implementation.

Mitigation: Reject or canonicalize symlinked sender, upload, and generated paths before transfer operations, and deploy only with trusted per-sender workspaces until that containment is fixed.

Risk: S3 credentials can be used against caller-named buckets.

Mitigation: Scope credentials tightly, restrict downloads to approved inbox buckets or prefixes, and avoid runtime bucket creation unless it is explicitly required and separately authorized.

## Reference(s):

- [README](README.md)
- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-transfer-file)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; transfer script returns JSON or a file_output:// URI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a current senderId, AIOS S3 environment variables, local Node.js dependencies, and S3 credentials scoped for the intended inbox and outbox buckets.]

## Skill Version(s):

1.0.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
