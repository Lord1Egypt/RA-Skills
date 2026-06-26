## Description: <br>
Find Ai Consultancy helps agents find, shortlist, vet, and enrich US AI, ML, and data consulting firms through the ServiceGraph pro_services catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and procurement teams use this skill to identify US AI, ML, data analytics, MLOps, LLM, computer vision, NLP, and related consulting firms. It guides authenticated ServiceGraph searches, filter validation, shortlist review, and optional paid firm-detail enrichment. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph API key or OAuth-backed ServiceGraph access. <br>
Mitigation: Store credentials in the harness environment or .env.local and do not paste keys into chat or generated artifacts. <br>
Risk: Firm-detail unlocks consume ServiceGraph credits. <br>
Mitigation: Use free search and brief reads first, then confirm selected apex domains and expected credit cost before unlocking details. <br>
Risk: The catalog is scoped to US firms and can omit or misclassify some AI-related companies. <br>
Mitigation: Keep the industry:data_ai_consulting filter pinned, validate filters before search, and skip results that are SaaS products, non-US firms, or otherwise outside the user's procurement scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nostrband/find-ai-consultancy) <br>
- [Publisher Profile](https://clawhub.ai/user/nostrband) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>
- [ServiceGraph pro_services Fields Endpoint](https://api.servicegraph.co/v1/datasets/pro_services/fields) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and shortlist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe ServiceGraph filters, credit costs, API calls, and credential setup steps without exposing secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
