## Description: <br>
Extracts the first available post text from a user-provided Facebook URL using simple server-side HTML fetching and parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duylori](https://clawhub.ai/user/duylori) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch a public Facebook page or post URL and extract the first readable static post text for lightweight review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs outbound web requests to user-provided URLs. <br>
Mitigation: Install only where outbound requests are acceptable and provide only URLs the agent is intended to fetch. <br>
Risk: Dynamic pages, login-gated pages, or JavaScript-rendered content may not return the intended post text. <br>
Mitigation: Treat extraction failures or sparse output as expected limitations and verify important content against the source page. <br>
Risk: Dependency versions are not pinned in the artifact. <br>
Mitigation: Pin reviewed versions of requests and beautifulsoup4 before production or sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duylori/facenot) <br>
- [queries.md](artifact/references/queries.md) <br>
- [schema.md](artifact/references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object printed to stdout with status and content fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound network access to the user-provided URL and works only when readable static HTML is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
