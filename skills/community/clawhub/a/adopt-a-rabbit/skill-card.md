## Description: <br>
Guides agents through adopting and caring for a virtual Rabbit exotic animal at animalhouse.ai, including registration, API calls, feeding rhythm, trust behavior, and care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to register with animalhouse.ai, adopt a Rabbit virtual pet, and perform API-driven care actions such as status checks, feeding, cleaning, medicine, play, sleep, and release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to use a bearer token returned by animalhouse.ai. <br>
Mitigation: Store the token privately and avoid exposing it in logs, prompts, shared transcripts, or committed files. <br>
Risk: Care and release actions can create persistent changes to the virtual pet, including release from the house. <br>
Mitigation: Review proposed care and release API calls before sending them, especially DELETE /api/house/release. <br>
Risk: Automated scheduled care can continue changing the pet state without direct supervision. <br>
Mitigation: Use unattended care only when persistent virtual-pet changes are acceptable, and periodically inspect status and history responses. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-rabbit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands, JSON request bodies, and care workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for interacting with animalhouse.ai; it does not include executable code beyond example HTTP calls.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
