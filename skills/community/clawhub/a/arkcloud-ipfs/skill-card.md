## Description: <br>
ARKCloud IPFS OpenClaw skill for file.arklink.hk that uploads, publishes, lists, and deletes files through ARKCloud and returns IPFS CID, access link, credit usage, and duplicate status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djanngau](https://clawhub.ai/user/djanngau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent manage ARKCloud IPFS uploads, retrieve upload metadata, check API health, list uploaded resources, and delete or unpublish uploads when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload files to ARKCloud, which may expose user-selected content through an access link. <br>
Mitigation: Confirm the exact file and destination before uploading, and do not upload secrets or sensitive files without explicit user confirmation. <br>
Risk: The delete helper can unpublish or delete an upload when provided a valid session, CSRF token, and upload ID. <br>
Mitigation: Confirm the upload_id before destructive actions unless the user explicitly requested the deletion. <br>
Risk: The skill requires ARKCloud credentials, including bearer tokens and optional session cookies. <br>
Mitigation: Keep credentials in local environment variables, avoid sharing them in chat, and never print, store, or commit plaintext tokens, cookies, wallet private keys, seed phrases, or .env files. <br>


## Reference(s): <br>
- [ARKCloud IPFS skill homepage](https://github.com/djanngau/arkcloud-ipfs-skill) <br>
- [ARKCloud file service](https://file.arklink.hk/) <br>
- [ClawHub skill page](https://clawhub.ai/djanngau/arkcloud-ipfs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Upload results can include CID, filename, byte size, access link, credits charged, credits remaining, and duplicate status.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
