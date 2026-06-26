## Description: <br>
Paid client skill for calling the Esri Workflow Smell Detector endpoint via x402 on Base/USDC and returning a deterministic ArcGIS Pro automation preflight report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danmaps](https://clawhub.ai/user/danmaps) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and GIS automation engineers use this skill to submit an ArcGIS Pro project snapshot to a paid endpoint and receive a preflight risk report before automating with ArcPy, geoprocessing, or ArcGIS Online. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danmaps/esri-smells-consumer) <br>
- [Esri Workflow Smell Detector endpoint](https://api.x402layer.cc/e/esri-smells) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON response with summary, risk_score, issues, flags, version, and requestHash fields, plus helper command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Base wallet private key and wallet address; uploads the provided project snapshot to the configured endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
