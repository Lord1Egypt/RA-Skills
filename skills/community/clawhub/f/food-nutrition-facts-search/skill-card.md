## Description: <br>
Searches nutrition facts, food scores, and packaged product data via public AI-friendly endpoints for food names, brands, products, and barcodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charliex2](https://clawhub.ai/user/charliex2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find, compare, and summarize food and packaged product nutrition data, including label-style nutrients, scores, ingredients, brands, and barcodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food names, product names, brands, and barcodes entered by the user may be sent to foodbenchmark.com for public lookup. <br>
Mitigation: Avoid submitting sensitive or private queries and use only the disclosed public foodbenchmark.com endpoints. <br>


## Reference(s): <br>
- [Food Benchmark AI search endpoint](https://foodbenchmark.com/api/ai/search?q=whole%20milk&type=products) <br>
- [Food Benchmark product detail endpoint](https://foodbenchmark.com/api/ai/products/3017620422003) <br>
- [ClawHub skill page](https://clawhub.ai/charliex2/food-nutrition-facts-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown with concise structured summaries and optional comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include canonical Food Benchmark URLs; avoids raw data unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
