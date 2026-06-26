## Description: <br>
Search and retrieve Japanese government statistics (人口, GDP, CPI, 貿易, 雇用) from e-Stat API — Japan's official open data portal with 3,000+ statistical tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to search Japanese government statistics and retrieve e-Stat tables for population, CPI, GDP, trade, and labor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the third-party estat-mcp Python package, and an unpinned uv install may fetch a package version different from this skill release. <br>
Mitigation: Install only if the estat-mcp package is trusted, and pin or review the package version before use in controlled environments. <br>
Risk: The skill requires an ESTAT_APP_ID credential in the runtime environment. <br>
Mitigation: Use a service-specific e-Stat app ID and avoid placing unrelated secrets in the same environment. <br>
Risk: The e-Stat API is documented by the artifact as rate limited to 1 request per second. <br>
Mitigation: Throttle automated workflows to respect the 1 request per second limit. <br>


## Reference(s): <br>
- [e-Stat API key registration](https://www.e-stat.go.jp/api/api-info/use-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output from the estat-mcp CLI when users request programmatic data retrieval.] <br>

## Skill Version(s): <br>
0.2.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
