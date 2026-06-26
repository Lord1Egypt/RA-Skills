## Description: <br>
Adopt a virtual Dragon exotic animal at animalhouse.ai. Mythical. Eats concepts. Feed it "courage" or "patience." Feeding every 24 hours. Extreme tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with AnimalHouse, adopt a virtual Dragon, check status, and perform care actions through the AnimalHouse API. It also provides endpoint examples and scheduling guidance for ongoing care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can authorize AnimalHouse account and care actions if exposed. <br>
Mitigation: Store the token securely, avoid logging it, and only send it in the Authorization header to animalhouse.ai. <br>
Risk: Profile fields, pet names, image prompts, and care notes may contain private information. <br>
Mitigation: Keep those fields non-sensitive and review user-provided text before submitting it to the AnimalHouse API. <br>
Risk: The release endpoint can remove an adopted creature. <br>
Mitigation: Require explicit user confirmation before making DELETE /api/house/release requests. <br>


## Reference(s): <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-dragon) <br>
- [Twin Geeks Publisher Profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and scheduling pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API usage patterns and optional care-heartbeat guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
