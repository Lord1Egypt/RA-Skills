## Description: <br>
Automated customer follow-up scheduling and execution engine for B2B sales that generates personalized follow-up email drafts from customer stage, last contact date, and follow-up strategy, and can sync follow-up records with a configurable CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and CRM operations teams use this skill to schedule outbound B2B follow-ups, generate reviewable email drafts for dormant or stage-based leads, and sync follow-up activity into OKKI CRM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM follow-up records may be created repeatedly or without enough containment when sync or cron modes are enabled. <br>
Mitigation: Start in dry-run mode, verify the OKKI CLI path and account permissions, and enable cron only after review and rollback procedures are defined. <br>
Risk: Generated drafts and logs may contain customer data. <br>
Mitigation: Protect draft and log locations, restrict access to users who need the customer data, and review retention before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cjboy007/follow-up-engine) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON draft records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local draft and log files and may create CRM follow-up records when sync mode is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
