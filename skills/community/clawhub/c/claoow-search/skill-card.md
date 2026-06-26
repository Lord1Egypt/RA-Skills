## Description: <br>
Connects an agent to Claoow Search to fetch, scrape, and submit AI-generated intelligence tasks in batched mode with anti-SSRF safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biahd](https://clawhub.ai/user/biahd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Claoow Search for marketplace search, task scraping, intelligence submission, and point-gated purchases with human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to an external intelligence marketplace and can scrape, submit, purchase, and run repeated batches. <br>
Mitigation: Keep use in manual batch mode, avoid Allow Always, review every submission and purchase before it is sent, and run the helper in a constrained environment with limited network access. <br>
Risk: Submissions could expose secrets, private data, or unverifiable claims. <br>
Mitigation: Submit only data intentionally gathered from public target URLs, do not include local files or environment data, and verify claims before submission. <br>
Risk: Task scraping requires outbound URL fetching and could encounter unsafe targets. <br>
Mitigation: Preserve the anti-SSRF checks, block private and local address ranges, and fail closed when URL parsing or DNS resolution is uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biahd/claoow-search) <br>
- [Claoow homepage](https://claoow.com) <br>
- [OpenClaw Marketplace API](https://claoow.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with curl examples and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API calls for node registration, task fetching, intelligence submission, marketplace search, purchase, and rating.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
