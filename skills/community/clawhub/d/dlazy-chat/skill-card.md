## Description:

Chat with the dLazy sandbox agent, a project-scoped assistant for running skills over multiple turns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can have project-scoped, multi-turn conversations with the dLazy sandbox agent, discover available skills and projects, and continue ongoing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad chat triggers could send unrelated messages to dLazy without clear intent.

Mitigation: Invoke the skill only when explicitly requested and check that its trigger phrases match the intended task.

Risk: Files attached with --files are uploaded to dLazy media storage.

Mitigation: Attach only files approved for upload to the dLazy service.

Risk: The security scan was partial, leaving some installation and runtime details unverified.

Mitigation: Review the CLI installation details and service behavior before use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/dlazy-chat)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text, optionally formatted as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are streamed from a project-scoped chat session.]

## Skill Version(s):

1.2.47 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
