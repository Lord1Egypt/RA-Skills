## Description: <br>
Generate advertising images automatically from a product URL and brand profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and marketing teams use this skill to generate product advertising images from e-commerce product URLs, brand profiles, and campaign funnel objectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary product URLs, which may expose internal or private links if misused. <br>
Mitigation: Use only public product URLs and review requested links before running the skill. <br>
Risk: Model and reference images may preserve or replicate a person's likeness in advertising output. <br>
Mitigation: Provide model or reference images only when rights and consent cover advertising use of that likeness or source image. <br>
Risk: Product, logo, model, reference, brand, and brief data may be sent to ComfyDeploy and downstream AI services. <br>
Mitigation: Avoid confidential assets and review data-sharing expectations before installing or running the skill. <br>


## Reference(s): <br>
- [Ad-Ready ClawHub release](https://clawhub.ai/PauldeLavallaz/ad-ready) <br>
- [PauldeLavallaz publisher profile](https://clawhub.ai/user/PauldeLavallaz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated through ComfyDeploy and saved to the requested local image path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
