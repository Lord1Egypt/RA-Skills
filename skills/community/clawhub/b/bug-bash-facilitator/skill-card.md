## Description: <br>
Plan, run, and debrief structured pre-release bug bash sessions with scoped surfaces, participant mix, exploratory test charters, severity triage, de-duplication, fix prioritization, and retrospective artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Release managers, QA leads, engineering managers, product teams, and cross-functional SaaS release teams use this skill to plan and facilitate pre-release exploratory testing. It produces structured bug bash artifacts for scope definition, participant coordination, charters, intake, triage, prioritization, waiver handling, and retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug bash charters for billing, checkout, or account-management flows may involve money, account access, or user data if testers run them against production systems. <br>
Mitigation: Run those charters in staging with seeded test accounts and sandbox payment systems. <br>
Risk: The release metadata lists crypto and can-make-purchases capability tags even though the security summary describes the artifact as instruction-only. <br>
Mitigation: Review the capability tag mismatch before deployment if the host platform treats tags as permissions or install-time privileges. <br>
Risk: Generated triage and fix-prioritization guidance could be mistaken for final release authority. <br>
Mitigation: Require release owners to review severity calls, ship-with decisions, and waivers before acting on the generated plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/bug-bash-facilitator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured text templates for release planning and triage workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces paste-ready planning artifacts such as scope docs, charter boards, intake forms, severity rubrics, ranked bug lists, waiver notes, and retrospectives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
