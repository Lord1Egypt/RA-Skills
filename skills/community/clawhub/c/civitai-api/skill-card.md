## Description: <br>
Query the Civitai public REST API to search models, inspect creators, fetch model or version details, reverse-lookup models by hash, list images or tags, and build authenticated download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to query Civitai assets from an agent workflow, inspect model metadata, identify files by hash, and construct download URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated download URLs may include the user's Civitai API token and should be treated as credentials. <br>
Mitigation: Keep CIVITAI_API_KEY out of source control, avoid placing unrelated secrets in the .env file read by the script, and do not share generated download URLs. <br>


## Reference(s): <br>
- [Civitai Public REST API notes](references/api-notes.md) <br>
- [Civitai Public REST API documentation](https://developer.civitai.com/docs/api/public-rest) <br>
- [Civitai](https://civitai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated download URLs that include a Civitai API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
