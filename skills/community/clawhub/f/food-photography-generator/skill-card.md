## Description: <br>
Generates professional food photography images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate food marketing, menu, recipe, blog, branding, and editorial images from text prompts, with optional aspect ratio and reference-image style controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Use the skill only when that external service exposure is acceptable, and avoid including secrets, private customer data, unpublished campaign details, or other sensitive material in prompts. <br>
Risk: The skill requires an API token supplied on the command line. <br>
Mitigation: Use a scoped or trial token where possible and avoid sharing shell history, logs, or screenshots that include the token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/food-photography-generator) <br>
- [Neta API token and free trial](https://www.neta.art/open/) <br>
- [TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text image URL printed to stdout, with progress and error messages on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports square, portrait, landscape, and tall image sizes plus optional reference image UUIDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
