## Description: <br>
Manage Cloudflare Workers, Pages, KV, D1, R2, and secrets using Wrangler CLI commands and direct Cloudflare API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ItamarCoh3n](https://clawhub.ai/user/ItamarCoh3n) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy Cloudflare Workers and Pages, manage Cloudflare storage, databases, secrets, and queues, and troubleshoot Wrangler or Cloudflare API configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare administration commands can delete infrastructure or data, change secrets, deploy code, run SQL, alter lifecycle rules, or perform bulk operations if used carelessly. <br>
Mitigation: Use least-privilege Cloudflare tokens, verify the Wrangler package, and require explicit confirmation before deletes, deployments, migrations, SQL execution, secret changes, bulk operations, direct API calls, or lifecycle-rule changes. <br>


## Reference(s): <br>
- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/) <br>
- [Workers Docs](https://developers.cloudflare.com/workers/) <br>
- [D1 Docs](https://developers.cloudflare.com/d1/) <br>
- [R2 Docs](https://developers.cloudflare.com/r2/) <br>
- [KV Docs](https://developers.cloudflare.com/kv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, TOML, JavaScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance and command examples for Cloudflare administration; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
