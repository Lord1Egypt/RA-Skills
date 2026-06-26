## Description: <br>
Bonds provides a local command-line interface for recording bond-related notes, viewing recent activity and statistics, searching entries, and exporting saved logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this as a local personal-finance note and logging utility for bond-related entries, searches, summaries, and exports. It should not be treated as a real bond-analysis or portfolio-management system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as bond analysis, while security evidence says it mostly acts as a generic plaintext input logger for potentially sensitive financial data. <br>
Mitigation: Use it only as a local note and logging tool; verify any financial analysis with a separate trusted portfolio or bond-analysis system. <br>
Risk: Entered data and history are stored in plaintext under ~/.local/share/bonds. <br>
Mitigation: Do not enter account numbers, credentials, or sensitive portfolio details, and review or remove local stored data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/bonds) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and terminal text or local export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local plaintext logs under ~/.local/share/bonds and can export JSON, CSV, or TXT files.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
