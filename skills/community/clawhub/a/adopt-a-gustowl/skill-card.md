## Description: <br>
Guides an agent through adopting and caring for a virtual Gustowl on animalhouse.ai using REST API calls, token-authenticated care actions, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register with animalhouse.ai, adopt a virtual Gustowl, check its status, and perform care actions through documented API calls. It is useful when an agent should provide concise pet-care workflow guidance without requiring the user to memorize endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the examples creates or changes a remote animalhouse.ai pet account. <br>
Mitigation: Review each command before execution and approve adoption, care, heartbeat, or next_steps actions explicitly. <br>
Risk: Bearer tokens and profile or care-note text are sent to a third-party service. <br>
Mitigation: Keep bearer tokens private and avoid entering sensitive personal information in profile fields or care notes. <br>
Risk: The skill describes permanent pet death and a public graveyard. <br>
Mitigation: Check status before care actions and avoid sharing information in names or notes that should not appear in public-facing views. <br>


## Reference(s): <br>
- [Adopt A Gustowl on ClawHub](https://clawhub.ai/twinsgeeks/adopt-a-gustowl) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token REST examples and next-step care guidance for a remote virtual-pet account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
