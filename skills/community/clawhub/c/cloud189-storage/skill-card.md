## Description:

Guides an agent through Cloud189 storage tasks, including authentication token retrieval, semantic image search, folder lookup, file listing, file search, and download-link retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngcrazy](https://clawhub.ai/user/youngcrazy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to help users authenticate to Cloud189 and perform cloud-drive operations such as finding folders, listing files, searching by filename or image content, and retrieving download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Cloud189 auth codes, access tokens, and download URLs that can expose account data if stored or shared carelessly.

Mitigation: Treat these values as secrets, prefer temporary in-memory use, and avoid writing them to project files or chat logs unless the user explicitly chooses secure storage.

Risk: Generic cloud-drive requests could trigger Cloud189 authentication when the user intended a different provider.

Mitigation: Confirm Cloud189 is the intended cloud-drive provider before starting authentication or requesting an authorization code.

Risk: Cloud189 operations are constrained to the documented application folder and may fail with permission errors outside that scope.

Mitigation: Keep file lookup, listing, search, and download operations within the documented Cloud189 application folder and explain permission failures clearly.

## Reference(s):

- [Cloud189 Storage Skill on ClawHub](https://clawhub.ai/youngcrazy/skills/cloud189-storage)
- [Cloud189 OAuth Authorization Page](https://cloud.189.cn/web/ecloud-auth/index.html)
- [Cloud189 OAuth Token Endpoint](https://api.cloud.189.cn/open/oauth2/getAccessTokenByCloudCode?authCode={authCode})
- [Cloud189 Unified Skill API Endpoint](https://api.cloud.189.cn/smart/server/api/open/cloud/skills)
- [Authentication workflow](reference/auth.md)
- [Folder lookup workflow](reference/getFolderInfo.md)
- [File listing workflow](reference/listFiles.md)
- [File search workflow](reference/searchFiles.md)
- [Image search workflow](reference/searchImages.md)
- [File download workflow](reference/downloadFile.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step operational guidance for Cloud189 API interactions; returned tokens, file metadata, and download URLs should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
