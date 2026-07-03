## Description: <br>
AnnData MCP is a tool for retrieving and summarizing AnnData object information through an MCP-compatible XiaoBenYang API service for biomedical data analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and biomedical data analysts use this skill to query AnnData files by path or URL, view selected raw attributes, generate summaries, and compute descriptive statistics through the configured XiaoBenYang MCP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends AnnData query parameters and the configured API key to the XiaoBenYang API service. <br>
Mitigation: Install only if the API service is trusted for the intended data and prefer environment variables or a platform secret store for XBY_APIKEY. <br>
Risk: The security summary notes copy-paste documentation errors that may make examples or project labels unreliable. <br>
Mitigation: Review the documented examples against the actual AnnData tool functions before relying on them in workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/anndata) <br>
- [XiaoBenYang API service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown summary of structured API responses containing raw, success, and message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided XBY_APIKEY before API calls can be made.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
