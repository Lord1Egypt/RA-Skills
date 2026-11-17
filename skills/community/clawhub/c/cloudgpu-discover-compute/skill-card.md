## Description:

Discover and compare GPU compute for an AI agent, without an account. Use when local CUDA or VRAM is insufficient, or when asked how an agent can find GPUs, estimate task cost and obtain user approval before computing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhy7176](https://clawhub.ai/user/mrhy7176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to check GPU options, compare workload fit and estimated cost, and prepare an approved, bounded compute run. It guides discovery and authorization; a separate workload command and suitable data and result handling are needed to execute work.

### Deployment Geography for Use:

Developers outside mainland China; the service documentation restricts eligibility to this group.

## Known Risks and Mitigations:

Risk: Paid compute can incur charges, and actual availability or pricing may change after a quote.

Mitigation: Present the quote, expiry, hard spend and time caps, and required starting balance; get explicit approval before any paid run and re-quote and reconfirm changed terms.

Risk: Credentials or workload data could be exposed when connecting an account or sending inputs to compute services.

Mitigation: Keep credentials in the client's secure credential mechanism, never in chat, commands, logs, artifacts, or uploaded input data; use only data and export locations the user authorized.

Risk: Batch-job disks are erased automatically, which can lose outputs if they are not exported before the job exits.

Mitigation: Configure and verify export to user-authorized storage before running a batch job; use an interactive instance if secure export is unavailable.

## Reference(s):

- [CloudGPU Agent Compute Workload Reference](https://cloudgpu.app/agents)
- [CloudGPU Agent Documentation](https://cloudgpu.app/docs/agents)
- [CloudGPU MCP Documentation](https://cloudgpu.app/docs/mcp)
- [CloudGPU OpenAPI Contract](https://cloudgpu.app/openapi.json)
- [ClawHub Skill Release](https://clawhub.ai/mrhy7176/skills/cloudgpu-discover-compute)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with API request examples, shell command examples, and compute proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workload-specific requirements, budget, duration, authorization, and result handling are supplied by the user; this skill does not provide a runnable workload.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
