## Description:

Build with Deno runtime avoiding permission gotchas, URL import traps, and Node.js migration pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for Deno runtime guidance, especially when configuring permissions, managing URL and npm dependencies, and migrating Node.js code to Deno.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deno commands generated from this guidance could grant broader filesystem, network, environment, subprocess, or FFI permissions than intended.

Mitigation: Scope permissions to specific paths, hosts, environment variables, and binaries, and review each command before running it.

Risk: Remote URL or npm dependency guidance could lead to unpinned or unavailable dependencies in production.

Mitigation: Use lockfiles, exact versions, cached dependencies, or vendored dependencies for production workflows.

Risk: CI or automated runs can hang or fail if Deno permission prompts are not handled explicitly.

Mitigation: Use explicit permission flags and no-prompt execution in CI, then test with the same permissions expected in production.

## Reference(s):

- [Deno Skill Page](https://clawhub.ai/ivangdavila/skills/deno)
- [Permission System Traps](artifact/permissions.md)
- [Import and Dependency Traps](artifact/imports.md)
- [Node.js Migration Traps](artifact/node-compat.md)
- [Deno Standard Library Example](https://deno.land/std@0.210.0/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; review generated commands and permission scopes before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
