## Description: <br>
Handle messages in a food-tracking channel by routing food intake events through a deterministic food tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill in a dedicated food-tracking channel to log barcode lookups, estimate meals from images, and request daily nutrition summaries with configurable limit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food intake logs are persisted in the workspace and may contain sensitive personal nutrition data. <br>
Mitigation: Install only where persistent food logs are acceptable, and set FOOD_LOG and FOOD_PROFILE_PATH to locations controlled by the user. <br>
Risk: Barcode lookups send product codes to the Open Food Facts public API. <br>
Mitigation: Use barcode logging only when querying Open Food Facts is acceptable for the user's privacy posture. <br>
Risk: Photo estimates may send meal images to a remote vision model. <br>
Mitigation: Avoid photo estimates for private images unless remote image processing is acceptable. <br>


## Reference(s): <br>
- [Food Channel on ClawHub](https://clawhub.ai/cdmichaelb/food-channel) <br>
- [Open Food Facts API](https://world.openfoodfacts.org/api/v2/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown replies with inline shell commands and JSON-backed nutrition summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent CSV food logs and may process food images through a remote vision tool.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
