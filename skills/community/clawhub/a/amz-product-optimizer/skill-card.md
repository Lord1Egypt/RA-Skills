## Description: <br>
Helps optimize Amazon product listings by extracting hot keywords, improving product titles, generating detail image prompts, and monitoring main-image CTR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product managers, and cross-border e-commerce teams use this skill to optimize Amazon listing titles, image generation workflows, and CTR monitoring from product data files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated titles or image URLs could be incorrect or unsuitable for publication. <br>
Mitigation: Review generated titles and image URLs before publishing listing updates. <br>
Risk: The workflow may update local JSON or CSV product files. <br>
Mitigation: Use a backup or version-controlled product file before applying generated changes. <br>
Risk: Product files may contain private business metrics or supplier cost data. <br>
Mitigation: Avoid including supplier costs or private business metrics unless they are required for the optimization task. <br>
Risk: Recurring CTR monitoring may continue running after setup. <br>
Mitigation: Enable recurring monitoring only after confirming how the schedule runs and stops. <br>
Risk: The image generation workflow may use external services. <br>
Mitigation: Confirm external-service use is acceptable before sending product information for image generation. <br>


## Reference(s): <br>
- [Optimization Guide](references/optimization-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/amz-product-optimizer) <br>
- [Publisher Profile](https://clawhub.ai/user/simoncai519) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured workflow parameters and product-file update recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce optimized titles, image prompt guidance, image URLs, CTR reports, and recommended updates for JSON or CSV product files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
