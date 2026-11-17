## Description:

Start and manage tmux-backed dev servers exposed through Caddy at wildcard subdomains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start, expose, list, restart, and stop local project dev servers through tmux and Caddy-backed wildcard HTTPS routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can persistently modify Caddyfile and Vite configuration files.

Mitigation: Use it only on trusted repositories, review generated file changes, and keep backups or diffs before committing or reusing those changes.

Risk: Crafted project names, domains, or ports could change files or execute commands because of input-handling flaws.

Mitigation: Use simple DNS-safe folder names, a trusted DEV_SERVE_DOMAIN, numeric ports, and review commands before running them.

Risk: Pointing CADDY_ADMIN at an unintended endpoint could reload or affect the wrong Caddy instance.

Mitigation: Keep CADDY_ADMIN restricted to the intended local Caddy admin endpoint.

## Reference(s):

- [Dev Serve ClawHub skill page](https://clawhub.ai/brennerspear/skills/dev-serve)
- [Caddy companion skill](https://clawhub.com/skills/caddy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may edit Caddyfile, state JSON, and Vite configuration files when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
