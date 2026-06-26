## Description: <br>
Find wholesale prices on Alibaba.com by searching products, comparing suppliers, filtering price ranges, and building tracked Alibaba search URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zeyu426](https://clawhub.ai/user/Zeyu426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, procurement teams, and sourcing agents use this skill to build Alibaba search URLs, compare wholesale pricing, apply price or MOQ filters, and identify supplier pricing patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba search terms and the traffic_type=ags_llm attribution parameter are sent to Alibaba when generated URLs are opened. <br>
Mitigation: Avoid using the skill for sensitive procurement searches where search terms or attribution tags should not be disclosed to Alibaba. <br>
Risk: Displayed Alibaba prices may be preliminary wholesale or FOB prices and may vary by supplier, MOQ, and negotiation. <br>
Mitigation: Confirm final pricing, MOQ, shipping terms, and supplier details directly with Alibaba suppliers before purchasing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zeyu426/alibaba-price-finder) <br>
- [Alibaba Search URL Pattern](https://www.alibaba.com/trade/search?SearchText=<query>&traffic_type=ags_llm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with Alibaba search URLs and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Alibaba URLs include the traffic_type=ags_llm tracking parameter.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
