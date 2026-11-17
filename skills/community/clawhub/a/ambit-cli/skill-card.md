## Description:

Guides agents through Ambit CLI workflows for creating and destroying private networks, deploying apps, checking router health, listing routers, and diagnosing connectivity issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toxicpine](https://clawhub.ai/user/toxicpine)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to operate Ambit CLI workflows for private Fly.io deployments reachable only through Tailscale. It supports network creation, app deployment, router status checks, troubleshooting, and teardown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Fly.io and Tailscale network changes.

Mitigation: Review planned changes before execution, avoid --yes for destructive or routing operations, and confirm the Fly.io organization, Tailscale ACL tags, autoApprovers, and network names.

Risk: The skill may deploy mutable third-party templates or container images.

Mitigation: Use reviewed immutable commits or pinned images, and keep Fly.io and Tailscale permissions narrow.

Risk: Tailscale API tokens may be exposed if passed on the command line.

Mitigation: Use interactive prompts or managed secret handling, and avoid exposing tokens through shell history or shared logs.

## Reference(s):

- [ClawHub Ambit Cli Skill](https://clawhub.ai/toxicpine/skills/ambit-cli)
- [Tailscale API Access Tokens](https://login.tailscale.com/admin/settings/keys)
- [Tailscale ACL Tags](https://login.tailscale.com/admin/acls/visual/tags)
- [Tailscale ACL Access Rules](https://login.tailscale.com/admin/acls/visual/general-access-rules)
- [Flyctl Installation](https://fly.io/docs/flyctl/install/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command guidance when the Ambit CLI --json flag is relevant.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
