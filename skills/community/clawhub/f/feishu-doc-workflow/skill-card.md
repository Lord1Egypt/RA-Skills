## Description: <br>
Feishu document writing and formatting workflow for rewriting Feishu docx content, polishing sections, inserting images, positioning block-level edits, adding links, setting public read access, and troubleshooting Feishu document 400/403 write issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users with a configured Feishu integration use this skill to edit, format, illustrate, share, and troubleshoot Feishu docx documents through Feishu document tools and Drive permission APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-link sharing can expose Feishu documents outside the intended audience. <br>
Mitigation: Before enabling public read access, verify the exact document and confirm it contains no confidential, internal, personal, or regulated data; prefer narrower Feishu sharing when public access is not necessary. <br>
Risk: Document edits or image insertions can overwrite content or place blocks incorrectly. <br>
Mitigation: Read the document and list blocks before editing, use localized update or insert operations when possible, and re-read or list blocks after changes to confirm placement. <br>
Risk: Write failures can occur when Feishu scopes or document-level app permissions are incomplete. <br>
Mitigation: Verify the documented Feishu scopes and confirm the specific document grants the app edit access before write, append, update, insert, or image operations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Feishu tool actions, API request details, JSON permission payloads, and troubleshooting steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to read, update, append, insert, upload images, delete blocks, and verify Feishu document public permission settings when the user asks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
