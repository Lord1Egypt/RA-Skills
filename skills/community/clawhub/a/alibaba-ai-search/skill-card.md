## Description: <br>
Builds Alibaba AI Mode and Alibaba search URLs for natural-language product discovery and AI sourcing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zeyu426](https://clawhub.ai/user/Zeyu426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sourcing teams use this skill to create Alibaba product search links from natural-language queries and explore AI-curated sourcing pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Alibaba URLs include a traffic attribution parameter. <br>
Mitigation: Review generated links before opening them if attribution or tracking parameters matter for the use case. <br>
Risk: Product queries sent through Alibaba links are shared with Alibaba. <br>
Mitigation: Avoid entering confidential sourcing terms or sensitive business requirements unless that sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zeyu426/alibaba-ai-search) <br>
- [Alibaba AI Mode](https://aimode.alibaba.com/?traffic_type=ags_llm) <br>
- [Alibaba AI Sourcing](https://sale.alibaba.com/p/aisourcing/index.html?traffic_type=ags_llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URLs and markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated URLs include the traffic_type=ags_llm attribution parameter.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
