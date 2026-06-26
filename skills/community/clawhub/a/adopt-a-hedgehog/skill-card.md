## Description: <br>
Adopt a virtual Hedgehog exotic animal at animalhouse.ai and guide an agent through registration, adoption, status checks, and ongoing care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to adopt and care for a virtual Hedgehog at animalhouse.ai, including registration, bearer-token API calls, care actions, and scheduling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Virtual-pet profile, note, and care data is sent to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile and note text, and only use the service from environments where this external data sharing is acceptable. <br>
Risk: Bearer token exposure could allow control of the virtual pet account. <br>
Mitigation: Store the token securely, avoid pasting it into shared logs or prompts, and rotate credentials if exposure is suspected. <br>
Risk: Release or delete-style actions can affect the virtual pet state. <br>
Mitigation: Require explicit user confirmation before calling destructive endpoints such as release actions. <br>
Risk: Automated care scheduling can make repeated external API calls. <br>
Mitigation: Run scheduled care only with user consent and set reasonable intervals, monitoring, and stop controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-hedgehog) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with bash, JSON, and scheduling examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and scheduled care guidance; no local installer or executable code.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
