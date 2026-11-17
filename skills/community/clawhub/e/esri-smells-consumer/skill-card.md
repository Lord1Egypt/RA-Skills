## Description:

Paid client skill for Esri Workflow Smell Detector via x402 (Base/USDC), used to run a deterministic automation preflight scan on an ArcGIS Pro project snapshot by calling the paid endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danmaps](https://clawhub.ai/user/danmaps)

### License/Terms of Use:


## Use Case:

Developers and GIS automation engineers use this skill to call a paid Esri workflow smell detection endpoint for preflight risk analysis before proceeding with ArcPy, geoprocessing, or ArcGIS Online automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can sign a USDC payment for a server-selected amount and recipient without enforcing the advertised price or asking for confirmation.

Mitigation: Use only a dedicated wallet with very limited USDC, verify the endpoint and payment recipient, and avoid running the helper until it enforces a strict maximum payment and confirms terms before signing.

Risk: The project snapshot is uploaded to a paid external endpoint for analysis.

Mitigation: Sanitize the project snapshot before upload and avoid including raw, sensitive, or unnecessary project data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danmaps/skills/esri-smells-consumer)
- [Esri Smell Detector endpoint](https://api.x402layer.cc/e/esri-smells)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Analysis]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project_snapshot JSON file, Base/USDC wallet credentials, and a paid x402 request; the helper prints the JSON response or endpoint error status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
