## Description:

ClawSoul gives an OpenClaw agent an MBTI-based personality, learns local interaction preferences, adjusts response style, and accepts Pro token-based personality injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyur-wang](https://clawhub.ai/user/fanyur-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to add an MBTI-style persona layer, local preference learning, status reporting, recommendation controls, and optional Pro personality injection to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads chat history, modifies prompts, and stores local behavioral profile or token-derived data.

Mitigation: Install only when those permissions are acceptable, review stored state handling, and avoid use in conversations containing secrets or confidential data.

Risk: Recent conversation text may be sent to configured LLM endpoints when network-backed analysis is enabled.

Mitigation: Disable network analysis or configure trusted endpoints before using the skill with sensitive conversations.

Risk: Untrusted Pro injection tokens can overwrite personality and preference state.

Mitigation: Accept Pro tokens only from trusted sources and review resulting persona and preference changes after injection.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fanyur-wang/skills/clawsoul-skill-new)
- [ClawHub publisher profile](https://clawhub.ai/user/fanyur-wang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with command examples and local configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify the active agent persona prompt and persist local profile, preference, and token-derived state.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
