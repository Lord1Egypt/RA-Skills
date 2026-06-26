## Description: <br>
Helps agents provide PowerShell guidance for detecting Chinese text encodings, reading and writing Chinese files safely, and fixing terminal display settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petersunpingww-droid](https://clawhub.ai/user/petersunpingww-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when working with Chinese-language files in PowerShell, especially when they need encoding detection, safe read/write examples, or terminal UTF-8 configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the package references PowerShell scripts that may be missing or replaced by another source. <br>
Mitigation: Inspect any supplied scripts before running them and do not execute replacement scripts from another source without review. <br>
Risk: Write and batch-conversion examples can overwrite or transform user files. <br>
Mitigation: Back up files first and prefer check, read-only, or small-sample runs before write or batch-conversion workflows. <br>
Risk: Terminal repair examples can permanently modify PowerShell profile or terminal settings. <br>
Mitigation: Prefer non-permanent checks first, use -Check or temporary settings where possible, and review any -Permanent profile changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/petersunpingww-droid/chinese-encoding-handler) <br>
- [Publisher profile](https://clawhub.ai/user/petersunpingww-droid) <br>
- [PowerShell character encoding documentation](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_character_encoding) <br>
- [Unicode UTF-8 BOM FAQ](https://www.unicode.org/faq/utf_bom.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, encoding names, and PowerShell flags such as -Check, -Reset, and -Permanent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
