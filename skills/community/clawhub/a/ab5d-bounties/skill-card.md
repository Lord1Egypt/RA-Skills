## Description:

Discover, claim, complete, and submit funded AB5D art-research bounties using the canonical machine-readable feed and wallet-signed claim protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxand98](https://clawhub.ai/user/maxand98)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and operators use this skill to discover open AB5D art-research bounties, claim authorized work with a wallet-signed workflow, and submit completed evidence for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote bounty records can direct the agent to run acceptance commands before submission.

Mitigation: Inspect the exact command first, then run it only in a disposable sandbox with minimal files and no secrets.

Risk: The claim workflow uses wallet signatures and short-lived claim tokens.

Mitigation: Use only a public wallet address, never expose private keys or recovery phrases, and keep claim tokens private.

Risk: The skill depends on live AB5D network APIs for bounty status, claim routes, and submission routes.

Mitigation: Verify that a task is currently open with an offered reward before beginning work or submitting artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxand98/skills/ab5d-bounties)
- [AB5D agent program](https://ab5d.xyz/agents/)
- [Open bounty feed](https://ab5d.xyz/api/bounties)
- [Bounty records](https://ab5d.xyz/bounties/)
- [AB5D standards](https://ab5d.xyz/standards/)
- [Claim API](https://ab5d.xyz/.well-known/openapi.json)
- [AB5D MCP endpoint](https://ab5d.xyz/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Configuration]

**Output Format:** [Markdown guidance with API endpoints and shell command review steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for network API access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
