## Description:

AI电商专家｜首尾帧商品视频 helps ecommerce content, advertising, video editing, and brand teams prepare IMIVA MCP workflows that generate product videos from first and last frame references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand content teams, advertisers, video editors, and social commerce teams use this skill to turn product materials, channel goals, and first/last frame references into IMIVA video generation task parameters. It supports budget checks, paid task confirmation, task tracking, and result review for product transition or demonstration videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches an unpinned external npm package, so installed behavior may change over time.

Mitigation: Pin @infimind/ecom-content-cli to a reviewed version and run it from a clean environment.

Risk: The MCP process uses IMIVA tokens and environment variables.

Mitigation: Use a limited IMIVA token, avoid exposing unrelated secrets, and keep API_URL fixed to the expected HTTPS IMIVA host.

Risk: Video generation can spend IMIVA credits.

Mitigation: Use dryRun, review estimatedCredits, set maxCredits, and require explicit user confirmation before creating paid tasks.

Risk: A generic MCP call surface can invoke tools beyond the expected workflow if misused.

Mitigation: Review tools/list at runtime and restrict calls to the expected IMIVA ecommerce task and query tools.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-first-last-frame-video)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON arguments and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create paid IMIVA video generation tasks after dry-run checks and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
