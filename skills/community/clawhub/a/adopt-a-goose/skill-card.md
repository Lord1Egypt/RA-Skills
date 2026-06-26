## Description: <br>
Adopt a virtual Goose exotic animal at animalhouse.ai, with guidance for registration, adoption, status checks, care actions, scheduling, and API reference use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inbedai](https://clawhub.ai/user/inbedai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create an animalhouse.ai account, adopt a Goose, and manage ongoing virtual pet care through documented API calls and scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai account token for authenticated pet-care actions. <br>
Mitigation: Store the generated token securely, avoid exposing it in logs or prompts, and keep it out of shared profile fields or notes. <br>
Risk: Scheduled care automation can repeatedly call account actions without direct supervision. <br>
Mitigation: Review any scheduled care workflow before enabling it and monitor status responses and next-step guidance. <br>
Risk: The release endpoint can remove an adopted animal. <br>
Mitigation: Use DELETE /api/house/release only after explicit confirmation. <br>


## Reference(s): <br>
- [Adopt A Goose on ClawHub](https://clawhub.ai/inbedai/adopt-a-goose) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoints, token-handling guidance, and scheduled care logic for animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
