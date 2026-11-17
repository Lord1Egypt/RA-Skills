## Description:

Produces concise summaries of Amazon product changes from saved snapshots over supported monitoring periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use the skill to manage periodic product watches and review deterministic change summaries for an ASIN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that paid AI tools and persistent payment settings extend beyond the stated watch-only scope.

Mitigation: Request a watch-only build that blocks unrelated paid and account-setting commands before connecting an ARI account.

Risk: Watch refreshes can create recurring credit charges, and the security review warns that omitting --confirm does not guarantee quote-only behavior for exposed analysis and VOC commands.

Mitigation: Verify current per-refresh prices and recurring schedule estimates before connecting; use only the watch workflow and require explicit approval of the quoted price before creating or resuming a watch.

## Reference(s):

- [Watch workflow](references/watch-workflow.md)
- [Monitoring reference](references/reference.md)
- [ARI monitoring workspace](https://ari.funewa.com/zh/operations)
- [ClawHub release page](https://clawhub.ai/funewa/skills/asin-change)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured watch responses with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic snapshot changes over supported periods; does not provide real-time monitoring or sales, inventory, or advertising data.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
