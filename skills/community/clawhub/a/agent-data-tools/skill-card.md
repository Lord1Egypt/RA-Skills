## Description:

Agent Data Tools helps agents find and call live data and AI services over HTTP, including web research, content extraction, and financial, company, weather, and blockchain lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to retrieve current information or make outside lookups when no better-connected tool is available. The tool finder is free; individual calls may use free allowances, a prepaid key, or user-approved wallet payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags that the MCP URL form can put a prepaid API key in the URL, where logs or diagnostics could expose it. The scan evidence is partial.

Mitigation: Use the Authorization header form when supported; treat a key-bearing URL as secret and do not share it.

Risk: Some calls incur per-call charges or spend from a connected wallet.

Mitigation: Use the free finder and previews first, then confirm the call price and user budget before making a paid call.

## Reference(s):

- [Agent Data Tools API catalog](https://agent-data-tools.revmesh2074.workers.dev/openapi.json)
- [Agent Data Tools readable catalog](https://agent-data-tools.revmesh2074.workers.dev/llms.txt)
- [ClawHub release page](https://clawhub.ai/nutshell2000/skills/agent-data-tools)
- [Support and issue tracker](https://github.com/Nutshell2000/agent-data-tools/issues)

## Skill Output:

**Output Type(s):** [JSON data, Text and summaries, Analysis results, Audio]

**Output Format:** [JSON responses, text or Markdown, and base64-encoded MP3 for speech output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by tool and may contain structured records or media data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
