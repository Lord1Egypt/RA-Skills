## Description:

Anima Aios gives OpenClaw agents persistent memory management, cognitive profiles, daily growth tasks, team ranking, and layered knowledge organization using local memory stores with optional LLM-assisted processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liruozhou](https://clawhub.ai/user/liruozhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent agent memory, memory search, cognitive growth reports, daily quests, and optional team ranking to agent workflows. It is most relevant for agents that need local memory continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad persistent local memory and session processing.

Mitigation: Install only when persistent local indexing is intended, use private storage paths, and review the configured facts_base before enabling the skill.

Risk: Remote LLM configuration can expose memory prompts outside the local machine.

Mitigation: Avoid remote LLM endpoints unless memory content may leave the machine; prefer local or rule-mode processing for sensitive memory.

Risk: Team ranking can scan other agents' cognitive profiles when enabled.

Mitigation: Keep team_mode disabled unless cross-agent ranking is explicitly intended and authorized.

Risk: Broad permission repair guidance can make sensitive memory or config directories too permissive.

Mitigation: Do not apply chmod -R 755 to sensitive memory or configuration directories; use least-privilege permissions instead.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liruozhou/skills/anima-aios)
- [Anima GitHub Repository](https://github.com/anima-aios/anima)
- [Security and Privacy Notes](artifact/SECURITY.md)
- [Usage Guide](artifact/docs/USAGE.md)
- [Architecture Principles](artifact/docs/ARCHITECTURE_PRINCIPLES.md)
- [Session JSONL Schema](artifact/docs/session-jsonl-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown/text responses, JSON profile and ranking files, local memory files, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local memory, fact, profile, learning, health, and ranking artifacts under the configured facts_base path.]

## Skill Version(s):

6.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
