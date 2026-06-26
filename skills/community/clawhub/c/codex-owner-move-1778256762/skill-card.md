## Description: <br>
Validates end-to-end skill owner migration by publishing, transferring with an explicit migration flag, verifying the result, and cleaning up a temporary skill. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub maintainers use this temporary guide to validate publishing a skill, moving it from a personal publisher to an organization publisher with an explicit migration flag, inspecting the result, and cleaning up afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow involves publishing, transferring, inspecting, and deleting a registry skill, which can be high-impact outside a controlled test environment. <br>
Mitigation: Run it only as a maintainer test with a throwaway slug, and confirm the account, organization, registry, migration flag, and cleanup target before each step. <br>
Risk: Using the procedure against the wrong skill could affect ownership and release history. <br>
Mitigation: Verify the temporary slug and expected owner before publishing, transferring, inspecting, or deleting anything. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-1778256762) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown procedure text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended for controlled maintainer validation only.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
