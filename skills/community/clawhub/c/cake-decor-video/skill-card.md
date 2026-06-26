## Description: <br>
Generate vertical short videos of cake decorating and pastry finishing with WeryAI, including frosting, piping, mirror glaze, and other handmade dessert moments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to turn cake decorating or pastry briefs into WeryAI text-to-video or image-to-video generation runs. It expands the user's brief, confirms model parameters before submission, and returns generated video URLs or clear API failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key for model lookup, generation, and status checks. <br>
Mitigation: Install only when the publisher is trusted enough to receive WERYAI_API_KEY, and keep the key out of committed files. <br>
Risk: WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL can redirect requests, prompts, images, and bearer tokens to alternate endpoints. <br>
Mitigation: Leave endpoint override variables unset unless intentionally using trusted alternate WeryAI endpoints. <br>
Risk: Successful video generation runs consume paid WeryAI credits. <br>
Mitigation: Review the confirmation table and parameters before each generation request. <br>


## Reference(s): <br>
- [Cake Decor Video on ClawHub](https://clawhub.ai/zoucdr/cake-decor-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY; successful generation requests may consume paid WeryAI credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
