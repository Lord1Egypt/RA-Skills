## Description: <br>
Ctrip Compare helps an agent extract and compare Ctrip group-tour products from detail or search-list URLs, then produce a concise Markdown comparison for the user's travel choice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxiaoshuai98](https://clawhub.ai/user/zhangxiaoshuai98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel shoppers and agents use this skill to compare multiple Ctrip group-tour products by date-sensitive price, itinerary, supplier, hotel, meal, transport, and activity details. It supports both selected product-detail URLs and Ctrip search-list URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a local Chromium browser through remote debugging port 9222, which can expose broad control over the active browser session. <br>
Mitigation: Run it only against a separate temporary Chromium profile for Ctrip, not an everyday logged-in browser profile, and close the debug browser when finished. <br>
Risk: The documented restart flow may terminate browser processes before reopening the browser in debug mode. <br>
Mitigation: Save browser work first, avoid automatic process kills unless necessary, and approve any restart action explicitly. <br>


## Reference(s): <br>
- [Ctrip Compare on ClawHub](https://clawhub.ai/zhangxiaoshuai98/ctrip-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated comparison files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces raw extracted text files and summarized text files before the final Markdown comparison.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
