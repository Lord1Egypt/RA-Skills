## Description: <br>
Executes Coze workflows from an agent by accepting a workflow_id and JSON parameters, calling Coze, and returning the raw workflow response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this base skill to invoke Coze workflows by workflow_id with arbitrary JSON parameters, especially as a dependency for higher-level Coze workflow skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Coze API key and a local configuration file. <br>
Mitigation: Treat the API key as a secret, protect the config file, and avoid committing credentials. <br>
Risk: Workflow parameters are sent to Coze and may include sensitive or credential-like data. <br>
Mitigation: Avoid sending personal data or credentials as workflow parameters unless the workflow and data handling are approved. <br>
Risk: Some Coze workflows may spend credits, publish content, or modify external data. <br>
Mitigation: Require confirmation or allowlists for workflow IDs that can create cost or change external state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/noah-1106/coze-workflow) <br>
- [Coze Homepage](https://www.coze.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API response] <br>
**Output Format:** [JSON object with Coze execution status, output, execute_id, and debug_url.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the Coze API raw response; workflow output may be encoded as a JSON string.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata; artifact frontmatter reports 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
