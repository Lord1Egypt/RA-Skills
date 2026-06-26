## Description: <br>
Use the ClawBox CLI to upload, download, organize, search, and share files on ClawBox (clawbox.ink) or a self-hosted ClawBox server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyoooo](https://clawhub.ai/user/bennyoooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage cloud or self-hosted ClawBox files from the CLI, including uploads, downloads, folder organization, semantic search, sharing links, and token or quota checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide uploads to a third-party cloud file service where sensitive files may be stored or shared. <br>
Mitigation: Avoid uploading sensitive files to clawbox.ink unless the user trusts the service; prefer self-hosting for private data. <br>
Risk: ClawBox tokens grant access to stored files and can be exposed through copied logs or shared shell history. <br>
Mitigation: Treat tokens as secrets and redact them from logs, transcripts, and shared command output. <br>
Risk: Upload, share, and delete commands can mutate remote storage or expose files through share links. <br>
Mitigation: Confirm uploads, shares, and deletions before running them, and prefer non-destructive inspection commands first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bennyoooo/clwbox) <br>
- [ClawBox API Reference](references/api.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawBox service](https://clawbox.ink) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report file IDs, download paths, share links, status output, and token or quota state after CLI operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
