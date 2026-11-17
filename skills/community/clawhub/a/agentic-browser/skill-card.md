## Description:

Agent Browser helps agents automate browser workflows through inference.sh, including navigation, element interaction with @e refs, screenshots, video recording, uploads, proxy use, and JavaScript execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate web browsing tasks such as data extraction, form submission, UI testing, authenticated workflows, screenshots, and video-based debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start installs a CLI through a remote shell command, which can expose users to remote code execution risk if the installer path is not verified.

Mitigation: Review the inference.sh CLI installer through a verified manual path and use the published checksums before installation.

Risk: Authenticated browsing can involve credentials, cookies, session IDs, screenshots, videos, uploads, and proxy details in a hosted browser workflow.

Mitigation: Use test accounts where possible, avoid exporting or printing cookies, handle captured files as sensitive data, and close sessions promptly.

Risk: Browser automation can access private, regulated, or third-party sites and may violate site policies or data-handling requirements if used without authorization.

Mitigation: Use the skill only on sites and accounts where automation is permitted and avoid private or regulated sites without explicit approval.

## Reference(s):

- [Command Reference](artifact/references/commands.md)
- [Snapshot and Refs](artifact/references/snapshot-refs.md)
- [Session Management](artifact/references/session-management.md)
- [Authentication Patterns](artifact/references/authentication.md)
- [Video Recording](artifact/references/video-recording.md)
- [Proxy Support](artifact/references/proxy-support.md)
- [inference.sh](https://inference.sh)
- [inference.sh Sessions](https://inference.sh/docs/extend/sessions)
- [Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with bash snippets and JSON examples; browser calls return JSON plus screenshot or video files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Templates may create text extraction files, link files, screenshot JSON, and session-video JSON.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
