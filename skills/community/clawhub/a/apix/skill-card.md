## Description: <br>
Use `apix` to search, browse, and execute API endpoints from local markdown vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dngpng](https://clawhub.ai/user/dngpng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to discover REST API endpoints, inspect request and response schemas, and make API calls directly from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real API calls, including mutating requests against production services. <br>
Mitigation: Review the method, destination, headers, and payload before allowing POST, PUT, PATCH, DELETE, or production API calls. <br>
Risk: API calls may require credentials or tokens that could grant broad access. <br>
Mitigation: Use least-privilege API tokens and avoid exposing credentials in shared logs or outputs. <br>
Risk: The CLI installation path affects local execution trust. <br>
Mitigation: Install apix only from a trusted source and prefer the Homebrew route when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dngpng/apix) <br>
- [apix installer](https://apix.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw markdown returned by apix and HTTP response data from called endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
