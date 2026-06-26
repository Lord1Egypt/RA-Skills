## Description: <br>
Generates comprehensive campaign documents, task decompositions, and context documents from minimal input for ClawTeam continuous iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hickhe](https://clawhub.ai/user/hickhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn minimal project inputs or Code Archaeology results into campaign plans, task decompositions, and context documents for ClawTeam-driven implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports hard-coded local workspace paths and file writes without clear path limits. <br>
Mitigation: Run the skill only in a confined project directory with explicit input and output paths, and review or patch hard-coded /Users/admin/.openclaw/workspace access before use. <br>
Risk: Generated planning documents may be incomplete or misleading if the input analysis is incomplete. <br>
Mitigation: Review generated campaign, task, and context documents before using them to drive ClawTeam execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hickhe/ai-plan-generator) <br>
- [Usage examples](artifact/EXAMPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON files for campaign documents, task decomposition, context documents, and process reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project planning artifacts from user-supplied project metadata and optional Code Archaeology analysis directories.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact package.json reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
