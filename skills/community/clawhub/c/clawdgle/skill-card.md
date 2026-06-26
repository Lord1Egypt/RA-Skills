## Description: <br>
Use Clawdgle API to search markdown content, fetch markdown by URL, request URL indexing, or access the donation link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RubyBrewsday](https://clawhub.ai/user/RubyBrewsday) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to interact with Clawdgle's public markdown search, document retrieval, URL ingest, and donation endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search, document fetch, and ingest requests send URL or query data to the external clawdgle.com service. <br>
Mitigation: Use the skill for public markdown and avoid submitting private, confidential, or sensitive URLs or content unless the user accepts that external-service exposure. <br>
Risk: The ingest endpoint can request indexing of URLs and may create unwanted service load if used repeatedly. <br>
Mitigation: Rate-limit or batch ingest requests and confirm that indexing the target URL is appropriate before submitting it. <br>
Risk: The donate endpoint is outside the core search and retrieval workflow. <br>
Mitigation: Treat donation links as optional and present them only when the user asks for contribution or support information. <br>


## Reference(s): <br>
- [Clawdgle Skill Page](https://clawhub.ai/RubyBrewsday/clawdgle) <br>
- [Clawdgle API Base URL](https://clawdgle.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, API calls] <br>
**Output Format:** [Markdown with inline HTTP endpoints and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to public Clawdgle endpoints and expects public URL/query inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
