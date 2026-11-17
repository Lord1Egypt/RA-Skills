## Description:

Clawsoul Skill gives an OpenClaw agent an MBTI-based personality, adapts its tone from local interaction learning, and supports optional Pro token-based personality injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyur-wang](https://clawhub.ai/user/fanyur-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to give an agent an MBTI-style persona, persist local preference learning, and adjust the agent's response style across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read_chat_history, modify_system_prompt, and local_storage access, and security evidence flags under-scoped persistent prompt modification.

Mitigation: Install only in trusted OpenClaw workspaces, review requested permissions before enabling, and inspect or reset the generated state after use.

Risk: Chat content may leave the machine if a cloud LLM provider is configured.

Mitigation: Use a local provider or a trusted cloud provider, avoid configuring cloud API keys for sensitive conversations, and assume analyzed chat content may be sent to that provider.

Risk: Pro injection tokens can overwrite the agent personality, preferences, interaction patterns, learnings, and injected state.

Mitigation: Use injection tokens only from a trusted source and delete or reset ~/.clawsoul/state.json to remove learned or injected profile data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyur-wang/skills/clawsoul-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/fanyur-wang)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Plain text status messages and Markdown-style command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist MBTI, preference, and injected profile state locally; optional LLM analysis may use configured local or cloud providers.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
