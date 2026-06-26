## Description: <br>
Prepares Dataify builder requests for the github.com scraper family rooted at github_repository_by-repo-url, including tool selection, saved parameter options, and generation of a Dataify builder curl request using DATAIFY_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to assemble Dataify builder requests for GitHub repository scraping tools, normalize spider_parameters from saved options or user inputs, and produce a curl command for the Dataify builder API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DATAIFY_API_TOKEN can be exposed if generated curl commands containing a literal bearer token are shared, logged, or committed. <br>
Mitigation: Keep the token in an environment variable, avoid sharing generated commands that include the token value, and rotate the token if it is exposed. <br>
Risk: The artifact references a tool-params catalog and a PowerShell helper that are not included in the released files. <br>
Mitigation: Confirm required helper files and parameter catalogs are available before relying on saved options; otherwise collect needed values from the user and prefer the included Python helper. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-github-repository-by-repo-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder API endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated curl commands may include a Dataify bearer token when the helper script is run with DATAIFY_API_TOKEN set.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
