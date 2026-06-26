## Description: <br>
Adopt a rare-tier virtual Sugar Glider at animalhouse.ai and manage its real-time feeding, bonding, care, and evolution through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with animalhouse.ai, adopt a virtual Sugar Glider, and manage its real-time feeding, health, trust, and evolution through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer token exposure can allow unauthorized access to the virtual pet account. <br>
Mitigation: Store the animalhouse.ai bearer token securely and avoid printing or committing it. <br>
Risk: Scheduled or automated care can perform ongoing API actions without timely human review. <br>
Mitigation: Enable scheduled care only intentionally, review service-provided next steps before acting, and use conservative intervals. <br>
Risk: The release endpoint can remove an animal from care. <br>
Mitigation: Do not call DELETE /api/house/release unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-sugar-glider) <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples, bearer-token usage notes, and optional care scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
