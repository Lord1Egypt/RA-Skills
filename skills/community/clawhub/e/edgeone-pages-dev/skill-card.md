## Description:

This skill guides development of full-stack features on EdgeOne Pages, including Edge Functions, Cloud Functions for Node.js, Go, and Python, Middleware, KV Storage, and local development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edgeone-pages](https://clawhub.ai/user/edgeone-pages)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement EdgeOne Pages APIs, serverless functions, middleware, WebSocket endpoints, KV-backed edge features, and local development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready API, middleware, and KV examples may produce weak authentication, missing object-level authorization, or public persistent-data endpoints.

Mitigation: Require verified authentication, object-level authorization checks, input validation, and safe JSON serialization before accepting generated application code.

Risk: Examples that expose IP, geolocation, environment variables, or KV deletion behavior may mishandle privacy-sensitive data or destructive operations.

Mitigation: Limit collection and exposure of IP/geolocation data, keep environment secrets out of responses and logs, and require explicit safeguards for KV delete or bulk mutation paths.

## Reference(s):

- [EdgeOne Pages Dev on ClawHub](https://clawhub.ai/edgeone-pages/skills/edgeone-pages-dev)
- [Edge Functions](references/edge-functions.md)
- [Node.js Functions](references/node-functions.md)
- [Go Functions](references/go-functions.md)
- [Python Functions](references/python-functions.md)
- [Middleware](references/middleware.md)
- [KV Storage](references/kv-storage.md)
- [Common Recipes](references/recipes.md)
- [Debugging and Troubleshooting](references/troubleshooting.md)
- [EdgeOne Pages Console](https://console.cloud.tencent.com/edgeone/pages)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, file paths, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be adapted to the selected EdgeOne Pages runtime and project structure.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
