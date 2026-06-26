## Description: <br>
Professional assistant for 3D printing, laser engraving, and 3D modeling workflows, including visual references for sculpting, Meshy AI 3D model generation, and FDM or resin print-setting optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaulustus](https://clawhub.ai/user/Jaulustus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, artists, and fabrication teams use this skill to plan 3D printing, laser engraving, sculpting-reference, and Meshy.ai model-generation workflows. It helps connect AI-generated references to practical modeling, slicing, and manufacturing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image URLs are sent to Meshy.ai using the user's API key. <br>
Mitigation: Install only when Meshy.ai use is intended, and avoid submitting prompts or image URLs that should not be shared with that external service. <br>
Risk: The set-key helper saves MESHY_API_KEY in a local plaintext .env file. <br>
Mitigation: Prefer setting MESHY_API_KEY in the environment; if .env is used, keep it private, do not commit it, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [3D Maker Companion on ClawHub](https://clawhub.ai/Jaulustus/3d-maker-companion) <br>
- [Meshy OpenAPI v1 endpoint](https://api.meshy.ai/openapi/v1) <br>
- [Meshy OpenAPI v2 endpoint](https://api.meshy.ai/openapi/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON API responses from the Meshy client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MESHY_API_KEY for Meshy.ai API calls; the set-key helper can write the key to a local .env file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
