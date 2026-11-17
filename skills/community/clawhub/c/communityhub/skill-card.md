## Description:

Communityhub helps agents generate community-management templates, engagement ideas, health metrics, content planning, growth, monetization, and crisis-handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Community managers, moderators, and operators use this skill to draft onboarding messages, rules, engagement ideas, community-health metrics, and other community operations guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store user-provided community data and command history locally with limited disclosure and weak filesystem safeguards.

Mitigation: Review the skill before installing, avoid entering sensitive community, business, or member information, and configure COMMUNITYHUB_DIR to a controlled location when local storage is needed.

Risk: The remove command is misleading and may not actually delete stored entries.

Mitigation: Do not rely on the remove command for erasure; inspect exported or stored data directly when deletion matters.

Risk: One script adds an always-on promotional footer to output.

Mitigation: Review generated text before publishing or sending it outside the organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/communityhub)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style guidance emitted to stdout, with shell command examples in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required. Some commands can write local data and history under the configured communityhub data directory.]

## Skill Version(s):

2.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
