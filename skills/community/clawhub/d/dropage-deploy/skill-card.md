## Description: <br>
Deploys a selected HTML file or supported site archive to Dropage and returns a temporary public URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiantoucn](https://clawhub.ai/user/jiantoucn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to publish a single HTML page or supported site archive to a temporary public Dropage URL for sharing, preview, or lightweight hosting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files or archives become publicly accessible through a Dropage URL. <br>
Mitigation: Review files before upload and do not deploy confidential pages, embedded secrets, internal documents, private assets, or anything not intended for public access. <br>
Risk: A deployed page can remain reachable until its expiration time or visit limit is reached. <br>
Mitigation: Choose the shortest suitable expiry and set a visit limit when the page should only be available briefly. <br>
Risk: Unsupported, oversized, or incorrectly packaged archives can fail deployment and consume rate-limit attempts. <br>
Mitigation: Verify the file type, 10 MB size limit, root-level index.html requirement, and 50-file archive limit before uploading. <br>


## Reference(s): <br>
- [Dropage Deploy on ClawHub](https://clawhub.ai/jiantoucn/skills/dropage-deploy) <br>
- [Dropage upload API](https://dropage.online/api/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with curl commands and parsed JSON response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the public URL, expiration time, visit limit when configured, or the API error reason.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
