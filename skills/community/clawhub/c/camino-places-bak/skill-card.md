## Description:

Locate places using flexible query formats - free-form search or structured address components. Returns coordinates, addresses, and optional street-level photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valvoc](https://clawhub.ai/user/valvoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to look up named places or geocode structured addresses through Camino, returning coordinates, formatted addresses, and optional street-level imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Place searches and addresses are sent to Camino.

Mitigation: Avoid submitting sensitive addresses or personal data unless the deployment has approved that data sharing.

Risk: CAMINO_API_KEY grants access to the Camino API.

Mitigation: Store the key only in trusted agent settings and avoid exposing it in prompts, logs, or shared files.

Risk: Mutable or unpinned installs can change the reviewed skill behavior.

Mitigation: Prefer a pinned or reviewed ClawHub version rather than @latest or an unpinned GitHub URL.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/valvoc/skills/camino-places-bak)
- [ClawHub publisher profile](https://clawhub.ai/user/valvoc)
- [Camino search API endpoint](https://api.getcamino.ai/search)
- [Camino skill activation](https://app.getcamino.ai/skills/activate)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY and the curl and jq command-line tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
