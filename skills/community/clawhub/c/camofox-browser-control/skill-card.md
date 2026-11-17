## Description:

Control a standalone camofox-browser server over its REST API, especially when a local or remote service is already running on port 9377. Use for opening tabs, navigating, snapshotting pages, clicking refs, typing into forms, pressing keys, scrolling, exporting storage state, importing cookies, or debugging browser automation against camofox-browser/Camoufox behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate a standalone camofox-browser server through REST endpoints for tab management, navigation, page snapshots, form input, session cookies, and storage state workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-session cookies and storage_state exports can contain login credentials.

Mitigation: Treat cookies and storage_state as credentials and use the skill only against a camofox-browser server you control.

Risk: The evaluate endpoint can run scripts in an active browser page.

Mitigation: Avoid /evaluate on sensitive authenticated pages unless explicitly necessary; keep expressions small and targeted.

Risk: Browser automation can affect authenticated sessions or remote pages without enough scoping.

Mitigation: Install and run the skill only for intentional high-trust browser automation and keep --base pointed at a known server.

## Reference(s):

- [camofox-browser API cheatsheet](references/api-cheatsheet.md)
- [Camofox Browser Control on ClawHub](https://clawhub.ai/lotfinity/skills/camofox-browser-control)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with JSON request examples and Python helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser-control guidance and helper CLI/API calls; actions should be verified with fresh page snapshots.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
