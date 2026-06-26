## Description: <br>
Generate 200+ page authority site content using the Authority-Knowledge-Answer (AKA) framework, including structured content, internal linking maps, and SEO metadata for platform-agnostic publishing with optional WordPress deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lebtiga](https://clawhub.ai/user/lebtiga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, SEO operators, content teams, and developers use this skill to plan and generate topical authority content hubs, SEO metadata, internal-linking structures, and exportable Markdown or JSON for CMS publishing. WordPress deployment is optional and should be tested with dry-run and staging workflows before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and publish large volumes of AI-written SEO content that may be inaccurate, misleading, or unsuitable for regulated topics. <br>
Mitigation: Review and fact-check all generated content before publishing, and require qualified professional review for legal, medical, or financial content. <br>
Risk: Optional WordPress deployment and auto-fix workflows can create or modify live pages, navigation, SEO metadata, theme settings, and site structure. <br>
Mitigation: Use --dry-run first, test on a staging site, use a dedicated limited WordPress account or application password, and revoke credentials after deployment. <br>
Risk: Business configuration and contact details are sent to Anthropic for content generation. <br>
Mitigation: Avoid including unnecessary sensitive data in the business configuration and confirm external API use is acceptable before generation. <br>
Risk: External packages or theme assets may affect local or WordPress environments. <br>
Mitigation: Verify any external npx package or theme ZIP before running or installing it. <br>


## Reference(s): <br>
- [AKA SEO Wireframe on ClawHub](https://clawhub.ai/lebtiga/aka-seo-wireframe) <br>
- [Publisher Profile](https://clawhub.ai/user/lebtiga) <br>
- [AKA SEO Wireframe Breakdown](https://rabihrizk.com/aka-seo-wireframe) <br>
- [AKA Content Generator](references/content-generator.md) <br>
- [AKA Internal Linker](references/internal-linker.md) <br>
- [AKA Wireframe WordPress Orchestrator](references/orchestrator.md) <br>
- [Master Prompts Collection](references/prompts-library.md) <br>
- [AKA SEO Optimizer](references/seo-optimizer.md) <br>
- [AKA Strategy Planner](references/strategy-planner.md) <br>
- [AKA WordPress Deployer](references/wordpress-deployer.md) <br>
- [AKA Framework WordPress Theme](assets/aka-framework-theme/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON files, SEO metadata, internal-link maps, configuration guidance, and optional WordPress REST deployment instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate many content files and optionally create or update WordPress pages when credentials are provided.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
