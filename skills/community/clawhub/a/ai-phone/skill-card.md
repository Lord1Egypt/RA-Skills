## Description:

A smarter phone powered by AI. Polly manages your calls, screens unknown numbers, transcribes voicemails, and gives you a complete AI-enhanced phone experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhugelaing888](https://clawhub.ai/user/zhugelaing888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use AI Phone to activate PollyReach phone service, place outbound calls, retrieve call results, review inbound call summaries, customize answering behavior, and monitor account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends phone numbers, call content, transcripts, recordings, summaries, and account metadata to PollyReach.

Mitigation: Use only after explicit user approval and avoid sending sensitive calls or regulated information unless the user accepts the third-party data handling risk.

Risk: The local PollyReach token grants access to call and account actions.

Mitigation: Store the token file as a secret, avoid printing it in chat or logs, and rotate or remove it if exposed.

Risk: Outbound calls and scheduled inbound polling can contact real people or retrieve sensitive call content.

Mitigation: Require clear human approval before calls or scheduled polling and review call results before taking follow-up action.

Risk: The artifact includes promotional or referral behavior outside the core phone workflow.

Mitigation: Keep promotional messages optional and separate from task completion, and do not forward remote installation text as executable instructions.

## Reference(s):

- [AI Phone ClawHub Skill Page](https://clawhub.ai/zhugelaing888/skills/ai-phone)
- [PollyReach Homepage](https://pollyreach.ai)
- [PollyReach Agent Dashboard](https://agent.pollyreach.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return phone numbers, call transcripts, recordings links, summaries, task status, credit balance, and account activation status.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
