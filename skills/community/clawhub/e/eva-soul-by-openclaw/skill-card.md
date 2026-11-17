## Description:

Eva Soul is an OpenClaw plugin that adds persona, emotion, memory, decision support, concept extraction, pattern recognition, and knowledge graph tools to an AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catfei0518](https://clawhub.ai/user/catfei0518)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to add persistent persona, emotional state, memory retrieval, decision suggestions, and related cognitive tools to an AI assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory features can store conversation content and personal data.

Mitigation: Review saved memory files regularly, avoid sharing secrets or sensitive personal data while hooks are enabled, and disable automatic memory if persistent storage is not needed.

Risk: Persona hooks can inject behavior-changing context into assistant responses.

Mitigation: Review the generated persona and state behavior before deployment, and disable automatic personality features when predictable assistant behavior is required.

Risk: Conversation or memory text may be sent to an external embedding service when SILICONFLOW_API_KEY is configured.

Mitigation: Unset SILICONFLOW_API_KEY unless external embeddings are explicitly intended and approved for the data being processed.

Risk: The plugin requests broad tool permissions including exec and message.

Mitigation: Remove unnecessary exec and message permissions where the deployment platform permits least-privilege configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catfei0518/skills/eva-soul-by-openclaw)
- [Publisher profile](https://clawhub.ai/user/catfei0518)
- [EVA documentation site](https://eva.catx.ltd)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON-like tool results, with Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist assistant state, memory, concept, pattern, and knowledge graph files under the configured OpenClaw memory path.]

## Skill Version(s):

2.5.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
