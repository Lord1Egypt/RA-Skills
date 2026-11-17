## Description:

Doc Consistency checks .docx, .md, and .txt documents for internal consistency issues such as dangling references, numbering gaps, TOC/body mismatches, terminology drift, placeholders, stale years, and merge-loss indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, editors, proposal teams, and documentation maintainers use this skill to run an offline document consistency check and return a located findings report with a rerun command. It is suited for manuscripts, textbooks, proposals, RFP responses, manuals, theses, and contract sets that need repeatable cross-reference, numbering, terminology, placeholder, and merge-loss checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npx installation command can fetch a later or unreviewed package.

Mitigation: Install only from trusted sources and prefer a pinned or directly reviewed copy before use.

Risk: Generated reports include a U-King URL and contact footer that may appear in externally shared deliverables.

Mitigation: Review report output or use --json before sharing externally, and preserve required attribution unless separate white-label terms apply.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/doc-consistency)
- [U-King toolchain](https://u-king.org)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report or JSON findings list with inline shell commands for re-checking]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include severity counts, finding locations, suggested fixes, and a rerunnable check command; JSON output is available with --json.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
