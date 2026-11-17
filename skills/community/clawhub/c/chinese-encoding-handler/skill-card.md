## Description:

Helps agents guide PowerShell users through Chinese text encoding detection, safe file read/write workflows, and terminal display fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petersunpingww-droid](https://clawhub.ai/user/petersunpingww-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when diagnosing Chinese character garbling in Windows PowerShell workflows, reading or writing Chinese text files, or configuring a terminal for UTF-8 display. Users should verify the referenced PowerShell scripts are present and trusted before running the documented commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation references PowerShell scripts that are not included in the submitted artifact.

Mitigation: Verify the scripts are present in the installed package or obtain them from a trusted source before running any documented commands.

Risk: Permanent terminal fixes may modify PowerShell profile or terminal settings.

Mitigation: Use non-permanent checks first, review the exact changes, and back up the PowerShell profile before using a permanent option.

Risk: Write and batch conversion examples can alter or overwrite files.

Mitigation: Back up target files and test on copies before using write or conversion workflows on important data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/petersunpingww-droid/skills/chinese-encoding-handler)
- [PowerShell character encoding documentation](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_character_encoding)
- [Unicode UTF-8 BOM FAQ](https://www.unicode.org/faq/utf_bom.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include encoding names, file path examples, terminal configuration steps, and cautions for persistent profile changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
