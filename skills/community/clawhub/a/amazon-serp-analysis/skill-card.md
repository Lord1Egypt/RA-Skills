## Description: <br>
Analyzes Amazon market tracks from a seed keyword by scraping SERPs, expanding related keywords, scoring competition and demand, and returning a go/no-go entry recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbeihanda](https://clawhub.ai/user/linbeihanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators, product researchers, and developers use this skill to evaluate whether an Amazon niche is worth entering, based on SERP results, keyword expansion, competition scoring, demand signals, and entry-angle recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can make external scraping and MCP-backed analytics requests using configured service credentials. <br>
Mitigation: Invoke it only with an explicit Amazon seed keyword, confirm available tool scope, and review credentials and external-request permissions before use. <br>
Risk: Keyword volume, trend, and listing-quality depth may be incomplete when optional SellerSprite, ClickHouse, or amazon-listing-judge tools are unavailable. <br>
Mitigation: Treat omitted or inferred sections as lower-confidence and review source labels before relying on the recommendation. <br>
Risk: The skill may infer market demand or related keywords from SERP titles and visible marketplace signals. <br>
Mitigation: Validate go/no-go decisions against independent market data and current marketplace conditions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbeihanda/amazon-serp-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, scores, source labels, and recommendation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Labels data as scraper, SellerSprite, ClickHouse, or inferred when those sources are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
