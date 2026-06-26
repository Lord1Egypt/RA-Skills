## Description: <br>
Searches the DugganUSA public index of DOJ-released Jeffrey Epstein documents by name, topic, location, or keyword and returns document previews, entity metadata, source references, and direct DOJ PDF links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChuXo](https://clawhub.ai/user/ChuXo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, researchers, and external users can search public DOJ Epstein records from an agent workflow, inspect structured result metadata, and retrieve direct source-document links for verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the third-party DugganUSA API. <br>
Mitigation: Avoid confidential or legally sensitive searches unless sharing those terms with DugganUSA is acceptable. <br>
Risk: Results may mention sensitive allegations about people and may be incomplete or misleading without source context. <br>
Mitigation: Verify results against official DOJ source documents before sharing, citing, or acting on them. <br>
Risk: The search tool depends on external network availability and DugganUSA API responses. <br>
Mitigation: Treat API errors or empty responses as operational limitations and retry later or consult the DOJ records directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChuXo/epstein) <br>
- [Project Einstein homepage](https://emc2ai.io) <br>
- [DOJ Epstein Records](https://www.justice.gov/epstein) <br>
- [DugganUSA Analytics](https://analytics.dugganusa.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON search or stats output with human-readable status text and PDF quick links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requires a query and supports a result limit from 1 to 500; stats output reports index size, document count, update state, and indexing status.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
