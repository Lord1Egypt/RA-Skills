## Description:

Print images and PDFs to any CUPS printer with PPD-aware settings for paper sizes, margins, resolution, and duplex, and query printer capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to list CUPS printers, inspect printer capabilities, and submit PDF or image print jobs with printer-aware options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit CUPS print jobs on the host machine.

Mitigation: Install and run it only where agent-submitted print jobs are acceptable, and review the selected printer, file, and CUPS options before execution.

Risk: Image printing depends on Pillow to convert images before sending them to CUPS.

Mitigation: Use a virtual environment and a reviewed or pinned Pillow version.

Risk: Custom CUPS options can affect media selection, duplexing, quality, trays, and other printer behavior.

Mitigation: Use the options command to inspect supported values and pass only CUPS options the operator understands.

## Reference(s):

- [Setup](SETUP.md)
- [ClawHub Skill Page](https://clawhub.ai/odrobnik/skills/cups-printer)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit CUPS print jobs and can emit machine-readable JSON for list, info, options, and print commands.]

## Skill Version(s):

1.2.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
