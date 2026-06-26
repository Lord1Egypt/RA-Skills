## Description: <br>
Upload files to the litterbox.catbox.moe file sharing service and get shareable URLs (72h expiry). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RaphaCastelloes](https://clawhub.ai/user/RaphaCastelloes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other external users use this skill to upload a local file through a Node.js command-line tool and receive a temporary public sharing URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected file is uploaded to a public third-party temporary hosting service and can be accessed by anyone with the URL. <br>
Mitigation: Do not upload secrets, credentials, private documents, regulated data, or files that require access control. <br>
Risk: A mistaken file path could upload the wrong local file. <br>
Mitigation: Verify the file path and file contents before running the upload command. <br>
Risk: The upload depends on curl, internet access, and the availability of litterbox.catbox.moe. <br>
Mitigation: Use this for temporary sharing workflows only, and retry later or choose another transfer method when the service or network is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RaphaCastelloes/file-upload-cli) <br>
- [Litterbox upload API endpoint](https://litterbox.catbox.moe/resources/internals/api.php) <br>
- [Catbox service site](https://catbox.moe) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and upload URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The upload command returns a public URL for a single file that expires after 72 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
