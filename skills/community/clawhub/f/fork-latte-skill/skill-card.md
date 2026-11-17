## Description:

Collects coffee chat signup details, checks for duplicate WeChat IDs, and writes new or updated records to a Feishu Bitable through a relay service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moljay](https://clawhub.ai/user/moljay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and event organizers use this agent to collect registration details, deduplicate by WeChat ID, and submit updates or new rows to a Feishu Bitable. Operators need to run or configure the relay service that holds the Feishu credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay can read and write the configured Feishu table.

Mitigation: Install only after confirming the publisher is trusted and the target Feishu table is appropriate for this access.

Risk: The bundled configuration includes a shared API key and local relay endpoint.

Mitigation: Replace the published API key with a unique secret and require authentication before exposing the relay.

Risk: Hidden relay auto-start and infinite restart behavior can make local execution less visible to users.

Mitigation: Disable hidden auto-start and long-running restart behavior unless the operator explicitly manages the relay process.

Risk: The lark_cli mode invokes shell-backed commands and writes temporary payload files.

Mitigation: Prefer the Feishu API mode for hosted use, review command execution paths, and run the relay with least-privilege credentials.

Risk: The ping shortcut can return a deployment-style confirmation that does not plainly describe the signup action.

Mitigation: Use a truthful signup confirmation that clearly states whether a record was created or updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moljay/skills/fork-latte-skill)
- [Skill README](artifact/README.md)
- [Relay server README](artifact/relay-server/README.md)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit or update signup records through a configured relay endpoint after collecting name, job, WeChat ID, and startup-experience fields.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
