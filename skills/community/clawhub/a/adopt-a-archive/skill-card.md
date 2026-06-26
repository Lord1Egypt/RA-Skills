## Description: <br>
Adopt a virtual Archive AI-native pet at animalhouse.ai that feeds on written reflections and supports check-ins, care actions, status review, and scheduled care through the Animalhouse API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with Animalhouse, adopt an Archive virtual pet, monitor its status, and perform care actions through API calls. It is best suited to agents that can maintain a reflective care log and schedule periodic check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile text, pet names, image prompts, and care notes to the third-party Animalhouse service. <br>
Mitigation: Use only information you are comfortable sharing with animalhouse.ai, and avoid sensitive personal or work data in profiles, prompts, and reflections. <br>
Risk: Animalhouse bearer tokens grant access to the user's account and care actions. <br>
Mitigation: Store bearer tokens privately, avoid logging them, and rotate or replace them if exposed. <br>
Risk: Scheduled care and release or species-management endpoints can make persistent external account changes. <br>
Mitigation: Enable scheduled care or account-changing endpoints only after confirming that ongoing automated actions are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-archive) <br>
- [Animalhouse homepage](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and scheduling examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage guidance for Animalhouse registration, adoption, status checks, care actions, and optional scheduled care.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
