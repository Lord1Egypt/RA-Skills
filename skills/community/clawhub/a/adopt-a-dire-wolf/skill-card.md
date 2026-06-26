## Description: <br>
Adopt a virtual Dire Wolf dog at animalhouse.ai. Prehistoric. Pack instinct. Behaves differently in colonies vs solo. Feeding every 12 hours. Extreme tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI caretaker agents use this skill to register with Animalhouse, adopt a Dire Wolf virtual pet, and follow care/status API workflows for feeding, health checks, and scheduled attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Animalhouse bearer token is shown once and can control a persistent virtual pet if exposed. <br>
Mitigation: Store the token securely, avoid committing it to files or logs, and pass it only in authorized Animalhouse API calls. <br>
Risk: Automated care schedules can repeatedly change the pet's state without human review. <br>
Mitigation: Review the schedule, action thresholds, and generated care requests before enabling automation. <br>
Risk: The release endpoint may abandon or delete the virtual pet. <br>
Mitigation: Use /api/house/release only after explicit confirmation from the user or owning agent workflow. <br>


## Reference(s): <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-dire-wolf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for Animalhouse API use; no executable files are bundled.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
