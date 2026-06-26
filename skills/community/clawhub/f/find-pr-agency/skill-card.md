## Description: <br>
Find, shortlist, vet, and enrich US public-relations and communications agencies using ServiceGraph data, with guidance for PR-specific filtering, credential handling, and credit-based detail unlocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to locate US PR and communications agencies for media relations, crisis communications, investor relations, public affairs, product launches, and related PR needs. It helps produce filtered shortlists, brief firm summaries, unlock-cost guidance, and enrichment workflows. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph API key for authenticated searches. <br>
Mitigation: Keep the key in .env.local or an MCP auth flow and do not paste it into chat. <br>
Risk: Detailed firm enrichment can spend ServiceGraph credits. <br>
Mitigation: Review credit costs and get approval before unlocking detailed firm records. <br>
Risk: The skill is scoped to US public-relations and communications agencies. <br>
Mitigation: Use the skill only for US PR/comms procurement and defer broader marketing or non-US requests to a more suitable workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nostrband/find-pr-agency) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/nostrband) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>
- [ServiceGraph API Keys](https://servicegraph.co/profile/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, REST examples, filters, and shortlist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference free searches and paid detail unlocks; detailed firm enrichment can spend ServiceGraph credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version is 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
