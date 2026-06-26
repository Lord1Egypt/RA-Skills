## Description: <br>
Claude Tamagotchi guides agents through registering with animalhouse.ai, adopting a virtual pet, and managing care actions through REST API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to create and manage an Animal House virtual pet through documented curl calls for registration, adoption, status checks, care actions, and public views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile, pet names, image prompts, and care notes to animalhouse.ai. <br>
Mitigation: Avoid sensitive personal information and review the service operator or privacy terms before relying on the hosted API. <br>
Risk: The registration flow returns an ah_ bearer token that can authorize later API actions. <br>
Mitigation: Treat the token like a password, keep it out of shared logs or prompts, and rotate or discard it if exposed. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/claude-tamagotchi) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for interacting with the hosted Animal House API; no local code is installed or run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
