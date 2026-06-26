## Description: <br>
Return earning rates, bonus categories, caps, exclusions, and merchant-coding caveats for one major-US credit card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for the earning rates, reward categories, caps, exclusions, or merchant-coding caveats for a specific major U.S. credit card. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credit-card reward rates, caps, exclusions, and category rules can change or conflict across sources. <br>
Mitigation: Use current issuer information and approved secondary sources, then flag uncertain or conflicting details in confidence notes. <br>
Risk: The skill may use web lookups and can optionally use a Brave Search API key. <br>
Mitigation: Provide only the public card name, avoid account numbers or other private financial details, and supply a Brave Search API key only when that optional path is needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with rate summary, earning categories, caps and exclusions, confidence notes, and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Condensed factual output for one resolved card variant; ambiguous card names produce a numbered choice list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
