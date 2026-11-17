## Description:

Reviews Chinese contracts and helps produce Word documents with tracked changes, comments, clean versions, risk reports, and multi-round iteration records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wux818738-alt](https://clawhub.ai/user/wux818738-alt)

### License/Terms of Use:

GPL-3.0

## Use Case:

Legal, business, and operations users can use this skill to review Chinese-language contracts, identify clause-level risks, draft tracked changes and comments, and manage clean versions across review rounds. Agents can also use its scripts and references to parse contracts, recommend clauses, check cross-references, and structure review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document-processing code handles contracts and generates modified Word documents.

Mitigation: Run the skill in an isolated workspace, use copies of original contracts, and review tracked changes and clean versions before relying on them.

Risk: The PDF OCR path can automatically install unpinned dependencies.

Mitigation: Disable or review the auto-install path and install pinned dependencies in an isolated environment before processing PDFs.

Risk: Unsafe shell execution may be reachable through document-derived filenames.

Mitigation: Avoid attacker-controlled filenames or suffixes, sanitize input paths, and process only trusted contract files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wux818738-alt/skills/contract-reviewer-wudi)
- [Project homepage](https://github.com/wux818738-alt/contract-reviewer-wudi)
- [Review playbook](references/review-playbook.md)
- [Engine guide](references/engine-guide.md)
- [Output specification](references/output-spec.md)
- [Contract type references](references/contract-types/README.md)
- [Clause library index](references/clause-library/index.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell commands; generated review artifacts include DOCX, TXT, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core file outputs include a tracked-changes DOCX, clean DOCX, text review report, changes JSON, optional structure JSON, and optional comparison report.]

## Skill Version(s):

2.9.5 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
