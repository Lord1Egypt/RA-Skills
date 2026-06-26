## Description: <br>
Uploads local files or remote URLs to Cloudinary with optional automatic image compression and batch upload support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnhkahn](https://clawhub.ai/user/mnhkahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run a Cloudinary CLI uploader for local files or remote URLs, including image compression and batch uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudinary credentials are stored in a project-local cmd/cli/.env file. <br>
Mitigation: Use least-privilege Cloudinary keys, keep the .env file gitignored and out of logs, restrict file permissions, and rotate keys if exposure is possible. <br>
Risk: The skill uploads local files or remote URLs to Cloudinary, which may expose data to an external service. <br>
Mitigation: Review input paths, remote URLs, destination folder, and account before upload; avoid uploading sensitive files unless the user has approved it. <br>


## Reference(s): <br>
- [Go Downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run a local Go CLI that reads Cloudinary credentials from cmd/cli/.env and returns command-line status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
