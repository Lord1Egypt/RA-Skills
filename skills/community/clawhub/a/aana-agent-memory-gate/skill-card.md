## Description:

AANA Agent Memory Gate Skill provides instruction-only guardrails for storing, reusing, editing, importing, exporting, and deleting user memory with explicit approval and data minimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make agent memory operations deliberate, relevant, user-approved, and reversible where possible. It is useful when an agent may store, reuse, edit, delete, import, or export user memory, especially sensitive or inferred memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may store or reuse sensitive, stale, inferred, or unrelated memory without the user's expectation if memory operations are not gated.

Mitigation: Require relevance, source, sensitivity, approval, and lifecycle checks before memory use, and ask before sensitive reuse or persistent changes.

Risk: Raw secrets, private records, logs, transcripts, or speculative sensitive inferences could be retained unnecessarily.

Mitigation: Prefer temporary context and redacted summaries, apply data minimization, and forbid storage of credentials, raw private records, and speculative sensitive inferences.

Risk: The skill changes agent behavior around memory decisions and may prompt users more often before using or changing memories.

Mitigation: Disclose the approval behavior to installers and use it where explicit user control over memory is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-agent-memory-gate)
- [README](README.md)
- [Agent memory gate schema](schemas/agent-memory-gate.schema.json)
- [Redacted memory gate example](examples/redacted-agent-memory-gate.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with optional JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not execute commands, install dependencies, persist memory, or call services by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
