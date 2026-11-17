## Description:

Everclaw provides cloud memory backup and restore for an agent's identity, profile, memory, tool notes, and heartbeat files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlxue](https://clawhub.ai/user/tlxue)

### License/Terms of Use:


## Use Case:

External developers and agent users use Everclaw to back up and restore OpenClaw memory and identity files across devices, reinstalls, and workspace resets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically upload sensitive agent identity, profile, memory, tool notes, and heartbeat files to the Everclaw service.

Mitigation: Install only after reviewing the exact sync list, removing secrets from synced files, and confirming that sending those files to the service is acceptable.

Risk: The skill creates recurring sync behavior through heartbeat instructions.

Mitigation: Use a version that asks before enabling recurring sync and provides a clear disable or uninstall path.

Risk: The artifact makes encryption assurances that the security evidence does not substantiate.

Mitigation: Do not rely on confidentiality claims unless verifiable client-side encryption is implemented and reviewed before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlxue/skills/everclaw)
- [Everclaw API base URL](https://everclaw.chong-eae.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and HTTP API command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local OpenClaw configuration and selected workspace memory files when invoked.]

## Skill Version(s):

0.3.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
