## Description:

Minimal TOS smoke tests. Validate AK/SK config, list buckets, and upload/download with Volcengine TOS. Supports both tosutil CLI and tos_manage.py script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[day253](https://clawhub.ai/user/day253)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to smoke test Volcengine TOS object storage access with configured AK/SK credentials, including bucket listing, object upload, download validation, metadata checks, presigned URL creation, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The smoke test uses credentials to upload, presign, download, and delete objects in Volcengine TOS.

Mitigation: Use least-privilege test credentials and run commands only against a disposable bucket or clearly isolated test prefix.

Risk: The workflow depends on the tos package, tosutil CLI, and any tos_manage.py script available in the user's environment.

Mitigation: Verify the package, CLI, and script before use, and install or run them only in an isolated environment.

## Reference(s):

- [Volcengine tosutil CLI documentation](https://www.volcengine.com/docs/6349/148772)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to run smoke-test commands and compare expected command results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
