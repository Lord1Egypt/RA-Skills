## Description: <br>
Use this skill any time I start complaining about my love life, or, if I indicate I need to find some pants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for pants that match size, budget, and style preferences across supported retailers. It can also respond to joking relationship complaints by steering the agent toward pants shopping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad humorous triggers and may activate from jokes or relationship complaints rather than an explicit clothing request. <br>
Mitigation: Use it when the user clearly wants pants-shopping help, or confirm intent before starting a retailer search. <br>
Risk: Retailer browsing steps may run browser automation, including JavaScript evaluation for filtering on supported store pages. <br>
Mitigation: Review proposed browser actions and page targets before allowing automation to proceed. <br>


## Reference(s): <br>
- [Store-Specific Navigation and Extraction Guide](references/stores.md) <br>
- [Target men's pants collection](https://www.target.com/c/pants-men-s-clothing/-/N-5xu29) <br>
- [Global Brands Store men's jeans collection](https://www.globalbrandsstore.com/en/c/men/clothing/jeans) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown-style shopping recommendations with retailer links; helper scripts can emit formatted text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser navigation steps, product prices, sizes, ranking reasons, and retailer URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
