## Description:

Object storage operations for Volcengine TOS (Tinder Object Storage), including bucket management, object upload and download, listing, deletion, presigned URLs, and storage troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[day253](https://clawhub.ai/user/day253)

### License/Terms of Use:


## Use Case:

Developers and cloud operators use this skill to inspect and manage Volcengine TOS buckets and objects through a normalized Python command interface. It supports read-only checks, uploads, downloads, copies, deletions, metadata inspection, and presigned URL generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate cloud storage through create, upload, copy, delete, and presign operations.

Mitigation: Require explicit user confirmation for mutating operations, scope commands to named buckets and keys, and verify results after execution.

Risk: The skill uses Volcengine credentials and may read local .env files.

Mitigation: Use least-privilege IAM keys, run in an isolated working directory, and avoid untrusted directories that may contain credential files.

Risk: The runtime depends on the external tos Python SDK.

Mitigation: Install a pinned and reviewed tos SDK version before use.

## Reference(s):

- [Volcengine TOS SDK (Python) API Reference](references/api_reference.md)
- [Sources](references/sources.md)
- [TOS Python SDK GitHub](https://github.com/volcengine/ve-tos-python-sdk)
- [TOS Python SDK PyPI](https://pypi.org/project/tos/)
- [Volcengine TOS Python SDK Quick Start](https://www.volcengine.com/docs/6349/92786)
- [Volcengine TOS Presigned URL Documentation](https://www.volcengine.com/docs/6349/135725)
- [Volcengine TOS API Overview](https://www.volcengine.com/docs/6349/74837)
- [ClawHub Skill Page](https://clawhub.ai/day253/skills/day253-volcengine-storage-tos)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation results, manifests, and logs are saved under output/volcengine-storage-tos/ unless OUTPUT_DIR overrides the base directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
