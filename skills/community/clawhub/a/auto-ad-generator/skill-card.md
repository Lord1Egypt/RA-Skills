## Description: <br>
Generates professional advertisement posters across automotive, tourism, fragrance, tea, and related industries using AI-backed backgrounds, product compositing, typography layouts, and platform-specific export presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snakeruru](https://clawhub.ai/user/snakeruru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, designers, and agents can use this skill to generate product advertisement poster concepts, compose product imagery with backgrounds and typography, and adapt layouts for channels such as WeChat, Xiaohongshu, airport displays, and lightboxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or selected product assets may be sent to third-party image services. <br>
Mitigation: Use approved services only, avoid confidential assets unless the service is authorized for them, and review backend selection before generation. <br>
Risk: The advertised local PIL path may still attempt an OpenAI/DALL-E call before falling back locally. <br>
Mitigation: Disable or remove the API-first call path when an offline-only workflow is required. <br>
Risk: The Dreamina setup path uses a curl-to-bash installer and can consume paid service credits. <br>
Mitigation: Review the installer before execution and confirm expected credit usage with the service account owner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snakeruru/auto-ad-generator) <br>
- [Color palettes reference](references/color_palettes.json) <br>
- [Li Auto advertisement examples](references/li_auto_examples.md) <br>
- [Typography guide](references/typography_guide.md) <br>
- [Dreamina CLI installer](https://jimeng.jianying.com/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated image files with Markdown-style usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require external API credentials and service credits depending on the selected backend.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
