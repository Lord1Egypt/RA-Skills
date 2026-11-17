## Description:

A virtual ASCII companion that lives in your chat, hatches from an egg, reacts to conversations with sprites, celebrates wins, mourns errors, and grows over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-ryland](https://clawhub.ai/user/l-ryland)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Buddy to add a persistent ASCII companion to agent chats, including companion management commands, keyword-triggered reactions, mood changes, and local state-backed customization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buddy passively reacts in chat and retains companion state across sessions.

Mitigation: Install only when passive companion reactions are desired, and review or delete ~/.openclaw/workspace/buddy-state.json to clear retained companion data.

Risk: Untrusted custom companion names or attributes may affect the robustness of locally written JSON state.

Mitigation: Avoid untrusted custom names or attributes until JSON encoding is fixed.

## Reference(s):

- [Buddy ClawHub Skill](https://clawhub.ai/l-ryland/skills/claudebuddy)
- [Publisher Profile](https://clawhub.ai/user/l-ryland)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown and plain text with monospace ASCII sprite code blocks, shell command examples, and JSON state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and jq; stores companion state locally at ~/.openclaw/workspace/buddy-state.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
