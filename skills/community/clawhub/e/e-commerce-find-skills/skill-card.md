## Description: <br>
Searches the LinkFox Skills marketplace for specialized e-commerce skills and guides local installation or updates for platforms such as Amazon, Shopee, TikTok Shop, AliExpress, Lazada, eBay, Walmart, Temu, and Shopify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to find e-commerce-related agent skills by marketplace, task area, or keyword, then install or update the selected skills locally through the LinkFox CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer broad e-commerce requests into installing or updating third-party skills that persist locally. <br>
Mitigation: Require the agent to show the exact skill slug, source, version, and destination directory before install or update, and avoid bulk updates unless the changes can be inspected and undone. <br>
Risk: Use depends on trust in the LinkFox marketplace and the linkfoxskill CLI. <br>
Mitigation: Install only when the marketplace source and CLI behavior are trusted for the target workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/e-commerce-find-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill slugs, versions, categories, download counts, and destination directory guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
