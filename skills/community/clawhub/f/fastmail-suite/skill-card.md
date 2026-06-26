## Description: <br>
Secure, safe-by-default Fastmail integration (email, contacts, calendar) via JMAP + CalDAV for setup checks, email triage/search, thread inspection, contact lookup, calendar review, and explicitly enabled sending or calendar changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TassieDaddy](https://clawhub.ai/user/TassieDaddy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with their Fastmail mailbox, contacts, and calendars through local CLI scripts. It supports read-first workflows such as setup validation, triage, search, thread summaries, contact lookup, and upcoming-event review, with sending and calendar writes only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses real Fastmail credentials and can expose mailbox, contact, and calendar data to the agent workflow. <br>
Mitigation: Install only when that access is intended, prefer read-only Fastmail tokens for normal use, and keep credentials scoped to the minimum required roles. <br>
Risk: Sending mail or changing calendar events can occur if write mode and suitable credentials are enabled. <br>
Mitigation: Keep FASTMAIL_ENABLE_WRITES unset or 0 for routine use, and enable it only for deliberate sending or calendar changes. <br>
Risk: Raw output and custom service endpoints can weaken the default safety posture. <br>
Mitigation: Avoid --raw unless needed, keep redaction enabled by default, and do not point FASTMAIL_BASE_URL or FASTMAIL_CALDAV_BASE_URL at non-Fastmail hosts. <br>


## Reference(s): <br>
- [Fastmail Suite on ClawHub](https://clawhub.ai/TassieDaddy/fastmail-suite) <br>
- [TassieDaddy publisher profile](https://clawhub.ai/user/TassieDaddy) <br>
- [Fastmail API token settings](https://app.fastmail.com/settings/security/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and optional JSON from bundled Python CLI scripts, with Markdown setup guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redacted by default unless raw output is explicitly requested; writes require FASTMAIL_ENABLE_WRITES=1 and suitable credentials.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
