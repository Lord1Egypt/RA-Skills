## Description: <br>
File Organizer automatically groups files by type into folders such as images, documents, code, videos, audio, archives, and others. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People managing local folders use this skill to inspect file-type statistics and organize common directories such as Desktop, Downloads, Documents, or an explicitly provided Windows path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move many files in common folders without a preview or undo step. <br>
Mitigation: Test on a small folder first and use statistics or view mode before organizing important directories. <br>
Risk: Files may be reorganized into category folders in a way the user did not intend. <br>
Mitigation: Use an explicit target path and review the folder contents before allowing file moves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/file-organizer-zh) <br>
- [Publisher profile](https://clawhub.ai/user/huangjingzhi07) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text status messages and file statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report moved files, skipped errors, target folders, file counts, and aggregate sizes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
