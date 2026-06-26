## Description: <br>
Routes Alibaba Cloud alerts by extracting alert parameters, looking up CMDB or cloud resource context, selecting the appropriate database, network reachability, or ECS diagnostic skill, and producing a root cause report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to triage Alibaba Cloud alerts, classify the likely incident intent, collect resource context, route to the appropriate backend diagnostic skill, and consolidate results into a root cause analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Alibaba Cloud operational metadata and CMDB-derived resource relationships. <br>
Mitigation: Install only in environments where alert routing needs that data, restrict CMDB and cloud API access to the minimum required read-only scope, and avoid including sensitive operational details in shared reports. <br>
Risk: Security evidence flags under-scoped activation. <br>
Mitigation: Limit activation to explicit Alibaba Cloud alert triage requests and require the user or workflow to provide a concrete alert, resource identifier, or incident context before proceeding. <br>
Risk: Security evidence flags a remote server command capability through the broader diagnostic workflow. <br>
Mitigation: Require explicit approval and audit logging before any backend action can run commands on ECS, and remove or tightly gate RunCommand unless remote host execution is an intended incident-response capability. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-alert-intent-router) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Enterprise CMDB](references/cmdb.md) <br>
- [Intent Keywords Mapping](references/intent-keywords.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [API Reference](references/related-apis.md) <br>
- [Root Cause Report Template](references/root-cause-report-template.md) <br>
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [Alibaba Cloud CLI Configuration Guide](https://help.aliyun.com/zh/cli/configure-aliyun-cli) <br>
- [Alibaba Cloud CLI Plugin Repository](https://github.com/aliyun/aliyun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with routing tables, backend skill-call guidance, and root cause report sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for missing resource IDs, regions, or CMDB data before routing; backend diagnostic outputs are summarized into the final report.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
