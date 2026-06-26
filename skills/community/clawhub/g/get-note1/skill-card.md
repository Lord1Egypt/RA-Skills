## Description: <br>
GetNote is a personal notes and knowledge-base skill that lets an agent save text, links, and images, manage tags and knowledge bases, and semantically search private notes through the Get笔记 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Deuscx](https://clawhub.ai/user/Deuscx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent capture, retrieve, organize, and search personal GetNote notes, links, image notes, tags, and knowledge-base content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private personal notes and knowledge-base content. <br>
Mitigation: Install only if the user trusts GetNote and openapi.biji.com, keep GETNOTE_API_KEY out of chat, and configure GETNOTE_OWNER_ID in shared or group settings. <br>
Risk: The skill can trash notes, change tags, and run broad searches over private content. <br>
Mitigation: Ask the user to confirm before deleting notes, changing tags, or performing broad searches that may expose sensitive note contents. <br>
Risk: Link and image note creation can involve asynchronous processing and external content handling. <br>
Mitigation: Tell the user when processing is pending, poll task status before reporting completion, and show only the resulting content needed for the user's request. <br>


## Reference(s): <br>
- [GetNote ClawHub release](https://clawhub.ai/Deuscx/get-note1) <br>
- [GetNote homepage](https://biji.com) <br>
- [GetNote OpenAPI base URL](https://openapi.biji.com) <br>
- [GetNote API details](references/api-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API request details, JSON payloads, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GETNOTE_API_KEY as the primary environment credential and optional GETNOTE_CLIENT_ID and GETNOTE_OWNER_ID settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
