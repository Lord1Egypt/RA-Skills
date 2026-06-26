## Description: <br>
Use local All Routes APIs, repo-backed handlers, and optional local MCP for airport, airline, route-map, timetable-context, and dataset-health lookups without hosted credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and route-planning users use this skill to answer airport, airline, route-map, timetable-context, and dataset-health questions from local APIs, local MCP, or repo-backed code inspection without hosted All Routes credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route answers can be misleading when local services are unavailable or when results come from code inspection rather than live endpoint output. <br>
Mitigation: Label each answer as local API, local MCP, or offline code inspection output, and avoid presenting code-backed reasoning as a live lookup. <br>
Risk: Natural-language city, airport, airline, alliance, or region terms can be ambiguous or unsupported by a local endpoint. <br>
Mitigation: Normalize aliases before endpoint selection, ask one concise clarification question when ambiguity remains, and state unsupported filters as visible limitations. <br>
Risk: Hosted credentials, deployment hostnames, or third-party route sites could be used unnecessarily. <br>
Mitigation: Prefer local web APIs and localhost MCP, do not require hosted All Routes credentials, avoid disclosing non-approved hostnames, and do not scrape third-party route sites when local data can answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skylinehk/all-routes-offline) <br>
- [README](artifact/README.md) <br>
- [Local Surfaces](artifact/references/local-surfaces.md) <br>
- [Query Normalization](artifact/references/query-normalization.md) <br>
- [Filter Intelligence](artifact/references/filter-intelligence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with optional local API, MCP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should label whether answers come from local APIs, local MCP, or offline code inspection and should keep unsupported filters visible.] <br>

## Skill Version(s): <br>
1.3.24 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
