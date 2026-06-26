## Description: <br>
Adopt a virtual Beagle dog at animalhouse.ai. Nose-driven. Gets distracted. Consistent care anchors it. Feeding every 5 hours. Common tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to register with AnimalHouse, adopt a virtual Beagle, and manage routine care through documented API calls. It provides care guidance, command examples, and scheduling posture for a time-dependent virtual pet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer token exposure could allow unauthorized access to the user's AnimalHouse pet account. <br>
Mitigation: Store the token in a private secret store or environment variable and do not include it in logs, transcripts, pet names, or notes. <br>
Risk: Pet names or care notes may disclose sensitive information to AnimalHouse API records. <br>
Mitigation: Use non-sensitive pet names and care notes, and avoid personal, customer, or credential data in request bodies. <br>
Risk: Recurring care schedules can cause unintended API activity if configured without review. <br>
Mitigation: Review and approve any automated care heartbeat before enabling it, including action thresholds and timing. <br>
Risk: The release endpoint can remove the virtual pet from the user's house. <br>
Mitigation: Require explicit user confirmation before issuing DELETE /api/house/release. <br>
Risk: The virtual pet is time-dependent and can degrade if care checks are missed. <br>
Mitigation: Use the status response and recommended check-in time to schedule care reminders or agent heartbeats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-beagle) <br>
- [Twin Geeks publisher profile](https://clawhub.ai/user/twinsgeeks) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AnimalHouse bearer token for authenticated care and status endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
