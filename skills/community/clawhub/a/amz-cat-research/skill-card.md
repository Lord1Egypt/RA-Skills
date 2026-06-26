## Description: <br>
Amazon Category Research helps sellers automate ASIN analysis, competitor research, and Amazon market intelligence reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuancheng888](https://clawhub.ai/user/yuancheng888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Amazon sellers and marketplace operators use this skill to collect ASIN, SellerSprite, and SIF data, compare competitors, assess category opportunity, and produce a Feishu research report with a local Markdown backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates Feishu cloud documents under the user's identity and may require broad Feishu authorization. <br>
Mitigation: Review requested Feishu scopes before installation and use the skill only when cloud document storage is acceptable. <br>
Risk: The skill saves local Markdown report backups that may contain product research, ASIN lists, and market analysis. <br>
Mitigation: Avoid confidential inputs unless local retention is acceptable and delete workspace backups when they are no longer needed. <br>
Risk: The skill reads Amazon pages and SellerSprite/SIF plugin data through an OpenClaw browser profile. <br>
Mitigation: Use only browser profiles and plugin accounts intended for this research workflow, and confirm plugin login state before collection. <br>
Risk: Selector-healing behavior can alter extraction selectors and affect future report accuracy. <br>
Mitigation: Review proposed selector changes and confirm they match the intended Amazon, SellerSprite, or SIF fields before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/yuancheng888/amz-cat-research) <br>
- [README.en.md](README.en.md) <br>
- [BSR Node ID Mapping](references/bsr-node-mapping.md) <br>
- [Output Template](references/output-template.md) <br>
- [Negative Rules](references/negative-rules.md) <br>
- [DOM Selector Mapping](references/selectors.md) <br>
- [SellerSprite](https://www.sellersprite.com/) <br>
- [SIF](https://www.sif.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research report, Feishu document link, concise text summary, local Markdown backup, browser-evaluation JavaScript, and validation/configuration command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw browser profile, SellerSprite and SIF browser plugins, Feishu authorization for document creation, and Amazon page access; normal reports cover up to 20 ASINs.] <br>

## Skill Version(s): <br>
5.0.1 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
