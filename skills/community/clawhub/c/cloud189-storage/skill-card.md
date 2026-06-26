## Description: <br>
Helps an agent work with Cloud189 storage by guiding authentication, semantic image search, folder lookup, file listing, file search, and file download-link retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngcrazy](https://clawhub.ai/user/youngcrazy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to authorize access to a Cloud189 account and locate, list, search, and retrieve files in permitted Cloud189 folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Cloud189 authorization codes, access tokens, thumbnail URLs, and download links that can expose private account data. <br>
Mitigation: Use it only for intentional Cloud189 requests, keep credentials and generated links private, and avoid storing tokens unless the user approves a trusted secure location. <br>
Risk: The skill asks agents to collect and persist cloud access tokens with weak scoping and safeguards. <br>
Mitigation: Prefer session-scoped or explicitly approved environment/config storage, remove expired tokens, and re-authenticate when needed. <br>
Risk: File lookup and download workflows can return private file metadata or download links. <br>
Mitigation: Confirm the intended provider, folder, file ID or path, and user intent before API calls or returning download links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youngcrazy/cloud189-storage) <br>
- [Authentication workflow](reference/auth.md) <br>
- [Image search guide](reference/searchImages.md) <br>
- [Folder lookup guide](reference/getFolderInfo.md) <br>
- [File listing guide](reference/listFiles.md) <br>
- [File search guide](reference/searchFiles.md) <br>
- [File download guide](reference/downloadFile.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include access tokens, file identifiers, thumbnail URLs, and download links that should be treated as private.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
