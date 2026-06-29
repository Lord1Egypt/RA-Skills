## Description: <br>
Conducts a nine-step audit workflow to identify bid-rigging and collusion signals across bidder relationships, pricing, timing, document similarity, qualification checks, and risk grading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rc17777](https://clawhub.ai/user/rc17777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Auditors, compliance teams, and procurement reviewers use this skill to run a structured bidding audit workflow, collect collusion indicators, score risk, and produce an audit findings report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit findings and risk grades may affect procurement or compliance decisions if treated as final conclusions. <br>
Mitigation: Use the generated findings as decision support and require qualified human review against source procurement records before taking action. <br>
Risk: The workflow depends on external pipeline scripts and related audit skills, so results may be incomplete or unavailable if those dependencies are missing or unauthorized. <br>
Mitigation: Run the skill only in an authorized audit environment where required dependencies and data access have been reviewed. <br>
Risk: Security evidence describes the reviewed operational skills as powerful but purpose-aligned and gated by user or admin control. <br>
Mitigation: Install and run the skill only when its disclosed audit workflow is intended, and keep execution under explicit user or administrator authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rc17777/audit-bidding-detection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and structured audit workflow outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bidder profiles, relationship findings, pricing and timing findings, document-similarity findings, qualification findings, a risk assessment, and a bidding audit report when the referenced workflow dependencies are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
