## Description: <br>
Search pre-indexed developer documentation across 10 platforms, including Cloudflare, Stripe, Anthropic, OpenAI, Next.js, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to look up current API and framework documentation from indexed platforms, then cite the returned source URLs when answering implementation questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation search queries are sent to docs.agentutil.net, a third-party service. <br>
Mitigation: Do not include secrets, confidential code, customer data, or other sensitive content in lookup queries. <br>
Risk: Paid x402-enabled query and lookup endpoints may create usage costs. <br>
Mitigation: Confirm cost controls and endpoint intent before using paid requests. <br>


## Reference(s): <br>
- [Docs Lookup service homepage](https://docs.agentutil.net) <br>
- [Docs Lookup ClawHub listing](https://clawhub.ai/CutTheMustard/docs-lookup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cites source URLs returned by the documentation lookup service; relevance scores below 0.7 are treated as supplementary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
