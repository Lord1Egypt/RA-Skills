## Description:

AList CLI provides file-management commands for AI agents to upload, download, list, create, delete, move, search, and retrieve URLs for files on an AList server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and agent users use this skill to manage files on a configured AList cloud storage server through conversational workflows, including upload, download, browsing, search, sharing-link retrieval, folder creation, deletion, and move operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because setup and login guidance can expose credentials or encourage risky shell handling.

Mitigation: Use only trusted HTTPS AList servers, avoid eval or source of login output, and keep ALIST_PASSWORD out of shell startup files unless the user explicitly approves persistent storage.

Risk: The skill can delete or move files on the connected AList server.

Mitigation: Require explicit user confirmation before rm or mv operations and restate the source and destination paths before running the command.

Risk: Installing dependencies or command aliases can modify the host environment.

Mitigation: Prefer a virtual environment or direct script path, and avoid privileged installation steps unless the user explicitly requests them.

## Reference(s):

- [AList CLI onboarding](references/ONBOARDING.md)
- [AList API specification](references/openapi.json)
- [AList CLI source repository](https://github.com/KinemaClawWorkspace/alist-cli)
- [AList CLI ClawHub page](https://clawhub.ai/leeshunee/skills/alist-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AList paths, file metadata, preview URLs, download URLs, and environment-variable setup guidance.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
