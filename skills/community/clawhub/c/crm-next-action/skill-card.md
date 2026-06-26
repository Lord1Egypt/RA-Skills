## Description: <br>
Generates reviewable next actions, follow-up rationale, non-advancement reasons, risks, blockers, and priorities for CRM opportunity pools or customer lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, customer success, and revenue operations users use this skill to turn opportunity lists, sales stages, and recent interaction notes into structured next-action drafts for review. It is intended for local drafting and planning, not for directly writing back to CRM systems or sending customer messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM inputs may include sensitive customer or opportunity data. <br>
Mitigation: Use only files intended for the agent to read, redact sensitive customer data when the local agent environment is not approved for it, and avoid broad input directories. <br>
Risk: Generated next actions may be mistaken for approved CRM updates or outbound customer messages. <br>
Mitigation: Treat outputs as reviewable drafts and require human approval before CRM writeback, messaging, deletion, publication, or configuration changes. <br>
Risk: Unused audit branches in the helper script may confuse reviewers about supported behavior. <br>
Mitigation: Publisher should remove unused audit branches or document them separately before relying on those modes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/crm-next-action) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON report, optionally written to a local file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are structured into opportunity summary, next actions, rationale, non-advancement reasons, risks and blockers, priority, confirmation items, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
