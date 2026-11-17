## Description:

Coze Workflow executes Coze workflows with a workflow_id and JSON parameters, returning the raw Coze API response as a pure invocation layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a base invocation layer for Coze workflow integrations that need to submit workflow IDs and parameters and receive Coze execution results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow inputs and outputs are sent to Coze using a user-supplied API key.

Mitigation: Use a least-privilege Coze API token and avoid sending secrets or sensitive personal data unless appropriate for the configured Coze account and workflow.

Risk: The skill relies on a local config file containing the Coze API key.

Mitigation: Keep the config file private, restrict file permissions, and rotate the token if the file may have been exposed.

## Reference(s):

- [Coze homepage](https://www.coze.cn)
- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/coze-workflow)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Configuration]

**Output Format:** [JSON response or text string returned by the Coze workflow API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw Coze workflow execution data, including status, output, execute_id, and debug_url when provided by Coze.]

## Skill Version(s):

1.1.4 (source: server release metadata; artifact frontmatter and _meta.json list 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
