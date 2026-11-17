## Description:

Create scheduled Google Calendar events with OPEN access Google Meet spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kumadun](https://clawhub.ai/user/kumadun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to schedule Google Calendar events, create Google Meet conference links, and configure the Meet space access level from a local command line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Google OAuth tokens in meeting_token.pickle, which may expose account access if the file is shared, committed, or readable by other users.

Mitigation: Use the skill only in a trusted local workspace, keep token files out of version control, prefer owner-only permissions or keychain storage, and revoke the OAuth token if exposure is suspected.

Risk: The requested Google Calendar scope is broader than the script appears to need.

Mitigation: Review scopes before authorization and prefer a patched version that removes unnecessary broad Calendar access.

Risk: OPEN Meet access allows broad link-based meeting access.

Mitigation: Use TRUSTED or RESTRICTED access for private meetings and reserve OPEN access for meetings intended to be broadly joinable by link.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kumadun/skills/book-google-meet)
- [Publisher profile](https://clawhub.ai/user/kumadun)
- [Google Calendar API](https://developers.google.com/calendar/api/v3/reference)
- [Google Meet API](https://developers.google.com/workspace/meet/api/reference/rest)
- [Meet spaces.get](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/get)
- [Meet spaces.patch](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/patch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output with Google Meet and Google Calendar links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Google OAuth credentials and writes an OAuth token cache file.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
