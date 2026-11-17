## Description:

Create polished multi-shot videos with the Future Video Studio MCP, using either an account API key or no-account Link pay-per-render quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariadne-coil](https://clawhub.ai/user/ariadne-coil)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to create Future Video Studio scene, music, or custom video renders, including quoted pay-per-render jobs and account-backed jobs. It helps prepare render requests, attach public or local assets, poll or cancel jobs, download finished videos, and return final signed video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account mode can spend wallet-backed Future Video Studio credits when an API key is configured.

Mitigation: Show the render summary, requested duration and resolution, any available estimate or budget cap, and get explicit user approval before submitting an account-mode render.

Risk: Custom host opt-in can allow the helper to send an API key and uploaded files to a non-default HTTP(S) host.

Mitigation: Keep the default production endpoint unless a trusted local or staging backend is explicitly configured; avoid plaintext remote HTTP when using a production wallet-backed API key.

Risk: Local uploads can disclose user files to Future Video Studio processing.

Mitigation: Confirm that each local file is intended to be shared before attaching it, and prefer public HTTPS upload URLs for remote MCP workflows.

Risk: Pay-per-render mode involves payment approval and claim-token handling.

Mitigation: Use the returned Link or approved payment surface, never request raw card details, and keep the payment URL, status URL, quote ID, and claim token together until the render completes.

## Reference(s):

- [Future Video Studio MCP And Agent API](artifact/references/api.md)
- [Future Video Studio API Docs](https://future.video/api-docs)
- [Future Video Studio MCP Manifest](https://mcp.future.video/server.json)
- [Future Video Studio MCP Well-Known Manifest](https://mcp.future.video/.well-known/mcp-server.json)
- [Future Video Studio MCP Endpoint](https://mcp.future.video/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; runtime responses include JSON status data, payment links, downloaded files, and signed video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signed final video URLs may expire; paid-render claim tokens, payment URLs, and status URLs should be kept together until completion.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
