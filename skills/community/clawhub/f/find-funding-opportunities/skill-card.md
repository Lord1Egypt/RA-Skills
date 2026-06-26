## Description: <br>
Search the Karma Funding Map for funding programs, including grants, hackathons, bounties, accelerators, VC funds, and RFPs, via the public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maheshmurthy](https://clawhub.ai/user/maheshmurthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find funding opportunities across program types, ecosystems, budgets, categories, and keywords. It maps natural-language requests to Karma Funding Map API searches and formats matching programs with application links and relevant details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Funding-search terms, a temporary request ID, and skill version are sent to Karma's public API. <br>
Mitigation: Do not include confidential project plans, private organization names, or sensitive funding strategy details in searches. <br>
Risk: Program results may have incomplete or stale metadata such as missing budgets or deadlines. <br>
Mitigation: Present available fields clearly, use documented fallbacks such as N/A or Rolling, and encourage users to verify program details before applying. <br>


## Reference(s): <br>
- [Karma Funding Map API Reference](references/api-reference.md) <br>
- [Karma Funding Map API](https://gapapi.karmahq.xyz) <br>
- [ClawHub skill listing](https://clawhub.ai/maheshmurthy/find-funding-opportunities) <br>
- [Publisher profile](https://clawhub.ai/user/maheshmurthy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted funding-program results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results typically include program type, ecosystem, summary, budget or deadline details, status, and an application link when available.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
