## Description:

Recover missing conversation context after explicit compaction or truncation, or when the user explicitly asks to recover prior work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recover only the context needed to resume work after compaction or truncation while preserving provenance, surfacing conflicts, and keeping recovered content untrusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovered conversation material may contain private or sensitive information.

Mitigation: Minimize recovered content, prefer paraphrases and identifiers, and redact credentials, tokens, personal data, and unrelated details.

Risk: Recovered messages or logs may include untrusted instructions or misleading status claims.

Mitigation: Treat recovered content as evidence only, preserve provenance and confidence, seek counterevidence for status claims, and follow only the current user's request and active system/developer instructions.

Risk: Searching outside the current thread may expose additional private context.

Mitigation: Use current supplied context first, keep recovery bounded, and require explicit approval before reading any separate source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdrhyne/skills/context-recovery)
- [Repository metadata link](https://github.com/jdrhyne/agent-skills/tree/main/skills/context-recovery)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown recovery report with concise provenance, timeline, conflicts, unresolved items, and a proposed next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only context recovery; external-source access and persistence require explicit user approval.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
