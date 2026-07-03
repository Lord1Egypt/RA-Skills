## Description: <br>
Generates final e-commerce video payloads by reading storyboard JSON, compressing script text, extracting duration and product reference images, and optionally submitting the request to an AIGC video service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bstory28](https://clawhub.ai/user/bstory28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and e-commerce creative operators use this skill after storyboard generation to prepare the final video-generation request. It produces compressed script text and a standardized video payload, with preview mode by default and submit mode when external generation is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submit mode can send storyboard text, product reference images, and payload details to the configured AIGC service. <br>
Mitigation: Use preview mode first for sensitive or unreleased assets, and run `--submit` only after reviewing the configured service's privacy and retention terms. <br>
Risk: The generated video payload may contain product or customer-sensitive material from upstream storyboard and image inputs. <br>
Mitigation: Review the generated `video_payload.json` before submission and avoid using real customer or proprietary assets unless approved for the external service. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/BStory28/ecommerce-video-generator) <br>
- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-video-generator) <br>
- [Upstream product info generator](https://github.com/BStory28/ecommerce-product-info-generator) <br>
- [Upstream video script generator](https://github.com/BStory28/ecommerce-video-script-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance plus generated text and JSON payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AIGC_APP_KEY/AIGC_APP_SECRET for submit mode; preview mode saves payload files without external submission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter and release changelog mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
