## Description: <br>
Converts a static image URL into a generated video clip using a configured image-to-video API provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to turn static image URLs into short generated video clips for visual media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provided image URL is sent to the configured external API provider. <br>
Mitigation: Use only providers whose privacy, retention, and usage terms are acceptable for the image content. <br>
Risk: A broadly scoped API key could increase impact if the configured provider or runtime is misused. <br>
Mitigation: Prefer a limited-scope API key and rotate it according to the provider's credential-management guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghwyever/05-image-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, JSON] <br>
**Output Format:** [JSON object containing a video_url string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY, API_BASE, and MODEL_NAME environment configuration; sends the provided image URL to the configured external provider.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
