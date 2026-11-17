## Description:

Lade den Abfallkalender fuer den Landkreis Ravensburg ueber die offizielle Athos-Webseite herunter. Verwende diesen Skill, wenn du fuer Orte wie Ravensburg, Weingarten, Wangen im Allgaeu usw. anhand von Ort, Strasse und Hausnummer einen PDF- oder ICS-Abfallkalender holen sollst.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolf128058](https://clawhub.ai/user/wolf128058)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve address-specific waste collection calendars for the Ravensburg district in Germany as ICS or PDF files. Agents should prefer ICS output when they need structured calendar data for downstream scheduling or integration.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: The downloader may write to a server-provided filename when no explicit output path is supplied.

Mitigation: Run it with an explicit --output path in a dedicated directory and review the destination before use.

Risk: Address-specific calendar data can be retained in the local cache.

Mitigation: Use --no-cache when local retention is not desired, or set --cache-dir to a controlled location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wolf128058/skills/abfallkalender-rv)
- [Publisher profile](https://clawhub.ai/user/wolf128058)
- [Landkreis Ravensburg Athos online services](https://athos-onlinedienste.rv.de/)
- [OpenClaw](https://openclaw.com/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands; downloader output is an ICS or PDF file path plus status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads may use an address-bound local cache under ~/.cache/abfallkalender-rv unless --no-cache is used.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
