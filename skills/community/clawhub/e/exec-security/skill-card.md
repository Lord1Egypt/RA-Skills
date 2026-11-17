## Description:

Pre-execution security checker for shell commands that detects dangerous patterns before running exec/bash tools, including destructive operations, credential leaks, data exfiltration, download-and-execute attacks, injection, Unicode obfuscation, resource exhaustion, and system file tampering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yozu](https://clawhub.ai/user/yozu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review non-trivial shell commands before execution, especially commands assembled programmatically or derived from external data. It helps agents decide whether to refuse, ask for confirmation, warn, or proceed with safer alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides advisory shell-command safety guidance, not runtime enforcement.

Mitigation: Treat results as a pre-execution checklist and pair them with the agent platform's execution approval or deny policy for enforcement.

Risk: Credential-handling guidance could be misapplied if an agent prints raw secret values after user confirmation.

Mitigation: Never print raw secrets; use redacted checks such as length, set/unset status, or scoped variable names.

Risk: Pattern-based command review can miss encoded strings, multi-step attacks, Unicode obfuscation, symlink targets, or shell-specific behavior.

Mitigation: Inspect each command segment, warn on unusual Unicode or shell-specific constructs, resolve paths before writes, and use timeouts for resource-heavy commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text, shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory pre-execution review; it does not enforce command execution policy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
