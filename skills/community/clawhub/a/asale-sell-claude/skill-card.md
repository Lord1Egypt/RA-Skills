## Description:

Lists a Claude Code or Claude subscription on the asale market, with account import, price floor, concurrency cap, and lane status guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide selling a Claude Code or Claude subscription through asale by importing local credentials, setting sale limits, and checking which model lanes are active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide selling access to a paid Claude subscription by importing local Claude or opencode credentials.

Mitigation: Install and use it only after confirming the exact account, price floor, concurrency, and daily cap before enabling selling.

Risk: The provided install and update paths use remote scripts.

Mitigation: Avoid running pipe-to-shell installers unless the script source and expected behavior have been independently verified.

Risk: The skill reads a local daemon token used for loopback RPC calls.

Mitigation: Keep the token local, verify the daemon endpoint is loopback, and stop if authentication or sign-in errors occur.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-sell-claude)
- [asale homepage](https://asale.ai)
- [asale source link from skill metadata](https://github.com/asale-ai/asale)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, a local asale daemon token, and user confirmation before lowering price floors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
