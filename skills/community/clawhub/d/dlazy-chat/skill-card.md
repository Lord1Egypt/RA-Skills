## Description:

Chat with the dLazy sandbox agent, a project-scoped assistant for multi-turn work that runs skills end-to-end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to chat with a hosted, project-scoped dLazy agent, start or continue multi-turn tasks, and discover available skills and projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad conversation triggers could activate the hosted chat service without a clear request.

Mitigation: Review the trigger wording before installing and invoke the skill only when you intend to use the hosted service; consider that messages may be sent externally or billable actions may start.

Risk: The security scan is partial, leaving unresolved references and unexamined behavior uncertain.

Mitigation: Review the skill and CLI behavior before use, and avoid relying on the scan as a complete assessment.

Risk: Files attached to a chat are uploaded to dLazy media storage.

Mitigation: Attach only files you are comfortable sending to the hosted service.

## Reference(s):

- [CLI repository link listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Streamed conversational text, which may include Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected dLazy skill and project context.]

## Skill Version(s):

1.2.44 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
