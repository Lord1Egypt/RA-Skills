## Description: <br>
This skill guides development of full-stack features on EdgeOne Pages, including Edge Functions, Cloud Functions, Middleware, KV Storage, and local development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edgeone-pages](https://clawhub.ai/user/edgeone-pages) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add EdgeOne Pages APIs, middleware, WebSocket endpoints, KV-backed edge features, and cloud functions in Node.js, Go, or Python. It helps agents choose the correct runtime and apply platform-specific file layout, local development, and framework patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated middleware or function code could affect production traffic or persistent KV data if applied without review. <br>
Mitigation: Review generated middleware, functions, and KV access patterns before deploying them, and test changes locally with EdgeOne Pages development workflows. <br>
Risk: Secrets or project tokens could be exposed if copied into code or configuration files. <br>
Mitigation: Keep secrets in environment variables and link only the intended EdgeOne Pages project. <br>
Risk: Using the wrong EdgeOne runtime can produce broken or misleading implementations. <br>
Mitigation: Follow the skill's runtime decision tree and reference files before creating Edge Functions, Cloud Functions, Middleware, or KV-backed features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edgeone-pages/edgeone-pages-dev) <br>
- [EdgeOne Pages Console](https://console.cloud.tencent.com/edgeone/pages) <br>
- [Edge Functions](references/edge-functions.md) <br>
- [Cloud Functions - Node.js](references/node-functions.md) <br>
- [Cloud Functions - Go](references/go-functions.md) <br>
- [Cloud Functions - Python](references/python-functions.md) <br>
- [Middleware](references/middleware.md) <br>
- [KV Storage](references/kv-storage.md) <br>
- [Common Recipes](references/recipes.md) <br>
- [Debugging and Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, file paths, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before applying generated middleware, functions, KV access patterns, or project configuration to production traffic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter metadata reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
