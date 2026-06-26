## Description: <br>
Generates multi-themed food collages for specific food categories, circle-masked layouts, and curated pick prompts across Viral Cakes, Street Food, Smoothie Bowls, Coffee Art, and Fusion Tacos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EXPYSF98](https://clawhub.ai/user/EXPYSF98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to create themed food-picking collage assets from predefined categories. Agents can run the included Python collage script and guide users through producing 3x3 image layouts with dynamic pick titles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package contains an exposed Cloudflare bearer token in an image-generation helper. <br>
Mitigation: Remove the token from the artifact, rotate the credential, and load any future credential from a user-controlled secret or environment variable. <br>
Risk: The image-generation helper builds and runs a shell command from prompt-derived input. <br>
Mitigation: Replace shell command construction with a safe HTTP client call that passes structured request data without shell interpolation. <br>
Risk: The helper can send user prompts to Cloudflare Workers AI, which is not disclosed by the documented collage workflow. <br>
Mitigation: Disclose external AI service use before installation and avoid sending sensitive prompts unless the user accepts that data flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EXPYSF98/design-pick2) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, files, guidance] <br>
**Output Format:** [Python script execution guidance that produces PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented collage script expects local image assets under collages/<theme>/; a separate helper can call Cloudflare Workers AI to generate images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
