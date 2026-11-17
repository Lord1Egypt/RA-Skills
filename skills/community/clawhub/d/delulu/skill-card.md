## Description:

DELULU helps agents install and operate an AI dating assistant that matches profiles, manages dating context, replies to unread messages, posts updates, likes posts, and comments on behalf of the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahray](https://clawhub.ai/user/ahray)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to configure and run an AI dating assistant for match search, profile context management, unread-message replies, and scheduled social interactions on the OpenDelulu service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive dating, contact, preference, chat, and token data under the user's Delulu configuration directory.

Mitigation: Install only if comfortable with that local data storage; delete Delulu local data and revoke tokens when discontinuing use.

Risk: The skill can enable recurring messages, posts, likes, and comments on the user's behalf with unclear consent boundaries.

Mitigation: Do not enable automatic dating tasks unless the user understands the schedules and account actions; review or disable scheduled tasks when they are no longer wanted.

Risk: Dating profile and chat automation can expose private information if generated replies are not reviewed carefully.

Mitigation: Keep privacy protections in place and avoid exposing keys, tokens, contact information, chat logs, photos, files, or other private data in replies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahray/skills/delulu)
- [OpenDelulu Home](https://www.opendelulu.com)
- [Install and Login Guide](references/install_login.md)
- [Heartbeat Scheduling Guide](references/heartbeat.md)
- [OpenAPI Reference](references/openapi.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional shell commands and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Delulu configuration, profile, search preference, match, chat, and posting-history files when installed and used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
