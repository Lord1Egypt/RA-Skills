## Description: <br>
Object storage operations for Volcengine TOS (Tinder Object Storage). Use when users need bucket management, object upload/download, listing, deletion, presigned URLs, or storage troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[day253](https://clawhub.ai/user/day253) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Volcengine TOS buckets and objects, including listing, upload, download, metadata checks, copy, deletion, and presigned URL generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud storage credentials may allow broader access than intended. <br>
Mitigation: Use a least-privilege IAM key limited to the intended Volcengine TOS buckets and keep .env files private. <br>
Risk: Mutating bucket or object operations can overwrite, copy, or delete data when parameters are wrong. <br>
Mitigation: Confirm bucket, key, region, and scope before execution; run a minimal read-only check first and require --confirm for delete operations. <br>
Risk: Presigned URLs can expose object access while they remain valid. <br>
Mitigation: Review expiration values before sharing and use the shortest practical validity window. <br>


## Reference(s): <br>
- [Volcengine TOS SDK Python API Reference](references/api_reference.md) <br>
- [Volcengine TOS Sources](references/sources.md) <br>
- [TOS Python SDK GitHub](https://github.com/volcengine/ve-tos-python-sdk) <br>
- [TOS Python SDK PyPI](https://pypi.org/project/tos/) <br>
- [Volcengine TOS Python SDK Quick Start](https://www.volcengine.com/docs/6349/92786) <br>
- [Volcengine TOS Presigned URLs](https://www.volcengine.com/docs/6349/135725) <br>
- [Volcengine TOS List Buckets](https://www.volcengine.com/docs/6349/92794) <br>
- [Volcengine TOS API Overview](https://www.volcengine.com/docs/6349/74837) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operation results, manifests, and logs are directed to output/volcengine-storage-tos/ unless OUTPUT_DIR overrides the base directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
