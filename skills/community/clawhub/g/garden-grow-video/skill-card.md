## Description: <br>
Generate vertical short videos of gardening and plant growth with WeryAI, including seed germination, blooms, fruiting plants, succulents, mushrooms, and time-lapse growth stories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and agents use this skill to prepare and submit WeryAI text-to-video or image-to-video requests for vertical gardening and plant-growth clips, then return playable video URLs or clear failure guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key and sends generation requests over the network. <br>
Mitigation: Install only from trusted sources, keep WERYAI_API_KEY out of committed files, and run generation in an isolated or short-lived environment when higher assurance is needed. <br>
Risk: Successful generation requests may spend WeryAI credits and send prompts plus any public image URLs to WeryAI. <br>
Mitigation: Review the full expanded prompt, image URLs, model, duration, aspect ratio, and paid-run implications before confirming a request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/garden-grow-video) <br>
- [WeryAI API host](https://api.weryai.com) <br>
- [WeryAI model registry host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON CLI parameters and returned video URLs or error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and public HTTPS image URLs for image-based generation.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
