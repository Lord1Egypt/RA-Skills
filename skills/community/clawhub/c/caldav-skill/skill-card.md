## Description: <br>
Manage CalDAV calendars and events, with special support for Radicale server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chakyiu](https://clawhub.ai/user/Chakyiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and calendar operators use this skill to create, update, delete, query, import, and export CalDAV calendars, events, and todos, and to inspect or administer Radicale server configuration, users, status, and storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad CalDAV and Radicale administration can change or delete calendars, events, todos, users, configuration, and storage state. <br>
Mitigation: Run the skill only against systems you control, review the scripts before use, and require explicit confirmation before deletes, imports, exports, or Radicale user/config changes. <br>
Risk: Calendar and server credentials can be exposed if entered on shared command lines or stored loosely. <br>
Mitigation: Avoid command-line credentials such as curl -u user:pass on shared systems and keep credentials in protected environment variables or configuration files. <br>


## Reference(s): <br>
- [Caldav Python Project](https://github.com/python-caldav/caldav) <br>
- [ClawHub Skill Page](https://clawhub.ai/Chakyiu/caldav-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command results, CalDAV examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the caldav Python package; uses local environment variables or config files for CalDAV credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
