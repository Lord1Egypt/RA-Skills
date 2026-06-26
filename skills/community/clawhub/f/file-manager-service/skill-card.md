## Description: <br>
File Manager Service starts and stops a local Flask file manager and provides web, CLI, and API access for browsing, uploading, downloading, editing, searching, and organizing files under the OpenClaw projects directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lengyhua](https://clawhub.ai/user/lengyhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage project files through a local web interface, command-line helper, or HTTP API. It supports file browsing, text editing, upload and download, search, directory notes, and service lifecycle commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful file-changing APIs with under-scoped network and upload protections. <br>
Mitigation: Use it only in a trusted local environment, bind the service to 127.0.0.1, stop it when finished, and add authentication or request protection before broader use. <br>
Risk: Uploaded or viewed HTML/SVG content and unsanitized upload filenames can create avoidable local-file or browser exposure. <br>
Mitigation: Avoid opening untrusted HTML or SVG through the UI, sanitize upload filenames, validate final paths, and prefer a fixed version that pins or self-hosts browser dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lengyhua/file-manager-service) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local web service and modify files under ~/.openclaw/workspace/projects.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
