## Description: <br>
Read-only file browsing and reading in the OpenClaw workspace for listing directories or reading text files up to 10k characters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nagilem](https://clawhub.ai/user/Nagilem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect workspace contents without granting write, delete, or arbitrary execution capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports weak workspace containment for a read-only file browser. <br>
Mitigation: Install only in workspaces where read access is acceptable, and harden path resolution, symlink handling, and JSON encoding before sensitive use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown text summarizing directory listings, file contents, or read errors from JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads are limited to text output up to 10k characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
