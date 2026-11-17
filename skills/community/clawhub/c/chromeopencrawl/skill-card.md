## Description:

Crawl JavaScript-rendered webpages through distributed Chrome browsers without requiring a local browser installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlyylly](https://clawhub.ai/user/hlyylly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve rendered webpage text, extract selected page content, run web searches, and check OpenCrawl account or platform status through the OpenCrawl service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and browsing or search targets may be sent to a plaintext HTTP public endpoint.

Mitigation: Use a self-hosted HTTPS OpenCrawl server for normal operation, and do not send API keys or sensitive browsing targets to the public HTTP endpoint.

Risk: Crawled content may be processed by remote workers and stored in R2.

Mitigation: Avoid authenticated, internal, private, or otherwise sensitive pages unless the deployment and storage path have been reviewed.

Risk: The tool trusts server-provided download URLs for crawl results.

Mitigation: Review the service trust boundary before deployment and prefer a controlled self-hosted server for sensitive workloads.

## Reference(s):

- [OpenCrawl project homepage](https://github.com/hlyylly/OpenCrawl)
- [ClawHub skill page](https://clawhub.ai/hlyylly/skills/chromeopencrawl)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text for crawled content, JSON for raw crawl/search/balance/status responses, and shell command examples for agent execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCRAWL_API_KEY and optionally OPENCRAWL_API_URL.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
