## Description:

BanditDB is an in-memory decision database for AI agents - real-time learning from outcomes, used to auto-tune notification timing, model routing, or prompt selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simeonlukov](https://clawhub.ai/user/simeonlukov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to a self-hosted BanditDB service for contextual bandit decisions, predictions, rewards, and campaign diagnostics. It supports adaptive workflows such as notification timing, tool routing, model selection, prompt strategy selection, and response style tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from unpinned release, container, or package sources can create supply-chain exposure.

Mitigation: Use a specific reviewed BanditDB release or image digest where possible, and verify checksums or signatures when provided.

Risk: Campaign deletion and reward recording are state-changing operations that can remove campaigns or alter learning outcomes.

Mitigation: Run BanditDB with least privilege and expose DELETE and reward-recording tools only to agents trusted to manage BanditDB campaigns.

## Reference(s):

- [BanditDB API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance, campaign creation, prediction, reward recording, export, and MCP tool registration details.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
