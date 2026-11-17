## Description:

Generate vertical short videos of cake decorating and pastry finishing with WeryAI, including frosting, piping, mirror glaze, and other high-aesthetic handmade dessert moments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn cake decorating briefs or public HTTPS image inputs into WeryAI video generation requests. The agent expands prompts, confirms parameters before paid generation, runs the bundled Node CLI, and returns playable video URLs or a clear failure explanation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WERYAI_API_KEY, prompts, and image URLs to hosts selected by WERYAI_BASE_URL or WERYAI_MODELS_BASE_URL.

Mitigation: Keep override variables unset or pin them to trusted official HTTPS hosts before running the CLI.

Risk: Successful wait runs can consume WeryAI credits.

Mitigation: Review the expanded prompt and all generation parameters before confirming paid requests, with particular attention to generate_audio.

Risk: The security verdict is suspicious because runtime environment configuration can redirect API traffic.

Mitigation: Install only from a trusted publisher and run generation in a controlled or isolated environment with a limited, revocable API key.

## Reference(s):

- [Cake Decor Video on ClawHub](https://clawhub.ai/zoucdr/skills/cake-decor-video)
- [Publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI API host](https://api.weryai.com)
- [WeryAI models registry host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with confirmation tables, inline shell commands, and JSON CLI/API responses containing video URLs or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; successful wait runs may consume WeryAI credits.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
