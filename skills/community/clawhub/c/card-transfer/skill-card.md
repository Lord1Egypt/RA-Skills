## Description: <br>
Returns transfer partners, ratios, timing, and restrictions for one major U.S. credit card across major issuers, including co-branded hotel and airline cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel rewards users and agents use this skill to identify credit card transfer partners, ratios, timing, caveats, and source-backed confidence notes for a specific card variant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transfer partners, ratios, timing, and restrictions can change or conflict across sources. <br>
Mitigation: Use current issuer and approved secondary sources, list fetched sources, and flag uncertain or conflicting claims in confidence notes. <br>
Risk: The optional BRAVE_API_KEY is a search API credential. <br>
Mitigation: Configure the key only when needed and avoid asking the skill to process private account numbers or personal financial details. <br>
Risk: The skill uses web search and page fetches to answer current card-program questions. <br>
Mitigation: Fetch only public HTTPS issuer or approved secondary pages and review source links before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahongc/card-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with section headings, numbered lists, confidence notes, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask a clarification question for ambiguous card names; relies on current public web sources when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
