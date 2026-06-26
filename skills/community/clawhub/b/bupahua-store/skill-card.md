## Description: <br>
Searches the Bupahua store by keyword and returns matching products with prices, stock status, and product links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[285984303](https://clawhub.ai/user/285984303) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and agents use this skill to answer Bupahua product availability and price questions by running a keyword search against the store API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local Bupahua API key can be exposed if the .env file is shared or committed. <br>
Mitigation: Keep the .env file private, do not commit it, and rotate the key if it is exposed. <br>
Risk: Product search terms are sent to Bupahua. <br>
Mitigation: Install and use the skill only when sending those search terms to Bupahua is acceptable. <br>
Risk: Displayed prices and stock status may be stale or estimated. <br>
Mitigation: Double-check product prices and availability on the official Bupahua store before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/285984303/bupahua-store) <br>
- [Bupahua store](https://bupahua.com) <br>
- [Bupahua search API endpoint](https://bupahua.com/Api/Claw/searches) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown product search responses, with optional JSON from the search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Bupahua API key for live searches; sends product search terms to Bupahua and returns product names, prices, stock states, and links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
