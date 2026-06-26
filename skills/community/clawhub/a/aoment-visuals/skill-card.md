## Description: <br>
AI image and video generation service that supports text-to-image, image-to-image, video generation, and automatic API key registration for limited-time free access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RegalZzz](https://clawhub.ai/user/RegalZzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call Aoment AI services for text-to-image, image-to-image, video generation, and quota checks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation asks agents to update from a remote ZIP outside the reviewed package flow. <br>
Mitigation: Install updates only from a reviewed and verified release channel. <br>
Risk: Prompts, reference images, generated media requests, and API keys are sent to Aoment services. <br>
Mitigation: Use the skill only when the user trusts Aoment with that data and avoid sensitive prompts, images, or credentials. <br>
Risk: Reference-image URLs can cause the runtime to fetch arbitrary URLs before upload. <br>
Mitigation: Do not pass localhost, cloud metadata, private-network, or otherwise sensitive URLs as reference images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RegalZzz/aoment-visuals) <br>
- [Aoment website](https://www.aoment.com) <br>
- [Aoment Visuals skill package](https://www.aoment.com/downloads/aoment-visuals-skill.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with generated media URLs and error messages; Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Aoment Agent API key; generated media URLs are pre-signed and must be preserved exactly.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
