## Description:

Condenses long agent session transcripts into compact handoff memos with decisions, open tasks, risks, facts, links, and best-effort credential redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Context Compactor to turn long session transcripts into concise handoff or daily digest memos after context compaction or before handing work to another agent or human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated memos may still include sensitive transcript content because credential redaction is best-effort and can miss parts of quoted multi-word secrets.

Mitigation: Review generated memos before sharing and use the tool only on transcript files intentionally selected with user consent.

Risk: Strict mode may reduce sensitive output but is not a complete secret scrubber.

Mitigation: Treat strict mode as an additional filter, not as a replacement for human review of generated handoff memos.

## Reference(s):

- [Context Compactor ClawHub page](https://clawhub.ai/vnbochkarev-netizen/skills/context-compactor-cli)
- [Context Compactor npm package](https://www.npmjs.com/package/@vibo-dev/context-compactor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown handoff memo or stdout text from a local Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Best-effort credential values are redacted before output; strict mode drops whole suspect lines.]

## Skill Version(s):

1.1.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
