## Description:

基于Morgan Levine PhenoAge时钟模型，通过血液生物标志物计算生物年龄的服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call XiaoBenYang tools that calculate biological age from blood biomarkers using the Morgan Levine PhenoAge model and retrieve biomarker reference ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a XiaoBenYang API key in a local .env file.

Mitigation: Use only in environments where local .env storage is acceptable, restrict file access, and rotate the API key if exposure is suspected.

Risk: The skill sends biomarker inputs to a remote XiaoBenYang API.

Mitigation: Obtain user consent before submitting biomarker data and avoid using sensitive health data unless the remote service is approved for that use.

Risk: The artifact contains stale gaokao references unrelated to the biological-age workflow.

Mitigation: Review prompts, configuration names, and generated responses for domain mismatch before relying on the skill in a sensitive setting.

Risk: Dependencies are declared with lower bounds instead of pinned versions.

Mitigation: Pin and review dependency versions before deployment in controlled or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/biomarker-ranges)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Markdown or plain text summarizing JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends biomarker inputs to the remote API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
