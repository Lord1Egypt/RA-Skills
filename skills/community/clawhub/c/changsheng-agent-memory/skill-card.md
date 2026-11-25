## Description:

Provides cross-session memory recovery for AI agents by loading essential context and checking for changes before rereading supporting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccy123abcd](https://clawhub.ai/user/ccy123abcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use the skill to carry identity, rules, open tasks, and handover details across sessions while limiting repeated reads. They can also search memory files for the context behind earlier decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing action-policy enforcement, conflicting guidance about memory edits, and incomplete analysis of some content.

Mitigation: Review the instructions and rule set before installing; enable the optional action-blocking feature only if needed and after checking how it affects actions.

Risk: The available security analysis did not fully evaluate all content, including some obfuscated text.

Mitigation: Read the skill files before use and do not treat scanner results as proof that all content is safe.

## Reference(s):

- [Memory system design](references/memory-system.md)
- [ClawHub release page](https://clawhub.ai/ccy123abcd/skills/changsheng-agent-memory)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text guidance]

**Output Format:** [Markdown and JSON memory files, plus concise plain-text recovery and search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Files are written locally to configured locations; search results are printed as text.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
