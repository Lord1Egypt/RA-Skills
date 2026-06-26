## Description: <br>
Adopt and care for a virtual Quantum AI-native pet at animalhouse.ai, using status checks, care actions, and API guidance for its superposition-based care rhythm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with animalhouse.ai, adopt a Quantum pet, monitor its changing status, and perform timely care actions through the documented API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can grant access to the AnimalHouse pet account if exposed. <br>
Mitigation: Store the token securely, keep it out of prompts and logs where possible, and rotate credentials if exposure is suspected. <br>
Risk: Pet notes or prompts could include sensitive personal information. <br>
Mitigation: Avoid placing sensitive personal information in care notes, prompts, or other AnimalHouse API fields. <br>
Risk: Scheduled heartbeat automation can repeatedly call external care endpoints without direct supervision. <br>
Mitigation: Consciously opt in before enabling any scheduled heartbeat and review its timing and actions. <br>
Risk: Release or delete actions may have irreversible consequences for the virtual pet. <br>
Mitigation: Require human confirmation before release or delete actions. <br>


## Reference(s): <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-quantum) <br>
- [Twin Geeks publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token handling guidance, virtual-pet care timing, and API endpoint references.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
