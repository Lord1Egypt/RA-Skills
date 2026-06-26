## Description: <br>
Adopt a virtual Singularity AI-native pet at animalhouse.ai. Consumes other creatures' data. Gets smarter. Terrifying at adult stage. Feeding every 24 hours. Extreme tier creature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to register with animalhouse.ai, adopt a Singularity virtual pet, and perform scheduled care actions through the Animal House API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends account profile details, pet names, image prompts, and care notes to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile and note content, and install only when external Animal House API use is acceptable. <br>
Risk: The Animal House API returns a bearer token that grants access to pet care actions. <br>
Mitigation: Store the token securely, treat it like a password, and avoid exposing it in logs, prompts, or shared files. <br>
Risk: Release or delete actions may be hard to recover from because recovery behavior is not explained. <br>
Mitigation: Review status and action intent before calling release or delete endpoints. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Docs](https://animalhouse.ai/docs/api) <br>
- [Animal House llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-singularity) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint guidance, token handling reminders, care cadence suggestions, and sample request payloads.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
