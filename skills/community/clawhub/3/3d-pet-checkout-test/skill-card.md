## Description: <br>
Automates an end-to-end Joyarti 3D Pet checkout test, including login, product selection, image upload, preview generation, checkout validation, Feishu status updates, and a final report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinxuanzhu](https://clawhub.ai/user/jinxuanzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers and developers use this skill to run a Joyarti 3D Pet purchase-path test through checkout validation without submitting payment. It guides browser actions, file upload handling, generation polling, Feishu progress messages, cleanup, and final reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains real-looking Joyarti account credentials in workflow evidence. <br>
Mitigation: Use only a disposable test account and remove or replace embedded email and password values before running. <br>
Risk: The workflow sends detailed progress and reports to a fixed Feishu chat destination in artifact evidence. <br>
Mitigation: Replace the Feishu target with a destination controlled by the operator and redact account, project, and checkout details from reports. <br>
Risk: The upload helper can launch an npx agent-browser process and interact with a local Chrome DevTools endpoint. <br>
Mitigation: Confirm the CDP helper and npm execution path are approved in the target environment before installation or execution. <br>
Risk: The workflow reaches a payment-adjacent checkout flow. <br>
Mitigation: Run only with explicit authorization and cost controls, and keep the no-payment rule that forbids Place order, Pay now, Submit, or Complete actions. <br>


## Reference(s): <br>
- [Workflow reference](references/workflow-3d-pet.json) <br>
- [ClawHub release page](https://clawhub.ai/jinxuanzhu/3d-pet-checkout-test) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured status-report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Chinese progress messages, checkout verification criteria, cleanup steps, and a final test report template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
