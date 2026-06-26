## Description: <br>
Interacts with the Forge AI platform to manage authentication, articles, evaluations, tags, and file uploads through the Forge AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scemoon](https://clawhub.ai/user/scemoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Forge AI content from an agent session, including logging in, preparing JSON payloads, listing local article and evaluation files, creating or updating Forge records, managing tags, and uploading selected files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists authentication tokens in .forgeai/session.json. <br>
Mitigation: Treat .forgeai/session.json as sensitive, avoid using synced or shared directories, and run logout when finished. <br>
Risk: The skill can create or update remote Forge AI content from raw JSON payloads. <br>
Mitigation: Review JSON files before execution and confirm the target action before creating or updating Forge records. <br>
Risk: The skill can upload user-selected files to the Forge AI service. <br>
Mitigation: Upload only files explicitly intended for Forge AI and confirm the storage path before execution. <br>


## Reference(s): <br>
- [Forge AI Skill release page](https://clawhub.ai/scemoon/forge-skill) <br>
- [Publisher profile](https://clawhub.ai/user/scemoon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .forgeai state files and may send user-selected JSON payloads or files to Forge AI when executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
