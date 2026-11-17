## Description:

Coordinates embroidery digitizing jobs between BaconCo's Odoo records and an outside digitizer, then files returned designs and updates job records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

BaconCo operations staff and their agents use this skill to submit eligible embroidery artwork for digitizing, track outsourcing in Odoo, and receive and archive finished files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented manifest-writing shell pattern can execute crafted job metadata.

Mitigation: Before use, replace it with a JSON serializer or a non-expanding heredoc with separately serialized values.

Risk: Odoo access and vendor submissions can expose job data or send work unintentionally.

Mitigation: Use a least-privilege Odoo token, test on staging, and confirm each vendor submission before changing Odoo state.

Risk: Persistent job archives can retain customer artwork and related information indefinitely.

Mitigation: Set access controls and a retention policy for archived job files.

## Reference(s):

- [Digitizing outsourcing routine details](references/routine.md)
- [ClawHub skill release](https://clawhub.ai/zmtucker/skills/drivethru-digitize-outsourcing)
- [Odoo](https://www.odoo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown status summaries and archived vendor files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports submitted and pending jobs; updates Odoo records and retains returned design files in a persistent job archive.]

## Skill Version(s):

0.5.3 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
