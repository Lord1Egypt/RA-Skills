## Description: <br>
Adopt a virtual Calico cat at animalhouse.ai. Three personalities in one cat. Mood shifts unpredictably. Feeding every 6 hours. Common tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with animalhouse.ai, adopt a virtual Calico cat, and manage care through documented API calls and optional scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens for animalhouse.ai can grant access to the adopted pet account if exposed. <br>
Mitigation: Store the token securely, avoid logging it, and inject it through the agent's secret-management mechanism rather than hard-coding it. <br>
Risk: Automated care routines may send unwanted care actions or trigger sensitive endpoints such as DELETE /api/house/release. <br>
Mitigation: Review scheduled actions before enabling automation and require explicit confirmation before any release or deletion request. <br>
Risk: Care notes and account details are sent to the external animalhouse.ai service. <br>
Mitigation: Use the skill only when the user is comfortable creating or using an animalhouse.ai account and sharing the submitted care data with that service. <br>


## Reference(s): <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/adopt-a-calico) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Animalhouse API request examples and care-heartbeat guidance; requires user-managed bearer token for live API calls.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
