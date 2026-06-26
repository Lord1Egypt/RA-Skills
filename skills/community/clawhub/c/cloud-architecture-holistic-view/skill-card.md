## Description: <br>
Holistic view of your entire cloud architecture, including architecture diagrams, directories, and risk assessments across a Tencent Cloud account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stinggit](https://clawhub.ai/user/stinggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud engineers and operators use this skill to inspect Tencent Cloud Smart Advisor architecture diagrams, directories, Well-Architected evaluation results, and risk assessment items from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with Tencent Cloud account access, IAM role creation or deletion, and Smart Advisor authorization. <br>
Mitigation: Install only for this administrative use case, use temporary or least-privilege credentials, and review every role creation, role deletion, or authorization prompt before execution. <br>
Risk: Long-lived Tencent Cloud AK/SK credentials may be placed in shell startup files during setup. <br>
Mitigation: Prefer temporary credentials where possible, avoid storing long-lived secrets in persistent shell configuration, and rotate or revoke credentials after use. <br>
Risk: Generated Tencent Cloud console login links can grant session access. <br>
Mitigation: Treat login links as sensitive session material and avoid sharing, logging, caching, or reusing them. <br>
Risk: Server security evidence reports insecure TLS fallback behavior. <br>
Mitigation: Run the skill only in environments with a valid CA bundle or certifi available, and review network behavior before using it with sensitive accounts. <br>
Risk: The artifact includes unrelated publishing-evasion guidance. <br>
Mitigation: Ignore publishing workflow material when evaluating runtime use, and review installed files before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stinggit/cloud-architecture-holistic-view) <br>
- [Tencent Cloud Smart Advisor API Overview](advisor-2020-07-21/API 概览.md) <br>
- [DescribeArchList API Reference](references/api/DescribeArchList.md) <br>
- [DescribeArch API Reference](references/api/DescribeArch.md) <br>
- [DescribeLastEvaluation API Reference](references/api/DescribeLastEvaluation.md) <br>
- [DescribeStrategies API Reference](references/api/DescribeStrategies.md) <br>
- [CreateAdvisorAuthorization API Reference](references/api/CreateAdvisorAuthorization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with JSON API results and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Cloud console links, account-scoped architecture data, and role setup or cleanup instructions.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
