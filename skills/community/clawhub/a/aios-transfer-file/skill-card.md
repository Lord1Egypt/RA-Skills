## Description: <br>
Transfers OpenClaw and AIOS agent files through an S3-compatible SDK, downloading file_input URIs into the workspace and uploading local files as file_output URIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AIOS/OpenClaw operators use this skill to receive user-provided file_input objects and return generated or processed files through file_output links. It is intended for controlled environments where agents need repeatable S3-backed file transfer behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload files and create S3 buckets, and the security scan notes that this power is not tightly enforced at runtime. <br>
Mitigation: Install it only in a controlled AIOS/OpenClaw environment and scope S3 credentials to the intended inbox and outbox buckets. <br>
Risk: Uploads may expose unintended workspace files if an agent stages the wrong local path. <br>
Mitigation: Use the skill only for files the user asked to receive, verify the staged file before upload, and clean up file_output staging files after successful uploads. <br>
Risk: Dependency installation can change the runtime package set if it ignores the bundled lockfile. <br>
Mitigation: Prefer npm ci from the included lockfile and run the transfer script from the skill directory so it resolves the local AWS SDK dependency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-transfer-file) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the transfer script outputs JSON or a file_output URI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are staged under file_input, uploads are staged under file_output, and successful uploads return a file_output URI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
