## Description: <br>
AI portrait image generation with 140+ nationalities, diverse styles, professional headshots, character design, and fashion visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luruibu](https://clawhub.ai/user/luruibu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents in generating professional portraits, character images, avatars, fashion visuals, and headshots through the DiversityFaces portrait API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided API key for an external portrait-generation API. <br>
Mitigation: Configure BEAUTY_API_KEY deliberately, keep it private, and avoid exposing it in prompts, logs, scripts, or shared files. <br>
Risk: Prompts are sent to gen1.diversityfaces.org for processing. <br>
Mitigation: Do not send sensitive personal data or images unless the user trusts the provider's handling of those requests. <br>
Risk: The skill can be used to request human portrait generation that may cross safety boundaries. <br>
Mitigation: Follow the artifact's refusal guidance for minors, nudity, sexual content, violence, hate, illegal activity, harmful behavior, undisclosed deepfakes, and personal identifying information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luruibu/beauty-generation-api) <br>
- [DiversityFaces API homepage](https://gen1.diversityfaces.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline curl and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers API key setup, quota checks, request polling, image download, and content-safety refusal boundaries.] <br>

## Skill Version(s): <br>
1.2.50 (source: evidence.json release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
