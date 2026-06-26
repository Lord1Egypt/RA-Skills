## Description: <br>
Provides a structured CatLab data analysis workflow for querying collections, aggregating statistics, and presenting verified business data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Beelkic](https://clawhub.ai/user/Beelkic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CatLab operators and analysts use this skill to guide an agent through safe, accurate data queries, statistical summaries, trend analysis, and business-data comparisons. It emphasizes inspecting collection structure first, using database-side aggregation, and presenting readable results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide analysis over sensitive private-message and wallet-related collections. <br>
Mitigation: Install it only with read-only, least-privilege database tools limited to data the user is allowed to analyze, and rely on tool-side audit logs and access controls. <br>
Risk: Incorrect assumptions about collection fields or business logic could produce misleading results. <br>
Mitigation: Inspect collection samples before complex queries and base responses only on real query results. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown responses with tables, lists, and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses real database results, defaults to limited result sets, and avoids raw document dumps unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
