## Description: <br>
CLI to read Coda.io documents and pages. List docs, list pages, read content in markdown/json/html. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Auniik](https://clawhub.ai/user/Auniik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to authenticate with Coda.io, discover available documents and pages, and read requested page content for analysis or downstream work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Coda API token and can read Coda documents requested by the agent. <br>
Mitigation: Use the least-privileged token available and avoid exporting sensitive pages unless they are needed for the task. <br>
Risk: Credential setup may create a temporary .env file containing CODA_API_TOKEN. <br>
Mitigation: Delete the temporary .env file after authentication, never commit it, and run coda-ai logout when stored credentials should be removed. <br>


## Reference(s): <br>
- [coda-ai npm package](https://www.npmjs.com/package/coda-ai) <br>
- [coda-ai README](https://github.com/auniik/coda-ai#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [CLI output as markdown, JSON, HTML, table, tree, or toon text, with setup commands documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the coda-ai binary and a CODA_API_TOKEN for authenticated Coda.io access.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
