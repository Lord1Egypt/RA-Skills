## Description:

Generate a daily digest from memory and interactions, stored under journals/digest/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to produce a local daily Markdown digest from current memory notes and recent interactions. It is intended for recurring personal or team workflow summaries saved under journals/digest/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory notes may contain credential values that could be copied into persistent digest files.

Mitigation: Run only on sanitized memory notes, review generated digest files before sharing or committing them, and rotate any real secrets already copied into digest output.

Risk: Memory files are an untrusted input surface and may contain prompt-injection text framed as instructions.

Mitigation: Treat memory content as source data only and keep digest generation limited to summarization rather than executing embedded requests.

Risk: Digest content and memory-derived summaries can expose private user information if transmitted externally.

Mitigation: Keep processing local and avoid sending digest contents, metadata, or memory excerpts to webhooks, APIs, or other external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/daily-digest-hardened)
- [Faberlens daily-digest safety evaluation](https://faberlens.ai/explore/daily-digest)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown file with structured digest sections and optional inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated digest file to journals/digest/ when the script is executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
