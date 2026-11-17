## Description:

Agent Hush is a local privacy scanner for agent workspaces that checks outbound actions such as git pushes, skill publishing, and file sharing for sensitive data leaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliotllliu](https://clawhub.ai/user/elliotllliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Agent Hush to scan local workspaces before code pushes, skill publication, file sharing, or explicit privacy checks. It helps identify secrets, PII, infrastructure details, and other sensitive content before files leave the local environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run workspace scans silently, which can surprise users or cover files beyond the immediate outbound action.

Mitigation: Prefer explicit scans of the exact files being pushed, published, or shared, and avoid heartbeat or background scanning unless users have clearly accepted that behavior.

Risk: The artifact includes commands that can change files, update allowlists, create sanitized exports, or overwrite an export destination with --force.

Mitigation: Review proposed edits and .sanitize.json allowlist changes before applying them, keep backups, and use export --force only on a disposable destination outside the source tree.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elliotllliu/skills/agent-hush)
- [Installation guide](docs/install.md)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise user-facing findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local scan results, proposed redactions, allowlist configuration changes, sanitized file copies, or in-place edits when the user approves.]

## Skill Version(s):

1.2.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
