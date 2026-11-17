## Description:

Legal/compliance guardrails for outbound OpenClaw actions (anti-spam, defamation, privacy, financial claims).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawyered0](https://clawhub.ai/user/lawyered0)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to preflight outbound posts, comments, messages, market commentary, and other publish actions before execution. It returns policy status and rewrite guidance for legal, defamation, privacy, HR, anti-spam, and financial-claim risk families.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-wrapper path can execute publishing commands after REVIEW decisions by default.

Mitigation: Prefer direct checker use for sensitive drafts, enable --strict for wrapper runs, and route REVIEW outcomes to human or legal review before publishing.

Risk: Wrapped command execution depends on operational scoping and can be under-controlled if broad command permissions are used.

Mitigation: Use absolute-path allowlists, avoid --allow-any-command in production, require ticketed approval when bypassing allowlists, set timeouts, and enable audit logging for wrapped outbound commands.

Risk: Sensitive draft text passed through process arguments may appear in local process metadata or logs.

Mitigation: Avoid passing sensitive text through command-line arguments; prefer file or stdin inputs where appropriate and enable --sanitize-env with narrow keep rules for wrapped commands.

## Reference(s):

- [Guardrail Policy Map](references/guardrail-policy-map.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON guardrail reports with status, findings, suggestions, optional safe text, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Statuses are PASS, WATCH, REVIEW, and BLOCK; wrapper execution can emit stderr warnings, return process exit codes, and write JSONL audit records when configured.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
