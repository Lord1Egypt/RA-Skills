## Description: <br>
Check URL health status, including HTTP response code, redirect outcome, broken links, and server errors, using Python standard library networking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site maintainers, and content operators use this skill to check whether a URL is reachable, inspect HTTP status results, and identify broken links or server-side errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound HTTP requests to user-supplied URLs, which may expose sensitive internal endpoints if used carelessly. <br>
Mitigation: Review target URLs before execution and avoid checking private, credential-bearing, or internal-only endpoints unless the environment is approved for that use. <br>
Risk: HTTP status and error output can be transient or misleading because remote servers, redirects, and network conditions change. <br>
Mitigation: Treat results as point-in-time diagnostics and re-run checks before making operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/freedompixels/cn-url-health-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The URL checker returns status, final_url when available, redirect metadata placeholder, and error text when a request fails.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata; artifact/SKILL.md frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
