## Description: <br>
Guides agents through BATNA and ZOPA analysis for non-trivial negotiations, including walk-away points, reservation prices, counterparty alternatives, and deal/no-deal strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure salary, term-sheet, vendor, customer-pricing, partnership, and M&A negotiations by computing BATNA, reservation, aspiration, opening offer, counterparty BATNA, and ZOPA before deciding whether to proceed or walk away. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Negotiation guidance can be wrong if BATNA, reservation, or counterparty estimates are incomplete or biased. <br>
Mitigation: Use the skill's falsifier and verification checklist, validate assumptions against current deal evidence, and seek qualified legal, financial, or HR review for high-stakes negotiations. <br>
Risk: The skill is text-only guidance, so its recommendations may not match a user's specific workflow or negotiation context. <br>
Mitigation: Review the SKILL.md guidance before deployment and adapt use to the user's jurisdiction, culture, organization policy, and deal constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/batna-zopa) <br>
- [Publisher profile](https://clawhub.ai/user/deciqai) <br>
- [Sources - batna-zopa](references/sources.md) <br>
- [Method in Action: Fisher and Ury, 1981 - The Harvard Negotiation Project](examples/fisher-and-ury-1981-the-harvard-negotiation-project.md) <br>
- [Harvard Program on Negotiation](https://www.pon.harvard.edu/) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis template with structured negotiation fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; no executable code, credential access, persistence, or data exfiltration behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
