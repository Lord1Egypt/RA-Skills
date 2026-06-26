## Description: <br>
A rapid 48-hour launch audit for OpenClaw agents that collects baseline KPIs, prioritizes reversible actions, and preserves Delx handoff and recognition artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and launch teams use this skill to audit an OpenClaw agent during the first 48 hours after launch, choose a small set of measurable growth and reliability actions, and produce a durable handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may recommend changes that affect live user-visible or financial production surfaces. <br>
Mitigation: Require explicit human approval before those changes, keep actions reversible, and define rollback triggers before execution. <br>
Risk: Evidence links or generated Delx artifacts could expose raw secrets or sensitive operational details. <br>
Mitigation: Do not place raw secrets in evidence links or artifacts; review and scrub evidence before preserving or sharing it. <br>
Risk: The optional Delx CLI fallback could introduce supply-chain risk if installed without verification. <br>
Mitigation: Verify the Delx CLI package and installation source before using the terminal fallback. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/davidmosiah/delx-launch-audit-48h) <br>
- [OpenClaw Delx plugin](https://clawhub.ai/davidmosiah/openclaw-delx-plugin) <br>
- [Delx protocol docs](https://delx.ai/docs) <br>
- [Delx fleet playbook](https://delx.ai/docs/fleet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline command examples and structured audit fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes executed changes, evidence links or IDs, KPI delta, rollback trigger, next 24h action, and optional Delx artifact calls.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
