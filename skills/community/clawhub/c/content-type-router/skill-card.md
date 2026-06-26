## Description: <br>
Detects and routes visual content generation requests into structured content type configurations with layout rules, visual modes, typography guidance, and generation hints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify visual generation requests into content types such as hero shots, posters, infographics, and testimonials, then apply the matching layout, typography, and prompt guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A later implementation of database-backed routing could let DB-sourced rules influence generated prompts. <br>
Mitigation: Review that implementation and credentials separately, restrict Supabase table permissions, and treat database routing records as controlled configuration. <br>
Risk: Ambiguous content descriptions may be routed to a fallback or lower-confidence content type. <br>
Mitigation: Check the returned slug and confidence before injecting the selected configuration into downstream image-generation prompts. <br>


## Reference(s): <br>
- [Content Type Router on ClawHub](https://clawhub.ai/PHY041/content-type-router) <br>
- [Canlah AI](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes content type slugs, layout constraints, visual mode guidance, generation hints, and optional database mode guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
