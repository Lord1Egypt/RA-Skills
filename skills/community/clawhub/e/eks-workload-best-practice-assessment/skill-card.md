## Description: <br>
Assesses Kubernetes workloads running on Amazon EKS for best practice compliance across workload configuration, security posture, observability, networking, storage, image security, and CI/CD practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect Amazon EKS workload configurations and produce a best-practice assessment report for selected clusters, namespaces, or workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assessment can collect broad cluster, workload, RBAC, service account, image scan, and event data that may expose sensitive operational details. <br>
Mitigation: Limit execution to approved clusters, regions, namespaces, and workloads, and handle generated reports as sensitive operational data. <br>
Risk: The documentation includes access setup examples that can exceed read-only assessment needs. <br>
Mitigation: Use least-privilege read-only Kubernetes and AWS permissions where possible, and separately approve any cluster-admin access before use. <br>
Risk: Remediation guidance or commands may change workload behavior if applied without review. <br>
Mitigation: Review proposed changes before execution, validate them in an appropriate environment, and confirm whether a workload restart or rollout is required. <br>


## Reference(s): <br>
- [EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html) <br>
- [AWS Knowledge MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) <br>
- [Context7 MCP](https://github.com/upstash/context7) <br>
- [Check Dimensions](references/check-dimensions.md) <br>
- [Kubectl Assessment Commands](references/kubectl-assessment-commands.md) <br>
- [Output Template](references/output-template.md) <br>
- [Search Queries](references/search-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with assessment tables, summarized terminal status, and inline shell commands or remediation guidance when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill saves the full assessment report to a local markdown file and prints only a concise summary with file path, score, and PASS/FAIL/WARN counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
