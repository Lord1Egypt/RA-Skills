## Description: <br>
Uses the FOFA OpenAPI to run batch asset searches and export results as CSV, with optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biglizi775](https://clawhub.ai/user/biglizi775) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run FOFA queries, automatically page through results, and export asset data for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive FOFA API key. <br>
Mitigation: Provide the key at runtime, prefer environment variables, and avoid storing credentials in code, artifacts, or commits. <br>
Risk: FOFA search results may contain sensitive asset information. <br>
Mitigation: Choose export paths carefully, restrict access to generated CSV or JSON files, and review results before sharing. <br>
Risk: A custom FOFA base URL could send credentials and queries to an untrusted endpoint. <br>
Mitigation: Keep the default FOFA endpoint unless the alternative endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [FOFA](https://fofa.info) <br>
- [ClawHub skill page](https://clawhub.ai/biglizi775/fofasearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled CLI writes CSV and optional JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FOFA API key at runtime and may export sensitive asset information to local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
