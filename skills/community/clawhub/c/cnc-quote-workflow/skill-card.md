## Description: <br>
CNC intelligent quotation workflow that parses manufacturing requests, retrieves comparable cases, assesses risk, and generates a transparent quote report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing, sourcing, and engineering users can use this workflow to turn CNC part descriptions into structured quote inputs, retrieved case context, risk warnings, and a human-reviewable quote report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quote requests and generated reports may contain customer, proprietary, or commercially sensitive part data. <br>
Mitigation: Treat logs, workflow results, and reports as sensitive; avoid sending real customer data until storage and retention controls are reviewed. <br>
Risk: Email and calendar notification behavior is declared but underspecified. <br>
Mitigation: Disable notifications or tightly scope destinations and permissions until the notification path is explicitly reviewed. <br>
Risk: Optional UniSkill/local-code integration can expand the trusted execution surface if enabled. <br>
Mitigation: Keep UniSkill disabled unless the local code path and dependency source are trusted and reviewed. <br>


## Reference(s): <br>
- [CNC Quote Workflow on ClawHub](https://clawhub.ai/timo2026/cnc-quote-workflow) <br>
- [Related CNC Quote Skill](https://clawhub.com/timo2026/cnc-quote-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown quote report with structured pricing, risk, competitor comparison, debate log, and approval sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive quote request details in logs or reports; notification outputs should be reviewed before use.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
