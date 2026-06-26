## Description: <br>
AI video generation - Sora, Kling, Veo 3, Seedance, Hailuo, WAN, Grok; text-to-video, image-to-video, video editing, 37 models, and one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, developers, and agents use this skill to create AI videos from text, image references, and video-editing intents through EvoLink's API and MCP tools. It helps choose models, gather parameters, upload references, poll generation tasks, and return expiring result URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EvoLink API key and sends prompts, images, videos, and referenced URLs to EvoLink services. <br>
Mitigation: Use only approved media and prompts, avoid sensitive or regulated content, and treat EVOLINK_API_KEY as confidential. <br>
Risk: Uploaded files and generated result URLs are hosted externally and remain available for a limited time. <br>
Mitigation: Delete hosted files when no longer needed and save generated results before their URLs expire. <br>
Risk: Video generation can consume account credits and may rely on an MCP package installed with an @latest command. <br>
Mitigation: Estimate or monitor credit usage, and consider reviewing or pinning the MCP package before setup. <br>


## Reference(s): <br>
- [Evolink Video API Parameter Reference](references/video-api-params.md) <br>
- [Evolink File Hosting API](references/file-api.md) <br>
- [Evolink Homepage](https://evolink.ai) <br>
- [Evolink Video Skill Page](https://clawhub.ai/EvoLinkAI/evolink-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API calls, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline commands, API parameters, task IDs, and result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include expiring hosted file URLs and generated video result URLs.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
