## Description:

Firecrawl Local lets agents scrape web pages, map site structure, and crawl websites through a self-hosted Firecrawl v1 REST API running on localhost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saddamtechie](https://clawhub.ai/user/saddamtechie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to extract clean page content, discover site URLs, and bulk ingest documentation into RAG or analysis workflows through a local Firecrawl service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports unsafe optional API-key handling in run.sh before installation.

Mitigation: Fix FIRECRAWL_API_KEY header handling to pass the Authorization header as one quoted argument, for example with a Bash array, before using authenticated endpoints.

Risk: Changing FIRECRAWL_LOCAL_URL can send scrape requests and any configured API key to a non-local server.

Mitigation: Keep FIRECRAWL_LOCAL_URL on localhost unless the endpoint is intentionally trusted and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saddamtechie/skills/firecrawl-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Shell command output as formatted JSON containing markdown, HTML, links, and metadata depending on the selected command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a reachable local Firecrawl endpoint; crawl results are asynchronously polled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
