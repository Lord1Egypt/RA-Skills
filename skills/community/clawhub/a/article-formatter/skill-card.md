## Description: <br>
Formats raw Chinese research report, official document, or general article text into standard Word .docx documents using embedded layout rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunshineorangejuice](https://clawhub.ai/user/sunshineorangejuice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, administrators, and agents use this skill to turn raw Chinese drafts into formatted Word documents for research reports, official documents, and general articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local Word documents that may contain sensitive draft content. <br>
Mitigation: Review or choose the output path before running the skill with sensitive drafts. <br>
Risk: The formatter relies on python-docx to generate .docx files. <br>
Mitigation: Install python-docx only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunshineorangejuice/article-formatter) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance and local Word .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates .docx documents; the default output path is ~/Desktop/openclaw专属文件夹/ unless a custom path is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
