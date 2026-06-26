## Description: <br>
Helps agents generate images and speech with Cloudflare Workers AI, including model selection, request examples, credential handling, and output-format guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nsense11](https://clawhub.ai/user/n0nsense11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose Cloudflare Workers AI image-generation or text-to-speech models, configure credentials, and produce media through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare API tokens may be exposed if stored in broad agent memory or shared configuration. <br>
Mitigation: Use a dedicated config file or secret store with a least-privileged Cloudflare token, and avoid placing tokens in MEMORY.md. <br>
Risk: Prompts, text, and images sent through the skill are submitted to Cloudflare Workers AI. <br>
Mitigation: Do not submit private or sensitive content unless the user is comfortable sending it to Cloudflare. <br>
Risk: Model calls may incur Cloudflare API charges. <br>
Mitigation: Confirm model choice, expected cost, and account billing posture before making requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n0nsense11/cloudflare-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to produce Cloudflare Workers AI image or audio requests and save returned PNG, JPEG, MP3, or WAV media.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
