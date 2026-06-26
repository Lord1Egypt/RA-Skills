## Description: <br>
Bohrium LKM via open.bohrium.com helps agents search scientific knowledge graphs, verify scientific claims with evidence, query variable relationships, and perform batch paper OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to call Bohrium LKM endpoints for scientific knowledge graph search, claim evidence matching, variable relationship lookup, and structured OCR extraction from papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scientific searches, claims, paper identifiers, and OCR requests are submitted to Bohrium as a third-party service. <br>
Mitigation: Do not submit confidential manuscripts, proprietary hypotheses, regulated data, or restricted/licensed documents unless approved and covered by appropriate data handling terms. <br>
Risk: The skill requires a sensitive Bohrium access key. <br>
Mitigation: Store ACCESS_KEY in an approved secret manager or environment variable and avoid placing it in prompts, logs, source files, or shared configuration. <br>


## Reference(s): <br>
- [Bohrium LKM API Base Endpoint](https://open.bohrium.com/openapi/v1/lkm) <br>
- [ClawHub Skill Page](https://clawhub.ai/sorrymaker0624/bohrium-lkm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bohrium ACCESS_KEY and sends submitted scientific queries, claims, paper identifiers, and OCR requests to a third-party service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
