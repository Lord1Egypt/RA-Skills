## Description:

Extracts and cleans text from CAD DXF building and structural drawings, including normalization of TSSD-style rebar symbols into standard labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Construction cost estimators, structural engineers, and CAD-processing agents use this skill to extract TEXT, MTEXT, and ATTRIB annotations from DXF drawings into a complete Markdown report for downstream quantity and feature matching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags silent installation of an unpinned Python dependency at runtime.

Mitigation: Preinstall and pin ezdxf in an isolated environment, review the skill before installation, and run it only on DXF files intentionally provided by the user.

Risk: DXF parsing may fail or produce unresolved CAD symbol encodings for damaged files, binary DWG inputs, or project-specific fonts.

Mitigation: Convert DWG files to a valid DXF format before use, preserve the full extraction output for review, and update the documented symbol map only after confirming unknown symbols with the user.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/lialia691691-alt/skills/dxf-text-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown extraction report with line-oriented drawing text and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The extraction script writes a UTF-8 Markdown report named from the input DXF file and preserves extracted drawing text without agent summarization.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
