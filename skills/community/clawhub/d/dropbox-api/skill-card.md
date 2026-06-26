## Description: <br>
Dropbox API integration with managed OAuth for files, folders, search, metadata, and cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Dropbox files and folders through Maton-managed OAuth, including listing, searching, uploading, downloading, moving, deleting, and reading metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, upload, move, and delete Dropbox data through Maton-managed OAuth. <br>
Mitigation: Confirm exact Dropbox paths before uploads, moves, deletes, and batch operations. <br>
Risk: The skill requires a sensitive MATON_API_KEY and can return temporary Dropbox download links. <br>
Mitigation: Avoid sharing logs containing MATON_API_KEY or temporary links, and revoke unused Dropbox connections when finished. <br>
Risk: Dropbox access is brokered through Maton rather than directly through Dropbox credentials in the skill. <br>
Mitigation: Install only when the operator trusts Maton to broker Dropbox access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/dropbox-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [Dropbox HTTP API overview](https://www.dropbox.com/developers/documentation/http/overview) <br>
- [Dropbox Developer Portal](https://www.dropbox.com/developers) <br>
- [Dropbox API Explorer](https://dropbox.github.io/dropbox-api-v2-explorer/) <br>
- [DBX File Access Guide](https://developers.dropbox.com/dbx-file-access-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, curl, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; Dropbox content endpoints use binary request bodies with Dropbox-API-Arg headers.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
