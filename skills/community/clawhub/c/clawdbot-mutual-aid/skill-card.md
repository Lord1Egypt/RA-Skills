## Description:

Automatically records task experience and tags, requests help from peer AI assistants when negative feedback is detected, and shares stored experience to support collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwl481306354-blip](https://clawhub.ai/user/mwl481306354-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to capture task experience, search recent experience records, and exchange help with peer assistants through chat commands and HTTP endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic local logging and peer-network sharing can expose prompts, tool activity, private context, or proprietary information.

Mitigation: Use only where local logging and peer sharing are acceptable; avoid tasks containing secrets, personal data, private files, or proprietary information until redaction and sharing controls are reviewed.

Risk: Automatic peer-network connection can share stored experience without clear per-item consent.

Mitigation: Disable autoConnect unless peer sharing is explicitly needed, and review stored experience records before enabling networked help exchange.

Risk: Bundled network credentials and long-lived configuration may be unsuitable for shared or production environments.

Mitigation: Provide environment-specific credentials through configuration or environment variables and rotate them before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwl481306354-blip/skills/clawdbot-mutual-aid)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [Command text and HTTP JSON responses backed by local JSON experience records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records task descriptions, tool-call summaries, generated tags, success state, reputation counters, and peer-help responses in local state.]

## Skill Version(s):

1.0.0 (source: server release evidence, openclaw.plugin.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
