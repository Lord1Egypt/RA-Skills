## Description:

Agent Lens helps agents track AI API calls, analyze token usage, monitor costs, and generate cost reports for OpenAI, Anthropic, Google, and DeepSeek APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Agent Lens to monitor LLM API spending, inspect token usage, latency, and error trends, and generate reports for cost optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party code from GitHub.

Mitigation: Review the package before installation, pin it to a trusted release or commit, and run it in an isolated environment.

Risk: Local trace data and exports may reveal model usage, costs, timestamps, and prompt-related context.

Mitigation: Restrict access to the local trace database and exported files, avoid recording secrets or unnecessary prompt content, and clean or rotate stored data periodically.

Risk: Cost estimates can differ from actual provider billing because pricing and discounts may vary.

Mitigation: Use reports for operational analysis, then verify material cost decisions against provider billing and current pricing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with code blocks and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost-analysis guidance, command suggestions, and code snippets for tracking API usage.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
