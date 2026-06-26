## Description: <br>
AI 衣橱搭配 generates outfit recommendation images from date, city, province, and style preferences by calling the AI Closet API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houdamiao](https://clawhub.ai/user/houdamiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistants use this skill to request outfit recommendations for a given date, city, province, and style. The skill returns terminal text and a generated outfit overview image from the AI Closet service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a dedicated API key and outfit context such as city, date, and style to the AI Closet endpoint. <br>
Mitigation: Install only if the AI Closet endpoint is trusted, use a dedicated API key, and avoid submitting sensitive outfit context. <br>
Risk: The skill runs a local Python script that invokes ImageMagick, writes generated images to a temp folder, and may auto-open the result on desktop systems. <br>
Mitigation: Review and scan the skill before deployment, confirm ImageMagick is installed from a trusted source, and account for local preview and temp-file behavior. <br>
Risk: Supported chat channels may upload the generated outfit image when processing the MEDIA output line. <br>
Mitigation: Use the skill only in channels where sharing generated outfit images is acceptable, and preserve the MEDIA line so the intended delivery pipeline can handle it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houdamiao/aicloset-outfit) <br>
- [AI Closet API base URL](https://aicloset-dev-h5.wxbjq.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, image files] <br>
**Output Format:** [Terminal text with a MEDIA file path for a generated PNG overview image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICLOSET_API_KEY and ImageMagick; sends date, city, province, and style to the AI Closet endpoint.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
