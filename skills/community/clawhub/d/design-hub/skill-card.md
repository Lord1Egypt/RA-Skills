## Description:

Create and operate a local Design System Hub that stores multiple design systems, generates entries from screenshots, URLs, or written style descriptions, and exposes browsable documentation, live mocks, copied tokens, DESIGN.md, standalone HTML, and JSON APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofine](https://clawhub.ai/user/yofine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to initialize a local React/Vite design-system hub, add complete systems from visual or written inputs, and export structured design documentation for implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local development server binds to 0.0.0.0 by default and is unauthenticated, which can expose hub contents to other reachable machines.

Mitigation: Bind the server to 127.0.0.1 unless LAN access is intentional, and avoid adding sensitive screenshots or proprietary briefs until server exposure is constrained.

Risk: The bundled template does not include a reviewed lockfile, so dependency resolution may vary across installs.

Mitigation: Add and review a package-lock.json for releases, then use npm ci for reproducible installation.

## Reference(s):

- [Design System Hub on ClawHub](https://clawhub.ai/yofine/skills/design-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated or edited project files, JSON API data, standalone HTML, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local React/Vite service with design-system data, dedicated live mock files, export endpoints, and validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
