## Description: <br>
Fetch any public web page and get back clean, LLM-ready markdown (polite, robots-respecting). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foomworks](https://clawhub.ai/user/foomworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Agent Web to fetch a publicly reachable static HTML page and convert its readable content into title, word count, and clean markdown for summarization, extraction, or LLM input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote service receives the public URLs supplied by the user and the resulting page content. <br>
Mitigation: Submit only public, non-confidential URLs and avoid private, authenticated, internal, or sensitive resources. <br>
Risk: Web page content may be incomplete when a target requires JavaScript rendering, PDF parsing, screenshots, authentication, or access blocked by robots.txt. <br>
Mitigation: Use the output for static public HTML pages and verify important summaries or extracted facts against the original source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/foomworks/agent-web) <br>
- [Agent Web Service](https://agent-web.foomworks.workers.dev) <br>
- [Agent Web MCP Endpoint](https://agent-web.foomworks.workers.dev/mcp) <br>
- [Agent Web OpenAPI Descriptor](https://agent-web.foomworks.workers.dev/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [JSON containing a page title, word count, and markdown content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview output returns the first ~600 characters; full reads are limited to static HTML pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
