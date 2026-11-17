## Description:

Helps agents check live domain availability, generate brandable available domains, run pattern-based domain searches, and perform basic domain due diligence through Domain Search King's remote MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmalls22-rgb](https://clawhub.ai/user/johnsmalls22-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs verified domain availability, naming candidates, RDAP-informed domain checks, or registration next-step links without guessing availability from model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain names, keywords, and business descriptions are sent to Domain Search King during use.

Mitigation: Avoid submitting sensitive naming plans or confidential business descriptions unless the user accepts disclosure to the third-party service.

Risk: The skill instructs agents to pass through third-party registration links verbatim.

Mitigation: Treat registration links as untrusted third-party links; verify the registrar, destination URL, pricing, and terms before purchase.

Risk: The skill encourages automatic external calls for domain checks.

Mitigation: Confirm the user is comfortable with the external live-registry check, and report failed or empty responses instead of guessing availability.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/johnsmalls22-rgb/skills/dsk-available-domains)
- [Domain Search King MCP docs](https://domainsearchking.com/mcp)
- [Domain Search King MCP endpoint](https://domainsearchking.com/api/mcp)
- [Domain Search King AI Hallucination Index](https://domainsearchking.com/ai-hallucination-index)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown guidance with JSON-RPC curl examples and domain availability results from the remote service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned results may include registration URLs that should be shown verbatim and independently verified before purchase.]

## Skill Version(s):

1.1.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
