## Description: <br>
Generates e-commerce product main-image and detail-page poster images through the Flyelep API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnwanj](https://clawhub.ai/user/cnwanj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request e-commerce product poster generation for marketplaces such as Amazon, Taobao, and other supported platforms. The agent prepares a JSON request, calls Flyelep by HTTP POST, and returns the generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product descriptions, reference image URLs, and the user's Flyelep API key to Flyelep. <br>
Mitigation: Only use it when sharing that data with Flyelep matches the user's data-handling requirements, and avoid private image URLs or proprietary product data unless approved. <br>
Risk: The Flyelep API requires the API key in the JSON body. <br>
Mitigation: Provide the key only at runtime, avoid storing real keys in examples or logs, and do not hard-code credentials in skill files. <br>


## Reference(s): <br>
- [Generate Poster Skill Page](https://clawhub.ai/cnwanj/generate-poster) <br>
- [Flyelep Platform](https://www.flyelep.cn) <br>
- [Flyelep Poster Generation API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generate) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies, curl examples, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs may be returned as a semicolon-delimited string; image generation can require a 300-600 second timeout.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
