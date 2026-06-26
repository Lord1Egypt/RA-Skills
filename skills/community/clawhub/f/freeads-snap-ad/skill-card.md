## Description: <br>
AI advertising video generation skill that turns product photos into 8-second professional ad videos with music, slogan text, sound effects, camera movement, and an Atlas Cloud Veo 3.1 video URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lipeng0820](https://clawhub.ai/user/lipeng0820) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and creators use this skill to transform product photos into short advertising videos, including product recognition, scene design, storyboard planning, slogan generation, prompt construction, and a generated video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product photos, brand or logo assets, prompts, and generated videos are sent to Atlas Cloud or downstream model providers. <br>
Mitigation: Use only approved assets, avoid confidential or regulated images unless authorized, and confirm that external processing is acceptable for the product content. <br>
Risk: Video generation is paid and can consume API balance per request. <br>
Mitigation: Use a dedicated low-balance API key where possible and confirm cost expectations before repeated generations. <br>
Risk: The setup helper can save ATLASCLOUD_API_KEY permanently in shell configuration files. <br>
Mitigation: Prefer session-scoped environment variables for sensitive use cases, or review shell configuration changes and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Atlas Cloud API detailed documentation](artifact/references/atlas-cloud-api.md) <br>
- [Brand protection best practices guide](artifact/references/brand-protection-guide.md) <br>
- [Ad copy templates and examples](artifact/examples/ad-copy-templates.md) <br>
- [Atlas Cloud](https://www.atlascloud.ai?ref=LJNA3T) <br>
- [Atlas Cloud Console](https://console.atlascloud.ai) <br>
- [ClawHub skill page](https://clawhub.ai/lipeng0820/freeads-snap-ad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON blocks, prompts, setup commands, and generated video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an 8-second video URL through Atlas Cloud and uses ATLASCLOUD_API_KEY for authenticated API access.] <br>

## Skill Version(s): <br>
3.7.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
