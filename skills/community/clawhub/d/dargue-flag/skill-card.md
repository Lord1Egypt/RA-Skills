## Description: <br>
Dargue Flag helps an agent search and browse video content by keyword, category, popularity, and selected item details through a credentialed video API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe-evolver](https://clawhub.ai/user/pe-evolver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search video content, browse video categories and popular lists, and retrieve details for selected results. The agent can also guide API key configuration and quota checks for the video service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill appears intended for adult video search and playback despite generic wording. <br>
Mitigation: Use the skill only in environments where that content category is acceptable and disclose the content category to users before deployment. <br>
Risk: The security evidence says the skill stores an API key on disk. <br>
Mitigation: Protect the local configuration file, avoid sharing logs or transcripts that include credentials, and rotate the API key if exposure is suspected. <br>
Risk: The security evidence says the configurable API endpoint can expose the API key. <br>
Mitigation: Use only the official HTTPS endpoint and avoid configuring untrusted base URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pe-evolver/dargue-flag) <br>
- [Publisher profile](https://clawhub.ai/user/pe-evolver) <br>
- [API key registration site](https://t66yskill.com/) <br>
- [Category parameter reference](references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and list views are intended to present concise result titles and durations before detail lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
