## Description:

Use when user wants to add items to Bring! shopping lists. For adding single items, batch items, or items from stdin/files. Supports dry-run preview and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkdevelopers](https://clawhub.ai/user/darkdevelopers)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to add one or more items to Bring! shopping lists from an agent-controlled command line, including batch, stdin, dry-run, and JSON-output workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bring! account credentials may be exposed because the CLI requires BRING_EMAIL and BRING_PASSWORD.

Mitigation: Use the least-privileged Bring! account available, avoid shared shell profiles and CI logs, and unset credentials after use.

Risk: Dependency setup needs review because bring-shopping is unpinned and the lockfile points to a local linked path outside the package.

Mitigation: Pin or replace the dependency with a reviewed registry version that includes an integrity hash before installation.

Risk: The CLI can modify Bring! shopping lists when invoked.

Mitigation: Use --dry-run for previews and pass an explicit list name or UUID when list selection matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI workflows can emit plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bring! account credentials and supports dry-run previews before modifying a shopping list.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json, and package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
