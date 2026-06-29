## Description: <br>
Helps agents guide business portfolio reviews using the BCG growth-share matrix to classify strategic business units by market growth and relative market share and recommend invest, harvest, or exit actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external consultants, and strategy teams use this skill to prioritize business units, brands, or portfolio holdings that compete for shared capital. It supports annual strategy reviews, budget allocation, board discussions, PE/VC portfolio reviews, and M&A retain-versus-divest decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may disclose confidential revenue, market-share, competitor, or business-unit data while using the skill. <br>
Mitigation: Use the skill only in an agent environment trusted for the sensitivity of the business information being analyzed. <br>
Risk: Portfolio recommendations can be misleading if market boundaries, competitor share, growth data, or retained-unit synergies are not verified. <br>
Mitigation: Validate SBU definitions, external growth data, relative share calculations, trend arrows, and quantified synergies before acting on recommendations. <br>


## Reference(s): <br>
- [Sources - bcg-matrix](references/sources.md) <br>
- [The Product Portfolio](https://www.bcg.com/publications/1970/strategy-the-product-portfolio) <br>
- [The Experience Curve Reviewed](https://www.bcg.com/publications/1973/experience-curve-reviewed-history) <br>
- [Reversing the Images of BCG's Growth/Share Matrix](https://doi.org/10.1002/smj.4250050108) <br>
- [Strategic Attributes and Performance in the BCG Matrix](https://doi.org/10.2307/256079) <br>
- [Procter & Gamble Annual Reports](https://pginvestor.com/financial-information/annual-reports/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with tables, portfolio map fields, trend notes, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quadrant assignments, trend arrows, cash generator and absorber summaries, and dated strategy decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
