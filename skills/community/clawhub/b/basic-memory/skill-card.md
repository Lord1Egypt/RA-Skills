## Description:

Gives OpenClaw agents persistent memory across conversations by organizing, loading, saving, retrieving, and pruning entries in MEMORY.md and daily memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give OpenClaw agents persistent, structured memory for facts, preferences, action items, decisions, and recurring context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically saves and reuses personal context across sessions, which can retain sensitive or unwanted details.

Mitigation: Review saved memory regularly, use forget or deletion workflows for unwanted entries, and install only when automatic personal-memory behavior is acceptable.

Risk: Users may ask the agent to store secrets or highly sensitive personal data.

Mitigation: Do not store passwords, API keys, national IDs, payment details, or health data; acknowledge the request and skip the write.

## Reference(s):

- [Memory Hygiene Reference](references/memory-hygiene.md)
- [ClawHub skill page](https://clawhub.ai/billyhetech/skills/basic-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown files and concise natural-language confirmations or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md and daily memory logs; sensitive secrets, financial identifiers, and health data should not be stored.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
