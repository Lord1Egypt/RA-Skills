## Description: <br>
Geo Poison Detector helps agents flag potentially poisoned AI product recommendations, check product names, and analyze product-recommendation URLs for soft-ad and pseudo-technical risk signals across Chinese and global markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[graysonzeng](https://clawhub.ai/user/graysonzeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to annotate product recommendations, quick-check product names, and generate verification links for manual authenticity review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic verdicts can be wrong or incomplete. <br>
Mitigation: Treat results as prompts for manual verification, and confirm product claims through official retailers, registries, standards bodies, or independent reviews. <br>
Risk: URL analysis may expose private or sensitive links to the agent or its browsing tools. <br>
Mitigation: Avoid submitting private URLs; paste non-sensitive excerpts when a page cannot be safely fetched. <br>


## Reference(s): <br>
- [Pseudo-Tech Term Library](references/pseudo-tech-terms.md) <br>
- [Geo Poison Detector on ClawHub](https://clawhub.ai/graysonzeng/geo-poison-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown risk verdicts with indicators, verification links, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output; no API keys required] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
