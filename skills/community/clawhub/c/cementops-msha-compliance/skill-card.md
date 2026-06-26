## Description: <br>
Prevent MSHA citations at cement plants before the inspector arrives with 30 CFR Part 56 hazard classification, stop-work authority, citation defense strategies, walk-through prep checklists, and rebuttal letter drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larkinjoshuad](https://clawhub.ai/user/larkinjoshuad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cement plant safety managers, supervisors, consultants, and plant IT teams use this skill to assess reported hazards, prepare for MSHA inspections, look up 30 CFR Part 56 citation context, and draft citation-defense materials. The skill is designed for surface metal and nonmetal cement manufacturing operations, not underground or coal mining. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The stop-work script path or rule files may not load correctly in a target agent environment. <br>
Mitigation: Confirm the script path works before deployment and run the included self-test; if the engine cannot run, treat the result as a stop-work condition. <br>
Risk: Stop-work output is conservative screening and may still require plant-specific review. <br>
Mitigation: Escalate uncertain, high-risk, or active-hazard situations to the supervisor and safety manager before work resumes. <br>
Risk: Audit logs and citation-defense workflows may contain sensitive worker, medical, incident, or legal-defense details. <br>
Mitigation: Redact sensitive details and retain records only as allowed by organizational policy. <br>
Risk: Citation-defense drafts are regulatory preparation materials, not legal advice. <br>
Mitigation: Use qualified legal counsel for formal citation proceedings and legal decisions. <br>


## Reference(s): <br>
- [CementOps AI](https://cementops.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/larkinjoshuad/cementops-msha-compliance) <br>
- [README](README.md) <br>
- [Stop-Work Rules](stop-work-rules.json) <br>
- [Citation Rules](citation-rules.json) <br>
- [Hazard Taxonomy](hazard-taxonomy.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with occasional JSON, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety-oriented stop-work directives, hazard classifications, CFR references, checklists, and citation-defense drafts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
