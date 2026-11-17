## Description:

Monitor your brand's AI visibility via BotSee API

This skill is ready for commercial/non-commercial use.

## Publisher:

[grahac](https://clawhub.ai/user/grahac)

### License/Terms of Use:


## Use Case:

External developers and marketing teams use BotSee to manage BotSee API workflows for brand visibility analysis, AI search results, competitive findings, and generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved API keys can be sent to an environment-selected API host if BOTSEE_BASE_URL is set.

Mitigation: Leave BOTSEE_BASE_URL unset unless it points to a trusted BotSee-controlled endpoint, and avoid pasting live API keys into chat.

Risk: The skill exposes non-interactive billing, top-up, analysis, and content commands that can spend credits or initiate payments.

Mitigation: Check the account balance first and require explicit user approval before commands that spend credits or start payment flows.

Risk: Archive and delete commands can make remote account changes.

Mitigation: Confirm target UUIDs and user intent before running archive-site, archive-type, archive-persona, or delete-question.

## Reference(s):

- [BotSee ClawHub skill page](https://clawhub.ai/grahac/skills/botsee)
- [BotSee homepage](https://botsee.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with shell commands, human-readable CLI text, JSON API result payloads, and saved markdown/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API credentials to ~/.botsee/config.json, workspace configuration to .context/botsee-config.json, and generated content as timestamped Markdown.]

## Skill Version(s):

0.2.5 (source: frontmatter, plugin manifest, CHANGELOG released 2026-02-24, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
