## Description: <br>
DeepContent helps an agent turn URLs into branded LinkedIn, X, and Reddit posts, discover topics, manage posts and brands, and route team, billing, and authentication workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and content teams, founders, and social media operators use this skill through an agent to generate branded social posts from URLs, discover content topics, manage saved posts, and coordinate brand or team account tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an account API key for brand, team, billing, and post-management workflows. <br>
Mitigation: Install only for trusted DeepContent accounts, keep DEEPCONTENT_API_KEY scoped to the intended account, and confirm before team invites, brand updates, approvals, or other account-changing actions. <br>
Risk: Generated posts and saved preferences may contain URLs, brand details, campaign strategy, or other sensitive marketing context. <br>
Mitigation: Review generated content and saved preferences before sharing, and clear or avoid storing confidential strategy when it is not needed for future sessions. <br>
Risk: Some endpoints are documented as slow and may require longer request timeouts. <br>
Mitigation: Use the documented longer timeouts for brand onboarding and topic generation, and present progress clearly when requests take longer than usual. <br>


## Reference(s): <br>
- [DeepContent ClawHub release](https://clawhub.ai/thierrypdamiba/deepcontentskill23223) <br>
- [DeepContent publisher profile](https://clawhub.ai/user/thierrypdamiba) <br>
- [DeepContent homepage](https://deepcontent-frontend.scaleintelligence.workers.dev) <br>
- [DeepContent OpenAPI specification](https://deepcontent-api.scaleintelligence.workers.dev/api/docs/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with social post drafts, dashboard links, and API-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DEEPCONTENT_API_KEY and may include generated post previews, remaining credit status, and links to DeepContent dashboard resources.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
