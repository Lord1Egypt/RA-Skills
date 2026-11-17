## Description:

Baidu Map Cli guides agents through Baidu Maps CLI setup, account and API key handling, personalized map styles, Agent Plan map tools, and BMapGL/WebAPI code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare Baidu Maps CLI environments, manage Baidu Maps API keys and styles with user approval, and generate runnable Baidu Maps integrations or perform supported map tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and execute a remote Baidu-hosted CLI without a bundled checksum or signature.

Mitigation: Trust the download host only after confirming it matches the expected Baidu Maps source, and verify an official checksum or signature when available before use.

Risk: The skill can activate additional skills or MCP configuration and persist API keys or tokens across sessions.

Mitigation: Review each proposed configuration change before applying it, restrict credential file permissions, and document where credentials are stored for later rotation or removal.

Risk: Wildcard browser referrer API keys can be exposed or abused outside local demos.

Mitigation: Use wildcard referrers only for controlled local testing; use narrowly scoped domain allowlists for production projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidu-maps/skills/bmap-cli)
- [Baidu Maps CLI download endpoint](https://open-agent-cli.bj.bcebos.com/cli/bmap-cli-<BMAP_OS>-<BMAP_ARCH>)
- [Baidu Maps WebGL JS API endpoint](https://api.map.baidu.com/api?v=1.0&type=webgl&...)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked API keys in explanatory text; generated code is expected to use complete keys selected from current CLI output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
