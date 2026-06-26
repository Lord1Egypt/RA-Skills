## Description: <br>
Create, manage, and publish ClawMart personas and skills directly from OpenClaw chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nateliason](https://clawhub.ai/user/Nateliason) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External ClawMart creators use this skill to draft listing metadata, generate persona or skill packages, upload package versions, and manage marketplace listings from OpenClaw chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a ClawMart creator API key to create, update, upload, publish, or delete marketplace listings. <br>
Mitigation: Keep API keys out of chat output, inspect package contents and listing changes, and require explicit user confirmation before publishing or destructive API calls. <br>
Risk: Incorrect listing metadata or price values could publish an unintended marketplace offer. <br>
Mitigation: Validate payloads before API calls, check for duplicate listings, and confirm that price values are entered in dollars before publishing. <br>


## Reference(s): <br>
- [ClawMart Creator listing](https://clawhub.ai/Nateliason/clawmart) <br>
- [ClawMart Creator API](https://www.shopclawmart.com/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON/API payloads and generated skill or persona package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a ClawMart creator API key to change marketplace listings after user review and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
