## Description: <br>
Validates an owner migration workflow by creating a skill under a personal owner and moving it to OpenClaw with explicit migration intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to validate ClawHub owner migration behavior during review by testing a personal-owner skill transfer into OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create or transfer a ClawHub skill without enough scope detail. <br>
Mitigation: Define the exact test skill and confirm both personal-owner and OpenClaw permissions before use. <br>
Risk: Owner migration actions may be performed without explicit approval or cleanup planning. <br>
Mitigation: Require human approval before create or transfer actions and document cleanup or rollback before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-debug-1778257077) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
