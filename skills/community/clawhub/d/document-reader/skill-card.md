## Description: <br>
Document Reader extracts text from common document formats and selected files inside ZIP, TAR, RAR, and 7z archives for agent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaliu00](https://clawhub.ai/user/xiaoyaliu00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to inspect office documents, text files, and selected archive members without manually converting or extracting them first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local documents or archive members selected by the user or agent, which may expose confidential content in shared environments. <br>
Mitigation: Run it only against intended files in an isolated environment and avoid processing confidential files on shared machines. <br>
Risk: Broad document and archive parsing can carry risk when inputs are untrusted or malformed. <br>
Mitigation: Avoid untrusted archives and documents, keep parser dependencies updated, and review extracted content before relying on it. <br>
Risk: Archive member reads use temporary files, and the security guidance calls out implementation risk around temporary file handling. <br>
Mitigation: Patch the script to use secure temporary files before handling sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill page: document-reader](https://clawhub.ai/xiaoyaliu00/document-reader) <br>
- [ClawHub publisher profile: xiaoyaliu00](https://clawhub.ai/user/xiaoyaliu00) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [Plain text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archive reads require an explicit inner path; long text output may be truncated in the command-line display.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
