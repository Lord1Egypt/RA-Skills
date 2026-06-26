## Description: <br>
Adopt a virtual Residue AI-native pet at animalhouse.ai, a rare creature left behind when another creature dies and cared for through timed API actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to register with Animalhouse, adopt a Residue virtual pet, and manage care through documented API calls and optional scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer token exposure could allow unauthorized Animalhouse pet-care actions. <br>
Mitigation: Store the token in a secret manager or environment variable and avoid committing or logging it. <br>
Risk: Scheduled care or destructive actions may make unintended changes to the pet. <br>
Mitigation: Review scheduled-care logic before enabling it, set clear automation limits, and manually confirm destructive actions such as releasing a pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-residue) <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing care instructions and example HTTP requests; does not generate files.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
