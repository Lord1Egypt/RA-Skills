## Description: <br>
API Hunter searches for free API providers that match a requested capability and returns a concise report of candidate services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryyehai](https://clawhub.ai/user/terryyehai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover API providers for a requested feature, with emphasis on free tiers and no-signup options. It is useful for early integration research before selecting and validating a provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results and provider pages can be stale, incomplete, or inaccurate about pricing, signup requirements, and API key availability. <br>
Mitigation: Verify shortlisted providers against their current official documentation before using them in production workflows. <br>
Risk: The skill makes HTTP requests to a local search service and to discovered provider URLs. <br>
Mitigation: Run it in a trusted environment, review outbound network behavior, and avoid submitting sensitive queries unless the search endpoint is approved for that data. <br>


## Reference(s): <br>
- [API Hunter ClawHub page](https://clawhub.ai/terryyehai/api-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/terryyehai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with links, tables, and short code or command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the configured local search endpoint and the availability of external provider pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
