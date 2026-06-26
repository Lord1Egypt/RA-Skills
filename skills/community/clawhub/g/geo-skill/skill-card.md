## Description: <br>
Geo Skill helps agents prepare generative engine optimization materials for industrial parks, including llms.txt content, JSON-LD schema templates, AI-friendly content plans, and monitoring report drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, operations, and developer teams use this skill to structure industrial park information so AI systems can parse official details, generate optimization assets, and draft monitoring or diagnostic reports. It is most useful as a template and content-production aid rather than as a validated live monitoring system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic and monitoring scripts can produce misleading reports because the security evidence says they are not a trustworthy live diagnostic or monitoring system unless completed and validated. <br>
Mitigation: Use the scripts as template aids only until their checks, data sources, and scoring logic are reviewed and validated against real park websites and AI search workflows. <br>
Risk: Data-handling guidance is under-scoped for consultation records, phone logs, forms, or user feedback. <br>
Mitigation: Publish only official business contact information, avoid personal employee details, and define privacy controls for any collected records or feedback before using the templates. <br>
Risk: Generated marketing and GEO materials may overstate park availability, rankings, or AI visibility if placeholders or simulated monitoring output are treated as facts. <br>
Mitigation: Require human review against official park sources, dated evidence, and current operational data before distributing generated content or reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangm-a3/geo-skill) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [clawhub.yaml](artifact/clawhub.yaml) <br>
- [llms.txt template](artifact/templates/llms.txt) <br>
- [Organization schema template](artifact/templates/schema/organization.json) <br>
- [Product schema template](artifact/templates/schema/product.json) <br>
- [Event schema template](artifact/templates/schema/event.json) <br>
- [Question graph template](artifact/templates/content/question_graph.md) <br>
- [Monitoring report template](artifact/templates/monitoring/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, plain-text llms.txt content, JSON-LD schema snippets, Python command examples, and generated report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-supplied park details and should be reviewed for factual accuracy, current contact information, and privacy controls before publication.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub server release metadata, released 2026-05-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
