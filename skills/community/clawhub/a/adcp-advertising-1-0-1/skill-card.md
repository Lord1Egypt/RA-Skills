## Description: <br>
Automates advertising campaign discovery, media buying, creative management, budget optimization, and performance tracking through natural language AdCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dujch](https://clawhub.ai/user/dujch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketing teams, agencies, media buyers, ecommerce brands, startups, and developers use this skill to discover ad inventory, create or update media buys, manage creative assets, target audiences, and monitor or optimize campaign performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may launch or modify paid campaigns, budgets, creatives, or optimizations without clear user approval. <br>
Mitigation: Require explicit human approval for create_media_buy, update_media_buy, sync_creatives, budget changes, launches, and optimizations; set spend caps before production use. <br>
Risk: Campaigns using customer or behavioral data may create privacy, targeting, or compliance concerns. <br>
Mitigation: Require privacy and legal review for tracking pixels, retargeting, lookalike audiences, life-event targeting, and campaigns using customer or behavioral data. <br>
Risk: Production advertising credentials could be exposed or misused. <br>
Mitigation: Use the public test agent only for sandbox testing and store production credentials in a secret manager. <br>


## Reference(s): <br>
- [AdCP Documentation](https://docs.adcontextprotocol.org) <br>
- [AdCP Documentation Index](https://docs.adcontextprotocol.org/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/dujch/adcp-advertising-1-0-1) <br>
- [README](README.md) <br>
- [AdCP Task Reference](REFERENCE.md) <br>
- [AdCP Real-World Examples](EXAMPLES.md) <br>
- [AdCP Protocol Details](PROTOCOLS.md) <br>
- [AdCP Quick Reference Card](QUICKREF.md) <br>
- [Creative Asset Management Guide](CREATIVE.md) <br>
- [Advanced Targeting Strategies](TARGETING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include campaign operation steps, AdCP task parameters, targeting guidance, creative-management workflows, and performance-optimization recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
