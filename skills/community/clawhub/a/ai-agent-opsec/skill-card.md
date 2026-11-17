## Description:

Prevents an AI agent from leaking classified terms to external APIs, subagents, or logs by using a local term registry, runtime redaction, and pre-publish audit workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce accidental disclosure of configured sensitive terms before outbound calls, subagent tasks, and audit logging. It is intended for local runtime enforcement around agent workflows that handle private project names, credentials, personal details, or other registered sensitive strings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs may retain partially sanitized payload snippets after registry-based redaction.

Mitigation: Use a protected audit directory, add memory/security/ to .gitignore, and do not treat the current logging behavior as proof that no sensitive content was retained.

Risk: Sensitive terms omitted from classified/classified-terms.md may not be redacted before outbound use.

Mitigation: Maintain the local term registry before use, review it regularly, and test redaction behavior with representative sensitive strings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/ai-agent-opsec)
- [ClawHub Publisher Profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and local JSONL audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local filesystem reads and writes; no network activity is declared.]

## Skill Version(s):

1.4.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
