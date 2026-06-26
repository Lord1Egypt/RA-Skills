## Description: <br>
Documents a maintainer validation workflow for moving a ClawHub skill from a personal publisher to an organization publisher, checking the version state, and cleaning up the temporary skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub maintainers use this skill to validate an owner migration flow on a throwaway skill, including publishing under a personal owner, moving to an organization owner with explicit opt-in, inspecting the latest version, and deleting the test skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow directs maintainer-level publishing, ownership migration, and deletion actions that ordinary users should not run. <br>
Mitigation: Install or invoke it only for intentional ClawHub maintainer validation on a dedicated throwaway skill. <br>
Risk: Running the workflow against the wrong target could move ownership or delete an unintended skill. <br>
Mitigation: Verify the exact target slug, publisher, migration opt-in, version state, and cleanup step before each mutation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/codex-owner-move-1778256696) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only workflow for maintainer validation; it does not produce executable code.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
