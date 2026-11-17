## Description:

Feishu All In One helps agents configure Feishu messaging workflows for text, image and file sending, voice transcription, proactive messages, and interactive cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arvenwang](https://clawhub.ai/user/arvenwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to connect agents with Feishu for bot messaging, file delivery, interactive card workflows, callback handling, and optional voice-to-text processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The callback server can forward full Feishu card interaction data to a configurable Gateway, which evidence.security flags as needing review.

Mitigation: Disable Gateway forwarding unless required, restrict the Gateway URL to a trusted HTTPS or local endpoint, and avoid sending raw callback data.

Risk: Feishu App Secret and Gateway tokens are required for message and callback flows.

Mitigation: Store secrets in protected configuration or environment variables, limit access to the configuration file, and rotate tokens if exposed.

Risk: The security guidance recommends regenerating the npm lockfile from an approved HTTPS registry with updated dependencies before production use.

Mitigation: Regenerate and review package-lock.json in a trusted build environment before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arvenwang/skills/feishu-all-in-one)
- [Feishu Open Platform](https://open.feishu.cn/)
- [README.md](README.md)
- [confirmation-card.json](references/confirmation-card.json)
- [form-card.json](references/form-card.json)
- [poll-card.json](references/poll-card.json)
- [test-card.json](references/test-card.json)
- [todo-card.json](references/todo-card.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, JavaScript snippets, and Feishu card JSON templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, node, Feishu App ID/App Secret, and OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json; artifact SKILL.md frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
