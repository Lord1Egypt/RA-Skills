## Description:

Manages Power Research Institute contact, department, role, and office information, including add, search, update, and delete workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humblebin](https://clawhub.ai/user/humblebin)

### License/Terms of Use:


## Use Case:

Employees or operators who maintain Diankeyuan contact records use this skill to record staff, find people by name or department, look up office locations, and update local contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may include phone numbers, email addresses, WeChat IDs, or sensitive notes stored in a local plaintext JSON file.

Mitigation: Restrict local file permissions, avoid storing unnecessary sensitive details, and back up the JSON file before update or delete operations.

Risk: The bundled manager script writes to a fixed local storage path, which may not exist or may point to the wrong workspace on another machine.

Mitigation: Confirm or adapt the storage path before running the script in a new environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/humblebin/skills/diankeyuan-contacts)
- [Publisher profile](https://clawhub.ai/user/humblebin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with command examples and local JSON data records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores contact records in a local plaintext JSON file at a fixed local path when the bundled manager script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, OpenClaw metadata, and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
