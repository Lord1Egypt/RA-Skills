## Description:

flightroutes24 ai helps agents parse international flight requests, search demo or procurement fares, verify offers, and place explicitly confirmed orders through Flightroutes24.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mafly](https://clawhub.ai/user/mafly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to search international flight options, refine results by airline or departure time, and proceed to booking only after required user confirmations. Developers can install it into agent environments such as Cursor or Claude Code and configure procurement credentials locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive booking data and credentials may be stored in local cache or configuration files.

Mitigation: Use the skill only in a protected workspace, keep .cache and local credential files out of sharing and version control, and clear local secrets when no longer needed.

Risk: Bundled local agent permissions allow git remote add and git push commands.

Mitigation: Remove or review the bundled .claude permissions before installation unless those Git actions are explicitly required.

Risk: Booking actions can create real orders.

Mitigation: Require the documented passenger confirmation and final order confirmation before running verification or order commands.

Risk: Internal script output can contain trace IDs, offer IDs, payloads, or local paths.

Mitigation: Show users only the documented message and userView fields, and keep agentOnly and raw stdout out of user-facing exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mafly/skills/fr24-ai)
- [Flightroutes24](https://www.flightroutes24.com/)
- [README.en.md](artifact/README.en.md)
- [INSTALL.md](artifact/INSTALL.md)
- [Booking workflow](artifact/references/booking.md)
- [Output rules](artifact/references/output-rules.md)
- [Search parameters](artifact/references/search_params.md)
- [User APPKEY configuration](artifact/references/user-appkey-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON script output with user-facing message/userView fields, plus Markdown guidance and shell commands for agent operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing internal fields such as agentOnly and local cache paths are not intended for user-visible output.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
