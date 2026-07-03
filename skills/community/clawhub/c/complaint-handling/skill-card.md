## Description: <br>
Complaint Handling helps agents classify, track, remind, close, and report on customer complaints using a defined complaint-management workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Property service and customer operations staff use this skill to record complaints, classify severity and category, monitor response deadlines, generate reminders and reports, and manage customer follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complaint records may include identifiable customer data and complaint details. <br>
Mitigation: Use only in an authorized business environment, apply retention and redaction controls, and restrict access to complaint records and generated reports. <br>
Risk: The artifact reads and writes local Excel files, backups, and report files. <br>
Mitigation: Configure storage paths deliberately and limit filesystem permissions to the intended complaint-management data locations. <br>
Risk: Optional WeCom forwarding can disclose real customer data to broad chat groups. <br>
Mitigation: Enable WeCom forwarding only after approval, route messages to limited groups, and avoid sending sensitive complaint details unless they are necessary and authorized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/perrykono-debug/complaint-handling) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown guidance, Python command outputs, and JSON complaint reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Excel complaint records and can optionally forward text or Markdown notifications through WeCom webhooks when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
