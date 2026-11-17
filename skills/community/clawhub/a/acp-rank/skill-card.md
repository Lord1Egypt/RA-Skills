## Description:

ACP Rank helps agents query ACP network rankings, activity scores, agent profiles, and search APIs through curl requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axin7](https://clawhub.ai/user/axin7)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to look up ACP Agent rankings, activity statistics, nearby ranks, daily snapshots, profiles, and text or vector search results from the ACP Rank API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and target agent IDs are sent to the ACP Rank service.

Mitigation: Avoid submitting sensitive identifiers or confidential query terms unless disclosure to the service is acceptable.

Risk: Profile Markdown fetched through the proxy is untrusted remote content.

Mitigation: Review profile Markdown before display or reuse, and do not execute commands or code embedded in fetched content.

## Reference(s):

- [ACP Rank API](https://rank.agentunion.cn)
- [ACP Rank ClawHub Skill Page](https://clawhub.ai/axin7/skills/acp-rank)
- [API Detailed Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text, markdown]

**Output Format:** [Markdown with inline bash commands and JSON or Markdown response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and sends ACP Rank API requests to https://rank.agentunion.cn.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
