## Description:

Audit a public webpage or website for crawlability, indexing signals, metadata, canonical URLs, headings, structured data, and evidence-backed SEO fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site operators use this skill to run bounded technical and on-page SEO audits for public HTTP(S) pages or websites. It helps diagnose crawlability, metadata, canonical, heading, structured-data, internal-link, and indexation-proxy issues with evidence-backed fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes broader business-intelligence and generic Dataify task tooling beyond the SEO-audit workflow.

Mitigation: Review the included scripts before installing or enabling the skill, and execute only the SEO audit workflow needed for the task.

Risk: Target URLs, page content, and optional keywords may be sent to Dataify services.

Mitigation: Use the skill only with public URLs and avoid sensitive keywords or private site content.

Risk: The workflow depends on a Dataify API token and external service calls.

Mitigation: Use a limited Dataify token, keep it in the environment, and do not paste or print it in chat or reports.

## Reference(s):

- [Dataify documentation](https://doc.dataify.com)
- [Dataify support](https://www.dataify.com/)
- [Five-layer audit framework](references/audit-framework.md)
- [SEO checks](references/checks.md)
- [SEO finding contract](references/output-contract.md)
- [Site-type playbooks](references/site-type-playbooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Markdown report, JSON report, raw evidence files, and concise execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include scope, collection time, priority, layer, impact, evidence, and fix; reports separate measured findings from external-only checks.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
