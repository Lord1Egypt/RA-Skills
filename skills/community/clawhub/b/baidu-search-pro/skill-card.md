## Description:

Baidu Search Pro provides a compatibility alias for a Baidu realtime search chain used for live information, documentation, and research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when existing workflows need a Baidu-based realtime search alias for live information, documentation lookup, or research queries. New workflows should prefer the canonical realtime-web-search skill when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package delegates execution to a local realtime-web-search script that is not bundled or verified with this release.

Mitigation: Install only when the referenced realtime-web-search script is trusted and verified, or prefer installing the canonical realtime-web-search skill directly.

Risk: The skill requires a Baidu API key and may send queries to configured Baidu search or summary endpoints.

Mitigation: Provide BAIDU_API_KEY through the runtime secret mechanism and review endpoint overrides before use.

## Reference(s):

- [Baidu Search Pro on ClawHub](https://clawhub.ai/wangziiiiii/skills/baidu-search-pro)
- [Publisher profile](https://clawhub.ai/user/wangziiiiii)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Search responses and summaries returned through a Python script interface, with configuration via environment variables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BAIDU_API_KEY; optional endpoint override environment variables are documented by the skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
