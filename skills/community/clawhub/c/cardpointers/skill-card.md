## Description:

Query CardPointers card recommendations, wallet cards, and offers via the CardPointers CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emcro](https://clawhub.ai/user/emcro)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to choose credit cards for purchases, inspect wallet cards, search and filter offers, and compare rewards across linked CardPointers profiles. It requires a CardPointers+ subscription and an authenticated CardPointers CLI session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CardPointers CLI stores and uses a login token for account data access.

Mitigation: Install only from trusted CardPointers sources, run with normal user privileges, avoid sharing logs that may contain sensitive output, and run cardpointers logout when the token should be cleared.

Risk: Recommendations, wallet cards, and offers can expose personal financial account information.

Mitigation: Use the skill only with authorized CardPointers accounts and review outputs before sharing them outside the intended session.

## Reference(s):

- [CardPointers CLI](https://cardpointers.com/cli/)
- [CardPointers ClawHub Skill](https://clawhub.ai/emcro/skills/cardpointers)
- [emcro Publisher Profile](https://clawhub.ai/user/emcro)
- [CardPointers MCP Endpoint](https://mcp.cardpointers.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CardPointers CLI commands, filters, profile selectors, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
