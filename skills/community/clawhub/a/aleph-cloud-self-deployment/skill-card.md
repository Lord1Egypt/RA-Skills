## Description:

Autonomously provision and configure a VM on Aleph Cloud, install the OpenClaw agent framework, and deploy an AI agent runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[san-npm](https://clawhub.ai/user/san-npm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide an AI agent through creating an Aleph Cloud VM, installing OpenClaw, configuring credentials and gateway access, and transferring identity or skills to the new environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous provisioning can create paid cloud resources and recurring spend.

Mitigation: Use an isolated test account or VM, set hard spending and instance limits outside the agent, and require human approval before provisioning.

Risk: Spawned VMs may receive broad Aleph account credentials or parent private keys.

Mitigation: Use delegated per-child Aleph keys and avoid copying parent keys to child instances.

Risk: Setup examples may expose secrets through command-line arguments, logs, copied files, or weak host verification.

Mitigation: Avoid placing API keys or wallet keys in command-line arguments or logs, verify SSH host keys, and restrict credential files with explicit permissions.

Risk: Dependency installation commands fetch packages and setup scripts at runtime.

Mitigation: Pin and verify dependencies before use in a production or shared environment.

## Reference(s):

- [Aleph account portal](https://account.aleph.im/)
- [ClawHub skill page](https://clawhub.ai/san-npm/skills/aleph-cloud-self-deployment)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, Python, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides procedural deployment guidance and example commands that should be reviewed before execution.]

## Skill Version(s):

1.0.2004 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
