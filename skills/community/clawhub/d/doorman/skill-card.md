## Description:

Manage firewall rules as code across Vercel, Cloudflare, Fastly, and Google Cloud Armor with the Doorman CLI, including authoring, validating, syncing, and documenting WAF configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gfargo](https://clawhub.ai/user/gfargo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use Doorman to write, validate, synchronize, and document web application firewall rules across supported providers, including CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment had medium confidence because analysis was partial and three local references were unresolved.

Mitigation: Review the source and unresolved provider guidance before installation.

Risk: Sync can apply local firewall configuration to a live provider.

Mitigation: Validate and diff changes before syncing, and create a backup before major changes.

## Reference(s):

- [ClawHub release](https://clawhub.ai/gfargo/skills/doorman)
- [Source repository (server-resolved provenance)](https://github.com/gfargo/doorman/tree/main/skills/doorman)
- [Doorman npm package](https://www.npmjs.com/package/@gfargo/doorman)
- [Rule Authoring Reference](references/rules.md)
- [Cloudflare Provider Reference](references/cloudflare.md)
- [Fastly Next-Gen WAF Provider Reference](references/fastly.md)
- [GCP Cloud Armor Provider Reference](references/gcp.md)
- [CI/CD & Automation Reference](references/cicd.md)
- [Templates Reference](references/templates.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON, YAML, Markdown, or Terraform configuration exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provider-dependent; credentials are required for provider operations, and supported rules and exports vary by provider.]

## Skill Version(s):

0.1.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
