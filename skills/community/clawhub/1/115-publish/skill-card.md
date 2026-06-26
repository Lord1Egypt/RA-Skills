## Description: <br>
Provides conversational management for 115 cloud drive accounts, including QR login, file browsing and search, share transfer, offline downloads, file organization, storage checks, and cleanup advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukris](https://clawhub.ai/user/sukris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage a 115 cloud drive account through chat-driven commands for login, browsing, search, transfer, offline download, storage review, and organization tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles 115 account cookies and stores session material locally. <br>
Mitigation: Install only from a trusted publisher, confirm cookies can be cleared, and avoid sharing logs or outputs that may contain account identifiers. <br>
Risk: Network authentication and API calls can expose account activity to the 115 service and depend on correct TLS handling. <br>
Mitigation: Review or patch TLS verification before use and restrict execution to trusted networks and machines. <br>
Risk: Bulk file moves, deletes, recycle-bin clearing, share transfers, and offline-download cleanup can change or remove user data. <br>
Mitigation: Require a preview, target-path check, and explicit user confirmation before any destructive or bulk operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sukris/115-publish) <br>
- [Publisher profile](https://clawhub.ai/user/sukris) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, files, configuration, guidance] <br>
**Output Format:** [Markdown-style conversational responses with status summaries, prompts, and result lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send QR-code image data during login and may save encrypted account cookies on the user's machine.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
