## Description: <br>
Finds, shortlists, vets, and enriches US web development firms for website builds, rebuilds, ecommerce, CMS, landing page, microsite, and frontend projects using the ServiceGraph pro_services catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find US-based web development firms, apply platform, location, and vertical filters, review brief firm cards, and optionally enrich selected domains after credit approval. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ServiceGraph API key, which is a sensitive credential. <br>
Mitigation: Keep the key in an environment file or shell export and do not paste it into chat or generated content. <br>
Risk: Unlocking firm details spends ServiceGraph credits. <br>
Mitigation: Show the selected firms and credit cost before calling the unlock endpoint, and proceed only after user approval. <br>
Risk: The catalog is limited to US firms and excludes individual freelancers and offshore procurement requests. <br>
Mitigation: Keep searches scoped to US web development firms and defer or decline requests outside that boundary. <br>
Risk: Platform, framework, and vertical filters are keyword matches rather than structured tags. <br>
Mitigation: Validate filters with the check endpoint and present results as shortlist candidates that still need review. <br>


## Reference(s): <br>
- [Find Web Developer on ClawHub](https://clawhub.ai/nostrband/find-web-developer) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ServiceGraph API key; paid detail unlocks should be approved before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
