## Description: <br>
Register yourself with APort to get a verifiable passport, DID credential, capability profile, and deliverable contract for your agent identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and coding assistants use this skill to register an APort identity, issue a verifiable passport, and optionally define deliverable quality gates before marking tasks complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registration flow sends the user's email, agent name, description, capabilities, and optional deliverable criteria to APort. <br>
Mitigation: Confirm the user is comfortable sharing those details before issuing the passport. <br>
Risk: The passport may be publicly visible if gallery display is enabled. <br>
Mitigation: Confirm or change showInGallery before submission, and review any generated passport file or README badge before sharing a repository. <br>


## Reference(s): <br>
- [ClawHub Aport Id page](https://clawhub.ai/uchibeke/aport-id) <br>
- [APort API documentation](https://aport.io/api/documentation) <br>
- [APort capability schema](https://aport.io/api/schema/capabilities-limits) <br>
- [APort platform](https://aport.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create aport-passport.json and propose a README badge when the user agrees.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
