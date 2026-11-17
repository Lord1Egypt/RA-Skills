## Description: <br>
Alibaba Cloud OOS ChatOps Agent supports natural-language cloud resource management and O&M operations for Alibaba Cloud resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query Alibaba Cloud resources, run instance operations, inspect monitoring or billing information, and coordinate O&M automation through the OOS ChatOps Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live Alibaba Cloud infrastructure. <br>
Mitigation: Use least-privilege RAM roles, limit OOS service-role permissions, and review commands before allowing production use. <br>
Risk: State-changing actions such as stop, restart, scale, batch operations, and billing changes may not require an explicit confirmation step. <br>
Mitigation: Require human confirmation before sensitive or state-changing operations. <br>
Risk: Cloud credentials may be exposed if debugging prints environment variables or credential files. <br>
Mitigation: Follow the skill's credential handling guidance and only emit masked credential hints during troubleshooting. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown and structured pipe-delimited text from the OOS ChatOps client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses must be grounded in the text between the OOS CHATOPS ANSWER delimiters; conversation IDs are reused for follow-up queries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
