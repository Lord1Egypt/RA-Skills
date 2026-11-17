## Description:

Collects Douyin live chat messages in real time and uses DeepSeek to generate short, persona-aware reply suggestions for livestream hosts.

This skill is for research and development only.

## Publisher:

[go522000](https://clawhub.ai/user/go522000)

### License/Terms of Use:

MIT-0

## Use Case:

Livestream operators and developers can use this skill to monitor Douyin live chat, filter low-value messages, and generate concise AI-assisted reply suggestions for ecommerce, education, gaming, entertainment, and knowledge-sharing streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package executes an opaque eval-based Douyin signing script.

Mitigation: Replace it with a documented, reviewable signer before production-like use, or isolate execution under a non-privileged account.

Risk: The WebSocket connection path disables normal TLS certificate verification.

Mitigation: Require standard TLS verification and review network behavior before connecting to live services.

Risk: Viewer messages and generated replies may be sent to DeepSeek and written to local chat logs or caches.

Mitigation: Disclose AI assistance and third-party processing to operators and viewers, and define retention and deletion rules for local logs.

Risk: Dependencies are installed from unpinned package names.

Mitigation: Pin dependencies and install in an isolated virtual environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/go522000/skills/douyin-live-ai)
- [AI prompt reference](references/prompts.md)
- [DeepSeek Platform](https://platform.deepseek.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline commands; runtime emits console text and JSON/JSONL reply records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply generation uses configured host persona, style, filters, token limits, and a local LRU cache.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
