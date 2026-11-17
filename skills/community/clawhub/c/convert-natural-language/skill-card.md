## Description:

Converts natural-language requests into structured SQL, JSON, API requests, search queries, regular expressions, schemas, or shell commands, with explanations and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate plain-language requirements into structured outputs such as queries, schemas, requests, regular expressions, and commands. It is intended to surface assumptions, ambiguity, confidence, and warnings before generated artifacts are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL, shell commands, and API requests may be executable or may change external systems if run without review.

Mitigation: Review generated artifacts before use and require explicit confirmation before executing commands, sending API calls, or running mutating SQL.

Risk: Authorization headers, API keys, and environment auth tokens may expose sensitive credentials if copied into generated API requests or commands.

Mitigation: Use placeholders or user-supplied test tokens, scope credentials tightly, and avoid automatic execution or transmission of generated requests.

Risk: Ambiguous natural-language input can produce incorrect table names, fields, date ranges, database dialects, or overly broad regular expressions.

Mitigation: Ask clarifying questions when required information is missing and flag assumptions, confidence, and warnings in the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/convert-natural-language)
- [Metadata source repository](https://github.com/MiniMax-AI/skills)
- [MiniMax](https://minimax.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown containing structured snippets such as SQL, JSON, API requests, search queries, regular expressions, schemas, shell commands, explanations, confidence, warnings, and assumptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask clarifying questions and requires human review before executing generated commands, mutating SQL, or API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
