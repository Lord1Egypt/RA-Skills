## Description: <br>
Build Alibaba.com URLs for agent navigation, including product searches, product detail pages, supplier profiles, RFQ pages, and special sections like AI Mode and Top Ranking, with the traffic_type=ags_llm tracking parameter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zeyu426](https://clawhub.ai/user/Zeyu426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, procurement professionals, and developers use this skill to construct Alibaba.com search, product, supplier, RFQ, and special-section URLs for product sourcing and browsing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated links carry the traffic_type=ags_llm attribution parameter. <br>
Mitigation: Use the skill only when that visible attribution is acceptable for the browsing workflow. <br>
Risk: Opening the cart or purchase-list URL from a logged-in Alibaba session may expose account-specific shopping context to the agent. <br>
Mitigation: Avoid logged-in cart or purchase-list navigation unless the agent is intended to access that context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zeyu426/alibaba-url-builder) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with URL patterns, Python examples, shell commands, and generated URL strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated URLs include the traffic_type=ags_llm attribution parameter.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
