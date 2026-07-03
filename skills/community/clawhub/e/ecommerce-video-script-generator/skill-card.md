## Description: <br>
Generates 10-second and 15-second structured e-commerce video storyboards from product selling points, category, function, user pain point, and target market, with JSON output for an AI pipeline and Markdown for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bstory28](https://clawhub.ai/user/bstory28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, e-commerce operators, and video production agents use this skill to convert product images and selling-point configuration into localized short-form commerce video storyboards. It is intended as the second stage of an AI video generation pipeline, producing structured storyboard files for downstream rendering and human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selling-point and usage-instruction fields can influence generated storyboards. <br>
Mitigation: Treat product configuration as untrusted input and review generated storyboard JSON and Markdown before downstream use. <br>
Risk: The skill declares SUDOCODE_API_KEY for AI-assisted generation. <br>
Mitigation: Provide credentials only in trusted environments and avoid including private or unnecessary sensitive data in product inputs. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/BStory28/ecommerce-video-script-generator) <br>
- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-video-script-generator) <br>
- [Upstream product information generator](https://github.com/BStory28/ecommerce-product-info-generator) <br>
- [Downstream ecommerce video generator](https://github.com/BStory28/ecommerce-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, text, shell commands, guidance] <br>
**Output Format:** [Structured storyboard JSON, human-review Markdown, and concise chat guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates storyboard.json and storyboard.md; uses target market, video type, product category, function, pain point, and duration to shape the storyboard.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; source skill frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
