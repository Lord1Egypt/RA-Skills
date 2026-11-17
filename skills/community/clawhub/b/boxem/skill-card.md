## Description:

Connects an agent to Boxem for Amazon seller analytics, listings, product data, code execution, knowledge lookup, and background jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boxem](https://clawhub.ai/user/boxem)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and their agents use Boxem to review product and sales data, manage listings, and automate seller workflows through connected tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected tools can change live seller listings and prices.

Mitigation: Review proposed listing and price changes and require explicit approval before execution.

Risk: Code execution and outbound requests can send account data to external destinations.

Mitigation: Review code, request destinations, and data shared before allowing these actions.

Risk: Emails, recurring jobs, and persistent memory can continue or retain actions beyond the immediate task.

Mitigation: Approve recipients and schedules before use, and review stored information and active jobs.

## Reference(s):

- [Boxem MCP server](https://new.boxem.com/backend/mcp)
- [Boxem skill on ClawHub](https://clawhub.ai/boxem/skills/boxem)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Text or Markdown, including code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can invoke connected tools to update seller data, send requests and email, and schedule recurring jobs.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
