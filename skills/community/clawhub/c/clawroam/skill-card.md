## Description:

Portable identity vault for OpenClaw that syncs knowledge, packages, and memory across machines with automatic, encrypted sync through user-managed storage or ClawRoam Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlighty](https://clawhub.ai/user/getlighty)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent developers use this skill to keep an agent vault, knowledge, memory, package inventory, and migration state synchronized across multiple machines while choosing managed or bring-your-own storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports high-impact authentication and scoping concerns in a skill that syncs OpenClaw data.

Mitigation: Do not install on machines with sensitive OpenClaw data until the maintainer resolves the cloud authentication flow and narrows sync behavior to an explicit allowlist.

Risk: The security evidence warns about curl-to-bash installers, eval-based package installs, and disabled SSH host key verification.

Mitigation: Test only with a throwaway vault and non-sensitive provider account, and manually review generated commands before execution.

Risk: The skill can interact with private credentials, session files, storage providers, and managed cloud sync.

Mitigation: Use no private credentials or sensitive session files during evaluation, and prefer isolated test accounts until security issues are remediated.

## Reference(s):

- [ClawRoam ClawHub listing](https://clawhub.ai/getlighty/skills/clawroam)
- [Publisher profile](https://clawhub.ai/user/getlighty)
- [ClawRoam Cloud API endpoint](https://clawroam-api.ovisoftblue.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file operations, provider setup commands, sync status checks, migration steps, and package installation commands.]

## Skill Version(s):

3.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
