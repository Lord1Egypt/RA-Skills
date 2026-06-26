## Description: <br>
Generates real-estate social marketing copy, image prompts, and optional local image-generation requests by combining a property profile with current Weibo hot-search topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chowshawn62-a11y](https://clawhub.ai/user/chowshawn62-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and sales users use this skill to create Chinese social posts and image-generation prompts for real-estate projects after checking property facts and current Weibo trends. It can also guide agents to fetch trend data, prepare a reusable property profile, and archive generated outputs locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime configuration can route Weibo trend collection through an external shell command. <br>
Mitigation: Review or remove the external_command option before installation, and keep runtime.json writable only by trusted users. <br>
Risk: The skill can contact Weibo and other real-estate or content sources while preparing property profiles and trend-linked copy. <br>
Mitigation: Use it only when external lookups are acceptable, and avoid confidential project details unless that external-search behavior is approved. <br>
Risk: Generated profiles and marketing outputs may be saved locally for reuse. <br>
Mitigation: Inspect archive locations and generated files, and avoid storing sensitive or unapproved project information. <br>
Risk: Marketing copy may include unverified property claims or overly strong promotional language. <br>
Mitigation: Review outputs against the provided risk rules before publication, especially claims about pricing, discounts, school access, delivery status, and guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chowshawn62-a11y/estate-flyer) <br>
- [Weibo hot search](https://weibo.com/hot/search) <br>
- [Weibo hot-search workflow](references/workflows/03-weibo-hot-search.md) <br>
- [Image-generation workflow](references/workflows/06-image-generation.md) <br>
- [Risk rules](references/compliance/risk-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured sections, inline command guidance, generated copy, image prompts, and status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs normally include Weibo trend scan results, property summary, main and alternate social copy, image prompts, negative prompts, image-generation result notes, and local archive guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
