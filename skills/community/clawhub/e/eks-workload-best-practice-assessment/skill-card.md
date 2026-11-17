## Description:

Assesses Kubernetes workloads on Amazon EKS against Kubernetes and EKS best practices across workload configuration, security, observability, networking, storage, platform integration, CI/CD, and image security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and security reviewers use this skill to assess workload-level Kubernetes configurations in Amazon EKS clusters and produce a prioritized compliance report. It supports cluster-wide, namespace-specific, or workload-targeted assessments using kubectl, AWS CLI, and documentation research tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation can steer users toward persistent cluster-admin access and cluster authentication changes beyond a read-oriented assessment need.

Mitigation: Use an explicitly chosen cluster, region, and namespace or workload scope; avoid the cluster-admin access example as a default; prefer a dedicated short-lived least-privilege assessment identity.

Risk: Generated assessment reports may contain sensitive security details about cluster workloads and configuration gaps.

Mitigation: Treat report files as sensitive security artifacts and restrict their storage, sharing, and retention.

## Reference(s):

- [EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html)
- [AWS Knowledge MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)
- [Context7 MCP](https://github.com/upstash/context7)
- [Check Dimensions](references/check-dimensions.md)
- [Kubectl Assessment Commands](references/kubectl-assessment-commands.md)
- [Output Template](references/output-template.md)
- [Search Queries](references/search-queries.md)
- [EKS Best Practices - Reliability](https://docs.aws.amazon.com/eks/latest/best-practices/reliability.html)
- [EKS Best Practices - Security](https://docs.aws.amazon.com/eks/latest/best-practices/security.html)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report saved to a local file, with a brief terminal summary of file path, overall score, and PASS/FAIL/WARN counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment output includes compliance scorecards, per-dimension findings, per-workload details, critical issues, and prioritized remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
