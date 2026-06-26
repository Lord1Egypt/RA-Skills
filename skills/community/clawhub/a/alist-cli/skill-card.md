## Description: <br>
AList CLI helps agents manage files on an AList server, including login, listing, upload, download, folder creation, delete, move, search, and URL retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to operate an AList-backed cloud storage workspace from the command line. It is useful for authenticated file browsing, upload and download workflows, folder management, search, and generating preview or download URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to configure AList credentials and documentation includes examples that persist secrets in shell startup files. <br>
Mitigation: Use a least-privilege AList account, prefer session-scoped environment variables or a secret manager, and avoid storing passwords in ~/.bashrc. <br>
Risk: Onboarding suggests privileged setup steps such as sudo pip installation or creating a system-wide symlink. <br>
Mitigation: Prefer a non-sudo alias, user-local installation, or virtual environment before using privileged setup commands. <br>
Risk: The CLI can upload, delete, move, and publish file links on a configured remote AList server. <br>
Mitigation: Require explicit user confirmation before destructive file operations, uploads, or public-link actions, and verify target paths before execution. <br>
Risk: Security evidence rates the release as suspicious because remote file changes and credential handling need review. <br>
Mitigation: Install only if the publisher and configured AList server are trusted, and review the skill behavior before deployment. <br>


## Reference(s): <br>
- [AList API specification](references/openapi.json) <br>
- [ClawHub release page](https://clawhub.ai/leeshunee/alist-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AList server URL, username, and password environment variables; generated public or signed links may expire or expose files depending on the configured path.] <br>

## Skill Version(s): <br>
1.6.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
