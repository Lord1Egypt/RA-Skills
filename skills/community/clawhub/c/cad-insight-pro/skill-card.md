## Description:

CAD洞察专家 helps agents analyze PDF and DWG engineering drawings by extracting title blocks, dimensions, annotations, symbols, scales, quality findings, and quantity takeoff reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CAD reviewers, estimators, and engineering teams use this skill to convert PDF and DWG drawings into structured drawing metadata, quality checks, reports, and quantity takeoff outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file access, command execution, credential handling, and external API behavior without enough scope or user-control detail.

Mitigation: Use it only for local CAD/PDF/DWG analysis, dependency setup, and explicitly requested report exports; confirm output filenames and commands before allowing writes or shell use, and do not provide credentials unless a trusted service and data flow are clarified.

Risk: OCR, scale detection, and automated quantity takeoff can produce incorrect drawing measurements or compliance findings.

Mitigation: Review low-confidence OCR items, detected scales, drawing-quality findings, and exported takeoff quantities before relying on results for engineering, estimating, or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cad-insight-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured text, code snippets, shell command blocks, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report-export guidance or file-write instructions when explicitly requested by the user.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
