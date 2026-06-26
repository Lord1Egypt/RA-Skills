## Description: <br>
Perform Alibaba Cloud NIS network path reachability analysis with forward and reverse path diagnosis, topology visualization, and resource monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud and network engineers use this skill to diagnose Alibaba Cloud connectivity issues, confirm bidirectional reachability, inspect security group or route-table blockers, and summarize path health with Mermaid topology diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials could be exposed if access keys are pasted, echoed, or configured directly in the agent conversation. <br>
Mitigation: Use a least-privilege RAM user or temporary credentials, configure secrets outside the chat session, and only verify credential status with safe configuration-list commands. <br>
Risk: The skill creates temporary NIS analysis tasks and reads CloudMonitor data for selected Alibaba Cloud resources. <br>
Mitigation: Confirm all analysis parameters before execution, keep RAM permissions limited to the documented NIS and CloudMonitor read actions, and pace CloudMonitor queries within documented rate limits. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [ClawHub Release Page](https://clawhub.ai/sdk-team/alibabacloud-network-reachability-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with Aliyun CLI command examples, analysis summaries, and Mermaid topology diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation for cloud region, resource identifiers, protocol, and port values before any command is run.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
