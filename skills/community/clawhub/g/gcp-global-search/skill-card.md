## Description:

Query Google Cloud product information, documentation, parameters, features, and pricing from official sources without login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbingpeng](https://clawhub.ai/user/wangbingpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud architects, and operators use this skill to find and compare Google Cloud product documentation, specifications, parameters, features, and pricing in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied cloud provisioning examples can create billable Google Cloud resources.

Mitigation: Review all gcloud, SDK, and Terraform snippets for billing impact, region, quota, and cleanup steps before execution.

Risk: Some GKE examples use broad node OAuth scopes.

Mitigation: Prefer least-privilege service accounts and Workload Identity guidance before adapting GKE examples.

Risk: Pricing, specifications, and product limits can change after the skill content was authored.

Mitigation: Verify current values against official Google Cloud documentation and pricing pages before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangbingpeng/skills/gcp-global-search)
- [Google Cloud products](https://cloud.google.com/products)
- [Google Cloud documentation](https://cloud.google.com/docs)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator)
- [Compute Engine documentation](https://cloud.google.com/compute/docs)
- [GKE documentation](https://cloud.google.com/kubernetes-engine/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, links, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese responses; examples may include gcloud, SDK, and Terraform snippets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
