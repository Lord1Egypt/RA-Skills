## Description:

Measure and safely reduce always-loaded agent instruction context in characters and tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posthuman](https://clawhub.ai/user/posthuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to measure recurring always-loaded instruction cost, reduce duplicated or task-specific context, and verify that safety, authority, and meaning are preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instruction-file edits can weaken authority, safety, or behavior even when text appears equivalent.

Mitigation: Require explicit operator intent, preserve higher-precedence rules, verify moved rules remain available, and run the documented assurance regressions before accepting changes.

Risk: Exact token counting sends complete selected-file contents to the chosen tokenizer service.

Mitigation: Use exact token counting only with an explicitly selected trusted loopback tokenizer and confirm that it does not retain requests.

Risk: Budget reports can disclose instruction file names, section headings, path prefixes, and, with --show-content, duplicated instruction text and the workspace path.

Mitigation: Keep reports local by default, use --show-content only with explicit intent, and redact sensitive details before sharing output.

## Reference(s):

- [Method and measurements](references/method.md)
- [ClawHub skill page](https://clawhub.ai/posthuman/skills/context-budget)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts are estimates unless the operator explicitly selects a trusted loopback tokenizer model.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
