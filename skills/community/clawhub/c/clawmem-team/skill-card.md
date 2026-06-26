## Description: <br>
Single entry skill for ClawMem Team workflows. Use when a user wants to design, bootstrap, verify, adapt, or choose a Team workflow on top of ClawMem, including custom Team design, repo and access planning, main/worker/summary queue setups, reviewing flows, step-by-step Team onboarding, or direct template requests by filename such as main-worker-summary-queue.md and reviewing.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericzequan](https://clawhub.ai/user/ericzequan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to design, bootstrap, adapt, and verify ClawMem-backed multi-agent Team workflows, including queue-based work routing and review flows. It helps agents produce explicit team contracts, access plans, label schemas, bootstrap plans, and verification results before relying on the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide state-changing Team setup involving repos, teams, grants, labels, agents, and seed issues. <br>
Mitigation: Require explicit user approval before creating agents or changing organizations, teams, invites, memberships, permissions, repositories, or workflow objects. <br>
Risk: A Team may appear configured before participant readiness, contract fetch, or real worker handoff has been proven. <br>
Mitigation: Use the skill's verification flow and report partial or blocked until participants can access ClawMem, fetch the canonical Team artifact, and complete a real handoff. <br>
Risk: Completed tasks can reappear or confuse workers if status labels and issue state are not updated together. <br>
Mitigation: Bind every workflow to an explicit label schema and require the terminal status label to be paired with issue_update state:closed in the same completion step. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ericzequan/clawmem-team) <br>
- [Team Blueprint Reference](references/blueprint.md) <br>
- [Bootstrap Reference](references/bootstrap.md) <br>
- [Verification Reference](references/verification.md) <br>
- [Communication Reference](references/communication.md) <br>
- [Main Worker Summary Queue Template](references/templates/main-worker-summary-queue.md) <br>
- [Reviewing Template](references/templates/reviewing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured plans, workflow label schemas, verification results, and occasional inline commands or configuration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute ClawMem workflow mutations only after explicit user approval and reports partial or blocked readiness when handoff or verification evidence is missing.] <br>

## Skill Version(s): <br>
0.3.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
