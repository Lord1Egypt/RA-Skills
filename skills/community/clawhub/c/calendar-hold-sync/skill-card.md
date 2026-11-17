## Description:

Sync one or more source Google calendars into private Busy hold events in one or more target calendars using gog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tdewitt](https://clawhub.ai/user/tdewitt)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to implement and operate config-driven Google Calendar hold mirroring that prevents double-booking across accounts while supporting dry runs, backfill, reconciliation, and polling-based watch mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source event titles and identifiers may be copied into target calendar descriptions.

Mitigation: Use the skill only when this metadata sharing fits the calendar sharing model; prefer dedicated target calendars where possible.

Risk: The sync can create, update, or delete managed hold events.

Mitigation: Start with dryRun enabled, keep maxChangesPerRun conservative, and test mappings before normal operation.

Risk: Custom gog command overrides can change command behavior.

Mitigation: Leave custom gog command overrides disabled unless the config has been fully audited.

## Reference(s):

- [Calendar Hold Sync on ClawHub](https://clawhub.ai/tdewitt/skills/calendar-hold-sync)
- [gog CLI Homepage](https://gogcli.sh/)
- [gog CLI Source](https://github.com/steipete/gogcli)
- [Referenced gog Skill](https://clawhub.ai/steipete/gog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON configuration, and implementation-oriented code instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-hosted calendar sync implementation guidance; users supply their own accounts, calendar IDs, OAuth setup, and runtime configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
