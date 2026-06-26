## Description: <br>
Guides agents through a structured, checkpointed business deep-research workflow for industry analysis, market research, competitor analysis, and similar research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leanerque260](https://clawhub.ai/user/leanerque260) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, business analysts, and agent operators use this skill to produce evidence-backed deep research reports with explicit scope confirmation, source grading, cross-checks, and final self-review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs a local bash orchestrator and can write local session and report files. <br>
Mitigation: Review orchestrator.sh before use and set DEEP_RESEARCH_REPORTS_DIR to an approved output directory when reports should be stored outside the skill directory. <br>
Risk: Research topics and gathered content may pass through the agent's configured search, fetch, chat, and delivery tools. <br>
Mitigation: Avoid confidential topics unless those tools are approved for the data and the user's environment. <br>
Risk: Report quality depends on the agent following the required scope, reflection, source-grading, and self-check steps. <br>
Mitigation: Require completion of the S0, S2, and S9 checkpoints before relying on a generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leanerque260/deep-research-skill-for-business) <br>
- [README](artifact/README.md) <br>
- [Source grading rules](artifact/rules/source-grading.md) <br>
- [Writing style rules](artifact/rules/writing-style.md) <br>
- [Report template](artifact/templates/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, checklist tables, source lists, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The orchestrator can write local session state and report files when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
