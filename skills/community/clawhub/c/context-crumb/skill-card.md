## Description:

ContextCrumb helps agents cheaply inspect and summarize large local prose-heavy files before deciding what raw text to load into context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchen20](https://clawhub.ai/user/yuchen20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to triage large Markdown documents, notes, transcripts, issue threads, research dumps, and narrative logs before loading raw source text into an LLM context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the ContextCrumb CLI from an unpinned package source could introduce supply-chain risk.

Mitigation: Install from a trusted source, pin ContextCrumb to a reviewed version when practical, and use a vetted environment.

Risk: Compressed output may omit wording, punctuation, or details needed for exact edits, quotations, commands, or configuration changes.

Mitigation: Use compressed output only for orientation, then inspect the raw source around relevant sections before quoting, editing, or copying exact syntax.

Risk: Running the CLI with broad filesystem access can expose more local files than needed for the document being compressed.

Mitigation: Run ContextCrumb with only the file access needed for the target document.

## Reference(s):

- [ContextCrumb ClawHub Skill Page](https://clawhub.ai/yuchen20/skills/context-crumb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compressed output is for orientation and triage, not authoritative quotation, exact syntax, or exact wording.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
