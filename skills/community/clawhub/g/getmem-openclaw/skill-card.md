## Description:

Persistent memory for OpenClaw agents via getmem.ai; it retrieves user memory before replies and ingests conversation exchanges after replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimblev2023](https://clawhub.ai/user/nimblev2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this plugin to add cross-session memory to agents by retrieving relevant user context before a reply and storing new conversation turns after a reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, replies, and user identifiers are sent to and stored by getmem.ai.

Mitigation: Install only where users and administrators explicitly accept third-party memory storage and avoid sensitive or regulated deployments without appropriate controls.

Risk: Retrieved memories are injected into later agent context and may affect future replies.

Mitigation: Use only in deployments with clear opt-in, deletion, retention, and identity-scoping controls, and review behavior before enabling it for multiple tenants.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimblev2023/skills/getmem-openclaw)
- [getmem.ai](https://getmem.ai)
- [getmem.ai API reference](https://getmem.ai/llms-full.txt)
- [getmem.ai platform](https://platform.getmem.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with inline shell commands and configuration keys]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and sends user identifiers, prompts, and replies to getmem.ai when enabled.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
