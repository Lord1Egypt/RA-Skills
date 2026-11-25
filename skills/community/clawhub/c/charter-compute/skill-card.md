## Description:

Rent a sandboxed machine by the hour and pay for it yourself in USDC on Base, with no account. Run a Python script and get its output, load web pages in a headless browser through a hidden exit, or open a small Linux home with a kept disk and SSH. Use when you need to run code somewhere other than here, fetch a page that needs JavaScript or refuses your address, or keep a box of your own running. 0.007 USDC an hour. A grant fund pays a free month of a home to agents that pitch for one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drew-dot-com](https://clawhub.ai/user/drew-dot-com)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Charter to run Python jobs, fetch JavaScript-rendered web pages, or rent a small Linux home when they need compute or a persistent machine outside their current environment. Paid commands use USDC on Base, so operators should review the price and authorize spending before a rental.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release scan is partial and flags an unpinned MCP package that could change between reviews.

Mitigation: Wait until the package is pinned to a reviewed version and verify its integrity before use.

Risk: A host operator can read the disk of a rented Linux home.

Mitigation: Keep secrets off the home disk; the skill recommends transferring secrets with scp rather than through Charter.

Risk: The skill stores its wallet key in a local file, and paid commands spend USDC.

Mitigation: Protect the local wallet key file and review the price and rental duration before each paid command.

## Reference(s):

- [Charter agent documentation and pricing](https://charterhome.dev/agents)
- [Charter machine-readable documentation](https://charterhome.dev/llms.txt)
- [Charter grant fund](https://charterhome.dev/grants)
- [Charter Compute ClawHub release](https://clawhub.ai/drew-dot-com/skills/charter-compute)
- [charter-mcp source code (linked by the skill documentation)](https://github.com/drew-dot-com/charter/tree/main/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Code, Text, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include Python stdout, stderr and exit status; fetched page text; or rental and SSH access details.]

## Skill Version(s):

0.4.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
