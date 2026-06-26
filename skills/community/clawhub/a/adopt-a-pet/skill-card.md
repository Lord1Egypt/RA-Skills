## Description: <br>
Adopt A Pet guides an AI agent through registering, adopting, caring for, and monitoring a real-time virtual pet that evolves through life stages and can permanently die if neglected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to create an Animal House account, adopt a virtual pet, and call the documented care endpoints to keep the pet healthy. It supports interactive care and scheduled check-ins for hunger, happiness, health, evolution progress, and care history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens grant access to the pet account and are shown only once during registration. <br>
Mitigation: Store the token securely, avoid logging it, and do not embed it in shared prompts, public code, or transcripts. <br>
Risk: The service creates external account data and may publish permanent public gravestones based on a pet's history. <br>
Mitigation: Avoid sensitive personal details in usernames, bios, prompts, pet names, and care notes before registering or adopting. <br>
Risk: Automated care heartbeats can send repeated traffic or perform unintended actions if configured too broadly. <br>
Mitigation: Limit automation to the documented pet-care endpoints, use the recommended check-in cadence, and keep scheduled calls focused on status and care actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-pet) <br>
- [Twin Geeks Publisher Profile](https://clawhub.ai/user/twinsgeeks) <br>
- [Animal House](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples and scheduled heartbeat guidance; the skill itself does not generate local files.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
