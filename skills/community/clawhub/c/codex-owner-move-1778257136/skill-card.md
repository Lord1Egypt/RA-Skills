## Description: <br>
Documents a maintainer-only workflow for validating that a ClawHub skill can be published, moved to an organization owner, inspected, and cleaned up. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[openclaw](https://clawhub.ai/user/openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub maintainers use this temporary skill to validate owner migration behavior across publishing, migration, inspection, and cleanup steps. It is scoped to disposable validation and should not be installed for normal agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow could be run against the wrong skill or owner during validation. <br>
Mitigation: Use only a disposable validation skill and confirm the slug, owner, version, migration flag, and cleanup target before publishing, migrating, inspecting, or deleting. <br>
Risk: Users could mistake the temporary validation skill for normal installable functionality. <br>
Mitigation: Treat it as maintainer-only validation guidance and do not install it for normal agent use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclaw/codex-owner-move-1778257136) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown procedure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintainer-only validation checklist with no executable code.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
