## Description:

This skill teaches an agent how to operate the Clawpatch CLI for automated repository review, structured findings, and controlled per-finding fixes when Clawpatch is explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when a user explicitly asks to run Clawpatch, review its findings, choose a scanner-only or full-cycle fix path, and avoid known workflow hazards around provider CLIs and repository state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running Clawpatch requires trusting an npm package and the skills installer.

Mitigation: Prefer pinned package versions, avoid running install commands as root, and review the install source before use.

Risk: Provider CLIs can access repository contents during review or fix workflows.

Mitigation: Authenticate providers deliberately, choose providers appropriate for the repository, and treat full-repo review as code exposure.

Risk: Automated fixes can modify project code or act on false-positive findings.

Mitigation: Require user selection before fixing, keep worktrees clean for full-cycle fixes, validate changes with tests, and avoid parallel Clawpatch fixes on shared state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmchow/skills/clawpatch)
- [Clawpatch homepage](https://clawpatch.ai)
- [Clawpatch upstream project](https://github.com/openclaw/clawpatch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented parsing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for an agent; does not itself install Clawpatch or authenticate provider CLIs.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
