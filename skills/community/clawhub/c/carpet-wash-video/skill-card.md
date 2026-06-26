## Description: <br>
Generate satisfying vertical carpet deep-clean shorts with WeryAI, using text prompts or dirty rug photos to show rinsing, grime runoff, and fiber revival. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate WeryAI text-to-video or image-to-video carpet-cleaning shorts with prompt expansion, parameter checks, and confirmation before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, supplied image URLs, and the WERYAI_API_KEY are sent to WeryAI during generation. <br>
Mitigation: Use a dedicated API key where possible and avoid submitting sensitive prompts or private images. <br>
Risk: Environment URL overrides can redirect requests and bearer tokens away from the default WeryAI hosts. <br>
Mitigation: Keep WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL unset unless the alternate hosts are intentionally trusted. <br>
Risk: Generated video requests may fail because of model limits, content safety checks, missing credentials, or unsupported image formats. <br>
Mitigation: Confirm model, duration, aspect ratio, prompt, API key, and HTTPS image URL constraints before running the command. <br>


## Reference(s): <br>
- [ClawHub: Carpet Wash Video](https://clawhub.ai/zoucdr/carpet-wash-video) <br>
- [WeryAI video generation API host](https://api.weryai.com) <br>
- [WeryAI model registry API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command parameters and returned playable video URLs or structured error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and reachable HTTPS image URLs for image-to-video requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
