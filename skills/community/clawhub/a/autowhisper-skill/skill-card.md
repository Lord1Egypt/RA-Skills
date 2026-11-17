## Description:

AutoWhisper lets an agent drive its AI CMO over an HTTP API to add products, generate marketing content, schedule and publish approved posts, and report account or campaign status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xnjiang](https://clawhub.ai/user/xnjiang)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use AutoWhisper to hand off product marketing workflows: adding a product, generating UGC video, social copy, graphics, reviewing feed items, scheduling or publishing content, and checking analytics or status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to store and use an AutoWhisper API token that can operate the user's account and publish through connected channels.

Mitigation: Use a least-privilege or revocable token when available, protect the credentials file with owner-only permissions, and rotate or revoke the token if access is no longer needed.

Risk: Autonomous publishing can send unwanted marketing content to connected public channels.

Mitigation: Keep human approval enabled for publishing unless the user intentionally authorizes autonomous operation, and summarize high-impact actions before confirming them.

Risk: The skill's error-handling guidance can hide service failures, which may leave users believing content was generated or published when it was not.

Mitigation: Verify operations through status, feed, post, or platform endpoints before reporting completion, and do not claim that publishing succeeded until the API and connected platform state support it.

## Reference(s):

- [AutoWhisper Skill on ClawHub](https://clawhub.ai/xnjiang/skills/autowhisper-skill)
- [AutoWhisper Homepage](https://autowhisper.xyz)
- [AutoWhisper API Reference](references/api-reference.md)
- [Collaborating with the AutoWhisper CMO](references/cmo-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May relay AutoWhisper CMO text in the user's language and may include setup commands, API calls, status summaries, confirmation prompts, and content-operation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata and changelog report 0.2.x)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
